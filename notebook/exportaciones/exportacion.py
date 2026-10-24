import os
from importlib import import_module
from pathlib import Path

# 1. Rutas y nombres
NOMBRE_ENTIDAD = "empresas"
CARPETA_PROYECTO = Path(__file__).resolve().parent.parent
CARPETA_CRUDO = CARPETA_PROYECTO / "data" / "crudo"
CARPETA_LIMPIO = CARPETA_PROYECTO / "data" / "limpio"
CARPETA_REPORTES = CARPETA_PROYECTO / "reportes"

# Traigo la función del script anterior (cambio el nombre si mi archivo se llama distinto)
generar_empresas = import_module("simulaciones.simular_empresa").generar_empresas


# 2. Funciones para guardar los archivos
def preparar_carpeta(carpeta):
    # Creo la carpeta si no existe
    os.makedirs(carpeta, exist_ok=True)
    return carpeta


def exportar_csv(datos_df, carpeta, nombre_archivo):
    ruta = Path(preparar_carpeta(carpeta)) / f"{nombre_archivo}.csv"
    datos_df.to_csv(ruta, index=False, encoding="utf-8")
    return ruta


def exportar_excel(datos_df, carpeta, nombre_archivo):
    ruta = Path(preparar_carpeta(carpeta)) / f"{nombre_archivo}.xlsx"
    datos_df.to_excel(ruta, index=False, sheet_name="empresas")
    return ruta


def exportar_json(datos_df, carpeta, nombre_archivo):
    ruta = Path(preparar_carpeta(carpeta)) / f"{nombre_archivo}.json"
    datos_df.to_json(ruta, orient="records", force_ascii=False, indent=2)
    return ruta


# 3. Crear los tres archivos
def exportar_empresas(datos_df_sucio):
    nombre = f"{NOMBRE_ENTIDAD}_sucio"
    return [
        exportar_csv(datos_df_sucio, CARPETA_CRUDO, nombre),
        exportar_excel(datos_df_sucio, CARPETA_CRUDO, nombre),
        exportar_json(datos_df_sucio, CARPETA_CRUDO, nombre),
    ]


# 4. Ejecutar
if __name__ == "__main__":
    df = generar_empresas()
    rutas = exportar_empresas(df)

    # Muestro la ruta y el tamaño de cada archivo
    for ruta in rutas:
        print(f"{ruta} | shape: {df.shape}")