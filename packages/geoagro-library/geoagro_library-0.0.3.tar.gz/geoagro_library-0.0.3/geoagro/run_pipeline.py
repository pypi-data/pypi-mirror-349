#!/usr/bin/env python3
import os
import re
import importlib
import sys
import multiprocessing


# ===================================================================
# Configuración de parámetros por módulo.
# Clave: nombre del módulo (sin .py) -> dict de parámetros para la función main()
# Ejemplo:
# PARAMS = {
#     '1_extract': {'input_path': 'data/raw', 'output_path': 'data/processed'},
#     '2_all_clipp': {'threshold': 0.5, 'mode': 'fast'},
# }
# ===================================================================

from pathlib import Path

# --------------------------------------------------
# Definición de rutas base
# --------------------------------------------------
BASE = Path("/home/agrosavia/Documents/rs_agrosavia"
            "/DATA_CUBE_AGROSAVIA/ROI/GIS_FEDEPANELA")
RASTER_CLEAN = BASE / "4.RASTER_CLEAN"
POLYGON_TOWN = BASE / "3.POLYGON_TOWN"
RECORTES = BASE / "5.RECORTES" / "2023_2024"
CSV_ALL = BASE / "8.CSV_ALL" / "2023_2024"
OUTPUT = BASE / "9_output" / "2023_2024"
PROJECT = "Santana606_1057_Prueba"


PARAMS = {
    "1_extract": {
        "source_folder": BASE / "RASTER" / "NICFI",
        "destination_folder": RASTER_CLEAN / PROJECT,
    },
    "2_all_clipp": {
        "source_folder": RASTER_CLEAN / PROJECT / "2023_2024",
        "shape_file": POLYGON_TOWN / "Santana606_1057" / "Santana606_1057.shp",
        "destination_folder": RECORTES / "2023_2024" / PROJECT / "RECORTES", 
    },
    "3_stack": {
        "root_folder": RECORTES / "2023_2024" / PROJECT / "RECORTES",
    },
    "5_2_outliers_IQR": {
        "input_csv": CSV_ALL / PROJECT / "ndvi" / "serie" / "CSV_ALL.csv",
        "output_csv": CSV_ALL / PROJECT / "ndvi" / "serie" / "datos_sin_outliers_IQR.csv"
    },
    "5_2_outliers_IQR": {
        "input_csv": CSV_ALL / PROJECT / "evi" / "serie" / "CSV_ALL.csv",
        "output_csv": CSV_ALL / PROJECT / "evi" / "serie" / "datos_sin_outliers_IQR.csv"
    },

    "5_3_ADF_KPSS": {
        "input_csv": str(CSV_ALL / PROJECT / "ndvi/seasonal/"
                          "datos_sin_outliers_IQR.csv"),
        "output_all_csv": str(CSV_ALL / PROJECT / "ndvi/seasonal/"
                              "datos_resultados_double_validation.csv"),
        "output_clean_csv": str(CSV_ALL / PROJECT / "ndvi/seasonal/"
                               "datos_stationarity.csv"),
        "alpha": 0.05,
        "n_jobs": multiprocessing.cpu_count(),  
    },
    "5_4_seasonal_components":{
        "base_dirs": [
            str(RECORTES / "2023_2024" / PROJECT / "RECORTES")
        ],
        "output_csv": str(CSV_ALL / PROJECT / "evi/seasonal"
                          "CSV_ALL.csv"),
        "append": False,
        "period": 12
    },
    "7_1_cluster_new": {
        "input_csv": str(CSV_ALL / PROJECT / "ndvi/seasonal/CSV_ALL.csv"),
        "n_clusters": 5,
        "output_plot_raw": str(OUTPUT / "grafico_crudos.png"),
        "output_plot_norm": str(OUTPUT / "grafico_normalizados.png"),
    },
    "7_2_cluster_raw": {
        "csv_path": str(CSV_ALL / PROJECT / "ndvi/seasonal/datos_stationarity.csv"),
        "base_tif_folder": str(RECORTES / "2023_2024" / PROJECT / "RECORTES"),
        "output_folder": str(OUTPUT / "2023_2024" / PROJECT / "ndvi/seasonal/rst_stationary"),
        "climate_shp": str(POLYGON_TOWN / "Santana606_1057/Santana606_1057.shp"),
        "climate_start_date": "2020-09-01",
        "climate_end_date": "2025-01-01",
        "climate_freq": "monthly",
        "max_k": 20,
        "polygon_id": None,
    },
    "7_3_fourth_clusters": {
        "csv_path": str(CSV_ALL / PROJECT / "ndvi/serie/CSV_ALL.csv"),
        "output_csv": str(OUTPUT / "all_polygons_cluster_signatures.csv"),
        "output_csv_clusters": str(OUTPUT / "all_polygons_clusters.csv"),
        "n_clusters": 4,
    },
    "7_4_read_fourth_clusters": {
        "csv_path": str(OUTPUT / "all_polygons_cluster_signatures.csv"),
        "polygon_fid": 1405,
    },

    "7_5_cluster_norm": {
        "csv_path": str(BASE / "8.CSV_ALL/464_moniquira_CSV_ALL.csv"),
        "base_tif_folder": str(BASE / "5.RECORTES/2023_2024" / PROJECT),
        "output_folder": str(OUTPUT),
        "climate_shp": str(BASE / "3.POLYGON_TOWN/Santana606_1057/Santana606_1057.shp"),
        "climate_start_date": "2020-09-01",
        "climate_end_date": "2025-01-01",
        "climate_freq": "monthly",
        "max_k": 5,
        "polygon_id": 1897  
        },
    "8_all_cluster_segmentation": {
        "csv_path": str(OUTPUT / "2023_2024" / PROJECT / "ndvi/seasonal/rst_stationary/clusters_and_signatures.csv"),
        "base_raster_dir": str(RECORTES / "2023_2024" / PROJECT / "RECORTES"),
        "output_folder": str(OUTPUT / "2023_2024" / PROJECT / "ndvi/seasonal/rst_stationary/png_clusters_poligonos")
    },
    "8_2_tif_clustered": {
        "csv_path": str(OUTPUT / "2023_2024" / PROJECT / "ndvi/seasonal/rst_stationary/clusters_and_signatures.csv"),
        "base_raster_dir": str(RECORTES / "2023_2024" / PROJECT / "RECORTES"),
        "output_folder": str(OUTPUT / "2023_2024" / PROJECT / "ndvi/seasonal/rst_stationary/tiff_clusters_poligonos")
    },
  
}

