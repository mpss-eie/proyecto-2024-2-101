# Avance del Proyecto
A continuacion se va a presentar lo que se realizó para el avance del protecto de Modelos Probabilisticos de señales y sistemas.
## Cambios en el modelo de base de datos y tareas de recoleccion de datos
En los dados de `models.py` y `task.py` se realizan cambios menores para la creacion de base de datos en el archivo `models.py` ya que en los datos que se van a recibir `kalouk.xyz` por medio de la API, son dos variables de tipo float, y el modelo esta hecho para tres variables, de la misma forma se adaptó la tarea de recoleccion de datos en el archivo `task.py` para que esté construidos para dos variables.
## Recoleccion de datos  

Para la recoleccion de datos se estuvo realizando una solicitud a la API para obtener los datos de la pagina web, en un periodo de 15 segundos, en el cual se va a estar recibiendo 100 datos en ese perido, para esto se utilizó el administrador de tareas `Celery Worker` en conjunto con el planificador de tareas `Celery Beat` con el intermediador de `redis` para que se pueda recolectar 12 horas continuas los datos del sitio web, al final, se dejó un poco mas de tiempo recolectando datos,alrededor de 14 horas , por lo cual se recopilaron cerca de 330 000 datos.

## Análisis exploratorio de los datos

Se recopilaron dos conjuntos de datos `variable_1` y `variable_2`, con distribuciones desconocidas y con una transformación indicada como: `variable_2` = (`variable_1`)^2 + 1.

###  Gráficas descriptivas de `variable_1` y `variable_2`

Para obtener una presentacion visual de la manera que estan distribuidos los datos se crearon los histogramas de las variables.

##### Variable_1
![Histograma de variable_1](img/histogramaVariable_1.png)
##### Variable_2
![Histograma de variable_2](img/histogramaVariable_2.png)

Se aprecia que en `variable_1` posee una distribucion normal o gaussiana, ya que se aprecia la famosa forma de campana y es simetrica, mientras que `variable_2` tiene una distribución aparentemente exponencial debido a que se pasa tener una densidad grande a una pequeña de una forma muy rapida.

### Modelos de probabilidad para los datos

Se obtuvieron los modelos de ambas variables, para esto se calculan la función de densidad de probabilidad (PDF) y la función de probabilidad acumulativa (CDF) de ambas.

##### Variable_1
![PDF y CDF Variable_1](img/ajuste_variable_1.png)
##### Variable_2
![PDF y CDF Variable_2](img/comparativa_ajustes.png)

Las PDF y CDF del modelo para la `variable_1` y el primer set de la `variable_2` se calcularon por medio de módulos de python con la librería `scipy.stats`. Se calcularon según los modelos identificados en la sección anterior (normal y exponencial). Para la `variable_1` se nota que el modelo se ajusta relativamente bien en forma, pues la curva sigue el comportamiento del histograma y se muestra como el CDF aumenta drásticamente cerca de los puntos más probables y se estabiliza en 1. Para la `variable_2` se empleó primeramente el modelo exponencial, generando las figuras superiores que presentan un ajuste ligeramente más lento en decrecimiento al del histograma pero cumplen en la mayoría de aspectos. Por otro lado, se muestra otra curva para la misma variable, la cual se obtiene de calcular la PDF de la `variable_2` por medio de la transformación citada y asumiendo que la `variable_1` proviene de una distribución normal. Se nota que esta tiene un mejor ajuste a la exponencial, por lo que es mas cercana al ajuste real, solo posee el problema que se indefine en 1 causando que la densidad de probabilidad crezca indefinidamente. Aún así, su integral converge a 1, para más información en como se obtuvo la fórmula y su comprobación visitar anexo.

### Momentos de los modelos


### Anexos

## Obtención de fórmula de PDF para `variable_2`

Se obtuvo la ecuación empleando

Se comprueba la forma de la PDF al igual que la convergencia de la CDF al mostrar ambas curvas en geogebra, se tiene la memoria de la simulación en un [archivo geogebra](misc/geogebra-export.ggb) el cual se puede abrir en [calculadora geogebra](https://www.geogebra.org/calculator) para utilizar la simulación.
![PDF y CDF Variable_2](img/geogebra-export.png)
