# coding: utf-8
import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from tkcalendar import DateEntry
import csv
from datetime import datetime

SCOPES = [
    'https://www.googleapis.com/auth/classroom.courses',
    'https://www.googleapis.com/auth/classroom.coursework.students',
    'https://www.googleapis.com/auth/classroom.courseworkmaterials'
]

creds = None
service = None
courses = []

def authenticate():
    global creds, service
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
    service = build('classroom', 'v1', credentials=creds)
    messagebox.showinfo("Autenticado", "Autenticación completada con éxito.")
    show_courses()

def list_courses():
    all_courses = []
    next_page_token = None
    while True:
        response = service.courses().list(pageSize=100, pageToken=next_page_token).execute()
        all_courses.extend(response.get('courses', []))
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
    return all_courses

def show_courses():
    global courses
    courses = list_courses()
    for widget in courses_frame.winfo_children():
        widget.destroy()
    if not courses:
        tk.Label(courses_frame, text="No se encontraron cursos.").pack()
    else:
        for course in courses:
            btn = tk.Button(courses_frame, text=f"📚 {course['name']}", width=60, anchor='w',
                            command=lambda c=course: show_tasks(c['id'], c['name']),
                            bg="white", fg="black", activebackground="#ddd", relief="groove", font=("Segoe UI", 10))
            btn.pack(pady=2)

from tkcalendar import DateEntry

