import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm, expon, skew, kurtosis
import sqlite3

# Extraer los datos a usar.
conn = sqlite3.connect("proyecto.db")
data = pd.read_sql_query("SELECT * FROM test_data", conn)


# 1. Visualizar histograma de variable_1 con marcas de momentos
def visualizar_histograma_var1():
    """
    Genera un histograma de los datos de 'variable_1' con líneas
    marcando la media y una desviación estándar (por encima y por
    debajo de la media). Además, guarda la imagen generada en formato PNG.

    Parámetros:
    -----------
    Ninguno. Los datos son tomados directamente de la variable 'data' global.

    Salida:
    -------
    Muestra un gráfico del histograma de 'variable_1' y guarda la imagen como
    "docs/img/histograma_variable_1_con_momentos.png".
    """

    # Obtener los datos de variable_1
    variable_1 = data["variable_1"]

    # Calcular la media y desviación estándar de los datos
    media = np.mean(variable_1)
    desviacion_estandar = np.std(variable_1)

    # Crear la figura
    plt.figure(figsize=(10, 5))

    # Generar el histograma de variable_1
    plt.hist(
        variable_1,
        bins=100,           # Número de barras en el histograma
        density=True,       # Normalización para que el área total sea 1
        alpha=0.6,          # Transparencia
        color="blue",       # Color de las barras
        edgecolor='black'   # Color del borde de las barras
    )

    # Título y etiquetas del gráfico
    plt.title("Histograma de variable_1")
    plt.xlabel("Variable_1")
    plt.ylabel("Densidad")

    # Marcar la media
    plt.axvline(
        media, color="r", linestyle="dashed", linewidth=2,
        label=f"Media: {media:.2f}"
    )

    # Marcar la desviación estándar (una por cada lado de la media)
    plt.axvline(
        media - desviacion_estandar,
        color="g", linestyle="dotted", linewidth=2,
        label=f"-1σ: {media - desviacion_estandar:.2f}"
    )
    plt.axvline(
        media + desviacion_estandar,
        color="g", linestyle="dotted", linewidth=2,
        label=f"+1σ: {media + desviacion_estandar:.2f}"
    )

    # Añadir la leyenda
    plt.legend()

    # Guardar la imagen generada
    plt.savefig("docs/img/histograma_variable_1_con_momentos.png")

    # Mostrar el gráfico
    plt.show()


# 2. Visualizar histograma de variable_2 con ajuste a distribución exponencial
def visualizar_histograma_var2():
    """
    Genera un histograma de los datos de 'variable_2' con un ajuste de
    distribución exponencial. Marca la media y una desviación estándar
    (por encima y por debajo de la media).
    Además, guarda la imagen generada en formato PNG.

    Parámetros:
    -----------
    Ninguno. Los datos son tomados directamente de la variable 'data' global.

    Salida:
    -------
    Muestra un gráfico del histograma de 'variable_2' y guarda la imagen como
    "docs/img/histograma_variable_2_con_momentos.png".
    """

    # Obtener los datos de variable_2
    variable_2 = data["variable_2"]

    # Ajustar la distribución exponencial a los datos
    params = expon.fit(variable_2)

    # Calcular momentos teóricos (media y varianza) de la distribución ajustada
    media, varianza = expon.stats(*params, moments='mv')

    # Desviación estándar es la raíz cuadrada de la varianza
    desviacion_estandar = np.sqrt(varianza)

    # Crear la figura
    plt.figure(figsize=(10, 5))

    # Generar el histograma de variable_2
    plt.hist(
        variable_2,
        bins=1500,          # Número de barras en el histograma
        density=True,       # Normalización para que el área total sea 1
        alpha=0.6,          # Transparencia
        color="green",      # Color de las barras
        edgecolor='black'   # Color del borde de las barras
    )

    # Título y etiquetas del gráfico
    plt.title("Histograma de variable_2")
    plt.xlim(-2, 25)        # Límite del eje x
    plt.xlabel("Variable_2")
    plt.ylabel("Densidad")

    # Marcar la media
    plt.axvline(
        media, color="r", linestyle="dashed", linewidth=2,
        label=f"Media: {media:.2f}"
    )

    # Marcar la desviación estándar (una por cada lado de la media)
    plt.axvline(
        media - desviacion_estandar,
        color="g", linestyle="dotted", linewidth=2,
        label=f"-1σ: {media - desviacion_estandar:.2f}"
    )
    plt.axvline(
        media + desviacion_estandar,
        color="g", linestyle="dotted", linewidth=2,
        label=f"+1σ: {media + desviacion_estandar:.2f}"
    )

    # Añadir la leyenda
    plt.legend()

    # Guardar la imagen generada
    plt.savefig("docs/img/histograma_variable_2_con_momentos.png")

    # Mostrar el gráfico
    plt.show()


