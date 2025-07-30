# 8_2_tif_clustered.py
import os
import numpy as np
import pandas as pd
import rasterio
import matplotlib.cm as cm
from matplotlib.colors import ListedColormap
from pathlib import Path

def plot_and_save_cluster_tif(
    csv_path: str,
    base_raster_dir: str,
    output_folder: str
) -> None:
    """
    Para cada polígono en el CSV:
      - Carga stack_ndvi.tif
      - Crea máscara indexada por cluster y escribe TIFF con paleta.
    """
    os.makedirs(output_folder, exist_ok=True)

    df = pd.read_csv(csv_path)
    df = df[df['type'] == 'individual']
    if df.empty:
        print("No se encontraron firmas individuales en el CSV.")
        return

    global_clusters = sorted(df['cluster_label'].unique())
    n_global_clusters = len(global_clusters)
    global_cluster_to_index = {cl: i+1 for i, cl in enumerate(global_clusters)}

    polygon_ids = sorted(df['polygon_fid'].unique())
    print(f"Se encontraron {len(polygon_ids)} polígonos en el CSV.")

    # Generar paleta global una vez
    palette = [(0,0,0,255)] * 256
    base_cmap = cm.get_cmap('jet', n_global_clusters)
    for i, cl in enumerate(global_clusters):
        r, g, b, _ = base_cmap(i)
        palette[i+1] = (int(r*255), int(g*255), int(b*255), 255)
    colormap_dict = {i: palette[i] for i in range(len(palette))}

    for pid in polygon_ids:
        df_poly = df[df['polygon_fid'] == pid]
        if df_poly.empty:
            continue

        raster_path = Path(base_raster_dir) / str(pid) / "STACK" / "stack_ndvi.tif"
        if not raster_path.exists():
            print(f"Raster no encontrado para polígono {pid}: {raster_path}")
            continue

        with rasterio.open(raster_path) as src:
            profile = src.profile.copy()
            height, width = profile['height'], profile['width']

        mask = np.zeros((height, width), dtype=np.uint8)

        for _, row in df_poly.iterrows():
            x = int(row['pixel_x'])
            y = int(row['pixel_y'])
            cl = row['cluster_label']
            idx = global_cluster_to_index.get(cl, 0)
            if 0 <= y < height and 0 <= x < width:
                mask[y, x] = idx

        profile.update({
            'count': 1,
            'dtype': 'uint8',
            'photometric': 'PALETTE',
            'nodata': 0,
        })

        out_tif_path = Path(output_folder) / f"polygon_{pid}_clusters.tif"
        with rasterio.open(out_tif_path, 'w', **profile) as dst:
            dst.write(mask, 1)
            dst.write_colormap(1, colormap_dict)

        print(f"Guardado TIFF para polígono {pid}: {out_tif_path}")

def main(
    csv_path: str,
    base_raster_dir: str,
    output_folder: str
) -> None:
    """
    Función de entrada para pipeline.
    """
    plot_and_save_cluster_tif(
        csv_path,
        base_raster_dir,
        output_folder
    )

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_path')
    parser.add_argument('base_raster_dir')
    parser.add_argument('output_folder')
    args = parser.parse_args()
    main(
        args.csv_path,
        args.base_raster_dir,
        args.output_folder
    )
