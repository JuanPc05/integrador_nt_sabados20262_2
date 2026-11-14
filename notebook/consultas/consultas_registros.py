# Resuelve las cinco consultas de la HU Q01 sobre la tabla registros con pandas.
# Lee data/limpio/registros_limpio.csv y guarda data/limpio/registros_consulta_N.csv
# Este archivo vive en notebook/consultas/

import os
import sys
from pathlib import Path

import pandas as pd

CARPETA_PROYECTO = Path(__file__).resolve().parents[2]   # raíz del proyecto
RUTA_ENTRADA = CARPETA_PROYECTO / "data" / "limpio" / "registros_limpio.csv"
CARPETA_SALIDA = CARPETA_PROYECTO / "data" / "limpio"
COLUMNAS_NECESARIAS = ["id", "estado", "id_usuario", "id_reto", "mes"]


# leo el archivo limpio (no el sucio) con pandas
def leer_registros(ruta):
    return pd.read_csv(ruta)


# reviso que estén las columnas que usan las consultas, porque sin ellas fallan a la mitad
def faltan_columnas(df):
    return [c for c in COLUMNAS_NECESARIAS if c not in df.columns]


# guardo el resultado de una consulta en registros_consulta_N.csv y creo la carpeta si no existe
def guardar_resultado(resultado, numero, carpeta):
    os.makedirs(carpeta, exist_ok=True)
    ruta = os.path.join(carpeta, f"registros_consulta_{numero}.csv")
    if isinstance(resultado, pd.Series):
        # las series son conteos y su índice es la clave (estado, reto o mes), así que lo dejo
        resultado.rename("participaciones").to_csv(ruta, encoding="utf-8")
    else:
        resultado.to_csv(ruta, index=False, encoding="utf-8")
    print(f"(guardado en {ruta})")


# consulta 1: participaciones que ya están completadas
def consulta_completados(df, carpeta):
    print("\nConsulta 1: ¿Qué participaciones ya están completadas?")
    completados = df[df["estado"] == "COMPLETADO"]
    print("Total:", len(completados))
    print(completados)
    guardar_resultado(completados, 1, carpeta)
    return completados


# consulta 2: el mismo usuario inscrito más de una vez en el mismo reto
def consulta_repetidos(df, carpeta):
    print("\nConsulta 2: ¿Qué participaciones están repetidas (mismo usuario en el mismo reto)?")
    repetidos = df[df.duplicated(subset=["id_usuario", "id_reto"], keep=False)]
    # las ordeno por usuario y reto para ver juntas las filas de cada par
    repetidos = repetidos.sort_values(["id_usuario", "id_reto"])
    print("Total:", len(repetidos))
    if repetidos.empty:
        print("No hay participaciones repetidas.")
    else:
        print(repetidos)
    guardar_resultado(repetidos, 2, carpeta)
    return repetidos


# consulta 3: cuántas participaciones hay por estado
def consulta_conteo_por_estado(df, carpeta):
    print("\nConsulta 3: ¿Cuántas participaciones hay por estado?")
    conteo = df["estado"].value_counts()
    print(conteo)
    guardar_resultado(conteo, 3, carpeta)
    return conteo


# consulta 4 (groupby): los 10 retos con más participantes
def consulta_top_retos(df, carpeta):
    print("\nConsulta 4: ¿Cuáles son los 10 retos con más participantes?")
    top_retos = df.groupby("id_reto")["id"].count().nlargest(10)
    print(top_retos)
    guardar_resultado(top_retos, 4, carpeta)
    return top_retos


# consulta 5 (groupby): cuántas participaciones hubo cada mes
def consulta_por_mes(df, carpeta):
    print("\nConsulta 5: ¿Cuántas participaciones hubo cada mes?")
    por_mes = df.groupby("mes")["id"].count()
    print(por_mes)
    guardar_resultado(por_mes, 5, carpeta)
    return por_mes


# leo el archivo limpio, reviso las columnas y ejecuto las cinco consultas en orden
def ejecutar_consultas(ruta_entrada=RUTA_ENTRADA, carpeta=CARPETA_SALIDA):
    if not os.path.isfile(ruta_entrada):
        raise FileNotFoundError(
            f"No encuentro {ruta_entrada}. Primero hay que correr la limpieza."
        )
    df = leer_registros(ruta_entrada)
    faltan = faltan_columnas(df)
    if faltan:
        raise ValueError(
            "Faltan columnas en el archivo: " + ", ".join(faltan)
            + ". Usa el archivo LIMPIO (el que sale de limpiar_registros.py)."
        )

    # para que la consola muestre todas las columnas y no corte los resultados largos
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 200)
    pd.set_option("display.max_rows", 20)

    consulta_completados(df, carpeta)
    consulta_repetidos(df, carpeta)
    consulta_conteo_por_estado(df, carpeta)
    consulta_top_retos(df, carpeta)
    consulta_por_mes(df, carpeta)


if __name__ == "__main__":
    try:
        ejecutar_consultas()
    except (FileNotFoundError, ValueError) as error:
        print(error, file=sys.stderr)
        sys.exit(1)
