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

# ---------- Mostrar tareas ----------
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

# ---------- Menú principal ----------
if __name__ == "__main__":
    init_db()
    while True:
        print("\n📋 MENÚ DE TAREAS")
        print("1. Agregar tarea")
        print("2. Mostrar tareas")
        print("3. Marcar como completada")
        print("4. Salir")
        
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
        else:
            print("❌ Opción no válida, intenta de nuevo.")
