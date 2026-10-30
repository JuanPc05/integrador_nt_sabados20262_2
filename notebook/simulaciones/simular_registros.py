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


def generar_datos_limpios(n=FILAS, ids_usuario=None, ids_reto=None):
    random.seed(42)
    Faker.seed(42)
    fake.seed_instance(42)

    lista_usuarios = list(ids_usuario) if ids_usuario is not None else IDS_USUARIO
    lista_retos = list(ids_reto) if ids_reto is not None else IDS_RETO

    duplicados = int(n * 0.05)
    base = n - duplicados

    registros = []
    for _ in range(base):
        registros.append({
            "id": fake.uuid4(),
            "fecha_registro": fake.date_time_between(start_date="-1y", end_date="now"),
            "observacion": fake.sentence(nb_words=10),
            "estado": random.choice(ESTADOS),
            "id_usuario": random.choice(lista_usuarios),
            "id_reto": random.choice(lista_retos),
        })
    return pd.DataFrame(registros)


def obtener_muestra(datos_df, porcentaje):
    return datos_df.sample(frac=porcentaje, random_state=random.randint(0, 999)).index


def ensuciar(datos_df, n=FILAS):
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

    # filas repetidas tal cual (5% del total)
    duplicados = n - len(datos_df)
    if duplicados > 0:
        copias = datos_df.sample(n=duplicados, random_state=42)
        datos_df = pd.concat([datos_df, copias], ignore_index=True)

    return datos_df


def generar_registros(n=FILAS, ids_usuario=None, ids_reto=None):
    df = ensuciar(generar_datos_limpios(n, ids_usuario=ids_usuario, ids_reto=ids_reto), n=n)
    return df


if __name__ == "__main__":
    df = generar_registros(FILAS)
    print(df.shape)
    print(df.head())
    print(df.isna().sum())