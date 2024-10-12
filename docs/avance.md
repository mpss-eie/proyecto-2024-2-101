# Avance del Proyecto
A continuacion se va a presentar lo que se realizó para el avance del protecto de Modelos Probabilisticos de señales y sistemas.
## Cambios en el modelo de base de datos y tareas de recoleccion de datos
En los dados de `models.py` y `task.py` se realizan cambios menores para la creacion de base de datos en el archivo `models.py` ya que en los datos que se van a recibir `kalouk.xyz` por medio de la API, son dos variables de tipo float, y el modelo esta hecho para tres variables, de la misma forma se adaptó la tarea de recoleccion de datos en el archivo `task.py` para que esté construidos para dos variables.
## Recoleccion de datos  

Para la recoleccion de datos se estuvo realizando una solicitud a la API para obtener los datos de la pagina web, en un periodo de 15 segundos, en el cual se va a estar recibiendo 100 datos en ese perido, para esto se utilizó el administrador de tareas `Celery Worker` en conjunto con el planificador de tareas `Celery Beat` con el intermediador de `redis` para que se pueda recolectar 12 horas continuas los datos del sitio web, al final, se dejó un poco mas de tiempo recolectando datos,alrededor de 14 horas , por lo cual se recopilaron cerca de 330 000 datos.

## Análisis exploratorio de los datos

###  Gráficas descriptivas de `variable_1` y `variable_2`

Para obtener una presentacion visual de la manera que estan distribuidos los datos se crearon los histogramas de las variables.

#### Variable_1