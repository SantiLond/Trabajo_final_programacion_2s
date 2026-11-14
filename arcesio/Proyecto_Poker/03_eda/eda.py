import json
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

archivos = [
    "file_poker.json",
    "file_poker_hands.json",
    "file_poker_page_2.json"
]

ruta_actual = os.path.dirname(os.path.abspath(__file__))
ruta_proyecto = os.path.dirname(ruta_actual)
ruta_originales = os.path.join(
    ruta_proyecto, "02_datos", "originales"
)
ruta_evidencias = os.path.join(
    ruta_proyecto, "05_evidencias"
)
ruta_procesados = os.path.join(
    ruta_proyecto, "02_datos", "procesados"
)
# Guardar la salida de la consola en un archivo de texto
ruta_archivo = os.path.join(ruta_evidencias, "resultado_eda.txt")
archivo_salida = open(ruta_archivo, "w", encoding="utf-8", buffering=1)
sys.stdout = archivo_salida
print("Inicio del análisis exploratorio de datos")

manos = []
for archivo in archivos:
    with open(os.path.join(ruta_originales, archivo),
              encoding="utf-8") as f:
        datos = json.load(f)
    print(archivo, len(datos))
    manos.extend(datos)
df = pd.DataFrame(manos)
print(df.head())
print(df.shape)

# Identificación de las dimensiones del DataFrame
print("Cantidad de registros:", df.shape[0])
print("Cantidad de columnas:", df.shape[1])
# Identificación de las columnas
print("\nColumnas del DataFrame:")
print(df.columns)
# Información general de los datos
print("\nInformación del DataFrame:")
df.info()


# Identificación de registros duplicados
duplicados = df.duplicated(subset=["hands_id"])
print("\nCantidad de registros duplicados:")
print(duplicados)
print(duplicados.sum())


# Visualizar los registros con identificadores repetidos
registros_repetidos = df[df.duplicated(subset=["hands_id"], keep=False)]
print("\nRegistros repetidos:")
print(registros_repetidos[["hands_id", "hero_cards"]])


# Verificar el contenido de los registros duplicados
manos_revisadas = {}
diferencias = 0
for mano in manos:
    identificador = mano["hands_id"]
    if identificador in manos_revisadas:
        if mano != manos_revisadas[identificador]:
            diferencias += 1
            print("Diferencia encontrada:", identificador)
    else:
        manos_revisadas[identificador] = mano
print("Duplicados con diferencias:", diferencias)



# Eliminación de registros duplicados
print("Registros antes de la limpieza:", len(df))
df = df.drop_duplicates(subset=["hands_id"], keep="first")
print("Registros después de la limpieza:", len(df))


# Reorganización de los índices
df = df.reset_index(drop=True)
print(df.head())


# Identificación de valores nulos
valores_nulos = df.isnull()
print("\nCantidad de valores nulos por columna:")
print(valores_nulos.sum())

# Porcentaje de valores nulos por columna
porcentaje_nulos = valores_nulos.sum() / len(df) * 100
print("\nPorcentaje de valores nulos:")
print(porcentaje_nulos)

# Estadística descriptiva de las variables numéricas
print("\nEstadística descriptiva:")
print(df.describe())


# Frecuencia del número de asientos
frecuencia_asientos = df["seats"].value_counts()
print("\nFrecuencia de asientos:")
print(frecuencia_asientos)

# Frecuencia relativa porcentual
frecuencia_relativa = df["seats"].value_counts(normalize=True) * 100
print("\nFrecuencia relativa de asientos:")
print(frecuencia_relativa)


# Gráfica de frecuencia de asientos
plt.bar(frecuencia_asientos.index, frecuencia_asientos.values)
plt.title("Distribución del número de asientos")
plt.xlabel("Número de asientos")
plt.ylabel("Frecuencia")
# Guardar la gráfica como evidencia
plt.savefig(os.path.join(ruta_evidencias, "01_frecuencia_asientos.png"),dpi=300, bbox_inches="tight")
plt.show()



