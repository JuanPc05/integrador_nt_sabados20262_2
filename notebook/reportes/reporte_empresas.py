# Crea las tres gráficas de la HU E2-EMP-G01 sobre la tabla empresas y escribe las conclusiones.
# Lee data/limpio/empresas_limpio.csv y guarda reportes/empresas_grafica_N.png
# Este archivo vive en src/

import os
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # sin ventana: el script guarda las imágenes y no se queda esperando
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MaxNLocator

CARPETA_PROYECTO = Path(__file__).resolve().parents[2]   # raíz del proyecto
RUTA_ENTRADA = CARPETA_PROYECTO / "data" / "limpio" / "empresas_limpio.csv"
CARPETA_REPORTES = CARPETA_PROYECTO / "reportes"
COLUMNAS_NECESARIAS = ["id", "nit", "sector", "activa"]

ACTIVA = "Activa"
INACTIVA = "Inactiva"


# leo el archivo limpio con pandas y conservo el nit como texto
def leer_empresas(ruta):
    return pd.read_csv(ruta, dtype={"nit": str})


# reviso que estén las columnas que usan las gráficas, porque sin ellas fallan a la mitad
def faltan_columnas(df):
    return [c for c in COLUMNAS_NECESARIAS if c not in df.columns]


# dejo activa como booleana, aunque el CSV la traiga como True/False, 1/0 o SI/NO
def normalizar_activa(serie):
    if serie.dtype == bool:
        return serie
    texto = serie.astype(str).str.strip().str.upper()
    return texto.isin(["TRUE", "1", "SI", "SÍ"])


# guardo la figura activa con dpi=120, la cierro (no uso plt.show) y devuelvo la ruta
def guardar_grafica(carpeta, numero):
    os.makedirs(carpeta, exist_ok=True)
    ruta = os.path.join(carpeta, f"empresas_grafica_{numero}.png")
    plt.tight_layout()
    plt.savefig(ruta, dpi=120)
    plt.close()
    return ruta


# consulta 1: cantidad de empresas por sector
def consulta_por_sector(df):
    return df.groupby("sector")["id"].count().sort_values(ascending=False)


# consulta 2: empresas activas vs inactivas
def consulta_activas_vs_inactivas(df):
    return (
        df["activa"].map({True: ACTIVA, False: INACTIVA})
        .value_counts()
        .reindex([ACTIVA, INACTIVA], fill_value=0)
    )


# tabla de activas e inactivas por sector
def tabla_activas_por_sector(df):
    tabla = df.groupby(["sector", "activa"]).size().unstack(fill_value=0)
    tabla = tabla.reindex(columns=[True, False], fill_value=0)
    tabla.columns = [ACTIVA, INACTIVA]
    return tabla


# gráfica 1: cantidad de empresas por sector
def grafica_empresas_por_sector(df, carpeta):
    por_sector = consulta_por_sector(df)
    plt.figure(figsize=(9, 5))
    por_sector.plot(kind="bar")
    plt.title("Cantidad de empresas por sector")
    plt.xlabel("Sector")
    plt.ylabel("Número de empresas")
    plt.xticks(rotation=45, ha="right")
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    return guardar_grafica(carpeta, 1)


# gráfica 2: empresas activas vs inactivas
def grafica_activas_vs_inactivas(df, carpeta):
    conteo = consulta_activas_vs_inactivas(df)
    plt.figure(figsize=(6, 6))
    conteo.plot(kind="pie", autopct="%1.1f%%")
    plt.title("Empresas activas vs inactivas")
    plt.ylabel("")
    return guardar_grafica(carpeta, 2)


# gráfica 3: activas e inactivas por sector
def grafica_activas_por_sector(df, carpeta):
    tabla = tabla_activas_por_sector(df)
    plt.figure(figsize=(9, 5))
    tabla.plot(kind="bar", stacked=True, ax=plt.gca())
    plt.title("Empresas activas e inactivas por sector")
    plt.xlabel("Sector")
    plt.ylabel("Número de empresas")
    plt.xticks(rotation=45, ha="right")
    plt.legend(title="Estado")
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    return guardar_grafica(carpeta, 3)


# devuelve los valores máximos y si hay empate
def texto_maximo(conteo):
    maximo = int(conteo.max())
    ganadores = [str(clave) for clave in conteo[conteo == maximo].index]
    return ", ".join(ganadores), maximo, len(ganadores) > 1


# imprime un resumen de sectores, estados y nit repetidos
def imprimir_conclusiones(df):
    print("\n===== CONCLUSIONES =====")
    total = len(df)

    sector, cantidad, empate = texto_maximo(consulta_por_sector(df))
    if empate:
        print(f"1. Sectores con más empresas (empatados): {sector}, con {cantidad} cada uno.")
    else:
        print(f"1. El sector con más empresas es {sector}, con {cantidad} de {total}.")

    activas = int(df["activa"].sum())
    inactivas = total - activas
    print(
        f"2. Hay {activas} empresas activas ({activas / total:.1%}) y "
        f"{inactivas} inactivas ({inactivas / total:.1%})."
    )

    tabla = tabla_activas_por_sector(df)
    sector_act, n_act, empate_act = texto_maximo(tabla[ACTIVA])
    sector_ina, n_ina, empate_ina = texto_maximo(tabla[INACTIVA])
    etiqueta_act = (
        "Sectores con más empresas activas (empatados)"
        if empate_act else "El sector con más empresas activas"
    )
    etiqueta_ina = (
        "Sectores con más empresas inactivas (empatados)"
        if empate_ina else "El sector con más empresas inactivas"
    )
    print(f"3. {etiqueta_act}: {sector_act}, con {n_act}.")
    print(f"   {etiqueta_ina}: {sector_ina}, con {n_ina}.")

    repetidos = int(df.duplicated(subset=["nit"], keep="first").sum())
    print(f"4. Empresas con nit repetido encontradas: {repetidos}.")


# lee el CSV limpio, crea las gráficas e imprime las conclusiones
def crear_reporte(ruta_entrada=RUTA_ENTRADA, carpeta=CARPETA_REPORTES):
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
    if df.empty:
        raise ValueError("El archivo no tiene filas, no hay nada que graficar.")

    df["activa"] = normalizar_activa(df["activa"])

    print("Gráficas guardadas:")
    for ruta in (
        grafica_empresas_por_sector(df, carpeta),
        grafica_activas_vs_inactivas(df, carpeta),
        grafica_activas_por_sector(df, carpeta),
    ):
        print(" -", ruta)

    imprimir_conclusiones(df)


if __name__ == "__main__":
    try:
        crear_reporte()
    except (FileNotFoundError, ValueError) as error:
        print(error, file=sys.stderr)
        sys.exit(1)