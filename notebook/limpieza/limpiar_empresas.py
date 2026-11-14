# Limpia los datos de la HU E2-EMP-L01 sobre la tabla empresas con pandas.
# Lee data/crudo/empresas_sucio.csv y guarda data/limpio/empresas_limpio.csv
# Este archivo vive en notebook/limpieza/

import os
import re
import sys
from pathlib import Path

import pandas as pd

CARPETA_PROYECTO = Path(__file__).resolve().parents[2]   # raíz del proyecto
RUTA_ENTRADA = CARPETA_PROYECTO / "data" / "crudo" / "empresas_sucio.csv"
RUTA_SALIDA = CARPETA_PROYECTO / "data" / "limpio" / "empresas_limpio.csv"
COLUMNAS_NECESARIAS = ["id", "nombre", "nit", "sector", "contacto", "correo", "telefono", "activa"]

VALORES_VERDADEROS = {"TRUE", "1", "SI", "SÍ"}
VALORES_FALSOS = {"FALSE", "0", "NO"}
PATRON_CORREO = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


# leo el archivo sucio con todo como texto, para que no se pierdan ceros ni formatos
def leer_empresas(ruta):
    return pd.read_csv(ruta, dtype=str)


# reviso que estén las columnas que usa la limpieza, porque sin ellas falla a la mitad
def faltan_columnas(df):
    return [c for c in COLUMNAS_NECESARIAS if c not in df.columns]


# imprimo shape, info y nulos (la evidencia del antes y el después)
def mostrar_estado(df, titulo):
    print(f"\n===== {titulo} =====")
    print("shape:", df.shape)
    print("\ninfo:")
    df.info()
    print("\nnulos por columna:")
    print(df.isna().sum())


# nombre: quito espacios de los lados y dobles, y dejo cada palabra con mayúscula inicial
def limpiar_nombre(df):
    df["nombre"] = (
        df["nombre"].str.strip().str.replace(r"\s+", " ", regex=True).str.title()
    )
    return df


# nit: dejo solo los 10 dígitos y los escribo siempre como #########-#
def formatear_nit(valor):
    if pd.isna(valor):
        return pd.NA
    digitos = re.sub(r"\D", "", str(valor))
    if len(digitos) != 10:
        return pd.NA
    return f"{digitos[:9]}-{digitos[9]}"


def limpiar_nit(df):
    df["nit"] = df["nit"].apply(formatear_nit)
    return df


# sector: sin espacios y con mayúscula inicial (Tecnologia, Salud, ...)
def limpiar_sector(df):
    df["sector"] = df["sector"].str.strip().str.capitalize()
    return df


# contacto: los nulos se llenan con un texto claro para no perder la empresa
def limpiar_contacto(df):
    df["contacto"] = df["contacto"].str.strip().fillna("Sin contacto")
    return df


# correo: en minúscula y sin espacios; si no tiene un formato válido (por ejemplo sin @) queda como "Sin correo"
def limpiar_correo(df):
    correo = df["correo"].str.strip().str.lower()
    valido = correo.str.match(PATRON_CORREO, na=False)
    df["correo"] = correo.where(valido, "Sin correo")
    return df


# telefono: dejo solo los 10 dígitos (quito espacios, guiones y el +57)
def formatear_telefono(valor):
    if pd.isna(valor):
        return pd.NA
    digitos = re.sub(r"\D", "", str(valor))
    if len(digitos) == 12 and digitos.startswith("57"):
        digitos = digitos[2:]
    return digitos if len(digitos) == 10 else pd.NA


def limpiar_telefono(df):
    df["telefono"] = df["telefono"].apply(formatear_telefono).fillna("Sin telefono")
    return df


# activa: paso True/False, SI/NO y 1/0 a una columna booleana
def limpiar_activa(df):
    texto = df["activa"].str.strip().str.upper()
    df["activa"] = texto.map(
        lambda v: True if v in VALORES_VERDADEROS else (False if v in VALORES_FALSOS else pd.NA)
    )
    df["activa"] = df["activa"].fillna(False).astype(bool)
    return df


# duplicados: primero las filas idénticas y luego los nit repetidos entre empresas distintas
def quitar_duplicados(df):
    antes = len(df)
    df = df.drop_duplicates()
    print(f"Duplicados exactos eliminados: {antes - len(df)}")

    antes = len(df)
    df = df[df["nit"].isna() | ~df.duplicated(subset=["nit"], keep="first")]
    print(f"Empresas con nit repetido eliminadas: {antes - len(df)}")
    return df.reset_index(drop=True)


# leo el archivo sucio, limpio columna por columna y guardo el resultado
def limpiar_empresas(ruta_entrada=RUTA_ENTRADA, ruta_salida=RUTA_SALIDA):
    if not os.path.isfile(ruta_entrada):
        raise FileNotFoundError(
            f"No encuentro {ruta_entrada}. Primero hay que simular los datos."
        )
    df = leer_empresas(ruta_entrada)
    faltan = faltan_columnas(df)
    if faltan:
        raise ValueError("Faltan columnas en el archivo: " + ", ".join(faltan))

    mostrar_estado(df, "ANTES DE LIMPIAR")

    print("\n--- Limpiando ---")
    df = limpiar_nombre(df)
    df = limpiar_nit(df)
    df = limpiar_sector(df)
    df = limpiar_contacto(df)
    df = limpiar_correo(df)
    df = limpiar_telefono(df)
    df = limpiar_activa(df)
    df = quitar_duplicados(df)

    mostrar_estado(df, "DESPUÉS DE LIMPIAR")

    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
    df.to_csv(ruta_salida, index=False, encoding="utf-8")
    print(f"\nArchivo limpio guardado en {ruta_salida}")
    return df


if __name__ == "__main__":
    try:
        limpiar_empresas()
    except (FileNotFoundError, ValueError) as error:
        print(error, file=sys.stderr)
        sys.exit(1)