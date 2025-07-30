import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import os
import re
import numpy as np
from pathlib import Path
from PIL import Image
from osgeo import gdal
import rasterio
from skimage import exposure
import argparse

# Funciones para extraer y ordenar fechas
def extract_date(file_name):
    """
    Extrae la fecha en formato 'MM_YYYY' del nombre del archivo.
    """
    match = re.search(r'\d{2}_\d{4}', str(file_name))
    return match.group(0) if match else None

def extract_month_year(date_str):
    """
    Extrae el año y el mes como enteros a partir de una cadena 'MM_YYYY'.
    """
    if date_str:
        month, year = date_str.split('_')
        return int(year), int(month)
    return None, None

def sort_tif_files(tif_files):
    """
    Ordena los archivos .tif basado en la fecha extraída del nombre.
    """
    return sorted(tif_files, key=lambda x: extract_month_year(extract_date(x.name)))

def create_titled_image(data, title, is_ndvi=False):
    """
    Crea una imagen con título a partir de datos numpy.
    
    Parámetros:
    - data: Array numpy con los datos de la imagen
    - title: Título de la imagen
    - is_ndvi: Si es True, usa colormap RdYlGn y rango 0-1
    
    Retorna:
    - Objeto PIL.Image con la imagen generada
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Configurar visualización
    cmap = 'RdYlGn' if is_ndvi else None
    vmin = 0 if is_ndvi else None
    vmax = 1 if is_ndvi else None
    
    if is_ndvi:
        im = ax.imshow(data, cmap=cmap, vmin=vmin, vmax=vmax)
    else:
        im = ax.imshow(data)
    
    # Configurar título y estilo
    ax.set_title(title, fontsize=12, pad=20)
    ax.axis('off')
    fig.tight_layout()
    
    # Convertir a imagen Pillow
    fig.canvas.draw()
    buf = fig.canvas.buffer_rgba()
    width, height = fig.canvas.get_width_height()
    img = Image.frombytes('RGBA', (width, height), buf).convert('RGB')
    
    plt.close(fig)
    return img

def create_polygon_gif(polygon_folder, duration=1000):
    """
    Crea un GIF timelapse para un polígono.
    
    Parámetros:
    - polygon_folder: Ruta a la carpeta del polígono
    - duration: Duración de cada frame en milisegundos
    
    Retorna:
    - Ruta al archivo GIF creado o None si hubo error
    """
    # Configurar rutas
    polygon_path = Path(polygon_folder)
    recortes_folder = polygon_path / "RECORTES"
    gif_folder = polygon_path / "GIF"
    gif_folder.mkdir(parents=True, exist_ok=True)
    output_gif = gif_folder / f"{polygon_path.name}_timelapse.gif"

    # Validar estructura
    if not recortes_folder.exists():
        raise FileNotFoundError(f"No existe carpeta RECORTES en {polygon_path}")
    
    # Obtener y ordenar archivos .tif por fecha
    tif_files = list(recortes_folder.glob("*.tif"))
    tif_files = sort_tif_files(tif_files)  # Ordenar por fecha
    
    if not tif_files:
        raise ValueError(f"No hay archivos TIFF en {recortes_folder}")

    # Procesar imágenes
    image_frames = []
    
    for idx, tif_path in enumerate(tif_files):
        try:
            # Procesar NDVI
            ds = gdal.Open(str(tif_path))
            nir = ds.GetRasterBand(4).ReadAsArray().astype(np.float32)
            red = ds.GetRasterBand(3).ReadAsArray().astype(np.float32)
            ndvi = np.nan_to_num((nir - red) / (nir + red), nan=0.0)
            ndvi_norm = (ndvi - ndvi.min()) / (ndvi.max() - ndvi.min() + 1e-9)

            # Procesar RGB
            with rasterio.open(tif_path) as src:
                rgb = np.dstack([src.read(3), src.read(2), src.read(1)])
                rgb_norm = exposure.equalize_adapthist(rgb, clip_limit=0.03)

            # Crear y combinar imágenes
            date_tag = extract_date(tif_path.name)
            title_base = f"{date_tag.replace('_', '/')}"
            
            img_ndvi = create_titled_image(ndvi_norm, f"{title_base}\nNDVI", is_ndvi=True)
            img_rgb = create_titled_image(rgb_norm, f"{title_base}\nRGB")
            
            combined = Image.new('RGB', (img_rgb.width + img_ndvi.width, img_rgb.height))
            combined.paste(img_rgb, (0, 0))
            combined.paste(img_ndvi, (img_rgb.width, 0))
            image_frames.append(combined)

        except Exception as e:
            print(f"Error en archivo {tif_path.name}: {str(e)}")
            continue

    # Guardar GIF
    if image_frames:
        image_frames[0].save(
            output_gif,
            save_all=True,
            append_images=image_frames[1:],
            duration=duration,
            loop=0,
            optimize=True,
            quality=85
        )
        return output_gif
    return None

def process_all_polygons(root_folder, duration=1000):
    """
    Procesa todas las carpetas de polígonos dentro de un directorio raíz.
    
    Parámetros:
    - root_folder: Ruta contenedora de todas las carpetas de polígonos
    - duration: Duración de cada frame en milisegundos
    """
    root_path = Path(root_folder)
    
    if not root_path.exists():
        raise FileNotFoundError(f"El directorio raíz no existe: {root_folder}")
    
    processed = 0
    errors = 0
    
    for polygon_folder in root_path.iterdir():
        if polygon_folder.is_dir():
            try:
                print(f"\n{'='*50}")
                print(f"Procesando polígono: {polygon_folder.name}")
                
                # Crear GIF para el polígono
                gif_path = create_polygon_gif(polygon_folder, duration)
                
                if gif_path:
                    print(f"GIF generado con éxito: {gif_path}")
                    processed += 1
                else:
                    errors += 1
                    
            except Exception as e:
                print(f"Error procesando {polygon_folder.name}: {str(e)}")
                errors += 1
                continue

    print(f"\n{'='*50}")
    print(f"Proceso completado")
    print(f"Polígonos procesados: {processed}")
    print(f"Errores: {errors}")
    print(f"Total carpetas: {processed + errors}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generar GIFs temporales para múltiples polígonos')
    parser.add_argument('root_folder', help='Carpeta raíz conteniendo todas las carpetas de polígonos')
    parser.add_argument('--duration', type=int, default=1000, help='Duración por frame en milisegundos')
    
    args = parser.parse_args()
    
    try:
        process_all_polygons(args.root_folder, args.duration)
    except Exception as e:
        print(f"Error general: {str(e)}")

        