# 3. Ajuste de modelos para variable_1 (distribución normal)
# con marcas de momentos.
def modelosMomentosVar1():
    """
    Ajusta un modelo de distribución normal a los datos de variable_1
    y visualiza un histograma junto con la función de densidad
    ajustada. Se marcan momentos estadísticos como la media,
    la desviación estándar, la varianza, la asimetría y la curtosis.
    """
    variable_1 = data["variable_1"]

    # Ajustar la distribución normal a los datos de variable_1
    params = norm.fit(variable_1)

    # Calcular momentos estadísticos
    media = np.mean(variable_1)
    desviacion_estandar = np.std(variable_1)
    varianza = np.var(variable_1)
    inclinacion = skew(variable_1)
    curtosis = kurtosis(variable_1)

    # Generar un rango de valores x para la función de densidad
    x = np.linspace(variable_1.min(), variable_1.max(), 200)

    # Se obtiene la PDF ajustada para la distribución normal
    pdf = norm.pdf(x, *params)

    # Gráfico del histograma y la PDF ajustada
    plt.figure(figsize=(10, 5))
    plt.hist(
        variable_1, bins=100, density=True, alpha=0.6,
        color="blue", label="Histograma", edgecolor="black"
    )
    plt.plot(x, pdf, "r-", lw=2, label="PDF Ajustado")

    # Marcar la media y la desviación estándar
    plt.axvline(
        media, color="r", linestyle="dashed", linewidth=2,
        label=f"Media: {media:.2f}"
    )
    plt.axvline(
        media - desviacion_estandar,
        color="g", linestyle="dotted", linewidth=2,
        label=f"-1σ: {media - desviacion_estandar:.2f}"
    )
    plt.axvline(
        media + desviacion_estandar,
        color="g", linestyle="dotted", linewidth=2,
        label=f"+1σ: {media + desviacion_estandar:.2f}"
    )

    # Añadir información de varianza, inclinación y curtosis al gráfico
    plt.text(
        0.05, 0.85, f"Varianza: {varianza:.2f}",
        transform=plt.gca().transAxes, fontsize=10
    )
    plt.text(
        0.05, 0.80, f"Asimetría (Skewness): {inclinacion:.2f}",
        transform=plt.gca().transAxes, fontsize=10
    )
    plt.text(
        0.05, 0.75, f"Curtosis: {curtosis:.2f}",
        transform=plt.gca().transAxes, fontsize=10
    )

    # Añadir título y etiquetas a los ejes
    plt.title("Histograma y ajuste de la distribución normal para variable_1")
    plt.xlabel("Variable_1")
    plt.ylabel("Densidad")
    plt.legend()

    # Guardar la imagen con el ajuste para variable_1
    plt.savefig("docs/img/ajuste_variable_1_con_momentos.png")
    plt.show()


