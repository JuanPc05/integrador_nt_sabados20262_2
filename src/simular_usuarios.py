import random 
import uuid
import pandas as pd
from faker import Faker

#1. Sembrar semillas para los datos a simular
random.seed(42)
Faker.seed(42)

#2. IdentiFicar los datos a simular con su tipo de dato
#id (texto (UUID)), 
#nombre (texto), 
#correo (texto), 
#contrasena_hash (texto), 
#rol (texto), 
#activo (booleano), 
#fecha_registro (fecha y hora).

#3. ESTABLECER UNA CONSTANTE PARA EL NUEMRO DE SIMULACIONS
FILAS=400
ROLES=["administrador","empresario","estudiante","profesor"]
FALSITO=Faker("es_CO")

#4. Funcion generadora
def generar_datos(numero_filas=400):
    usuarios=[]
    for _ in range(numero_filas):
        usuarios.append({
            "id":str(uuid.uuid4()),
            "nombre":FALSITO.name(),
            "correo":FALSITO.email(),
            "contrasena_hash":FALSITO.sha256(),
            "activo":random.choice([True,False]),
            "rol":random.choice(ROLES),
            "fecha_registro":FALSITO.date_time_between(start_date="-2y", end_date="now")
        })
    return usuarios

#5. Conviertindo los datos generados en un dataframe con PANDAS
tabla_ordenada_usuarios=pd.DataFrame(generar_datos())

#6. Probar la funcion (Opcional: puedes comentarlo si solo quieres ver la final)
# print("--- DATOS LIMPIOS ---")
# print(tabla_ordenada_usuarios.head())

#7.1 funcion para ensuciar una muestra de los datos
def obtener_muestra(datos, porcentaje):
    # CORRECCIÓN: 'fraccion' cambiado a 'frac'
    return datos.sample(frac=porcentaje, random_state=random.randint(0, 999)).index

#7.2 Funcion auxiliar para cambiar valores de un texto 
def escribir_mal(texto): 
    variantes=[texto.lower(),texto.title(),texto.capitalize(),f" {texto} ", "Andres Florez"]
    return random.choice(variantes)

#7.3 funcion auxiliar para cambiar los booleanos
def convertir_booleano(valor):
    if valor:
        return random.choice(["SI", "1"])
    else: 
        # CORRECCIÓN: Se agregaron los corchetes para formar la lista
        return random.choice(["NO", "0"])

#7.4 Funcion principal para ensuciar los datos simulados
def ensuciar(datos_df):
    datos_df=datos_df.copy()
    
    filas_elegidas=obtener_muestra(datos_df,0.1)
    datos_df.loc[filas_elegidas, "nombre"] = " " +datos_df.loc[filas_elegidas, "nombre"] + " "

    filas_elegidas=obtener_muestra(datos_df,0.08)
    datos_df.loc[filas_elegidas, "nombre"] = datos_df.loc[filas_elegidas, "nombre"].str.upper()

    filas_elegidas=obtener_muestra(datos_df, 0.05)
    datos_df.loc[filas_elegidas, "correo"]=datos_df.loc[filas_elegidas, "correo"].str.replace("@","")
    
    # CORRECCIÓN: Retornar el dataframe modificado para que no se pierda
    return datos_df

# CORRECCIÓN FINAL: Llamar a la función y guardar el resultado
tabla_sucia = ensuciar(tabla_ordenada_usuarios)

print("\n--- DATOS SUCIOS ---")
print(tabla_sucia.head(15))