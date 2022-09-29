import tkinter as tk

window_main = tk.Tk(className = 'tutorial_window')
window_main.geometry('400x200')

def add():
    return 3 + 4

def submit_function():
    x = add()
    print (f'{x} submit function was pressed')

button_submit = tk.Button(window_main, text = 'Submit', command = submit_function)
button_submit.config(width = 20, height = 2)

button_submit.pack()
window_main.mainloop()