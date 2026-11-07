import pandas as pd
from pathlib import Path

# 1. Definición de rutas respetando tu arquitectura
# Subimos 2 niveles desde notebook/consultas/ para llegar a la raíz
CARPETA_PROYECTO = Path(__file__).resolve().parents[2]
RUTA_LIMPIO = CARPETA_PROYECTO / "data" / "limpio" / "categorias_limpio.csv"
CARPETA_DESTINO = CARPETA_PROYECTO / "data" / "limpio"

def consulta_1(df):
    print("\n=== CONSULTA 1: ¿Cuántas veces aparece cada categoría? ===")
    conteo = df["nombre"].value_counts()
    print(conteo)
    
    # Guardar resultado (Al ser una Serie de Pandas, se guarda con encabezados automáticos)
    ruta = CARPETA_DESTINO / "categorias_consulta_1.csv"
    conteo.to_csv(ruta, header=["cantidad"], index_label="nombre")

def consulta_2(df):
    print("\n=== CONSULTA 2: Categorías sin descripción ===")
    sin_desc = df[df["descripcion"] == "Sin descripcion"]
    print(f"Total de registros sin descripción: {len(sin_desc)}")
    print(sin_desc.head()) # Mostramos solo las primeras 5 para no saturar la consola
    
    ruta = CARPETA_DESTINO / "categorias_consulta_2.csv"
    sin_desc.to_csv(ruta, index=False, encoding="utf-8")

def consulta_3(df):
    print("\n=== CONSULTA 3 (GROUPBY): Largo promedio de la descripción por categoría ===")
    largos = df.groupby("nombre")["largo_desc"].mean().round(1).sort_values(ascending=False)
    print(largos)
    
    ruta = CARPETA_DESTINO / "categorias_consulta_3.csv"
    largos.to_csv(ruta, header=["promedio_caracteres"], index_label="nombre")

def consulta_4(df):
    print("\n=== CONSULTA 4 (GROUPBY): ¿Cuántas categorías maneja cada área? ===")
    por_area = df.groupby("area_responsable")["id"].count().sort_values(ascending=False)
    print(por_area)
    
    ruta = CARPETA_DESTINO / "categorias_consulta_4.csv"
    por_area.to_csv(ruta, header=["cantidad_categorias"], index_label="area_responsable")

def consulta_5(df):
    print("\n=== CONSULTA 5 (GROUPBY DOBLE): Categorías por área (Tabla cruzada) ===")
    # unstack() convierte el segundo nivel de la agrupación en columnas, llenando vacíos con 0
    tabla = df.groupby(["area_responsable", "nombre"])["id"].count().unstack(fill_value=0)
    print(tabla)
    
    ruta = CARPETA_DESTINO / "categorias_consulta_5.csv"
    tabla.to_csv(ruta, encoding="utf-8")

def ejecutar_consultas():
    # Asegurarnos de que el archivo limpio existe antes de consultar
    if not RUTA_LIMPIO.exists():
        print(f"Error: No se encontró el archivo {RUTA_LIMPIO}. Ejecuta primero el script de limpieza.")
        return

    print("Cargando el dataset limpio para análisis...")
    df = pd.read_csv(RUTA_LIMPIO)
    
    # Ejecución secuencial de las funciones
    consulta_1(df)
    consulta_2(df)
    consulta_3(df)
    consulta_4(df)
    consulta_5(df)
    
    print(f"\n¡Análisis completado! Los 5 archivos CSV se guardaron exitosamente en:\n{CARPETA_DESTINO.relative_to(CARPETA_PROYECTO)}")

if __name__ == "__main__":
    ejecutar_consultas()