import random
import uuid
import pandas as pd
from faker import Faker

random.seed(42)
Faker.seed(42)

fake = Faker("es_CO")

FILAS = 800
ESTADOS = ["Pendiente", "En Progreso", "Completado"]
IDS_USUARIO = [fake.uuid4() for _ in range(400)]
IDS_RETO = [fake.uuid4() for _ in range(100)]

ESTADOS_SUCIOS = ["inscrito", "EN PROCESO", " Finalizado "]


def generar_datos_limpios(n=800):
    registros = []
    for _ in range(n):
        registros.append({
            "id": str(uuid.uuid4()),
            "fecha_registro": fake.date_time_between(start_date="-1y", end_date="now"),
            "observacion": fake.sentence(nb_words=10),
            "estado": random.choice(ESTADOS),
            "id_usuario": random.choice(IDS_USUARIO),
            "id_reto": random.choice(IDS_RETO),
        })
    return pd.DataFrame(registros)


def obtener_muestra(datos_df, porcentaje):
    return datos_df.sample(frac=porcentaje, random_state=random.randint(0, 999)).index


def ensuciar(datos_df):
    datos_df = datos_df.copy()

    # fecha en dos formatos
    formato_iso = datos_df["fecha_registro"].dt.strftime("%Y-%m-%d %H:%M:%S")
    formato_latino = datos_df["fecha_registro"].dt.strftime("%d/%m/%Y %H:%M")
    datos_df["fecha_registro"] = formato_iso
    filas_elegidas = obtener_muestra(datos_df, 0.5)
    datos_df.loc[filas_elegidas, "fecha_registro"] = formato_latino.loc[filas_elegidas]

    # observacion nula
    filas_elegidas = obtener_muestra(datos_df, 0.20)
    datos_df.loc[filas_elegidas, "observacion"] = None

    # estado escrito distinto
    filas_elegidas = obtener_muestra(datos_df, 0.30)
    datos_df.loc[filas_elegidas, "estado"] = [random.choice(ESTADOS_SUCIOS) for _ in filas_elegidas]

    # mismo usuario inscrito dos veces en el mismo reto
    filas_elegidas = obtener_muestra(datos_df, 0.10)
    otras_filas = datos_df.drop(filas_elegidas).sample(n=len(filas_elegidas), random_state=random.randint(0, 999))
    datos_df.loc[filas_elegidas, ["id_usuario", "id_reto"]] = otras_filas[["id_usuario", "id_reto"]].values

    # filas repetidas tal cual
    filas_elegidas = obtener_muestra(datos_df, 0.05)
    otras_filas = datos_df.drop(filas_elegidas).sample(n=len(filas_elegidas), random_state=random.randint(0, 999))
    datos_df.loc[filas_elegidas] = otras_filas.values

    return datos_df


def generar_registros(n=800):
    df = ensuciar(generar_datos_limpios(n))
    return df


if __name__ == "__main__":
    df = generar_registros(FILAS)
    print(df.shape)
    print(df.head())
    print(df.isna().sum())