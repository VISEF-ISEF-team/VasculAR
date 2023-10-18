import customtkinter
import tkinter
from PIL import Image, ImageTk
import SimpleITK as sitk
import matplotlib.pyplot as plt
import cv2 
import numpy as np
from tkinter import filedialog, Canvas
from helpers import *
from draw import draw_canvas

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
    file_path.configure(placeholder_text=filename)

def button_callback():
    pass

uploader_frame = customtkinter.CTkFrame(app)
uploader_frame.grid(column=0, row=0, columnspan=2, rowspan=2, sticky='nsew', padx=5)

uploader_frame.grid_columnconfigure(0, weight=1)
uploader_frame.grid_rowconfigure((0, 1, 2), weight=1)

label_text = customtkinter.CTkButton(uploader_frame, text='File uploader', state='disabled', fg_color='#3b3b3b', text_color_disabled='#dce4e2')
label_text.grid(column=0, row=0, sticky="ew", padx=10, pady=0.5)

file_path = customtkinter.CTkEntry(uploader_frame, placeholder_text="File path here")
file_path.grid(column=0, row=1, sticky="ew",  padx=10)

choose_button = customtkinter.CTkButton(uploader_frame, text="Choose File", command=choose_file)
choose_button.grid(column=0, row=2, sticky="ew", padx=10)


# Load volumn image
info_frame = customtkinter.CTkScrollableFrame(app, orientation='horizontal', label_text='Image info')
info_frame.grid(column=0, row=2, columnspan=2, rowspan=4, sticky='nsew', pady=5, padx=5)

info_frame.grid_columnconfigure(0, weight=1)
info_frame.grid_columnconfigure(1, weight=2)
info_frame.grid_rowconfigure((0, 1, 2, 3), weight=1)

print(file_path.get())
if file_path.get() != "File path here":
    print(file_path.get())
    img_raw = sitk.ReadImage('../DeepLearning/data/MM_WHS/train_images/ct_train_1001_image.nii.gz', sitk.sitkFloat32)
    img = sitk.GetArrayFromImage(img_raw)
    
    # Show image info
    info = show_sitk_img_info(img_raw)
    for i, (k, v) in enumerate(info.items()):
        label1 = customtkinter.CTkLabel(info_frame, text=k)
        label1.grid(column=0, row=i, sticky="w", padx=5)
        
        label2 = customtkinter.CTkLabel(info_frame, text=v)
        label2.grid(column=1, row=i, sticky="w", padx=5)
        
        
# Main canvas      
# Tab view    
tabview = customtkinter.CTkTabview(master=app) # add command argument here
tabview.grid(column=2, row=1, columnspan=8, rowspan=8, sticky="nsew", padx=5, pady=5)
tab_1 = tabview.add("axial")
tab_2 = tabview.add("sagittal")
tab_3 = tabview.add("coronal")
tabview.set("axial") 

# Functions control
def slider_volume_show(value):
    index_slice = round(value, 0)
    text_show_volume.configure(text=int(index_slice))
    slice_control(index_slice)
    


# ====== 1. Slider control ======
slider_control = customtkinter.CTkFrame(app)
slider_control.grid(column=2, row=0, columnspan=2, rowspan=1, sticky='nsew')
slider_control.grid_rowconfigure((0, 1), weight=1)
slider_control.grid_columnconfigure(0, weight=2)
slider_control.grid_columnconfigure(1, weight=1)

label_text = customtkinter.CTkButton(slider_control, text='View slice', state='disabled', fg_color='#3b3b3b', text_color_disabled='#dce4e2')
label_text.grid(column=0, row=0, columnspan=2, sticky="ew", padx=10, pady=0.5)

slider_volume = customtkinter.CTkSlider(slider_control, from_=0, to=img.shape[0]-1, command=slider_volume_show, bg_color='#2b2b2b')
slider_volume.grid(column=0, row=1, sticky='ew', padx=5)

text_show_volume = customtkinter.CTkLabel(slider_control, text="", bg_color='#2b2b2b')
text_show_volume.grid(column=1, row=1, sticky='ew')

# ====== 2. Color picker ======
color_picker_frame = customtkinter.CTkFrame(app)
color_picker_frame.grid(column=4, row=0, columnspan=2, rowspan=1, sticky='nsew', padx=5)
color_picker_frame.grid_rowconfigure((0, 1), weight=1)
color_picker_frame.grid_columnconfigure(0, weight=1)

