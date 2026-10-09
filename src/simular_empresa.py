import random
import uuid

import pandas as pd
from faker import Faker


# 1. Sembrar semillas para que los datos sean siempre los mismos
random.seed(42)
Faker.seed(42)

# 2. Constantes del proyecto
FILAS = 300

SECTORES = [
    "Tecnologia",
    "Salud",
    "Educacion",
    "Logistica",
    "Manufactura",
    "Comercio",
    "Finanzas",
    "Construccion",
    "Agroindustria",
    "Turismo",
]

LOCALE = Faker("es_CO")


# 3. Función generadora
def generar_empresas(n=300):
    empresas = []

    # 3.1 Generar 5% menos filas (para luego agregar los duplicados)
    duplicados = int(n * 0.05)
    base = n - duplicados

    for _ in range(base):
        empresas.append({
            "id": str(uuid.uuid4()),
            "nombre": LOCALE.company(),
            "nit": LOCALE.numerify("#########-#"),
            "sector": random.choice(SECTORES),
            "contacto": LOCALE.name(),
            "correo": LOCALE.company_email(),
            "telefono": LOCALE.numerify("3#########"),
            "activa": random.choice([True, False]),
        })

    df = pd.DataFrame(empresas)

    # 3.2 Ensuciar nombre: 10% espacios, 15% MAYÚSCULAS
    for i in df.index:
        r = random.random()
        if r < 0.10:
            df.at[i, "nombre"] = f"  {df.at[i, 'nombre']}  "
        elif r < 0.25:
            df.at[i, "nombre"] = df.at[i, "nombre"].upper()

    # 3.3 Ensuciar nit: mitad con puntos y guiones, mitad sin nada
    for i in df.index:
        limpio = df.at[i, "nit"].replace("-", "")
        if random.random() < 0.5:
            df.at[i, "nit"] = (
                f"{limpio[:3]}.{limpio[3:6]}.{limpio[6:9]}-{limpio[9]}"
            )
        else:
            df.at[i, "nit"] = limpio

    # 3.4 Ensuciar sector: variantes del mismo sector
    for i in df.index:
        variante = random.choice(["original", "mayus", "espacios"])
        if variante == "mayus":
            df.at[i, "sector"] = df.at[i, "sector"].upper()
        elif variante == "espacios":
            df.at[i, "sector"] = f" {df.at[i, 'sector'].lower()} "

    # 3.5 Ensuciar contacto: 8% nulos
    for i in df.index:
        if random.random() < 0.08:
            df.at[i, "contacto"] = None

    # 3.6 Ensuciar correo: 6% sin arroba
    for i in df.index:
        if random.random() < 0.06:
            df.at[i, "correo"] = df.at[i, "correo"].replace("@", "")

        # 3.7 Ensuciar telefono: tres formatos mezclados
    for i in df.index:
        tel = df.at[i, "telefono"]
        formato = random.choice(["plano", "espacios", "internacional"])
        if formato == "espacios":
            df.at[i, "telefono"] = f"{tel[:3]} {tel[3:6]} {tel[6:]}"
        elif formato == "internacional":
            df.at[i, "telefono"] = f"+57 {tel[:3]}-{tel[3:6]}-{tel[6:]}"

    # 3.8 Antes de ensuciar activa, cambiar el dtype a object
    df["activa"] = df["activa"].astype(object)

    # 3.9 5% de duplicados exactos
    copias = df.sample(n=duplicados, random_state=42)
    df = pd.concat([df, copias], ignore_index=True)

    # 3.10 3% de nit repetidos entre empresas distintas
    repetidos = int(n * 0.03)
    indices = random.sample(range(base), repetidos * 2)
    for j in range(0, len(indices), 2):
        df.at[indices[j], "nit"] = df.at[indices[j + 1], "nit"]

    return df

    return df


# 4. Bloque principal
if __name__ == "__main__":
    df = generar_empresas(FILAS)
    print(df.shape)
    print(df.head())
    print(df.isna().sum())


# 5 Convirtiendo los datos generado en un dataFrame con PANDAS. 
tabla_ordenada_empresas = generar_empresas(FILAS)



#6 Probar la función
print (tabla_ordenada_empresas)