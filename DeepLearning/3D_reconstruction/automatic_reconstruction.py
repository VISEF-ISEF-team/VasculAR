import nibabel as nib
import numpy as np
from stl import mesh
from skimage import measure
from vedo import *
from vedo.applications import RayCastPlotter
import os
import SimpleITK as sitk
from tqdm import tqdm
from vedo.applications import IsosurfaceBrowser
import vedo
from DetailCutting import ShowDetails

class AutomaticReconstruction():
    def __init__(self, path_stl, path_volume_rendering, input_analysis, info_patient_dict):
        self.path = path_stl
        self.path_volume_rendering = path_volume_rendering
        self.files = [f for f in os.listdir(self.path) if f.endswith('.stl')]
        self.meshes = []
        self.buttons = []
        self.textures = [
            'main_texture_1.jpg',  
            'main_texture_2.png', 
            'main_texture_1.jpg', 
            'main_texture_3.png', 
            'main_texture_3.png', 
            'main_texture_1.jpg', 
            'main_texture_2.png', 
            'main_texture_3.png', 
            'main_texture_1.jpg', 
            'main_texture_1.jpg', 
            'main_texture_1.jpg',
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
            'Động mạch chủ trên',
        ]
        self.input_analysis = input_analysis
        self.info_patient_dict = info_patient_dict
        self.analysis()
        self.show_info_patient()


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
        Tổng Quan
        {self.input_analysis['Tổng quan']}
        """

        # Create a Text object with the specified content
        self.txt = Text2D(text_content, pos=('top-left'), font='C:/Windows/Fonts/Arial.ttf', s=0.7, c='w')
        
    def show_info_patient(self):
        self.info_patient = f"""
        Đơn vị tổ chức: {self.info_patient_dict['Organization']}
        Tên bệnh nhân: {self.info_patient_dict["Patient's name"]}
        Phương thức chụp: {self.info_patient_dict["Modality"]}
        ID bệnh nhân: {self.info_patient_dict['Patient ID']}
        Bộ phận chụp: {self.info_patient_dict["Body Part Examined"]}
        Ngày chụp: {self.info_patient_dict["Acquisition Date"]}
        """
        self.info = Text2D(self.info_patient, pos=('top-right'), font='C:/Windows/Fonts/Arial.ttf', s=0.5, c='#00EA94')

    def show_mesh(self):
        self.plt = Plotter()
        
        show_another_win = self.plt.add_button(
            self.view_2,
            pos=(0.5, 0.9),                                                                   
            states=['Volume Rendering', 'Volume Rendering'],                    
            c=["w", "w"],                                                                 
            bc=["dv", "dv"],                                                                         
            font='C:/Windows/Fonts/Arial.ttf',                                 
            size=10,                                                                              
            bold=True,                                                                             
            italic=False,                                                                          
            angle=0.3,
        )
        
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
                
                def show_detail(index):
                    def btn_func():
                        instance = ShowDetails(
                            mesh=self.meshes[index], 
                            analysis_header=self.classes[index],
                            analysis_note=self.input_analysis[self.classes[index]],
                        )
                    return btn_func
    
                # Add a button for each mesh in meshes
                button = self.plt.add_button(
                    toggle_alpha(mesh, i),
                    pos=(0.1, 0.4 - i * 0.035),                                                                    # x,y fraction from bottom left corner
                    states=[f'{str(i+1)}. {self.classes[i]}', f'{str(i+1)}. {self.classes[i]}'],                    # text for each state
                    c=["w", "w"],                                                                                   # font color for each state
                    bc=["#0d6efd", "dv"],                                                                           # background color for each state
                    font='C:/Windows/Fonts/Arial.ttf',                                                              # font type
                    size=10,                                                                                        # font size
                    bold=True,                                                                                      # bold font
                    italic=False,                                                                                   # non-italic font style
                    angle=0.3,
                )
                
                button_show_detail = self.plt.add_button(
                    show_detail(i),
                    pos=(0.2, 0.4 - i * 0.035),                                                                    
                    states=['Xem chi tiết'],                    
                    c=["w", "w"],                                                                                  
                    bc=["red", "red"],                                                                           
                    font='C:/Windows/Fonts/Arial.ttf',                                                             
                    size=10,                                                                                       
                    bold=True,                                                                                      
                    italic=False,                                                                                  
                    angle=0.3,
                )
                
                self.buttons.append(button)       
    
        self.plt.show(self.meshes, self.txt, self.info, bg='black')
        self.plt.interactive().close()
    
    def view_2(self):
        self.plt2 = Plotter()
        nifti_image = sitk.ReadImage(self.path_volume_rendering)
        array=sitk.GetArrayFromImage(nifti_image)
        volume = vedo.Volume(array) 

        scrange = volume.scalar_range()
        delta = scrange[1] - scrange[0]
        if not delta:
            return

        isovalue = None
        if isovalue is None:
            isovalue = delta / 3.0 + scrange[0]

        ### isovalue slider callback
        def slider_isovalue(widget, event):
            value = widget.GetRepresentation().GetValue()
            isovals.SetValue(0, value)

        isovals = volume.GetProperty().GetIsoSurfaceValues()
        isovals.SetValue(0, isovalue)

        self.plt2.renderer.AddActor(volume.mode(5).alpha(1).c('copper'))

        self.plt2.add_slider(
            slider_isovalue,
            scrange[0] + 0.02 * delta,
            scrange[1] - 0.02 * delta,
            value=isovalue,
            pos=2,
            title="Tái Tạo cấu trúc 3 Chiều Nguyên Khối",
            font='C:/Windows/Fonts/Arial.ttf', 
            show_value=True,
            delayed=False,
        )
        
        self.plt2.show(axes=0, bg='black').close()
    
    
isinstance = AutomaticReconstruction(
    path_stl='D:/Documents/GitHub/VascuIAR/DeepLearning/data/VnRawData/SegmentationData/ct_0016_label_resized/',
    path_volume_rendering= 'D:/Documents/GitHub/VascuIAR/DeepLearning/data/MM_WHS/train_images/ct_train_1017_image.nii.gz',
    input_analysis = {
        'Tổng quan': 'Phân tích tổng quan',
        'Tĩnh mạch chủ': 'Phân tích tĩnh mạch chủ',
        'Tiểu nhĩ': 'Phân tích tiểu nhĩ',
        'Động mạch vành' :  'Phân tích động mạch vành',
        'Tâm thất trái' : 'Phân tích tâm thất trái',
        'Tâm thất phải' : 'Phân tích tâm thất phải',
        'Tâm nhĩ trái':  'Phân tích tâm nhĩ trái',
        'Tâm nhĩ phải' : 'Phân tích tâm nhĩ phải',
        'Thành cơ tim' : 'Phân tích thành cơ tim',
        'Cung động mạch chủ' : 'Phant ích cung động mạch chủ',
        'Động mạch phổi': 'Phân tích động mạch phổi',
        'Động mạch chủ trên': 'Phân tích động mạch chủ trên',
    },
    
    info_patient_dict = {
        "Organization": "Benh vien Cho Ray",
        "Patient's name": "Ton That Hung",
        "Modality": "MRI",
        "Patient ID": "0000097031",
        "Body Part Examined": "CHEST_TO_PELVIS",
        "Acquisition Date": "20231019"
    }
)
isinstance.show_mesh()



