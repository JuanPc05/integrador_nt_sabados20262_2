import sys
from pathlib import Path
import pandas as pd

def limpiar_prioridades():
    """
    Función encargada de leer el dataset crudo de prioridades,
    limpiar duplicados, imputar nulos y exportar los datos limpios.
    """
    # Definición de rutas relativas
    CARPETA_PROYECTO = Path(__file__).resolve().parents[2]
    RUTA_CRUDO = CARPETA_PROYECTO / "data" / "crudo" / "prioridades_sucio.csv"
    CARPETA_LIMPIO = CARPETA_PROYECTO / "data" / "limpio"
    RUTA_LIMPIO = CARPETA_LIMPIO / "prioridades_limpio.csv"
    RUTA_CATALOGO = CARPETA_LIMPIO / "prioridades_catalogo.csv"

    NIVELES = {
        "Critica": 0,
        "Urgente": 1,
        "Alta": 2,
        "Media": 3,
        "Baja": 4
    }

    # Validación de seguridad: Comprobar si el archivo existe antes de procesar
    if not RUTA_CRUDO.exists():
        print(f"Error: No se encontró el archivo a limpiar en la ruta:\n{RUTA_CRUDO}")
        return

    # --- INICIO DEL PROCESAMIENTO PANDAS ---
    df = pd.read_csv(RUTA_CRUDO)
    
    filas_antes = df.shape[0]
    
    print("--- DIAGNÓSTICO INICIAL (PRIORIDADES) ---")
    print(f"Shape: {df.shape}")
    print("\nInfo:")
    df.info()
    print("\nNulos por columna:")
    print(df.isna().sum())
    print(f"\nDuplicados exactos: {df.duplicated().sum()}")
    print("-" * 30)

    # Limpieza
    df = df.drop_duplicates()

    df["nombre"] = df["nombre"].str.strip().str.capitalize()

    mapa_palabras = {"cero": 0, "uno": 1, "dos": 2, "tres": 3, "cuatro": 4}
    df["nivel"] = df["nivel"].replace(mapa_palabras)
    df["nivel"] = pd.to_numeric(df["nivel"], errors="coerce")

    # Imputación basada en diccionario
    df["nivel"] = df["nivel"].fillna(df["nombre"].map(NIVELES))

    df["dias_max_respuesta"] = pd.to_numeric(df["dias_max_respuesta"], errors="coerce")
    
    # Manejo de outliers e imputación con mediana
    df.loc[df["dias_max_respuesta"] > 60, "dias_max_respuesta"] = None
    mediana_dias = df["dias_max_respuesta"].median()
    df["dias_max_respuesta"] = df["dias_max_respuesta"].fillna(mediana_dias)

    # --- CREACIÓN DE DIRECTORIOS Y EXPORTACIÓN ---
    CARPETA_LIMPIO.mkdir(parents=True, exist_ok=True)

    df_catalogo = df.drop_duplicates(subset=["nombre"])
    df_catalogo.to_csv(RUTA_CATALOGO, index=False, encoding="utf-8")

    filas_despues = df.shape[0]
    filas_eliminadas = filas_antes - filas_despues

    print("\n--- DIAGNÓSTICO FINAL (PRIORIDADES) ---")
    print(f"Shape: {df.shape}")
    print("\nInfo:")
    df.info()
    print("\nNulos por columna:")
    print(df.isna().sum())
    print(f"\nFilas eliminadas en total: {filas_eliminadas}")
    print("-" * 30)

    df.to_csv(RUTA_LIMPIO, index=False, encoding="utf-8")


# Esto permite que el script se pueda probar solo, o se pueda importar desde main.py
if __name__ == "__main__":
    limpiar_prioridades()