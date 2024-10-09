import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats
import sqlite3

# Extraer los datos a usar.
conn = sqlite3.connect("proyecto.db")
data = pd.read_sql_query("SELECT * FROM test_data", conn)

# 1. Visualizar histograma de los datos


# 2. Crear distribuciones


# 3. Visualizar los momentos
