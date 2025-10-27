import tkinter as tk
from tkinter import messagebox
import threading
import time
import pyautogui

running = False
log_visible = False  # Log initially hidden

# Standard- and log-window size
STANDARD_SIZE = "300x250"
LOG_SIZE = "1000x600"


def log_message(message):
    """Adds a message to the log if visible."""
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
        log_message(f"Mouse moved and 'shift' pressed. (Iteration: {counter})")
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
        messagebox.showerror("Error", "Please enter a valid number greater than 0.")
        return

    running = True
    label_status.config(text="Status: Active", fg="green")
    log_message("Started mouse movement.")
    threading.Thread(target=move_mouse, args=(delay,), daemon=True).start()


def stop():
    global running
    running = False
    label_status.config(text="Status: Stopped", fg="red")
    log_message("Stopped mouse movement.")


def toggle_log():
    """Show or hide the log panel and resize window."""
    global log_visible
    if log_visible:
        # Hide log
        log_text.pack_forget()
        toggle_button.config(text="Show Log")
        root.geometry(STANDARD_SIZE)
        log_visible = False
    else:
        # Show log
        log_text.pack(fill='both', expand=True, pady=10)
        toggle_button.config(text="Hide Log")
        root.geometry(LOG_SIZE)
        log_visible = True
        log_message("--- Log window opened ---")


# Create GUI
root = tk.Tk()
root.title("Mouse Mover")
root.geometry(STANDARD_SIZE)

tk.Label(root, text="Delay (seconds):").pack(pady=5)
entry_delay = tk.Entry(root)
entry_delay.insert(0, "5")
entry_delay.pack(pady=5)

tk.Button(root, text="Start", command=start, width=17).pack(pady=5)
tk.Button(root, text="Stop", command=stop, width=17).pack(pady=5)

label_status = tk.Label(root, text="Status: Stopped", fg="red")
label_status.pack(pady=10)

# Toggle log button
toggle_button = tk.Button(root, text="Show Log", command=toggle_log, width=17)
toggle_button.pack(pady=5)

# Log field (initially hidden)
log_text = tk.Text(root, height=8)

root.mainloop()
