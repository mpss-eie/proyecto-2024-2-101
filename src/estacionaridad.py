import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import os

# Extraer los datos a usar.
conn = sqlite3.connect("proyecto.db")
data = pd.read_sql_query("SELECT * FROM data_proyecto", conn)


def guardar_grafica(ruta, nombre):
    """
    Guarda la gráfica actual en la ruta especificada con el nombre
    proporcionado.

    Esta función verifica si la ruta de destino existe, y si no, la
    crea. Luego, guarda la gráfica actual en la ruta proporcionada,
    con el nombre de archivo indicado y una resolución de 300 dpi.
    Finalmente, cierra la gráfica para liberar recursos.

    Parámetros:
    ruta (str): Directorio en el que se guardará la gráfica.
    nombre (str): Nombre del archivo de la gráfica, incluyendo
    la extensión (por ejemplo, 'grafica.png').

    Ejemplo:
    guardar_grafica('src/imagenes', 'grafica.png')
    """
    if not os.path.exists(ruta):
        os.makedirs(ruta)
    plt.savefig(os.path.join(ruta, nombre), dpi=300)
    plt.close()  # Cierra la gráfica después de guardarla


def analizar_noche(data, ruta_guardado='src_im'):
    """
    Analiza los datos de la noche para calcular y graficar la correlación en
    ventanas de 40 minutos.

    Esta función filtra los datos para obtener solo los valores
    correspondientes a la noche (0-359 y 1080-1400 minutos),
    ajusta los minutos para que los rangos sean continuos, calcula el
    promedio por minuto y luego calcula la correlación en ventanas de 40
    minutos desplazadas (lagged correlation). Finalmente, genera una gráfica
    de estas correlaciones.

    Parámetros:
    data (DataFrame): Conjunto de datos con columnas 'minutes' y 'value'.
    ruta_guardado (str): Ruta donde se guardará la gráfica generada
    (por defecto, 'src_im').

    Ejemplo:
    analizar_noche(data)
    """
    # Filtrar datos de noche (0-359 y 1080-1400)
    data_noche = data[(data['minutes'].between(0, 359)) |
                      (data['minutes'].between(1080, 1400))].copy()

    # Ajustar los minutos para que los rangos sean continuos
    data_noche['minutes'] = data_noche['minutes'].apply(
        lambda x: x if x <= 359 else x - 720)

    # Calcular el promedio por minuto
    promedio_noche = data_noche.groupby('minutes')['value'].mean()

    # Calcular correlación en ventanas de 40-40 minutos usando numpy.corrcoef
    ventana_correlacion = []
    minutos_ordenados = promedio_noche.index.sort_values()
    for inicio in range(0, len(minutos_ordenados) - 40, 40):
        ventana = promedio_noche.iloc[inicio:inicio + 40]

        # Calcular la correlación (lagged correlation)
        x = ventana.values[:-1]  # Valores actuales
        y = ventana.values[1:]   # Valores desplazados (lag 1)
        correlacion = np.corrcoef(x, y)[0, 1]

        ventana_correlacion.append((minutos_ordenados[inicio], correlacion))

    # Mostrar resultados de la correlación por ventanas
    print("Correlación por ventanas de 40 a 40 minutos (noche):")
    for inicio, corr in ventana_correlacion:
        print(f"Minuto {inicio}-{inicio+40}: Correlación = {corr:.4f}")

    # Graficar las correlaciones
    inicio_ventanas = [v[0] for v in ventana_correlacion]
    valores_correlacion = [v[1] for v in ventana_correlacion]

    plt.figure(figsize=(10, 5))
    plt.bar(inicio_ventanas, valores_correlacion, width=15, color="purple")
    plt.axhline(0, color="black", linestyle="--")
    plt.title("Correlación en ventanas de 40-40 minutos (noche)")
    plt.xlabel("Minuto de inicio de la ventana")
    plt.ylabel("Correlación")
    plt.grid()

    # Guardar la gráfica de correlación
    guardar_grafica(ruta_guardado, "correlacion_noche.png")


