from get_order import *
#from start_params import count


import tkinter as tk
global count
#count = 271
print ('is this outside the loop?')
window_main = tk.Tk(className = 'place order')
window_main.geometry('200x100')





button_submit = tk.Button(window_main, text = 'Place Order', command = lambda: place_order(count))
button_submit.config(width = 20, height = 2)
count+=1
button_submit.pack()
window_main.mainloop()