# Frecuencia de las modalidades de juego
frecuencia_modalidad = df["tournament"].value_counts()
frecuencia_modalidad = frecuencia_modalidad.rename({
    True: "Torneo",
    False: "Cash Game"
})
print("\nFrecuencia de modalidades de juego:")
print(frecuencia_modalidad)


# Gráfica de modalidades de juego
plt.figure()
plt.pie(
    frecuencia_modalidad.values,
    labels=frecuencia_modalidad.index,
    autopct="%1.2f%%"
)
plt.title("Distribución de las modalidades de juego")
plt.savefig(
    os.path.join(ruta_evidencias, "02_modalidades_juego.png"),
    dpi=300,
    bbox_inches="tight"
)
plt.show()

print(df["players"].iloc[0])
df["cantidad_jugadores"] = df["players"].apply(len)
print(df[["hands_id", "seats", "cantidad_jugadores"]])
print("\nEstadística descriptiva de jugadores:")
print(df["cantidad_jugadores"].describe())

plt.figure()
plt.hist(df["cantidad_jugadores"],
         bins=range(2, 11),
         edgecolor="black",
         align="left")
plt.title("Distribución del número de jugadores")
plt.xlabel("Cantidad de jugadores")
plt.ylabel("Frecuencia")
plt.xticks(range(2, 10))
plt.savefig(
    os.path.join(ruta_evidencias, "03_cantidad_jugadores.png"),
    dpi=300,
    bbox_inches="tight"
)
plt.show()



#Estructura delas cartas de los jugadores
print(df["hero_cards"].iloc[0])
# Clasificación de las cartas iniciales
categorias = []
for cartas in df["hero_cards"]:
    carta1 = cartas[0]
    carta2 = cartas[1]
    if carta1["rank"] == carta2["rank"]:
        categorias.append("Pareja")
    elif carta1["suit"] == carta2["suit"]:
        categorias.append("Mismo palo")
    else:
        categorias.append("Distinto palo")
df["categoria_cartas"] = categorias
print(df[["hero_cards", "categoria_cartas"]])

frecuencia_cartas = df["categoria_cartas"].value_counts()
print("\nFrecuencia de cartas iniciales:")
print(frecuencia_cartas)

#Grafica
plt.figure()
plt.bar(frecuencia_cartas.index, frecuencia_cartas.values)
plt.title("Distribución de las cartas iniciales")
plt.xlabel("Categoría de cartas")
plt.ylabel("Frecuencia")
plt.savefig(
    os.path.join(ruta_evidencias, "04_cartas_iniciales.png"),
    dpi=300,
    bbox_inches="tight"
)
plt.show()


#Identificación de las manos ganadas
print(df["players"].iloc[0])
print(df["results"].iloc[0])

# Identificar el asiento del jugador de referencia
asientos_hero = []
for jugadores in df["players"]:
    for jugador in jugadores:

        if jugador.get("hero") == True:
            asientos_hero.append(jugador["seat"])
            break
df["asiento_hero"] = asientos_hero
print(df[["hands_id", "asiento_hero"]])



# Identificación de las manos ganadas
victorias = []
for i in range(len(df)):
    asiento = str(df["asiento_hero"].iloc[i])
    resultados = df["results"].iloc[i]
    resultado_jugador = resultados["seats"].get(asiento, {})
    if resultado_jugador.get("collected"):
        victorias.append(1)
    else:
        victorias.append(0)
df["victoria"] = victorias
print("\nResultado de las manos:")
print(df[["hands_id", "asiento_hero", "victoria"]])


#Calcular las frecuencias
frecuencia_victorias = df["victoria"].value_counts()
print("\nFrecuencia de victorias:")
print(frecuencia_victorias)
porcentaje_victorias = df["victoria"].mean() * 100
print(f"Porcentaje de victorias: {porcentaje_victorias:.2f}%")

frecuencia_victorias = frecuencia_victorias.rename({
    1: "Ganadas",
    0: "No ganadas"
})

#Generar y guardar la gráfica
plt.figure()
plt.pie(
    frecuencia_victorias.values,
    labels=frecuencia_victorias.index,
    autopct="%1.2f%%"
)
plt.title("Distribución de manos ganadas")
plt.savefig(
    os.path.join(ruta_evidencias, "05_manos_ganadas.png"),
    dpi=300,
    bbox_inches="tight"
)
plt.show()