def show_tasks(course_id, course_name):
    global task_window

    def edit_task(task):
        edit_window = tk.Toplevel(task_window)
        edit_window.title("✏️ Editar tarea")
        edit_window.geometry("450x360")
        edit_window.configure(bg="#f9f9f9")

        is_draft = task.get("state") == "DRAFT"

        tk.Label(edit_window, text="Título:", font=("Segoe UI", 10), bg="#f9f9f9").pack(anchor="w", padx=20, pady=(15, 0))
        title_entry = tk.Entry(edit_window, width=50, font=("Segoe UI", 10))
        title_entry.insert(0, task.get("title", ""))
        title_entry.pack(padx=20, pady=5)

        tk.Label(edit_window, text="Descripción:", font=("Segoe UI", 10), bg="#f9f9f9").pack(anchor="w", padx=20, pady=(10, 0))
        desc_text = tk.Text(edit_window, height=5, width=50, font=("Segoe UI", 10))
        desc_text.insert("1.0", task.get("description", ""))
        desc_text.pack(padx=20, pady=5)

        tk.Label(edit_window, text="Fecha programada (YYYY-MM-DD HH:MM):", font=("Segoe UI", 10), bg="#f9f9f9").pack(anchor="w", padx=20, pady=(10, 0))
        scheduled_entry = tk.Entry(edit_window, width=50, font=("Segoe UI", 10))
        if is_draft and task.get("scheduledTime"):
            try:
                dt = datetime.strptime(task["scheduledTime"], "%Y-%m-%dT%H:%M:%SZ")
                scheduled_entry.insert(0, dt.strftime("%Y-%m-%d %H:%M"))
            except:
                scheduled_entry.insert(0, task["scheduledTime"])
        scheduled_entry.config(state="normal" if is_draft else "disabled")
        scheduled_entry.pack(padx=20, pady=5)

        def submit_changes():
            updated = {
                "title": title_entry.get(),
                "description": desc_text.get("1.0", "end").strip()
            }
            if is_draft and scheduled_entry.get().strip():
                try:
                    new_dt = datetime.strptime(scheduled_entry.get().strip(), "%Y-%m-%d %H:%M")
                    updated["scheduledTime"] = new_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
                except ValueError:
                    messagebox.showerror("Error", "Formato de fecha incorrecto.")
                    return
            try:
                service.courses().courseWork().patch(
                    courseId=course_id,
                    id=task["id"],
                    updateMask="title,description,scheduledTime",
                    body=updated
                ).execute()
                messagebox.showinfo("✅ Éxito", "Tarea actualizada correctamente.")
                edit_window.destroy()
                task_window.destroy()
                show_tasks(course_id, course_name)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar la tarea:\n{e}")

        tk.Button(edit_window, text="💾 Guardar cambios", command=submit_changes, bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(edit_window, text="❌ Cancelar", command=edit_window.destroy, bg="#e0e0e0").pack()

    def delete_task(task):
        confirm = messagebox.askyesno("Confirmar borrado", f"¿Deseas borrar la tarea '{task['title']}'?")
        if confirm:
            try:
                service.courses().courseWork().delete(courseId=course_id, id=task["id"]).execute()
                messagebox.showinfo("🗑️ Tarea eliminada", "La tarea fue eliminada con éxito.")
                task_window.destroy()
                show_tasks(course_id, course_name)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar la tarea:\n{e}")

    def open_create_task_window():
        create_window = tk.Toplevel(task_window)
        create_window.title("➕ Crear nueva tarea")
        create_window.geometry("450x400")
        create_window.configure(bg="#f9f9f9")

        tk.Label(create_window, text="Título:", font=("Segoe UI", 10), bg="#f9f9f9").pack(anchor="w", padx=20, pady=(15, 0))
        title_entry = tk.Entry(create_window, width=50, font=("Segoe UI", 10))
        title_entry.pack(padx=20, pady=5)

        tk.Label(create_window, text="Descripción:", font=("Segoe UI", 10), bg="#f9f9f9").pack(anchor="w", padx=20, pady=(10, 0))
        desc_text = tk.Text(create_window, height=5, width=50, font=("Segoe UI", 10))
        desc_text.pack(padx=20, pady=5)

        tk.Label(create_window, text="Fecha programada:", font=("Segoe UI", 10), bg="#f9f9f9").pack(anchor="w", padx=20)
        row = tk.Frame(create_window, bg="#f9f9f9")
        row.pack(padx=20, pady=5, anchor="w")

        date_entry = DateEntry(row, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern="yyyy-mm-dd")
        date_entry.pack(side="left", padx=(0, 10))

        hour_spin = tk.Spinbox(row, from_=0, to=23, width=3, format="%02.0f")
        hour_spin.pack(side="left", padx=(0, 5))
        minute_spin = tk.Spinbox(row, from_=0, to=59, width=3, format="%02.0f")
        minute_spin.pack(side="left")

        def submit_task():
            title = title_entry.get()
            description = desc_text.get("1.0", "end").strip()
            if not title:
                messagebox.showerror("Error", "El título no puede estar vacío.")
                return

            task_body = {
                "title": title,
                "description": description,
                "workType": "ASSIGNMENT"
            }

            if hour_spin.get() and minute_spin.get():
                try:
                    dt_str = f"{date_entry.get_date()} {hour_spin.get()}:{minute_spin.get()}"
                    dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
                    task_body["scheduledTime"] = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
                    task_body["state"] = "DRAFT"
                except ValueError:
                    messagebox.showerror("Error", "Fecha u hora incorrecta.")
                    return
            else:
                task_body["state"] = "PUBLISHED"

            try:
                service.courses().courseWork().create(courseId=course_id, body=task_body).execute()
                messagebox.showinfo("Tarea creada", "La tarea se creó correctamente.")
                create_window.destroy()
                task_window.destroy()
                show_tasks(course_id, course_name)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear la tarea:\n{e}")

        tk.Button(create_window, text="Crear tarea", command=submit_task, bg="#4CAF50", fg="white").pack(pady=15)

    try:
        response = service.courses().courseWork().list(courseId=course_id, courseWorkStates=['PUBLISHED', 'DRAFT']).execute()
        tasks = response.get('courseWork', [])

        task_window = tk.Toplevel(root)
        task_window.title(f"Tareas de: {course_name}")
        task_window.geometry("800x600")
        task_window.configure(bg="#f0f0f0")

        canvas = tk.Canvas(task_window, bg="#f0f0f0", highlightthickness=0)
        scrollbar = tk.Scrollbar(task_window, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="#f0f0f0")
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        top_frame = tk.Frame(scroll_frame, bg="#f0f0f0")
        top_frame.pack(fill="x", padx=10, pady=(10, 5))
        tk.Button(top_frame, text="➕ Crear nueva tarea", command=open_create_task_window, bg="#2196F3", fg="white").pack(anchor="e")

        for task in tasks:
            status = "Publicado" if task.get("state") == "PUBLISHED" else "Borrador"
            title = task.get("title", "Sin título")
            description = task.get("description", "Sin descripción")
            scheduled_fmt = ""
            if task.get("scheduledTime"):
                try:
                    scheduled_dt = datetime.strptime(task["scheduledTime"], "%Y-%m-%dT%H:%M:%SZ")
                    scheduled_fmt = scheduled_dt.strftime("📅 %d/%m/%Y a las %H:%M")
                except ValueError:
                    scheduled_fmt = f"📅 {task['scheduledTime']}"
            card = tk.Frame(scroll_frame, bg="white", bd=1, relief="solid")
            card.pack(fill="x", padx=15, pady=10)
            tk.Label(card, text=title, font=("Segoe UI", 12, "bold"), bg="white", anchor="w").pack(fill="x", padx=10, pady=(10, 0))
            tk.Label(card, text=f"🗂 Estado: {status}", font=("Segoe UI", 10), bg="white", anchor="w", fg="#555").pack(fill="x", padx=10, pady=(0, 2))
            if scheduled_fmt:
                tk.Label(card, text=scheduled_fmt, font=("Segoe UI", 10, "italic"), bg="white", fg="#007acc", anchor="w").pack(fill="x", padx=10)
            tk.Label(card, text=description, font=("Segoe UI", 10), bg="white", anchor="w", wraplength=680, justify="left").pack(fill="x", padx=10, pady=(5, 5))
            btn_frame = tk.Frame(card, bg="white")
            btn_frame.pack(pady=(0, 10), padx=10, anchor="e")
            tk.Button(btn_frame, text="✏️ Editar", command=lambda t=task: edit_task(t), bg="#ffc107", fg="black").pack(side="left", padx=5)
            tk.Button(btn_frame, text="🗑️ Borrar", command=lambda t=task: delete_task(t), bg="#f44336", fg="white").pack(side="left", padx=5)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar las tareas:\n{e}")
def read_tasks_from_file(filepath):
    tasks = []
    if filepath.endswith('.csv'):
        with open(filepath, 'r', newline='', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                tasks.append(row)
    elif filepath.endswith('.txt'):
        with open(filepath, 'r') as file:
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

def create_tasks():
    file_path = filedialog.askopenfilename(title="Selecciona archivo de tareas", filetypes=[("Text and CSV", "*.txt *.csv")])
    if not file_path:
        return
    tasks = read_tasks_from_file(file_path)
    created_window = tk.Toplevel(root)
    created_window.title("Resultado de creación de tareas")
    created_window.geometry("600x400")
    result_output = scrolledtext.ScrolledText(created_window, width=80, height=25)
    result_output.pack(padx=10, pady=10)
    for task in tasks:
        try:
            course_work = {
                'title': task.get('title', 'SIN TÍTULO'),
                'description': task.get('description', 'SIN DESCRIPCIÓN'),
                'workType': task.get('workType', 'ASSIGNMENT'),
                'state': 'DRAFT' if task.get('scheduledTime') else 'PUBLISHED'
            }
            if task.get('scheduledTime'):
                course_work['scheduledTime'] = task['scheduledTime']
            service.courses().courseWork().create(courseId=task['course_id'], body=course_work).execute()
            result_output.insert(tk.END, f"✅ Tarea creada: {task.get('title')}")
        except Exception as e:
            result_output.insert(tk.END, f"❌ Error al crear: {task.get('title')} - {e}")

# Crear ventana principal
root = tk.Tk()
root.configure(bg="#f0f0f0")
root.title("Gestor de tareas Google Classroom")

frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(pady=10)

btn_auth = tk.Button(frame, text="🔐 Autenticar y mostrar cursos", width=30, command=authenticate, bg="#4CAF50", fg="white", activebackground="#45a049", font=("Segoe UI", 10))
btn_auth.pack(pady=5)

btn_create = tk.Button(frame, text="📝 Crear Tareas desde archivo", width=30, command=create_tasks, bg="#2196F3", fg="white", activebackground="#1976D2", font=("Segoe UI", 10))
btn_create.pack(pady=5)

canvas = tk.Canvas(root, height=300, bg="#f0f0f0", highlightthickness=0)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scroll_frame = tk.Frame(canvas, bg="#f0f0f0")
scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True, padx=10)
scrollbar.pack(side="right", fill="y")

courses_frame = scroll_frame

root.mainloop()
