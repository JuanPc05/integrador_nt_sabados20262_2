# Resuelve las cinco consultas de la HU E2-EMP-Q01 sobre la tabla empresas con pandas.
# Lee data/limpio/empresas_limpio.csv y guarda data/limpio/empresas_consulta_N.csv
# Este archivo vive en src/

import os
import sys
from pathlib import Path

import pandas as pd

CARPETA_PROYECTO = Path(__file__).resolve().parents[2]   # raíz del proyecto
RUTA_LIMPIO = CARPETA_PROYECTO / "data" / "limpio" / "empresas_limpio.csv"
CARPETA_SALIDA = CARPETA_PROYECTO / "data" / "limpio"
COLUMNAS_NECESARIAS = ["id", "nombre", "sector", "activa"]



def leer_empresas(ruta):
    return pd.read_csv(ruta)


def faltan_columnas(df):
    return [c for c in COLUMNAS_NECESARIAS if c not in df.columns]


def normalizar_activa(serie):
    if serie.dtype == bool:
        return serie
    texto = serie.astype(str).str.strip().str.upper()
    return texto.isin(["TRUE", "1", "SI", "SÍ"])


def consulta_1_activas(df):
    print("\n--- Consulta 1: Empresas activas ---")
    activas = df[df["activa"] == True]
    print("Total:", len(activas))
    print(activas.head())
    ruta = CARPETA_SALIDA / "empresas_consulta_1.csv"
    activas.to_csv(ruta, index=False, encoding="utf-8")
    print(f"(guardado en {ruta})")
    return activas


# consulta 2: empresas de un sector (Logistica), ordenadas por nombre
def consulta_2_sector_ordenado(df):
    print("\n--- Consulta 2: Empresas del sector Logistica, ordenadas por nombre ---")
    logistica = df[df["sector"] == "Logistica"].sort_values("nombre")
    print("Total:", len(logistica))
    if logistica.empty:
        print("No hay empresas del sector Logistica.")
    else:
        print(logistica.head())
    ruta = CARPETA_SALIDA / "empresas_consulta_2.csv"
    logistica.to_csv(ruta, index=False, encoding="utf-8")
    print(f"(guardado en {ruta})")
    return logistica


# consulta 3: cuántas empresas hay por sector (conteo rápido)
def consulta_3_conteo(df):
    print("\n--- Consulta 3: Cuántas empresas hay por sector ---")
    conteo = df["sector"].value_counts()
    print(conteo)
    ruta = CARPETA_SALIDA / "empresas_consulta_3.csv"
    conteo.to_csv(ruta, header=["cantidad"], index_label="sector", encoding="utf-8")
    print(f"(guardado en {ruta})")
    return conteo


# consulta 4 (GROUPBY): empresas por sector, de mayor a menor
def consulta_4_por_sector(df):
    print("\n--- Consulta 4: Empresas por sector, de mayor a menor (GROUPBY) ---")
    por_sector = df.groupby("sector")["id"].count().sort_values(ascending=False)
    print(por_sector)
    ruta = CARPETA_SALIDA / "empresas_consulta_4.csv"
    por_sector.to_csv(ruta, header=["cantidad"], index_label="sector", encoding="utf-8")
    print(f"(guardado en {ruta})")
    return por_sector


# consulta 5 (GROUPBY doble): activas e inactivas por sector
def consulta_5_activas_por_sector(df):
    print("\n--- Consulta 5: Activas e inactivas por sector (GROUPBY doble) ---")
    tabla = df.groupby(["sector", "activa"])["id"].count().unstack(fill_value=0)
    print(tabla)
    ruta = CARPETA_SALIDA / "empresas_consulta_5.csv"
    tabla.to_csv(ruta, encoding="utf-8")
    print(f"(guardado en {ruta})")
    return tabla


# leo el archivo limpio, reviso las columnas y ejecuto las cinco consultas en orden
def ejecutar_consultas(ruta_entrada=RUTA_LIMPIO):
    if not os.path.isfile(ruta_entrada):
        raise FileNotFoundError(
            f"No encuentro {ruta_entrada}. Primero hay que correr la limpieza."
        )
    df = leer_empresas(ruta_entrada)
    faltan = faltan_columnas(df)
    if faltan:
        raise ValueError(
            "Faltan columnas en el archivo: " + ", ".join(faltan)
            + ". Usa el archivo LIMPIO de empresas."
        )

    df["activa"] = normalizar_activa(df["activa"])
    os.makedirs(CARPETA_SALIDA, exist_ok=True)

    # para que la consola muestre todas las columnas y no corte los resultados largos
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 200)

    consulta_1_activas(df)
    consulta_2_sector_ordenado(df)
    consulta_3_conteo(df)
    consulta_4_por_sector(df)
    consulta_5_activas_por_sector(df)


if __name__ == "__main__":
    try:
        ejecutar_consultas()
    except (FileNotFoundError, ValueError) as error:
        print(error, file=sys.stderr)
        sys.exit(1)