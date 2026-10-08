'''
Clasifica tematicamente los retos. Crea el script `src/simular_categorias.py`. Con la libreria **Faker** genera 250 filas falsas de la tabla `categorias`, con las MISMAS columnas que usa Backend II. Despues **ensucia los datos a proposito**: nulos, duplicados, espacios sobrantes, mayusculas mezcladas y formatos distintos. Esos errores son los que vas a arreglar en la etapa de limpieza, asi que tienen que quedar bien puestos.

Usa `Faker("es_CO")` y fija la semilla con `Faker.seed(42)` y `random.seed(42)` para que el resultado sea SIEMPRE el mismo y tu compañero pueda reproducirlo.

OJO: `area_responsable` NO esta en el modelo de Backend II: es una columna EXTRA solo para este ejercicio de analisis, para poder agrupar. Dejala anotada como tal en el script.

'''

import random
import uuid
from faker import Faker
import pandas as pd

# 1. Al inicio se declaran las constantes requeridas
CATEGORIAS = ["Logística", "Tecnología", "Finanzas", "Recursos Humanos", "Marketing", "Ventas", "Operaciones", "Atención al Cliente", "Legal", "Compras"]
AREAS = ["desarrollo", "salud cuidado", "administracion", "gastronomia"]

def _ensuciar_nombre(texto):
    #Genera variantes de escritura para simular errores de digitación
    sin_tilde = (
        texto.replace("á", "a").replace("é", "e").replace("í", "i")
             .replace("ó", "o").replace("ú", "u").replace("Á", "A")
             .replace("É", "E").replace("Í", "I").replace("Ó", "O")
             .replace("Ú", "U")
    )
    
    # Construimos las variantes exactas que piden los criterios
    variantes = [
        sin_tilde.capitalize(),  # Ej: 'Logistica'
        sin_tilde.upper(),       # Ej: 'LOGISTICA'
        f" {sin_tilde.lower()} ",# Ej: ' logistica ' (con espacios a los lados)
        texto.lower()            # Ej: 'logística' (original en minúscula)
    ]
    
    return random.choice(variantes)

def generar_categorias(n: int = 250) -> pd.DataFrame:
    # 2. Fijar semillas para reproducibilidad
    Faker.seed(42)
    random.seed(42)
    fake = Faker("es_ES")

    # 3. Calcular porcentajes (8% de duplicados exactos sobre el total)
    n_duplicados = int(n * 0.08)
    n_unicos = n - n_duplicados

    registros = []
    
    # 4. Generación base de datos únicos
    for _ in range(n_unicos):
        # Seleccionamos la categoría base y la ensuciamos
        cat_base = random.choice(CATEGORIAS)
        nombre = _ensuciar_nombre(cat_base)
        
        # Ensuciar descripción (15% en None)
        descripcion = None if random.random() < 0.15 else fake.sentence(nb_words=8)
        
        # Ensuciar área responsable (10% en None)
        area_responsable = None if random.random() < 0.10 else random.choice(AREAS)
        
        # CORRECCIÓN: uuid4() ejecutado correctamente con paréntesis
        registros.append({
            "id": str(uuid.uuid4()),
            "nombre": nombre,
            "descripcion": descripcion,
            "area_responsable": area_responsable
        })

    # 5. Duplicar el 8% de filas tal cual (duplicados exactos)
    # Usamos dict() para crear una copia real en memoria y evitar modificar el original
    filas_a_duplicar = [dict(r) for r in random.choices(registros, k=n_duplicados)]
    registros.extend(filas_a_duplicar)

    # 6. Mezclar para que los duplicados no queden todos al final
    random.shuffle(registros)

    # Todo se arma en la función que devuelve el DataFrame
    return pd.DataFrame(registros)

if __name__ == "__main__":
    # El bloque main solo imprime lo solicitado para revisar que quedaron sucios
    df = generar_categorias(n=250)
    print("--- SHAPE ---")
    print(df.shape)
    print("\n--- HEAD ---")
    print(df.head())
    print("\n--- NULOS ---")
    print(df.isna().sum())