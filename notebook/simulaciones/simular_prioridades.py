import random
import uuid
import pandas as pd
from faker import Faker

random.seed(42)
Faker.seed(42)

FILAS=200
LOCALE=Faker("es_CO")

NIVELES = {
    "Critica": 0,
    "Urgente": 1,
    "Alta": 2,
    "Media": 3,
    "Baja": 4
}
DIAS = [1, 2, 5, 8, 15]

def obtener_muestra(datos, porcentaje):
    return datos.sample(frac=porcentaje, random_state=42).index

def escribir_mal_nombre(texto):
    variantes = [texto.upper(), f" {texto.lower()} ", texto.capitalize()]
    return random.choice(variantes)

def numero_en_palabra(num):
    mapa = {0: "cero", 1: "uno", 2: "dos", 3: "tres", 4: "cuatro"}
    return mapa.get(num, num)

#Funcion principal orquestadora

def generar_prioridades(numero_filas):
    cantidad_duplicas = int(numero_filas  * 0.08)
    cantidad_unicas = numero_filas - cantidad_duplicas

    datos_limpios=[]
    for _ in range(cantidad_unicas):
        nombre = random.choice(list(NIVELES.keys()))
        nivel = NIVELES[nombre]

        datos_limpios.append({
            "id": str(uuid.uuid4()),
            "nombre": nombre,
            "nivel": nivel,
            "dias_max_respuesta": DIAS[nivel]
        })

    df = pd.DataFrame(datos_limpios)

    df["nombre"] = df["nombre"].apply(escribir_mal_nombre)

    df["nivel"] = df["nivel"].astype("object")

    idx_nivel_none = obtener_muestra(df, 0.07)
    df.loc[idx_nivel_none, "nivel"] = None

    idx_nivel_texto = obtener_muestra(df.drop(idx_nivel_none), 0.15)
    df.loc[idx_nivel_texto, "nivel"] = df.loc[idx_nivel_texto, "nivel"].astype(str)

    idx_nivel_palabra = obtener_muestra(df.drop(idx_nivel_none).drop(idx_nivel_texto), 0.10)
    df.loc[idx_nivel_palabra, "nivel"] = df.loc[idx_nivel_palabra, "nivel"].apply(numero_en_palabra)

    idx_dias_none = obtener_muestra(df, 0.05)
    df.loc[idx_dias_none, "dias_max_respuesta"] = None

    idx_dias_absurdo = obtener_muestra(df.drop(idx_dias_none), 0.03)
    df.loc[idx_dias_absurdo, "dias_max_respuesta"] = 999                                  

    df_duplicados = df.sample(n=cantidad_duplicas, random_state=42)
    df_final = pd.concat([df, df_duplicados], ignore_index=True)

    return df_final

if __name__ == "__main__":
    df = generar_prioridades(FILAS)
    print("Shape del DataFrame:", df.shape)
    print("\nPrimeras filas:\n", df.head())
    print("\nNulos por columna:\n", df.isna().sum())