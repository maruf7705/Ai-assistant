import tkinter as tk
import sqlite3


# Set up the database
def setup_database():
    conn = sqlite3.connect("tasks.db")  # Connect to database
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            status TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


# Function to add a new task
def add_task():
    task = entry_task.get()
    if task:
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (task, status) VALUES (?, ?)", (task, "Pending"))
        conn.commit()
        conn.close()
        entry_task.delete(0, tk.END)
        update_task_list()


# Function to update task list
def update_task_list():
    listbox_tasks.delete(0, tk.END)
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, task, status FROM tasks")
    tasks = cursor.fetchall()
    conn.close()

    for task in tasks:
        listbox_tasks.insert(tk.END, f"{task[0]} - {task[1]} [{task[2]}]")


# Function to mark task as completed
def complete_task():
    selected = listbox_tasks.curselection()
    if selected:
        task_id = listbox_tasks.get(selected).split(" - ")[0]  # Extract task ID
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET status = 'Completed' WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
        update_task_list()


# GUI Setup
root = tk.Tk()
root.title("Task Manager")
root.geometry("400x500")
root.configure(bg="#B2E4E6")

# Entry Field
entry_task = tk.Entry(root, font=("Arial", 14))
entry_task.pack(pady=10)

# Buttons
btn_add = tk.Button(root, text="Add Task", command=add_task, font=("Arial", 12), bg="#6AC7D4", fg="white")
btn_add.pack(pady=5)

btn_complete = tk.Button(root, text="Complete Task", command=complete_task, font=("Arial", 12), bg="#4AA6B3",
                         fg="white")
btn_complete.pack(pady=5)

# Listbox
listbox_tasks = tk.Listbox(root, font=("Arial", 12), width=50, height=15)
listbox_tasks.pack(pady=10)

# Initialize Database and Load Data
setup_database()
update_task_list()

# Run the main loop
root.mainloop()
