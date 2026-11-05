import pandas as pd
from pathlib import Path

# 1. Definición de rutas respetando la estructura notebook/limpieza/
# Al estar en notebook/limpieza/limpiar_categorias.py, subimos 2 niveles para llegar a la raíz
CARPETA_PROYECTO = Path(__file__).resolve().parents[2]
RUTA_CRUDO = CARPETA_PROYECTO / "data" / "crudo" / "categorias_sucio.csv"
CARPETA_LIMPIO = CARPETA_PROYECTO / "data" / "limpio"

def limpiar_datos():
    # Asegurar que exista la carpeta de destino
    CARPETA_LIMPIO.mkdir(parents=True, exist_ok=True)
    
    # 2. Cargar los datos
    print("Iniciando proceso de limpieza...\n")
    df = pd.read_csv(RUTA_CRUDO)
    
    # 3. Diagnóstico Inicial (El "Antes")
    filas_antes = df.shape[0]
    print("--- DIAGNÓSTICO INICIAL (ANTES) ---")
    print(f"Shape: {df.shape}")
    print("\nInfo:")
    df.info()
    print("\nNulos por columna:")
    print(df.isna().sum())
    print(f"\nDuplicados exactos encontrados: {df.duplicated().sum()}")
    print("-" * 40 + "\n")

    # 4. Limpieza: Eliminar duplicados exactos
    df = df.drop_duplicates()

    # 5. Limpieza: Estandarizar la columna 'nombre'
    # a) Quitar espacios sobrantes y poner formato Título
    df["nombre"] = df["nombre"].str.strip().str.title()
    # b) Quitar tildes (normalizar caracteres especiales)
    df["nombre"] = df["nombre"].str.normalize("NFKD").str.encode("ascii", "ignore").str.decode("utf-8")

    # 6. Limpieza: Rellenar valores nulos (Imputación)
    df["descripcion"] = df["descripcion"].fillna("Sin descripcion")
    df["area_responsable"] = df["area_responsable"].fillna("Sin asignar")

    # 7. Transformación: Crear nueva columna 'largo_desc'
    df["largo_desc"] = df["descripcion"].str.len()

    # 8. Extraer y guardar el catálogo real (Valores únicos de categorías)
    df_catalogo = df.drop_duplicates(subset=["nombre"])
    ruta_catalogo = CARPETA_LIMPIO / "categorias_catalogo.csv"
    df_catalogo.to_csv(ruta_catalogo, index=False, encoding="utf-8")
    
    # 9. Guardar el dataset limpio
    ruta_limpio = CARPETA_LIMPIO / "categorias_limpio.csv"
    df.to_csv(ruta_limpio, index=False, encoding="utf-8")

    # 10. Diagnóstico Final (El "Después")
    filas_despues = df.shape[0]
    filas_eliminadas = filas_antes - filas_despues
    
    print("--- RESULTADOS DE LA LIMPIEZA (DESPUÉS) ---")
    print(f"Filas originales: {filas_antes}")
    print(f"Filas finales: {filas_despues}")
    print(f"Filas eliminadas (duplicados): {filas_eliminadas}")
    print(f"\nNuevo Shape: {df.shape}")
    print("\nNulos restantes por columna:")
    print(df.isna().sum())
    print(f"\nArchivos guardados en:\n- {ruta_limpio.relative_to(CARPETA_PROYECTO)}\n- {ruta_catalogo.relative_to(CARPETA_PROYECTO)}")

if __name__ == "__main__":
    limpiar_datos()