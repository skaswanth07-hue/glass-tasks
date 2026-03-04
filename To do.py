import tkinter as tk
from tkinter import messagebox

# Main window
root = tk.Tk()
root.title("Simple To-Do List")
root.geometry("400x400")
root.config(bg='lightblue')

# Data structures
tasks = {}   # Dictionary to store task and status

# Functions
def add_task():
    task = entry.get()
    if task != "":
        tasks[task] = "Pending"
        listbox.insert(tk.END, task + " - Pending")
        # color pending tasks (blue)
        idx = listbox.size() - 1
        listbox.itemconfig(idx, fg='blue')
        entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Please enter a task!")

def delete_task():
    selected = listbox.curselection()
    if selected:
        task_text = listbox.get(selected)
        task_name = task_text.split(" - ")[0]
        del tasks[task_name]
        listbox.delete(selected)
    else:
        messagebox.showwarning("Warning", "Select a task to delete!")

def mark_complete():
    selected = listbox.curselection()
    if selected:
        idx = selected[0]
        task_text = listbox.get(idx)
        task_name = task_text.split(" - ")[0]
        tasks[task_name] = "Completed"
        # replace at same index and color completed tasks (gray)
        listbox.delete(idx)
        listbox.insert(idx, task_name + " - Completed")
        listbox.itemconfig(idx, fg='gray')
    else:
        messagebox.showwarning("Warning", "Select a task to mark complete!")

# UI Elements
entry = tk.Entry(root, width=40, bg="white")
entry.pack(pady=10)

add_btn = tk.Button(root, text="Add Task", command=add_task,width=20, bg="lightyellow")
add_btn.pack(pady=5)

delete_btn = tk.Button(root, text="Delete Task", bg="lightcoral", command=delete_task,width=20)
delete_btn.pack(pady=5)

complete_btn = tk.Button(root, text="Mark as Completed", bg="lightgreen", command=mark_complete,width=20)
complete_btn.pack(pady=5)

listbox = tk.Listbox(root, width=45)
listbox.pack(pady=10)

root.mainloop()
