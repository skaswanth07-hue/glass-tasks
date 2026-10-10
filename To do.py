
import tkinter as tk
from tkinter import messagebox
import json
import os
import uuid
from datetime import date, datetime

# ============================================================
# GLASS TASKS — Single-file Python productivity app
# Built using Python's standard tkinter library
# ============================================================

BG = "#080E1C"
PANEL = "#111B2E"
CARD = "#162239"
CARD_HOVER = "#1D2C46"
BORDER = "#263954"
BLUE = "#69AFFF"
CYAN = "#66F0E4"
WHITE = "#EDF4FF"
MUTED = "#8C9BB4"
GREEN = "#73E6B0"
RED = "#FF8195"
ORANGE = "#FFCC80"

DATA_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "glass_tasks.json"
)

FONT = "Segoe UI"


def load_tasks():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (OSError, json.JSONDecodeError):
        return []


def save_tasks():
    try:
        temp_file = DATA_FILE + ".tmp"
        with open(temp_file, "w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=2, ensure_ascii=False)
        os.replace(temp_file, DATA_FILE)
        status_var.set("All changes saved")
    except OSError as error:
        status_var.set("Save failed")
        messagebox.showerror("Save error", str(error))


tasks = load_tasks()
filter_mode = "All"


def rounded_card(parent, color=CARD, border=BORDER):
    frame = tk.Frame(
        parent,
        bg=color,
        highlightbackground=border,
        highlightthickness=1,
        bd=0
    )
    return frame


def make_label(parent, text, size=10, color=WHITE,
               bold=False, **kwargs):
    return tk.Label(
        parent,
        text=text,
        bg=kwargs.pop("bg", parent.cget("bg")),
        fg=color,
        font=(FONT, size, "bold" if bold else "normal"),
        **kwargs
    )


def make_button(parent, text, command, bg=CARD,
                fg=WHITE, active=None, **kwargs):
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=bg,
        fg=fg,
        activebackground=active or CARD_HOVER,
        activeforeground=WHITE,
        relief="flat",
        bd=0,
        cursor="hand2",
        font=(FONT, 10, "bold"),
        padx=12,
        pady=8,
        **kwargs
    )


