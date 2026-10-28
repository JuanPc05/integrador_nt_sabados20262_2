from pathlib import Path
from notebook.simulaciones.simular_registros import generar_registros, FILAS

# 1. rutas y nombres
NOMBRE_ENTIDAD = "registros"
CARPETA_PROYECTO = Path(__file__).resolve().parents[2]
CARPETA_CRUDO = CARPETA_PROYECTO / "data" / "crudo"

# 2. una funcion por formato
def preparar_carpeta(carpeta):
    carpeta.mkdir(parents=True, exist_ok=True)
    return carpeta

def exportar_csv(datos_df, carpeta, nombre_archivo):
    ruta = preparar_carpeta(carpeta) / f"{nombre_archivo}.csv"
    datos_df.to_csv(ruta, index=False, encoding="utf-8")
    return ruta

def exportar_excel(datos_df, carpeta, nombre_archivo):
    ruta = preparar_carpeta(carpeta) / f"{nombre_archivo}.xlsx"
    datos_df.to_excel(ruta, index=False, sheet_name="registros")
    return ruta

def exportar_json(datos_df, carpeta, nombre_archivo):
    ruta = preparar_carpeta(carpeta) / f"{nombre_archivo}.json"
    datos_df.to_json(ruta, orient="records", force_ascii=False, indent=2)
    return ruta

# 3. creo los tres archivos
def exportar_registros(datos_df_sucio):
    nombre = f"{NOMBRE_ENTIDAD}_sucio"
    return [
        exportar_csv(datos_df_sucio, CARPETA_CRUDO, nombre),
        exportar_excel(datos_df_sucio, CARPETA_CRUDO, nombre),
        exportar_json(datos_df_sucio, CARPETA_CRUDO, nombre),
    ]

# 4. ejecutar
if __name__ == "__main__":
    df = generar_registros(FILAS)
    for ruta in exportar_registros(df):
        print(f"{ruta.relative_to(CARPETA_PROYECTO)} | shape: {df.shape}")