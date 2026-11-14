# Limpia registros_sucio.csv (tabla registros) siguiendo los criterios de la HU L01.
# Lee data/crudo/registros_sucio.csv y guarda data/limpio/registros_limpio.csv
# Este archivo vive en notebook/limpieza/

import os
import sys
from pathlib import Path

import pandas as pd

CARPETA_PROYECTO = Path(__file__).resolve().parents[2]   # raíz del proyecto
RUTA_ENTRADA = CARPETA_PROYECTO / "data" / "crudo" / "registros_sucio.csv"
RUTA_SALIDA = CARPETA_PROYECTO / "data" / "limpio" / "registros_limpio.csv"
COLUMNAS_OBLIGATORIAS = [
    "id", "fecha_registro", "observacion", "estado", "id_usuario", "id_reto",
]


# leo el csv con pandas
def leer_registros(ruta):
    return pd.read_csv(ruta)


# reviso que el csv traiga las columnas que pide la HU, porque sin ellas la limpieza falla a la mitad
def faltan_columnas(df):
    return [c for c in COLUMNAS_OBLIGATORIAS if c not in df.columns]


# imprimo el diagnóstico (shape, info, nulos y duplicados) para comparar antes y después
def imprimir_diagnostico(df, titulo):
    print(f"\n===== {titulo} =====")
    print("shape:", df.shape)
    print("\ninfo:")
    df.info()
    print("\nnulos por columna:")
    print(df.isna().sum())
    print("\nduplicados exactos:", df.duplicated().sum())


# quito las filas repetidas tal cual, todas las columnas iguales
def quitar_duplicados_exactos(df):
    df = df.drop_duplicates()
    return df


# convierto la fecha aunque venga en dos formatos; los que no se puedan convertir quedan en NaT
def convertir_fechas(df):
    df = df.copy()
    df["fecha_registro"] = pd.to_datetime(
        df["fecha_registro"], format="mixed", dayfirst=True, errors="coerce"
    )
    print("Fechas que no se pudieron convertir (NaT):", int(df["fecha_registro"].isna().sum()))
    return df


# develop mezcla dos juegos de nombres de estado (Pendiente/En Progreso/Completado y
# los sucios inscrito/EN PROCESO/Finalizado); los llevo todos a los tres estados oficiales
EQUIVALENCIAS_ESTADO = {
    "INSCRITO": "PENDIENTE",
    "EN_PROCESO": "EN_PROGRESO",
    "FINALIZADO": "COMPLETADO",
}


# unifico el estado: sin espacios sobrantes, en mayúscula, con guion bajo y con los nombres oficiales
def unificar_estado(df):
    df = df.copy()
    df["estado"] = df["estado"].str.strip().str.upper().str.replace(" ", "_")
    df["estado"] = df["estado"].replace(EQUIVALENCIAS_ESTADO)
    print("Estados distintos después de unificar:", sorted(df["estado"].dropna().unique().tolist()))
    return df


# relleno las observaciones vacías con un texto fijo para que no queden nulos
def rellenar_observaciones(df):
    df = df.copy()
    df["observacion"] = df["observacion"].fillna("Sin observacion")
    return df


# detecto las participaciones repetidas (mismo usuario en el mismo reto) y cuento cuántas son
def detectar_participaciones_repetidas(df):
    repetidos = df[df.duplicated(subset=["id_usuario", "id_reto"], keep=False)]
    print("Participaciones repetidas (filas involucradas):", len(repetidos))
    return repetidos


# me quedo solo con la primera participación de cada par usuario + reto (el backend rechazaría las demás con 409)
def dejar_primera_participacion(df):
    df = df.drop_duplicates(subset=["id_usuario", "id_reto"], keep="first")
    return df


# creo la columna mes para poder agrupar después
def crear_columna_mes(df):
    df = df.copy()
    df["mes"] = df["fecha_registro"].dt.to_period("M")
    return df


# compruebo que no queden nulos en las columnas obligatorias ni duplicados exactos
def verificar_resultado(df):
    nulos = int(df[COLUMNAS_OBLIGATORIAS].isna().sum().sum())
    duplicados = int(df.duplicated().sum())
    print("\n===== VERIFICACIÓN FINAL =====")
    print(f"Nulos en columnas obligatorias: {nulos} -> {'PASA' if nulos == 0 else 'FALLA'}")
    print(f"Duplicados exactos: {duplicados} -> {'PASA' if duplicados == 0 else 'FALLA'}")


# guardo el resultado en csv y creo la carpeta si no existe
def guardar_limpio(df, ruta):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    df.to_csv(ruta, index=False, encoding="utf-8")
    print("\nArchivo limpio guardado en:", ruta)


# sigo el orden de los criterios: diagnóstico, correcciones, diagnóstico final y guardado
def limpiar_registros(ruta_entrada=RUTA_ENTRADA, ruta_salida=RUTA_SALIDA):
    if not os.path.isfile(ruta_entrada):
        raise FileNotFoundError(
            f"No encuentro {ruta_entrada}. Primero hay que correr la simulación y la exportación."
        )
    df = leer_registros(ruta_entrada)
    faltan = faltan_columnas(df)
    if faltan:
        raise ValueError("Faltan columnas en el archivo: " + ", ".join(faltan))

    filas_inicio = len(df)
    imprimir_diagnostico(df, "DIAGNÓSTICO ANTES DE LIMPIAR")

    print("\n===== LIMPIEZA =====")
    df = quitar_duplicados_exactos(df)
    eliminadas_exactas = filas_inicio - len(df)
    print("Duplicados exactos eliminados:", eliminadas_exactas)

    df = convertir_fechas(df)
    df = unificar_estado(df)
    df = rellenar_observaciones(df)

    detectar_participaciones_repetidas(df)
    filas_antes_pares = len(df)
    df = dejar_primera_participacion(df)
    eliminadas_pares = filas_antes_pares - len(df)
    print("Participaciones repetidas eliminadas (se deja la primera):", eliminadas_pares)

    df = crear_columna_mes(df)

    imprimir_diagnostico(df, "DIAGNÓSTICO DESPUÉS DE LIMPIAR")
    eliminadas = filas_inicio - len(df)
    print(
        f"\nFilas eliminadas en total: {eliminadas} de {filas_inicio} "
        f"({eliminadas_exactas} duplicados exactos + {eliminadas_pares} participaciones repetidas)"
    )

    verificar_resultado(df)
    guardar_limpio(df, ruta_salida)
    return df


if __name__ == "__main__":
    try:
        limpiar_registros()
    except (FileNotFoundError, ValueError) as error:
        print(error, file=sys.stderr)
        sys.exit(1)