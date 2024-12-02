import pandas as pd
import sqlite3
from fitter import Fitter
import matplotlib.pyplot as plt
from collections import Counter
from scipy.stats import norm
import numpy as np

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


def obtenerMejorFit(data):
    """Función para contar la cantidad de veces que
    una distribución es el mejor ajuste para los datos,
    usando toda la muestra de datos.

    :param data: Datos recolectados por 24 horas
    :type data: DataFrame
    """
    valores = data['value']

    # Iniciar contadores de cantidad de veces que
    # aparece una distribución como la mejor, general y según si es día
    contador_general = Counter()
    contador_dia = Counter()
    contador_noche = Counter()

    # Obtener el mejor fit de cada instante de tiempo
    x = 0
    for _ in range(max(data['minutes'].values) - 1):
        # Valores y estado de sunlight del instante
        instante = valores.iloc[x:x + 100]
        sunlight = data['sunlight'].iloc[x]

        # Hacer el fit
        f = Fitter(instante.values, distributions=distributions)
        f.fit()

        # Agregar a contadores
        contador_general[next(iter(f.get_best()))] += 1

        if sunlight:
            contador_dia[next(iter(f.get_best()))] += 1
        else:
            contador_noche[next(iter(f.get_best()))] += 1
        x += 100

    print('\nContador general:')
    print(contador_general)

    print('\nContador dia:')
    print(contador_dia)

    print('\nContador noche:')
    print(contador_noche)


def calcularPromedios(data):
    """Función para calcular los promedios de cada instante
    y graficarlos en función del tiempo.

    :param data: Datos recolectados por 24 horas
    :type data: DataFrame
    :param data: Datos recolectados por 24 horas con promedios agregados
    :type data: DataFrame
    """
    # Calcular el promedio y agregarlo al dataFrame
    data['average'] = data.groupby('minutes')['value'].transform('mean')

    # Ordenar el dataFrame
    data = data.sort_values(by=['minutes', 'id']).reset_index(drop=True)

    # Mostrar figura de los promedios vs minutos
    eje_minutos = data[['minutes', 'average']].drop_duplicates()

    # Plot
    plt.figure(figsize=(8, 5))
    plt.plot(eje_minutos['minutes'], eje_minutos['average'],
             marker='o', linestyle='-')
    # sns.lineplot(data=eje_minutos, x='minutes', y='average', marker='o')
    plt.title('Promedio de proceso en función del tiempo.')
    plt.xlabel('Tiempo (Minutos)')
    plt.ylabel('Promedio')
    plt.grid()
    plt.savefig('src/img/promedio_tiempo.png', dpi=300)
    plt.show()

    return data


