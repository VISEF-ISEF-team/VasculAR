import customtkinter
import tkinter
from PIL import Image
import SimpleITK as sitk
import matplotlib.pyplot as plt
import cv2 
import cmapy
import numpy as np


# window theme
customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

# window configuration
app = customtkinter.CTk()
app.title('VasculAR software')
app.geometry("1600x800")
app.iconbitmap('imgs/logo.ico')

# Functions control
def slider_volume_show(value):
    index_slice = round(value, 0)
    text_show_volume.configure(text=index_slice)
    slice_control(index_slice)

    
# Tab view    
tabview = customtkinter.CTkTabview(master=app, width=500, height=500) # add command argument here
tabview.pack(padx=100, pady=100)
tab_1 = tabview.add("axial")
tab_2 = tabview.add("sagittal")
tab_3 = tabview.add("coronal")
tabview.set("axial") 

# Load volumn image
img = sitk.ReadImage('../data/MM_WHS/train_images/ct_train_1001_image.nii.gz', sitk.sitkFloat32)
img = sitk.GetArrayFromImage(img)

slider_volume = customtkinter.CTkSlider(app, from_=0, to=img.shape[0]-1, command=slider_volume_show)
slider_volume.pack()

text_show_volume = customtkinter.CTkLabel(app, text="")
text_show_volume.pack()

# Colormap choose 
colors = ["gray", "viridis", "plasma", "inferno", "magma", "cividis", "Greys", "Purples", "Blues", "Greens", "Reds", "YlOrBr", "YlOrRd", "OrRd", "PuRd", "GnBu"]
color_picker_default = customtkinter.StringVar(value="Grayscale")
color_picker = customtkinter.CTkComboBox(app, values=colors, variable=color_picker_default)
color_picker.pack()

# Slice display
# axial view
image_label_axial = customtkinter.CTkLabel(tab_1, text="")  # create the CTkLabel here
image_label_axial.pack()

# sagittal view
image_label_sagittal = customtkinter.CTkLabel(tab_2, text="")  # create the CTkLabel here
image_label_sagittal.pack()

# coronal view
image_label_coronal = customtkinter.CTkLabel(tab_3, text="")  # create the CTkLabel here
image_label_coronal.pack()

def slice_control(index_slice):
    view_axis = tabview.get()
    color_choice = color_picker.get()
    if view_axis == "axial":
        plt.imsave('temp.jpg', img[int(index_slice), :, :], cmap=color_choice)
        image_gray = cv2.imread('temp.jpg')
        image_display = Image.fromarray(image_gray)
        my_image = customtkinter.CTkImage(dark_image=image_display, size=(400, 400))
        image_label_axial.configure(image=my_image)  
        image_label_axial.image = my_image  
        
    elif view_axis == "sagittal":
        plt.imsave('temp.jpg', img[:, int(index_slice), :], cmap=color_choice)
        image_gray = cv2.imread('temp.jpg')
        image_display = Image.fromarray(image_gray)
        my_image = customtkinter.CTkImage(dark_image=image_display, size=(400, 400))
        image_label_sagittal.configure(image=my_image)  
        image_label_sagittal.image = my_image  
        
    else:
        plt.imsave('temp.jpg', img[:, :, int(index_slice)], cmap=color_choice)
        image_gray = cv2.imread('temp.jpg')
        image_display = Image.fromarray(image_gray)
        my_image = customtkinter.CTkImage(dark_image=image_display, size=(400, 400))
        image_label_coronal.configure(image=my_image)  
        image_label_coronal.image = my_image  
        
    
app.mainloop()