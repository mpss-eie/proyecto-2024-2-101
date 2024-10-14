# Importaciones necesarias
 # Módulo que contiene funciones para generar histogramas de las variables
from histogramas import histograma_variable_1, histograma_variable_2
# Módulo que contiene funciones para modelar distribuciones y comparar fórmulas
from analisis import modelosVar1, modelosVar2, comparacionFormula  
 # Módulo para cálculos de momentos estadísticos y visualización de histogramas
from momentos import (visualizar_histograma_var1, visualizar_histograma_var2,
                      calcular_momentos_var1, calcular_momentos_var2, 
                      modelosMomentosVar1, modelosMomentosVar2)
import pandas as pd  # Biblioteca para manejo y análisis de datos
import sqlite3  # Biblioteca para interactuar con bases de datos SQLite

if __name__ == "__main__":
    """ 
    Ejecutas las funciones realizadas en los otros archivos .py
    para visualizacion de los histogramas de cada variable, asi
    como la obtencion de sus modelos y momentos y las comparaciones
    de dichos resultados.
    
    """

    # Establecer conexión a la base de datos SQLite
    conn = sqlite3.connect("proyecto.db")

    # Extraer los datos de la tabla 'test_data' de la base de datos
    data = pd.read_sql_query("SELECT * FROM test_data", conn)

    # Generar y guardar el histograma de la variable 1
    histograma_variable_1(data)

    # Generar y guardar el histograma de la variable 2
    histograma_variable_2(data)

    # Ajustar modelos de distribución sobre el histograma de la variable 1
    modelosVar1()

    # Ajustar modelos de distribución sobre el histograma de la variable 2
    modelosVar2()

    # Generar y guardar una imagen comparativa entre los modelos de las variables
    comparacionFormula()

    # Visualizar y guardar el histograma de la variable 1
    visualizar_histograma_var1()

    # Visualizar y guardar el histograma de la variable 2
    visualizar_histograma_var2()

    # Calcular y mostrar momentos estadísticos (media, varianza, etc.) para la variable 1
    calcular_momentos_var1(data["variable_1"], "Variable_1")

    # Calcular y mostrar momentos estadísticos (media, varianza, etc.) para la variable 2
    calcular_momentos_var2(data["variable_2"], "Variable_2")

    # Ajustar modelos de distribución basados en los momentos estadísticos para la variable 1
    modelosMomentosVar1()

    # Ajustar modelos de distribución basados en los momentos estadísticos para la variable 2
    modelosMomentosVar2()
