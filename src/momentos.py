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
    variable_1 = data["variable_1"]
    # Calcular momentos
    media = np.mean(variable_1)
    desviacion_estandar = np.std(variable_1)

    plt.figure(figsize=(6, 5))

    # Histograma de variable_1
    plt.hist(
        variable_1,
        bins=50,
        density=True,
        alpha=0.6,
        color="blue",
        edgecolor='black')
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

    # Guardar la imagen del histograma de variable_1
    plt.savefig("src/img/histograma_variable_1_con_momentos.png")
    plt.show()


# 2. Visualizar histograma de variable_2 con marcas de momentos
def visualizar_histograma_var2():
    variable_2 = data["variable_2"]

    # Calcular momentos
    media = np.mean(variable_2)
    desviacion_estandar = np.std(variable_2)

    plt.figure(figsize=(6, 5))
    # Definir los límites de los bins
    bins = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 30]
    # Histograma de variable_2
    plt.hist(
        variable_2,
        bins=bins,
        density=True,
        alpha=0.6,
        color="green",
        edgecolor='black')
    plt.title("Histograma de variable_2")
    plt.xlim(0, 40)
    plt.xlabel("Variable_2")
    plt.ylabel("Densidad")

    # Marcar la media
    plt.axvline(
        media, color="r", linestyle="dashed", linewidth=2,
        label=f"Media: {media:.2f}"
    )
    # Marcar la desviación estándar
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

    # Guardar la imagen del histograma de variable_2
    plt.savefig("src/img/histograma_variable_2_con_momentos.png")
    plt.show()


# 3. Ajuste de modelos para variable_1 (distribución normal)
# con marcas de momentos.
def modelosVar1():
    variable_1 = data["variable_1"]
    params = norm.fit(variable_1)
    media = np.mean(variable_1)
    desviacion_estandar = np.std(variable_1)
    varianza = np.var(variable_1)
    inclinacion = skew(variable_1)
    curtosis = kurtosis(variable_1)

    x = np.linspace(variable_1.min(), variable_1.max(), 200)

    # Se obtiene el ajuste
    pdf = norm.pdf(x, *params)

    # Gráfico del histograma y el ajuste PDF
    plt.figure(figsize=(10, 5))
    plt.hist(
        variable_1, bins=50, density=True, alpha=0.6,
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

    # Añadir información de varianza, inclinación y curtosis
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

    plt.title("Histograma y ajuste de la distribución normal para variable_1")
    plt.xlabel("Variable_1")
    plt.ylabel("Densidad")
    plt.legend()

    # Guardar la imagen con el ajuste para variable_1
    plt.savefig("src/img/ajuste_variable_1_con_momentos.png")
    plt.show()


# 4. Ajuste de modelos para variable_2 (distribución exponencial)
# con marcas de momentos.
def modelosVar2():
    variable_2 = data["variable_2"]
    params = expon.fit(variable_2)
    media = np.mean(variable_2)
    desviacion_estandar = np.std(variable_2)
    varianza = np.var(variable_2)
    inclinacion = skew(variable_2)
    curtosis = kurtosis(variable_2)

    x = np.linspace(variable_2.min(), variable_2.max(), 200)
    # Se obtiene el ajuste
    pdf = expon.pdf(x, *params)

    # Gráfico del histograma y el ajuste PDF
    # Definir los límites de los bins
    bins = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 30]
    plt.figure(figsize=(10, 5))
    plt.hist(
        variable_2, bins=bins, density=True, alpha=0.6,
        color="green", label="Histograma", edgecolor="black"
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

    # Añadir información de varianza, inclinación y curtosis
    plt.text(
        0.09, 0.85, f"Varianza: {varianza:.2f}",
        transform=plt.gca().transAxes, fontsize=10
    )
    plt.text(
        0.09, 0.80, f"Asimetría (Skewness): {inclinacion:.2f}",
        transform=plt.gca().transAxes, fontsize=10
    )
    plt.text(
        0.09, 0.75, f"Curtosis: {curtosis:.2f}",
        transform=plt.gca().transAxes, fontsize=10
    )

    plt.title(
        "Histograma y ajuste de la distribución"
        " exponencial para variable_2"
    )
    plt.xlim(0, 40)
    plt.xlabel("Variable_2")
    plt.ylabel("Densidad")
    plt.legend()

    # Guardar la imagen con el ajuste para variable_2
    plt.savefig("src/img/ajuste_variable_2_con_momentos.png")
    plt.show()


# 5. Calcular momentos (promedio, varianza,
# desviación estándar, inclinación, kurtosis)
def calcular_momentos(variable, nombre_variable):
    media = np.mean(variable)
    varianza = np.var(variable)
    desviacion_estandar = np.std(variable)
    inclinacion = skew(variable)
    curtosis = kurtosis(variable)

    print(f"Momentos de {nombre_variable}:")
    print(f"Media: {media}")
    print(f"Varianza: {varianza}")
    print(f"Desviación estándar: {desviacion_estandar}")
    print(f"Asimetría (Skewness): {inclinacion}")
    print(f"Curtosis: {curtosis}\n")


# 6. Ejecutar todo el programa
if __name__ == "__main__":
    visualizar_histograma_var1()  # Generar y guardar histograma de variable_1
    visualizar_histograma_var2()  # Generar y guardar histograma de variable_2

    # Calcular y mostrar momentos
    calcular_momentos(data["variable_1"], "Variable_1")
    calcular_momentos(data["variable_2"], "Variable_2")

    # Calcular y mostrar momentos
    modelosVar1()  # Generar y guardar ajuste sobre histograma de variable_1
    modelosVar2()  # Generar y guardar ajuste sobre histograma de variable_2
