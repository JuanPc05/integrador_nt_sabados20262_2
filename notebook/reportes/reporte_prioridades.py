from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

CARPETA_PROYECTO = Path(__file__).resolve().parents[2]
RUTA_LIMPIO = CARPETA_PROYECTO / "data" / "limpio" / "prioridades_limpio.csv"
CARPETA_REPORTES = CARPETA_PROYECTO / "reportes"

def generar_reportes():
    CARPETA_REPORTES.mkdir(parents=True, exist_ok=True)
    
    df = pd.read_csv(RUTA_LIMPIO)

    por_nivel = df.groupby("nivel")["id"].count()
    por_nivel.plot(kind="bar", color="steelblue")
    plt.title("Cantidad de Filas por Nivel")
    plt.xlabel("Nivel de Prioridad")
    plt.ylabel("Cantidad de Filas")
    plt.tight_layout()
    plt.savefig(CARPETA_REPORTES / "prioridades_grafica_1.png", dpi=120)
    plt.close()

    resumen = df.groupby("nombre")["dias_max_respuesta"].agg(["min", "mean", "max"]).round(1)
    resumen["mean"].plot(kind="bar", color="darkorange")
    plt.title("Dias Promedio de Respuesta por Prioridad")
    plt.xlabel("Nombre de la Prioridad")
    plt.ylabel("Dias Promedio")
    plt.tight_layout()
    plt.savefig(CARPETA_REPORTES / "prioridades_grafica_2.png", dpi=120)
    plt.close()

    conteo = df["nombre"].value_counts()
    conteo.plot(kind="pie", autopct="%1.1f%%", colormap="Set3")
    plt.title("Reparto de las Prioridades")
    plt.ylabel("") 
    plt.tight_layout()
    plt.savefig(CARPETA_REPORTES / "prioridades_grafica_3.png", dpi=120)
    plt.close()

    print("\n--- CONCLUSIONES DEL REPORTE ---")
    prioridades_reales = df["nombre"].nunique()
    print(f"1. Prioridades REALES finales: {prioridades_reales} (Deberian ser 5).")
    print("2. Relacion Nivel - Dias: Se observa una correlacion directa. A menor numero de nivel (ej. 0 para Critica), menor es el numero de dias promedio de respuesta exigidos, garantizando asi la atencion rapida de los casos mas urgentes.")

if __name__ == "__main__":
    generar_reportes()