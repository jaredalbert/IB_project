from get_order import *

import tkinter as tk

window_main = tk.Tk(className = 'place order')
window_main.geometry('200x100')

def add():
    return 3 + 4

def submit_function():
    x = add()
    print (f'{x} submit function was pressed')

button_submit = tk.Button(window_main, text = 'Split Order', command = get_order )
button_submit.config(width = 20, height = 2)

button_submit.pack()
window_main.mainloop()