def parse_due(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def task_status(task):
    due = parse_due(task.get("due", ""))
    if task.get("done"):
        return "Completed"
    if due and due < date.today():
        return "Overdue"
    if due == date.today():
        return "Due today"
    return "Upcoming"


# ---------------- WINDOW ----------------

root = tk.Tk()
root.title("Glass Tasks | Focus Studio")
root.geometry("1060x760")
root.minsize(800, 620)
root.configure(bg=BG)

try:
    root.tk.call("tk", "scaling", 1.15)
except tk.TclError:
    pass

status_var = tk.StringVar(value="Your workspace is ready")
search_var = tk.StringVar()
title_var = tk.StringVar()
due_var = tk.StringVar()
priority_var = tk.StringVar(value="Medium")
category_var = tk.StringVar(value="Personal")
filter_var = tk.StringVar(value="All")

# ---------------- HEADER ----------------

header = tk.Frame(root, bg=BG)
header.pack(fill="x", padx=28, pady=(24, 16))

brand = tk.Frame(header, bg=BG)
brand.pack(side="left")

logo = tk.Label(
    brand, text="✦", bg="#163454", fg=CYAN,
    font=(FONT, 23, "bold"), padx=12, pady=5
)
logo.pack(side="left", padx=(0, 13))

heading = tk.Frame(brand, bg=BG)
heading.pack(side="left")

make_label(heading, "GLASS TASKS", 21, WHITE, True).pack(anchor="w")
make_label(
    heading, "A quieter space for a clearer mind.", 10, MUTED
).pack(anchor="w", pady=(2, 0))

make_button(
    header, "＋  New task", lambda: title_entry.focus_set(),
    bg="#24599B", fg=WHITE, active="#3075C4"
).pack(side="right", pady=8)

# ---------------- DASHBOARD STATS ----------------

stats_frame = tk.Frame(root, bg=BG)
stats_frame.pack(fill="x", padx=28, pady=(0, 18))

stat_values = {}

def create_stat(parent, key, title, accent):
    card = rounded_card(parent, PANEL)
    card.pack(side="left", fill="both", expand=True, padx=(0, 10))
    make_label(card, title.upper(), 9, MUTED, True).pack(
        anchor="w", padx=16, pady=(14, 4)
    )
    value = make_label(card, "0", 24, accent, True)
    value.pack(anchor="w", padx=16, pady=(0, 13))
    stat_values[key] = value


create_stat(stats_frame, "total", "Total tasks", BLUE)
create_stat(stats_frame, "pending", "In progress", ORANGE)
create_stat(stats_frame, "completed", "Completed", GREEN)
create_stat(stats_frame, "overdue", "Overdue", RED)

# ---------------- MAIN CONTENT ----------------

main = tk.Frame(root, bg=BG)
main.pack(fill="both", expand=True, padx=28, pady=(0, 12))

sidebar = rounded_card(main, PANEL)
sidebar.pack(side="left", fill="y", padx=(0, 16))
sidebar.configure(width=260)
sidebar.pack_propagate(False)

make_label(sidebar, "CREATE A TASK", 10, CYAN, True).pack(
    anchor="w", padx=17, pady=(19, 15)
)

make_label(sidebar, "Task name", 10, MUTED).pack(
    anchor="w", padx=17
)

title_entry = tk.Entry(
    sidebar, textvariable=title_var, bg="#0B1425",
    fg=WHITE, insertbackground=CYAN,
    relief="flat", font=(FONT, 11), bd=0
)
title_entry.pack(fill="x", padx=17, pady=(7, 14), ipady=10)

make_label(sidebar, "Due date  ·  optional", 10, MUTED).pack(
    anchor="w", padx=17
)

due_entry = tk.Entry(
    sidebar, textvariable=due_var, bg="#0B1425",
    fg=WHITE, insertbackground=CYAN,
    relief="flat", font=(FONT, 10), bd=0
)
due_entry.pack(fill="x", padx=17, pady=(7, 5), ipady=9)
due_var.set(date.today().isoformat())

make_label(
    sidebar, "Format: YYYY-MM-DD", 8, MUTED
).pack(anchor="w", padx=17, pady=(0, 13))

make_label(sidebar, "Priority", 10, MUTED).pack(
    anchor="w", padx=17
)

priority_menu = tk.OptionMenu(
    sidebar, priority_var, "Low", "Medium", "High"
)
priority_menu.configure(
    bg="#0B1425", fg=WHITE, activebackground=CARD_HOVER,
    activeforeground=WHITE, relief="flat", bd=0,
    highlightthickness=0, font=(FONT, 10), anchor="w"
)
priority_menu["menu"].configure(
    bg=CARD, fg=WHITE, activebackground="#24599B",
    activeforeground=WHITE
)
priority_menu.pack(fill="x", padx=17, pady=(7, 13), ipady=3)

make_label(sidebar, "Category", 10, MUTED).pack(
    anchor="w", padx=17
)

category_menu = tk.OptionMenu(
    sidebar, category_var,
    "Personal", "College", "Work", "Projects", "Other"
)
category_menu.configure(
    bg="#0B1425", fg=WHITE, activebackground=CARD_HOVER,
    activeforeground=WHITE, relief="flat", bd=0,
    highlightthickness=0, font=(FONT, 10), anchor="w"
)
category_menu["menu"].configure(
    bg=CARD, fg=WHITE, activebackground="#24599B",
    activeforeground=WHITE
)
category_menu.pack(fill="x", padx=17, pady=(7, 17), ipady=3)

# Functions are defined before buttons invoke them.

def add_task(event=None):
    name = title_var.get().strip()
    due = due_var.get().strip()

    if not name:
        messagebox.showinfo("Task name needed", "Enter a task name first.")
        title_entry.focus_set()
        return "break"

    if due and not parse_due(due):
        messagebox.showwarning(
            "Invalid date",
            "Use YYYY-MM-DD, for example 2026-10-15."
        )
        due_entry.focus_set()
        return "break"

    tasks.insert(0, {
        "id": uuid.uuid4().hex,
        "title": name,
        "due": due,
        "priority": priority_var.get(),
        "category": category_var.get(),
        "done": False,
        "created": datetime.now().isoformat(timespec="seconds")
    })

    title_var.set("")
    due_var.set(date.today().isoformat())
    priority_var.set("Medium")
    category_var.set("Personal")

    save_tasks()
    render_tasks()
    title_entry.focus_set()
    return "break"


add_btn = make_button(
    sidebar, "＋  Add task", add_task,
    bg="#24599B", fg=WHITE, active="#3075C4"
)
add_btn.pack(fill="x", padx=17, pady=(0, 18))

make_label(sidebar, "QUICK TIP", 9, CYAN, True).pack(
    anchor="w", padx=17, pady=(4, 7)
)
make_label(
    sidebar,
    "Keep tasks small. Set a deadline.\nFinish one thing at a time.",
    9, MUTED, justify="left", wraplength=215
).pack(anchor="w", padx=17)

title_entry.bind("<Return>", add_task)
due_entry.bind("<Return>", add_task)

# ---------------- TASK LIST ----------------

right = tk.Frame(main, bg=BG)
right.pack(side="left", fill="both", expand=True)

toolbar = tk.Frame(right, bg=BG)
toolbar.pack(fill="x", pady=(0, 12))

make_label(toolbar, "Your tasks", 18, WHITE, True).pack(side="left")

search_entry = tk.Entry(
    toolbar, textvariable=search_var, bg=PANEL, fg=WHITE,
    insertbackground=CYAN, relief="flat",
    font=(FONT, 10), width=19
)
search_entry.pack(side="right", ipady=9, padx=(8, 0))
search_entry.insert(0, "")

make_label(toolbar, "⌕", 17, CYAN).pack(side="right")

filter_row = tk.Frame(right, bg=BG)
filter_row.pack(fill="x", pady=(0, 12))

task_canvas = tk.Canvas(
    right, bg=BG, highlightthickness=0, bd=0
)
scrollbar = tk.Scrollbar(
    right, orient="vertical", command=task_canvas.yview,
    bg=PANEL, troughcolor=BG, activebackground=BLUE,
    relief="flat", bd=0
)
task_canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
task_canvas.pack(side="left", fill="both", expand=True)

task_container = tk.Frame(task_canvas, bg=BG)
canvas_window = task_canvas.create_window(
    (0, 0), window=task_container, anchor="nw"
)

def update_scroll_region(event=None):
    task_canvas.configure(scrollregion=task_canvas.bbox("all"))

def resize_task_container(event):
    task_canvas.itemconfigure(canvas_window, width=event.width)

task_container.bind("<Configure>", update_scroll_region)
task_canvas.bind("<Configure>", resize_task_container)

def on_mousewheel(event):
    if os.name == "nt":
        task_canvas.yview_scroll(int(-event.delta / 120), "units")
    else:
        task_canvas.yview_scroll(
            -1 if event.delta > 0 else 1, "units"
        )

task_canvas.bind("<MouseWheel>", on_mousewheel)

# ---------------- TASK ACTIONS ----------------

def toggle_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = not task.get("done", False)
            break
    save_tasks()
    render_tasks()


def delete_task(task_id):
    if not messagebox.askyesno(
        "Delete task", "Remove this task permanently?"
    ):
        return
    tasks[:] = [t for t in tasks if t["id"] != task_id]
    save_tasks()
    render_tasks()


def edit_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return

    dialog = tk.Toplevel(root)
    dialog.title("Edit task")
    dialog.configure(bg=PANEL)
    dialog.geometry("370x340")
    dialog.resizable(False, False)
    dialog.transient(root)
    dialog.grab_set()

    make_label(dialog, "EDIT TASK", 15, CYAN, True).pack(
        anchor="w", padx=22, pady=(22, 15)
    )

    name = tk.StringVar(value=task["title"])
    due = tk.StringVar(value=task.get("due", ""))
    priority = tk.StringVar(value=task.get("priority", "Medium"))
    category = tk.StringVar(value=task.get("category", "Personal"))

    def field(label, variable):
        make_label(dialog, label, 9, MUTED).pack(
            anchor="w", padx=22, pady=(5, 3)
        )
        entry = tk.Entry(
            dialog, textvariable=variable, bg="#0B1425",
            fg=WHITE, insertbackground=CYAN,
            relief="flat", font=(FONT, 10)
        )
        entry.pack(fill="x", padx=22, ipady=7)
        return entry

    field("Task name", name)
    field("Due date (YYYY-MM-DD or blank)", due)

    def save_edit():
        if not name.get().strip():
            messagebox.showwarning("Missing name", "Enter a task name.")
            return
        if due.get().strip() and not parse_due(due.get().strip()):
            messagebox.showwarning(
                "Invalid date", "Use YYYY-MM-DD or leave it blank."
            )
            return

        task["title"] = name.get().strip()
        task["due"] = due.get().strip()
        task["priority"] = priority.get()
        task["category"] = category.get()
        save_tasks()
        dialog.destroy()
        render_tasks()

    make_button(
        dialog, "Save changes", save_edit,
        bg="#24599B", active="#3075C4"
    ).pack(fill="x", padx=22, pady=20)


def clear_completed():
    completed = sum(1 for t in tasks if t.get("done"))
    if not completed:
        status_var.set("No completed tasks to clear")
        return
    if messagebox.askyesno(
        "Clear completed", f"Delete {completed} completed task(s)?"
    ):
        tasks[:] = [t for t in tasks if not t.get("done")]
        save_tasks()
        render_tasks()


def set_filter(value):
    global filter_mode
    filter_mode = value
    render_tasks()


for label in ("All", "Pending", "Today", "Completed"):
    make_button(
        filter_row, label,
        lambda v=label: set_filter(v),
        bg=PANEL if filter_mode != label else "#24599B",
        fg=WHITE
    ).pack(side="left", padx=(0, 5))


# ---------------- DASHBOARD & RENDERING ----------------

def render_tasks():
    for widget in task_container.winfo_children():
        widget.destroy()

    today = date.today()
    total = len(tasks)
    completed = sum(1 for t in tasks if t.get("done"))
    pending = total - completed
    overdue = sum(
        1 for t in tasks
        if not t.get("done")
        and parse_due(t.get("due", ""))
        and parse_due(t.get("due", "")) < today
    )

    stat_values["total"].configure(text=str(total))
    stat_values["pending"].configure(text=str(pending))
    stat_values["completed"].configure(text=str(completed))
    stat_values["overdue"].configure(text=str(overdue))

    query = search_var.get().strip().lower()
    visible = []

    for task in tasks:
        due = parse_due(task.get("due", ""))
        done = task.get("done", False)

        if query and query not in " ".join([
            task.get("title", ""),
            task.get("category", ""),
            task.get("priority", "")
        ]).lower():
            continue

        if filter_mode == "Pending" and done:
            continue
        if filter_mode == "Completed" and not done:
            continue
        if filter_mode == "Today" and (due != today or done):
            continue

        visible.append(task)

    if not visible:
        empty = rounded_card(task_container, PANEL)
        empty.pack(fill="x", pady=12)
        make_label(
            empty, "✦", 25, CYAN, True
        ).pack(pady=(28, 5))
        make_label(
            empty,
            "Your space is clear." if not tasks else "No matching tasks.",
            14, WHITE, True
        ).pack(pady=3)
        make_label(
            empty,
            "Add a task or try another filter.",
            10, MUTED
        ).pack(pady=(3, 28))
        return

    priority_colors = {
        "High": RED, "Medium": ORANGE, "Low": GREEN
    }

    for task in visible:
        tid = task["id"]
        done = task.get("done", False)
        priority = task.get("priority", "Medium")
        category = task.get("category", "Personal")
        due = task.get("due", "")
        status = task_status(task)

        card = rounded_card(task_container, PANEL)
        card.pack(fill="x", pady=(0, 9))

        row = tk.Frame(card, bg=PANEL)
        row.pack(fill="x", padx=13, pady=13)

        check = tk.Button(
            row, text="✓" if done else "○",
            command=lambda i=tid: toggle_task(i),
            bg="#163B3B" if done else CARD,
            fg=GREEN if done else BLUE,
            activebackground=CARD_HOVER,
            activeforeground=CYAN,
            relief="flat", bd=0, cursor="hand2",
            font=(FONT, 15, "bold"), width=2
        )
        check.pack(side="left", padx=(0, 11))

        body = tk.Frame(row, bg=PANEL)
        body.pack(side="left", fill="x", expand=True)

        title_color = MUTED if done else WHITE
        title_text = task.get("title", "Untitled task")
        if done:
            title_text = "✓  " + title_text

        make_label(
            body, title_text, 11, title_color, True,
            anchor="w", justify="left", wraplength=430
        ).pack(fill="x", anchor="w")

        info = f"{category}   ·   {priority} priority"
        if due:
            info += f"   ·   {due}"

        make_label(body, info, 9, MUTED, anchor="w").pack(
            anchor="w", pady=(5, 0)
        )

        color = (
            GREEN if status == "Completed"
            else RED if status == "Overdue"
            else ORANGE if status == "Due today"
            else priority_colors.get(priority, BLUE)
        )

        badge = tk.Label(
            row, text=status, bg=CARD, fg=color,
            font=(FONT, 8, "bold"), padx=8, pady=5
        )
        badge.pack(side="left", padx=(6, 7))

        actions = tk.Frame(row, bg=PANEL)
        actions.pack(side="right")

        make_button(
            actions, "Edit", lambda i=tid: edit_task(i),
            bg=PANEL, fg=BLUE, padx=6, pady=5
        ).pack(side="left")

        make_button(
            actions, "×", lambda i=tid: delete_task(i),
            bg=PANEL, fg=RED, padx=6, pady=5
        ).pack(side="left")

    task_canvas.yview_moveto(0)


search_var.trace_add("write", lambda *_: render_tasks())

footer = tk.Frame(root, bg=BG)
footer.pack(fill="x", padx=28, pady=(0, 17))

make_label(
    footer, "✦  GLASS TASKS", 9, MUTED, True
).pack(side="left")

make_label(
    footer, "Local storage · Your tasks stay on this PC",
    9, MUTED
).pack(side="left", padx=16)

make_label(
    footer, "Clear completed", 9, RED, True,
    cursor="hand2"
).pack(side="right")

# Bind the clear-completed action to a visible footer control.
for widget in footer.winfo_children():
    if isinstance(widget, tk.Label) and widget.cget("text") == "Clear completed":
        widget.bind("<Button-1>", lambda event: clear_completed())

# Recreate filters with accurate active-state colors.
def rebuild_filters():
    for widget in filter_row.winfo_children():
        widget.destroy()
    for label in ("All", "Pending", "Today", "Completed"):
        make_button(
            filter_row, label,
            lambda v=label: choose_filter(v),
            bg="#24599B" if filter_mode == label else PANEL,
            fg=WHITE
        ).pack(side="left", padx=(0, 5))

def choose_filter(value):
    global filter_mode
    filter_mode = value
    rebuild_filters()
    render_tasks()

rebuild_filters()
render_tasks()
root.mainloop()
