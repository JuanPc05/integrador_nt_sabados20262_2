import pandas as pd

# 1. Importar simulaciones
from notebook.simulaciones.simular_empresa import generar_empresas
from notebook.simulaciones.simular_registros import generar_registros
from notebook.simulaciones.simular_usuarios import generar_datos_limpios, ensuciar
from notebook.simulaciones.simulacion_categorias import generar_categorias

# 2. Importar exportaciones creadas hasta el momento (Enfoque 1: un archivo por entidad)
from notebook.exportaciones.exportacion_empresas import exportar_empresas
from notebook.exportaciones.exportar_registros import exportar_registros
# NOTA: Los demás compañeros agregarán sus exportadores cuando suban su respectivo script:
# from notebook.exportaciones.exportar_usuarios import exportar_usuarios
# from notebook.exportaciones.exportar_categorias import exportar_categorias


print("***** SIMULACION *****")
# Generar datos simulados
empresas_sucias_df = generar_empresas()
registros_sucios_df = generar_registros()

usuarios_df = pd.DataFrame(generar_datos_limpios())
usuarios_sucios_df = ensuciar(usuarios_df)

categorias_sucias_df = generar_categorias()

# Mostrar muestra de datos (primeras 5 filas)
print("\n--- EMPRESAS (Muestra) ---")
print(empresas_sucias_df.head(5))

print("\n--- REGISTROS (Muestra) ---")
print(registros_sucios_df.head(5))

print("\n--- USUARIOS (Muestra) ---")
print(usuarios_sucios_df.head(5))

print("\n--- CATEGORIAS (Muestra) ---")
print(categorias_sucias_df.head(5))


print("\n***** EXPORTACION O GENERACION DE ARCHIVOS CON DATOS *****")
# Exportar las entidades que ya tienen su script de exportación listo:
rutas_empresas = exportar_empresas(empresas_sucias_df)
print(f"Empresas exportadas: {len(rutas_empresas)} archivos en data/crudo")

rutas_registros = exportar_registros(registros_sucios_df)
print(f"Registros exportados: {len(rutas_registros)} archivos en data/crudo")

# NOTA: A medida que cada compañero termine su archivo en 'exportaciones/',
# se conectará aquí para exportar todo desde main:
# rutas_usuarios = exportar_usuarios(usuarios_sucios_df)
# rutas_categorias = exportar_categorias(categorias_sucias_df)

print("\nArchivos creados exitosamente.")