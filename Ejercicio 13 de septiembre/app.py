import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

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
    cursor.execute("SELECT id, title, status FROM tasks ORDER BY id ASC")
    tareas = cursor.fetchall()
    conn.close()
    if not tareas:
        lista.insert(tk.END, "⚠️ No hay tareas registradas.")
    else:
        for t in tareas:
            lista.insert(tk.END, f"{t[0]} | {t[1]} | {t[2]}")

def listar_popup():
    """Popup tipo tabla con scrollbar."""
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, status FROM tasks ORDER BY id ASC")
    tareas = cursor.fetchall()
    conn.close()

    popup = tk.Toplevel()
    popup.title("Listado de todas las tareas")
    popup.geometry("650x400")

    if not tareas:
        tk.Label(popup, text="⚠️ No hay tareas registradas").pack(pady=20)
        return

    # Tabla Treeview
    columns = ("id", "title", "status")
    tree = ttk.Treeview(popup, columns=columns, show="headings")
    tree.heading("id", text="ID")
    tree.heading("title", text="Título")
    tree.heading("status", text="Estado")
    tree.column("id", width=60, anchor="center")
    tree.column("title", width=420, anchor="w")
    tree.column("status", width=120, anchor="center")

    # Scrollbar vertical
    yscroll = ttk.Scrollbar(popup, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=yscroll.set)

    # Empaquetar con scroll
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    yscroll.pack(side=tk.RIGHT, fill=tk.Y)

    # Insertar filas
    for t in tareas:
        tree.insert("", tk.END, values=t)

def marcar_completada():
    sel = lista.curselection()
    if not sel:
        messagebox.showwarning("Error", "Selecciona una tarea para marcarla")
        return
    seleccion = lista.get(sel)
    if seleccion.startswith("⚠️"):
        return
    task_id = seleccion.split(" | ")[0]
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status = 'completada' WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    mostrar_tareas()

def borrar_tarea():
    sel = lista.curselection()
    if not sel:
        messagebox.showwarning("Error", "Selecciona una tarea para borrar")
        return
    seleccion = lista.get(sel)
    if seleccion.startswith("⚠️"):
        return
    task_id = seleccion.split(" | ")[0]
    if not messagebox.askyesno("Confirmar", f"¿Eliminar la tarea ID {task_id}?"):
        return
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    mostrar_tareas()

def borrar_todas():
    if not messagebox.askyesno("Confirmar", "¿Seguro que quieres borrar TODAS las tareas?"):
        return
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks")
    conn.commit()
    conn.close()
    mostrar_tareas()

def editar_tarea():
    sel = lista.curselection()
    if not sel:
        messagebox.showwarning("Error", "Selecciona una tarea para editar")
        return
    seleccion = lista.get(sel)
    if seleccion.startswith("⚠️"):
        return
    task_id, titulo_actual, _estado = seleccion.split(" | ", 2)
    nuevo_titulo = simpledialog.askstring("Editar tarea", "Nuevo título:", initialvalue=titulo_actual)
    if nuevo_titulo and nuevo_titulo.strip():
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET title = ? WHERE id = ?", (nuevo_titulo.strip(), task_id))
        conn.commit()
        conn.close()
        mostrar_tareas()

# ---------- Interfaz gráfica ----------
def agregar_desde_input():
    titulo = entrada.get()
    agregar_tarea(titulo)
    entrada.delete(0, tk.END)

if __name__ == "__main__":
    init_db()

    ventana = tk.Tk()
    ventana.title("Gestor de Tareas")
    ventana.geometry("720x560")

    # Entrada y botón agregar
    entrada = tk.Entry(ventana, width=60)
    entrada.pack(pady=10)
    btn_agregar = tk.Button(ventana, text="Agregar tarea", command=agregar_desde_input)
    btn_agregar.pack()

    # Frame para lista + scrollbar
    frame_lista = tk.Frame(ventana)
    frame_lista.pack(pady=10, fill=tk.BOTH, expand=True)

    scrollbar_y = tk.Scrollbar(frame_lista, orient=tk.VERTICAL)
    scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

    lista = tk.Listbox(frame_lista, width=90, height=16, yscrollcommand=scrollbar_y.set)
    lista.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar_y.config(command=lista.yview)

    # Botones de acciones
    frame_botones = tk.Frame(ventana)
    frame_botones.pack(pady=8)

    btn_listar = tk.Button(frame_botones, text="Listar todas las tareas", width=25, command=listar_popup)
    btn_listar.grid(row=0, column=0, padx=5, pady=2)

    btn_completar = tk.Button(frame_botones, text="Marcar como completada", width=25, command=marcar_completada)
    btn_completar.grid(row=0, column=1, padx=5, pady=2)

    btn_editar = tk.Button(frame_botones, text="Editar tarea seleccionada", width=25, command=editar_tarea)
    btn_editar.grid(row=1, column=0, padx=5, pady=2)

    btn_borrar = tk.Button(frame_botones, text="Borrar tarea seleccionada", width=25, command=borrar_tarea)
    btn_borrar.grid(row=1, column=1, padx=5, pady=2)

    btn_borrar_todas = tk.Button(frame_botones, text="Borrar todas las tareas", width=25, command=borrar_todas)
    btn_borrar_todas.grid(row=2, column=0, columnspan=2, pady=6)

    # Cargar lista al inicio
    mostrar_tareas()

    ventana.mainloop()
