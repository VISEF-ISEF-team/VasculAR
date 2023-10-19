import tkinter as tk
import customtkinter
from tkinter import Entry, Frame, Label
from tkinter.constants import HORIZONTAL, RAISED, SUNKEN
from tkinter import Canvas

class Colorpicker:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Picker")
        self.root.geometry("300x480")
        self.root.iconbitmap('imgs/logo.ico')
        self.root.resizable(0,0)

        self.R = tk.IntVar()
        self.G = tk.IntVar()
        self.B = tk.IntVar()
        self.hex = tk.IntVar()


        self.color_canvas = Canvas(master=self.root, bg="black", width=400, height=250, highlightthickness=0)
        self.color_canvas.grid(row=0, column=0)
        self.color_canvas.bind("<Double-1>", self.copy_color)
        
        frame = customtkinter.CTkFrame(master=self.root)
        frame.grid(row=1, column=0, padx=6, pady=10, sticky="nsew")
            
        r_label = customtkinter.CTkLabel(frame, text="Red")
        r_label.grid(row=0, column=0, pady=5, padx=10, sticky="nw")

        self.R_Scale = customtkinter.CTkSlider(frame, from_=0, to=255, width=200, fg_color="#f2004a",
                                            button_color="#f2004a", button_hover_color="#f2004a", orientation="horizontal", command=self.scaleMove)
        self.R_Scale.set(132)
        self.R_Scale.grid(row=0, column=1, pady=5)

        g_label = customtkinter.CTkLabel(frame, text="Green")
        g_label.grid(row=1, column=0, pady=5, padx=10, sticky="nw")

        self.G_Scale = customtkinter.CTkSlider(frame, from_=0, to=255, width=200, fg_color="#00a200",
                                            button_color="#00a200", button_hover_color="#00a200", orientation="horizontal", command=self.scaleMove)
        self.G_Scale.grid(row=1, column=1, pady=5)

        b_label = customtkinter.CTkLabel(frame, text="Blue")
        b_label.grid(row=2, column=0, pady=5, padx=10, sticky="nw")

        self.B_Scale = customtkinter.CTkSlider(
            frame, from_=0, to=255, width=200, fg_color="#0087f2", orientation="horizontal", command=self.scaleMove)
        self.B_Scale.set(255)
        self.B_Scale.grid(row=2, column=1, pady=5)

        hex_label = customtkinter.CTkLabel(frame, text="Hex Code :")
        hex_label.grid(row=3, column=0, pady=5, padx=10)

        self.hex_entry = customtkinter.CTkEntry(frame)
        self.hex_entry.insert(tk.END, '#8400ff')
        self.hex_entry.grid(row=3,column=1, pady=5, padx=10)

        rbg_label = customtkinter.CTkLabel(frame, text="RGB Code :")
        rbg_label.grid(row=4, column=0, pady=5, padx=10)

        self.rgb_entry = customtkinter.CTkEntry(frame)
        self.rgb_entry.grid(row=4, column=1, pady=5, padx=10)
        
        self.button_another = customtkinter.CTkButton(master=self.root, text="More", command=self.ask_color, width=250)
        self.button_another.grid(row=5, column=0, pady=10, columnspan=2)
        
        self.button_ok = customtkinter.CTkButton(master=self.root, text="Done", command=self.terminate,  width=250)
        self.button_ok.grid(row=6, column=0, pady=10, columnspan=2)
        
    def terminate(self, *arg):
        return self.hex_entry.get()
       
    def ask_color(self, *args):
        pass
                         
    def scaleMove(self, *args):
        self.R = int(self.R_Scale.get())
        self.G = int(self.G_Scale.get())
        self.B = int(self.B_Scale.get())
        rgb = f"{self.R},{self.G},{self.B}"

        # print(r,g,b)
        self.hex = "#%02x%02X%02x" % (self.R, self.G, self.B)
        self.color_canvas.config(bg=self.hex)
        # Hex to RGB
        # h = color_hex.lstrip('#')
        # print('RGB =', tuple(int(h[i:i+2], 16) for i in (0, 2, 4)))

        self.hex_entry.delete(0, tk.END)
        self.hex_entry.insert(0, self.hex)

        self.rgb_entry.delete(0, tk.END)
        self.rgb_entry.insert(0, rgb)

    def copy_color(self, *args):
        root.clipboard_clear()  # clear clipboard contents
        root.clipboard_append(self.hex)  # append new value to clipbaord

if __name__ == "__main__":
    root = customtkinter.CTk()
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("blue")
    color_choosed = Colorpicker(root) 
    print(color_choosed)
    root.mainloop()
    


