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
    """ Genera los ajustes de función de densidad y probabilidad
        acumulativa de la variable_1, genera gráficos de estas y
        los guarda en /src/img. Emplea ajuste de scipy.stats.norm.
    """

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
    # Se guarda la figura
    plt.savefig("src/img/ajuste_variable_1.png")
    plt.show()


#   Encontrar modelos de variable_2
def modelosVar2():
    """ Genera los ajustes de función de densidad y probabilidad
        acumulativa de la variable_2, genera gráficos de estas y
        los guarda en /src/img. Emplea el ajuste de scipy.stats.expon.
    """
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
    """ Genera 2 ajustes de función de densidad y probabilidad
        acumulativa de la variable_2, genera gráficos de estas y
        los guarda en /src/img. Emplea dos ajustes distintos uno
        con el ajuste exponencial de scipy.stats.expon y el otro
        proviene de las funciones pdfEcuacion y cdfEcuacion.
    """

    # Se obtienen los datos de la variable_2
    variable_2 = data["variable_2"]
    params = expon.fit(variable_2)
    x = np.linspace(variable_2.min(), variable_2.max(), 1500)

    # Se obtienen los ajustes
    pdf = expon.pdf(x, *params)
    cdf = expon.cdf(x, *params)

    # Crear una figura con una cuadrícula de 2x2
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Comparativa entre PDF exponencial y por fórmula.')

    max_x = 20  # Límite en x para la graficación de las curvas.
    bins = 1000  # Cantidad de barras a graficar del histograma.

    # Primer gráfico: PDF
    axes[0, 0].plot(x, pdf, 'r-', lw=2, label='PDF')
    axes[0, 0].hist(variable_2, bins=bins, density=True, alpha=0.6,
                    color="green", label="Histograma", edgecolor="black")
    axes[0, 0].set_xlim([0, max_x])
    axes[0, 0].set_title('Función de densidad de probabilidad')
    axes[0, 0].set_xlabel('Variable_2')
    axes[0, 0].set_ylabel('Densidad de Probabilidad')

    # Segundo gráfico: CDF
    axes[0, 1].plot(x, cdf, 'b-', lw=2, label='CDF')
    axes[0, 1].set_xlim([0, max_x])
    axes[0, 1].set_title('Función de probabilidad acumulativa')
    axes[0, 1].set_xlabel('Variable_2')
    axes[0, 1].set_ylabel('Probabilidad acumulativa')

    # Redefinir límites de x para fórmula
    # Esto evita problemas donde la ecuación
    # se hace muy grande por indefinición.
    xFormula = np.linspace(1.009, 50, 500)

    # Tercer gráfico: PDF con fórmula
    axes[1, 0].plot(xFormula, pdfEcuacion(xFormula), 'b-', lw=2, label='PDF')
    axes[1, 0].hist(variable_2, bins=bins, density=True, alpha=0.6,
                    color="green", label="Histograma", edgecolor="black")
    axes[1, 0].set_xlim([0, max_x])
    axes[1, 0].set_ylim([0, 1])
    axes[1, 0].set_title('Función de densidad de probabilidad con fórmula')
    axes[1, 0].set_xlabel('Variable_2')
    axes[1, 0].set_ylabel('Densidad de Probabilidad')

    # Cuarto gráfico: CDF con fórmula
    axes[1, 1].plot(xFormula, cdfEcuacion(xFormula), 'b-', lw=2, label='CDF')
    axes[1, 1].set_xlim([0, max_x])
    axes[1, 1].set_title('Función de probabilidad acumulativa con fórmula')
    axes[1, 1].set_xlabel('Variable_2')
    axes[1, 1].set_ylabel('Probabilidad acumulativa')

    plt.tight_layout()
    plt.savefig("src/img/comparativa_ajustes.png")
    plt.show()


def pdfEcuacion(x):
    """ Función de densidad de probabilidad con la
        fórmula calculada. Proviene del cálculo de
        la función de densidad de una variable aleatoria
        resultante de una transformación no monotónica en
        una variable aleatoria normal.

    :param x: Dominio en el que se calcula/grafica la PDF.
    :type x: numpy.ndarray
    :return: Función evaluada en distintos puntos del dominio x.
    :rtype: numpy.ndarray
    """

    # Parámetros obtenidos del ajuste normal de la variable_1
    variable_1 = data["variable_1"]
    [mu, std] = norm.fit(variable_1)

    # En la fórmula se usa la varianza, por lo que se eleva al
    # cuadrado, esto reduce el tamaño de la ecuación escrita.
    std2 = std**2

    # Se retorna la ecuación evaluada en x, la ecuación se detalla
    # en la documentación (Sección de avance, en el anexo)
    return 1/(2*np.sqrt(x-1)*np.sqrt(2*np.pi*std2)) \
        * (np.exp(-(np.power(np.sqrt(x-1)-mu, 2))/(2*std2))
           + np.exp(-(np.power(-np.sqrt(x-1)-mu, 2))/(2*std2)))


def cdfEcuacion(x):
    """ Se genera la función de probabilidad acumulativa
        correspondiente a la función de densidad calculada
        en la función pdfEcuacion. Se usa una integración
        acumulativa con regla trapezoidal para evitar errores
        por no tomar en cuenta el periodo entre datos. Se
        asigna un valor inicial 0.

    :param x: Dominio en el que se calcula/grafica la CDF.
    :type x: numpy.ndarray
    :return: Función evaluada en distintos puntos del dominio x.
    :rtype: numpy.ndarray
    """
    return cumulative_trapezoid(pdfEcuacion(x), x=x, initial=0)
