import tkinter as tk
from tkinter import ttk

window = tk.Tk()
window.title('buttons')
window.geometry('600x400')

def button_func():
    print('a basic button')
    print(radio_var.get())

# button
button_string = tk.StringVar(value = 'a button with stringvar')
button = ttk.Button(window, 
                    text='A simple button', 
                    command = button_func, 
                    textvariable = button_string)
button.pack()

# checkbutton
check_var = tk.IntVar()
check1 = ttk.Checkbutton(
    window, 
    text = 'checkbox 1',
    command = lambda: print(check_var.get()),
    variable = check_var,
    onvalue = 10,
    offvalue = 5
    )
check1.pack()

check2 = ttk.Checkbutton(
    window,
    text = 'Checkbox 2',
    variable = check_var,
    command = lambda: print('test'))
check2.pack()


# radio buttons
radio_var = tk.StringVar()
radio1 = ttk.Radiobutton(
    window, 
    text = 'radio button 1', 
    value = 'radio 1',
    variable = radio_var,
    command = lambda: print(radio_var.get()))
radio1.pack()

radio2 = ttk.Radiobutton(
    window, 
    text = 'radio button 2', 
    variable = radio_var,
    value = 2)
radio2.pack()


# excercise radios
def radio_func():
    print(check_bool.get())
    check_bool.set(False)
    
# data
radio_string = tk.StringVar()
check_bool = tk.BooleanVar()

# widgets
exercise_radio1 = ttk.Radiobutton(
    window, 
    text = 'Radio A',  
    value = 'A', 
    command = radio_func, 
    variable = radio_string)
exercise_radio2 = ttk.Radiobutton(
    window, 
    text = 'Radio B',  
    value = 'B', 
    command = radio_func, 
    variable = radio_string) 

exercise_check = ttk.Checkbutton(
    window, 
    text = 'Excercise Check',
    variable = check_bool,
    command = lambda: print(radio_string.get()))

# layout
exercise_radio1.pack()
exercise_radio2.pack()
exercise_check.pack()

# run
window.mainloop()