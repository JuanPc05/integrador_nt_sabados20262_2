"""Consultas de la HU Q01 sobre la tabla retos (archivo LIMPIO).

Lee    data/limpio/retos_limpio.csv
Guarda data/limpio/retos_consulta_N.csv  (N = 1 a 5)

Uso directo:
    python notebook/consultas/consultas_retos.py
"""
import sys
from pathlib import Path

import pandas as pd

# 1. Rutas y nombres
NOMBRE_ENTIDAD = "retos"

# El script está en 'notebook/consultas/'. La raíz del proyecto está 2 niveles arriba.
CARPETA_PROYECTO = Path(__file__).resolve().parents[2]
CARPETA_LIMPIO = CARPETA_PROYECTO / "data" / "limpio"
RUTA_ENTRADA = CARPETA_LIMPIO / f"{NOMBRE_ENTIDAD}_limpio.csv"

COLUMNAS = ["id", "nombre", "estado", "duracion_dias", "fecha_inicio"]


# 2. Carga y guardado
def cargar_datos(ruta=RUTA_ENTRADA):
    """Lee el CSV limpio, valida las columnas y convierte los tipos."""
    df = pd.read_csv(ruta)
    faltan = [c for c in COLUMNAS if c not in df.columns]
    if faltan:
        raise ValueError(f"Faltan columnas en {ruta}: {faltan}")
    df["duracion_dias"] = pd.to_numeric(df["duracion_dias"], errors="coerce")
    df["fecha_inicio"] = pd.to_datetime(df["fecha_inicio"], errors="coerce")
    return df


def guardar(resultado, carpeta, n, indice=True):
    """Guarda el resultado de la consulta N como retos_consulta_N.csv."""
    resultado.to_csv(Path(carpeta) / f"{NOMBRE_ENTIDAD}_consulta_{n}.csv", index=indice)


# 3. Las cinco consultas (cada una en su función)
def consulta_1(df, carpeta):
    """Consulta 1: ¿Qué retos están en curso?"""
    print("\n=== Consulta 1: ¿Qué retos están en curso? ===")
    en_curso = df[df["estado"] == "EN_CURSO"]
    print(en_curso.to_string(index=False))
    guardar(en_curso, carpeta, 1, indice=False)
    return en_curso


def consulta_2(df, carpeta):
    """Consulta 2: ¿Cuáles son los 10 retos más largos?"""
    print("\n=== Consulta 2: ¿Cuáles son los 10 retos más largos? ===")
    largos = df.nlargest(10, "duracion_dias")[["nombre", "duracion_dias", "estado"]]
    print(largos.to_string(index=False))
    guardar(largos, carpeta, 2, indice=False)
    return largos


def consulta_3(df, carpeta):
    """Consulta 3: ¿Cuántos retos hay por estado?"""
    print("\n=== Consulta 3: ¿Cuántos retos hay por estado? ===")
    conteo = df["estado"].value_counts()
    print(conteo.to_string())
    guardar(conteo, carpeta, 3)
    return conteo


def consulta_4(df, carpeta):
    """Consulta 4 (GROUPBY): duración promedio, mínima y máxima por estado."""
    print("\n=== Consulta 4: ¿Cuál es la duración promedio, mínima y máxima por estado? ===")
    resumen = df.groupby("estado")["duracion_dias"].agg(["count", "mean", "min", "max"])
    resumen["mean"] = resumen["mean"].round(2)
    print(resumen.to_string())
    guardar(resumen, carpeta, 4)
    return resumen


def consulta_5(df, carpeta):
    """Consulta 5 (GROUPBY): ¿cuántos retos empiezan cada mes?"""
    print("\n=== Consulta 5: ¿Cuántos retos empiezan cada mes? ===")
    por_mes = df.groupby(df["fecha_inicio"].dt.to_period("M"))["id"].count()
    por_mes.name = "retos"
    print(por_mes.to_string())
    guardar(por_mes, carpeta, 5)
    return por_mes


# 4. Flujo completo
def consultar_retos(ruta_entrada=RUTA_ENTRADA, carpeta_salida=CARPETA_LIMPIO):
    """Lee el archivo limpio y corre las 5 consultas en orden."""
    df = cargar_datos(ruta_entrada)
    for consulta in (consulta_1, consulta_2, consulta_3, consulta_4, consulta_5):
        consulta(df, carpeta_salida)
    print(f"\nListo: 5 archivos {NOMBRE_ENTIDAD}_consulta_N.csv guardados en "
          f"{Path(carpeta_salida).relative_to(CARPETA_PROYECTO)}/")


# 5. Ejecutar
if __name__ == "__main__":
    if not RUTA_ENTRADA.is_file():
        sys.exit(f"No se encontró el archivo: {RUTA_ENTRADA}")
    consultar_retos()