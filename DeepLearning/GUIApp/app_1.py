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

def change_colormap(choice):
    output_label.configure(text=choice)
    
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
colors = ["Spectrum", "Fire", "Hot-and-cold", "Gold", "Overlay", "Red Overlay", "Green overlay", "Blue overlay"]
default_combox = customtkinter.StringVar(value="Select colormap")
colors_selection = customtkinter.CTkComboBox(app, values=colors, command=change_colormap, variable=default_combox)
colors_selection.pack()

output_label = customtkinter.CTkLabel(app, text="")
output_label.pack()

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
    if view_axis == "axial":
        img_colorized = cv2.applyColorMap(img[int(index_slice), :, :].astype(np.uint8), cmapy.cmap('viridis'))
        image_display = Image.fromarray(img_colorized)
        
        plt.title("Virdis color display")
        plt.imshow(img[int(index_slice), :, :], cmap='viridis')
        plt.show()
        
        my_image = customtkinter.CTkImage(dark_image=image_display, size=(400, 400))
        image_label_axial.configure(image=my_image)  
        image_label_axial.image = my_image  
        
    elif view_axis == "sagittal":
        img_colorized = cv2.applyColorMap(img[:, int(index_slice), :].astype(np.uint8), cmapy.cmap('Pastel1'))
        image_display = Image.fromarray(img_colorized)
        my_image = customtkinter.CTkImage(dark_image=image_display, size=(400, 400))
        image_label_sagittal.configure(image=my_image)  
        image_label_sagittal.image = my_image  
        
    else:
        img_colorized = cv2.applyColorMap(img[:, :, int(index_slice)].astype(np.uint8), cmapy.cmap('Pastel2'))
        image_display = Image.fromarray(img_colorized)
        my_image = customtkinter.CTkImage(dark_image=image_display, size=(400, 400))
        image_label_coronal.configure(image=my_image)  
        image_label_coronal.image = my_image  
    
app.mainloop()