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
    def __init__(self, path, input_analysis):
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
        self.classes = [
            'Tĩnh mạch chủ', 
            'Tiểu nhĩ', 
            'Động mạch vành', 
            'Tâm thất trái', 
            'Tâm thất phải', 
            'Tâm nhĩ trái', 
            'Tâm nhĩ phải', 
            'Thành cơ tim', 
            'Cung động mạch chủ', 
            'Động mạch phổi', 
            'Động mạch chủ trên'
        ]
        self.input_analysis = input_analysis
        self.analysis()


    def load_mesh(self, filename, texture):
        mesh = load(filename)
        mesh.smooth(niter=100)
        mesh.texture('textures/' + texture)
        return mesh
    
    def analysis(self):
        text_content = f"""
        ********************************************
        Đoạn chẩn đoán gợi ý bệnh lý dưới đây 
        được tạo ra từ mô hình Deep Learning
        của VasculAR, cần được duyệt qua bởi 
        người có chuyên môn. Bạn có thể chỉnh
        sửa nội dung bằng phần mềm VasculAR.
        
        ********************************************
        
        Đây là nội dung phân tích:
        {self.input_analysis}
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
                    pos=(0.04, 0.5 - i * 0.035),                                                                   # x,y fraction from bottom left corner
                    states=[f'{str(i+1)}. {self.classes[i]}', f'{str(i+1)}. {self.classes[i]}'],                    # text for each state
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
    path='D:/Documents/GitHub/VascuIAR/DeepLearning/data/MM_WHS/seg_res/1070/',
    input_analysis = ''
)
isinstance.show_mesh()



