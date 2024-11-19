import sys
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from datetime import datetime
import csv

# Definir los permisos necesarios
SCOPES = [
    'https://www.googleapis.com/auth/classroom.courses',
    'https://www.googleapis.com/auth/classroom.courses.readonly',
    'https://www.googleapis.com/auth/classroom.coursework.students',
    'https://www.googleapis.com/auth/classroom.coursework.me',
    'https://www.googleapis.com/auth/classroom.courseworkmaterials'
]

def authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
 
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
           
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
           
        with open('token.json', 'w') as token_file:
            token_file.write(creds.to_json())
    return creds

# Autenticar y construir el servicio de Google Classroom
creds = authenticate()
service = build('classroom', 'v1', credentials=creds)

def list_courses():
    """Devuelve una lista completa de cursos disponibles en Google Classroom."""
    try:
        courses = []
        next_page_token = None

        while True:
            # Llamada a la API con paginación
            response = service.courses().list(pageSize=100, pageToken=next_page_token).execute()
            courses.extend(response.get('courses', []))
            next_page_token = response.get('nextPageToken')

            if not next_page_token:
                break  # Salir del bucle si no hay más páginas

        return courses
    except Exception as e:
        print("Error al obtener la lista de cursos:", e)
        return []


def list_course_tasks(course_id, course_name):
    """Muestra todas las tareas en un curso específico, indicando su estado, tipo, descripción y fecha de programación si está en borrador."""
    try:
        # Llamar a la API con el parámetro 'courseWorkStates' para obtener publicadas y borradores
        response = service.courses().courseWork().list(
            courseId=course_id,
            courseWorkStates=['PUBLISHED', 'DRAFT']  # Obtener tanto publicadas como borradores
        ).execute()
        tasks = response.get('courseWork', [])
        
        # Mapear tipos de tarea a nombres personalizados
        work_type_map = {
            'ASSIGNMENT': 'Tarea regular',
            'SHORT_ANSWER_QUESTION': 'Pregunta corta',
            'MULTIPLE_CHOICE_QUESTION': 'Opción múltiple'
        }
        
        print(f"\nMostrando las tareas de '{course_name}':")
        if not tasks:
            print("No se encontraron tareas en este curso.")
        else:
            for task in tasks:
                # Obtener el estado y tipo de la tarea
                status = '(P)' if task.get('state') == 'PUBLISHED' else '(B)'
                work_type = work_type_map.get(task.get('workType', 'Desconocido'))
                title = task.get('title')
                description = task.get('description', 'Sin descripción')
                
                # Formatear la fecha de programación si la tarea es un borrador
                scheduled_time = task.get('scheduledTime')
                if status == '(B)' and scheduled_time:
                    # Convertir la fecha de ISO a "dd-mm-aaaa a las hh:mm"
                    scheduled_dt = datetime.strptime(scheduled_time, "%Y-%m-%dT%H:%M:%SZ")
                    formatted_scheduled_time = scheduled_dt.strftime("%d-%m-%Y a las %H:%M")
                    scheduled_display = f" - Programado para: {formatted_scheduled_time}"
                else:
                    scheduled_display = ""
                
                # Mostrar el estado, tipo, título, descripción y, si es borrador, la fecha de programación
                print(f"{status} {work_type} - {title}{scheduled_display}\n{description}\n\n")
    except Exception as e:
        print(f"Error al obtener las tareas del curso '{course_name}': {e}")


def read_tasks_from_txt(file_path):
    """Lee tareas desde un archivo de texto y devuelve una lista de tareas."""
    tasks = []
    with open(file_path, 'r') as file:
        task_details = {}
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line == "---":
                if task_details:
                    tasks.append(task_details)
                    task_details = {}
            else:
                key, value = line.split(": ", 1)
                task_details[key.strip()] = value.strip()
        if task_details:
            tasks.append(task_details)
    return tasks

