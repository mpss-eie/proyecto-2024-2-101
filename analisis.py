import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm, expon
from scipy.integrate import cumulative_trapezoid
import sqlite3

# Extraer los datos a usar.
conn = sqlite3.connect("proyecto.db")
data = pd.read_sql_query("SELECT * FROM test_data", conn)

# 1. Visualizar histograma de los datos


# 2. Crear distribuciones

#   Encontrar modelos de variable_1
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

    # Mostrar PDF
    plt.subplot(1, 2, 1)
    plt.plot(x, pdf, 'r-', lw=2, label='PDF')
    plt.title('Función de densidad de probabilidad')
    plt.xlabel('Variable_1')
    plt.ylabel('Probabilidad')

    # Mostrar CDF
    plt.subplot(1, 2, 2)
    plt.plot(x, cdf, 'b-', lw=2, label='CDF')
    plt.title('Función de probabilidad acumulativa')
    plt.xlabel('Variable_1')
    plt.ylabel('Probabilidad acumulativa')

    plt.tight_layout()
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

    # Crear una figura con una cuadrícula de 2x2
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Primer gráfico: PDF
    axes[0, 0].plot(x, pdf, 'r-', lw=2, label='PDF')
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
    x = np.linspace(1.01, 20, 500)

    # Tercer gráfico: PDF con fórmula
    axes[1, 0].plot(x, pdfEcuacion(x), 'b-', lw=2, label='PDF')
    axes[1, 0].set_xlim(left=1.077)
    axes[1, 0].set_title('Función de probabilidad acumulativa con fórmula')
    axes[1, 0].set_xlabel('Variable_2')
    axes[1, 0].set_ylabel('Densidad de Probabilidad')

    # Cuarto gráfico: CDF con fórmula
    axes[1, 1].plot(x, cdfEcuacion(x), 'b-', lw=2, label='CDF')
    axes[1, 1].set_title('Función de probabilidad acumulativa con fórmula')
    axes[1, 1].set_xlabel('Variable_2')
    axes[1, 1].set_ylabel('Probabilidad acumulativa')

    plt.tight_layout()
    plt.show()


def pdfEcuacion(x):
    mu = -0.000339176289247862
    std2 = 1.6719790870752245

    return 1/(2*np.sqrt(x-1)*np.sqrt(2*np.pi*std2)) \
        * (np.exp(-(np.power(np.sqrt(x-1)-mu, 2))/(2*std2))
           + np.exp(-(np.power(-np.sqrt(x-1)-mu, 2))/(2*std2)))


def cdfEcuacion(x):
    return np.concatenate(([0], cumulative_trapezoid(pdfEcuacion(x), x=x)))


# 3. Visualizar los momentos


if __name__ == "__main__":
    modelosVar1()
    modelosVar2()
