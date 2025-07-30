import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import os
import re
import rasterio 

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

def visualize_bands(stacked_array, tif_files):
    """
    Visualiza las bandas de un archivo GeoTIFF apilado.

    Parámetros:
    - stacked_array: Ruta al archivo GeoTIFF apilado.
    - tif_files: Lista de rutas a los archivos .tif individuales.
    """
    # Cargar el archivo GeoTIFF apilado
    with rasterio.open(stacked_array) as src:
        stacked_data = src.read()  
        stacked_data = np.moveaxis(stacked_data, 0, -1)  

    tif_files.sort(key=lambda x: extract_month_year(extract_date(x.name)))

    # Verificar que el número de bandas coincida con el número de archivos .tif
    bands = stacked_data.shape[2]
    if bands != len(tif_files):
        raise ValueError(f"El número de bandas en el archivo apilado ({bands}) no coincide con el número de archivos .tif ({len(tif_files)}).")

    # Configurar la visualización
    columns = 8
    rows = int(np.ceil(bands / columns))
    plt.figure(figsize=(14, rows * 2))

    # Visualizar cada banda
    for i in range(bands):
        plt.subplot(rows, columns, i + 1)
        plt.imshow(stacked_data[:, :, i], cmap="RdYlGn", vmin=0, vmax=1)
        title = os.path.basename(tif_files[i].stem)
        plt.title(title, fontsize=12)
        plt.axis('off')

    plt.tight_layout()
    plt.show()

# Rutas de los archivos

stacked_array = "/home/agrosavia/Documents/rs_agrosavia/DATA_CUBE_AGROSAVIA/ROI/GIS_FEDEPANELA/5.RECORTES/464_moniquira/1687.0/STACK/stack_ndvi.tif"


tif_files = list(Path("/home/agrosavia/Documents/rs_agrosavia/DATA_CUBE_AGROSAVIA/ROI/GIS_FEDEPANELA/5.RECORTES/464_moniquira/1687.0/RECORTES").glob("*.tif"))

visualize_bands(stacked_array, tif_files)