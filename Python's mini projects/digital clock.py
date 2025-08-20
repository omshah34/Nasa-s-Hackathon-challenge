import tkinter as tk
import time

def update_time():
    current_time = time.strftime("%H:%M:%S")
    canvas.delete("all")  

    width = canvas.winfo_width()
    height = canvas.winfo_height()

    font_size = int(height * 0.6)

    canvas.create_text(width/2, height/2, text=current_time, fill=foreground,font=("boulder", font_size, "bold"))

    canvas.after(200, update_time) 

app_window = tk.Tk()
app_window.title("Digital Clock")
app_window.geometry("500x200")
app_window.configure(bg="#000000")  

background = "#f2bc07"
foreground = "#363634"

canvas = tk.Canvas(app_window, bg=background, highlightthickness=0)
canvas.pack(expand=True, fill='both')

update_time()
app_window.mainloop()