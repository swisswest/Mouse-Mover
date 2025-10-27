import tkinter as tk
from tkinter import messagebox
import threading
import time
import pyautogui

running = False

def move_mouse(delay):
    global running
    while running:
        pyautogui.moveRel(10, 0, duration=0.2)
        pyautogui.moveRel(-10, 0, duration=0.2)
        pyautogui.press('shift')
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
    threading.Thread(target=move_mouse, args=(delay,), daemon=True).start()

def stop():
    global running
    running = False
    label_status.config(text="Status: Gestoppt", fg="red")

# GUI erstellen
root = tk.Tk()
root.title("Maus Beweger")
root.geometry("300x200")

tk.Label(root, text="Pause (Sekunden):").pack(pady=5)
entry_delay = tk.Entry(root)
entry_delay.insert(0, "5")  # Standardwert
entry_delay.pack(pady=5)

tk.Button(root, text="Start", command=start, width=17).pack(pady=5)
tk.Button(root, text="Stop", command=stop, width=17).pack(pady=5)

label_status = tk.Label(root, text="Status: Gestoppt", fg="red")
label_status.pack(pady=10)

root.mainloop()
