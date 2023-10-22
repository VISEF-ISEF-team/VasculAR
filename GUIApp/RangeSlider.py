from CTkRangeSlider import *
import customtkinter

def show_value(value):
    print(value[0], value[1])
    another_func()
    
def another_func():
    print("Get Func:", range_slider.get())    
    
root = customtkinter.CTk()
range_slider = CTkRangeSlider(root, from_=-1000, to=10000, command=show_value)
range_slider.pack(padx=30, pady=30, fill="both")
root.mainloop()