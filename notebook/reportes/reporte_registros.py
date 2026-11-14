# Crea las tres gráficas de la HU G01 sobre la tabla registros y escribe las conclusiones.
# Lee data/limpio/registros_limpio.csv y guarda reportes/registros_grafica_N.png
# Este archivo vive en notebook/reportes/

import os
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # sin ventana: el script guarda las imágenes y no se queda esperando
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MaxNLocator

CARPETA_PROYECTO = Path(__file__).resolve().parents[2]   # raíz del proyecto
RUTA_ENTRADA = CARPETA_PROYECTO / "data" / "limpio" / "registros_limpio.csv"
CARPETA_REPORTES = CARPETA_PROYECTO / "reportes"
COLUMNAS_NECESARIAS = ["id", "estado", "id_usuario", "id_reto", "mes"]


# leo el archivo limpio con pandas
def leer_registros(ruta):
    return pd.read_csv(ruta)


# reviso que estén las columnas que usan las gráficas, porque sin ellas fallan a la mitad
def faltan_columnas(df):
    return [c for c in COLUMNAS_NECESARIAS if c not in df.columns]


# guardo la figura activa con dpi=120, la cierro (no uso plt.show) y devuelvo la ruta
def guardar_grafica(carpeta, numero):
    os.makedirs(carpeta, exist_ok=True)
    ruta = os.path.join(carpeta, f"registros_grafica_{numero}.png")
    plt.tight_layout()
    plt.savefig(ruta, dpi=120)
    plt.close()
    return ruta


# gráfica 1 (barras): participaciones por estado
def grafica_participaciones_por_estado(df, carpeta):
    conteo = df["estado"].value_counts()
    plt.figure(figsize=(8, 5))
    conteo.plot(kind="bar")
    plt.title("Participaciones por estado")
    plt.xlabel("Estado")
    plt.ylabel("Número de participaciones")
    plt.xticks(rotation=0)
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    return guardar_grafica(carpeta, 1)


# gráfica 2 (línea): participaciones por mes
def grafica_participaciones_por_mes(df, carpeta):
    por_mes = df.groupby("mes")["id"].count()
    plt.figure(figsize=(8, 5))
    por_mes.plot(kind="line", marker="o")
    plt.title("Participaciones por mes")
    plt.xlabel("Mes")
    plt.ylabel("Número de participaciones")
    plt.ylim(bottom=0)  # el eje parte de 0 para no exagerar las diferencias entre meses
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    return guardar_grafica(carpeta, 2)


# gráfica 3 (barras horizontales): los 10 retos con más participantes
def grafica_top_retos(df, carpeta):
    top_retos = df.groupby("id_reto")["id"].count().nlargest(10)
    # muestro los primeros 8 caracteres del id para que quepan las etiquetas;
    # si se repiten entre retos, uso el id completo para que se distingan
    etiquetas_cortas = top_retos.rename(index=lambda id_reto: str(id_reto)[:8])
    usar_cortas = etiquetas_cortas.index.is_unique
    datos = etiquetas_cortas if usar_cortas else top_retos
    plt.figure(figsize=(8, 5) if usar_cortas else (11, 5))
    datos.plot(kind="barh")
    plt.title("Los 10 retos con más participantes")
    plt.xlabel("Número de participantes")
    plt.ylabel("Reto (primeros 8 caracteres del id)" if usar_cortas else "Reto (id)")
    plt.gca().invert_yaxis()  # el reto con más participantes queda arriba
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    return guardar_grafica(carpeta, 3)


# escribo en una frase los valores máximos de un conteo; si hay empate los nombro todos
def texto_maximo(conteo):
    maximo = int(conteo.max())
    ganadores = [str(clave) for clave in conteo[conteo == maximo].index]
    return ", ".join(ganadores), maximo, len(ganadores) > 1


# imprimo las conclusiones: reto más popular, mes con más inscripciones y duplicados
def imprimir_conclusiones(df):
    print("\n===== CONCLUSIONES =====")

    reto, participantes, empate = texto_maximo(df.groupby("id_reto")["id"].count())
    palabra = "participante" if participantes == 1 else "participantes"
    if empate:
        print(f"1. Retos más populares (empatados): {reto}, con {participantes} {palabra} cada uno.")
    else:
        print(f"1. El reto más popular es {reto}, con {participantes} {palabra}.")

    mes, inscripciones, empate = texto_maximo(df.groupby("mes")["id"].count())
    if empate:
        print(f"2. Meses con más inscripciones (empatados): {mes}, con {inscripciones} cada uno.")
    else:
        print(f"2. El mes con más inscripciones fue {mes}, con {inscripciones}.")

    # inscripciones duplicadas = las filas que sobran del mismo usuario en el mismo reto
    sobrantes = int(df.duplicated(subset=["id_usuario", "id_reto"], keep="first").sum())
    pares = int(df[df.duplicated(subset=["id_usuario", "id_reto"], keep=False)]
                .drop_duplicates(subset=["id_usuario", "id_reto"]).shape[0])
    if sobrantes == 0:
        print("3. Inscripciones duplicadas encontradas: 0 (en este archivo no hay ningún usuario repetido en el mismo reto,")
        print("   porque la limpieza ya dejó solo la primera participación de cada par usuario + reto).")
    else:
        print(f"3. Inscripciones duplicadas encontradas: {sobrantes} (en {pares} pares usuario + reto).")
    print("   El back debe bloquearlas con 409 (Conflict): el usuario ya está inscrito en ese reto, así que repetir el")
    print("   registro entra en conflicto con lo que ya existe; si no se bloquea, un mismo usuario contaría dos veces")
    print("   en el reto y se inflarían las estadísticas.")


# leo el archivo limpio, creo las tres gráficas e imprimo las rutas y las conclusiones
def crear_reporte(ruta_entrada=RUTA_ENTRADA, carpeta=CARPETA_REPORTES):
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
    if df.empty:
        raise ValueError("El archivo no tiene filas, no hay nada que graficar.")

    print("Gráficas guardadas:")
    for ruta in (
        grafica_participaciones_por_estado(df, carpeta),
        grafica_participaciones_por_mes(df, carpeta),
        grafica_top_retos(df, carpeta),
    ):
        print(" -", ruta)

    imprimir_conclusiones(df)


if __name__ == "__main__":
    try:
        crear_reporte()
    except (FileNotFoundError, ValueError) as error:
        print(error, file=sys.stderr)
        sys.exit(1)