# 4. Ajuste de modelos para variable_2 (distribución exponencial)
# con marcas de momentos.
def modelosMomentosVar2():
    """
    Ajusta un modelo de distribución exponencial a los datos de variable_2
    y visualiza un histograma junto con la función de densidad
    ajustada. Se marcan momentos estadísticos como la media,
    la desviación estándar, la varianza, la asimetría y la curtosis.
    """
    variable_2 = data["variable_2"]

    # Ajustar la distribución exponencial a los datos
    params = expon.fit(variable_2)

    # Cálculos de los momentos teóricos a partir de la distribución ajustada
    media, varianza, inclinacion, curtosis = expon.stats(
        *params, moments='mvsk'
    )

    # Desviación estándar es la raíz cuadrada de la varianza
    desviacion_estandar = np.sqrt(varianza)

    # Definir los valores x para graficar la PDF ajustada
    x = np.linspace(variable_2.min(), variable_2.max(), 1000)
    # Se obtiene la PDF ajustada
    pdf = expon.pdf(x, *params)

    # Gráfico del histograma y el ajuste de la PDF
    plt.figure(figsize=(10, 5))
    plt.hist(
        variable_2, bins=1500, density=True, alpha=0.6,
        color="green", label="Histograma", edgecolor="black"
    )
    plt.plot(x, pdf, "r-", lw=2, label="PDF Ajustado")

    # Marcar la media y la desviación estándar en el gráfico
    plt.axvline(
        media, color="r", linestyle="dashed", linewidth=2,
        label=f"Media: {media:.2f}"
    )
    plt.axvline(
        media - desviacion_estandar,
        color="g", linestyle="dotted", linewidth=2,
        label=f"-1σ: {media - desviacion_estandar:.2f}"
    )
    plt.axvline(
        media + desviacion_estandar,
        color="g", linestyle="dotted", linewidth=2,
        label=f"+1σ: {media + desviacion_estandar:.2f}"
    )

    # Añadir información de varianza, inclinación y curtosis en el gráfico
    plt.text(
        0.38, 0.85, f"Varianza: {varianza:.2f}",
        transform=plt.gca().transAxes, fontsize=10
    )
    plt.text(
        0.38, 0.80, f"Asimetría (Skewness): {inclinacion:.2f}",
        transform=plt.gca().transAxes, fontsize=10
    )
    plt.text(
        0.38, 0.75, f"Curtosis: {curtosis:.2f}",
        transform=plt.gca().transAxes, fontsize=10
    )

    # Añadir título y etiquetas a los ejes
    plt.title(
        "Histograma y ajuste de la distribución"
        " exponencial para variable_2"
    )
    plt.xlim(-2, 25)
    plt.xlabel("Variable_2")
    plt.ylabel("Densidad")
    plt.legend()

    # Guardar la imagen con el ajuste para variable_2
    plt.savefig("docs/img/ajuste_variable_2_con_momentos.png")
    plt.show()


# 5. Calcular momentos (promedio, varianza,
# desviación estándar, inclinación, kurtosis)
def calcular_momentos_var1(variable, nombre_variable):
    """
    Calcula y muestra los momentos estadísticos (media, varianza,
    desviación estándar, asimetría y curtosis) de una variable dada.

    Parameters:
    variable: array-like
        Datos de la variable para calcular los momentos.
    nombre_variable: str
        Nombre de la variable, utilizado para la salida en consola.
    """
    media = np.mean(variable)
    varianza = np.var(variable)
    desviacion_estandar = np.std(variable)
    inclinacion = skew(variable)
    curtosis = kurtosis(variable)

    # Imprimir los momentos calculados
    print(f"Momentos de {nombre_variable}:")
    print(f"Media: {media}")
    print(f"Varianza: {varianza}")
    print(f"Desviación estándar: {desviacion_estandar}")
    print(f"Asimetría (Skewness): {inclinacion}")
    print(f"Curtosis: {curtosis}\n")


# 6. Calcular momentos (promedio, varianza,
# desviación estándar, inclinación, kurtosis)
# para una distribución exponencial ajustada.
def calcular_momentos_var2(variable, nombre_variable):
    """
    Calcula y muestra los momentos estadísticos (media, varianza,
    desviación estándar, asimetría y curtosis) de una variable dada,
    asumiendo que se ajusta a una distribución exponencial.

    Parameters:
    variable: array-like
        Datos de la variable para calcular los momentos.
    nombre_variable: str
        Nombre de la variable, utilizado para la salida en consola.
    """
    # Ajustar la distribución exponencial a los datos
    params = expon.fit(variable)

    # Obtener los momentos de la distribución exponencial ajustada
    media, varianza, inclinacion, curtosis = expon.stats(
        *params, moments='mvsk'
    )

    # Desviación estándar es la raíz cuadrada de la varianza
    desviacion_estandar = np.sqrt(varianza)

    # Imprimir los resultados
    print(f"Momentos de {nombre_variable} (Distribución Exponencial):")
    print(f"Media: {media}")
    print(f"Varianza: {varianza}")
    print(f"Desviación estándar: {desviacion_estandar}")
    print(f"Asimetría (Skewness): {inclinacion}")
    print(f"Curtosis: {curtosis}\n")
