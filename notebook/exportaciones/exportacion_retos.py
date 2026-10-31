import os
import sys
from pathlib import Path

# 1. Rutas y nombres
NOMBRE_ENTIDAD = "retos"

# El script está en 'src/'. La raíz del proyecto está 1 nivel arriba.
CARPETA_PROYECTO = Path(__file__).resolve().parents[1]
CARPETA_CRUDO = CARPETA_PROYECTO / "data" / "crudo"

# Permite ejecutar directamente: python src/exportar_retos.py
if str(CARPETA_PROYECTO) not in sys.path:
    sys.path.insert(0, str(CARPETA_PROYECTO))

# Se importa la generación; NO se copia su código
from src.simular_retos import generar_retos, FILAS


# 2. Funciones para guardar los archivos
def preparar_carpeta(carpeta_path):
    os.makedirs(carpeta_path, exist_ok=True)
    return Path(carpeta_path)


def exportar_csv(datos_df, carpeta, nombre_archivo):
    ruta = preparar_carpeta(carpeta) / f"{nombre_archivo}.csv"
    datos_df.to_csv(ruta, index=False, encoding="utf-8")
    return ruta


def exportar_excel(datos_df, carpeta, nombre_archivo):
    ruta = preparar_carpeta(carpeta) / f"{nombre_archivo}.xlsx"
    datos_df.to_excel(ruta, index=False, sheet_name="retos")
    return ruta


def exportar_json(datos_df, carpeta, nombre_archivo):
    ruta = preparar_carpeta(carpeta) / f"{nombre_archivo}.json"
    datos_df.to_json(ruta, orient="records", force_ascii=False, indent=2)
    return ruta


# 3. Crear los tres archivos
def exportar_registros_retos(datos_df_sucio):
    nombre = f"{NOMBRE_ENTIDAD}_sucio"
    return [
        exportar_csv(datos_df_sucio, CARPETA_CRUDO, nombre),
        exportar_excel(datos_df_sucio, CARPETA_CRUDO, nombre),
        exportar_json(datos_df_sucio, CARPETA_CRUDO, nombre),
    ]


# 4. Ejecutar
if __name__ == "__main__":
    df = generar_retos(FILAS)
    rutas = exportar_registros_retos(df)

    print("=== ARCHIVOS GENERADOS ===")
    for ruta in rutas:
        print(f"Ruta: {ruta.relative_to(CARPETA_PROYECTO)} | shape: {df.shape}")