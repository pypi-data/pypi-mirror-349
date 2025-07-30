import os
import re
import shutil
from pathlib import Path

def move_and_rename_tifs(source_folder, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Expresión regular para extraer el mes y el año del nombre de la carpeta
    pattern = re.compile(r'planet_medres_normalized_analytic_(\d{4})-(\d{2})_mosaic')

    # Recorrer las subcarpetas en la carpeta fuente
    for subdir, dirs, files in os.walk(source_folder):
        for dir_name in dirs:
            match = pattern.match(dir_name)
            if match:
                year, month = match.groups()  # Extraer el año y el mes
                folder_path = os.path.join(subdir, dir_name)

                # Buscar archivos .tif en la carpeta
                for file_name in os.listdir(folder_path):
                    if file_name.endswith('.tif'):
                        new_file_name = f"{month}_{year}.tif"
                        old_file_path = os.path.join(folder_path, file_name)
                        new_file_path = os.path.join(destination_folder, new_file_name)

                        # Mover y renombrar el archivo
                        shutil.move(old_file_path, new_file_path)
                        print(f"Renombrado y movido: {old_file_path} a {new_file_path}")

source_folder = Path('/home/agrosavia/Documents/rs_agrosavia/DATA_CUBE_AGROSAVIA/ROI/GIS_FEDEPANELA/RASTER/NICFI/Ocamonte6071060')
destination_folder = Path('/home/agrosavia/Documents/rs_agrosavia/DATA_CUBE_AGROSAVIA/ROI/GIS_FEDEPANELA/4.RASTER_CLEAN/ocamonte')

move_and_rename_tifs(source_folder, destination_folder)