def analizar_noche_con_covarianza(data, ruta_guardado='src_im'):
    """
    Analiza los datos de la noche para calcular y graficar la covarianza
    en ventanas de 40 minutos.

    Esta función filtra los datos para obtener solo los valores
    correspondientes a la noche (0-359 y 1080-1400 minutos), calcula
    el promedio por minuto y luego calcula la covarianza en ventanas de
    40 minutos desplazadas. Finalmente, genera una gráfica de estas
    covarianzas.

    Parámetros:
    data (DataFrame): Conjunto de datos con columnas 'minutes' y 'value'.
    ruta_guardado (str): Ruta donde se guardará la gráfica generada
    (por defecto, 'src_im').

    Ejemplo:
    analizar_noche_con_covarianza(data)
    """
    # Filtrar datos de noche
    data_noche = data[(data['minutes'].between(0, 359)) |
                      (data['minutes'].between(1080, 1400))]

    # Calcular promedios por minuto
    promedio_noche = data_noche.groupby('minutes')['value'].mean()

    # Calcular covarianza en ventanas de 40-40 minutos
    ventana_covarianza = []
    # Saltos de 40 minutos
    for inicio in range(0, len(promedio_noche) - 40, 40):
        ventana = promedio_noche.iloc[inicio:inicio + 40]

        # Cálculo de la covarianza
        x = ventana.values[:-1]  # Valores actuales
        y = ventana.values[1:]   # Valores desplazados (lag 1)
        # Matriz de covarianza y seleccionamos el valor [0, 1]
        covarianza = np.cov(x, y)[0, 1]

        ventana_covarianza.append((inicio, covarianza))

    # Mostrar resultados
    print("Covarianza por ventanas de 40 a 40 minutos (noche):")
    for inicio, cov in ventana_covarianza:
        print(f"Minuto {inicio}-{inicio+40}: Covarianza = {cov:.4f}")

    # Graficar covarianzas
    inicio_ventanas = [v[0] for v in ventana_covarianza]
    valores_covarianza = [v[1] for v in ventana_covarianza]

    plt.figure(figsize=(10, 5))
    plt.bar(inicio_ventanas, valores_covarianza, width=15, color="green")
    plt.axhline(0, color="black", linestyle="--")
    plt.title("Covarianza en ventanas de 40-40 minutos (noche)")
    plt.xlabel("Minuto de inicio de la ventana")
    plt.ylabel("Covarianza")
    plt.grid()

    # Guardar la gráfica de covarianza
    guardar_grafica(ruta_guardado, "covarianza_noche.png")


def verificar_estacionaridad(data, ruta_guardado='src/img'):
    """
    Verifica la estacionaridad de los datos nocturnos mediante el cálculo de
    media móvil y varianza.

    Esta función filtra los datos para obtener solo los valores
    correspondientes a la noche (0-359 y 1080-1400 minutos),
    ajusta los minutos para que los rangos sean continuos,
    calcula el promedio por minuto, luego calcula y grafica
    la media móvil y la varianza en ventanas de 40 minutos. Finalmente,
    se guarda la gráfica de la media móvil y varianza.

    Parámetros:
    data (DataFrame): Conjunto de datos con columnas 'minutes' y 'value'.
    ruta_guardado (str): Ruta donde se guardará la gráfica generada
    (por defecto, 'src/img').

    Ejemplo:
    verificar_estacionaridad(data)
    """
    # Filtrar datos nocturnos y ajustar minutos
    # Crear una copia explícita del DataFrame filtrado
    data_noche = data[(data['minutes'].between(0, 359)) |
                      (data['minutes'].between(1080, 1400))].copy()

    # Ajustar los minutos en la copia
    data_noche['minutes'] = data_noche['minutes'].apply(
        lambda x: x if x <= 359 else x - 720)

    # Calcular promedio por minuto
    promedio_noche = data_noche.groupby('minutes')['value'].mean()

    # Calcular media móvil
    ventana = 40
    media_movil = promedio_noche.rolling(window=ventana, center=True).mean()

    # Graficar promedio y media móvil
    plt.figure(figsize=(10, 5))
    plt.plot(promedio_noche.index, promedio_noche.values,
             label="Promedio por minuto", color="blue", alpha=0.7)
    plt.plot(promedio_noche.index, media_movil,
             label=f"Media móvil ({ventana} minutos)",
             color="orange", linestyle="--")
    plt.axhline(promedio_noche.mean(), color="red",
                linestyle="--", label="Media global")
    plt.title("Análisis de estacionaridad: promedio y media móvil")
    plt.xlabel("Minutos")
    plt.ylabel("Promedio")
    plt.legend()
    plt.grid()
    guardar_grafica(ruta_guardado, "media_movil_noche.png")

    # Calcular y mostrar varianza por ventanas
    varianzas = []
    inicio_minutos = range(0, len(promedio_noche), 40)
    for inicio in inicio_minutos:
        ventana_datos = promedio_noche.iloc[inicio:inicio + 40]
        varianza = ventana_datos.var()
        varianzas.append((inicio, varianza))

    # Mostrar varianzas
    print("Varianza por ventanas de 40 minutos:")
    for inicio, var in varianzas:
        print(f"Minuto {inicio}-{inicio + 40}: Varianza = {var:.4f}")

    # Graficar varianzas
    plt.figure(figsize=(10, 5))
    plt.bar([v[0] for v in varianzas], [v[1] for v in varianzas],
            width=15, color="purple", alpha=0.7)
    plt.axhline(np.mean([v[1] for v in varianzas]), color="red",
                linestyle="--",
                label=f"Varianza media: {varianza:.4f}")
    plt.title("Varianza por ventanas de 40 minutos")
    plt.xlabel("Minuto de inicio de la ventana")
    plt.ylabel("Varianza")
    plt.legend()
    plt.grid()
    guardar_grafica(ruta_guardado, "varianza_noche.png")


if __name__ == "__main__":
    # Ruta donde se guardarán las imágenes
    ruta_imagenes = 'src_im'

    # Análisis para la noche
    # Determinar estacionaridad
    analizar_noche(data, ruta_guardado=ruta_imagenes)
    analizar_noche_con_covarianza(data, ruta_guardado=ruta_imagenes)
    verificar_estacionaridad(data, ruta_guardado=ruta_imagenes)
    print("Análisis nocturno completo."
          f"Imágenes guardadas en {os.path.abspath(ruta_imagenes)}.")
