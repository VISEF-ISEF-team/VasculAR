import customtkinter
import tkinter
from PIL import Image
import SimpleITK as sitk
import matplotlib.pyplot as plt
import cv2 
import numpy as np
from tkinter import filedialog


# window theme
customtkinter.set_appearance_mode("dark")  
customtkinter.set_default_color_theme("blue") 

# window configuration
app = customtkinter.CTk()
app.title('VasculAR software')
app.geometry("1600x800")
app.iconbitmap('imgs/logo.ico')

for i in range(12): 
    app.rowconfigure(i, weight=1, uniform='a') 
    app.columnconfigure(i, weight=1, uniform='a') 
    
for i in range(12):
    for j in range(12):
        label = customtkinter.CTkFrame(app, fg_color="transparent")
        label.grid(column=i, row=j, sticky='nsew')
        
# create a button to open the file chooser dialog
def choose_file():
    filename = filedialog.askopenfilename()
    file_label.configure(placeholder_text=filename)

uploader_frame = customtkinter.CTkScrollableFrame(app, orientation='horizontal', label_text="File uploader")
uploader_frame.grid(column=0, row=0, columnspan=2, rowspan=2, sticky='nsew')
uploader_frame.columnconfigure(0, weight=1)

file_label = customtkinter.CTkEntry(uploader_frame, placeholder_text="No file selected")
file_label.grid(column=0, row=0, sticky='ew', padx=5, pady=5)

choose_button = customtkinter.CTkButton(uploader_frame, text="Choose File", command=choose_file)
choose_button.grid(column=0, row=1, sticky='ew', padx=5)


    


app.mainloop()