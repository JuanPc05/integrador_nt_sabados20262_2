import sys
from pathlib import Path

# 1. Rutas y nombres
NOMBRE_ENTIDAD = "prioridades"
CARPETA_PROYECTO = Path(__file__).resolve().parents[2]
CARPETA_CRUDO = CARPETA_PROYECTO / "data" / "crudo"

# Asegurar que la raíz del proyecto esté en sys.path para permitir ejecución directa
if str(CARPETA_PROYECTO) not in sys.path:
    sys.path.insert(0, str(CARPETA_PROYECTO))

from notebook.simulaciones.simular_prioridades import generar_prioridades, FILAS


# 2. Funciones para guardar los archivos
def preparar_carpeta(carpeta):
    carpeta.mkdir(parents=True, exist_ok=True)
    return carpeta


def exportar_csv(datos_df, carpeta, nombre_archivo):
    ruta = preparar_carpeta(carpeta) / f"{nombre_archivo}.csv"
    datos_df.to_csv(ruta, index=False, encoding="utf-8")
    return ruta


def exportar_excel(datos_df, carpeta, nombre_archivo):
    ruta = preparar_carpeta(carpeta) / f"{nombre_archivo}.xlsx"
    datos_df.to_excel(ruta, index=False, sheet_name="prioridades")
    return ruta


def exportar_json(datos_df, carpeta, nombre_archivo):
    ruta = preparar_carpeta(carpeta) / f"{nombre_archivo}.json"
    datos_df.to_json(ruta, orient="records", force_ascii=False, indent=2)
    return ruta


# 3. Crear los tres archivos
def exportar_prioridades(datos_df_sucio):
    nombre = f"{NOMBRE_ENTIDAD}_sucio"
    return [
        exportar_csv(datos_df_sucio, CARPETA_CRUDO, nombre),
        exportar_excel(datos_df_sucio, CARPETA_CRUDO, nombre),
        exportar_json(datos_df_sucio, CARPETA_CRUDO, nombre),
    ]


# 4. Ejecutar
if __name__ == "__main__":
    df = generar_prioridades(FILAS)
    rutas = exportar_prioridades(df)

    for ruta in rutas:
        print(f"{ruta.relative_to(CARPETA_PROYECTO)} | shape: {df.shape}")