label_text = customtkinter.CTkButton(color_picker_frame, text='Color picker', state='disabled', fg_color='#3b3b3b', text_color_disabled='#dce4e2')
label_text.grid(column=0, row=0, columnspan=2, sticky="ew", padx=10, pady=0.5)

# Colormap choose 
colors = ["gray", "nipy_spectral", "viridis", "plasma", "inferno", "magma", "cividis", "Greys", "Purples", "Blues", "Greens", "Reds", "YlOrBr", "YlOrRd", "OrRd", "PuRd", "GnBu"]
color_picker_default = customtkinter.StringVar(value="gray")
color_picker = customtkinter.CTkComboBox(color_picker_frame, values=colors, variable=color_picker_default)
color_picker.grid(column=0, row=1, sticky='ew', padx=10)

#====== 3. Draw control ======
draw_control = customtkinter.CTkFrame(app)
draw_control.grid(column=6, row=0, columnspan=2, rowspan=1, sticky='nsew')
draw_control.grid_rowconfigure((0, 1), weight=1)
draw_control.grid_columnconfigure(0, weight=2)
draw_control.grid_columnconfigure(1, weight=1)

# axial view
my_canvas_axial = Canvas(tab_1, width=700, height=700, bg='#2b2b2b', border=0)
my_canvas_axial.place(relx=0.5, rely=0.5, anchor="center")

radio_var = tkinter.IntVar(value=1)
line_distance = customtkinter.CTkLabel(tab_1, text="")
coordinate_label = customtkinter.CTkLabel(tab_1, text="")
draw_canvas_axial = draw_canvas(my_canvas_axial, radio_var, line_distance, coordinate_label)

# bind the functions to the mouse events on the canvas
my_canvas_axial.bind("<Button-1>", draw_canvas.on_press)
my_canvas_axial.bind("<ButtonRelease-1>", draw_canvas.on_release)

clear_button = customtkinter.CTkButton(draw_control, text="Clear", command=draw_canvas.clear)
clear_button.grid(column=0, row=1, padx=5)
redo_button = customtkinter.CTkButton(draw_control, text="Redo", command=draw_canvas.redo)
redo_button.grid(column=1, row=1, padx=5)
line_distance.pack()
coordinate_label.pack()


Rectangle = customtkinter.CTkRadioButton(draw_control, text="Rectangle", command=draw_canvas.radiobutton_event, variable=radio_var, value=1)
line = customtkinter.CTkRadioButton(draw_control, text="Line", command=draw_canvas.radiobutton_event, variable=radio_var, value=2)
Rectangle.grid(column=0, row=0)
line.grid(column=1, row=0)


# sagittal view
my_canvas_sagittal = Canvas(tab_2, width=700, height=700, bg='#2b2b2b', border=0)
my_canvas_sagittal.place(relx=0.5, rely=0.5, anchor="center")

# coronal view
my_canvas_coronal = Canvas(tab_3, width=700, height=700, bg='#2b2b2b', border=0)
my_canvas_coronal.place(relx=0.5, rely=0.5, anchor="center")

# Main canvas
def slice_control(index_slice):
    view_axis = tabview.get()
    color_choice = color_picker.get()
    if view_axis == "axial":
        plt.imsave("temp.jpg", img[int(index_slice), :, :], cmap=color_choice)
        image_display = Image.open("temp.jpg").resize((750, 750))
        my_image = ImageTk.PhotoImage(image_display)
        my_canvas_axial.create_image(0, 0, image=my_image, anchor="nw")  
        my_canvas_axial.image = my_image
        
    elif view_axis == "sagittal":
        plt.imsave("temp.jpg", img[:, int(index_slice), :], cmap=color_choice)
        image_display = Image.open("temp.jpg").resize((750, 750))
        my_image = ImageTk.PhotoImage(image_display)
        my_canvas_sagittal.create_image(0, 0, image=my_image, anchor="nw")  
        my_canvas_sagittal.image = my_image
        
    else:
        plt.imsave("temp.jpg", img[:, :, int(index_slice)], cmap=color_choice)
        image_display = Image.open("temp.jpg").resize((750, 750))
        my_image = ImageTk.PhotoImage(image_display)
        my_canvas_coronal.create_image(0, 0, image=my_image, anchor="nw")  
        my_canvas_coronal.image = my_image

app.mainloop()