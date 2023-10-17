import customtkinter
import nibabel as nib
import numpy as np
from stl import mesh
from skimage import measure
from vedo import *
from vedo.applications import RayCastPlotter
import os
import SimpleITK as sitk
from tqdm import tqdm

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green


app = customtkinter.CTk()
app.title('VasculAR software')
app.geometry("1600x800")
app.iconbitmap('imgs/logo.ico')

# Define a function to load and smooth a mesh from a file
def load_mesh(filename, color, texture):
    mesh = load(filename)
    mesh.color(color)
    mesh.smooth(niter=100)
    mesh.texture('textures/' + texture)
    return mesh

def show_mesh(path):
    meshes = []
    colors = ['#f1d691', '#b17a65', '#6fb8d2', '#d8654f', '#b17a65', '#b17a65', '#b17a65',  '#fc8184', '#0d05ff', '#e6dc46', '#fa0101', '#f4d631', '#fc8184', '#90ee90', '#0d05ff']
    textures = ['cardiac_texture_4.jpg', 'cardiac_texture_2.jpeg', 'cardiac_texture_2.jpeg', 'cardiac_texture_3.jpg', 'cardiac_texture_2.jpeg', 'cardiac_texture_2.jpeg', 'cardiac_texture_2.jpeg']
    files = [f for f in os.listdir(path) if f.endswith('.stl')]
    buttons = []
    plt = Plotter()
    progress = tqdm(total=len(files))

    for i in range(len(files)):
        if files[i].endswith('.stl'):
            print(path + files[i])
            mesh = load_mesh(path + files[i], colors[i], textures[i])
            meshes.append(mesh)

            # Define a function to toggle the alpha of a given mesh
            def toggle_alpha(mesh, i):
                def buttonfunc():
                    mesh.alpha(1 - mesh.alpha())  
                    buttons[i].switch()  
                return buttonfunc

            # Add a button for each mesh in meshes
            button = plt.add_button(
                toggle_alpha(mesh, i),
                pos=(0.03, 0.24 - i * 0.02),  # x,y fraction from bottom left corner
                states=[str(i+1), str(i+1)],  # text for each state
                c=["w", "w"],                 # font color for each state
                bc=["#0d6efd", "dv"],         # background color for each state
                font="courier",               # font type
                size=10,                      # font size
                bold=True,                    # bold font
                italic=False,                 # non-italic font style
                angle=0.3,
            )
            
            buttons.append(button)
            
        # Update the tqdm object with one iteration and set the postfix to the current file name
        progress.update(1)
        progress.set_postfix(file=files[i])

        # Update the reconstruction_progress_bar with the current value of tqdm
        reconstruction_progress_bar.set(int(round(progress.n / progress.total * 100, 0)))
        print('PROGRESS BAR:', int(round(progress.n / progress.total * 100, 0)))
            
    plt = show(meshes, bg='black')
    plt.show()

def start_reconstruction():
    reconstruction_progress_bar.start()
    show_mesh('../data/MM_WHS/seg_res/1006/')
    
def cancel_reconstruction():
    reconstruction_progress_bar.stop()

reconstruction_progress_bar = customtkinter.CTkProgressBar(app, orientation="horizontal")
reconstruction_progress_bar.set(0.1)
reconstruction_progress_bar.pack(pady=20)

reconstruction_btn = customtkinter.CTkButton(app, text="Automatic 3D reconstruction", command=start_reconstruction)
reconstruction_btn.pack(padx=10, pady=21)

cancel_reconstruction_btn = customtkinter.CTkButton(app, text="Cancel process", command=cancel_reconstruction)
cancel_reconstruction_btn.pack(padx=10, pady=21)

def change_colormap(choice):
    output_label.configure(text=choice)

text = customtkinter.CTkLabel(app, text="Pick a color")
text.pack(pady=40)

colors = ["Spectrum", "Fire", "Hot-and-cold", "Gold", "Overlay", "Red Overlay", "Green overlay", "Blue overlay"]
default_combox = customtkinter.StringVar(value="Select colormap")
colors_selection = customtkinter.CTkComboBox(app, values=colors, command=change_colormap, variable=default_combox)
colors_selection.pack(pady=42)

output_label = customtkinter.CTkLabel(app, text="")
output_label.pack(pady=46)

app.mainloop()