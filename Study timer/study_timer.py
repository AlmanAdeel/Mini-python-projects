import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

DATA_FILE = 'study_sessions.json'
POMODORO_DURATION = 25 * 60  # 25 minutes in seconds

def load_sessions():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_sessions(sessions):
    with open(DATA_FILE, 'w') as f:
        json.dump(sessions, f, indent=4)

def start_timer():
    global timer_job, start_time, remaining_seconds
    if timer_job:
        return
    task = task_var.get().strip()
    if not task:
        messagebox.showerror("Input Error", "Please enter a task name.")
        return
    start_time = datetime.now()
    remaining_seconds = POMODORO_DURATION
    update_timer_label()
    timer_job = root.after(1000, countdown)
    start_button.config(state='disabled')
    stop_button.config(state='normal')

def stop_timer():
    global timer_job
    if timer_job:
        root.after_cancel(timer_job)
        log_session()
        reset_timer()

def countdown():
    global remaining_seconds, timer_job
    remaining_seconds -= 1
    update_timer_label()
    if remaining_seconds <= 0:
        log_session(auto=True)
        reset_timer()
    else:
        timer_job = root.after(1000, countdown)

def update_timer_label():
    mins, secs = divmod(remaining_seconds, 60)
    timer_label.config(text=f"{mins:02d}:{secs:02d}")

def log_session(auto=False):
    end_time = datetime.now()
    duration = (end_time - start_time).seconds
    session = {
        'task': task_var.get().strip(),
        'start': start_time.strftime("%Y-%m-%d %H:%M:%S"),
        'end': end_time.strftime("%Y-%m-%d %H:%M:%S"),
        'duration_seconds': duration,
        'auto_completed': auto
    }
    sessions.append(session)
    save_sessions(sessions)
    msg = "Session auto-completed!" if auto else "Session stopped."
    messagebox.showinfo("Session Logged", f"{msg}\nTask: {session['task']}\nDuration: {duration//60} min")

def reset_timer():
    global timer_job
    timer_job = None
    timer_label.config(text="25:00")
    start_button.config(state='normal')
    stop_button.config(state='disabled')

def view_stats():
    total_seconds = sum(s['duration_seconds'] for s in sessions)
    total_minutes = total_seconds // 60
    hours = total_minutes // 60
    minutes = total_minutes % 60
    count = len(sessions)
    messagebox.showinfo("Productivity Stats",
                        f"Sessions: {count}\nTotal Time: {hours}h {minutes}m")

# Load existing sessions
sessions = load_sessions()
timer_job = None
start_time = None
remaining_seconds = POMODORO_DURATION

# GUI setup
root = tk.Tk()
root.title("Study Timer (Pomodoro)")
root.geometry("300x200")
root.resizable(False, False)

task_var = tk.StringVar()

frame = ttk.Frame(root, padding=10)
frame.pack(expand=True, fill='both')

ttk.Label(frame, text="Task Name:").grid(row=0, column=0, sticky='e')
ttk.Entry(frame, textvariable=task_var).grid(row=0, column=1, pady=5)

timer_label = ttk.Label(frame, text="25:00", font=("Arial", 24))
timer_label.grid(row=1, column=0, columnspan=2, pady=10)

start_button = ttk.Button(frame, text="Start", command=start_timer)
start_button.grid(row=2, column=0, padx=5, pady=5)

stop_button = ttk.Button(frame, text="Stop", command=stop_timer, state='disabled')
stop_button.grid(row=2, column=1, padx=5, pady=5)

stats_button = ttk.Button(frame, text="View Stats", command=view_stats)
stats_button.grid(row=3, column=0, columnspan=2, pady=10)

root.mainloop()

