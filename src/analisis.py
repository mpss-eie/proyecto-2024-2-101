import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm, expon
from scipy.integrate import cumulative_trapezoid
import sqlite3

# Extraer los datos a usar.
conn = sqlite3.connect("proyecto.db")
data = pd.read_sql_query("SELECT * FROM test_data", conn)


#  Encontrar modelos de variable_1
def modelosVar1():
    # Se obtienen los datos de la variable_1
    variable_1 = data["variable_1"]
    params = norm.fit(variable_1)
    x = np.linspace(variable_1.min(), variable_1.max(), 200)

    # Se obtienen los ajustes
    pdf = norm.pdf(x, *params)
    cdf = norm.cdf(x, *params)

    # Se arma una figura con 2 gráficos
    plt.figure(figsize=(10, 5))
    plt.suptitle('Histograma y ajuste de la '
                 'distribución normal para variable_1')

    # Mostrar PDF
    plt.subplot(1, 2, 1)
    plt.plot(x, pdf, 'r-', lw=2, label='PDF')
    plt.title('Función de densidad de probabilidad')
    plt.xlabel('Variable_1')
    plt.ylabel('Probabilidad')
    # Se agrega el histograma
    plt.hist(variable_1, bins=50, density=True, alpha=0.6,
             color="blue", label="Histograma", edgecolor="black")

    # Mostrar CDF
    plt.subplot(1, 2, 2)
    plt.plot(x, cdf, 'b-', lw=2, label='CDF')
    plt.title('Función de probabilidad acumulativa')
    plt.xlabel('Variable_1')
    plt.ylabel('Probabilidad acumulativa')

    plt.tight_layout()
    plt.savefig("src/img/ajuste_variable_1.png")
    plt.show()


#   Encontrar modelos de variable_2
def modelosVar2():
    max_x = 20

    # Se obtienen los datos de la variable_2
    variable_2 = data["variable_2"]
    params = expon.fit(variable_2)
    x = np.linspace(variable_2.min(), max_x, 200)

    # Se obtienen los ajustes
    pdf = expon.pdf(x, *params)
    cdf = expon.cdf(x, *params)

    # Se arma una figura con 2 gráficos
    plt.figure(figsize=(10, 5))
    plt.suptitle('Histograma y ajuste de la '
                 'distribución exponencial para variable_2')

    # Mostrar PDF
    plt.subplot(1, 2, 1)
    plt.plot(x, pdf, 'r-', lw=2, label='PDF')
    plt.title('Función de densidad de probabilidad')
    plt.xlabel('Variable_2')
    plt.ylabel('Probabilidad')

    # Se agrega el histograma
    # Definir los límites de los bins
    bins = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 30]
    plt.hist(variable_2, bins=bins, density=True, alpha=0.6,
             color="green", label="Histograma", edgecolor="black")

    # Mostrar CDF
    plt.subplot(1, 2, 2)
    plt.plot(x, cdf, 'b-', lw=2, label='CDF')
    plt.title('Función de probabilidad acumulativa')
    plt.xlabel('Variable_2')
    plt.ylabel('Probabilidad acumulativa')

    plt.tight_layout()
    plt.savefig("src/img/ajuste_variable_2.png")
    plt.show()


def comparacionFormula():
    max_x = 20

    bins = 1000

    # Se obtienen los datos de la variable_2
    variable_2 = data["variable_2"]
    params = expon.fit(variable_2)
    x = np.linspace(variable_2.min(), max_x, 200)

    # Se obtienen los ajustes
    pdf = expon.pdf(x, *params)
    cdf = expon.cdf(x, *params)

    # Crear una figura con una cuadrícula de 2x2
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    fig.suptitle('Comparativa entre PDF exponencial y por fórmula.')

    # Primer gráfico: PDF
    axes[0, 0].plot(x, pdf, 'r-', lw=2, label='PDF')
    axes[0, 0].hist(variable_2, bins=bins, density=True, alpha=0.6,
                    color="green", label="Histograma", edgecolor="black")
    axes[0, 0].set_xlim([0, 20])
    axes[0, 0].set_title('Función de densidad de probabilidad')
    axes[0, 0].set_xlabel('Variable_2')
    axes[0, 0].set_ylabel('Densidad de Probabilidad')

    # Segundo gráfico: CDF
    axes[0, 1].plot(x, cdf, 'b-', lw=2, label='CDF')
    axes[0, 1].set_title('Función de probabilidad acumulativa')
    axes[0, 1].set_xlabel('Variable_2')
    axes[0, 1].set_ylabel('Probabilidad acumulativa')

    # Redefinir límites de x para fórmula
    # Esto evita problemas donde la ecuación se hace muy grande.
    x = np.linspace(1.07, 50, 500)

    # Tercer gráfico: PDF con fórmula
    axes[1, 0].plot(x, pdfEcuacion(x), 'b-', lw=2, label='PDF')
    axes[1, 0].hist(variable_2, bins=bins, density=True, alpha=0.6,
                    color="green", label="Histograma", edgecolor="black")
    axes[1, 0].set_xlim([0, 20])
    axes[1, 0].set_title('Función de densidad de probabilidad con fórmula')
    axes[1, 0].set_xlabel('Variable_2')
    axes[1, 0].set_ylabel('Densidad de Probabilidad')

    # Cuarto gráfico: CDF con fórmula
    axes[1, 1].plot(x, cdfEcuacion(x), 'b-', lw=2, label='CDF')
    axes[1, 1].set_xlim([0, 20])
    axes[1, 1].set_title('Función de probabilidad acumulativa con fórmula')
    axes[1, 1].set_xlabel('Variable_2')
    axes[1, 1].set_ylabel('Probabilidad acumulativa')

    plt.tight_layout()
    plt.savefig("src/img/comparativa_ajustes.png")
    plt.show()


def pdfEcuacion(x):
    mu = -0.000339176289247862
    std2 = 1.6719790870752245

    return 1/(2*np.sqrt(x-1)*np.sqrt(2*np.pi*std2)) \
        * (np.exp(-(np.power(np.sqrt(x-1)-mu, 2))/(2*std2))
           + np.exp(-(np.power(-np.sqrt(x-1)-mu, 2))/(2*std2)))


def cdfEcuacion(x):
    return np.concatenate(([0], cumulative_trapezoid(pdfEcuacion(x), x=x)))


# 5. Ejecutar todo el programa
if __name__ == "__main__":
    modelosVar1()  # Generar y guardar ajuste sobre histograma de variable_1
    modelosVar2()  # Generar y guardar ajuste sobre histograma de variable_2
    comparacionFormula()