# Identificación de las combinaciones iniciales
orden_cartas = "23456789TJQKA"
combinaciones = []
for cartas in df["hero_cards"]:
    carta1 = cartas[0]
    carta2 = cartas[1]
    valor1 = carta1["rank"]
    valor2 = carta2["rank"]
    # Colocar primero la carta de mayor valor
    if orden_cartas.index(valor1) < orden_cartas.index(valor2):
        valor1, valor2 = valor2, valor1
    if valor1 == valor2:
        combinacion = valor1 + valor2
    elif carta1["suit"] == carta2["suit"]:
        combinacion = valor1 + valor2 + "s"
    else:
        combinacion = valor1 + valor2 + "o"
    combinaciones.append(combinacion)
df["combinacion_inicial"] = combinaciones
print(df[["hero_cards", "combinacion_inicial"]])


#Calcular las frecuencias
frecuencia_combinaciones = df["combinacion_inicial"].value_counts()
print("\nFrecuencia de combinaciones iniciales:")
print(frecuencia_combinaciones)
print("Combinaciones diferentes:",
      len(frecuencia_combinaciones))


#Generar y guardar la gráfica
plt.figure(figsize=(10, 12))
plt.barh(
    frecuencia_combinaciones.index,
    frecuencia_combinaciones.values
)
plt.title("Frecuencia de las combinaciones iniciales")
plt.xlabel("Frecuencia")
plt.ylabel("Combinación inicial")
plt.gca().invert_yaxis()
plt.savefig(
    os.path.join(ruta_evidencias, "06_combinaciones_iniciales.png"),
    dpi=300,
    bbox_inches="tight"
)
plt.show()


#Construir una tabla de contingencia
# Relación entre cartas iniciales y victorias
tabla_victorias = pd.crosstab(
    df["categoria_cartas"],
    df["victoria"]
)
print("\nTabla de contingencia:")
print(tabla_victorias)

# Porcentaje de victorias por categoría
tabla_porcentajes = pd.crosstab(
    df["categoria_cartas"],
    df["victoria"],
    normalize="index"
) * 100
print("\nPorcentaje de victorias por categoría:")
print(tabla_porcentajes)


# Gráfica de porcentajes de victorias
tabla_porcentajes.plot(kind="bar")
plt.title("Resultado según las cartas iniciales")
plt.xlabel("Categoría de cartas")
plt.ylabel("Porcentaje")
plt.legend(["No ganadas", "Ganadas"])
plt.xticks(rotation=0)
plt.ylim(0, 100)
plt.savefig(
    os.path.join(ruta_evidencias, "07_cartas_vs_victorias.png"),
    dpi=300,
    bbox_inches="tight"
)
plt.show()



#¿Existe una relación entre la cantidad de jugadores de una mesa y el porcentaje de manos ganadas?
# Relación entre cantidad de jugadores y victorias
resumen_jugadores = df.groupby("cantidad_jugadores")["victoria"].agg(
    ["count", "sum", "mean"]
)
print("\nVictorias según la cantidad de jugadores:")
print(resumen_jugadores)



#Calcular el porcentaje de victorias
resumen_jugadores.columns = [
    "total_manos", "manos_ganadas", "proporcion"
]
resumen_jugadores["porcentaje_victorias"] = (
    resumen_jugadores["proporcion"] * 100
)
print(resumen_jugadores)

#Generar y guardar la gráfica
plt.figure()
plt.bar(
    resumen_jugadores.index,
    resumen_jugadores["porcentaje_victorias"]
)
plt.title("Porcentaje de victorias según el número de jugadores")
plt.xlabel("Cantidad de jugadores")
plt.ylabel("Porcentaje de victorias")
plt.ylim(0, 100)
plt.xticks(resumen_jugadores.index)
plt.grid(axis="y", alpha=0.3)
plt.savefig(
    os.path.join(ruta_evidencias, "08_jugadores_vs_victorias.png"),
    dpi=300,
    bbox_inches="tight"
)
plt.show()



