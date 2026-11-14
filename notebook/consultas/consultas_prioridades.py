from pathlib import Path
import pandas as pd

CARPETA_PROYECTO = Path(__file__).resolve().parents[2]
RUTA_LIMPIO = CARPETA_PROYECTO / "data" / "limpio" / "prioridades_limpio.csv"
CARPETA_SALIDA = CARPETA_PROYECTO / "data" / "limpio"

def consulta_1_ordenadas(df):
    print("\n--- Consulta 1: Prioridades ordenadas de la mas urgente a la menos urgente ---")
    ordenadas = df.sort_values("nivel")
    print(ordenadas.head())
    ruta = CARPETA_SALIDA / "prioridades_consulta_1.csv"
    ordenadas.to_csv(ruta, index=False, encoding="utf-8")

def consulta_2_urgentes(df):
    print("\n--- Consulta 2: Solo las prioridades urgentes (nivel 1 y 2) ---")
    urgentes = df[df["nivel"] <= 2]
    print(urgentes.head())
    ruta = CARPETA_SALIDA / "prioridades_consulta_2.csv"
    urgentes.to_csv(ruta, index=False, encoding="utf-8")

def consulta_3_conteo(df):
    print("\n--- Consulta 3: Cuantas veces aparece cada nombre ---")
    conteo = df["nombre"].value_counts()
    print(conteo)
    ruta = CARPETA_SALIDA / "prioridades_consulta_3.csv"
    conteo.to_csv(ruta, header=["cantidad"], index_label="nombre", encoding="utf-8")

def consulta_4_agrupacion_nivel(df):
    print("\n--- Consulta 4: Cuantas filas hay por nivel (GROUPBY) ---")
    por_nivel = df.groupby("nivel")["id"].count()
    print(por_nivel)
    ruta = CARPETA_SALIDA / "prioridades_consulta_4.csv"
    por_nivel.to_csv(ruta, header=["cantidad"], index_label="nivel", encoding="utf-8")

def consulta_5_resumen_dias(df):
    print("\n--- Consulta 5: Dias de respuesta minimo, promedio y maximo por prioridad (GROUPBY) ---")
    resumen = df.groupby("nombre")["dias_max_respuesta"].agg(["min", "mean", "max"]).round(1)
    print(resumen)
    ruta = CARPETA_SALIDA / "prioridades_consulta_5.csv"
    resumen.to_csv(ruta, encoding="utf-8")

def ejecutar_consultas():
    """
    Función principal que lee los datos limpios y ejecuta todas las consultas.
    Esta es la función que importa main.py.
    """
    if not RUTA_LIMPIO.exists():
        print(f"Error: No se encontró el archivo limpio en:\n{RUTA_LIMPIO}")
        return
        
    df_limpio = pd.read_csv(RUTA_LIMPIO)
    
    consulta_1_ordenadas(df_limpio)
    consulta_2_urgentes(df_limpio)
    consulta_3_conteo(df_limpio)
    consulta_4_agrupacion_nivel(df_limpio)
    consulta_5_resumen_dias(df_limpio)

# Punto de entrada estandarizado para pruebas aisladas
if __name__ == "__main__":
    ejecutar_consultas()