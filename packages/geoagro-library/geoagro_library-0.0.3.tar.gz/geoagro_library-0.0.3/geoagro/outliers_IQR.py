import pandas as pd

def remove_outliers_iqr(input_csv: str, output_csv: str, factor: float = 1.5) -> pd.DataFrame:
    """
    Carga un CSV, detecta y filtra filas con outliers en columnas 'band*'
    usando el método IQR con el factor dado, y guarda el resultado.

    Parámetros:
    - input_csv: ruta al CSV de entrada.
    - output_csv: ruta donde se escribirá el CSV sin outliers.
    - factor: múltiplo del IQR para definir límites (por defecto 1.5).

    Retorna:
    - DataFrame limpio (sin outliers).
    """
    # 1) Leer datos
    df = pd.read_csv(input_csv)

    # 2) Columnas de interés 
    cols_bandas = [c for c in df.columns if "band" in c]

    # 3) DataFrame para flags de outlier
    flags = pd.DataFrame(False, index=df.index, columns=cols_bandas)

    # 4) Detectar outliers por columna
    for col in cols_bandas:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - factor * IQR
        upper = Q3 + factor * IQR

        flags[col] = (df[col] < lower) | (df[col] > upper)
        print(f"Columna {col}: umbrales {lower:.3f}, {upper:.3f}],"
              f"outliers detectados = {flags[col].sum()}")
        
    # 5) Filtrar filas con outliers
    df_clean = df[~flags.any(axis=1)].copy()
    print(f"Filas sin outliers: {len(df_clean)}")

    # 6) Guardar CSV limpio
    df_clean.to_csv(output_csv, index=False)
    print(f"Se guardó '{output_csv}'")

    return df_clean

IN_CSV = (
        "/home/agrosavia/Documents/rs_agrosavia/"
        "DATA_CUBE_AGROSAVIA/ROI/GIS_FEDEPANELA/"
        "8.CSV_ALL/2023_2024/464_moniquira/ndvi/serie/CSV_ALL.csv"
    )

OUT_CSV = (
        "/home/agrosavia/Documents/rs_agrosavia/"
        "DATA_CUBE_AGROSAVIA/ROI/GIS_FEDEPANELA/"
        "8.CSV_ALL/2023_2024/464_moniquira/ndvi/serie/"
        "datos_sin_outliers_IQR.csv"
    )

remove_outliers_iqr(IN_CSV, OUT_CSV, factor=1.5)
