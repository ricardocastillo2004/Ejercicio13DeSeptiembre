import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog

# ---------- Base de datos ----------
def init_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            status TEXT DEFAULT 'pendiente'
        )
    """)
    conn.commit()
    conn.close()

def agregar_tarea(titulo):
    if titulo.strip() == "":
        messagebox.showwarning("Error", "La tarea no puede estar vacía")
        return
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title) VALUES (?)", (titulo,))
    conn.commit()
    conn.close()
    mostrar_tareas()

def mostrar_tareas():
    lista.delete(0, tk.END)
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tareas = cursor.fetchall()
    conn.close()
    if len(tareas) == 0:
        lista.insert(tk.END, "⚠️ No hay tareas registradas.")
    else:
        for tarea in tareas:
            lista.insert(tk.END, f"{tarea[0]} | {tarea[1]} | {tarea[2]}")

def marcar_completada():
    try:
        seleccion = lista.get(lista.curselection())
        task_id = seleccion.split(" | ")[0]
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET status = 'completada' WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
        mostrar_tareas()
    except:
        messagebox.showwarning("Error", "Selecciona una tarea para marcarla")

def borrar_tarea():
    try:
        seleccion = lista.get(lista.curselection())
        task_id = seleccion.split(" | ")[0]
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
        mostrar_tareas()
    except:
        messagebox.showwarning("Error", "Selecciona una tarea para borrar")

def borrar_todas():
    respuesta = messagebox.askyesno("Confirmar", "¿Seguro que quieres borrar todas las tareas?")
    if respuesta:
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks")
        conn.commit()
        conn.close()
        mostrar_tareas()

def editar_tarea():
    try:
        seleccion = lista.get(lista.curselection())
        task_id = seleccion.split(" | ")[0]
        titulo_actual = seleccion.split(" | ")[1]
        nuevo_titulo = simpledialog.askstring("Editar tarea", "Nuevo título:", initialvalue=titulo_actual)
        if nuevo_titulo and nuevo_titulo.strip() != "":
            conn = sqlite3.connect("tasks.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE tasks SET title = ? WHERE id = ?", (nuevo_titulo, task_id))
            conn.commit()
            conn.close()
            mostrar_tareas()
    except:
        messagebox.showwarning("Error", "Selecciona una tarea para editar")

# ---------- Interfaz gráfica ----------
def agregar_desde_input():
    titulo = entrada.get()
    agregar_tarea(titulo)
    entrada.delete(0, tk.END)

if __name__ == "__main__":
    init_db()

    ventana = tk.Tk()
    ventana.title("Gestor de Tareas")
    ventana.geometry("520x500")

    # Entrada y botón agregar
    entrada = tk.Entry(ventana, width=40)
    entrada.pack(pady=10)
    btn_agregar = tk.Button(ventana, text="Agregar tarea", command=agregar_desde_input)
    btn_agregar.pack()

    # Lista de tareas
    lista = tk.Listbox(ventana, width=65, height=15)
    lista.pack(pady=10)

    # Botones de acciones
    frame_botones = tk.Frame(ventana)
    frame_botones.pack(pady=5)

    btn_listar = tk.Button(frame_botones, text="Listar todas las tareas", width=25, command=mostrar_tareas)
    btn_listar.grid(row=0, column=0, padx=5, pady=2)

    btn_completar = tk.Button(frame_botones, text="Marcar como completada", width=25, command=marcar_completada)
    btn_completar.grid(row=0, column=1, padx=5, pady=2)

    btn_editar = tk.Button(frame_botones, text="Editar tarea seleccionada", width=25, command=editar_tarea)
    btn_editar.grid(row=1, column=0, padx=5, pady=2)

    btn_borrar = tk.Button(frame_botones, text="Borrar tarea seleccionada", width=25, command=borrar_tarea)
    btn_borrar.grid(row=1, column=1, padx=5, pady=2)

    btn_borrar_todas = tk.Button(frame_botones, text="Borrar todas las tareas", width=25, command=borrar_todas)
    btn_borrar_todas.grid(row=2, column=0, columnspan=2, pady=5)

    # Cargar lista al inicio
    mostrar_tareas()

    ventana.mainloop()
