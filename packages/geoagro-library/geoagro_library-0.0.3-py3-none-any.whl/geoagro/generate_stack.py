import os
import re
import numpy as np
from osgeo import gdal
from pathlib import Path

def extract_date(file_name):
    """
    Extrae la fecha en formato 'MM_YYYY' del nombre del archivo.
    """
    match = re.search(r'\d{2}_\d{4}', str(file_name))
    return match.group(0) if match else None

# Función para extraer el mes y el año como enteros
def extract_month_year(date_str):
    """
    Extrae el año y el mes como enteros a partir de una cadena 'MM_YYYY'.
    """
    if date_str:
        month, year = date_str.split('_')
        return int(year), int(month)
    return None, None

def calculate_index(tif_path):
    
    ds = gdal.Open(str(tif_path))
    if ds is None:
        raise ValueError(f"No se pudo abrir el archivo: {tif_path}")
    
    blue = ds.GetRasterBand(1).ReadAsArray().astype(np.float32)
    red = ds.GetRasterBand(3).ReadAsArray().astype(np.float32)
    nir = ds.GetRasterBand(4).ReadAsArray().astype(np.float32)

    ds = None

    valid_mask = (blue != 0.0) & (red != 0.0) & (nir != 0.0)

    ndvi = np.full_like(nir, np.nan)
    evi  = np.full_like(nir, np.nan)
    evi2 = np.full_like(nir, np.nan)

    # NDVI
    ndvi[valid_mask] = (nir[valid_mask] - red[valid_mask]) / (nir[valid_mask] + red[valid_mask] + 1e-9)
    ndvi_min = np.nanmin(ndvi)
    ndvi_max = np.nanmax(ndvi)
    ndvi_norm = (ndvi - ndvi_min) / (ndvi_max - ndvi_min + 1e-9)
    ndvi_norm = np.nan_to_num(ndvi_norm, nan=0.0)

    # EVI
    evi[valid_mask] = 2.5 * (nir[valid_mask] - red[valid_mask]) / (nir[valid_mask] + 6.0 * red[valid_mask] - 7.5 * blue[valid_mask] + 1.0 + 1e-9)
    evi_min = np.nanmin(evi)
    evi_max = np.nanmax(evi)
    evi_norm = (evi - evi_min) / (evi_max - evi_min + 1e-9)
    evi_norm = np.nan_to_num(evi_norm, nan=0.0)

    # EVI2
    evi2[valid_mask] = 2.5 * (nir[valid_mask] - red[valid_mask]) / (nir[valid_mask] + 2.4 * red[valid_mask] + 1.0 + 1e-9)
    evi2_min = np.nanmin(evi2)
    evi2_max = np.nanmax(evi2)
    evi2_norm = (evi2 - evi2_min) / (evi2_max - evi2_min + 1e-9)
    evi2_norm = np.nan_to_num(evi2_norm, nan=0.0)

    return ndvi_norm, evi_norm, evi2_norm

def create_stacks(polygon_folder):
    
    recortes_folder = Path(polygon_folder) / "RECORTES"
    if not recortes_folder.exists():
        raise FileNotFoundError(f"No se encontró la carpeta RECORTES en {polygon_folder}")

    stack_folder = Path(polygon_folder) / "STACK"
    stack_folder.mkdir(parents=True, exist_ok=True)  

    tif_files = list(recortes_folder.glob("*.tif"))
    if not tif_files:
        raise ValueError(f"No hay archivos .tif en {recortes_folder}")

    tif_files.sort(key=lambda x: extract_month_year(extract_date(x.name)))
    
    ndvi_list = []
    evi_list = []
    evi2_list = []

    for tif_path in tif_files:
        ndvi_norm, evi_norm, evi2_norm = calculate_index(tif_path)
        ndvi_list.append(ndvi_norm)
        evi_list.append(evi_norm)
        evi2_list.append(evi2_norm)

    ndvi_stack = np.stack(ndvi_list, axis=0)
    evi_stack  = np.stack(evi_list,  axis=0)
    evi2_stack = np.stack(evi2_list, axis=0)

    save_geotiff(ndvi_stack, tif_files[0], stack_folder / "stack_ndvi.tif")
    save_geotiff(evi_stack,  tif_files[0], stack_folder / "stack_evi.tif")
    save_geotiff(evi2_stack, tif_files[0], stack_folder / "stack_evi2.tif")

def save_geotiff(data, reference_tif, output_path, nodata_value=0.0):
    
    ds = gdal.Open(str(reference_tif))
    if ds is None:
        raise ValueError(f"No se pudo abrir el archivo de referencia: {reference_tif}")

    # Obtener la información geográfica
    rows, cols = data.shape[1], data.shape[2]
    bands = data.shape[0]
    geotransform = ds.GetGeoTransform()
    projection = ds.GetProjection()
    ds=None

    driver = gdal.GetDriverByName("GTiff")
    out_ds = driver.Create(str(output_path), cols, rows, bands, gdal.GDT_Float32)

    out_ds.SetGeoTransform(geotransform)
    out_ds.SetProjection(projection)

    for i in range(bands):
        band = out_ds.GetRasterBand(i + 1)
        band.WriteArray(data[i])
        band.SetNoDataValue(nodata_value)

    out_ds.FlushCache()
    out_ds = None

def main(root_folder):
    
    root_path = Path(root_folder)
    if not root_path.exists():
        raise FileNotFoundError(f"El directorio raíz no existe: {root_folder}")

    # Procesar cada carpeta de polígono
    for polygon_folder in root_path.iterdir():
        if polygon_folder.is_dir():
            try:
                print(f"Procesando polígono: {polygon_folder.name}")
                create_stacks(polygon_folder)
                print(f"Stack de NDVI, EVI y EVI2 generados para {polygon_folder.name}")
            except Exception as e:
                print(f"Error procesando {polygon_folder.name}: {str(e)}")

# Ruta de la carpeta raíz
root_folder = "/home/agrosavia/Documents/rs_agrosavia/DATA_CUBE_AGROSAVIA/ROI/GIS_FEDEPANELA/5.RECORTES/2023_2024/Santana606_1057/RECORTES"  

if __name__ == "__main__":
    main(root_folder)
