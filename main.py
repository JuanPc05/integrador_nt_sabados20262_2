import pandas as pd

from notebook.simulaciones.simular_usuarios import generar_datos_limpios,ensuciar
from notebook.simulaciones.simulacion_categorias import generar_categorias,_ensuciar_categorias


from notebook.exportaciones.exportacion import exportar_usuarios_crudos
from notebook.exportaciones.exportacion import exportar_categorias_crudos



print ("***** SIMULACION *****")
usuarios_df=pd.DataFrame(generar_datos_limpios())
usuarios_sucios_df=ensuciar(usuarios_df)
categorias_df=pd.DataFrame(generar_datos_limpios())
categorias_sucios_df=ensuciar(categorias_df)


#.head significa que va a traer los primeros 20 datos
print (usuarios_sucios_df.head(20))
print(categorias_sucios_df.head(20))


print ("***** EXPORTACION O GENERACION DE ARCHIVOS CON DATOS")
rutas_creadas_usuarios=exportar_usuarios_crudos(usuarios_sucios_df)
rutas_creadas_categorias=exportar_categorias_crudos(categorias_sucios_df)


print("archivos creados ...")