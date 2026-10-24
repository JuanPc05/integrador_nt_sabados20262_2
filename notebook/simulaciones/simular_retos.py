import random
import uuid
from faker import Faker
import pandas as pd

# 1. Sembrar semillas para reproducibilidad
random.seed(42)
Faker.seed(42)

LOCALE = Faker("es_CO")

# 2. Identificar datos a simular y colecciones base
ESTADOS = ("abierto", "en_curso", "cerrado")
IDS_EMPRESA = tuple(str(uuid.uuid4()) for _ in range(10))
IDS_CATEGORIA = tuple(str(uuid.uuid4()) for _ in range(10))
IDS_PRIORIDAD = tuple(str(uuid.uuid4()) for _ in range(3))

# 3. Constante de simulación
FILAS = 500


# 4. Funciones auxiliares para ensuciar datos
def obtener_muestra(datos, porcentaje):
    """Devuelve los índices de una fracción aleatoria de filas."""
    return datos.sample(frac=porcentaje, random_state=random.randint(1, 9999)).index


def escribir_mal(texto):
    """Aplica variaciones de formato y espacios al texto."""
    variantes = [texto.lower(), texto.upper(), f" {texto} "]
    return random.choice(variantes)


# 5. Generación de datos base
def generar_datos(numero_filas=FILAS):
    random.seed(42)
    LOCALE.seed_instance(42)
    filas = []

    for _ in range(numero_filas):
        # Generar fechas iniciales
        fecha_inicio = LOCALE.date_between(start_date="-1y", end_date="+3m")
        duracion = random.randint(15, 180)
        fecha_fin = fecha_inicio + pd.Timedelta(days=duracion)

        filas.append(
            {
                "id": str(uuid.uuid4()),
                "nombre": LOCALE.sentence(nb_words=6).rstrip("."),
                "descripcion": LOCALE.sentence(nb_words=12),
                "fecha_inicio": fecha_inicio.strftime("%Y-%m-%d"),
                "fecha_fin": fecha_fin.strftime("%Y-%m-%d"),
                "estado": random.choice(ESTADOS),
                "id_empresa": random.choice(IDS_EMPRESA),
                "id_categoria": random.choice(IDS_CATEGORIA),
                "id_prioridad": random.choice(IDS_PRIORIDAD),
            }
        )

    return pd.DataFrame(filas)


# 6. Función principal para ensuciar datos (Lógica del profesor)
def ensuciar(datos_df):
    datos_df = datos_df.copy()

    # 1. nombre: 10% con espacios sobrantes
    filas_elegidas = obtener_muestra(datos_df, 0.10)
    datos_df.loc[filas_elegidas, "nombre"] = (
        "  " + datos_df.loc[filas_elegidas, "nombre"] + "  "
    )

    # 2. descripcion: 12% en None (nulos)
    filas_elegidas = obtener_muestra(datos_df, 0.12)
    datos_df.loc[filas_elegidas, "descripcion"] = None

    # 3. estado: aplicar variantes con escribir_mal usando .map()
    filas_elegidas = obtener_muestra(datos_df, 0.30)
    datos_df.loc[filas_elegidas, "estado"] = datos_df.loc[
        filas_elegidas, "estado"
    ].map(escribir_mal)

    # 4. fecha_inicio: mezclar formato ISO ('YYYY-MM-DD') y Latino ('DD/MM/YYYY')
    fechas_dt = pd.to_datetime(datos_df["fecha_inicio"])
    iso = fechas_dt.dt.strftime("%Y-%m-%d")
    latino = fechas_dt.dt.strftime("%d/%m/%Y")
    datos_df["fecha_inicio"] = iso
    filas_elegidas = obtener_muestra(datos_df, 0.50)
    datos_df.loc[filas_elegidas, "fecha_inicio"] = latino.loc[filas_elegidas]

    # 5. fecha_fin: 8% en None
    filas_elegidas = obtener_muestra(datos_df, 0.08)
    datos_df.loc[filas_elegidas, "fecha_fin"] = None

    # 6. fecha_fin: 5% ANTERIOR a fecha_inicio (error lógico)
    filas_disponibles = datos_df[datos_df["fecha_fin"].notna()]
    filas_elegidas = obtener_muestra(filas_disponibles, 0.05)
    f_inicio_dt = pd.to_datetime(
        datos_df.loc[filas_elegidas, "fecha_inicio"], format="mixed"
    )
    datos_df.loc[filas_elegidas, "fecha_fin"] = (
        f_inicio_dt - pd.to_timedelta(15, unit="D")
    ).dt.strftime("%Y-%m-%d")

    # 7. duplicados: 5% de filas repetidas tal cual
    filas_duplicadas = datos_df.sample(frac=0.05, random_state=42)
    datos_df = pd.concat([datos_df, filas_duplicadas], ignore_index=True)

    return datos_df


# 7. Función integradora solicitada por la Historia de Usuario
def generar_retos(n=FILAS) -> pd.DataFrame:
    df_base = generar_datos(numero_filas=n)
    return ensuciar(df_base)


# 8. Punto de entrada para pruebas
if __name__ == "__main__":
    df = generar_retos()

    print("=== DIMENSIONES (df.shape) ===")
    print(df.shape)

    print("\n=== PRIMERAS FILAS (df.head()) ===")
    print(df.head())

    print("\n=== CONTEO DE NULOS (df.isna().sum()) ===")
    print(df.isna().sum())