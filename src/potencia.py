import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


def graficar_promedio_por_minuto():
    """
    Esta función conecta con una base de datos SQLite llamada 'proyecto.db',
    extrae los datos de la tabla 'data_proyecto', y calcula el promedio de los
    valores (columna 'value') para cada minuto (columna 'minutes'). Luego,
    grafica estos promedios a lo largo del tiempo (minutos desde medianoche) y
    guarda la gráfica como una imagen.

    Pasos:
    1. Conexión a la base de datos SQLite.
    2. Extracción de datos de la tabla 'data_proyecto'.
    3. Agrupación por la columna 'minutes' para calcular
    el promedio de 'value'.
    4. Generación de un gráfico de línea con los resultados.
    5. Guardado de la gráfica en un archivo y visualización de la misma.
    """

    # Conectar a la base de datos
    conexion = sqlite3.connect("proyecto.db")

    # Leer los datos de la tabla
    query = "SELECT minutes, value FROM data_proyecto"
    df = pd.read_sql_query(query, conexion)

    # Cerrar la conexión
    conexion.close()

    # Agrupar por 'minutes' y calcular el promedio de 'value'
    promedio_por_minuto = df.groupby("minutes")["value"].mean()

    # Graficar los promedios
    plt.figure(figsize=(10, 6))
    promedio_por_minuto.plot(kind="line", color="blue")
    plt.title("Promedio por minuto")
    plt.xlabel("Minutos desde medianoche")
    plt.ylabel("Promedio de valores")
    plt.grid(True)
    plt.savefig("docs/img/proceso")  # Guardar la gráfica como una imagen
    plt.show()


# Llamar a la función
graficar_promedio_por_minuto()


def calcular_potencia_promedio():
    """
    Esta función conecta con la base de datos 'proyecto.db', extrae los datos
    de la tabla 'data_proyecto', y calcula:
    - El promedio de los valores en la columna 'value'.
    - El promedio de los valores en 'value' para cuando la columna 'sunlight'
      es igual a 1 y 0, respectivamente.
    - La potencia promedio, que es el segundo momento de los valores
    (promedio de
    los valores elevados al cuadrado) para los casos con y sin luz solar.
    Luego, imprime los resultados calculados.

    Pasos:
    1. Conexión a la base de datos SQLite.
    2. Extracción de datos de la tabla 'data_proyecto'.
    3. Cálculo del promedio de la columna 'value'.
    4. Filtrado y cálculo del promedio de 'value' para
    'sunlight' == 1 y 'sunlight' == 0.
    5. Cálculo de la potencia promedio para ambos casos de 'sunlight'.
    6. Cálculo del MSE (promedio del cuadrado de los valores).
    7. Impresión de los resultados.
    """

    # Conectar a la base de datos
    conexion = sqlite3.connect("proyecto.db")

    # Leer los datos de la tabla
    query = "SELECT value, sunlight FROM data_proyecto"
    df = pd.read_sql_query(query, conexion)

    # Cerrar la conexión
    conexion.close()

    # Calcular el promedio de los valores
    promedio = df["value"].mean()

    # Calcular el promedio y MSE para sunlight = 1
    df_sunlight_1 = df[df["sunlight"] == 1]
    promedio_1 = df_sunlight_1["value"].mean()
    pot_with_sunlight = (df_sunlight_1["value"] ** 2).mean()

    # Calcular el promedio y MSE para sunlight = 0
    df_sunlight_0 = df[df["sunlight"] == 0]
    promedio_0 = df_sunlight_0["value"].mean()
    pot_without_sunlight = (df_sunlight_0["value"] ** 2).mean()

    # Imprimir los resultados
    print(
        f"Sunlight = 1 -> Promedio: {promedio_1}"
        f"Potencia Promedio: {pot_with_sunlight}"
        )
    print(
        f"Sunlight = 0 -> Promedio: {promedio_0}"
        f"Potencia Promedio: {pot_without_sunlight}"
        )

    # Calcular el MSE: (x_i - promedio)^2 y luego el promedio de esos valores
    pot_total = (df["value"] ** 2).mean()

    print(
        f"El promedio total es {promedio}"
        f"La potencia promedio total es {pot_total}"
        )


# Llamada a la función
calcular_potencia_promedio()
