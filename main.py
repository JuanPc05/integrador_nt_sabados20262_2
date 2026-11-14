import pandas as pd

from notebook.simulaciones.simular_empresa import generar_empresas
from notebook.simulaciones.simular_registros import generar_registros
from notebook.simulaciones.simular_usuarios import generar_usuarios
from notebook.simulaciones.simulacion_categorias import generar_categorias
from notebook.simulaciones.simular_retos import generar_retos
from notebook.simulaciones.simular_prioridades import generar_prioridades

from notebook.exportaciones.exportacion_empresas import exportar_empresas
from notebook.exportaciones.exportar_registros import exportar_registros
from notebook.exportaciones.exportar_categorias import exportar_categorias
from notebook.exportaciones.exportar_usuarios import exportar_usuarios
from notebook.exportaciones.exportar_prioridades import exportar_prioridades

from notebook.limpieza.limpiar_prioridades import ejecutar_limpieza as limpiar_prioridades
from notebook.consultas.consultas_prioridades import ejecutar_consultas as consultar_prioridades
from notebook.reportes.reporte_prioridades import generar_reportes as reportar_prioridades


print("***** SIMULACION *****")
empresas_sucias_df = generar_empresas()
usuarios_sucios_df = generar_usuarios()
categorias_sucias_df = generar_categorias()
prioridades_sucias_df = generar_prioridades()

retos_sucios_df = generar_retos(
    ids_empresa=empresas_sucias_df["id"].unique(),
    ids_categoria=categorias_sucias_df["id"].unique(),
    ids_prioridad=prioridades_sucias_df["id"].unique(),
)
registros_sucios_df = generar_registros(
    ids_usuario=usuarios_sucios_df["id"].unique(),
    ids_reto=retos_sucios_df["id"].unique(),
)


print("\n--- EMPRESAS (Muestra) ---")
print(empresas_sucias_df.head(5))

print("\n--- REGISTROS (Muestra) ---")
print(registros_sucios_df.head(5))

print("\n--- USUARIOS (Muestra) ---")
print(usuarios_sucios_df.head(5))

print("\n--- CATEGORIAS (Muestra) ---")
print(categorias_sucias_df.head(5))

print("\n--- RETOS (Muestra) ---")
print(retos_sucios_df.head(5))

print("\n--- PRIORIDADES (Muestra) ---")
print(prioridades_sucias_df.head(5))


print("\n***** EXPORTACION O GENERACION DE ARCHIVOS CON DATOS (CRUDOS) *****")
rutas_empresas = exportar_empresas(empresas_sucias_df)
print(f"Empresas exportadas: {len(rutas_empresas)} archivos en data/crudo")

rutas_registros = exportar_registros(registros_sucios_df)
print(f"Registros exportados: {len(rutas_registros)} archivos en data/crudo")

rutas_categorias = exportar_categorias(categorias_sucias_df)
print(f"Categorias exportadas: {len(rutas_categorias)} archivos en data/crudo")

rutas_usuarios = exportar_usuarios(usuarios_sucios_df)
print(f"Usuarios exportados: {len(rutas_usuarios)} archivos en data/crudo")

rutas_prioridades = exportar_prioridades(prioridades_sucias_df)
print(f"Prioridades exportadas: {len(rutas_prioridades)} archivos en data/crudo")


print("\n***** LIMPIEZA DE DATOS *****")
limpiar_prioridades()
print("Prioridades limpiadas y guardadas en data/limpio")


print("\n***** CONSULTAS *****")
consultar_prioridades()
print("Consultas de prioridades ejecutadas y guardadas en data/limpio")


print("\n***** REPORTES VISUALES *****")
reportar_prioridades()
print("Reportes graficos de prioridades guardados en la carpeta reportes/")

print("\nPipeline ejecutado exitosamente.")

print("\n***** LIMPIEZA, CONSULTAS Y REPORTE DE REGISTROS *****")
from notebook.limpieza.limpiar_registros import limpiar_registros
from notebook.consultas.consultas_registros import ejecutar_consultas
from notebook.reportes.reporte_registros import crear_reporte

limpiar_registros()
ejecutar_consultas()
crear_reporte()
