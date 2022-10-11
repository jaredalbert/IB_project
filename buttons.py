



import tkinter as tk
from get_order import *

window_main = tk.Tk(className = 'place order')
window_main.geometry('200x100')

button_submit = tk.Button(window_main, text = 'Place Order', command = place_order)
button_submit.config(width = 20, height = 2)

button_submit.pack()
window_main.mainloop()