def list_modules(folder='.'):
    """
    Lista los archivos .py del directorio, los ordena por prefijo numérico
    y devuelve los nombres de módulo (sin extensión) en orden.
    """
    archivos = [f for f in os.listdir(folder) if f.endswith('.py')]
    def key(f):
        m = re.match(r'^(\d+)', f)
        num = int(m.group(1)) if m else float('inf')
        return (num, f)
    # Ordena y quita la extensión .py
    return [f[:-3] for f in sorted(archivos, key=key)]


def run_pipeline(config, folder='.'):
    """
    Importa cada módulo en orden y llama a su función main(**params).
    Si no existe main, llama a la primera función pública que encuentre.
    """
    # Aseguramos que el folder está en path para importaciones
    sys.path.insert(0, folder)
    for module_name in [m for m in list_modules(folder) if m in config]:
        print(f"\n=== Ejecutando módulo {module_name} ===")
        try:
            mod = importlib.import_module(module_name)
            # Si tiene main, lo usamos
            if hasattr(mod, 'main') and callable(mod.main):
                params = config[module_name]
                print(f"Parámetros: {params}")
                mod.main(**params)
            else:
                # Fallback: toma la primera función pública
                funcs = [getattr(mod, a) for a in dir(mod)
                         if callable(getattr(mod, a)) and not a.startswith('_')]
                if funcs:
                    func = funcs[0]
                    params = config.get(module_name, {})
                    print(f"Llamando a {func.__name__} con {params}")
                    func(**params)
                else:
                    print("⚠️ No se encontró función ejecutable en el módulo.")
        except Exception as e:
            print(f"✗ Error en {module_name}: {e}")
            break

if __name__ == '__main__':
    run_pipeline(PARAMS)
