# Proyecto de programación de IE0405 - Modelos Probabilísticos de Señales y Sistemas

Esta es la documentación del proyecto de programación del grupo 01 del curso Modelos Probabilísticos de Señales y Sistemas (Semestre 2 del 2024 UCR), integrado por:

- Diego Alfaro Segura C20259
- Bryan Cortés Espinola C22422
- Edgar Alvarado Taleno C10351

En adelante se muestran instrucciones para generar la documentación completa y ejecutar el código del proyecto.

## Documentación e instrucciones del proyecto

Se recomienda generar la documentación con mkdocs para obtener el informe de los resultados del proyecto. En este se muestra un análisis de los resultados obtenidos durante el mismo. Si ya tiene mkdocs instalado, ejecute desde el directorio principal el siguiente comando de bash:

```bash
mkdocs serve
```

Si no posee este paquete, refierase a las siguientes instrucciones para asegurar una configuración correcta de los archivos de código y documentación.

## Instrucciones para ejecución local

Algunos de los paquetes y funcionalidades del proyecto solamente operan en los sistemas operativos tipo Unix, como Linux y macOS.

Por esta razón, las personas con Windows deben utilizar WSL (*Windows Subsystem for Linux*).

Las [instrucciones de instalación](https://learn.microsoft.com/es-mx/windows/wsl/install) indican que solamente es necesario la siguiente instrucción en la terminal, que instala Ubuntu por defecto:

```bash
wsl --install
```

Una vez en la terminal (o consola o interfaz de línea de comandos) en Linux en WSL, es necesario tener un usuario con privilegios `sudo`. Es posible configurarlo con:

```bash
adduser <username>
```

donde `<username>` puede ser, por ejemplo, `bayes` o `laplace` o `markov` o un nombre de su preferencia, y luego

```bash
usermod -aG sudo <username>
```

para actualizar los permisos. Para cambiar de usuario `root` a `<username>` y empezar una nueva sesión de terminal con ese usuario, utilizar

```bash
su <username>
```

También es recomendado utilizar la [Terminal Windows](https://learn.microsoft.com/es-es/windows/terminal/install), que ofrece mejores herramientas para manejar múltiples terminales, tanto en Windows como en el WSL. 

Nótese que WSL no es ni una máquina virtual ni una configuración de arranque dual (*dual boot*), sino que opera nativamente en Windows. Además, los archivos de Windows están disponibles desde Linux y viceversa.

Una vez instalado WSL, las instrucciones a partir de ahora aplican para una terminal Unix con `bash` o `zsh`, indicado con el símbolo *prompt* `$`.

### Clonar el repositorio

Para comenzar, es necesario "clonar" el repositorio con sus archivos localmente. Para esto:

- Asegurarse de que Git está instalado. Es posible probar con `$ git --version`.
- Ubicarse en el directorio donde estará ubicado el proyecto, con `$ cd`.
- Clonar el proyecto con `$ git clone https://github.com/mpss-eie/proyecto-2024-2-101.git`.
- Moverse al directorio del proyecto con `$ cd proyecto/`.
- Si no fue hecho antes, configurar las credenciales de Git en el sistema local, con `$ git config --global user.name "Nombre Apellido"` y `$ git config --global user.email "your-email@example.com"`, de modo que quede vinculado con la cuenta de GitHub.

### Crear un ambiente virtual de Python

En una terminal, en el directorio raíz del repositorio, utilizar:

```bash
python3 -m venv env
```

donde `env` es el nombre del ambiente. Esto crea una carpeta con ese nombre.

Para activar el ambiente virtual, utilizar:

```bash
source env/bin/activate
```

donde `env/bin/activate` es el `PATH`. El *prompt* de la terminal cambiará para algo similar a:

```bash
base env ~/.../pipeline $
```

En este ambiente virtual no hay paquetes de Python instalados. Es posible verificar esto con `pip list`, que devolverá algo como:

```bash
Package    Version
---------- -------
pip        24.0
setuptools 65.5.0
```

### Instalar los paquetes necesarios para ejecutar el proyecto

Con el ambiente virtual activado, instalar los paquetes indicados en el archivo `requirements.txt`, con:

```bash
pip install -r requirements.txt
```

Para verificar la instalación, es posible usar nuevamente `pip list`, que ahora mostrará una buena cantidad de nuevos paquetes y sus dependencias.

### Para visualizar la documentación

En una terminal, en el directorio raíz del repositorio, utilizar:

```bash
mkdocs serve
```

Abrir en un navegador web la página del "servidor local" en el puerto 8000, en [http://127.0.0.1:8000/](http://127.0.0.1:8000/) o en [http://localhost:8000/](http://localhost:8000/).

Para salir de la visualización, utilizar `Ctrl + C`, de otro modo dejar el proceso corriendo mientras edita la documentación.

### Para ejecutar el proyecto

Para correr el código y así generar los resultados obtenidos, desde el directorio principal del repo debe ejecutar [`src/main.py`](/src/main.py) e ingresar según el menú mostrado cual sección quiere ejecutar (ya sea la sección del avance de proyecto, la de la parte final o ambas). Existen algunas funcionalidades que se consideraron muy extensas para incluir en este main, como lo fue la obtención de mejor distribución en la sección final del proyecto, para ejecutar dicha función se debe ejecutar el archivo [`src/finalPDF.py`](/src/finalPDF.py) directamente.