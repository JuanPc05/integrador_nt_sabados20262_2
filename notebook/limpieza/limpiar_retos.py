"""Limpia la tabla retos (HU L01 de Kaizen).

Lee    data/crudo/retos_sucio.csv
Guarda data/limpio/retos_limpio.csv

Uso directo:
    python notebook/limpieza/limpiar_retos.py
"""
import sys
from pathlib import Path

import pandas as pd

# 1. Rutas y nombres
NOMBRE_ENTIDAD = "retos"

# El script está en 'notebook/limpieza/'. La raíz del proyecto está 2 niveles arriba.
CARPETA_PROYECTO = Path(__file__).resolve().parents[2]
RUTA_ENTRADA = CARPETA_PROYECTO / "data" / "crudo" / f"{NOMBRE_ENTIDAD}_sucio.csv"
RUTA_SALIDA = CARPETA_PROYECTO / "data" / "limpio" / f"{NOMBRE_ENTIDAD}_limpio.csv"

# Columnas que no pueden quedar con nulos después de limpiar
COLUMNAS_OBLIGATORIAS = ["id", "nombre", "descripcion", "estado"]


# 2. Diagnóstico
def imprimir_diagnostico(df, titulo):
    """Imprime shape, info, nulos por columna y duplicados exactos."""
    print(f"\n===== {titulo} =====")
    print("shape:", df.shape)
    print("\ninfo:")
    df.info()
    print("\nNulos por columna:")
    print(df.isna().sum())
    print("\nDuplicados exactos:", df.duplicated().sum())


# 3. Pasos de limpieza (en el orden de los criterios)
def vaciar_textos_en_blanco(df):
    """Convierte textos vacíos o solo con espacios en nulos reales (NaN)."""
    for col in df.select_dtypes(include=["object", "string"]).columns:
        df[col] = df[col].where(df[col].astype("string").str.strip() != "", pd.NA)
    return df


def quitar_duplicados(df):
    """Elimina las filas duplicadas exactas."""
    return df.drop_duplicates()


def convertir_fechas(df):
    """Convierte fecha_inicio y fecha_fin a datetime aunque vengan en dos formatos.

    Primero se leen las fechas ISO (2026-01-10), porque dayfirst=True las
    invertiría (10 de enero -> 1 de octubre). Las que no son ISO (15/02/2026)
    se leen con format="mixed" y dayfirst=True, como piden los criterios.
    """
    for col in ["fecha_inicio", "fecha_fin"]:
        iso = pd.to_datetime(df[col], format="ISO8601", errors="coerce")
        resto = pd.to_datetime(
            df.loc[iso.isna(), col], format="mixed", dayfirst=True, errors="coerce"
        )
        df[col] = iso.where(iso.notna(), resto)
    return df


def unificar_estado(df):
    """Estado en mayúsculas, sin espacios en los bordes y con '_' en vez de espacios."""
    df["estado"] = df["estado"].str.strip().str.upper().str.replace(" ", "_")
    return df


def rellenar_descripciones(df):
    """Rellena las descripciones vacías con 'Sin descripcion'."""
    df["descripcion"] = df["descripcion"].fillna("Sin descripcion")
    return df


def calcular_duracion(df):
    """Crea duracion_dias y marca en fecha_valida las fechas coherentes (fin >= inicio)."""
    df["duracion_dias"] = (df["fecha_fin"] - df["fecha_inicio"]).dt.days
    df["fecha_valida"] = df["duracion_dias"] >= 0
    return df


# 4. Flujo completo
def limpiar_retos(ruta_entrada=RUTA_ENTRADA, ruta_salida=RUTA_SALIDA):
    """Lee, diagnostica, limpia, diagnostica otra vez y guarda retos_limpio.csv."""
    ruta_entrada = Path(ruta_entrada)
    ruta_salida = Path(ruta_salida)

    df = pd.read_csv(ruta_entrada, encoding="utf-8")
    filas_antes = len(df)
    nulos_antes = int(df.isna().sum().sum())
    imprimir_diagnostico(df, "DIAGNOSTICO ANTES DE LIMPIAR")

    df = vaciar_textos_en_blanco(df)
    df = quitar_duplicados(df)
    df = convertir_fechas(df)
    df = unificar_estado(df)
    df = rellenar_descripciones(df)
    df = calcular_duracion(df)

    imprimir_diagnostico(df, "DIAGNOSTICO DESPUES DE LIMPIAR")

    incoherentes = int((df["duracion_dias"] < 0).sum())
    sin_fecha = int(df["duracion_dias"].isna().sum())
    nulos_despues = int(df.isna().sum().sum())
    print("\n===== RESUMEN =====")
    print("Filas antes:", filas_antes, "| despues:", len(df))
    print("Filas eliminadas (duplicados exactos):", filas_antes - len(df))
    print("Fechas incoherentes (fin antes que inicio):", incoherentes)
    print("Filas con fecha ilegible o vacia (fecha_valida=False):", sin_fecha)
    print("Nulos totales antes:", nulos_antes, "| despues:", nulos_despues)
    print("Nulos en columnas obligatorias:",
          int(df[COLUMNAS_OBLIGATORIAS].isna().sum().sum()))
    print("Duplicados exactos que quedan:", int(df.duplicated().sum()))

    ruta_salida.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(ruta_salida, index=False, encoding="utf-8")
    print(f"\nArchivo limpio guardado en: {ruta_salida.relative_to(CARPETA_PROYECTO)}")
    return df


# 5. Ejecutar
if __name__ == "__main__":
    if not RUTA_ENTRADA.is_file():
        print(f"No se encontró el archivo: {RUTA_ENTRADA}")
        sys.exit(1)
    limpiar_retos()