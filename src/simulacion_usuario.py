""" # 7 preparcion la simulacion para ensuciar mis datos    

# 7.1 FUNCION PARA OBTENER UNA MUESTRA DE LOs datos 

from numpy import random


def obtener_muestra(datos,porcentaje):
    return datos.sample(fraccion=porcentaje, random_state=random.randint(1, 9999)).index


# 7.2 funcion auxiliar para cambiar valores de un texto 

def escribir_mal(texto):
    variantes=[texto.lower(),texto.title(),texto.capitalize(),f" {texto}.", "Andres"]
    random.choice(variantes)


# 7.3Funcion AUXILIAR PARA CAMBIAR LOS BOOLEANOS


def convertir_booleano(valor):
    if valor:
        return random.choice(["SI","1"])
    else:
        return random.choice(["NO","0"])

#7.4 funcion principal para ensuciar los datos simulados

def ensuciar (datos_df):
    datos_df=datos_df.copy()

    #nombre el 10% tenga espacios y 8% este en mayuscula
    filas_elegidas=obtener_muestra(datos_df,0.10)

   datos_df.loc[filas_elegidas,"nombre"]=" "+datos_df.loc[filas_elegidas,"nombre"]

    filas_elegidas_muestra(datos_df,0.08)
    datos_df.loc[filas_elegidas,"nombre"]=datos_df.loc[filas_elegidas,"nombre"].str.upper()


    # correo: el 5% de los datos este sin @ 

    filas_elegidas=obtener_muestra(datos_df,0.05)
datos_df.loc[filas_elegidas,"correo"]=datos_df.loc[filas_elegidas,"correo"].str.replace("@","")




# correo: el 4% de los correo  no deberia tener ningun valor  (none) 

filas_elegidas=obtener_muestra(datos_df,0.04)
datos_df.loc[filas_elegidas,"correo"]=None


# rol Aplicar errores de escritura (variantes )
filas_elegidas=obtener_muestra(datos_df,0.5)
datos_df.loc[filas_elegidas,"rol"]=datos_df.loc[fila_elegidas,"rol"].map(escribir_mal)

#activo: en ocaciones llega Si, no, 1, 0

datos_df["activo"]=datos_df["activo"].astype(object)
filas_elegidas=obtener_muestra(datos_df,0.15)
datos_df.loc[filas_elegidas,"activo"]=datos_df.loc[filas_elegidas,"activo"].map(convertir_booleano)


# Mezclar el formato
# ISO  2026-10-03 YYY-mm-dd HH:MM:SS
#Latino => d/m/Y H:M

iso=datos_df["fecha_registro"].dt.strftime("%Y-%m-%d %H:%M:%S")
latino=datos_df["fecha_registro"].dt.strftime("%d/%m/%Y %H:%M")
datos_df["fecha_registro"]=iso
filas_elegidas=obtener_muestra(datos_df,0.25)
datos_df """