import os
from pathlib import Path
import geopandas as gpd
import rasterio
from rasterio.mask import mask

def recortar_tifs_por_poligonos(source_folder: str, shapefile_path: str, destination_folder: str):
    """
    Recorta todos los   archivos .tif en source_folder usando cada poligono
    del shapefile y guarda los recortes den destination_folder/<fid>/RECORTES/.

    Parametros:
    - source_folder: ruta a la carpeta que contiene los TIFFs originales.
    - shape_file: ruta al shapefile con poligonos (campo 'fid').
    - destination_foldler: ruta base donde se crearan subcarpetas de salida.
    """

    src_folder = Path(source_folder)
    dest_base = Path(destination_folder)
    dest_base.mkdir(parents=True, exist_ok=True)

    # Leer shapefile
    gdf = gpd.read_file(shapefile_path)
    for _, row in gdf.iterrows():
         fid = row.get('fid', row.get('FID', None))
         geom = [row.geometry]
         if fid is None:
              continue
         
         # Carpeta de destino para este poligono
         poly_folder = dest_base / str(fid) / "RECORTES"
         poly_folder.mkdir(parents=True, exist_ok=True)

         # Iterar TIFFs
         for tif in src_folder.glob("*.tif"):
              with rasterio.open(tif) as src:
                   try:
                        out_img, out_tf = mask(src, geom, crop=True)
                        out_meta = src.meta.copy()
                        out_meta.update({
                             "driver": "GTiff",
                             "height": out_img.shape[1],
                             "width": out_img.shape[2],
                             "transform": out_tf
                        })
                        out_path = poly_folder / tif.name
                        with rasterio.open(out_path, "w", **out_meta) as dst:
                             dst.write(out_img)
                        print(f"Recortado {out_path}")
                   except Exception as e:
                        print(f"Error recortando {tif.name} con poligono {fid}: {e}")

def main(
    source_folder: str,
    shape_file: str,
    destination_folder: str
) -> None:
    """
    Punto de entrada para integrar en pipeline.
    """
    recortar_tifs_por_poligonos(
        source_folder,
        shape_file,
        destination_folder
    )

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('source_folder')
    parser.add_argument('shape_file')
    parser.add_argument('destination_folder')
    args = parser.parse_args()
    main(
        args.source_folder,
        args.shape_file,
        args.destination_folder
    )
         