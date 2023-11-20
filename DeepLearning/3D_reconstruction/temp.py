import nibabel as nib
import numpy as np
from stl import mesh
from skimage import measure
from vedo import *
from vedo.applications import RayCastPlotter
import os
import SimpleITK as sitk
from tqdm import tqdm
# from DetailCutting import NewWindow


class AutomaticReconstruction():
    def __init__(self, path):
        self.path = path
        self.files = [f for f in os.listdir(self.path) if f.endswith('.stl')]
        self.meshes = []
        self.buttons = []
        self.textures = [
            'cardiac_texture_3.jpg',  
            'cardiac_texture_3.jpg', 
            'cardiac_texture_3.jpg', 
            'cardiac_texture_3.jpg', 
            'cardiac_texture_3.jpg', 
            'cardiac_texture_3.jpg', 
            'cardiac_texture_3.jpg', 
            'cardiac_texture_3.jpg', 
            'cardiac_texture_3.jpg', 
            'cardiac_texture_3.jpg', 
            'cardiac_texture_3.jpg', 
            'cardiac_texture_3.jpg'
        ]
        self.analysis()


    def load_mesh(self, filename, texture):
        mesh = load(filename)
        mesh.smooth(niter=100)
        mesh.texture('textures/' + texture)
        return mesh
    
    def analysis(self):
        text_content = """
        ********************************************
        Đoạn chẩn đoán gợi ý bệnh lý dưới đây 
        được tạo ra từ mô hình Deep Learning
        của VasculAR, cần được duyệt qua bởi 
        người có chuyên môn. Bạn có thể chỉnh
        sửa nội dung bằng phần mềm VasculAR.
        
        ********************************************
        
        Đây là nội dung phân tích:
        """

        # Create a Text object with the specified content
        self.txt = Text2D(text_content, pos=('top-left'), font='C:/Windows/Fonts/Arial.ttf', s=0.7, c='w')

    def show_mesh(self):
        self.plt = Plotter()
        for i in tqdm(range(len(self.files))):
            
            if self.files[i].endswith('.stl'):
                print(self.path + self.files[i])
                mesh = self.load_mesh(self.path + self.files[i], self.textures[i])
                self.meshes.append(mesh)

                # Define a function to toggle the alpha of a given mesh
                def toggle_alpha(mesh, i):
                    def buttonfunc():
                        mesh.alpha(1 - mesh.alpha())  
                        self.buttons[i].switch()  
                    return buttonfunc
    
                # Add a button for each mesh in meshes
                button = self.plt.add_button(
                    toggle_alpha(mesh, i),
                    pos=(0.05, 0.24 - i * 0.04),                                                                    # x,y fraction from bottom left corner
                    states=[f'{str(i+1)}. Động mạch vành mở', f'{str(i+1)}. Động mạch vành tắt'],                   # text for each state
                    c=["w", "w"],                                                                                   # font color for each state
                    bc=["#0d6efd", "dv"],                                                                           # background color for each state
                    font='C:/Windows/Fonts/Arial.ttf',                                                              # font type
                    size=10,                                                                                        # font size
                    bold=True,                                                                                      # bold font
                    italic=False,                                                                                   # non-italic font style
                    angle=0.3,
                )
                
                self.buttons.append(button)
                

        
        self.plt = show(self.meshes, self.txt, bg='black')
        self.plt.show()
    
    
isinstance = AutomaticReconstruction(
    path='D:/Documents/GitHub/VascuIAR/DeepLearning/data/VnRawData/SegmentationData/ct_0035_label_resized/'
)
isinstance.show_mesh()



