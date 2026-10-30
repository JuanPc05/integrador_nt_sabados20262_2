import os
import sys
import pandas as pd

# 1. Ajuste de la ruta del sistema para evitar errores de importación (ModuleNotFoundError).
# Esto le dice a Python que la raíz del proyecto es el directorio base.
ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(ruta_raiz)

# 2. Importación exacta basada en tu estructura de carpetas
from notebook.simulaciones.simulacion_categorias import generar_categorias

def exportar_archivos():
    print("Iniciando la generación de categorías sintéticas...")
    
    # Obtenemos el DataFrame ejecutando tu función
    # Se usa n=250 ya que es el parámetro por defecto que tienes definido
    df = generar_categorias(n=250)
    
    # Aseguramos que la carpeta data/crudo exista en la raíz del proyecto
    directorio_salida = os.path.join(ruta_raiz, "data", "crudo")
    os.makedirs(directorio_salida, exist_ok=True)
    
    # Definimos las rutas absolutas para cada archivo
    ruta_csv = os.path.join(directorio_salida, "categorias_sucio.csv")
    ruta_excel = os.path.join(directorio_salida, "categorias_sucio.xlsx")
    ruta_json = os.path.join(directorio_salida, "categorias_sucio.json")
    
    # --- EXPORTACIONES ---
    
    # CSV: index=False para evitar la columna de índice numérico, utf-8 para tildes
    df.to_csv(ruta_csv, index=False, encoding="utf-8")
    print(f"✅ CSV exportado: {ruta_csv} | Tamaño: {df.shape}")
    
    # EXCEL: sheet_name para nombrar la pestaña
    df.to_excel(ruta_excel, index=False, sheet_name="categorias")
    print(f"✅ Excel exportado: {ruta_excel} | Tamaño: {df.shape}")
    
    # JSON: orient="records" para crear el array de objetos estándar usado en frontend
    df.to_json(ruta_json, orient="records", force_ascii=False, indent=2)
    print(f"✅ JSON exportado: {ruta_json} | Tamaño: {df.shape}")
    
    print("\n🚀 ¡Todas las exportaciones de categorías finalizaron con éxito!")

if __name__ == "__main__":
    exportar_archivos()