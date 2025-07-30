# 8_cluster_advanced.py
import re
import pandas as pd
import numpy as np
from pathlib import Path
from tslearn.clustering import TimeSeriesKMeans
from tslearn.preprocessing import TimeSeriesScalerMeanVariance
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import geopandas as gpd
import requests
import concurrent.futures
from typing import List, Optional, Tuple


def extract_date_from_tif(file_name: str) -> Optional[str]:
    match = re.search(r"\d{2}_\d{4}", str(file_name))
    return match.group(0) if match else None


def extract_month_year(date_str: Optional[str]) -> Tuple[Optional[int], Optional[int]]:
    if date_str:
        month, year = date_str.split('_')
        return int(year), int(month)
    return None, None


def find_tif_files(base_folder: str, polygon_id: Optional[int] = None) -> List[Path]:
    base = Path(base_folder)
    if polygon_id is not None:
        folder = base / f"{polygon_id}.0" / "RECORTES"
        return sorted(folder.glob("*.tif")) if folder.exists() else []
    candidates = [p for p in base.iterdir() if p.is_dir() and p.name.endswith('.0')]
    if not candidates:
        return []
    rec = sorted(candidates)[0] / "RECORTES"
    return sorted(rec.glob("*.tif")) if rec.exists() else []


def compute_inertia(k: int, X: np.ndarray, metric: str) -> float:
    model = TimeSeriesKMeans(n_clusters=k, metric=metric, random_state=42)
    model.fit(X)
    return model.inertia_

def compute_inertia_args(args_tuple):
    k, X, metric = args_tuple
    return compute_inertia(k, X, metric)

def elbow_method_time_series(X: np.ndarray, max_k: int = 20, metric: str = "euclidean") -> Tuple[List[int], List[float]]:
    ks = list(range(1, max_k+1))
    args = [(k, X, metric) for k in ks]
    with concurrent.futures.ProcessPoolExecutor() as executor:
        inertias = list(executor.map(compute_inertia_args, args))
    return ks, inertias


def find_elbow(ks: List[int], inertias: List[float]) -> int:
    if len(inertias) < 2:
        return ks[0]
    diffs = [inertias[i] - inertias[i+1] for i in range(len(inertias)-1)]
    return ks[int(np.argmax(diffs))+1]


def extract_centroids_from_shp(shp_path: str) -> Optional[pd.DataFrame]:
    try:
        gdf = gpd.read_file(shp_path)
        if gdf.crs and gdf.crs.to_epsg() != 4326:
            gdf = gdf.to_crs(epsg=4326)
        gdf['centroid'] = gdf.geometry.centroid
        gdf['latitude'] = gdf.centroid.y
        gdf['longitude'] = gdf.centroid.x
        return gdf[['latitude', 'longitude']]
    except Exception:
        return None


def fetch_om_data(latitude: float, longitude: float, start_date: str, end_date: str, freq: str) -> Optional[pd.DataFrame]:
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": ["temperature_2m", "relative_humidity_2m", "precipitation"],
        "start_date": start_date,
        "end_date": end_date,
        "timezone": "UTC"
    }
    try:
        res = requests.get(url, params=params)
        res.raise_for_status()
        data = res.json().get('hourly', {})
        df = pd.DataFrame({
            'date': pd.to_datetime(data.get('time', [])),
            'temperature_2m': data.get('temperature_2m', []),
            'relative_humidity_2m': data.get('relative_humidity_2m', []),
            'precipitation': data.get('precipitation', [])
        })
        if freq == 'daily':
            return df.resample('D', on='date').mean().reset_index()
        if freq == 'monthly':
            daily = df.resample('D', on='date').mean().reset_index()
            return daily.resample('M', on='date').mean().reset_index()
        return df
    except Exception:
        return None


