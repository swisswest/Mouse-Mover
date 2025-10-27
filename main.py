import tkinter as tk
from tkinter import messagebox
import threading
import time
import pyautogui

running = False

def log_message(message):
    """Fügt eine Nachricht ins Log ein, wenn das Log sichtbar ist."""
    if log_visible:
        log_text.insert(tk.END, message + "\n")
        log_text.see(tk.END)

def move_mouse(delay):
    counter = 0
    global running
    while running:
        counter += 1
        pyautogui.moveRel(10, 0, duration=0.2)
        pyautogui.moveRel(-10, 0, duration=0.2)
        pyautogui.press('shift')
        log_message("Mouse moved and 'shift' pressed." + f" (Count: {counter})")
        time.sleep(delay)

def start():
    global running
    if running:
        return
    try:
        delay = float(entry_delay.get())
        if delay <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Fehler", "Bitte eine gültige Zahl > 0 eingeben.")
        return

    running = True
    label_status.config(text="Status: Aktiv", fg="green")
    log_message("Started mouse movement.")
    threading.Thread(target=move_mouse, args=(delay,), daemon=True).start()

def stop():
    global running
    running = False
    label_status.config(text="Status: Gestoppt", fg="red")
    log_message("Stopped mouse movement.")

def check_window_size(event):
    """Überprüft die Fenstergröße und zeigt/versteckt das Log-Feld."""
    global log_visible
    width = root.winfo_width()
    height = root.winfo_height()

    if width > 1000 and height > 500 and not log_visible:
        log_text.pack(fill='both', expand=True, pady=10)
        log_visible = True
        log_message("Log panel activated due to window size.")

    elif (width <= 1000 or height <= 500) and log_visible:
        log_text.pack_forget()
        log_visible = False

# GUI erstellen
root = tk.Tk()
root.title("Maus Beweger")
root.geometry("300x200")

log_visible = False  

tk.Label(root, text="Pause (Sekunden):").pack(pady=5)
entry_delay = tk.Entry(root)
entry_delay.insert(0, "5")  
entry_delay.pack(pady=5)

tk.Button(root, text="Start", command=start, width=17).pack(pady=5)
tk.Button(root, text="Stop", command=stop, width=17).pack(pady=5)

label_status = tk.Label(root, text="Status: Gestoppt", fg="red")
label_status.pack(pady=10)


log_text = tk.Text(root, height=8, state='normal')


root.bind("<Configure>", check_window_size)

root.mainloop()
