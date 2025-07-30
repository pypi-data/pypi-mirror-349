#!/usr/bin/env python3
import os
import numpy as np
import pandas as pd
import rasterio
import matplotlib.cm as cm
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def main(csv_path, base_raster_dir, output_folder):
    """
    Para cada polígono en el CSV:
      - Carga el raster completo (base_raster_dir/<polygon_id>/STACK/stack_ndvi.tif).
      - Filtra las firmas individuales para ese polígono.
      - Crea una matriz (uint8) del tamaño total del raster, inicializada en 0 (fondo).
      - Para cada cluster_label, asigna un índice (1..n) en vez de su valor real.
      - Genera una paleta (colormap) con n_global_clusters colores usando 'jet' de matplotlib.
      - Crea una imagen RGBA aplicando la paleta y la guarda en PNG.
      
    Advertencia:
      - El número de clusters por polígono debe ser <= 255.
    """
    os.makedirs(output_folder, exist_ok=True)

    # 1) Leer el CSV y filtrar solo 'individual'
    df = pd.read_csv(csv_path)
    df = df[df['type'] == 'individual']
    if df.empty:
        print("No se encontraron firmas individuales en el CSV.")
        return

    global_clusters = sorted(df['cluster_label'].unique())
    n_global_clusters = len(global_clusters)
    # Diccionario global (0 se reserva para fondo, índices empiezan en 1)
    global_cluster_to_index = {cl: i+1 for i, cl in enumerate(global_clusters)}
    
    # 2) Obtener polygon_fid únicos
    polygon_ids = sorted(df['polygon_fid'].unique())
    print(f"Se encontraron {len(polygon_ids)} polígonos en el CSV.")

    for pid in polygon_ids:
        df_poly = df[df['polygon_fid'] == pid]
        if df_poly.empty:
            print(f"No hay datos para polygon_fid={pid}. Se omite.")
            continue

        # Ruta al raster
        raster_path = os.path.join(base_raster_dir, f"{pid}", "STACK", "stack_ndvi.tif")
        if not os.path.exists(raster_path):
            print(f"Raster no encontrado para polígono {pid} en: {raster_path}")
            continue

        # Abrir raster para obtener dimensiones
        with rasterio.open(raster_path) as src:
            height, width = src.height, src.width

        # Crear matriz de índices (uint8) con 0 (fondo)
        mask = np.zeros((height, width), dtype=np.uint8)

        # Llenar la máscara usando el mapeo global de clusters
        for _, row in df_poly.iterrows():
            x = int(row['pixel_x'])
            y = int(row['pixel_y'])
            cl = row['cluster_label']
            if 0 <= y < height and 0 <= x < width:
                mask[y, x] = global_cluster_to_index[cl]

        # Generar paleta: lista de 256 colores RGBA (0 reservado para fondo)
        palette = [(0, 0, 0, 255)] * 256
        base_cmap = cm.get_cmap('jet', n_global_clusters)
        for i in range(n_global_clusters):
            r, g, b, a = base_cmap(i)
            palette[i+1] = (int(r*255), int(g*255), int(b*255), 255)

        # Crear imagen RGBA aplicando la paleta a la máscara
        palette_array = np.array(palette, dtype=np.uint8) 
        img_rgba = palette_array[mask]  
        fig, ax = plt.subplots(figsize=(12, 12)) 
        ax.imshow(img_rgba)
        ax.axis('off')

        unique_clusters_poly = sorted(df_poly['cluster_label'].unique())
        legend_handles = []
        for cl in unique_clusters_poly:
            index = global_cluster_to_index[cl]
            r, g, b, a = palette[index]
            # Normalizar colores para matplotlib (0 a 1)
            color = (r/255, g/255, b/255, a/255)
            patch = mpatches.Patch(color=color, label=f"Cluster {cl}")
            legend_handles.append(patch)
        ax.legend(handles=legend_handles, loc='lower right', frameon=True)

        # Convertir a imagen y guardar como PNG usando PIL
        out_png_path = os.path.join(output_folder, f"polygon_{pid}_clusters.png")
        plt.savefig(out_png_path, bbox_inches='tight', pad_inches=0.1)
        plt.close(fig)
        print(f"Guardado PNG con paleta para polígono {pid}: {out_png_path}")

if __name__ == "__main__":
    # Ruta al CSV con la información de firmas y clusters
    csv_path = "/home/agrosavia/Documents/rs_agrosavia/DATA_CUBE_AGROSAVIA/ROI/GIS_FEDEPANELA/9_output/2023_2024/Santana606_1057/ndvi/seasonal/rst_stationary/clusters_and_signatures.csv"
    # Directorio base que contiene las carpetas de polígonos (cada una con su raster)
    base_raster_dir = "/home/agrosavia/Documents/rs_agrosavia/DATA_CUBE_AGROSAVIA/ROI/GIS_FEDEPANELA/5.RECORTES/2023_2024/Santana606_1057/RECORTES"
    # Carpeta donde se guardarán los PNG de salida
    output_folder = "/home/agrosavia/Documents/rs_agrosavia/DATA_CUBE_AGROSAVIA/ROI/GIS_FEDEPANELA/9_output/2023_2024/Santana606_1057/ndvi/seasonal/rst_stationary/png_clusters_poligonos"
    
    # Ejecutar para todos los polígonos en el CSV
    main(csv_path, base_raster_dir, output_folder)
