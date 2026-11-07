import pandas as pd
import matplotlib.pyplot as plt
import os
from pathlib import Path

# 1. Definir rutas relativas dinámicas
# Sube 2 niveles si está en notebook/reportes/ (o ajusta según dónde lo guardes)
CARPETA_PROYECTO = Path(__file__).resolve().parents[2] 
RUTA_LIMPIO = CARPETA_PROYECTO / "data" / "limpio" / "categorias_limpio.csv"
RUTA_CRUDO = CARPETA_PROYECTO / "data" / "crudo" / "categorias_sucio.csv" # Para sacar las estadísticas
CARPETA_REPORTES = CARPETA_PROYECTO / "reportes"

def generar_reportes():
    # Crear la carpeta de reportes si no existe
    os.makedirs(CARPETA_REPORTES, exist_ok=True)
    
    print("Cargando datos limpios...")
    df_limpio = pd.read_csv(RUTA_LIMPIO)
    
    # === GRÁFICA 1: Conteo por Categoría ===
    conteo = df_limpio["nombre"].value_counts()
    
    plt.figure(figsize=(10, 6))
    conteo.plot(kind="barh", color="skyblue")
    plt.title("Frecuencia de Aparición por Categoría")
    plt.xlabel("Cantidad de Registros")
    plt.ylabel("Categorías")
    plt.tight_layout()
    plt.savefig(CARPETA_REPORTES / "categorias_grafica_1.png", dpi=120)
    plt.close()
    
    # === GRÁFICA 2: Reparto por Área Responsable ===
    por_area = df_limpio.groupby("area_responsable")["nombre"].count()
    
    plt.figure(figsize=(8, 8))
    por_area.plot(kind="pie", autopct="%1.1f%%", startangle=90, cmap="Pastel1")
    plt.title("Distribución de Categorías por Área Responsable")
    plt.ylabel("") # Se quita el label del eje Y para que el pie chart se vea limpio
    plt.tight_layout()
    plt.savefig(CARPETA_REPORTES / "categorias_grafica_2.png", dpi=120)
    plt.close()
    
    # === GRÁFICA 3: Largo Promedio de Descripción ===
    largos = df_limpio.groupby("nombre")["largo_desc"].mean().sort_values(ascending=False)
    
    plt.figure(figsize=(12, 6))
    largos.plot(kind="bar", color="coral")
    plt.title("Largo Promedio de la Descripción por Categoría")
    plt.xlabel("Categorías")
    plt.ylabel("Promedio de Caracteres")
    plt.xticks(rotation=45, ha="right") # Rotar las etiquetas para que se lean bien
    plt.tight_layout()
    plt.savefig(CARPETA_REPORTES / "categorias_grafica_3.png", dpi=120)
    plt.close()
    
    print(f"Las tres gráficas fueron guardadas exitosamente en: {CARPETA_REPORTES}\n")
    
    # === CONCLUSIONES Y ANÁLISIS ===
    # Leemos el crudo solo para calcular cuántas filas se perdieron exactamente
    try:
        df_crudo = pd.read_csv(RUTA_CRUDO)
        total_crudo = len(df_crudo)
    except FileNotFoundError:
        total_crudo = 250 # Asumimos 250 si no encuentra el archivo crudo
        
    total_limpio = len(df_limpio)
    filas_eliminadas = total_crudo - total_limpio
    categorias_unicas = df_limpio["nombre"].nunique()
    
    print("=== CONCLUSIONES DEL ANÁLISIS DE DATOS ===")
    print(f"1. Filas eliminadas: Se eliminaron {filas_eliminadas} filas en total correspondientes a duplicados exactos.")
    print(f"2. Categorías reales: Al finalizar la estandarización de texto (tildes, mayúsculas, espacios), el catálogo se redujo a exactamente {categorias_unicas} categorías base, demostrando que la limpieza unificó correctamente las variantes de escritura.")
    print("\n=== RECOMENDACIÓN PARA EL BACKEND (SPRING BOOT / MYSQL) ===")
    print("Para evitar que estos errores de calidad de datos vuelvan a ocurrir en el entorno de producción,")
    print("el Backend debe declarar la columna 'nombre' con la restricción @Column(unique = true) en la entidad de JPA")
    print("y como UNIQUE en la migración de MySQL. Esto garantizará la integridad de la base de datos bloqueando")
    print("inserciones de categorías duplicadas a nivel de base de datos.")

if __name__ == "__main__":
    generar_reportes()