def calcularParametros(data):
    """Función para calcular los parámetros de un ajuste normal
    en cada instante de tiempo. También los grafica en función
    del tiempo.

    :param data: Datos recolectados por 24 horas
    :type data: DataFrame
    :param data: Datos recolectados con parámetros y funciones de estos
                 en el tiempo
    :type data: DataFrame, np.poly1d, np.poly1d
    """
    # Se agrupan en minutos y se sacan sus valores
    agrupados = data.groupby('minutes')['value']

    # Se calculan los parámetros y se crean como columnas
    params = agrupados.apply(lambda x: norm.fit(x)).apply(pd.Series)
    params.columns = ['loc', 'scale']

    # Se agregan al dataFrame original
    data = data.merge(params, left_on='minutes', right_index=True)

    # Se reordena
    data = data.sort_values(by=['minutes', 'id']).reset_index(drop=True)

    # Se grafica la variación de los parámetros
    eje_minutos = data[['minutes', 'loc', 'scale']].drop_duplicates()

    plt.figure(figsize=(8, 5))
    plt.plot(eje_minutos['minutes'], eje_minutos['loc'],
             marker='o', linestyle='--', label='μ')
    plt.plot(eje_minutos['minutes'], eje_minutos['scale'],
             marker='o', linestyle='--', label='σ')

    # Se hacen las aproximaciones y se grafican

    # Se usan los datos de día
    datos_dia = data[data['sunlight'] == 1].drop_duplicates()
    minDia = min(data[data['sunlight'] == 1]['minutes'])
    maxDia = max(data[data['sunlight'] == 1]['minutes'])

    # Se consiguen los polinomios
    poly_loc = np.poly1d(np.polyfit(datos_dia['minutes'],
                                    datos_dia['loc'], 2))

    poly_scale = np.poly1d(np.polyfit(datos_dia['minutes'],
                                      datos_dia['scale'], 2))

    # Se muestran los polinomios y los límites del día
    plt.plot(eje_minutos['minutes'], poly_loc(eje_minutos['minutes']),
             label='Polinomio μ')

    plt.plot(eje_minutos['minutes'], poly_scale(eje_minutos['minutes']),
             label='Polinomio σ')

    plt.plot((minDia, minDia), (-0.5, 7.2), scaley=False,
             linestyle='dashed', color='gray')
    plt.plot((maxDia, maxDia), (-0.5, 7.2), scaley=False,
             linestyle='dashed', color='gray')

    plt.text(1000, 6.5, 'Día', color='black')
    plt.text(200, 6.5, 'Noche', color='black')
    plt.text(200, 6.5, 'Noche', color='black')

    # Personalización
    plt.title('Variación de parámetros loc (μ) y scale (σ) según el tiempo.')
    plt.xlabel('Tiempo (Minutos)')
    plt.ylabel('Valor de parámetros')
    plt.grid()
    plt.legend()
    plt.ylim(top=7.2, bottom=-0.5)
    plt.savefig('src/img/parametros_tiempo.png', dpi=300)
    plt.show()

    # Se muestran los polinomios
    coef_loc = poly_loc.coefficients
    print(f"Poly_loc (μ) = {coef_loc[0]}t^2 + {coef_loc[1]}t "
          f"+ {coef_loc[2]}")

    coef_scale = poly_scale.coefficients
    print(f"Poly_scale (σ) = {coef_scale[0]}t^2 + {coef_scale[1]}t "
          f"+ {coef_scale[2]}")

    # Se indican los límites del día
    print(f"Inicio del sunlight en minuto: {minDia}")
    print(f"Final del sunlight en minuto: {maxDia}")

    return data, poly_loc, poly_scale


def pdf(x, t, func_mu, func_sigma):
    """Función para calcular valores de la PDF combinada para distintos
    valores de tiempo y variable aleatoria.

    :param x: Variable aleatoria
    :type x: NDArray
    :param t: Eje de tiempo a evaluar
    :type t: NDArray
    :param func_mu: Función de mu dependiente del tiempo
    :type func_mu: np.poly1d
    :param func_sigma: Función de sigma dependiente del tiempo
    :type func_sigma: np.poly1d
    :return: Superficie 3D de la PDF evaluada.
    :rtype: NDArray
    """
    # Se revisa si es de día o de noche
    mask = (t > 360) & (t < 1079)

    # Se calculan los parámetros según condición del día
    sigma = np.where(mask, func_sigma(t), 1)
    mu = np.where(mask, func_mu(t), 0)

    # Se calcula la densidad de probabilidad
    return (1 / np.sqrt(2 * np.pi * sigma**2)) \
        * np.exp(-((x - mu)**2) / (2 * sigma**2))


def mostrarPDF3D(func_mu, func_sigma):
    """Función que genera un gráfico 3D de la PDF evaluada en distintos
    puntos de tiempo y variable aleatoria.

    :param func_mu: Función de mu dependiente del tiempo
    :type func_mu: np.poly1d
    :param func_sigma: Función de sigma dependiente del tiempo
    :type func_sigma: np.poly1d
    """

    # Se generan vectores para los ejes
    x = np.linspace(-5, 15, 200)
    t = np.linspace(0, 24*60, 200)

    # Se juntan en una superficie
    X, T = np.meshgrid(x[:, None], t)

    # Se calcula el valor de la PDF
    Z = pdf(X, T, func_mu, func_sigma)

    # Se genera el gráfico
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(X, T, Z, cmap='viridis', edgecolor='none')

    # Personalización
    ax.set_xlabel('Variable aleatoria (x)')
    ax.set_ylabel('Tiempo en minutos (t)')
    ax.set_zlabel('PDF')
    ax.set_title('Gráfico 3D de PDF')
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10)
    ax.view_init(elev=23, azim=-51)

    plt.savefig('src/img/pdf3D.png')
    plt.show()


if __name__ == "__main__":
    # Solo habilitar esta función si se quiere verificar mejor ajuste
    # tiene tiempo de duración extenso
    obtenerMejorFit(data)
    data = calcularPromedios(data)
    data, func_mu, func_sigma = calcularParametros(data)
    mostrarPDF3D(func_mu, func_sigma)