def create_course_work(task_details):
    """Crea una tarea en Google Classroom basada en los detalles proporcionados."""
    from datetime import datetime
    import locale
    
    # Establecer la localización para nombres de meses (ajústala según tu sistema)
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')  # Español (España). Usa 'es_MX.UTF-8' para México.

    course_id = task_details.get('course_id')
    work_type = task_details.get('workType', 'ASSIGNMENT')
    
    # Configurar el estado de la tarea como 'DRAFT' si tiene una fecha de programación
    state = 'DRAFT' if task_details.get('scheduledTime') else 'PUBLISHED'
    
    # Leer y mostrar scheduledTime para depuración
    scheduled_time = task_details.get('scheduledTime')
    title = task_details.get('title', 'SIN TÍTULO')
    description = task_details.get('description', 'SIN DESCRIPCIÓN')
    
    # Formatear fecha programada si existe
    formatted_date = ""
    if scheduled_time:
        try:
            scheduled_dt = datetime.strptime(scheduled_time, "%Y-%m-%dT%H:%M:%SZ")
            formatted_date = scheduled_dt.strftime("El %d de %B de %Y a las %H:%M")
        except ValueError:
            formatted_date = scheduled_time  # Usar fecha sin formato si hay un error
    
    # Configurar el cuerpo de la solicitud
    course_work = {
        'title': title,
        'description': description,
        'workType': work_type,
        'state': state
    }

    # Añadir scheduledTime si existe para programar la tarea
    if scheduled_time:
        course_work['scheduledTime'] = scheduled_time
    
    try:
        # Enviar la solicitud a la API para crear la tarea programada
        task = service.courses().courseWork().create(
            courseId=course_id,
            body=course_work
        ).execute()
        
        # Mensaje en caso de éxito
        print("\n--- TAREA CREADA CON ÉXITO ---")
        print(f"TÍTULO: {title}")
        print(f"DESCRIPCIÓN: {description}")
        print(f"FECHA PROGRAMADA: {formatted_date or 'Sin programación'}")
        print(f"ID DE LA TAREA: {task.get('id')}")
        print("-" * 30 + "\n")
    
    except Exception as e:
        # Mensaje en caso de error
        print("\n*** ERROR AL CREAR LA TAREA ***")
        print(f"TÍTULO: {title}")
        print(f"DESCRIPCIÓN: {description}")
        print(f"FECHA PROGRAMADA: {formatted_date or 'Sin programación'}")
        print(f"ERROR: {e}")
        print("*" * 30 + "\n")



def read_tasks_from_csv(file_path):
    """Lee tareas desde un archivo CSV y devuelve una lista de tareas."""
    tasks = []
    with open(file_path, mode='r', newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file, delimiter=';')
        
        # Imprimir los encabezados del CSV para verificar
        print("Encabezados del CSV:", reader.fieldnames)
        
        for row in reader:
            # Imprimir la fila para verificar su contenido
            print("Fila leída:", row)
            
            # Convertir el formato CSV a lo que el script espera
            task_details = {
                'course_id': row.get('course_id') or row.get('Curso'),  # Asegúrate de que el encabezado coincida
                'title': row.get('title') or row.get('Título'),
                'description': row.get('description') or row.get('Descripción'),
                'scheduledTime': row.get('scheduledTime') or row.get('Fecha de programación'),  # Revisar nombre exacto
                'dueDate': row.get('dueDate') or row.get('Fecha de entrega'),
                'dueTime': row.get('dueTime') or row.get('Hora'),
                'workType': row.get('workType') or row.get('Tipo de trabajo', '').upper()
            }
            
            # Verificar que course_id y scheduledTime estén presentes
            if task_details['course_id']:
                tasks.append(task_details)
            else:
                print(f"Advertencia: 'course_id' no encontrado en esta fila. Fila ignorada.")
    return tasks



# Bloque principal del script
def main():
    # Mostrar información del creador
    print("")
    print("Este programa ha sido creado por Juan Ignacio Checa Franquelo.")
    print("Profesor de Ed. Primaria en el colegio Ntra. Sra. de la Consolación de Granada.")
    print("Contacto: jichef@gmail.com\n")
    
    # Si no se proporcionan argumentos, mostrar los cursos y pedir seleccionar uno
    if len(sys.argv) == 1:
        courses = list_courses()
        if not courses:
            print("No hay cursos disponibles.")
            sys.exit()
        
        print("Estos son los cursos disponibles:")
        for course in courses:
            print(f" - Nombre del curso: {course['name']}, ID: {course['id']}")
        
        course_input = input("\nEscribe el nombre o ID del curso que deseas ver: ").strip()
        
        # Buscar el curso por nombre o ID
        selected_course = None
        for course in courses:
            if course_input == course['id'] or course_input.lower() == course['name'].lower():
                selected_course = course
                break
        
        if selected_course:
            list_course_tasks(selected_course['id'], selected_course['name'])
        else:
            print("No se encontró un curso con ese nombre o ID.")
        sys.exit()
    
    elif len(sys.argv) == 3 and sys.argv[1] == "csv":
        # Leer y procesar archivo CSV
        file_path = sys.argv[2]
        if os.path.isfile(file_path):
            tasks = read_tasks_from_csv(file_path)
            for task_details in tasks:
                create_course_work(task_details)
        else:
            print(f"El archivo '{file_path}' no existe.")
            sys.exit()
    
    elif len(sys.argv) == 2:
        # Leer y procesar archivo de texto
        file_path = sys.argv[1]
        if os.path.isfile(file_path):
            tasks = read_tasks_from_txt(file_path)
            for task_details in tasks:
                create_course_work(task_details)
        else:
            print(f"El archivo '{file_path}' no existe.")
            sys.exit()
    
    else:
        print("Comando no reconocido. Usa 'classroom.py csv <archivo.csv>' o 'classroom.py <archivo.txt>'")
        sys.exit()

if __name__ == "__main__":
    main()
