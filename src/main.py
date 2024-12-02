# Importaciones necesarias
from histogramas import histograma_variable_1, histograma_variable_2
from analisis import modelosVar1, modelosVar2, comparacionFormula
from momentos import (visualizar_histograma_var1, visualizar_histograma_var2,
                      calcular_momentos_var1, calcular_momentos_var2,
                      modelosMomentosVar1, modelosMomentosVar2)
from finalPDF import calcularPromedios, calcularParametros, mostrarPDF3D
from ergo import analizar_ergodicidad
from estacionaridad import (analizar_noche, analizar_noche_con_covarianza,
                            verificar_estacionaridad)
from potencia import calcular_potencia_promedio, graficar_promedio_por_minuto
import pandas as pd
import sqlite3


def avance():
    """Función que reune todas las funciones para el análisis correspondiente
    al avance de proyecto.
    """
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

    # Generar y guardar una imagen comparativa
    # entre los modelos de las variables
    comparacionFormula()

    # Visualizar y guardar el histograma de la variable 1
    visualizar_histograma_var1()

    # Visualizar y guardar el histograma de la variable 2
    visualizar_histograma_var2()

    # Calcular y mostrar momentos estadísticos (media, varianza, etc.)
    # para la variable 1
    calcular_momentos_var1(data["variable_1"], "Variable_1")

    # Calcular y mostrar momentos estadísticos (media, varianza, etc.)
    # para la variable 2
    calcular_momentos_var2(data["variable_2"], "Variable_2")

    # Ajustar modelos de distribución basados en los momentos estadísticos
    # para la variable 1
    modelosMomentosVar1()

    # Ajustar modelos de distribución basados en los momentos estadísticos
    # para la variable 2
    modelosMomentosVar2()


def final():
    """Función que reune todas las funciones para el análisis correspondiente
    a la sección final del proyecto.
    """
    data = pd.read_sql_query("SELECT * FROM data_proyecto", conn)

    # Se obtiene figura de promedio en función del tiempo
    data = calcularPromedios(data)

    # Se genera figura de los parámetros de la distribución
    # en función del tiempo
    data, func_mu, func_sigma = calcularParametros(data)

    # Mostrar gráfico 3D de la PDF obtenida
    mostrarPDF3D(func_mu, func_sigma)

    # Se hace el análisis de la estacionaridad/ergodicidad
    ruta_imagenes = 'src/img'
    analizar_ergodicidad(data, ruta_guardado=ruta_imagenes)

    analizar_noche(data, ruta_guardado=ruta_imagenes)
    analizar_noche_con_covarianza(data, ruta_guardado=ruta_imagenes)
    verificar_estacionaridad(data, ruta_guardado=ruta_imagenes)

    # Se calcula la potencia promedio y promedio por minuto
    graficar_promedio_por_minuto()
    calcular_potencia_promedio()


if __name__ == "__main__":
    """
    Ejecuta las funciones realizadas en los otros archivos .py
    para visualizacion de los histogramas de cada variable, así
    como la obtención de sus modelos y momentos y las comparaciones
    de dichos resultados.
    """

    # Se genera un menú para escoger la sección de código a ejecutar
    print("Digite la sección de código que quiere correr:")
    print("1 - Solo avance")
    print("2 - Solo parte final")
    print("Algo más - Todas las secciones")
    seccion = input("Digite una opción: ")

    # Establecer conexión a la base de datos SQLite
    conn = sqlite3.connect("proyecto.db")

    match seccion:
        case "1":
            avance()
        case "2":
            final()
        case _:
            avance()
            final()
