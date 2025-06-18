import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import os
from datetime import datetime

API_KEY = 'YOUR_OPENWEATHERMAP_API_KEY'  # Replace with your API key
DATA_FILE = 'weather_journal.json'

def load_logs():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_logs(logs):
    with open(DATA_FILE, 'w') as f:
        json.dump(logs, f, indent=4)

def fetch_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather"
    params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return {
        'city': data['name'],
        'temp': data['main']['temp'],
        'description': data['weather'][0]['description']
    }

def add_log():
    city = city_var.get().strip()
    if not city:
        messagebox.showerror("Input Error", "Please enter a city name.")
        return
    try:
        weather = fetch_weather(city)
    except Exception as e:
        messagebox.showerror("Error Fetching", str(e))
        return
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = {
        'timestamp': timestamp,
        'city': weather['city'],
        'temp': weather['temp'],
        'description': weather['description']
    }
    logs.append(log_entry)
    save_logs(logs)
    messagebox.showinfo("Weather Logged", f"{weather['city']}: {weather['temp']}°C, {weather['description']}")

def view_logs():
    win = tk.Toplevel(root)
    win.title("Weather Logs")
    cols = ('Timestamp', 'City', 'Temp (°C)', 'Description')
    tree = ttk.Treeview(win, columns=cols, show='headings')
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor='center')
    for entry in logs:
        tree.insert('', tk.END, values=(
            entry['timestamp'],
            entry['city'],
            f"{entry['temp']:.1f}",
            entry['description']
        ))
    tree.pack(expand=True, fill='both')

# Load existing journal logs
logs = load_logs()

# Build GUI
root = tk.Tk()
root.title("Weather Journal App")
root.geometry("350x200")
root.resizable(False, False)

city_var = tk.StringVar()

frame = ttk.Frame(root, padding="10")
frame.pack(expand=True, fill='both')

ttk.Label(frame, text="City Name:").grid(row=0, column=0, sticky='e')
ttk.Entry(frame, textvariable=city_var).grid(row=0, column=1, padx=5)

ttk.Button(frame, text="Fetch & Log Weather", command=add_log).grid(row=1, column=0, columnspan=2, pady=10)
ttk.Button(frame, text="View Logs", command=view_logs).grid(row=2, column=0, columnspan=2, pady=5)

root.mainloop()
