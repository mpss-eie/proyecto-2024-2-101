import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, skew, kurtosis, norm


# Conectar a la base de datos SQLite
conn = sqlite3.connect('proyecto.db')

# Ejecutar una consulta SQL y cargar los datos en un DataFrame
df = pd.read_sql_query("SELECT * FROM test_data", conn)

# Cerrar la conexión
conn.close()



# Calcular la media y desviación estándar de variable_1 para el ajuste a la distribución normal
mu_1, std_1 = norm.fit(df['variable_1'])

# Calcular la media y desviación estándar de variable_2 para el ajuste a la distribución normal
mu_2, std_2 = norm.fit(df['variable_2'])

# Crear un espacio de valores para la curva de densidad
x_1 = np.linspace(min(df['variable_1']), max(df['variable_1']), 100)
x_2 = np.linspace(min(df['variable_2']), max(df['variable_2']), 100)

# Calcular la función de densidad de probabilidad (PDF) para ambas variables
pdf_1 = norm.pdf(x_1, mu_1, std_1)
pdf_2 = norm.pdf(x_2, mu_2, std_2)

# Graficar el histograma y la curva de probabilidad para variable_1
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.hist(df['variable_1'], bins=50, density=True, alpha=0.6, color='blue', edgecolor='black')
plt.plot(x_1, pdf_1, 'r-', lw=2, label=f'Normal Fit\n$\mu={mu_1:.2f}$, $\sigma={std_1:.2f}$')
plt.title('Histograma y Modelo de Probabilidad - variable_1')
plt.xlabel('Valores de variable_1')
plt.ylabel('Densidad')
plt.legend()

# Graficar el histograma y la curva de probabilidad para variable_2
plt.subplot(1, 2, 2)
plt.hist(df['variable_2'], bins=100, density=True, alpha=0.6, color='green', edgecolor='black')
plt.plot(x_2, pdf_2, 'r-', lw=2, label=f'Normal Fit\n$\mu={mu_2:.2f}$, $\sigma={std_2:.2f}$')
plt.title('Histograma y Modelo de Probabilidad - variable_2')
plt.xlim(0,40)
plt.xlabel('Valores de variable_2')
plt.ylabel('Densidad')
plt.legend()

plt.tight_layout()


plt.savefig('histogramas.png')


# Calcular los momentos para variable_1
mean_1 = np.mean(df['variable_1'])  # Promedio
variance_1 = np.var(df['variable_1'])  # Varianza
std_dev_1 = np.std(df['variable_1'])  # Desviación estándar
skewness_1 = skew(df['variable_1'])  # Inclinación (skewness)
kurt_1 = kurtosis(df['variable_1'])  # Kurtosis

# Calcular los momentos para variable_2
mean_2 = np.mean(df['variable_2'])  # Promedio
variance_2 = np.var(df['variable_2'])  # Varianza
std_dev_2 = np.std(df['variable_2'])  # Desviación estándar
skewness_2 = skew(df['variable_2'])  # Inclinación (skewness)
kurt_2 = kurtosis(df['variable_2'])  # Kurtosis

# Imprimir resultados para variable_1
print("Momentos para variable_1:")
print(f"Promedio: {mean_1}")
print(f"Varianza: {variance_1}")
print(f"Desviación Estándar: {std_dev_1}")
print(f"Inclinación (Skewness): {skewness_1}")
print(f"Kurtosis: {kurt_1}\n")

# Imprimir resultados para variable_2
print("Momentos para variable_2:")
print(f"Promedio: {mean_2}")
print(f"Varianza: {variance_2}")
print(f"Desviación Estándar: {std_dev_2}")
print(f"Inclinación (Skewness): {skewness_2}")
print(f"Kurtosis: {kurt_2}")


#plt.show()


# Crear el histograma con variable_1
#plt.hist(df['variable_1'], bins=50, edgecolor='black')  # edgecolor añade líneas entre las barras

# Añadir etiquetas y título
#plt.title('Histograma de variable_1')
#plt.xlabel('Valores de variable_1')
#plt.ylabel('Frecuencia')



# Crear el histograma con variable_1
#plt.hist(df['variable_2'], bins=500, edgecolor='black') 
#plt.xlim(0, 40)  # Cambia 0 y 10 por los límites que desees
#
## Añadir etiquetas y título
#plt.title('Histograma de variable_2')
#plt.xlabel('Valores de variable_2')
#plt.ylabel('Frecuencia')
#
#
plt.savefig('histograma_variable_2.png')

