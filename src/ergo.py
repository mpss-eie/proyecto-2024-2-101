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


def analizar_ergodicidad(data, ruta_guardado="src/img"):
    """
    Analiza la ergodicidad de los datos de la muestra durante la noche.

    Esta función calcula dos promedios: el promedio estadístico global
    (promedio de todos los datos nocturnos) y el promedio temporal (promedio
    de la función muestra). Luego, compara ambos promedios y determina si los
    datos son ergódicos, según si ambos promedios son cercanos entre sí.

    Además, genera y guarda una gráfica que muestra la función muestra, el
    promedio temporal y el promedio estadístico.

    Parámetros:
    data (DataFrame): El conjunto de datos que contiene una columna
    'minutes' con los minutos transcurridos y una columna 'value' con
    los valores correspondientes.
    ruta_guardado (str): Ruta donde se guardarán las imágenes generadas
    (por defecto, "src/img").

    Imprime en consola el promedio estadístico global, el promedio temporal
    y si los datos son ergódicos o no.

    Ejemplo:
    analizar_ergodicidad(data)
    """
    # Filtrar los datos para el cálculo del promedio estadístico
    data_noche_estadistico = data[(
        data["minutes"].between(0, 359)) |
        (data["minutes"].between(1080, 1400))]

    # Promedio estadístico (promedio global de los datos nocturnos)
    promedio_estadistico = data_noche_estadistico["value"].mean()

    # Filtrar los datos para el cálculo del promedio temporal
    #  (1 dato por minuto)
    data_noche_temporal = data[(
        data["minutes"].between(0, 359)) |
        (data["minutes"].between(1080, 1400))]

    # Ajustar los minutos entre 1080 y 1400
    data_noche_temporal.loc[data_noche_temporal["minutes"]
                            >= 1080, "minutes"] -= 1080
    data_noche_temporal.loc[data_noche_temporal["minutes"]
                            >= 0, "minutes"] += 360

    # Agrupar por minuto y tomar el promedio de cada grupo
    data_noche_temporal = data_noche_temporal.groupby("minutes")[
        "value"].mean()

    # Promedio temporal (promedio de la función muestra)
    promedio_temporal = data_noche_temporal.mean()

    # Reducir los datos para la visualización: tomar una muestra cada X minutos
    muestra_reducida = data_noche_temporal[::1]

    # Filtrar para solo mostrar los valores de tiempo deseados (0-720)
    muestra_reducida = muestra_reducida[muestra_reducida.index < 720]

    # Graficar la función muestra
    plt.figure(figsize=(10, 5))
    plt.plot(muestra_reducida.index, muestra_reducida.values,
             label="Función muestra")
    plt.axhline(
        promedio_temporal,
        color="red",
        linestyle="--",
        label=f"Promedio temporal:{promedio_temporal:.4f}",
    )
    plt.axhline(
        promedio_estadistico,
        color="green",
        linestyle="-.",
        label=f"Promedio estadístico:{promedio_estadistico:.4f}",
    )
    plt.title(
        "Función muestra, Promedio temporal"
        " y Promedio estadístico de los datos nocturnos"
    )
    plt.xlabel("Tiempo (minutos)")
    plt.ylabel("Valor")
    plt.legend()
    plt.grid()

    # Guardar la gráfica
    guardar_grafica(ruta_guardado, "funcion_muestra.png")

    # Comparar promedios
    print(f"Promedio estadístico (global): {promedio_estadistico:.4f}")
    print(f"Promedio temporal de la muestra: {promedio_temporal:.4f}")

    if np.isclose(promedio_estadistico, promedio_temporal, atol=0.1):
        print("Los datos son ergódicos.")
    else:
        print("Los datos NO son ergódicos.")


if __name__ == "__main__":
    # Ruta donde se guardarán las imágenes
    ruta_imagenes = "src_im2"

    # Determinar ergodicidad.
    analizar_ergodicidad(data, ruta_guardado=ruta_imagenes)
