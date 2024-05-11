import vedo
from vedo import *
import SimpleITK as sitk
import random
from vedo.applications import SplinePlotter
from vedo.applications import FreeHandCutPlotter
from _bit_marching_cubes_lewiner import *
from stl import mesh
from skimage.transform import resize
import sys
import json
import subprocess
from tqdm import tqdm

vedo.settings.use_parallel_projection = True 
specified_data = sys.argv[1]

class AutomaticReconstruction():
    def __init__(self, path, path_volume_rendering, input_analysis):
        
        # Paramters
        self.path = path
        self.path_volume_rendering = path_volume_rendering
        self.input_analysis = input_analysis
        
        # Default
        self.file_names = [
            'label_10_vena_cava.stl', 'label_11_auricle.stl', 'label_12_coronary_artery.stl', 
            'label_2_left_ventricle.stl', 'label_3_right_ventricle.stl', 'label_4_left_atrium.stl', 
            'label_5_right_atrium.stl', 'label_6_myocardium.stl', 'label_7_descending_aorta.stl' , 
            'label_8_pulmonary_trunk.stl', 'label_9_ascending_aorta.stl'
        ]
        
        self.raw_names = [
            f'ct_{specified_data}_label_10.nii.gz', f'ct_{specified_data}_label_11.nii.gz',
            f'ct_{specified_data}_label_12.nii.gz', f'ct_{specified_data}_label_2.nii.gz',
            f'ct_{specified_data}_label_3.nii.gz', f'ct_{specified_data}_label_4.nii.gz',
            f'ct_{specified_data}_label_5.nii.gz', f'ct_{specified_data}_label_6.nii.gz',
            f'ct_{specified_data}_label_7.nii.gz', f'ct_{specified_data}_label_8.nii.gz',
            f'ct_{specified_data}_label_9.nii.gz'
        ]

        self.classes_vn = [
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
            'Động mạch chủ dưới',
        ]
        
        self.classes = [
            'Vena Cava', 
            'Auricle', 
            'Coronary Artery', 
            'Left Ventricle', 
            'Right Ventricle', 
            'Left Atrium', 
            'Right Atrium', 
            'Myocardium', 
            'Ascending Aorta', 
            'Pulmonary Trunk', 
            'Descending Aorta',
        ]

        self.mapping = {
            self.path + 'label_10_vena_cava.stl': 0,
            self.path + 'label_11_auricle.stl': 1,
            self.path + 'label_12_coronary_artery.stl': 2,
            self.path + 'label_2_left_ventricle.stl': 3,
            self.path + 'label_3_right_ventricle.stl': 4,
            self.path + 'label_4_left_atrium.stl': 5,
            self.path + 'label_5_right_atrium.stl': 6,
            self.path + 'label_6_myocardium.stl': 7,
            self.path + 'label_7_descending_aorta.stl': 8,
            self.path + 'label_8_pulmonary_trunk.stl': 9,
            self.path + 'label_9_ascending_aorta.stl': 10,
        }
        
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
        
        # Variables
        sy, sx, dx = 0.15, 0.12, 0.01
        self.meshes = []
        self.vol_txt = []
        self.area_txt = []
        self.vola = []
        self.buttons = []
        self.list_points = set()
        self.pixel_spacing = 0.0858
        self.scaling_factor = 200/600 * (1/15)
        self.MAINFONT = 'C:/Windows/Fonts/Arial.ttf' 
        self.TITLE_FONT = 'c:/USERS/ADMIN/APPDATA/LOCAL/MICROSOFT/WINDOWS/FONTS/HELVETICA-NEUE-CONDENSED-BOLD.TTF'
        self.cur_volume = 0
        self.cur_area = 0
        self.color_dark = ''
        self.color_light = ''
        self.color_avg = ''
        self.cur_object = None
        self.cur_object_id = None
        self.enable_sphere = False
        
        # colors
        self.color_1 = '#242424'
        self.color_2 = '#3b3b3b'
        self.color_3 = '#565b5e'
        self.color_4 = '#565b5e'
        self.color_5 = '#111111'
        self.color_6 = '#ffffff'
        self.color_btn = '#1f6aa5'
        self.screen_color = '#00EA94'
        self.green_color = '#097d52'
        self.yellow_color = '#cee603'
        self.red_color = '#601124'
    
        # Functions
        self.load_patient_info()
        self.plotter_control(sy, sx, dx)
        self.reconstruction()
        self.initialize()
        self.show_mesh()
        self.slider()
        self.plt.at(26).show(self.title, self.function_description)
        self.plt.at(1).show(self.meshes, self.bbox, self.volume_main_display, self.area_main_display, self.info, self.sphere_txt)
        self.plt.interactive().close()
        
    def load_patient_info(self):
        with open(f'D:/Documents/GitHub/VascuIAR/DeepLearning/data/VnRawData/VHSCDD_raw_data/VHSCDD_{specified_data}_image/dict_info.json', 'r') as file:
            self.info_patient_dict = json.load(file)
        
    def reconstruction(self):
        for i in range(0,11,1):
            img_raw = sitk.ReadImage(self.path + self.raw_names[i], sitk.sitkFloat32)
            img = sitk.GetArrayFromImage(img_raw)
            img = resize(img, (150, 150, 150), anti_aliasing=False)

            vertices, faces, normals, values = marching_cubes(img)
            obj = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
            for index, face in enumerate(faces):
                obj.vectors[index] = vertices[face]
            obj.save(self.file_names[i])
            
    
    def plotter_control(self, sy, sx, dx):
        self.shape = [
            dict(bottomleft=(0,0),              topright=(1,1), bg=self.color_1),           # the full empty window -> 0
            dict(bottomleft=(dx*2+sx*2.5,0.01), topright=(1-dx,1-dx), bg=self.color_5),      # the display window -> 1
            
            dict(bottomleft=(dx,dx),         topright=(dx+sx*0.5,sy*0.8), bg=self.color_5),   # 2
            dict(bottomleft=(dx,sy*1.1*0.8), topright=(dx+sx*0.5,sy*0.8*2), bg=self.color_5), # 3
            dict(bottomleft=(dx,sy*2.1*0.8), topright=(dx+sx*0.5,sy*0.8*3), bg=self.color_5), # 4
            dict(bottomleft=(dx,sy*3.1*0.8), topright=(dx+sx*0.5,sy*0.8*4), bg=self.color_5), # 5
            dict(bottomleft=(dx,sy*4.1*0.8), topright=(dx+sx*0.5,sy*0.8*5), bg=self.color_5), # 6
            dict(bottomleft=(dx,sy*5.1*0.8), topright=(dx+sx*0.5,sy*0.8*6), bg=self.color_5), # 7
            
            dict(bottomleft=(dx+sx*1.26,dx),         topright=(dx+sx*1.75,sy*0.8), bg=self.color_5),    # 8
            dict(bottomleft=(dx+sx*1.26,sy*1.1*0.8), topright=(dx+sx*1.75,sy*2*0.8), bg=self.color_5),  # 9
            dict(bottomleft=(dx+sx*1.26,sy*2.1*0.8), topright=(dx+sx*1.75,sy*3*0.8), bg=self.color_5),  # 10
            dict(bottomleft=(dx+sx*1.26,sy*3.1*0.8), topright=(dx+sx*1.75,sy*4*0.8), bg=self.color_5),  # 11
            dict(bottomleft=(dx+sx*1.26,sy*4.1*0.8), topright=(dx+sx*1.75,sy*5*0.8), bg=self.color_5),  # 12
            dict(bottomleft=(dx+sx*1.26,sy*5.1*0.8), topright=(dx+sx*1.75,sy*6*0.8), bg=self.color_5),  # 13
            
            dict(bottomleft=(dx+sx*0.505,dx),         topright=(dx+sx*1.25,sy*0.8), bg=self.color_2),   # 14 
            dict(bottomleft=(dx+sx*0.505,sy*1.1*0.8), topright=(dx+sx*1.25,sy*0.8*2), bg=self.color_2), # 15
            dict(bottomleft=(dx+sx*0.505,sy*2.1*0.8), topright=(dx+sx*1.25,sy*0.8*3), bg=self.color_2), # 16
            dict(bottomleft=(dx+sx*0.505,sy*3.1*0.8), topright=(dx+sx*1.25,sy*0.8*4), bg=self.color_2), # 17
            dict(bottomleft=(dx+sx*0.505,sy*4.1*0.8), topright=(dx+sx*1.25,sy*0.8*5), bg=self.color_2), # 18 
            dict(bottomleft=(dx+sx*0.505,sy*5.1*0.8), topright=(dx+sx*1.25,sy*0.8*6), bg=self.color_2), # 19
            
            dict(bottomleft=(dx+sx*1.755,dx),         topright=(dx+sx*2.52,sy*0.8), bg=self.color_2),   # 20
            dict(bottomleft=(dx+sx*1.755,sy*1.1*0.8), topright=(dx+sx*2.52,sy*2*0.8), bg=self.color_2), # 21
            dict(bottomleft=(dx+sx*1.755,sy*2.1*0.8), topright=(dx+sx*2.52,sy*3*0.8), bg=self.color_2), # 22
            dict(bottomleft=(dx+sx*1.755,sy*3.1*0.8), topright=(dx+sx*2.52,sy*4*0.8), bg=self.color_2), # 23
            dict(bottomleft=(dx+sx*1.755,sy*4.1*0.8), topright=(dx+sx*2.52,sy*5*0.8), bg=self.color_2), # 24
            dict(bottomleft=(dx+sx*1.755,sy*5.1*0.8), topright=(dx+sx*2.52,sy*6*0.8), bg=self.color_2), # 25
            
            dict(bottomleft=(dx,sy*0.8*6.1), topright=(dx+sx*2.52, 1-dx), bg=self.color_1), # 26
        ]
    
        self.plt = Plotter(shape=self.shape, sharecam=False, size=(2000, 1200))
        self.plt.add_callback("RightButtonPress", self.change_object)
        self.plt.add_callback("MiddleButtonPress", self.add_object)
     
    def initialize(self):
        length = random.uniform(200 * 0.8, 200 * 1.2)
        width = random.uniform(200 * 0.8, 200 * 1.2)
        height = random.uniform(200 * 0.8, 200 * 1.2)
        pos_x = -200 + random.uniform(-20, 20)
        pos_y = -250 + random.uniform(-20, 20)
        pos_z = 250 + random.uniform(-20, 20)
        
        self.bbox = Box(pos=(pos_x, pos_y, pos_z), length=length, width=width, height=height, alpha=0)
        self.whole_mesh = load(self.path + 'whole.stl')
        self.whole_volume = self.whole_mesh.volume()
        self.whole_area = self.whole_mesh.area()
        self.volume_main_display = Text2D(f'Volume nguyên khối: {self.convert_vol(self.whole_volume)} ml', pos=(0.02, 0.97), c=self.color_6, bg=self.screen_color, s=0.8, font=self.MAINFONT)
        self.area_main_display = Text2D(f'Diện tích bề mặt: {self.convert_area(self.whole_area)} cm2', pos=(0.02,0.93), c=self.color_6, bg=self.screen_color, s=0.8, font=self.MAINFONT)
        self.segment_display = Text2D(pos=(0.02,0.90), c=self.color_6, s=0.8, font=self.MAINFONT)
        self.sphere_txt = Text2D(pos=(0.82, 0.15), c=self.screen_color, s=0.8, font=self.MAINFONT)
        func_des = """        
            The 3D post-reconstruction analysis functions allow for
            measurements of cardiac volumes, coronary artery diameters 
            (to identify artery stenosis), wall thickness of myocardium 
            (for tetralogy of Fallot) with high accuracy.

            Other functions include: 
            - Color mapping of individual components, 
            - Slicing & dissecting of cardiac structures
            - Localization of anomalies with 3D bounding box.
        """
        self.function_description = Text2D(func_des, pos=(0, 0.9), s=0.8, c=self.color_6, font=self.MAINFONT)
        
        self.title = Text2D('VasculAR - 3D Reconstruction & Post-analysis', s=1.28, c=self.color_6, font=self.TITLE_FONT)
        self.bbox_button = self.plt.at(26).add_button(
            self.toggle_bbox,
            pos=(0.16, 0.1),                                                                  
            states=['Disable Bounding Box', 'Enable Bounding Box'],                    
            c=["w", "w"],                                                                             
            bc=[self.green_color, self.color_btn],                                                                       
            font=self.MAINFONT,                                                       
            size=15,                                                                                   
            bold=True,                                                                                                       
            angle=0.3,
        )
        self.iso_button = self.plt.at(26).add_button(
            self.isosurface,
            pos=(0.42, 0.1),                                                                  
            states=['Isosurface', 'Isosurface'],
            c=["w", "w"], 
            bc=[self.color_btn, self.green_color],  
            font=self.MAINFONT,  
            size=15,     
            bold=True,
        )
        self.reset_button = self.plt.at(26).add_button(
            self.reset_meshes,
            pos=(0.6, 0.1),                                                                  
            states=['Reset 3D', 'Reset 3D'],
            c=["w", "w"], 
            bc=[self.color_btn, self.green_color],  
            font=self.MAINFONT,  
            size=15,     
            bold=True,
        )
        
        self.slicing_button = self.plt.at(26).add_button(
            self.slicing,
            pos=(0.76, 0.1),                                                                  
            states=['Slicing', 'Slicing'],
            c=["w", "w"], 
            bc=[self.color_btn, self.green_color],  
            font=self.MAINFONT,  
            size=15,     
            bold=True,
        )
        
        self.spline_button = self.plt.at(26).add_button(
            self.spline,
            pos=(0.9, 0.1),     
            states=['Splining', 'Splining'],
            c=["w", "w"], 
            bc=[self.color_btn, self.green_color],  
            font=self.MAINFONT,  
            size=15,     
            bold=True,
        )
        
        self.sphere_button = self.plt.at(25).add_button(
            self.start_hovering,
            pos=(0.4, 0.7),     
            states=['Sphere on', 'Sphere on'],
            c=["w", "w"], 
            bc=[self.color_btn, self.color_btn],  
            font=self.MAINFONT,  
            size=15,     
            bold=True,
        )
        
        self.sphere_button = self.plt.at(25).add_button(
            self.end_hovering,
            pos=(0.4, 0.4),     
            states=['Sphere off', 'Sphere off'],
            c=["w", "w"], 
            bc=[self.color_btn, self.color_btn],  
            font=self.MAINFONT,  
            size=15,     
            bold=True,
        )
        
        self.sync_database = self.plt.at(1).add_button(
            self.syncing_database,
            pos=(0.5,0.95),
            states=['Cloud Database Synchronization', 'Cloud Database Synchronization'],
            c=["w", "w"], 
            bc=[self.red_color, self.color_btn],  
            font=self.TITLE_FONT,  
            size=15,     
            bold=True,
        )
        
        self.info_patient = f"""
            Organization: {self.info_patient_dict['Organization']}
            Patient's name: Anonymous,
            Modality: {self.info_patient_dict["Modality"]}
            ID Patient: Anonymous,
            Examined part: {self.info_patient_dict["Body Part Examined"]}
            Date: {self.info_patient_dict["Acquisition Date"]}
        """
        self.info = Text2D(self.info_patient, pos=('top-right'), font=self.MAINFONT, s=0.7, c=self.screen_color)
        
        
    def start_hovering(self, evt, num):
        if (self.enable_sphere == True): return
        self.enable_sphere = True
        print(self.enable_sphere)
        self.sphere_callback = self.plt.at(1).add_callback('mouse hover', self.sphere)
        self.sphere_button.switch()
        
    def end_hovering(self, evt, num):
        if (self.enable_sphere == False): return
        self.enable_sphere = False
        print(self.enable_sphere)
        self.plt.at(1).remove_callback(self.sphere_callback)
        self.sphere_button.switch()
        return
        
    def sphere(self, evt):  
        if self.enable_sphere==False: return 
        p = evt.picked3d
        if p is None: return
        pts = Points(self.cur_object.closest_point(p, n=50), r=6)
        sph = fit_sphere(pts).alpha(0.1).pickable(False)
        pts.name = "mypoints"
        sph.name = "mysphere"
        self.sphere_txt.text(f'Diameter: {self.convert_dis(sph.radius)*2} mm \nRadius: {self.convert_dis(sph.radius)} mm \nResidue: {self.convert_dis(sph.residue)}')
        self.plt.at(1).remove("mypoints", "mysphere").add(pts, sph).render()
        
    def spline(self, evt, num):
        self.plt_splining = SplinePlotter(self.cur_object)
        self.plt_splining.show(bg=self.color_5)
        if self.plt_splining.line:
            print("Npts =", len(self.plt_splining.cpoints), "NSpline =", self.plt_splining.line.npoints)
        
    def slicing(self, evt, num):
        self.plt_slicing = FreeHandCutPlotter(self.cur_object)
        self.plt_slicing.add_hover_legend()
        self.plt_slicing.start(bg=self.color_5)
    
    def reset_meshes(self, evt, num):
        self.plt.at(1).clear().add(self.meshes, self.bbox, self.volume_main_display, self.area_main_display, self.info)
        self.plt.at(1).remove_callback(self.temp)
        
    def change_object(self, evt):
        if not evt.object: return
        self.cur_object = evt.object
        self.cur_object_id = self.mapping[evt.object.filename]
        self.cur_volume = self.vola[self.cur_object_id][0]
        self.cur_area = self.vola[self.cur_object_id][1]
        
        self.segment_display.text(f'Region: {self.classes[self.cur_object_id]}')
        self.volume_main_display.text(f'Volume: {round(self.cur_volume,3)} ml')
        self.area_main_display.text(f'Surface area: {round(self.cur_area,3)} cm2')
        self.plt.at(1).clear().add(evt.object, self.bbox, self.segment_display, self.volume_main_display, self.area_main_display, self.info)
        self.temp = self.plt.at(1).add_callback("LeftButtonPress", self.select_vertices)
        self.plt.at(1).add_callback("KeyPress", self.control_direction)
        
    def convert_vol(self, vol):
        return round(vol * self.pixel_spacing**3 * self.scaling_factor, 3)

    def convert_area(self, area):
        return round(area * self.pixel_spacing**2 * self.scaling_factor, 3)
    
    def convert_dis(self, dis):
        return round(dis * self.pixel_spacing * self.scaling_factor * 10, 5)
        
    def add_object(self, evt):
        if not evt.object: return
        index_object = self.mapping[evt.object.filename]
        self.cur_volume += self.vola[index_object][0]
        self.cur_area += self.vola[index_object][1]
        
        self.segment_display.text('')
        self.volume_main_display.text(f'Total Volume: {round(self.cur_volume,3)} ml')
        self.area_main_display.text(f'Total Surface Area: {round(self.cur_area,3)} cm2')
        self.plt.at(1).add(evt.object, self.bbox, self.segment_display, self.volume_main_display, self.area_main_display, self.info)
        
    def distort(self, direction):
        distorted_vertices = self.cur_object.vertices 
        vel=5
        for idx_vert in self.list_points:
            self.cur_object.vertices[idx_vert] += (np.array([vel,vel,vel]) * np.array(direction)).tolist()
            vel -= 0.05
                
        self.cur_object = Mesh([distorted_vertices, self.cur_object.cells])
        self.volume_main_display.text(f'Volume: {self.convert_vol(self.cur_object.volume())} ml')
        self.area_main_display.text(f'Surface area: {self.convert_area(self.cur_object.area())} cm2')
        self.plt.at(1).clear().add(self.cur_object.texture(f'textures/{self.textures[self.cur_object_id]}'), self.bbox, self.volume_main_display, self.area_main_display, self.info)
        
        
    def select_vertices(self, evt):
        picked = evt.picked3d
        if picked is not None and evt.object is not None:
            for i in range(100):
                vertex_id = self.cur_object.closest_point(picked, return_point_id=True)
                if (vertex_id > len(self.cur_object.vertices)): continue
                self.list_points.add(vertex_id)
                picked[0] += 2
                
    def control_direction(self, evt):
        key_pressed = evt.keypress
        if len(self.list_points) != 0:
            if (key_pressed == 't'):
                self.distort([0,1,0])
            if (key_pressed == 'r'):
                self.distort([1,1,0])
            if (key_pressed == 'f'):
                self.distort([1,0,0])
            if (key_pressed == 'v'):
                self.distort([-1,-1,0])
            if (key_pressed == 'b'):
                self.distort([0,-1,0])
            if (key_pressed == 'n'):
                self.distort([0,-1,-1])
            if (key_pressed == 'h'):
                self.distort([-1,0,0])
            if (key_pressed == 'y'):
                self.distort([1,1,0])
            if (key_pressed == 'g'):
                self.list_points.clear()
    
    def load_mesh(self, index):
        mesh = load(self.path + self.file_names[index])
        mesh.texture(f'textures/{self.textures[index]}')
        return mesh
    
    def toggle_bbox(self, evt, num):
        if (self.bbox.alpha() > 0):
            self.bbox.alpha(0)
        else:
            self.bbox.alpha(0.3)    
        self.bbox_button.switch()
        
    def buttonfunc(self, idx, bu):
        self.meshes[idx].alpha(1 - self.meshes[idx].alpha())  
        bu.switch()   
    
    def show_mesh(self):
        for index in tqdm(range(2,13)):
            idx = index-2
            self.meshes.append(self.load_mesh(idx))
            self.vola.append([self.convert_vol(self.meshes[idx].volume()), self.convert_area(self.meshes[idx].area())])
            
            self.name = Text2D(f'{idx+1}. {self.classes[idx]}', s=0.78, pos=(0.05, 0.9), font=self.TITLE_FONT, c=self.color_6, bg=self.color_4)
            self.vol_txt.append(Text2D(f'Volume: {self.vola[idx][0]} ml', s=0.7, pos=(0.05, 0.5), font=self.MAINFONT, c=self.color_6))
            self.area_txt.append(Text2D(f'Surface area: {self.vola[idx][1]} cm2', s=0.7, pos=(0.05, 0.3), font=self.MAINFONT, c=self.color_6))
            
            button = self.plt.at(1).add_button(
                lambda obj, ename, idx=idx: self.buttonfunc(idx, self.buttons[idx]),
                pos=(0.05, 0.4 - idx * 0.035),                                                                  
                states=[f'{str(idx+1)}. view', f'{str(idx+1)}. close'],                    
                c=["w", "w"],                                                                             
                bc=[self.color_btn, self.screen_color],                                                                       
                font=self.MAINFONT,                                                       
                size=15,                                                                                   
                bold=True,
                angle=0.3,
            )
            self.buttons.append(button)  

            self.plt.at(index).show(self.meshes[idx])
            self.plt.at(index + 12).show(self.name, self.vol_txt[idx], self.area_txt[idx])
            
            
    def syncing_database(self, evt, num):
        print(specified_data)
        venv_activate_script = os.path.join('D:/Documents/GitHub/VascuIAR/.venv/Scripts', 'activate')
        if sys.platform.startswith('win'):
            activation_command = f"call {venv_activate_script}"
            start_command = "start"
        else:
            activation_command = f"source {venv_activate_script}"
            start_command = "x-terminal-emulator -e"

        command = f"{activation_command} && {start_command} python stl_to_cloud.py {specified_data}"
        subprocess.run(command, shell=True)
            
    def isosurface(self, obj, num):
        plt2 = Plotter()
        nifti_image = sitk.ReadImage(self.path_volume_rendering)
        array=sitk.GetArrayFromImage(nifti_image)
        volume = Volume(array) 

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

        isovals = volume.properties.GetIsoSurfaceValues()
        isovals.SetValue(0, isovalue)

        plt2.add(volume.mode(5).alpha(1).cmap('copper'))

        plt2.add_slider(
            slider_isovalue,
            scrange[0] + 0.02 * delta,
            scrange[1] - 0.02 * delta,
            value=isovalue,
            pos=2,
            title="Isosurface non-region-based reconstruction",
            font= self.MAINFONT,
            show_value=True,
            delayed=False,
        )
            
        plt2.show(axes=0, bg='black').close()
        
    def slider(self):
        def slider1(widget, event):
            if self.cur_object is None: return
            self.cur_object.color(widget.value)
        
        self.plt.at(1).add_slider(    
            slider1,
            xmin=-9,
            xmax=1,
            value=0,
            pos=[(0.55,0.023), (0.65,0.023)],
            title="Change color",
        )
        
    
# specified_data = 1
isinstance = AutomaticReconstruction(
    path=f'D:/Documents/GitHub/VascuIAR/DeepLearning/data/VnRawData/VHSCDD_sep_labels/VHSCDD_{specified_data}_label/',
    path_volume_rendering= f'D:/Documents/GitHub/VascuIAR/DeepLearning/data/VnRawData/VHSCDD_raw_data/VHSCDD_{specified_data}_image/ct_{specified_data}_image.nii.gz',
    input_analysis = '',
)