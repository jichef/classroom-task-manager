  
# Classroom Task Manager UPDATE
He añadido un entorno visual en la carpeta GUI. Es mucho más sencillo que andar con comandos. En la ventana principal puedes autenticarte, mostrar tus clases y, dentro de cada clase, muestra todas las tareas (programadas o no, publicadas o borradores), permitiendo modificarlas, eliminarlas o simplemente revisarlas; además de crear nuevas o la función estrella por la que fue creado el programa: crear tareas en bloque desde un txt o un excel.

# Classroom Task Manager

Este proyecto es un script en Python para interactuar con la API de Google Classroom. Te permite listar cursos, gestionar tareas y programar publicaciones de forma eficiente. Te pongo un ejemplo:
 

¿Cuántas veces has tenido que crear la misma tarea en dos cursos diferentes? Cuánto tiempo tardas en hacer tantos clics, en copiar, pegar, copiar, pegar, seleccionar fecha y hora de programación... etc.

¿Tienes tareas repetitivas? Por ejemplo: todos los días mandas lecturas de algún libro:

1. Lunes: leer páginas 23 y 24
2. Martes: leer página 25 y 26
3. Miércoles: leer página 27 y 28
4. Jueves: leer página 29 y 30
5. Viernes: leer página 31 y 32.

Si además tienes que hacer lo mismo en otro curso... ya son 10 tareas.

Con este script podrás programar las tareas con vistas a un futuro bastante lejano y olvidarte de tener que sacar 15 minutos de tiempo en realizar todo el trabajo. Hazlo de una sentada. Te vas a ahorrar mucho mucho tiempo. Puedes incluir más de 50 tareas de una sentada (usa tu imaginación).
  
Si te ha gustado... invítame a un café ;)

