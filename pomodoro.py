import time
import subprocess
import tkinter as tk
from threading import Thread

def notify(title, message):
    subprocess.run(["notify-send", title, message])

def countdown(seconds):
    while seconds > 0:
        mins, secs = divmod(seconds, 60)
        update_label(f"Time left: {mins:02}:{secs:02}")
        time.sleep(1)
        seconds -= 1

def pomodoro_timer(work_duration=1, short_break=5, long_break=15, cycles=4):
    for cycle in range(1, cycles + 1):
        notify("Pomodoro Started", f"Cycle {cycle}: Focus for {work_duration} minutes")
        countdown(work_duration * 60)
        
        if cycle % cycles == 0:
            notify("Long Break", f"Take a long break for {long_break} minutes")
            countdown(long_break * 60)
        else:
            notify("Short Break", f"Take a short break for {short_break} minutes")
            countdown(short_break * 60)
    
    notify("Pomodoro Completed", "All cycles are done! Great job!")
    update_label("Pomodoro Completed!")

def start_timer():
    Thread(target=pomodoro_timer, daemon=True).start()

def update_label(text):
    label.config(text=text)

def on_press(event):
    tk_root.x = event.x
    tk_root.y = event.y

def on_drag(event):
    x = tk_root.winfo_pointerx() - tk_root.x
    y = tk_root.winfo_pointery() - tk_root.y
    tk_root.geometry(f"150x150+{x}+{y}")

tk_root = tk.Tk()
tk_root.title("Pomodoro Timer")
tk_root.geometry("150x150")
tk_root.configure(bg="black")
tk_root.overrideredirect(True)

tk_root.bind("<Button-1>", on_press)
tk_root.bind("<B1-Motion>", on_drag)

canvas = tk.Canvas(tk_root, width=300, height=150, bg="black", highlightthickness=0)
canvas.pack(fill="both", expand=True)
#canvas.create_oval(10, 10, 290, 140, fill="black", outline="white", width=2)

label = tk.Label(tk_root, text="Click Start to begin", font=("Arial", 12), fg="white", bg="black")
label.place(relx=0.5, rely=0.4, anchor="center")

start_button = tk.Button(tk_root, text="Start Pomodoro", command=start_timer, fg="black", bg="white", relief="flat", bd=0, highlightthickness=0)
start_button.place(relx=0.5, rely=0.7, anchor="center")

tk_root.mainloop()

