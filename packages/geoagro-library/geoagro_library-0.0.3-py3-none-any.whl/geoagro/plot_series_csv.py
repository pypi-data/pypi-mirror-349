import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import re

def extract_date_from_tif(file_name):
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

def get_band_dates(polygon_id, base_dir):
    """
    Obtiene las fechas correspondientes a cada banda del stack NDVI a partir de 
    los archivos en la carpeta RECORTES.
    
    Parámetros:
    polygon_id: ID del polígono
    base_dir: Directorio base donde se encuentran las carpetas de los polígonos
    
    Retorna:
    list: Lista de fechas ordenadas correspondientes a cada banda
    """
    # Construir la ruta a la carpeta RECORTES
    recortes_path = os.path.join(base_dir, str(polygon_id), "RECORTES")
    
    # Verificar si existe la carpeta
    if not os.path.exists(recortes_path):
        print(f"{recortes_path}")
        print(f"No se encontró la carpeta RECORTES para el polígono {polygon_id}")
        return None
    
    # Obtener todos los archivos .tif en la carpeta RECORTES
    tif_files = list(Path(recortes_path).glob("*.tif"))
    
    # Extraer fechas y ordenar los archivos por fecha
    dates = [extract_date_from_tif(tif.name) for tif in tif_files]
    paired_list = [(tif, date) for tif, date in zip(tif_files, dates) if date is not None]
    sorted_pairs = sorted(paired_list, key=lambda x: extract_month_year(x[1]))
    
    # Extraer las fechas ordenadas
    sorted_dates = [date for _, date in sorted_pairs]
    
    return sorted_dates

def plot_ndvi_timeseries_from_csv(csv_path, polygon_id=None, base_dir=None, sample_size=None, 
                                include_mean=True, include_std=True):
    """
    Genera gráficos de líneas de tiempo de NDVI para un polígono específico a partir del CSV.
    
    Parámetros:
    csv_path: Ruta al archivo CSV con los datos vectorizados
    polygon_id: ID del polígono para el cual generar las líneas de tiempo
    base_dir: Directorio base para buscar las fechas de las bandas (opcional)
    sample_size: Número de píxeles a mostrar (si None, muestra todos los píxeles)
    include_mean: Si se debe incluir la línea de tiempo media
    include_std: Si se debe incluir la desviación estándar
    
    Retorna:
    None
    """
    # Cargar los datos del CSV
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"Error al cargar el archivo CSV: {e}")
        return
    
    if polygon_id is None:
        polygon_ids = df['polygon_fid'].unique()
    else:
        polygon_ids= [polygon_id]

    plt.figure(figsize=(14, 8))
    colors = plt.cm.tab10.colors

    for idx, pid in enumerate(polygon_ids):
        polygon_df = df[df['polygon_fid']==pid]

        num_firmas = len(polygon_df)

        if len(polygon_df) == 0:
            print(f"No se encontraron datos para el poligono {pid} en el CSV") 
            continue
    
        # Identificar columnas de bandas
        band_columns = [col for col in polygon_df.columns if col.startswith('band_')]
        num_bands = len(band_columns)
    
        if num_bands == 0:
            print(f"No se encontraron columnas de banda en el CSV")
            return
    
        # Obtener fechas si base_dir existe
        dates = None
        if base_dir:
            dates = get_band_dates(polygon_id, base_dir)
            print(f"{len(dates), num_bands}")
    
        # Si no hay fechas, usar índices numéricos
        if not dates or len(dates) != num_bands:
            print("No se pudieron obtener fechas para las bandas. Usando índices numéricos.")
            dates = [f"Banda {i+1}" for i in range(num_bands)]
    
        # Muestrear píxeles si se especifica sample_size
        if sample_size and sample_size < len(polygon_df):
            sampled_df = polygon_df.sample(n=sample_size, random_state=42)
        else:
            sampled_df = polygon_df
    
        # Graficar cada píxel como una línea de tiempo
        for _, row in sampled_df.iterrows():
            values = [row[band] for band in band_columns]
            plt.plot(range(num_bands), values, color=colors[idx % len(colors)], alpha=0.3, linewidth=0.5)
    
        # Calcular y graficar la media y desviación estándar si se solicita
        if include_mean or include_std:
            mean_values = [polygon_df[band].mean() for band in band_columns]
        
            if include_mean:
                plt.plot(range(num_bands), mean_values, color=colors[idx % len(colors)], linewidth=3, label=f'Media (Polígono {pid})')
        
            if include_std:
                std_values = [polygon_df[band].std() for band in band_columns]
                plt.fill_between(
                    range(num_bands),
                    [m - s for m, s in zip(mean_values, std_values)],
                    [m + s for m, s in zip(mean_values, std_values)],
                    color=colors[idx % len(colors)], alpha=0.2, label=f'Desviación estándar (Polígono {pid})'
                )
    
        # Configurar el gráfico
        plt.title('Evolución temporal del NDVI para todos los polígonos' if polygon_id is None else f'Evolución temporal del NDVI para el polígono {polygon_id}')
        plt.ylabel('NDVI')
        plt.xlabel('Fecha')
        plt.ylim(-0.05, 1.05)  # NDVI generalmente está entre -1 y 1
        plt.grid(True, linestyle='--', alpha=0.7)
    
        # Configurar las etiquetas del eje X
        plt.xticks(range(num_bands), dates, rotation=45, ha='right')

        plt.text(0.95, 0.95, f"Firmas: {num_firmas}", fontsize=12, color='white', fontweight="bold", bbox=dict(facecolor="darkblue", alpha=0.6, edgecolor='none', boxstyle='round'), transform=plt.gca().transAxes, ha='right', va='top')
    
        # Añadir leyenda si corresponde
        if include_mean or include_std:
            plt.legend()
    
        # Ajustar la disposición
        plt.tight_layout()
        
        # Mostrar la figura en una ventana emergente
        plt.show()

if __name__ == "__main__":
    # Ruta al CSV con los datos vectorizados
    csv_path = "/home/agrosavia/Documents/rs_agrosavia/DATA_CUBE_AGROSAVIA/ROI/GIS_FEDEPANELA/8.CSV_ALL/669_chipata_all_polygons_clusters.csv"
    
    # Directorio base donde se encuentran las carpetas de los polígonos
    base_dir = "/home/agrosavia/Documents/rs_agrosavia/DATA_CUBE_AGROSAVIA/ROI/GIS_FEDEPANELA/5.RECORTES/669_chipata" # Agregar bien este parametro para que se agreguen las fechas correspondientes
    
    #polygon_id = None
    polygon_id = 1405.0

    plot_ndvi_timeseries_from_csv(
        csv_path=csv_path,
        polygon_id=polygon_id,
        base_dir=base_dir,
        sample_size=None # El número de pixeles que se grafican por polígono, dejar en None si se quieren visualizar todos los pixeles
        # En caso de dejar un número entero (por ejemplo, 100), se seleccionan aleatoriamente pixeles segun el número de muestra seleccionado 
    )