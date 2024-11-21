import pandas as pd
import sqlite3
from fitter import Fitter
import matplotlib
import matplotlib.pyplot as plt
# import numpy as np
# from scipy.stats import norm, expon
# from scipy.integrate import cumulative_trapezoid

matplotlib.use('TkAgg')

# Extraer los datos a usar.
conn = sqlite3.connect("proyecto.db")
data = pd.read_sql_query("SELECT * FROM data_proyecto", conn)


# Distribuciones indicadas
distributions = [
  "expon",
  "gompertz",
  "levy",
  "logistic",
  "norm",
  "rayleigh",
]


def calcularPromedios(data):
    # Calcular el promedio y agregarlo al dataFrame
    data['promedio'] = data.groupby('minutes')['value'].transform('mean')

    # Ordenar el dataFrame
    data = data.sort_values(by=['minutes', 'id']).reset_index(drop=True)

    print(data[data['minutes'] == 0])

    print(data)

    return data


def histogramaInstante(df):
    """
    Genera
    """
    # Crear el histograma
    plt.figure()
    plt.hist(df, density=True, bins=100, edgecolor='black')
    plt.title('Histograma de valor en cierto instante.')
    plt.xlabel('Valores de variable')
    plt.ylabel('densidad')
    # Guardar el gráfico como un archivo .png
    plt.show()


def obtenerFuncionDensidad():
    valores = data['value']

    # Datos correspondientes a un mismo instante de tiempo
    instante1 = valores.iloc[0:100]
    f_1 = Fitter(instante1.values, distributions=distributions)
    f_1.fit()
    # f_1.summary()

    instante2 = valores.iloc[100:200]
    f_2 = Fitter(instante2.values, distributions=distributions)
    f_2.fit()
    # f_2.get_best()

    instante3 = valores.iloc[200:300]
    f_3 = Fitter(instante3.values, distributions=distributions)
    f_3.fit()
    # f_3.get_best()

    f_2.summary()
    plt.show()
    histogramaInstante(instante2)


if __name__ == "__main__":
    # obtenerFuncionDensidad()
    data = calcularPromedios(data)
