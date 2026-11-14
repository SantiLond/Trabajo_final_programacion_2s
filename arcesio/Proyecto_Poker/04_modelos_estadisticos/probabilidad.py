import math
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

# Composición de la baraja
palos = 4
valores = 13
total_cartas = palos * valores

# Cantidad de cartas iniciales por jugador
cartas_iniciales = 2
# Calcular las combinaciones posibles
total_combinaciones = math.comb(total_cartas, cartas_iniciales)
print("Total de cartas:", total_cartas)
print("Combinaciones posibles:", total_combinaciones)



# Probabilidad de recibir una pareja inicial
parejas_por_valor = math.comb(palos, 2)
total_parejas = valores * parejas_por_valor
probabilidad_pareja = total_parejas / total_combinaciones
print("\nCombinaciones de parejas:", total_parejas)
print(f"Probabilidad de pareja: {probabilidad_pareja * 100:.2f}%")


# Probabilidad de recibir cartas del mismo palo
combinaciones_por_palo = math.comb(valores, 2)
total_mismo_palo = palos * combinaciones_por_palo
probabilidad_mismo_palo = total_mismo_palo / total_combinaciones
print("\nCombinaciones del mismo palo:", total_mismo_palo)
print(f"Probabilidad de mismo palo: {probabilidad_mismo_palo * 100:.2f}%")



# Probabilidad de recibir cartas de distinto palo sin pareja
total_distinto_palo = total_combinaciones - total_parejas - total_mismo_palo
probabilidad_distinto_palo = total_distinto_palo / total_combinaciones
print("\nCombinaciones de distinto palo:", total_distinto_palo)
print(f"Probabilidad de distinto palo: {probabilidad_distinto_palo * 100:.2f}%")


# Verificación de las probabilidades
total_probabilidad = (
    probabilidad_pareja +
    probabilidad_mismo_palo +
    probabilidad_distinto_palo
)
print(f"\nProbabilidad total: {total_probabilidad * 100:.2f}%")



# Cargar los datos procesados durante el EDA
ruta_actual = os.path.dirname(os.path.abspath(__file__))
ruta_proyecto = os.path.dirname(ruta_actual)
ruta_procesados = os.path.join(
    ruta_proyecto, "02_datos", "procesados"
)
ruta_evidencias = os.path.join(
    ruta_proyecto, "05_evidencias"
)
# Guardar los resultados del análisis matemático
ruta_archivo = os.path.join(
    ruta_evidencias, "resultado_probabilidad.txt"
)
archivo_salida = open(
    ruta_archivo, "w", encoding="utf-8", buffering=1
)
sys.stdout = archivo_salida
print("Inicio del análisis de probabilidades")

df = pd.read_csv(
    os.path.join(ruta_procesados, "manos_procesadas.csv")
)
print(df.head())


# Frecuencias observadas en los datos reales
frecuencias_observadas = df["categoria_cartas"].value_counts(
    normalize=True
) * 100
print("\nFrecuencias observadas:")
print(frecuencias_observadas)


# Comparación de resultados
comparacion = pd.DataFrame({
    "Categoria": ["Pareja", "Mismo palo", "Distinto palo"],
    "Teorica": [
        probabilidad_pareja * 100,
        probabilidad_mismo_palo * 100,
        probabilidad_distinto_palo * 100
    ],
    "Observada": [
        frecuencias_observadas["Pareja"],
        frecuencias_observadas["Mismo palo"],
        frecuencias_observadas["Distinto palo"]
    ]
})
print("\nComparación de probabilidades:")
print(comparacion)



# Gráfica comparativa
comparacion.plot(
    x="Categoria",
    y=["Teorica", "Observada"],
    kind="bar"
)
plt.title("Probabilidad teórica frente a frecuencia observada")
plt.xlabel("Categoría de cartas")
plt.ylabel("Porcentaje")
plt.xticks(rotation=0)
plt.ylim(0, 100)
plt.grid(axis="y", alpha=0.3)
plt.savefig(
    os.path.join(ruta_evidencias, "12_probabilidad_vs_realidad.png"),
    dpi=300,
    bbox_inches="tight"
)
plt.show()


comparacion.to_csv(
    os.path.join(ruta_evidencias, "comparacion_probabilidades.csv"),
    index=False
)


print("\nFin del análisis de probabilidades")
archivo_salida.flush()
sys.stdout = sys.__stdout__
archivo_salida.close()
print("Archivo de evidencias generado correctamente")