# Relación entre combinaciones iniciales y victorias
resumen_combinaciones = df.groupby("combinacion_inicial")["victoria"].agg(
    ["count", "sum", "mean"]
)
resumen_combinaciones.columns = [
    "total_manos", "manos_ganadas", "proporcion"
]
resumen_combinaciones["porcentaje_victorias"] = (
    resumen_combinaciones["proporcion"] * 100
)
print("\nVictorias por combinación inicial:")
print(resumen_combinaciones)


#Generar y guardar la gráfica
plt.figure(figsize=(10, 12))
plt.barh(
    resumen_combinaciones.index,
    resumen_combinaciones["manos_ganadas"]
)
plt.title("Victorias por combinación inicial")
plt.xlabel("Cantidad de victorias")
plt.ylabel("Combinación inicial")
plt.savefig(
    os.path.join(ruta_evidencias, "09_combinaciones_vs_victorias.png"),
    dpi=300,
    bbox_inches="tight"
)
plt.show()



# Separar las manos ganadas y no ganadas
ganadas = df[df["victoria"] == 1]["cantidad_jugadores"]
no_ganadas = df[df["victoria"] == 0]["cantidad_jugadores"]
print("\nEstadística de las manos ganadas:")
print(ganadas.describe())
print("\nEstadística de las manos no ganadas:")
print(no_ganadas.describe())


# Diagrama de cajas
plt.figure()
plt.boxplot([ganadas, no_ganadas])
plt.xticks([1, 2], ["Ganadas", "No ganadas"])
plt.title("Cantidad de jugadores según el resultado")
plt.xlabel("Resultado de la mano")
plt.ylabel("Cantidad de jugadores")
plt.grid(axis="y", alpha=0.3)
plt.savefig(
    os.path.join(ruta_evidencias, "10_boxplot_jugadores.png"),
    dpi=300,
    bbox_inches="tight"
)
plt.show()


# Identificación de las combinaciones finales
combinaciones_finales = []
for i in range(len(df)):
    asiento = str(df["asiento_hero"].iloc[i])
    resultados = df["results"].iloc[i]
    resultado_jugador = resultados["seats"].get(asiento, {})
    mano_final = resultado_jugador.get("final_hand", [])
    if len(mano_final) > 0:
        combinacion = mano_final[0].split(",")[0]
        combinaciones_finales.append(combinacion)
    else:
        combinaciones_finales.append("Desconocida")
df["combinacion_final"] = combinaciones_finales
print("\nCombinaciones finales:")
print(df[["combinacion_inicial", "combinacion_final"]])


#Calcular las frecuencias
frecuencia_finales = df["combinacion_final"].value_counts()
print("\nFrecuencia de combinaciones finales:")
print(frecuencia_finales)

#Generar y guardar la gráfica
plt.figure(figsize=(10, 6))
plt.barh(
    frecuencia_finales.index,
    frecuencia_finales.values
)
plt.title("Frecuencia de las combinaciones finales")
plt.xlabel("Frecuencia")
plt.ylabel("Combinación final")
plt.gca().invert_yaxis()
plt.savefig(
    os.path.join(ruta_evidencias, "11_combinaciones_finales.png"),
    dpi=300,
    bbox_inches="tight"
)
plt.show()


# Selección de las variables para el análisis posterior
df_procesado = df[[
    "hands_id",
    "game_type",
    "tournament",
    "seats",
    "cantidad_jugadores",
    "sb",
    "bb",
    "ante",
    "asiento_hero",
    "categoria_cartas",
    "combinacion_inicial",
    "combinacion_final",
    "victoria"
]]
print("\nDatos procesados:")
print(df_procesado.head())
print(df_procesado.shape)


# Guardar los datos procesados
df_procesado.to_csv(
    os.path.join(ruta_procesados, "manos_procesadas.csv"),
    index=False,
    encoding="utf-8"
)
print("\nDatos procesados guardados correctamente")





# Finalizar el registro de evidencias
print("\nFin del análisis exploratorio de datos")
archivo_salida.flush()
sys.stdout = sys.__stdout__
archivo_salida.close()
print("Archivo de evidencias generado correctamente.")