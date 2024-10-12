import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


# Conectar a la base de datos SQLite
conn = sqlite3.connect('proyecto.db')

# Ejecutar una consulta SQL y cargar los datos en un DataFrame
df = pd.read_sql_query("SELECT * FROM test_data", conn)

# Cerrar la conexión
conn.close()


def histograma_variable_1(df):
    # Crear el histograma
    plt.figure()
    plt.hist(df['variable_1'], density=True, bins=50, edgecolor='black')
    plt.title('Histograma de variable_1')
    plt.xlabel('Valores de variable_1')
    plt.ylabel('densidad')
    # Guardar el gráfico como un archivo .png
    plt.savefig('src/img/histograma_variable_1.png')
    plt.show()


def histograma_variable_2(df):
    # Crear el histograma
    plt.figure()

    # Definir los límites de los bins
    bins = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 30]
    plt.hist(
        df['variable_2'],
        bins=bins,
        density=True,
        alpha=0.6,
        color='g',
        edgecolor='black')
    plt.title("Histograma de variable_2")
    plt.xlabel('Variable_2')
    plt.ylabel('Densidad')
    # Guardar el gráfico como un archivo .png
    plt.savefig('src/img/histograma_variable_2.png')
    plt.show()


if __name__ == "__main__":
    histograma_variable_1(df)
    histograma_variable_2(df)