def main(
    csv_path: str,
    base_tif_folder: str,
    output_folder: str,
    climate_shp: str,
    climate_start_date: str,
    climate_end_date: str,
    climate_freq: str = 'monthly',
    max_k: int = 20,
    polygon_id: Optional[int] = None
) -> None:
    """
    1. Encuentra TIFs y extrae fechas.
    2. Carga y filtra CSV.
    3. Elbow method e inertia plot.
    4. Clustering con k sugerido.
    5. Fetch clima usando centroide promedio.
    6. Plotea clusters con overlay de temperatura.
    7. Exporta CSVs y gráficos en output_folder.
    """
    out_dir = Path(output_folder)
    out_dir.mkdir(parents=True, exist_ok=True)

    # TIF files
    tifs = find_tif_files(base_tif_folder, polygon_id)
    dates = [extract_date_from_tif(t.name) for t in tifs]
    pairs = [(t, d) for t, d in zip(tifs, dates) if d]
    pairs.sort(key=lambda x: extract_month_year(x[1]))
    num_bands = len(pairs)

    # Load CSV
    df_full = pd.read_csv(csv_path)
    df = df_full[df_full['polygon_fid']==polygon_id].copy() if polygon_id is not None else df_full.copy()

    band_cols = [c for c in df.columns if c.startswith('band_')]
    X = df[band_cols].values

    # Elbow
    ks, inertias = elbow_method_time_series(X, max_k)
    plt.figure()
    plt.plot(ks, inertias, marker='o')
    plt.title('Elbow - RAW')
    plt.xlabel('k'); plt.ylabel('Inertia'); plt.grid(True)
    plt.savefig(out_dir/'elbow_raw.png', dpi=150)
    plt.close()

    k_raw = find_elbow(ks, inertias)

    # Clustering
    km = TimeSeriesKMeans(n_clusters=k_raw, random_state=42)
    labels = km.fit_predict(X)
    df['cluster_raw'] = labels
    df.to_csv(out_dir/'clusters_raw.csv', index=False)

    # Climate data
    centroids = extract_centroids_from_shp(climate_shp)
    climate_df = None
    if centroids is not None:
        avg_lat, avg_lon = centroids['latitude'].mean(), centroids['longitude'].mean()
        climate_df = fetch_om_data(avg_lat, avg_lon, climate_start_date, climate_end_date, climate_freq)

    # Plot clusters
    for cl in sorted(df['cluster_raw'].unique()):
        sub = df[df['cluster_raw']==cl]
        plt.figure(figsize=(12,6))
        for _, row in sub.iterrows():
            plt.plot(range(num_bands), row[band_cols].values, color='lightblue', alpha=0.3)
        mean_series = sub[band_cols].mean()
        plt.plot(range(num_bands), mean_series.values, color='red', linewidth=3, label=f'Avg cluster {cl}')
        if climate_df is not None:
            x = np.linspace(0, num_bands-1, len(climate_df))
            ax = plt.gca()
            ax2 = ax.twinx()
            ax2.plot(x, climate_df['temperature_2m'], color='orange', linewidth=2, label='Temp')
            ax2.set_ylabel('Temp (°C)', color='orange')
            ax2.tick_params(axis='y', labelcolor='orange')
        plt.title(f"Cluster RAW {polygon_id or 'all'}")
        plt.legend(); plt.grid(True)
        plt.savefig(out_dir/f'cluster_{cl}.png', dpi=150)
        plt.close()

    # Signatures
    rows = []
    for cl in sorted(df['cluster_raw'].unique()):
        sub = df[df['cluster_raw']==cl]
        for _, r in sub.iterrows():
            rows.append([r.get('polygon_fid'), r.get('pixel_x'), r.get('pixel_y'), cl, 'individual'] + list(r[band_cols]))
        mean_r = sub[band_cols].mean()
        rows.append([polygon_id, None, None, cl, 'cluster'] + list(mean_r))
    cols = ['polygon_fid','pixel_x','pixel_y','cluster_label','type'] + band_cols
    pd.DataFrame(rows, columns=cols).to_csv(out_dir/'signatures.csv', index=False)

    print(f"Outputs saved in {out_dir}")
