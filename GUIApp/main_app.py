import customtkinter
import tkinter
from PIL import Image
import SimpleITK as sitk
import matplotlib.pyplot as plt
import cv2 
import numpy as np
from tkinter import filedialog

# window theme
customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

# window configuration
app = customtkinter.CTk()
app.title('VasculAR software')
app.geometry("1600x800")
app.iconbitmap('imgs/logo.ico')
for i in range(12): 
    app.rowconfigure(i, weight=1) 
    app.columnconfigure(i, weight=1) 

# Functions control
def slider_volume_show(value):
    index_slice = round(value, 0)
    text_show_volume.configure(text=index_slice)
    slice_control(index_slice)
    
# create a button to open the file chooser dialog
def choose_file():
    filename = filedialog.askopenfilename()
    file_label.configure(text=filename)

# Tab view    
tabview = customtkinter.CTkTabview(master=app) # add command argument here
tabview.grid(column=2, row=1, columnspan=6, rowspan=8, sticky="nsew")
tab_1 = tabview.add("axial")
tab_2 = tabview.add("sagittal")
tab_3 = tabview.add("coronal")
tabview.set("axial") 

# File uploader
file_uploader = customtkinter.CTkTextbox(app, activate_scrollbars=True)
file_uploader.grid(row=0, column=0, columnspan=2, sticky="nsew")

# Path
file_label = customtkinter.CTkLabel(file_uploader, text="No file selected")
file_label.grid(row=1, column=0)

# Uploader button
choose_button = customtkinter.CTkButton(file_uploader, text="Choose File", command=choose_file, width=20)
choose_button.grid(row=0, column=0)

# Load volumn image
img = sitk.ReadImage('../DeepLearning/data/MM_WHS/train_images/ct_train_1001_image.nii.gz', sitk.sitkFloat32)
img = sitk.GetArrayFromImage(img)

slider_volume = customtkinter.CTkSlider(app, from_=0, to=img.shape[0]-1, command=slider_volume_show)
slider_volume.grid(column=4, row=0)

text_show_volume = customtkinter.CTkLabel(app, text="")
text_show_volume.grid(column=4, row=1)

# Colormap choose 
colors = ["gray", "nipy_spectral", "viridis", "plasma", "inferno", "magma", "cividis", "Greys", "Purples", "Blues", "Greens", "Reds", "YlOrBr", "YlOrRd", "OrRd", "PuRd", "GnBu"]
color_picker_default = customtkinter.StringVar(value="gray")
color_picker = customtkinter.CTkComboBox(app, values=colors, variable=color_picker_default)
color_picker.grid(column=6, row=0)

# Slice display
# axial view
image_label_axial = customtkinter.CTkLabel(tab_1, text="")  # create the CTkLabel here
image_label_axial.place(relx=0.5, rely=0.5, anchor="center")

# sagittal view
image_label_sagittal = customtkinter.CTkLabel(tab_2, text="")  # create the CTkLabel here
image_label_sagittal.place(relx=0.5, rely=0.5, anchor="center")

# coronal view
image_label_coronal = customtkinter.CTkLabel(tab_3, text="")  # create the CTkLabel here
image_label_coronal.place(relx=0.5, rely=0.5, anchor="center")

def slice_control(index_slice):
    view_axis = tabview.get()
    color_choice = color_picker.get()
    if view_axis == "axial":
        plt.imsave('temp.jpg', img[int(index_slice), :, :], cmap=color_choice)
        image_gray = cv2.imread('temp.jpg')
        image_display = Image.fromarray(image_gray)
        my_image = customtkinter.CTkImage(dark_image=image_display, size=(512,512))
        image_label_axial.configure(image=my_image)  
        image_label_axial.image = my_image  
        
    elif view_axis == "sagittal":
        plt.imsave('temp.jpg', img[:, int(index_slice), :], cmap=color_choice)
        image_gray = cv2.imread('temp.jpg')
        image_display = Image.fromarray(image_gray)
        my_image = customtkinter.CTkImage(dark_image=image_display, size=(512,512))
        image_label_sagittal.configure(image=my_image)  
        image_label_sagittal.image = my_image  
        
    else:
        plt.imsave('temp.jpg', img[:, :, int(index_slice)], cmap=color_choice)
        image_gray = cv2.imread('temp.jpg')
        image_display = Image.fromarray(image_gray)
        my_image = customtkinter.CTkImage(dark_image=image_display, size=(512,512))
        image_label_coronal.configure(image=my_image)  
        image_label_coronal.image = my_image  
        
    
app.mainloop()