import os
import rasterio
import numpy as np
import pandas as pd
from pathlib import Path

def vectorize_ndvi_stacks_multiband(base_dir, csv_path=None, append=False):
    """
    Vectoriza los stacks de NDVI de múltiples polígonos y guarda los resultados en un CSV.
    Permite agregar los nuevos datos a un CSV existente.
    
    Parámetros:
    base_dir (str): Directorio base donde se encuentran las carpetas de los polígonos
    csv_path (str, opcional): Ruta al archivo CSV donde guardar/agregar los resultados. 
                             Si es None, se usa 'ndvi_vectors_multiband.csv' en el directorio base
    append (bool): Si es True, agrega los datos a un CSV existente en lugar de sobrescribirlo
    
    Retorna:
    str: Ruta al archivo CSV generado o actualizado
    """
    # Lista para almacenar todos los datos vectorizados
    all_data = []
    
    # Recorrer todas las carpetas en el directorio base
    for polygon_dir in os.listdir(base_dir):
        # Verificar si es un directorio válido con un nombre de polígono (debe ser convertible a float)
        try:
            polygon_fid = float(polygon_dir)
            stack_path = os.path.join(base_dir, polygon_dir, "STACK", "stack_ndvi.tif")
            
            # Verificar si existe el archivo stack_ndvi.tif
            if os.path.exists(stack_path):
                print(f"Procesando polígono {polygon_fid}...")
                
                # Abrir el stack con rasterio
                with rasterio.open(stack_path) as src:
                    # Leer todas las bandas
                    stack_data = src.read()
                    
                    # Obtener dimensiones del stack
                    num_bands, height, width = stack_data.shape
                    
                    # Crear máscara para identificar píxeles con información (no cero)
                    mask = np.any(stack_data != 0, axis=0)
                    
                    # Vectorizar solo los píxeles con información
                    pixel_count = 0
                    for y in range(height):
                        for x in range(width):
                            if mask[y, x]:
                                # Extraer el vector para este píxel (todas las bandas)
                                pixel_vector = stack_data[:, y, x]
                                
                                # Crear un registro para este píxel con el identificador del polígono
                                pixel_data = {"polygon_fid": polygon_fid}
                                
                                # Añadir cada banda como una columna separada
                                for band_idx in range(num_bands):
                                    pixel_data[f"band_{band_idx+1}"] = pixel_vector[band_idx]
                                
                                # Añadir las coordenadas del píxel
                                pixel_data["pixel_x"] = x
                                pixel_data["pixel_y"] = y
                                
                                # Añadir este registro a la lista
                                all_data.append(pixel_data)
                                pixel_count += 1
                
                print(f"  - {pixel_count} píxeles procesados para el polígono {polygon_fid}")
            else:
                print(f"No se encontró el archivo stack_ndvi.tif para el polígono {polygon_fid}")
                
        except ValueError:
            # Si el nombre de la carpeta no es un número, ignorarla
            continue
    
    # Definir la ruta del CSV si no se proporcionó
    if csv_path is None:
        csv_path = os.path.join(base_dir, "ndvi_vectors_multiband.csv")
    
    # Crear el DataFrame para el CSV
    if all_data:
        new_df = pd.DataFrame(all_data)
        
        if append and os.path.exists(csv_path):
            # Leer el CSV existente y agregar los nuevos datos
            try:
                existing_df = pd.read_csv(csv_path)
                # Verificar si las columnas coinciden
                if set(existing_df.columns) == set(new_df.columns):
                    # Combinar los DataFrames
                    combined_df = pd.concat([existing_df, new_df], ignore_index=True)
                    combined_df.to_csv(csv_path, index=False)
                    print(f"\nDatos agregados al archivo CSV existente: {csv_path}")
                    print(f"  - Registros anteriores: {len(existing_df)}")
                    print(f"  - Nuevos registros: {len(new_df)}")
                    print(f"  - Total registros: {len(combined_df)}")
                else:
                    print(f"Error: Las columnas del CSV existente no coinciden con los nuevos datos.")
                    print(f"  - Columnas existentes: {sorted(existing_df.columns)}")
                    print(f"  - Columnas nuevas: {sorted(new_df.columns)}")
                    
                    # Intentar hacer una unión basada en columnas comunes
                    common_columns = set(existing_df.columns).intersection(set(new_df.columns))
                    if len(common_columns) > 0 and "polygon_fid" in common_columns:
                        print(f"Intentando unir basándose en {len(common_columns)} columnas comunes...")
                        # Crear un backup del archivo original
                        backup_path = csv_path + ".backup"
                        existing_df.to_csv(backup_path, index=False)
                        print(f"  - Se ha creado una copia de seguridad en: {backup_path}")
                        
                        # Guardar el nuevo DataFrame en un archivo separado
                        new_csv_path = csv_path.replace(".csv", "_new.csv")
                        new_df.to_csv(new_csv_path, index=False)
                        print(f"  - Los nuevos datos se han guardado en: {new_csv_path}")
                        
                        return new_csv_path
            except Exception as e:
                print(f"Error al intentar agregar al CSV existente: {e}")
                print(f"Creando un nuevo archivo CSV...")
                new_df.to_csv(csv_path, index=False)
                print(f"\nNuevo archivo CSV guardado en: {csv_path}")
        else:
            # Crear un nuevo CSV o sobrescribir el existente
            new_df.to_csv(csv_path, index=False)
            print(f"\nArchivo CSV guardado en: {csv_path}")
            print(f"  - Total registros: {len(new_df)}")
        
        return csv_path
    else:
        print("No se encontraron píxeles con información en ningún polígono")
        return None

# Ejemplo de uso con múltiples directorios:
if __name__ == "__main__":
    # Lista de directorios base para procesar (puedes agregar más)
    directories = [
        "/home/agrosavia/Documents/rs_agrosavia/DATA_CUBE_AGROSAVIA/ROI/GIS_FEDEPANELA/5.RECORTES/2023_2024/Santana606_1057/RECORTES/",
        # Añadir aquí otros directorios para procesar
        # "/home/documents/Geo_Agro/for_real_2/",
        # "/home/documents/Geo_Agro/for_real_3/",
    ]
    
    # Ruta al CSV final donde se guardarán todos los datos
    final_csv = "/home/agrosavia/Documents/rs_agrosavia/DATA_CUBE_AGROSAVIA/ROI/GIS_FEDEPANELA/8.CSV_ALL/2023_2024/Santana606_1057/ndvi/CSV_ALL.csv"
    
    # Procesar cada directorio y agregar al mismo CSV
    for i, base_directory in enumerate(directories):
        print(f"\nProcesando directorio {i+1}/{len(directories)}: {base_directory}")
        # Para el primer directorio, no usamos append. Para los siguientes, sí.
        append_mode = (i > 0)
        vectorize_ndvi_stacks_multiband(
            base_directory, 
            csv_path=final_csv, 
            append=append_mode
        )
    
    print("\nProcesamiento completo. Todos los polígonos han sido vectorizados y guardados en un solo CSV.")