[![Buy Me a Coffee](https://img.buymeacoffee.com/button-api/?text=Buy%20me%20a%20coffee&emoji=&slug=jichef&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff)](https://www.buymeacoffee.com/jichef)
  

# Instrucciones para Usar el Código de Google Classroom

Este paso tendrás que hacerlo SOLO la primera vez. El código es un script en Python que permite gestionar tareas y cursos en Google Classroom utilizando la API de Google. A continuación, te explico cómo usarlo:

## IMPORTANTE.

Si te descargas el ejecutable `.exe` puedes obviar el paso 2 de los Requisitos previos. Además, en todas las refencias que se hagan a los scripts, con que escribas en la linea de comandos el ejecutable con sus argumentos, será suficiente.

Si decides descargar el `.py` tienes que tener en cuenta que a lo largo de este documento te encontrarás con los ejecutables `pip3` o `python3`. Si te da error en la ejecución, prueba a dejarlo solo como `pip` o `python`

## Requisitos Previos

1. **Autenticación con Google Classroom:**

- **Token:** Para acceder a la API, necesitas un archivo `credentials.json`, que se obtiene al registrar tu aplicación en la [Consola de APIs de Google](https://console.developers.google.com/). Este paso debe realizarlo tu Administrador de cuentas de Worksuite de tu centro. 

_____________ ** _____________

#### 1.1 Crear un Proyecto Nuevo
- Ve a [Google Cloud Console](https://console.cloud.google.com) y crea un proyecto nuevo. Puedes nombrarlo, por ejemplo, **"Classroom"**.

#### 1.2 Buscar APIs y Servicios
- En el menú lateral, selecciona **APIs y Servicios**.
- Haz clic en **Biblioteca**.

#### 1.3 Habilitar la API de Classroom
- En la Biblioteca, busca **Classroom**.
- Selecciona la API de Classroom y haz clic en **Habilitar**.

#### 1.4 Configurar la Pantalla de Consentimiento
- Una vez habilitada la API, regresa al menú de **APIs y Servicios** y selecciona **Pantalla de Consentimiento OAuth** en el menú lateral.
- Completa los datos obligatorios:
  - **Nombre de la organización**
  - **Correo electrónico de asistencia al usuario**
- Si lo deseas, puedes subir un logo para personalizar la pantalla, pero no es obligatorio.

  #### 1.5 Crear Credenciales

- En el menú lateral, selecciona **Credenciales**.
- Haz clic en **Crear Credenciales** y selecciona **ID de cliente de OAuth**.
- En **Tipo de aplicación**, elige **App de escritorio** y asigna un nombre, por ejemplo, **"Classroom Task"**.
 

#### 1.6 Descargar y Renombrar el Archivo JSON
- Una vez creadas las credenciales, se abrirá una ventana con los datos secretos.
- Descarga el archivo JSON.
- Este archivo es muy importante y solo será necesario la primera vez. Renómbralo a **credentials.json**.


- **Scopes:** El script tiene permisos específicos para acceder y administrar cursos y tareas. Estos permisos se definen en `SCOPES`.

_____________ ** _____________

2. **Instala Python**
Entra en la sección de descargas de [Python.org](https://www.python.org/downloads/), descarga la versión de tu sistema operativo e instala.

3. **Instalación de las Librerías Necesarias:**
- Ejecuta un terminal o consola de comandos. Para Windows: `Inicio` / `Ejecutar` / `cmd` y presiona `ENTER` o tecla de `Windows` + `R`, escribe `cmd` y presiona `ENTER`.

- Utiliza `pip3` para instalar las dependencias necesarias. Copia y pega el siguiente código:

```bash
pip3 install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

4. **Credenciales y Tokens:**

- Renombra el archivo descargado de la consola de google a `credentials.json` (si no lo has hecho ya) y colócalo en la misma carpeta del script.
- El script generará un archivo `token.json` cuando se autentique exitosamente por primera vez, el cual se utilizará para futuras autenticaciones. Si lo borras, tendrás que volver a autenticarte (necesitando nuevamente el `credentials.json`)

## Uso del Script

### 1. Ejecutar el Script sin Argumentos

- Cuando se ejecuta sin argumentos, el script muestra la lista de cursos disponibles en Google Classroom.

- Para ejecutarlo:

```bash
python3 classroom.py
```
- Introduce tus credenciales con las que accedes a Classroom (recuerda que este paso solo lo necesitas la primera vez)
- Selecciona un curso escribiendo el nombre o ID del curso para ver sus tareas.

### 2. Crear Tareas desde un Archivo de Texto

- Puedes proporcionar un archivo de texto como argumento. El archivo debe contener la información de las tareas en el siguiente formato:


```text
title: Nombre de la Tarea
description: Descripción de la Tarea
course_id: ID del curso
scheduledTime: 2023-11-19T14:30:00Z
workType: ASSIGNEMENT
---
```

En `workType` puedes utilizar `ASSIGNEMENT` o `SHORT_ANSWER_QUESTION` (tarea sencilla o respuesta corta)

Las `---` son muy importantes, pues son los separadores de las diferentes tareas. 

### 3. Crear Tareas desde un Archivo CSV
- Puedes utilizar un archivo CSV con la información de las tareas. El archivo debe contener los siguientes encabezados:
- `course_id`, `title`, `description`, `scheduledTime`, `dueDate`, `dueTime`, `workType`
- Cada fila del archivo CSV debe representar una tarea.
- A continuación, un ejemplo del archivo CSV:

```csv
course_id;title;description;scheduledTime;dueDate;dueTime;workType
123456;Lectura Capítulo 3;Leer y responder preguntas;2023-11-19T14:30:00Z;2023-11-20;14:00;ASSIGNMENT
123456;Tarea Matemáticas;Resolver problemas de la página 45;;;
```

  
  

- Para ejecutar el script con un archivo CSV:

```bash
python3 classroom.py csv archivo.csv

```

## 4. Detalles del Código

1. **Autenticación (`authenticate`)**:

- Esta función maneja la autenticación y generación de un token para acceder a la API de Google Classroom.
- Si el archivo `token.json` ya existe y es válido, el script lo utilizará automáticamente. Si el token ha expirado, se renovará. Si no hay token, se solicitará autenticación manual.


2. **Listar Cursos (`list_courses`)**:

- Esta función devuelve todos los cursos en los que el usuario tiene acceso.
- Utiliza paginación para obtener más de 100 cursos si es necesario.

3. **Listar Tareas de un Curso (`list_course_tasks`)**:

- Dado un ID de curso, esta función obtiene todas las tareas (publicadas y en borrador).
- Muestra información relevante como el estado, tipo y descripción de cada tarea.

4. **Leer Tareas desde un Archivo de Texto (`read_tasks_from_txt`)**:

- Esta función lee un archivo de texto y convierte cada bloque de información en un diccionario de tareas.

5. **Leer Tareas desde un CSV (`read_tasks_from_csv`)**:

- Lee un archivo CSV y convierte cada fila en un diccionario con la información de la tarea.

6. **Crear Tarea en Classroom (`create_course_work`)**:

- Esta función utiliza la API para crear una tarea en un curso específico, usando la información proporcionada.
- Permite crear tareas con detalles como título, descripción, tipo de tarea y fecha de programación.

## 5. Ejemplo de Uso
Una vez hayamos conseguido nuestro `credentials.json` ejecutamos nuestro código

```bash
python3 classroom.py
```

Nos pedirá iniciar sesión con nuestra cuenta Google. Una vez hayamos tenido éxito en el inicio de sesión mostrará todas las clases que tenemos activas (no archivadas):

```text
Estos son los cursos disponibles:
- Nombre del curso: 1º B LENGUA, ID: 1234564561
- Nombre del curso: 1ºA ENGLISH, ID: 1234564562
- Nombre del curso: 2ºB CONOCIMIENTO DEL MEDIO, ID: 1234564563
- Nombre del curso: 2ºA CONOCIMIENTO DEL MEDIO, ID: 1234564564
- Nombre del curso: 1ºA CONOCIMIENTO DEL MEDIO, ID: 1234564565
```

A continuación nos pedirá que introduzcamos un código de una clase para ver las tareas disponibles. Podemos finalizar el script con `Control + x`

Puedes en este momento dar forma al documento de texto

### Archivo de Texto (`archivo.txt`)

```text
title: Lectura Capítulo 3
description: Leer y responder preguntas del capítulo 3
course_id: 1234564561
scheduledTime: 2024-11-19T14:30:00Z
workType: ASSIGNEMENT
---
title: Tarea las plantas
description: Investigación sobre de diferentes tipos de hojas
course_id: 1234564563
workType: ASSIGNEMENT
---
```

Si te fijas, el `course_id` de ambas tareas es diferente. Creará diferentes tareas en diferentes clases.

Guarda el archivo en txt con codificación UTF-8 en el mismo lugar donde tienes el script para evitar tener que escribir la ruta. Para crear las tareas definidas en este archivo, ejecuta el siguiente comando:

```bash
python3 classroom.py archivo.txt
```

  

### Archivo CSV (`archivo.csv`)

El archivo CSV debe tener la siguiente estructura:
```csv
course_id;title;description;scheduledTime;dueDate;dueTime;workType
123456;Lectura Capítulo 3;Leer y responder preguntas;2023-11-19T14:30:00Z;2023-11-20;14:00;ASSIGNMENT
123456;Tarea Matemáticas;Resolver problemas de la página 45;;;
```

Puede parecer complejo realizar este archivo CSV, pero te adjunto un excel para que sea todo más rápido y sencillo. El libro está compuesto por 3 hojas: `Tareas`, `Exportar CSV` y `Clases y otros`.

1. **Añade tus clases**
En esta pestaña vamos a añadir las clases y su `course_id` correspondiente. Para ello ejecuta el script `python3 classroom.py` y toma nota del nombre de la clase y su `course_id`. Copia esos datos a la hoja Clases y otros.

ATENCIÓN: cuando pegues el `course_id` es posible que debas actualizar el formato de la celda a numérico (botón derecho sobre la celda -> formato de la celda). Puedes moficar también las horas, aunque no te lo recomiendo. Creo que cada 30 minutos es bastante fino.

3. **Añade las tareas**

Pasamos a la hoja "Tareas". Es muy intuitiva:

En la primera columna tienes un desplegable donde se mostrará el nombre de la clase que has definido en la hoja `Clases y otros`. En título y descripción detalla exactamente igual que lo harías en Classroom. En fecha de programación añade algo si quieres programarla (he incluido un selector de calendario para que sea más rápido, ya en el formato que espera Google), déjala en blanco si quieres que sea inmediata. La hora es obligatoria si has indicado fecha de programación. Lo mismo para la fecha de entrega y su correspondiente campo de hora, puedes seguir usando el mismo selector de fecha (igual que antes estos campos no son obligatorios). Por último, en tipo de trabajo puedes elegir si `Tarea regular` o `Pregunta de respuesta corta`.

5. **Exporta las tareas a CSV**

Ahora debes ir a la hoja Exportar CSV y asegurarte que todo es correcto. Ve a `Archivo`/ `Guardar cómo` y elige el formato `CSV codificado en UTF-8 (separado por comas)`. Se genera el archivo CSV. Guardalo en la misma carpeta que el script.

Para crear las tareas definidas en este archivo, ejecuta el siguiente comando:

```bash
python3 classroom.py csv archivo.csv
```

Eso es todo... espero que te resulte de utilidad. ¡Ya me cuentas el tiempo que has ahorrado!
[![Buy Me a Coffee](https://img.buymeacoffee.com/button-api/?text=Buy%20me%20a%20coffee&emoji=&slug=jichef&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff)](https://www.buymeacoffee.com/jichef)
