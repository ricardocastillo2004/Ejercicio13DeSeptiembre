import sqlite3

# ---------- Inicializar base de datos ----------
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

# ---------- Agregar tarea ----------
def agregar_tarea(titulo):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title) VALUES (?)", (titulo,))
    conn.commit()
    conn.close()

# ---------- Mostrar tareas (formato bonito) ----------
def mostrar_tareas():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tareas = cursor.fetchall()
    conn.close()
    
    if len(tareas) == 0:
        print("⚠️ No hay tareas registradas.")
    else:
        for tarea in tareas:
            print(f"ID: {tarea[0]} | Título: {tarea[1]} | Estado: {tarea[2]}")

# ---------- Marcar tarea como completada ----------
def marcar_completada(task_id):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status = 'completada' WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

# ---------- Borrar una tarea ----------
def borrar_tarea(task_id):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    print(f"🗑️ La tarea con ID {task_id} fue eliminada.")

# ---------- Borrar todas las tareas ----------
def borrar_todas():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks")  # borra todas las filas
    conn.commit()
    conn.close()
    print("🗑️ Todas las tareas fueron eliminadas.")

# ---------- Ver datos crudos de la BD ----------
def ver_crudo():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    filas = cursor.fetchall()
    conn.close()
    print("\n📂 Contenido crudo de la tabla 'tasks':")
    print(filas)

# ---------- Menú principal ----------
if __name__ == "__main__":
    init_db()
    while True:
        print("\n📋 MENÚ DE TAREAS")
        print("1. Agregar tarea")
        print("2. Mostrar tareas")
        print("3. Marcar como completada")
        print("4. Salir")
        print("5. Borrar una tarea")
        print("6. Borrar todas las tareas")
        print("7. Ver datos crudos de la BD")
        
        opcion = input("Elige una opción: ")
        
        if opcion == "1":
            titulo = input("Título de la tarea: ")
            agregar_tarea(titulo)
            print("✅ Tarea agregada.")
        elif opcion == "2":
            mostrar_tareas()
        elif opcion == "3":
            task_id = input("ID de la tarea a completar: ")
            marcar_completada(task_id)
            print("✅ Tarea completada.")
        elif opcion == "4":
            print("👋 Saliendo del programa.")
            break
        elif opcion == "5":
            task_id = input("ID de la tarea a borrar: ")
            borrar_tarea(task_id)
        elif opcion == "6":
            borrar_todas()
        elif opcion == "7":
            ver_crudo()
        else:
            print("❌ Opción no válida, intenta de nuevo.")
