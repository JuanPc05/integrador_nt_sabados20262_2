import random
import uuid
import pandas as pd
from faker import Faker

# 1. Sembrar semillas para reproducibilidad
random.seed(42)
Faker.seed(42)

# 2. Constantes iniciales
FILAS = 200
LOCALE = Faker("es_CO")

NIVELES = {
    "Critica": 0,
    "Urgente": 1,
    "Alta": 2,
    "Media": 3,
    "Baja": 4
}
DIAS = [1, 2, 5, 8, 15]

# 3. Funciones auxiliares
def obtener_muestra(datos, porcentaje):
    # Se usa randint para variar la semilla en cada llamado,
    # logrando muestras diferentes cada vez que reutilizamos "filas_elegidas"
    return datos.sample(frac=porcentaje, random_state=random.randint(0, 999)).index

def escribir_mal_nombre(texto):
    variantes = [texto.upper(), f" {texto.lower()} ", texto.capitalize()]
    return random.choice(variantes)

def numero_en_palabra(num):
    mapa = {0: "cero", 1: "uno", 2: "dos", 3: "tres", 4: "cuatro"}
    return mapa.get(num, num)

# 4. Función generadora de datos limpios
def generar_datos_limpios(numero_filas=FILAS):
    random.seed(42)
    Faker.seed(42)
    LOCALE.seed_instance(42)

    duplicados = int(numero_filas * 0.08)
    base = numero_filas - duplicados

    datos_limpios = []
    
    # Aquí solo nos preocupamos por generar la data perfecta
    for _ in range(base):
        nombre = random.choice(list(NIVELES.keys()))
        nivel = NIVELES[nombre]

        datos_limpios.append({
            "id": LOCALE.uuid4(),
            "nombre": nombre,
            "nivel": nivel,
            "dias_max_respuesta": DIAS[nivel]
        })
        
    return datos_limpios

# 5. Función principal para ensuciar los datos simulados
def ensuciar(datos_df, n=FILAS):
    datos_df = datos_df.copy()

    # --- Ensuciar nombres (30% de las filas) ---
    filas_elegidas = obtener_muestra(datos_df, 0.30)
    datos_df.loc[filas_elegidas, "nombre"] = datos_df.loc[filas_elegidas, "nombre"].apply(escribir_mal_nombre)

    # --- Ensuciar niveles ---
    datos_df["nivel"] = datos_df["nivel"].astype("object")

    # 10% en palabras (antes de pasar a texto o None para que coincida la llave numérica)
    filas_palabra = obtener_muestra(datos_df, 0.10)
    datos_df.loc[filas_palabra, "nivel"] = datos_df.loc[filas_palabra, "nivel"].apply(numero_en_palabra)

    # 15% como texto numérico (de las filas que aún son números enteros)
    filas_restantes = datos_df.drop(filas_palabra)
    filas_str = obtener_muestra(filas_restantes, 0.15)
    datos_df.loc[filas_str, "nivel"] = datos_df.loc[filas_str, "nivel"].astype(str)

    # 7% en None (nulos reales, sin que .astype(str) los convierta en "None")
    filas_nulas = obtener_muestra(datos_df, 0.07)
    datos_df.loc[filas_nulas, "nivel"] = None

    # --- Ensuciar dias_max_respuesta ---
    filas_elegidas = obtener_muestra(datos_df, 0.05)
    datos_df.loc[filas_elegidas, "dias_max_respuesta"] = None

    filas_elegidas = obtener_muestra(datos_df, 0.03)
    datos_df.loc[filas_elegidas, "dias_max_respuesta"] = 999                                   

    # --- Agregar filas duplicadas (8% del total) ---
    cantidad_duplicas = n - len(datos_df)
    if cantidad_duplicas > 0:
        df_duplicados = datos_df.sample(n=cantidad_duplicas, random_state=42)
        datos_df = pd.concat([datos_df, df_duplicados], ignore_index=True)

    return datos_df


def generar_prioridades(numero_filas=FILAS):
    lista_datos = generar_datos_limpios(numero_filas)
    df_limpio = pd.DataFrame(lista_datos)
    return ensuciar(df_limpio, n=numero_filas)


# 6. Bloque principal (Orquestador)
if __name__ == "__main__":
    df_sucio = generar_prioridades(FILAS)
    
    print("Shape del DataFrame:", df_sucio.shape)
    print("\nPrimeras filas:\n", df_sucio.head())
    print("\nNulos por columna:\n", df_sucio.isna().sum())