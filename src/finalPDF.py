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
    plt.savefig('src/img/promedio_tiempo.png')
    plt.show()

    return data


def calcularParametros(data):
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
    plt.savefig('src/img/parametros_tiempo.png')
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


if __name__ == "__main__":
    # ES SUPER DEMANDANTE SOLO ACTIVAR SI ES NECESARIO w(ﾟДﾟ)ww(ﾟДﾟ)ww(ﾟДﾟ)w
    # obtenerMejorFit(data)
    data = calcularPromedios(data)
    data, poly_loc, poly_scale = calcularParametros(data)
