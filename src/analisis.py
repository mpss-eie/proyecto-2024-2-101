import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm, expon
import sqlite3

# Extraer los datos a usar.
conn = sqlite3.connect("proyecto.db")
data = pd.read_sql_query("SELECT * FROM test_data", conn)


# 1. Visualizar histograma de variable_1
def visualizar_histograma_var1():
    plt.figure(figsize=(6, 5))

    # Histograma de variable_1
    plt.hist(data["variable_1"], bins=50, density=True, alpha=0.6, color="blue")
    plt.title("Histograma de variable_1")
    plt.xlabel("Variable_1")
    plt.ylabel("Densidad")

    # Guardar la imagen del histograma de variable_1
    #plt.savefig("histograma_variable_1.png")
    plt.show()


# 2. Visualizar histograma de variable_2
def visualizar_histograma_var2():
    plt.figure(figsize=(6, 5))

    # Histograma de variable_2
    plt.hist(data["variable_2"], bins=50, density=True, alpha=0.6, color="green")
    plt.title("Histograma de variable_2")
    plt.xlabel("Variable_2")
    plt.ylabel("Densidad")

    # Guardar la imagen del histograma de variable_2
    #plt.savefig("histograma_variable_2.png")
    plt.show()


# 3. Ajuste de modelos para variable_1 (distribución normal) con visualización
def modelosVar1():
    variable_1 = data["variable_1"]
    params = norm.fit(variable_1)
    x = np.linspace(variable_1.min(), variable_1.max(), 200)

    # Se obtiene el ajuste
    pdf = norm.pdf(x, *params)
    # Gráfico del histograma y el ajuste PDF
    plt.figure(figsize=(10, 5))
    plt.hist(variable_1, bins=50, density=True, alpha=0.6, color="blue", label="Histograma", edgecolor = "black")
    plt.plot(x, pdf, "r-", lw=2, label="PDF Ajustado")
    plt.title("Histograma y ajuste de la distribución normal para variable_1")
    plt.xlabel("Variable_1")
    plt.ylabel("Densidad")
    plt.legend()
    # Guardar la imagen con el ajuste para variable_1
    plt.savefig("src/img/ajuste_variable_1.png")
    plt.show()


# 4. Ajuste de modelos para variable_2 (distribución exponencial) con visualización
def modelosVar2():
    variable_2 = data["variable_2"]
    params = expon.fit(variable_2)
    x = np.linspace(variable_2.min(), variable_2.max(), 200)
    # Se obtiene el ajuste
    pdf = expon.pdf(x, *params)
    # Gráfico del histograma y el ajuste PDF
    bins = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 30] # Definir los límites de los bins
    plt.figure(figsize=(10, 5))
    plt.hist(variable_2, bins=bins, density=True, alpha=0.6, color="green", label="Histograma", edgecolor="black")
    plt.plot(x, pdf, "r-", lw=2, label="PDF Ajustado")
    plt.title("Histograma y ajuste de la distribución exponencial para variable_2")
    plt.xlim(0,40)
    plt.xlabel("Variable_2")
    plt.ylabel("Densidad")
    plt.legend()

    # Guardar la imagen con el ajuste para variable_2
    plt.savefig("src/img/ajuste_variable_2.png")
    plt.show()


# 5. Ejecutar todo el programa
if __name__ == "__main__":
    modelosVar1()  # Generar y guardar ajuste sobre histograma de variable_1
    modelosVar2()  # Generar y guardar ajuste sobre histograma de variable_2
