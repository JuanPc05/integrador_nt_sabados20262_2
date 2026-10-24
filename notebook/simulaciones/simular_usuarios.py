import random 
import uuid
import pandas as pd
from faker import Faker

# 1. Sembrar semillas para los datos a simular
random.seed(42)
Faker.seed(42)

# 2. IdentiFicar los datos a simular con su tipo de dato
# id (texto (UUID)), nombre, correo, contrasena_hash, rol, activo, fecha_registro

# 3. ESTABLECER UNA CONSTANTE PARA EL NUEMRO DE SIMULACIONS
FILAS=400
ROLES=["administrador","empresario","estudiante","profesor"]
FALSITO=Faker("es_CO")

# 4. Funcion generadora
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

# 5. Conviertindo los datos generados en un dataframe con PANDAS
# (Lo dejamos como global tal como lo tenías, aunque es buena práctica instanciarlo abajo)
tabla_ordenada_usuarios=pd.DataFrame(generar_datos())

# 7.1 funcion para ensuciar una muestra de los datos
def obtener_muestra(datos, porcentaje):
    return datos.sample(frac=porcentaje, random_state=random.randint(0, 999)).index

# 7.2 Funcion auxiliar para cambiar valores de un texto 
def escribir_mal(texto): 
    variantes=[texto.lower(),texto.title(),texto.capitalize(),f" {texto} ", "Andres Florez"]
    return random.choice(variantes)

# 7.3 funcion auxiliar para cambiar los booleanos
def convertir_booleano(valor):
    if valor:
        return random.choice(["SI", "1"])
    else: 
        return random.choice(["NO", "0"])

# 7.4 Funcion principal para ensuciar los datos simulados
def ensuciar(datos_df):
    datos_df=datos_df.copy()
    
    filas_elegidas=obtener_muestra(datos_df,0.1)
    datos_df.loc[filas_elegidas, "nombre"] = " " +datos_df.loc[filas_elegidas, "nombre"] + " "

    filas_elegidas=obtener_muestra(datos_df,0.08)
    datos_df.loc[filas_elegidas, "nombre"] = datos_df.loc[filas_elegidas, "nombre"].str.upper()

    filas_elegidas=obtener_muestra(datos_df, 0.05)
    datos_df.loc[filas_elegidas, "correo"]=datos_df.loc[filas_elegidas, "correo"].str.replace("@","")

    # CORRECCIÓN 1: Se eliminó la línea "datos_df.loc[filas_elegidas, "rol"].map" incompleta.
    filas_elegidas=obtener_muestra(datos_df,0.05)
    datos_df.loc[filas_elegidas, "rol"]=datos_df.loc[filas_elegidas, "rol"].map(escribir_mal)

    datos_df["activo"]=datos_df["activo"].astype(object)
    filas_elegidas=obtener_muestra(datos_df,0.15)
    datos_df.loc[filas_elegidas,"activo"]=datos_df.loc[filas_elegidas,"activo"].map(convertir_booleano)

    iso=datos_df["fecha_registro"].dt.strftime("%Y-%m-%d %H:%M:%S")
    latino=datos_df["fecha_registro"].dt.strftime("%d/%m/%Y %H:%M")
    datos_df["fecha_registro"]=iso
    
    filas_elegidas=obtener_muestra(datos_df,0.25)
    
    # CORRECCIÓN 2: Reemplazamos la línea "datos_df" por la asignación real
    datos_df.loc[filas_elegidas, "fecha_registro"] = latino[filas_elegidas]
    
    return datos_df

if __name__ == "__main__":
    # CORRECCIÓN 3: Convertimos la lista devuelta a DataFrame y ejecutamos la función ensuciar
    lista_datos = generar_datos(FILAS)
    df_limpio = pd.DataFrame(lista_datos) 
    
    df_sucio = ensuciar(df_limpio)
    
    print("Shape del DataFrame:", df_sucio.shape)
    print("\nPrimeras filas:\n", df_sucio.head())
    print("\nNulos por columna:\n", df_sucio.isna().sum())