'''
VasculAR software
Author: Nguyen Le Quoc Bao
Version: 0.2
Competition: Visef & Isef
'''

import customtkinter
import tkinter
from tkinter import filedialog, Canvas
from CTkRangeSlider import *
from CTkColorPicker import *
from NoteAnalysis import NoteWindow 
from filtering_segmentation import filtering
from pdf_save import create_pdf
from draw import draw_canvas
from PIL import Image, ImageTk, ImageGrab
import SimpleITK as sitk
from readdcm import ReadDCM
import cv2
import numpy as np
import matplotlib.pyplot as plt
import webbrowser
from cloud_database import LoginPage
import pyrebase
import os

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

firebaseConfig = {
    'apiKey': "AIzaSyCoG09bln3Qrmws87pxnNak-dLC58wCeWE",
    'authDomain': "vascular-68223.firebaseapp.com",
    'databaseURL': "https://vascular-68223-default-rtdb.asia-southeast1.firebasedatabase.app",
    'projectId': "vascular-68223",
    'storageBucket': "vascular-68223.appspot.com",
    'messagingSenderId': "1068291063816",
    'appId': "1:1068291063816:web:a1c19e8d2bd465cf7c91bd",
    'measurementId': "G-27VPL4BB1D"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()

class AboutWindow(customtkinter.CTkToplevel):
    def __init__(self, parent, title):
        super().__init__()
        self.title(title)
        self.transient(parent)
        self.width = int(self.winfo_screenwidth()/3.5)
        self.height = int(self.winfo_screenheight()/3)
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)
        self.iconbitmap('imgs/logo.ico')
        self.protocol("WM_DELETE_WINDOW", self.close_toplevel)
        self.font = customtkinter.ThemeManager.theme["CTkFont"]["family"]
        
        self.frame = customtkinter.CTkFrame(master=self)
        self.frame.pack(expand=True, fill="both", padx=10, pady=10)
        
    def close_toplevel(self):
        self.destroy()
    
class MenuBar:
    def __init__(self, master):
        self.master = master
        self.current_menu = None
        
        self.data = {
            'File': {
                'main_menu': {
                    'instance_name': 'file_btn',
                    'label_name': 'File'
                },
                'sub_menu': {
                    'add_nifti_file_btn': 'Add Nifti file',
                    'add_dcm_series_btn': 'Add Segmentation',
                    'save_case_btn': 'Save case',
                    'export_analysis_btn': 'Export analysis',
                }
            },
            'Setting': {
                'main_menu':{
                    'instance_name': 'setting_btn',
                    'label_name': 'Setting'
                }, 
                'sub_menu': {
                    'theme_setting_btn': 'Theme color',
                    'language_setting_btn': 'Language',
                },
                'sub_menu_2': {
                    'theme_setting_btn': {
                        'dark_theme_btn': 'Dark theme',
                        'light_theme_btn': 'Light theme',
                        },
                    'language_setting_btn': {
                        'eng_btn': 'English',
                        'vn_btn': 'Vietnamese',
                    }  
                }         
            },
            'Help': {
                'main_menu': {
                    'instance_name': 'help_btn',
                    'label_name': 'Help'
                },
                'sub_menu': {
                    'basic_functions_btn': 'Basic functions',
                    'defect_dectection_btn': 'Defect detection',
                    'reconstruction_btn': '3D reconstruction',
                    'connection_btn': 'VR & AR connection'
                }
            },
            'About': {
                'main_menu': {
                    'instance_name': 'about_btn',
                    'label_name': 'About', 
                }
            },
            'Account': {
                'main_menu': {
                    'instance_name': 'account_btn',
                    'label_name': 'Account',  
                }
            }
        }
        
        self.menu_item = {'main_menu':{}, 'sub_menu': {}, 'sub_menu_2':{}}
        
        self.create_widget()
        self.layout_widget()
        
    def sub_dropdown_frame(self, widget, row):
        x = self.dropdown.winfo_x() + widget.cget('width')
        y = self.dropdown.winfo_y() + (widget.cget('height') + 5) * row
        instance = widget.cget("text")
        self.menu_item['sub_menu_2'][instance] = customtkinter.CTkFrame(master=self.master)
        self.menu_item['sub_menu_2'][instance].place(x=x,y=y)
        self.menu_item['sub_menu_2'][instance].bind('<Leave>', lambda event : self.menu_item['sub_menu_2'][instance].place_forget())


        print(instance)
        if instance == 'Language':
            self.eng_btn = customtkinter.CTkButton(
                master=self.menu_item['sub_menu_2'][instance],
                text=self.data['Setting']['sub_menu_2']['language_setting_btn']['eng_btn'],
                fg_color='transparent', 
                hover_color=self.master.second_color,
            )
            
            self.eng_btn.pack(padx=5, pady=5)
            self.eng_btn.configure(anchor="w")
            
            self.vn_btn = customtkinter.CTkButton(
                master=self.menu_item['sub_menu_2'][instance],
                text=self.data['Setting']['sub_menu_2']['language_setting_btn']['vn_btn'],
                fg_color='transparent', 
                hover_color=self.master.second_color,
            )
            
            self.vn_btn.pack(padx=5, pady=5)
            self.vn_btn.configure(anchor="w")
            
        if instance == 'Theme color':
            self.eng_btn = customtkinter.CTkButton(
                master=self.menu_item['sub_menu_2'][instance],
                text=self.data['Setting']['sub_menu_2']['theme_setting_btn']['dark_theme_btn'],
                fg_color='transparent', 
                hover_color=self.master.second_color,
            )
            
            self.eng_btn.pack(padx=5, pady=5)
            self.eng_btn.configure(anchor="w")
            
            self.vn_btn = customtkinter.CTkButton(
                master=self.menu_item['sub_menu_2'][instance],
                text=self.data['Setting']['sub_menu_2']['theme_setting_btn']['light_theme_btn'],
                fg_color='transparent', 
                hover_color=self.master.second_color,
            )
            
            self.vn_btn.pack(padx=5, pady=5)
            self.vn_btn.configure(anchor="w")
            
    def choose_file_seg(self):
        self.master.path_seg = filedialog.askopenfilename()
        
        if self.master.path_seg.endswith('.nii.gz') or self.master.path_seg.endswith('.nii'):
            self.master.seg_raw = sitk.ReadImage(self.master.path_seg, sitk.sitkFloat32)
            self.master.seg = sitk.GetArrayFromImage(self.master.seg_raw)
            self.master.add_seg = True
        else:
            print("Error for segmentation uploading")
            
        self.hide_all_menu()
        self.master.event_generate("<<UpdateApp2>>")
            
    def choose_file(self):
        self.master.path = filedialog.askopenfilename()
        
        if self.master.path.endswith('.nii.gz') or self.master.path.endswith('.nii'):
            self.master.img_raw = sitk.ReadImage(self.master.path, sitk.sitkFloat32)
            self.master.img = sitk.GetArrayFromImage(self.master.img_raw)
        
        elif self.master.path.endswith('.dcm'):
            parent_dir = os.path.dirname(self.master.path)
            instance = ReadDCM(parent_dir)
            self.master.img_raw, self.master.img, self.master.dict_info, self.master.pixel_spacing = instance.read_file_dcm()
            print(self.master.dict_info)
            
        self.hide_all_menu()
        self.master.event_generate("<<UpdateApp>>")
        
    def export_analysis(self):
        print(self.master.analysis_data)
        create_pdf(package=self.master.analysis_data)
    
        
    def dropdown_options(self, instance, master):            
        for row, (instance_name, label_name) in enumerate(self.data[instance]['sub_menu'].items()):
            if instance_name == 'add_dcm_series_btn':
                print("seg_btn")
                self.menu_item['sub_menu'][instance_name] = customtkinter.CTkButton(
                    master=master, 
                    text=label_name,
                    fg_color='transparent', 
                    hover_color=self.master.second_color,
                    command = lambda: self.choose_file_seg(),
                )
            elif instance_name == 'add_nifti_file_btn': 
                self.menu_item['sub_menu'][instance_name] = customtkinter.CTkButton(
                    master=master, 
                    text=label_name,
                    fg_color='transparent', 
                    hover_color=self.master.second_color,
                    command = lambda: self.choose_file(),
                )
                
            elif instance_name == 'export_analysis_btn':
                self.menu_item['sub_menu'][instance_name] = customtkinter.CTkButton(
                    master=master, 
                    text=label_name,
                    fg_color='transparent', 
                    hover_color=self.master.second_color,
                    command = lambda: self.export_analysis(),
                )
            else:
                self.menu_item['sub_menu'][instance_name] = customtkinter.CTkButton(
                    master=master, 
                    text=label_name,
                    fg_color='transparent', 
                    hover_color=self.master.second_color,
                )
            self.menu_item['sub_menu'][instance_name].pack(padx=5, pady=5)
            self.menu_item['sub_menu'][instance_name].configure(anchor="w")
            

    def dropdown_frame(self, widget_option, col):
        self.hide_all_menu()
        if widget_option.cget("text") != 'About' and widget_option.cget("text") != 'Account':
            self.dropdown = customtkinter.CTkFrame(master=self.master)
            x = widget_option.winfo_x() - col
            self.dropdown.place(
                x=x,
                y=30
            )
            self.current_menu = self.dropdown
            if widget_option.cget("text") == 'File':
                self.dropdown_options(
                    instance=widget_option.cget("text"), 
                    master=self.dropdown
                )
                
            elif widget_option.cget("text") == 'Setting':
                self.dropdown_options(
                    instance=widget_option.cget("text"),
                    master=self.dropdown
                )
                self.menu_item['sub_menu']['theme_setting_btn'].bind('<Button-1>', lambda event :self.sub_dropdown_frame(widget=self.menu_item['sub_menu']['theme_setting_btn'], row=0))
                self.menu_item['sub_menu']['language_setting_btn'].bind('<Button-1>', lambda event :self.sub_dropdown_frame(widget=self.menu_item['sub_menu']['language_setting_btn'], row=1))

            elif widget_option.cget("text") == 'Help':
                self.dropdown_options(
                    instance=widget_option.cget("text"),
                    master=self.dropdown
                )

        
        elif widget_option.cget("text") == 'About':
            self.about_window = AboutWindow(
                parent=self.master,
                title='About VasculAR Software',
            )
            
        elif widget_option.cget("text") == 'Account':
            self.login_page = LoginPage(
                parent=self.master,
                title='VasculAR account login',
                auth=auth
            ) 
        
    def hide_all_menu(self):         
        if self.current_menu:
            self.current_menu.place_forget()
            self.current_menu = None

    
    def create_widget(self):
        self.current_menu = None
        self.menu_frame = customtkinter.CTkFrame(master=self.master, fg_color='transparent')
        self.menu_frame.grid(row=0, column=0, columnspan=15, sticky='w')
        self.menu_frame.rowconfigure((0, 1, 2), weight=1, uniform='a')
        
        col=0
        for menu_name, menu_data in self.data.items():
            instance_name = menu_data['main_menu']['instance_name'] 
            self.menu_item['main_menu'][instance_name] = customtkinter.CTkButton(
                master=self.menu_frame,
                text=menu_data['main_menu']['label_name'],
                fg_color='transparent',
                width=10,
                command=lambda instance_name=instance_name, col=col: self.dropdown_frame(widget_option=self.menu_item['main_menu'][instance_name], col=col)
            )
            col += 1
        
        self.master.bind("<Double-Button-1>", lambda event: self.hide_all_menu())
        
        
    def layout_widget(self):
        col=0
        for menu_name, menu_data in self.data.items():
            instance_name = menu_data['main_menu']['instance_name']
            self.menu_item['main_menu'][instance_name].grid(row=0, column=col, padx=(5, 0), sticky='w')
            col+=1
    
class ROI:
    def __init__(self, canvas_view, canvas_name, x1, y1, x2, y2):
        self.canvas_view = canvas_view
        self.canvas_name = canvas_name
        self.main_app = self.canvas_view.master
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.rec_width = self.x2 - self.x1
        self.rec_height = self.y2 - self.y1
        self.circle_width = 10
        self.circle_height = 10
        
        self.rect = self.canvas_view.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, outline='blue', width=5)
        self.nw_circle = self.canvas_view.canvas.create_oval(self.x1-self.circle_width, self.y1-self.circle_height, self.x1+self.circle_width, self.y1+self.circle_height, fill = "blue")
        self.ne_circle = self.canvas_view.canvas.create_oval(self.x1-self.circle_width+self.rec_width, self.y1-self.circle_height, self.x1+self.circle_width+self.rec_width, self.y1+self.circle_height, fill = "blue")
        self.sw_circle = self.canvas_view.canvas.create_oval(self.x1-self.circle_width, self.y1-self.circle_height+self.rec_height, self.x1+self.circle_width, self.y1+self.circle_height+self.rec_height, fill="blue")
        self.se_circle = self.canvas_view.canvas.create_oval(self.x1-self.circle_width+self.rec_width, self.y1-self.circle_height+self.rec_height, self.x1+self.circle_width+self.rec_width, self.y1+self.circle_height+self.rec_height, fill="blue")

        
        if self.canvas_view.master.tools.check_ROI.get() == "on":
            self.move_ne_corner()
            self.move_nw_corner()
            self.move_sw_corner()
            self.move_se_corner()
            
    def update_label(self):
        self.main_app.tools.axial_x1.set(f"x: {self.main_app.ROI_data['axial']['rec']['x1']}")
        self.main_app.tools.axial_y1.set(f"y: {self.main_app.ROI_data['axial']['rec']['y1']}")
        self.main_app.tools.axial_width.set(f"width: {self.main_app.ROI_data['axial']['rec']['x2'] - self.main_app.ROI_data['axial']['rec']['x1']}")
        self.main_app.tools.axial_height.set(f"height: {self.main_app.ROI_data['axial']['rec']['y2'] - self.main_app.ROI_data['axial']['rec']['y1']}")
        
        self.main_app.tools.sagittal_x1.set(f"x: {self.main_app.ROI_data['sagittal']['rec']['x1']}")
        self.main_app.tools.sagittal_y1.set(f"y: {self.main_app.ROI_data['sagittal']['rec']['y1']}")
        self.main_app.tools.sagittal_width.set(f"width: {self.main_app.ROI_data['sagittal']['rec']['x2'] - self.main_app.ROI_data['sagittal']['rec']['x1']}")
        self.main_app.tools.sagittal_height.set(f"height: {self.main_app.ROI_data['sagittal']['rec']['y2'] - self.main_app.ROI_data['sagittal']['rec']['y1']}")
        
        self.main_app.tools.coronal_x1.set(f"x: {self.main_app.ROI_data['coronal']['rec']['x1']}")
        self.main_app.tools.coronal_y1.set(f"y: {self.main_app.ROI_data['coronal']['rec']['y1']}")
        self.main_app.tools.coronal_width.set(f"width: {self.main_app.ROI_data['coronal']['rec']['x2'] - self.main_app.ROI_data['coronal']['rec']['x1']}")
        self.main_app.tools.coronal_height.set(f"height: {self.main_app.ROI_data['coronal']['rec']['y2'] - self.main_app.ROI_data['coronal']['rec']['y1']}")
        
        
    def update(self):
        self.update_label()
        self.rec_width = self.x2 - self.x1
        self.rec_height = self.y2 - self.y1
        self.canvas_view.canvas.coords(self.nw_circle, self.x1-self.circle_width, self.y1-self.circle_height, self.x1+self.circle_width, self.y1+self.circle_height)
        self.canvas_view.canvas.coords(self.ne_circle, self.x1-self.circle_width+self.rec_width, self.y1-self.circle_height, self.x1+self.circle_width+self.rec_width, self.y1+self.circle_height)
        self.canvas_view.canvas.coords(self.sw_circle, self.x1-self.circle_width, self.y1-self.circle_height+self.rec_height, self.x1+self.circle_width, self.y1+self.circle_height+self.rec_height)
        self.canvas_view.canvas.coords(self.se_circle, self.x1-self.circle_width+self.rec_width, self.y1-self.circle_height+self.rec_height, self.x1+self.circle_width+self.rec_width, self.y1+self.circle_height+self.rec_height)
    
    def move_ne_corner(self):
        def move(event):
            self.canvas_view.canvas.moveto(self.ne_circle, event.x-10, event.y-10)
            self.main_app.ROI_data[self.canvas_name]['ne']['x'] = event.x
            self.main_app.ROI_data[self.canvas_name]['ne']['y'] = event.y
            
            # update_rec
            self.canvas_view.canvas.coords(self.rect, self.x1, event.y, event.x, self.y2)
            self.main_app.ROI_data[self.canvas_name]['rec']['y1'] = event.y
            self.main_app.ROI_data[self.canvas_name]['rec']['x2'] = event.x
            
            self.y1 = event.y
            self.x2 = event.x
            
            self.update()
            
        self.canvas_view.canvas.tag_bind(self.ne_circle, '<Button1-Motion>', move)

        
    def move_nw_corner(self):
        def move(event):
            self.canvas_view.canvas.moveto(self.nw_circle, event.x-10, event.y-10)
            self.main_app.ROI_data[self.canvas_name]['nw']['x'] = event.x
            self.main_app.ROI_data[self.canvas_name]['nw']['y'] = event.y
            
            self.canvas_view.canvas.coords(self.rect, event.x, event.y, self.x2, self.y2)
            self.main_app.ROI_data[self.canvas_name]['rec']['x1'] = event.x
            self.main_app.ROI_data[self.canvas_name]['rec']['y1'] = event.y
            
            self.x1 = event.x
            self.y1 = event.y
            
            self.update()
            
        
        self.canvas_view.canvas.tag_bind(self.nw_circle, '<Button1-Motion>', move)
        
    def move_sw_corner(self):
        def move(event):
            self.canvas_view.canvas.moveto(self.sw_circle, event.x-10, event.y-10)
            self.main_app.ROI_data[self.canvas_name]['sw']['x'] = event.x
            self.main_app.ROI_data[self.canvas_name]['sw']['y'] = event.y
            
            self.canvas_view.canvas.coords(self.rect, event.x, self.y1, self.x2, event.y)
            self.main_app.ROI_data[self.canvas_name]['rec']['x1'] = event.x
            self.main_app.ROI_data[self.canvas_name]['rec']['y2'] = event.y
            
            self.x1 = event.x
            self.y2 = event.y
            
            self.update()
        
        self.canvas_view.canvas.tag_bind(self.sw_circle, '<Button1-Motion>', move)
        
    def move_se_corner(self):
        def move(event):
            self.canvas_view.canvas.moveto(self.se_circle, event.x-10, event.y-10)
            self.main_app.ROI_data[self.canvas_name]['se']['x'] = event.x
            self.main_app.ROI_data[self.canvas_name]['se']['y'] = event.y
            
            self.canvas_view.canvas.coords(self.rect, self.x1, self.y1,  event.x, event.y)
            self.main_app.ROI_data[self.canvas_name]['rec']['x2'] = event.x
            self.main_app.ROI_data[self.canvas_name]['rec']['y2'] = event.y
            
            self.x2 = event.x
            self.y2 = event.y
            
            self.update()
        
        self.canvas_view.canvas.tag_bind(self.se_circle, '<Button1-Motion>', move)


class CanvasAxial:
    def __init__(self, master):
        self.master = master
        self.create_frame()
        self.create_canvas()    
        self.create_tool_widgets()
        
    def save_canvas(self):
        # save into database
        index = self.master.analysis_data['number']
        for element, data in self.master.draw_data.items():
            
            print('cur_vol', int(round(self.slider_volume.get(), 0)))
            if element != 'number_of_elements' and data['slice'] == int(round(self.slider_volume.get(), 0)) and data['canvas'] == 'axial':
                print('data slice', data['slice'])
                print('equal')
                if (f'canvas_{index}.png' not in self.master.analysis_data):
                    self.master.analysis_data[f'canvas_{index}.png'] = {}
                self.master.analysis_data[f'canvas_{index}.png'][element] = data['note']
                print(self.master.analysis_data)

        # save file
        x = self.master.winfo_rootx() + self.canvas.winfo_x() + 7 
        y = self.master.winfo_rooty() + self.canvas.winfo_y() + 100 
        x1 = x + self.canvas.winfo_width()*1.255 
        y1 = y + self.canvas.winfo_height()*1.255  
        ImageGrab.grab().crop((x,y,x1,y1)).save(f"canvas_{index}.png")
        self.master.analysis_data['number'] = index + 1
    
    def create_tool_widgets(self):
        def rotation():
            def rotation_control():
                current_val = int(self.rotation_label.cget('text'))
                if current_val == 360:
                    current_val = 0
                self.rotation_label.configure(text=current_val+90)
             
            self.rotation_label = customtkinter.CTkLabel(master=self.frame, text="0") 
            icon = customtkinter.CTkImage(dark_image=Image.open("imgs/rotate.png"), size=(20, 20))
            self.rotation_btn = customtkinter.CTkButton(master=self.frame_tools, text="", image=icon, width=25, height=25, command=rotation_control)
            self.rotation_btn.grid(column=0, row=0, padx=5, sticky='w') 

        def flip_horizontal():
            def flip_control():
                cur_val = self.flip_horizontal_label.cget("text")
                if cur_val == "":  
                    self.flip_horizontal_label.configure(text="horizontal")
                else:
                    self.flip_horizontal_label.configure(text="")
                
            self.flip_horizontal_label = customtkinter.CTkLabel(master=self.frame, text="") 
            icon = customtkinter.CTkImage(dark_image=Image.open("imgs/flip_horizontal.png"), size=(20, 20))
            self.flip_horizontal_btn = customtkinter.CTkButton(master=self.frame_tools, text='', image=icon, width=25, height=25, command=flip_control)
            self.flip_horizontal_btn.grid(column=1, row=0, padx=5, sticky='w')  
            
        def flip_vertical():
            def flip_control():
                cur_val = self.flip_vertical_label.cget("text")
                if cur_val == "":
                    self.flip_vertical_label.configure(text="vertical")
                else:
                    self.flip_vertical_label.configure(text="")
                    
            self.flip_vertical_label = customtkinter.CTkLabel(master=self.frame, text="") 
            icon = customtkinter.CTkImage(dark_image=Image.open("imgs/flip_vertical.png"), size=(20, 20))
            self.flip_vertical_btn = customtkinter.CTkButton(master=self.frame_tools, text='', image=icon, width=25, height=25, command=flip_control)
            self.flip_vertical_btn.grid(column=2, row=0, padx=5, sticky='w')  
            
        def color_map():
            colors = ["gray", "bone", "nipy_spectral", "viridis", "plasma", "inferno", "magma", "cividis", "Greys", "Purples", "Blues", "Greens", "Reds", "YlOrBr", "YlOrRd", "OrRd", "PuRd", "GnBu"]
            self.color_map_default = customtkinter.StringVar(value="gray")
            self.color_map = customtkinter.CTkComboBox(self.frame_tools, values=colors, variable=self.color_map_default)
            self.color_map.grid(column=3, row=0, sticky='ew', padx=10)
            self.image_display(self.slider_volume.get())
            
        def save_photo():
            icon = customtkinter.CTkImage(dark_image=Image.open("imgs/save.png"), size=(20, 20))
            self.save_photo_btn = customtkinter.CTkButton(master=self.frame_tools, text='', image=icon, width=25, height=25, command=self.save_canvas)
            self.save_photo_btn.grid(row=0, column=4, padx=10, sticky='e')
            
        self.frame_tools = customtkinter.CTkFrame(master=self.master, fg_color='transparent')
        self.frame_tools.grid(column=3, row=0, columnspan=3, rowspan=1, pady=(35, 0), sticky='news')
        self.frame_tools.columnconfigure((0,1,2,3,4), weight=1)
        rotation()
        flip_horizontal()
        flip_vertical()
        color_map()
        save_photo()
        
    def create_frame(self):
        self.frame = customtkinter.CTkFrame(master=self.master, fg_color=self.master.second_color)
        self.frame.grid(row=1, column=0, rowspan=9, columnspan=6, padx=5, sticky='news')
        
        
    def image_display(self, index_slice):
        def create_crosshair():           
            def move_crosshair(event):
                x, y = event.x, event.y
                self.canvas.coords(self.horizontal_line, 0, y, self.canvas.winfo_width(), y)
                self.canvas.coords(self.vertical_line, x, 0, x, self.canvas.winfo_height())

            def on_mouse_press(event):
                if self.master.tools.check_ROI.get() == "off":
                    self.canvas.bind("<Motion>", move_crosshair)

            def on_mouse_release(event):
                if self.master.tools.check_ROI.get() == "off":
                    self.canvas.unbind("<Motion>")
            
            self.horizontal_line = self.canvas.create_line(0, self.canvas.winfo_height() // 2, self.canvas.winfo_width(), self.canvas.winfo_height() // 2, fill="red")
            self.vertical_line = self.canvas.create_line(self.canvas.winfo_width() // 2, 0, self.canvas.winfo_width() // 2, self.canvas.winfo_height(), fill="red")
            self.canvas.bind("<ButtonPress-1>", on_mouse_press)
            self.canvas.bind("<ButtonRelease-1>", on_mouse_release)       
            
        def image_position():
            try:
                image_position = self.canvas.coords(self.canvas_item)
                return image_position[0], image_position[1]
            except:
                return int(round(673/2,0)), int(round(673/2,0))
        def display_info():
            text_item = self.canvas.create_text(10, 20, text='AXIAL VIEW', anchor="w", fill=self.master.text_canvas_color)
            y = 40
            for k, v in self.master.dict_info.items():
                text_item = self.canvas.create_text(10, y, text=f'{k} : {v}', anchor="w", fill=self.master.text_canvas_color)
                y += 20
                   
        def display_drawings(zoom_ratio=0.1):
            for element, data in self.master.draw_data.items():
                if element != 'number_of_elements' and data['slice'] == int(round(self.slider_volume.get(), 0)) and data['canvas'] == 'axial':
                    if data['type'] == 'rectangle':
                        self.canvas.create_rectangle(data['x1'], data['y1'], data['x2'], data['y2'], outline=data['color'])
                        self.canvas.create_text((data['x2'] + data['x1'])/2, data['y1']-20, text=element, anchor="center", fill=data['color'])
                    elif data['type'] == 'circle':
                        self.canvas.create_oval(data['x1'], data['y1'], data['x2'], data['y2'], outline=data['color'])
                        self.canvas.create_text((data['x2'] + data['x1'])/2, data['y1']-20, text=element, anchor="center", fill=data['color'])
                    elif data['type'] == 'line':
                        self.canvas.create_line(data['x1'], data['y1'], data['x2'], data['y2'], fill=data['color'], width=3)
                        distance = int(round(((data['x2'] - data['x1'])**2 +  (data['y2'] - data['y1'])**2)**(1/2), 2))
                        self.canvas.create_text((data['x2'] + data['x1'])/2, data['y1']-20, text=f'{element} : {distance}mm', anchor="center", fill=data['color'])
        
                    if zoom_ratio > 0:
                        if data['y1'] < 673/2:
                            ratio = 673/2 - data['y1']
                            data['x1'] = data['x1'] - (zoom_ratio + 0.85 / ratio)
                            data['y1'] = data['y1'] - (zoom_ratio + 0.85 * 2)
                            data['x2'] = data['x2'] + (zoom_ratio + 0.85)
                            data['y2'] = data['y2'] + (zoom_ratio + 0.85 / ratio)
                            
                        if data['y1'] > 673/2:
                            ratio = data['y1'] - 673/2
                            data['x1'] = data['x1'] - (zoom_ratio + 0.85 / ratio)
                            data['y1'] = data['y1'] - (zoom_ratio + 0.85 * 2)
                            data['x2'] = data['x2'] + (zoom_ratio + 0.85)
                            data['y2'] = data['y2'] + (zoom_ratio + 0.85 / ratio)
                            
        self.images = [] 
        def create_image_alpha(x, y, image, image_seg):
            if self.master.add_seg == False:
                self.images.append(ImageTk.PhotoImage(image))
                self.canvas_item_1 = self.canvas.create_image(x, y, image=self.images[-1], anchor='center')
            else:
                opacity = int(round(self.master.tools.slider_opacity.get(), 0)) / 100
                alpha_seg = int(opacity * 255)
                image_seg = image_seg.convert('RGBA')
                image_seg.putalpha(alpha_seg)
                
                self.images.append(ImageTk.PhotoImage(image))
                self.canvas_item_1 = self.canvas.create_image(x, y, image=self.images[-1], anchor='center')
                self.images.append(ImageTk.PhotoImage(image_seg))
                self.canvas_item_2 = self.canvas.create_image(x, y, image=self.images[-1], anchor='center')

        # get size
        height = int(self.label_zoom.cget("text")) 
            
        # slice index
        image = self.master.img[int(index_slice),:, :]
            
        # hounsfield
        hf1, hf2 = int(round(self.master.tools.hounsfield_slider.get()[0], 0)), int(round(self.master.tools.hounsfield_slider.get()[1], 0))
        image = np.where((image >= hf1) & (image <= hf2), image, 0)
            
        # color map
        color_choice = plt.cm.bone if self.color_map.get() == 'bone' else  self.color_map.get()
        plt.imsave("temp.jpg", image, cmap=color_choice)
            
        # brightness
        image_display = cv2.imread("temp.jpg")
        brightness_image = cv2.convertScaleAbs(image_display, alpha=float(self.master.tools.entry_brightness_value.get()), beta=0)
        cv2.imwrite("temp.jpg", brightness_image)
        
        # resize
        image_display = Image.open("temp.jpg").resize((height, height))
            
        # rotate
        rotation_angle = int(self.rotation_label.cget("text"))
        image_display = image_display.rotate(rotation_angle)
        
        # flip
        horizontal = self.flip_horizontal_label.cget("text")
        vertical = self.flip_vertical_label.cget("text")
        if horizontal == "horizontal":
            image_display = image_display.transpose(Image.FLIP_LEFT_RIGHT)
        if vertical == "vertical":
            image_display = image_display.transpose(Image.FLIP_TOP_BOTTOM)
            
        # segmentation
        if self.master.add_seg == True:
            stacked_arrays = []
            for index, (class_name, data) in enumerate(self.master.class_data.items()):
                if data['visible'] == True:
                    seg = self.master.tools.label_arrays[index][int(index_slice), :, :]
                    stacked_arrays.append(seg)

            combined_seg = np.vstack(stacked_arrays)
            plt.imsave("temp2.jpg", combined_seg, cmap=color_choice)
            
            image_display_seg = cv2.imread("temp2.jpg")
            brightness_image_seg = cv2.convertScaleAbs(image_display_seg, alpha=float(self.master.tools.entry_brightness_value.get()), beta=0)
            cv2.imwrite("temp2.jpg", brightness_image_seg)
            image_display_seg = Image.open("temp2.jpg").resize((height, height))
            image_display_seg = image_display_seg.rotate(rotation_angle)
            
            if horizontal == "horizontal":
                image_display = image_display.transpose(Image.FLIP_LEFT_RIGHT)
                image_display_seg = image_display_seg.transpose(Image.FLIP_LEFT_RIGHT)
            if vertical == "vertical":
                image_display = image_display.transpose(Image.FLIP_TOP_BOTTOM)
                image_display_seg = image_display_seg.transpose(Image.FLIP_TOP_BOTTOM)
                
            x_cord, y_cord = image_position()
            create_image_alpha(x_cord, y_cord, image_display, image_display_seg)

        else:
            # diplay images
            x_cord, y_cord = image_position()
            create_image_alpha(x_cord, y_cord, image_display, image_seg=None)
            
        # create crosshair
        create_crosshair()
            
        # display info
        display_info()
            
        # ROI
        self.region_of_interest = ROI(self, 'axial',                                   
            self.master.ROI_data['axial']['rec']['x1'], 
            self.master.ROI_data['axial']['rec']['y1'],
            self.master.ROI_data['axial']['rec']['x2'], 
            self.master.ROI_data['axial']['rec']['y2'],
        )
            
        # display all drawings
        display_drawings(zoom_ratio=(6)/673)
        
        self.canvas.configure(bg='black')

    def create_canvas(self):    
        def movement_binding():
            def left():
                self.canvas.move(self.canvas_item_1, -10, 0)
                self.canvas.move(self.canvas_item_2, -10, 0)     
            def right():
                self.canvas.move(self.canvas_item_1, 10, 0)
                self.canvas.move(self.canvas_item_2, 10, 0)
            def up():
                self.canvas.move(self.canvas_item_1, 0, -10)
                self.canvas.move(self.canvas_item_2, 0, -10)
            def down():
                self.canvas.move(self.canvas_item_1, 0, 10)
                self.canvas.move(self.canvas_item_2, 0, 10)
                
                
            self.canvas.bind('<Left>', lambda event: left())
            self.canvas.bind('<Right>', lambda event: right())
            self.canvas.bind('<Up>', lambda event: up())
            self.canvas.bind('<Down>', lambda event: down())   
        
        def zoom(event):
            current_value = self.label_zoom.cget("text")
            new_value = int(current_value) + (event.delta/120)*6
            self.label_zoom.configure(text=new_value)
            self.image_display(self.slider_volume.get())   
            
        def slider_volume_show(value):
            index_slice = round(value, 0)
            self.text_show_volume.configure(text=int(index_slice))
            self.canvas.focus_set() 
            self.image_display(index_slice)

        def slider_widget():        
            self.slider_volume = customtkinter.CTkSlider(self.master, from_=0, to=self.master.img.shape[0]-1, command=slider_volume_show)
            self.slider_volume.grid(column=0, row=0, columnspan=2, rowspan=1, padx=(5,0), pady=(25,0), sticky='ew')
            self.text_show_volume = customtkinter.CTkLabel(self.master, text="")
            self.text_show_volume.grid(column=2, row=0, rowspan=1, pady=(25,0), sticky='ew')
            
        self.canvas = Canvas(master=self.frame, bd=0, bg=self.master.first_color, name='axial')
        self.canvas.pack(fill='both', expand=True)
        
        self.label_zoom = customtkinter.CTkLabel(master=self.frame, text="900")
        self.canvas.bind("<MouseWheel>", zoom)
        
        movement_binding()
        slider_widget()

class CanvasSagittal:
    def __init__(self, master):
        self.master = master
        self.create_frame()
        self.create_canvas()     
        self.create_tool_widgets()
        self.name = 'axial'
                
    def save_canvas(self):
        x = self.master.winfo_rootx() + 861
        y = self.master.winfo_rooty() + 100 
        x1 = x + self.canvas.winfo_width()*1.255 
        y1 = y + self.canvas.winfo_height()*1.255  
        ImageGrab.grab ().crop((x,y,x1,y1)).save("canvas.png")
        print('saved')
        
    def create_tool_widgets(self):
        def rotation():
            def rotation_control():
                current_val = int(self.rotation_label.cget('text'))
                if current_val == 360:
                    current_val = 0
                self.rotation_label.configure(text=current_val+90)
            
            self.rotation_label = customtkinter.CTkLabel(master=self.frame, text="0") 
            icon = customtkinter.CTkImage(dark_image=Image.open("imgs/rotate.png"), size=(20, 20))
            self.rotation_btn = customtkinter.CTkButton(master=self.frame_tools, text='', image=icon, width=25, height=25, command=rotation_control)
            self.rotation_btn.grid(column=0, row=0, padx=5, sticky='w') 

        def flip_horizontal():
            def flip_control():
                cur_val = self.flip_horizontal_label.cget("text")
                if cur_val == "":  
                    self.flip_horizontal_label.configure(text="horizontal")
                else:
                    self.flip_horizontal_label.configure(text="")
                
            self.flip_horizontal_label = customtkinter.CTkLabel(master=self.frame, text="") 
            icon = customtkinter.CTkImage(dark_image=Image.open("imgs/flip_horizontal.png"), size=(20, 20))
            self.flip_horizontal_btn = customtkinter.CTkButton(master=self.frame_tools, text='', image=icon,width=25, height=25, command=flip_control)
            self.flip_horizontal_btn.grid(column=1, row=0, padx=5, sticky='w')  
            
        def flip_vertical():
            def flip_control():
                cur_val = self.flip_vertical_label.cget("text")
                if cur_val == "":
                    self.flip_vertical_label.configure(text="vertical")
                else:
                    self.flip_vertical_label.configure(text="")
                    
            self.flip_vertical_label = customtkinter.CTkLabel(master=self.frame, text="") 
            icon = customtkinter.CTkImage(dark_image=Image.open("imgs/flip_vertical.png"), size=(20, 20))
            self.flip_vertical_btn = customtkinter.CTkButton(master=self.frame_tools, text='', image=icon, width=25, height=25, command=flip_control)
            self.flip_vertical_btn.grid(column=2, row=0, padx=5, sticky='w')  
        
        def color_map():
            colors = ["gray", "bone", "nipy_spectral", "viridis", "plasma", "inferno", "magma", "cividis", "Greys", "Purples", "Blues", "Greens", "Reds", "YlOrBr", "YlOrRd", "OrRd", "PuRd", "GnBu"]
            self.color_map_default = customtkinter.StringVar(value="gray")
            self.color_map = customtkinter.CTkComboBox(self.frame_tools, values=colors, variable=self.color_map_default)
            self.color_map.grid(column=3, row=0, sticky='ew', padx=10)
            self.image_display(self.slider_volume.get())
            
        def save_photo():
            icon = customtkinter.CTkImage(dark_image=Image.open("imgs/save.png"), size=(20, 20))
            self.save_photo_btn = customtkinter.CTkButton(master=self.frame_tools, text='', image=icon, width=25, height=25, command=self.save_canvas)
            self.save_photo_btn.grid(row=0, column=4, padx=10, sticky='e')
            
        self.frame_tools = customtkinter.CTkFrame(master=self.master, fg_color='transparent')
        self.frame_tools.grid(column=9, row=0, columnspan=3, rowspan=1, pady=(35, 0), sticky='news')
        self.frame_tools.columnconfigure((0,1,2,3, 4), weight=1)
        rotation()
        flip_horizontal()
        flip_vertical()
        color_map()
        save_photo()

    def create_frame(self):
        self.frame = customtkinter.CTkFrame(master=self.master, fg_color='transparent')
        self.frame.grid(row=1, column=6, rowspan=9, columnspan=6, padx=5, sticky='news')
        
                
    def image_display(self, index_slice):
        def create_crosshair():
            self.horizontal_line = self.canvas.create_line(0, self.canvas.winfo_height() // 2, self.canvas.winfo_width(), self.canvas.winfo_height() // 2, fill="red")
            self.vertical_line = self.canvas.create_line(self.canvas.winfo_width() // 2, 0, self.canvas.winfo_width() // 2, self.canvas.winfo_height(), fill="red")
                
            def move_crosshair(event):
                x, y = event.x, event.y
                self.canvas.coords(self.horizontal_line, 0, y, self.canvas.winfo_width(), y)
                self.canvas.coords(self.vertical_line, x, 0, x, self.canvas.winfo_height())

            def on_mouse_press(event):
                if self.master.tools.check_ROI.get() == "off":
                    self.canvas.bind("<Motion>", move_crosshair)

            def on_mouse_release(event):
                if self.master.tools.check_ROI.get() == "off":
                    self.canvas.unbind("<Motion>")
                        
            if self.master.tools.check_ROI.get() == "off":
                self.canvas.bind("<ButtonPress-1>", on_mouse_press)
                self.canvas.bind("<ButtonRelease-1>", on_mouse_release) 
            
        def image_position():
            try:
                image_position = self.canvas.coords(self.canvas_item)
                return image_position[0], image_position[1]
            except:
                return 400, 400
            
        def display_info():
            text_item = self.canvas.create_text(10, 20, text='SAGITTAL VIEW', anchor="w", fill=self.master.text_canvas_color)
            y = 40
            for k, v in self.master.dict_info.items():
                text_item = self.canvas.create_text(10, y, text=f'{k} : {v}', anchor="w", fill=self.master.text_canvas_color)
                y += 20
                
        def display_drawings():
            for element, data in self.master.draw_data.items():
                if element != 'number_of_elements' and data['slice'] == int(round(self.slider_volume.get(), 0)) and data['canvas'] == 'sagittal':
                    if data['type'] == 'rectangle':
                        self.canvas.create_rectangle(data['x1'], data['y1'], data['x2'], data['y2'], outline=data['color'])
                        self.canvas.create_text((data['x2'] + data['x1'])/2, data['y1']-20, text=element, anchor="center", fill=data['color'])
                    elif data['type'] == 'circle':
                        self.canvas.create_oval(data['x1'], data['y1'], data['x2'], data['y2'], outline=data['color'])
                        self.canvas.create_text((data['x2'] + data['x1'])/2, data['y1']-20, text=element, anchor="center", fill=data['color'])
                    elif data['type'] == 'line':
                        self.canvas.create_line(data['x1'], data['y1'], data['x2'], data['y2'], fill=data['color'], width=3)
                        distance = int(round(((data['x2'] - data['x1'])**2 +  (data['y2'] - data['y1'])**2)**(1/2), 2))
                        self.canvas.create_text((data['x2'] + data['x1'])/2, data['y1']-20, text=f'{element} : {distance}mm', anchor="center", fill=data['color'])
            
        self.images = [] 
        def create_image_alpha(x, y, image, image_seg):
            if self.master.add_seg == False:
                alpha_origin = int(225)
                image = image.convert('RGBA')
                image.putalpha(alpha_origin)
                self.images.append(ImageTk.PhotoImage(image))
                self.canvas_item_1 = self.canvas.create_image(x, y, image=self.images[-1], anchor='center')
                
            else:
                alpha_origin = int(225)
                opacity = int(round(self.master.tools.slider_opacity.get(), 0)) / 100
                alpha_seg = int(opacity * 255)
                image = image.convert('RGBA')
                image_seg = image_seg.convert('RGBA')
                image.putalpha(alpha_origin)
                image_seg.putalpha(alpha_seg)
                self.images.append(ImageTk.PhotoImage(image))
                self.canvas_item_1 = self.canvas.create_image(x, y, image=self.images[-1], anchor='center')
                self.images.append(ImageTk.PhotoImage(image_seg))
                self.canvas_item_2 = self.canvas.create_image(x, y, image=self.images[-1], anchor='center')

        # get size
        height = int(self.label_zoom.cget("text")) 
            
        # slice index
        image = self.master.img[:, int(index_slice), :]
            
        # hounsfield
        hf1, hf2 = int(round(self.master.tools.hounsfield_slider.get()[0], 0)), int(round(self.master.tools.hounsfield_slider.get()[1], 0))
        image = np.where((image >= hf1) & (image <= hf2), image, 0)
            
        # color map
        color_choice = plt.cm.bone if self.color_map.get() == 'bone' else  self.color_map.get()
        plt.imsave("temp.jpg", image, cmap=color_choice)
            
        # brightness
        image_display = cv2.imread("temp.jpg")
        brightness_image = cv2.convertScaleAbs(image_display, alpha=float(self.master.tools.entry_brightness_value.get()), beta=0)
        cv2.imwrite("temp.jpg", brightness_image)
        
        # resize
        image_display = Image.open("temp.jpg").resize((height, height))
            
        # rotate
        rotation_angle = int(self.rotation_label.cget("text"))
        image_display = image_display.rotate(rotation_angle)
        
        # flip
        horizontal = self.flip_horizontal_label.cget("text")
        vertical = self.flip_vertical_label.cget("text")
        if horizontal == "horizontal":
            image_display = image_display.transpose(Image.FLIP_LEFT_RIGHT)
        if vertical == "vertical":
            image_display = image_display.transpose(Image.FLIP_TOP_BOTTOM)
            
        # segmentation
        if self.master.add_seg == True:
            seg = self.master.seg[:, int(index_slice), :]
            plt.imsave("temp2.jpg", seg, cmap=color_choice)
            image_display_seg = cv2.imread("temp2.jpg")
            brightness_image_seg = cv2.convertScaleAbs(image_display_seg, alpha=float(self.master.tools.entry_brightness_value.get()), beta=0)
            cv2.imwrite("temp2.jpg", brightness_image_seg)
            image_display_seg = Image.open("temp2.jpg").resize((height, height))
            image_display_seg = image_display_seg.rotate(rotation_angle)
            
            if horizontal == "horizontal":
                image_display = image_display.transpose(Image.FLIP_LEFT_RIGHT)
                image_display_seg = image_display_seg.transpose(Image.FLIP_LEFT_RIGHT)
            if vertical == "vertical":
                image_display = image_display.transpose(Image.FLIP_TOP_BOTTOM)
                image_display_seg = image_display_seg.transpose(Image.FLIP_TOP_BOTTOM)
                
            x_cord, y_cord = image_position()
            create_image_alpha(x_cord, y_cord, image_display, image_display_seg)

        else:
            # diplay images
            x_cord, y_cord = image_position()
            create_image_alpha(x_cord, y_cord, image_display, image_seg=None) 
            
        # create crosshair
        create_crosshair()
            
        # display info
        display_info()
            
        # ROI
        self.region_of_interest = ROI(self, 'sagittal',                                   
            self.master.ROI_data['sagittal']['rec']['x1'], 
            self.master.ROI_data['sagittal']['rec']['y1'],
            self.master.ROI_data['sagittal']['rec']['x2'], 
            self.master.ROI_data['sagittal']['rec']['y2'],
        )
        
        # display drawings
        display_drawings()
            
        self.canvas.configure(bg='black')
        
    def create_canvas(self):                
        def movement_binding():
            def left():
                self.canvas.move(self.canvas_item_1, -10, 0)
                self.canvas.move(self.canvas_item_2, -10, 0)     
            def right():
                self.canvas.move(self.canvas_item_1, 10, 0)
                self.canvas.move(self.canvas_item_2, 10, 0)
            def up():
                self.canvas.move(self.canvas_item_1, 0, -10)
                self.canvas.move(self.canvas_item_2, 0, -10)
            def down():
                self.canvas.move(self.canvas_item_1, 0, 10)
                self.canvas.move(self.canvas_item_2, 0, 10)
                
                
            self.canvas.bind('<Left>', lambda event: left())
            self.canvas.bind('<Right>', lambda event: right())
            self.canvas.bind('<Up>', lambda event: up())
            self.canvas.bind('<Down>', lambda event: down())  
        
        
        def zoom(event):
            current_value = self.label_zoom.cget("text")
            new_value = int(current_value) + (event.delta/120)*6
            self.label_zoom.configure(text=new_value)
            self.image_display(self.slider_volume.get())   
            
        def slider_volume_show(value):
            index_slice = round(value, 0)
            self.text_show_volume.configure(text=int(index_slice))
            self.canvas.focus_set() 
            self.image_display(index_slice)

        def slider_widget():        
            self.slider_volume = customtkinter.CTkSlider(self.master, from_=0, to=self.master.img.shape[1]-1, command=slider_volume_show)
            self.slider_volume.grid(column=6, row=0, columnspan=2, rowspan=1, padx=(5,0), pady=(25,0), sticky='ew')
            self.text_show_volume = customtkinter.CTkLabel(self.master, text="")
            self.text_show_volume.grid(column=8, row=0, rowspan=1, pady=(25,0), sticky='ew')
            
        self.canvas = Canvas(master=self.frame, bd=0, bg=self.master.first_color, name='sagittal')
        self.canvas.pack(fill='both', expand=True)
        
        self.label_zoom = customtkinter.CTkLabel(master=self.frame, text="900")
        self.canvas.bind("<MouseWheel>", zoom)
        
        movement_binding()
        slider_widget()
        
class CanvasCoronal:
    def __init__(self, master):
        self.master = master
        self.create_frame()
        self.create_canvas()   
        self.create_tool_widgets()  
        
    def save_canvas(self):
        x = self.master.winfo_rootx() + 857*2
        y = self.master.winfo_rooty() + 100 
        x1 = x + self.canvas.winfo_width()*1.255 
        y1 = y + self.canvas.winfo_height()*1.255  
        ImageGrab.grab ().crop((x,y,x1,y1)).save("canvas.png")
        print('saved')

    def create_tool_widgets(self):            
        def rotation():
            def rotation_control():
                current_val = int(self.rotation_label.cget('text'))
                if current_val == 360:
                    current_val = 0
                self.rotation_label.configure(text=current_val+90)
             
            self.rotation_label = customtkinter.CTkLabel(master=self.frame, text="0") 
            icon = customtkinter.CTkImage(dark_image=Image.open("imgs/rotate.png"), size=(20, 20))
            self.rotation_btn = customtkinter.CTkButton(master=self.frame_tools, text="", image=icon, width=25, height=25, command=rotation_control)
            self.rotation_btn.grid(column=0, row=0, padx=5, sticky='w') 

        def flip_horizontal():
            def flip_control():
                cur_val = self.flip_horizontal_label.cget("text")
                if cur_val == "":  
                    self.flip_horizontal_label.configure(text="horizontal")
                else:
                    self.flip_horizontal_label.configure(text="")
                
            self.flip_horizontal_label = customtkinter.CTkLabel(master=self.frame, text="") 
            icon = customtkinter.CTkImage(dark_image=Image.open("imgs/flip_horizontal.png"), size=(20, 20))
            self.flip_horizontal_btn = customtkinter.CTkButton(master=self.frame_tools, text='', image=icon, width=25, height=25, command=flip_control)
            self.flip_horizontal_btn.grid(column=1, row=0, padx=5, sticky='w')  
            
        def flip_vertical():
            def flip_control():
                cur_val = self.flip_vertical_label.cget("text")
                if cur_val == "":
                    self.flip_vertical_label.configure(text="vertical")
                else:
                    self.flip_vertical_label.configure(text="")
                    
            self.flip_vertical_label = customtkinter.CTkLabel(master=self.frame, text="") 
            icon = customtkinter.CTkImage(dark_image=Image.open("imgs/flip_vertical.png"), size=(20, 20))
            self.flip_vertical_btn = customtkinter.CTkButton(master=self.frame_tools, text='', image=icon, width=25, height=25, command=flip_control)
            self.flip_vertical_btn.grid(column=2, row=0, padx=5, sticky='w')  
            
        def color_map():
            colors = ["gray", "bone", "nipy_spectral", "viridis", "plasma", "inferno", "magma", "cividis", "Greys", "Purples", "Blues", "Greens", "Reds", "YlOrBr", "YlOrRd", "OrRd", "PuRd", "GnBu"]
            self.color_map_default = customtkinter.StringVar(value="gray")
            self.color_map = customtkinter.CTkComboBox(self.frame_tools, values=colors, variable=self.color_map_default)
            self.color_map.grid(column=3, row=0, sticky='ew', padx=10)
            self.image_display(self.slider_volume.get())
            
        def save_photo():
            icon = customtkinter.CTkImage(dark_image=Image.open("imgs/save.png"), size=(20, 20))
            self.save_photo_btn = customtkinter.CTkButton(master=self.frame_tools, text='', image=icon, width=25, height=25, command=self.save_canvas)
            self.save_photo_btn.grid(row=0, column=4, padx=10, sticky='e')
            
        self.frame_tools = customtkinter.CTkFrame(master=self.master, fg_color='transparent')
        self.frame_tools.grid(column=15, row=0, columnspan=3, rowspan=1, pady=(35, 0), sticky='news')
        self.frame_tools.columnconfigure((0,1,2,3,4), weight=1)
        rotation()
        flip_horizontal()
        flip_vertical()
        color_map()
        save_photo()
        
        
        
    def create_frame(self):
        self.frame = customtkinter.CTkFrame(master=self.master, fg_color=self.master.second_color)
        self.frame.grid(row=1, column=12, rowspan=9, columnspan=6, padx=5, sticky='news')
        
    def image_display(self, index_slice):
        def create_crosshair():
            self.horizontal_line = self.canvas.create_line(0, self.canvas.winfo_height() // 2, self.canvas.winfo_width(), self.canvas.winfo_height() // 2, fill="red")
            self.vertical_line = self.canvas.create_line(self.canvas.winfo_width() // 2, 0, self.canvas.winfo_width() // 2, self.canvas.winfo_height(), fill="red")
            
            def move_crosshair(event):
                x, y = event.x, event.y
                self.canvas.coords(self.horizontal_line, 0, y, self.canvas.winfo_width(), y)
                self.canvas.coords(self.vertical_line, x, 0, x, self.canvas.winfo_height())

            def on_mouse_press(event):
                if self.master.tools.check_ROI.get() == "off":
                    self.canvas.bind("<Motion>", move_crosshair)

            def on_mouse_release(event):
                if self.master.tools.check_ROI.get() == "off":
                    self.canvas.unbind("<Motion>")

            self.canvas.bind("<ButtonPress-1>", on_mouse_press)
            self.canvas.bind("<ButtonRelease-1>", on_mouse_release)  
            
        def image_position():
            try:
                image_position = self.canvas.coords(self.canvas_item)
                return image_position[0], image_position[1]
            except:
                return 400, 400
        def display_info():
            text_item = self.canvas.create_text(10, 20, text='CORONAL VIEW', anchor="w", fill=self.master.text_canvas_color)
            y = 40
            for k, v in self.master.dict_info.items():
                text_item = self.canvas.create_text(10, y, text=f'{k} : {v}', anchor="w", fill=self.master.text_canvas_color)
                y += 20 
                
        def display_drawings():
            for element, data in self.master.draw_data.items():
                if element != 'number_of_elements' and data['slice'] == int(round(self.slider_volume.get(), 0)) and data['canvas'] == 'coronal':
                    if data['type'] == 'rectangle':
                        self.canvas.create_rectangle(data['x1'], data['y1'], data['x2'], data['y2'], outline=data['color'])
                        self.canvas.create_text((data['x2'] + data['x1'])/2, data['y1']-20, text=element, anchor="center", fill=data['color'])
                    elif data['type'] == 'circle':
                        self.canvas.create_oval(data['x1'], data['y1'], data['x2'], data['y2'], outline=data['color'])
                        self.canvas.create_text((data['x2'] + data['x1'])/2, data['y1']-20, text=element, anchor="center", fill=data['color'])
                    elif data['type'] == 'line':
                        self.canvas.create_line(data['x1'], data['y1'], data['x2'], data['y2'], fill=data['color'], width=3)
                        distance = int(round(((data['x2'] - data['x1'])**2 +  (data['y2'] - data['y1'])**2)**(1/2), 2))
                        self.canvas.create_text((data['x2'] + data['x1'])/2, data['y1']-20, text=f'{element} : {distance}mm', anchor="center", fill=data['color'])  
          
        self.images = [] 
        def create_image_alpha(x, y, image, image_seg):
            if self.master.add_seg == False:
                alpha_origin = int(225)
                image = image.convert('RGBA')
                image.putalpha(alpha_origin)
                self.images.append(ImageTk.PhotoImage(image))
                self.canvas_item_1 = self.canvas.create_image(x, y, image=self.images[-1], anchor='center')
                
            else:
                alpha_origin = int(225)
                opacity = int(round(self.master.tools.slider_opacity.get(), 0)) / 100
                alpha_seg = int(opacity * 255)
                image = image.convert('RGBA')
                image_seg = image_seg.convert('RGBA')
                image.putalpha(alpha_origin)
                image_seg.putalpha(alpha_seg)
                self.images.append(ImageTk.PhotoImage(image))
                self.canvas_item_1 = self.canvas.create_image(x, y, image=self.images[-1], anchor='center')
                self.images.append(ImageTk.PhotoImage(image_seg))
                self.canvas_item_2 = self.canvas.create_image(x, y, image=self.images[-1], anchor='center')

        # get size
        height = int(self.label_zoom.cget("text")) 
            
        # slice index
        image = self.master.img[:, :, int(index_slice)]
            
        # hounsfield
        hf1, hf2 = int(round(self.master.tools.hounsfield_slider.get()[0], 0)), int(round(self.master.tools.hounsfield_slider.get()[1], 0))
        image = np.where((image >= hf1) & (image <= hf2), image, 0)
            
        # color map
        color_choice = plt.cm.bone if self.color_map.get() == 'bone' else  self.color_map.get()
        plt.imsave("temp.jpg", image, cmap=color_choice)
            
        # brightness
        image_display = cv2.imread("temp.jpg")
        brightness_image = cv2.convertScaleAbs(image_display, alpha=float(self.master.tools.entry_brightness_value.get()), beta=0)
        cv2.imwrite("temp.jpg", brightness_image)
        
        # resize
        image_display = Image.open("temp.jpg").resize((height, height))
            
        # rotate
        rotation_angle = int(self.rotation_label.cget("text"))
        image_display = image_display.rotate(rotation_angle)
        
        # flip
        horizontal = self.flip_horizontal_label.cget("text")
        vertical = self.flip_vertical_label.cget("text")
        if horizontal == "horizontal":
            image_display = image_display.transpose(Image.FLIP_LEFT_RIGHT)
        if vertical == "vertical":
            image_display = image_display.transpose(Image.FLIP_TOP_BOTTOM)
            
        # segmentation
        if self.master.add_seg == True:
            seg = self.master.seg[:, :, int(index_slice)]
            plt.imsave("temp2.jpg", seg, cmap=color_choice)
            image_display_seg = cv2.imread("temp2.jpg")
            brightness_image_seg = cv2.convertScaleAbs(image_display_seg, alpha=float(self.master.tools.entry_brightness_value.get()), beta=0)
            cv2.imwrite("temp2.jpg", brightness_image_seg)
            image_display_seg = Image.open("temp2.jpg").resize((height, height))
            image_display_seg = image_display_seg.rotate(rotation_angle)
            
            if horizontal == "horizontal":
                image_display = image_display.transpose(Image.FLIP_LEFT_RIGHT)
                image_display_seg = image_display_seg.transpose(Image.FLIP_LEFT_RIGHT)
            if vertical == "vertical":
                image_display = image_display.transpose(Image.FLIP_TOP_BOTTOM)
                image_display_seg = image_display_seg.transpose(Image.FLIP_TOP_BOTTOM)
                
            x_cord, y_cord = image_position()
            create_image_alpha(x_cord, y_cord, image_display, image_display_seg)

        else:
            # diplay images
            x_cord, y_cord = image_position()
            create_image_alpha(x_cord, y_cord, image_display, image_seg=None)  
            
        # create crosshair
        create_crosshair()
            
        # display info
        display_info()
            
        # ROI
        self.region_of_interest = ROI(self, 'coronal',                                   
            self.master.ROI_data['coronal']['rec']['x1'], 
            self.master.ROI_data['coronal']['rec']['y1'],
            self.master.ROI_data['coronal']['rec']['x2'], 
            self.master.ROI_data['coronal']['rec']['y2'],
        )
        
        # display drawings
        display_drawings()
        
        self.canvas.configure(bg='black')

    def create_canvas(self):    
        def movement_binding():
            def left():
                self.canvas.move(self.canvas_item_1, -10, 0)
                self.canvas.move(self.canvas_item_2, -10, 0)     
            def right():
                self.canvas.move(self.canvas_item_1, 10, 0)
                self.canvas.move(self.canvas_item_2, 10, 0)
            def up():
                self.canvas.move(self.canvas_item_1, 0, -10)
                self.canvas.move(self.canvas_item_2, 0, -10)
            def down():
                self.canvas.move(self.canvas_item_1, 0, 10)
                self.canvas.move(self.canvas_item_2, 0, 10)
                
                
            self.canvas.bind('<Left>', lambda event: left())
            self.canvas.bind('<Right>', lambda event: right())
            self.canvas.bind('<Up>', lambda event: up())
            self.canvas.bind('<Down>', lambda event: down())  
            
        def zoom(event):
            current_value = self.label_zoom.cget("text")
            new_value = int(current_value) + (event.delta/120)*6
            self.label_zoom.configure(text=new_value)
            self.image_display(self.slider_volume.get())   
            
        def slider_volume_show(value):
            index_slice = round(value, 0)
            self.text_show_volume.configure(text=int(index_slice))
            self.canvas.focus_set() 
            self.image_display(index_slice)
            

        def slider_widget():        
            self.slider_volume = customtkinter.CTkSlider(self.master, from_=0, to=self.master.img.shape[2]-1, command=slider_volume_show)
            self.slider_volume.grid(column=12, row=0, columnspan=2, rowspan=1, padx=(5,0), pady=(25,0), sticky='ew')
            self.text_show_volume = customtkinter.CTkLabel(self.master, text="")
            self.text_show_volume.grid(column=14, row=0, rowspan=1, pady=(25,0), sticky='ew')
            
        self.canvas = Canvas(master=self.frame, bd=0, bg=self.master.first_color, name='coronal')
        self.canvas.pack(fill='both', expand=True)
        
        self.label_zoom = customtkinter.CTkLabel(master=self.frame, text="900")
        self.canvas.bind("<MouseWheel>", zoom)
        
        movement_binding()
        slider_widget()
        
    
        
class Tools:
    def __init__(self, master):
        self.master = master
        self.TabView1()
        self.TabView2()
        self.layers_management()          
        
    def title_toolbox(self, frame, title):
        header = customtkinter.CTkButton(master=frame, text=title, state='disabled', fg_color=self.master.second_color, text_color_disabled=self.master.text_disabled_color)
        header.grid(row=0, column=0, columnspan=12, padx=7, pady=7, sticky='new')
        return header
      
    def config(self):
        self.hounsfield_slider.configure(from_=2424, to=7878)
        
    def TabView1(self):
        def ROI():
            def frame():
                self.check_ROI_frame = customtkinter.CTkFrame(master=self.tabview_1_tab_1)
                self.check_ROI_frame.grid(column=0, row=0, columnspan=2, rowspan=3, pady=(0,5), sticky='news')
                self.check_ROI_frame.rowconfigure((0,1,2,3,4), weight=1)
                self.check_ROI_frame.columnconfigure((0,1,2,3,4), weight=1)
                
                self.check_ROI_header = self.title_toolbox(frame=self.check_ROI_frame, title='Region of Interest')
                
                self.check_var = customtkinter.StringVar(value="off")
                self.check_ROI = customtkinter.CTkCheckBox(master=self.check_ROI_frame, text="Edit ROI", variable=self.check_var, onvalue="on", offvalue="off")
                self.check_ROI.grid(row=1, column=0, columnspan=5, sticky='n')
            
            def axial():
                self.axial_label = customtkinter.CTkLabel(master=self.check_ROI_frame, text="Axial").grid(row=2, column=0, padx=(5,0), sticky='w')
                self.axial_x1 = customtkinter.StringVar(value=f"x: {self.master.ROI_data['axial']['rec']['x1']}")
                self.axial_x1_show = customtkinter.CTkLabel(master=self.check_ROI_frame, textvariable=self.axial_x1)
                self.axial_x1_show.grid(row=2, column=1, padx=(5,0),  sticky='w')
                
                self.axial_y1 = customtkinter.StringVar(value=f"y: {self.master.ROI_data['axial']['rec']['x1']}")
                self.axial_y1_show = customtkinter.CTkLabel(master=self.check_ROI_frame, textvariable=self.axial_y1)
                self.axial_y1_show.grid(row=2, column=2, padx=(10,0), sticky='w')
                
                self.axial_width = customtkinter.StringVar(value=f"width: {self.master.ROI_data['axial']['rec']['x2'] - self.master.ROI_data['axial']['rec']['x1']}")
                self.axial_width_show = customtkinter.CTkLabel(master=self.check_ROI_frame, textvariable=self.axial_width)
                self.axial_width_show.grid(row=2, column=3,padx=(10,0),  sticky='w')
                
                self.axial_height = customtkinter.StringVar(value=f"height: {self.master.ROI_data['axial']['rec']['y2'] - self.master.ROI_data['axial']['rec']['y1']}")
                self.axial_height_show = customtkinter.CTkLabel(master=self.check_ROI_frame, textvariable=self.axial_height)
                self.axial_height_show.grid(row=2, column=4,padx=(10,0),  sticky='w')
                
            def sagittal():
                self.sagittal_label = customtkinter.CTkLabel(master=self.check_ROI_frame, text="Sagittal").grid(row=3, column=0, sticky='w')
                self.sagittal_x1 = customtkinter.StringVar(value=f"x: {self.master.ROI_data['sagittal']['rec']['x1']}")
                self.sagittal_x1_show = customtkinter.CTkLabel(master=self.check_ROI_frame, textvariable=self.sagittal_x1)
                self.sagittal_x1_show.grid(row=3, column=1, padx=(10,0), sticky='w')
                
                self.sagittal_y1 = customtkinter.StringVar(value=f"y: {self.master.ROI_data['sagittal']['rec']['x1']}")
                self.sagittal_y1_show = customtkinter.CTkLabel(master=self.check_ROI_frame, textvariable=self.sagittal_y1)
                self.sagittal_y1_show.grid(row=3, column=2, padx=(10,0), sticky='w')
                
                self.sagittal_width = customtkinter.StringVar(value=f"width: {self.master.ROI_data['sagittal']['rec']['x2'] - self.master.ROI_data['sagittal']['rec']['x1']}")
                self.sagittal_width_show = customtkinter.CTkLabel(master=self.check_ROI_frame, textvariable=self.sagittal_width)
                self.sagittal_width_show.grid(row=3, column=3, padx=(10,0), sticky='w')
                
                self.sagittal_height = customtkinter.StringVar(value=f"height: {self.master.ROI_data['sagittal']['rec']['y2'] - self.master.ROI_data['sagittal']['rec']['y1']}")
                self.sagittal_height_show = customtkinter.CTkLabel(master=self.check_ROI_frame, textvariable=self.sagittal_height)
                self.sagittal_height_show.grid(row=3, column=4,padx=(10,0), sticky='w')
                
            def coronal():
                self.coronal_label = customtkinter.CTkLabel(master=self.check_ROI_frame, text="Coronal").grid(row=4, column=0, sticky='w')
                self.coronal_x1 = customtkinter.StringVar(value=f"x: {self.master.ROI_data['coronal']['rec']['x1']}")
                self.coronal_x1_show = customtkinter.CTkLabel(master=self.check_ROI_frame, textvariable=self.coronal_x1)
                self.coronal_x1_show.grid(row=4, column=1,padx=(10,0),  sticky='w')
                
                self.coronal_y1 = customtkinter.StringVar(value=f"y: {self.master.ROI_data['coronal']['rec']['x1']}")
                self.coronal_y1_show = customtkinter.CTkLabel(master=self.check_ROI_frame, textvariable=self.coronal_y1)
                self.coronal_y1_show.grid(row=4, column=2,padx=(10,0), sticky='w')
                
                self.coronal_width = customtkinter.StringVar(value=f"width: {self.master.ROI_data['coronal']['rec']['x2'] - self.master.ROI_data['coronal']['rec']['x1']}")
                self.coronal_width_show = customtkinter.CTkLabel(master=self.check_ROI_frame, textvariable=self.coronal_width)
                self.coronal_width_show.grid(row=4, column=3, padx=(10,0), sticky='w')
                
                self.coronal_height = customtkinter.StringVar(value=f"height: {self.master.ROI_data['coronal']['rec']['y2'] - self.master.ROI_data['coronal']['rec']['y1']}")
                self.coronal_height_show = customtkinter.CTkLabel(master=self.check_ROI_frame, textvariable=self.coronal_height)
                self.coronal_height_show.grid(row=4, column=4, padx=(10,0), sticky='w')
                
            frame()
            axial()
            sagittal()
            coronal()
            
        def HounsField():
            def frame():
                self.hounsfield_frame = customtkinter.CTkFrame(master=self.tabview_1_tab_1)
                self.hounsfield_frame.grid(column=0, row=3, columnspan=2, rowspan=3, sticky='news')
                self.hounsfield_frame.rowconfigure((0,1,2), weight=1)
                self.hounsfield_frame.columnconfigure(0, weight=1)
                
                self.hounsfield_header = self.title_toolbox(frame=self.hounsfield_frame, title='HounsField Unit')
                
            def widget():   
                def update_hounnsfield_slider(value):
                    self.btn_left_entry.configure(placeholder_text=value[0])
                    self.btn_right_entry.configure(placeholder_text=value[1])     
                    self.master.axial.image_display(self.master.axial.slider_volume.get())      
                    self.master.sagittal.image_display(self.master.sagittal.slider_volume.get())         
                    self.master.coronal.image_display(self.master.coronal.slider_volume.get())         
                    
                def left_increase_hf():
                    hf1, hf2 = int(round(self.hounsfield_slider.get()[0], 0)), int(round(self.hounsfield_slider.get()[1], 0))
                    hf1 += 50
                    self.hounsfield_slider.set([hf1, hf2])
                    self.btn_left_entry.configure(placeholder_text=hf1)
                    self.btn_right_entry.configure(placeholder_text=hf2)
                    
                def left_decrease_hf():
                    hf1, hf2 = int(round(self.hounsfield_slider.get()[0], 0)), int(round(self.hounsfield_slider.get()[1], 0))
                    hf1 -= 50
                    self.hounsfield_slider.set([hf1, hf2])
                    self.btn_left_entry.configure(placeholder_text=hf1)
                    self.btn_right_entry.configure(placeholder_text=hf2)
                
                def right_increase_hf():
                    hf1, hf2 = int(round(self.hounsfield_slider.get()[0], 0)), int(round(self.hounsfield_slider.get()[1], 0))
                    hf2 += 50
                    self.hounsfield_slider.set([hf1, hf2])
                    self.btn_left_entry.configure(placeholder_text=hf1)
                    self.btn_right_entry.configure(placeholder_text=hf2)

                    
                def right_decrease_hf():
                    hf1, hf2 = int(round(self.hounsfield_slider.get()[0], 0)), int(round(self.hounsfield_slider.get()[1], 0))
                    hf2 -= 50
                    self.hounsfield_slider.set([hf1, hf2])
                    self.btn_left_entry.configure(placeholder_text=hf1)
                    self.btn_right_entry.configure(placeholder_text=hf2)

                
                self.hounsfield_slider = CTkRangeSlider(self.hounsfield_frame, from_=-1000, to=1000, command=update_hounnsfield_slider)
                self.hounsfield_slider.grid(column=0, row=2, columnspan=2, sticky='new', padx=5)
                
                self.btn_left_increase = customtkinter.CTkButton(self.hounsfield_frame, text="+", width=20, command=left_increase_hf)
                self.btn_left_increase.grid(column=0, row=1, sticky='nw', padx=(30,0))
                
                self.btn_left_decrease = customtkinter.CTkButton(self.hounsfield_frame, text="-", width=20, command=left_decrease_hf)
                self.btn_left_decrease.grid(column=0, row=1, sticky='nw', padx=(5,0))
                
                self.btn_left_entry = customtkinter.CTkEntry(self.hounsfield_frame, placeholder_text=self.hounsfield_slider.get()[0], width=70, state='normal')
                self.btn_left_entry.grid(column=0, row=1, sticky='nw', padx=(60,0))
                
                self.btn_right_increase = customtkinter.CTkButton(self.hounsfield_frame, text="+", width=20, command=right_increase_hf)
                self.btn_right_increase.grid(column=0, row=1, sticky='ne', padx=(0,5))
                
                self.btn_right_decrease = customtkinter.CTkButton(self.hounsfield_frame, text="-", width=20, command=right_decrease_hf)
                self.btn_right_decrease.grid(column=0, row=1, sticky='ne', padx=(0,30))
                
                self.btn_right_entry = customtkinter.CTkEntry(self.hounsfield_frame, placeholder_text=self.hounsfield_slider.get()[1], width=70, state='normal')
                self.btn_right_entry.configure('normal')
                self.btn_right_entry.grid(column=0, row=1, sticky='ne', padx=(0,60))
                
            frame()
            widget()


        def DrawingTools():
            def frame():
                self.layer_frame = customtkinter.CTkScrollableFrame(self.tabview_1_tab_1, label_text='Layer elements')
                self.layer_frame.grid(row=0, column=2, columnspan=1, rowspan=6, padx=(5,0), sticky='news')
                self.layer_frame.columnconfigure((0,1,2,3,4,5,6), weight=1)
                
                self.draw_frame = customtkinter.CTkFrame(self.tabview_1_tab_1)
                self.draw_frame.grid(row=0, column=3, columnspan=3, rowspan=3, padx=(5,0), sticky='news')
                self.draw_frame.rowconfigure((0,1), weight=1)
                self.draw_frame.columnconfigure((0,1,2,3,4,5), weight=1)
                self.draw_header = self.title_toolbox(frame=self.draw_frame, title="Analysis tools")
        
            def create_radio_btn():
                self.radio_btn_var = tkinter.IntVar(value=0)
                self.rectangle_radio_btn = customtkinter.CTkRadioButton(self.draw_frame, variable=self.radio_btn_var, value=1)
                self.circle_radio_btn = customtkinter.CTkRadioButton(self.draw_frame, variable=self.radio_btn_var, value=2)
                self.ruler_radio_btn = customtkinter.CTkRadioButton(self.draw_frame, variable=self.radio_btn_var, value=3)
                self.polygon_radio_btn = customtkinter.CTkRadioButton(self.draw_frame, variable=self.radio_btn_var, value=4)
                self.brush_radio_btn = customtkinter.CTkRadioButton(self.draw_frame, variable=self.radio_btn_var, value=5)
                self.eraser_radio_btn = customtkinter.CTkRadioButton(self.draw_frame, variable=self.radio_btn_var, value=6)
                                    
            def create_tool_btns():     
                def create_shape(shape):
                    def create():
                        if self.canvas_focus == 'axial':
                            slice = int(round(self.master.axial.slider_volume.get(), 0))
                        elif self.canvas_focus == 'sagittal':
                            slice = int(round(self.master.sagittal.slider_volume.get(), 0))
                        if self.canvas_focus == 'coronal':
                            slice = int(round(self.master.coronal.slider_volume.get(), 0))
                            
                        self.num_element = self.master.draw_data['number_of_elements'] 
                        temp = {
                            self.shape + '_' + str(self.num_element): {
                                'canvas': self.canvas_focus,
                                'slice': slice,
                                'color': self.color_choosed,
                                'type': self.shape,
                                'note': ""
                            }
                        }
                        self.master.draw_data['number_of_elements'] = self.num_element + 1
                        self.master.draw_data.update(temp)
                    
                    def on_press_rec(event):
                        create()
                        element = self.shape + '_' + str(self.num_element) 
                        self.master.draw_data[element]['x1'] = event.x
                        self.master.draw_data[element]['y1'] = event.y
                        
                    def on_release_rec(event):
                        element = self.shape + '_' + str(self.num_element) 
                        self.master.draw_data[element]['x2'] = event.x
                        self.master.draw_data[element]['y2'] = event.y
                        
                        if self.shape=='rectangle':
                            if self.canvas_focus == 'axial':
                                self.master.axial.canvas.create_rectangle(self.master.draw_data[element]['x1'], self.master.draw_data[element]['y1'], event.x, event.y, outline=self.master.draw_data[element]['color'])
                                self.master.axial.image_display(int(round(self.master.axial.slider_volume.get(),0)))
                            elif self.canvas_focus == 'sagittal':
                                self.master.sagittal.canvas.create_rectangle(self.master.draw_data[element]['x1'], self.master.draw_data[element]['y1'], event.x, event.y, outline=self.master.draw_data[element]['color'])
                                self.master.sagittal.image_display(int(round (self.master.sagittal.slider_volume.get(),0)))
                            elif self.canvas_focus == 'coronal':
                                self.master.coronal.canvas.create_rectangle(self.master.draw_data[element]['x1'], self.master.draw_data[element]['y1'], event.x, event.y, outline=self.master.draw_data[element]['color'])
                                self.master.coronal.image_display(int(round(self.master.coronal.slider_volume.get(),0)))
                                
                        elif self.shape=='circle':
                            if self.canvas_focus == 'axial':
                                self.master.axial.canvas.create_oval(self.master.draw_data[element]['x1'], self.master.draw_data[element]['y1'], event.x, event.y, outline=self.master.draw_data[element]['color'])
                                self.master.axial.image_display(int(round(self.master.axial.slider_volume.get(),0)))
                            elif self.canvas_focus == 'sagittal':
                                self.master.sagittal.canvas.create_oval(self.master.draw_data[element]['x1'], self.master.draw_data[element]['y1'], event.x, event.y, outline=self.master.draw_data[element]['color'])
                                self.master.sagittal.image_display(int(round (self.master.sagittal.slider_volume.get(),0)))
                            elif self.canvas_focus == 'coronal':
                                self.master.coronal.canvas.create_oval(self.master.draw_data[element]['x1'], self.master.draw_data[element]['y1'], event.x, event.y, outline=self.master.draw_data[element]['color'])
                                self.master.coronal.image_display(int(round(self.master.coronal.slider_volume.get(),0)))
                                
                        elif self.shape=='line':
                            if self.canvas_focus == 'axial':
                                self.master.axial.canvas.create_line(self.master.draw_data[element]['x1'], self.master.draw_data[element]['y1'], event.x, event.y, fill=self.master.draw_data[element]['color'], width=3)
                                self.master.axial.image_display(int(round(self.master.axial.slider_volume.get(),0)))
                            elif self.canvas_focus == 'sagittal':
                                self.master.sagittal.canvas.create_line(self.master.draw_data[element]['x1'], self.master.draw_data[element]['y1'], event.x, event.y, fill=self.master.draw_data[element]['color'], width=3)
                                self.master.sagittal.image_display(int(round (self.master.sagittal.slider_volume.get(),0)))
                            elif self.canvas_focus == 'coronal':
                                self.master.coronal.canvas.create_line(self.master.draw_data[element]['x1'], self.master.draw_data[element]['y1'], event.x, event.y, fill=self.master.draw_data[element]['color'], width=3)
                                self.master.coronal.image_display(int(round(self.master.coronal.slider_volume.get(),0)))
                        
                        self.layers_management()
                    
                    self.canvas_focus = self.master.focus_get().winfo_name()  
                    self.num_element = self.master.draw_data['number_of_elements'] 
                    self.shape = shape
                    if self.canvas_focus == 'axial':
                        self.master.axial.canvas.bind('<Button-1>', on_press_rec)
                        self.master.axial.canvas.bind('<ButtonRelease-1>', on_release_rec)
                    elif self.canvas_focus == 'sagittal':
                        self.master.sagittal.canvas.bind('<Button-1>', on_press_rec)
                        self.master.sagittal.canvas.bind('<ButtonRelease-1>', on_release_rec)
                    elif self.canvas_focus == 'coronal':
                        self.master.coronal.canvas.bind('<Button-1>', on_press_rec)
                        self.master.coronal.canvas.bind('<ButtonRelease-1>', on_release_rec)
                        
                
                
                icon = customtkinter.CTkImage(dark_image=Image.open("imgs/square.png"),size=(25, 25))
                self.rec_icon = customtkinter.CTkButton(self.draw_frame, text="", image=icon, width=40, height=40, command=lambda shape='rectangle': create_shape(shape))
                self.rec_icon.grid(row=1, column=0, padx=5, pady=5, sticky='n')
                
                icon = customtkinter.CTkImage(dark_image=Image.open("imgs/circle.png"),size=(25, 25))
                self.circle_icon = customtkinter.CTkButton(self.draw_frame, text="", image=icon, width=40, height=40, command=lambda shape='circle': create_shape(shape))
                self.circle_icon.grid(row=1, column=1, padx=5, pady=5, sticky='n')
                
                icon = customtkinter.CTkImage(dark_image=Image.open("imgs/ruler.png"),size=(25, 25))
                self.ruler_icon = customtkinter.CTkButton(self.draw_frame, text="", image=icon, width=40, height=40, command=lambda shape='line': create_shape(shape))
                self.ruler_icon.grid(row=1, column=2, padx=5, pady=5, sticky='n')
                
                icon = customtkinter.CTkImage(dark_image=Image.open("imgs/polygon.png"),size=(25, 25))
                self.polygon_icon = customtkinter.CTkButton(self.draw_frame, text="", image=icon, width=40, height=40, command=lambda: self.radio_btn_var.set(4))
                self.polygon_icon.grid(row=1, column=3, padx=5, pady=5, sticky='n')
                
                icon = customtkinter.CTkImage(dark_image=Image.open("imgs/brush.png"),size=(25, 25))
                self.brush_icon = customtkinter.CTkButton(self.draw_frame, text="", image=icon, width=40, height=40, command=lambda: self.radio_btn_var.set(5))
                self.brush_icon.grid(row=1, column=4, padx=5, pady=5, sticky='n')
                
                icon = customtkinter.CTkImage(dark_image=Image.open("imgs/eraser.png"),size=(25, 25))
                self.eraser_icon = customtkinter.CTkButton(self.draw_frame, text="", image=icon, width=40, height=40, command=lambda: self.radio_btn_var.set(6))
                self.eraser_icon.grid(row=1, column=5, padx=5, pady=5, sticky='n')
                  
            def color_picker():
                def ask_color():
                    self.pick_color = AskColor() 
                    self.color_choosed = self.pick_color.get()
    
                self.color_picker_btn = customtkinter.CTkButton(master=self.draw_frame, text="choose color", command=ask_color)
                self.color_picker_btn.grid(row=2, column=0, columnspan=6, padx=10, pady=5, sticky='ew')
                
            
                
            frame()
            create_tool_btns()
            color_picker()
            create_radio_btn()
            
        

        def Thresholding():
            def frame():                
                self.thres_frame = customtkinter.CTkFrame(self.tabview_1_tab_1)
                self.thres_frame.grid(row=3, column=3, columnspan=3, rowspan=3, padx=(5,0), pady=(5,0), sticky='news')
                self.thres_frame.rowconfigure((0,1,2), weight=1)
                self.thres_frame.columnconfigure((0,1), weight=1)
                self.draw_header = self.title_toolbox(frame=self.thres_frame, title="Thresholding")
                
            def support_frame_callback(choice):
                if choice == 'None':
                    img_raw = self.master.img_raw
                if choice == 'Denoise':
                    img_raw = sitk.CurvatureFlow(self.master.img_raw)
                elif choice == 'Blurring':
                    img_raw = sitk.DiscreteGaussian(self.master.img_raw)
                elif choice == 'GrayscaleErode':
                    img_raw = sitk.GrayscaleErode(self.master.img_raw)
                elif choice == 'OtsuThreshold':
                    img_raw = sitk.OtsuThreshold(self.master.img_raw, 0, 1)
                elif choice == 'LiThreshold':
                    img_raw = sitk.LiThreshold(self.master.img_raw, 0, 1)
                elif choice == 'MomentsThreshold':
                    img_raw = sitk.MomentsThreshold(self.master.img_raw, 0, 1)
                self.master.img = sitk.GetArrayFromImage(img_raw)
            
            def support_function():
                self.support_label = customtkinter.CTkLabel(master=self.thres_frame, text="Thresholding")
                self.support_label.grid(row=1, column=0, padx=10, sticky='w')
                
                support_function_values = ["None", 'Denoise', 'Blurring', 'GrayscaleErode','OtsuThreshold', 'LiThreshold', 'MomentsThreshold']
                self.support_function_default = customtkinter.StringVar(value="None")
                self.support_function = customtkinter.CTkComboBox(master=self.thres_frame, values=support_function_values, variable=self.support_function_default, command=support_frame_callback)
                self.support_function.grid(column=1, row=1, padx=10, pady=15, sticky='we')
    
            def brightness():
                def increase_brightness():
                    cur_val = float(self.entry_brightness.get())
                    cur_val += 0.1
                    self.entry_brightness_value.set(round(cur_val,3))
                
                def decrease_brightness():
                    cur_val = float(self.entry_brightness.get())
                    cur_val -= 0.1
                    self.entry_brightness_value.set(round(cur_val,3))
                
                self.brightness = customtkinter.CTkLabel(master=self.thres_frame, text="Brightness")
                self.brightness.grid(row=2, column=0, padx=10, sticky='w')
                
                self.btn_left_decrease = customtkinter.CTkButton(master=self.thres_frame, text="-", width=25, height=25, command=decrease_brightness)
                self.btn_left_decrease.grid(column=1, row=2, sticky='nw', padx=(15,0))
                self.btn_right_increase = customtkinter.CTkButton(master=self.thres_frame, text="+", width=25, height=25, command=increase_brightness)
                self.btn_right_increase.grid(column=1, row=2, sticky='ne', padx=(0,15))
                
                self.entry_brightness_value = customtkinter.StringVar(value="1")
                self.entry_brightness = customtkinter.CTkEntry(master=self.thres_frame, placeholder_text="1", textvariable=self.entry_brightness_value)
                self.entry_brightness.grid(column=1, row=2, padx=(30,30), pady=(0,0))
                
            frame()
            support_function()
            brightness()

        def create_tabs():
            self.tabview_1 = customtkinter.CTkTabview(master=self.master)
            self.tabview_1.grid(column=0, row=10, columnspan=9, rowspan=5, padx=5, pady=5, sticky="nsew")
            # tab 1
            self.tabview_1_tab_1 = self.tabview_1.add("Image Processing")    
            self.tabview_1_tab_1.rowconfigure((0,1,2,3,4,5), weight=1)
            self.tabview_1_tab_1.columnconfigure((0,1,2,3,4,5), weight=1)
            self.tabview_1_tab_2 = self.tabview_1.add("Defect Detection")
            self.tabview_1.set("Image Processing") 
            
        create_tabs()
        ROI()
        HounsField()
        DrawingTools()
        Thresholding()
        
    def layers_management(self):
        def delete_element(element):
            self.master.draw_data['number_of_elements'] -= 1
            
            if self.master.draw_data[element]['canvas'] == 'axial':
                del(self.master.draw_data[element])
                self.master.axial.image_display(int(round(self.master.axial.slider_volume.get(),0)))
                
            elif self.master.draw_data[element]['canvas'] == 'sagittal':
                del(self.master.draw_data[element])
                self.master.sagittal.image_display(int(round(self.master.sagittal.slider_volume.get(), 0)))
                
            elif self.master.draw_data[element]['canvas'] == 'coronal':
                del(self.master.draw_data[element])
                self.master.coronal.image_display(int(round(self.master.coronal.slider_volume.get(),0)))
                
            self.layers_management()
            
        def note_analysis(layer_name):
            note = NoteWindow(
                layer_name=layer_name,
                analysis = self.master.draw_data[layer_name]['note'],
            )
            note.wait_window()
            if note.renamed_header != layer_name:
                self.master.draw_data[note.renamed_header] = self.master.draw_data[layer_name]
                del(self.master.draw_data[layer_name])
            self.master.draw_data[note.renamed_header]['note'] = note.analysis
            self.layers_management()
            
            if self.master.draw_data[note.renamed_header]['canvas'] == 'axial':
                self.master.axial.image_display(int(round(self.master.axial.slider_volume.get(),0)))
            elif self.master.draw_data[note.renamed_header]['canvas'] == 'sagittal':
                self.master.sagittal.image_display(int(round(self.master.sagittal.slider_volume.get(), 0)))
            elif self.master.draw_data[note.renamed_header]['canvas'] == 'coronal':
                self.master.coronal.image_display(int(round(self.master.coronal.slider_volume.get(),0)))
            
        data = self.master.draw_data
        for widget in self.layer_frame.winfo_children(): 
            widget.destroy()
            
        row_num = 0
        for element, data in data.items():
            if element != 'number_of_elements':
                layer = customtkinter.CTkButton(master=self.layer_frame, text=element, fg_color=self.master.second_color)
                layer.grid(row=row_num, column=0, columnspan=5, pady=5)
                
                note_icon = customtkinter.CTkImage(dark_image=Image.open("imgs/note.png"),size=(20, 20))
                note_icon = customtkinter.CTkButton(self.layer_frame, text="", image=note_icon, width=30, height=30, command=lambda element=element: note_analysis(element))
                note_icon.grid(row=row_num, column=5, padx=5, columnspan=1)
                
                bin_icon = customtkinter.CTkImage(dark_image=Image.open("imgs/bin.png"),size=(20, 20))
                bin_icon = customtkinter.CTkButton(self.layer_frame, text="", image=bin_icon, width=30, height=30, command=lambda element=element: delete_element(element))
                bin_icon.grid(row=row_num, column=6, columnspan=1)
                
            row_num += 1
                
    def TabView2(self):
        def create_tabs():
            self.tabview_2 = customtkinter.CTkTabview(master=self.master)
            self.tabview_2.grid(column=9, row=10, columnspan=9, rowspan=5, padx=5, pady=5, sticky="nsew")
            self.tabview_2_tab_1 = self.tabview_2.add("Segmentation")    
            self.tabview_2_tab_1.rowconfigure((0,1,2,3,4,5,6,7), weight=1, uniform='a')
            self.tabview_2_tab_1.columnconfigure((0,1,2,3,4,5), weight=1, uniform='a')

            self.tabview_2_tab_2 = self.tabview_2.add("3D reconstruction")
            self.tabview_2_tab_3 = self.tabview_2.add("VR/AR connection")
            self.tabview_2.set("Segmentation") 
        
        def Segmentation():
            def start_seg():
                def frame():
                    self.start_seg_frame = customtkinter.CTkFrame(master=self.tabview_2_tab_1)
                    self.start_seg_frame.grid(row=0, column=0, rowspan=4, columnspan=2, pady=(0,10), sticky='news')
                    self.start_seg_frame.columnconfigure(0, weight=1)
                    self.start_seg_frame.rowconfigure((0, 1, 2), weight=1)
                    self.start_seg_frame_header = self.title_toolbox(frame=self.start_seg_frame, title="Deep Segmentation")
                    
                def start_seg_callback():
                    if self.master.add_seg == True:
                        self.seg_progress_bar.start()
                    
                def widgets():
                    self.seg_progress_bar = customtkinter.CTkProgressBar(self.start_seg_frame, orientation="horizontal")
                    self.seg_progress_bar.set(0)
                    self.seg_progress_bar.grid(column=0, row=2, padx=(0,10), pady=(0,10), sticky='e')
                    self.start_seg_btn = customtkinter.CTkButton(self.start_seg_frame, text="Start", width=50, command=start_seg_callback)
                    self.start_seg_btn.grid(column=0, row=2, padx=(10,0), pady=(0,10), sticky='w')
                    
                    self.models = ["VAS", "Unet Attention", "U-Resnet", "Unet"]
                    self.model_picker_default = customtkinter.StringVar(value="VAS")
                    self.model_picker = customtkinter.CTkComboBox(self.start_seg_frame, values=self.models, variable=self.model_picker_default)
                    self.model_picker.grid(column=0, row=1, sticky='ew', padx=10, pady=10)
                    
                frame()
                widgets()
                
            def opacity():
                def frame():
                    self.opacity_frame = customtkinter.CTkFrame(master=self.tabview_2_tab_1)
                    self.opacity_frame.grid(row=4, column=0, rowspan=4, columnspan=2, sticky='news')
                    self.opacity_frame.columnconfigure(0, weight=1)
                    self.opacity_frame.rowconfigure((0, 1, 2), weight=1)
                    self.opacity_frame_header = self.title_toolbox(frame=self.opacity_frame, title="Opacity of Regions")
                    
                        
                def widgets():
                    def slider_opacity_callback(value):
                        self.opacity_label_var.set(f"{int(round(self.slider_opacity.get(), 0))}%")
                        
                    def increase_opacity_callback():
                        cur_val = int(round(self.slider_opacity.get(), 0))
                        cur_val += 2
                        self.slider_opacity.set(cur_val)
                        self.opacity_label_var.set(f"{cur_val}%")
                        
                    def decrease_oapcity_callback():
                        cur_val = int(round(self.slider_opacity.get(), 0))
                        cur_val -= 2
                        self.slider_opacity.set(cur_val)
                        self.opacity_label_var.set(f"{cur_val}%")
                    
                    self.slider_opacity = customtkinter.CTkSlider(master=self.opacity_frame, from_=0, to=100, command=slider_opacity_callback)
                    self.slider_opacity.set(25)
                    self.slider_opacity.grid(row=2, column=0, pady=(0,10), sticky='ew')
                    
                    self.opacity_de_btn = customtkinter.CTkButton(master=self.opacity_frame, text='-', width=35, height=35, command=decrease_oapcity_callback)
                    self.opacity_de_btn.grid(row=1, column=0, pady=(0,10), padx=10, sticky='w')
                    
                    self.opacity_in_btn = customtkinter.CTkButton(master=self.opacity_frame, text='+', width=35, height=35, command=increase_opacity_callback)
                    self.opacity_in_btn.grid(row=1, column=0, pady=(0,10), padx=10, sticky='e')
                    
                    self.opacity_label_var = customtkinter.StringVar(value="25%")
                    self.opacity_label = customtkinter.CTkLabel(master=self.opacity_frame, width=50, textvariable=self.opacity_label_var)
                    self.opacity_label.grid(row=1, column=0, pady=(0,10), padx=40)
                    
                frame()
                widgets()
                
            def regions():
                def frame():
                    self.regions_frame = customtkinter.CTkFrame(master=self.tabview_2_tab_1)
                    self.regions_frame.grid(row=0, column=2, rowspan=8, columnspan=4, padx=(5,0), sticky='news')
                    self.regions_frame.columnconfigure((0,1,2,3,4,5,6,7,8,9,10,11), weight=1)
                    self.regions_frame.rowconfigure((0,1,2,3,4,5,6,7,8), weight=1)
                    self.regions_frame_header = self.title_toolbox(frame=self.regions_frame, title="Regions Control")
                    
                def load_seg(): 
                    filtering_instance = filtering(self.master.seg)
                    self.label_arrays = filtering_instance.get()
                        
                def widgets():
                    self.region_list_vn = ['Phông nền', 'Động mạch chủ', 'Động mạch phổi', 'Tĩnh mạch phổi', 'Tâm thất trái', 'Tâm nhĩ trái', 'Tâm thất phải', 'Tấm nhĩ phải', 'Động mạch vành', 'Van 2 lá', 'Van 3 lá'] 
                    self.region_list_en = ['Background', 'Aorta', 'Pulmonary trunk', 'Pulmonary veins', 'Left ventricle', 'left atrium', 'right ventricle', 'right atrium', 'coronary artery', 'triscupid valve', 'biscupid valve']
                    # icon
                    eye_icon = customtkinter.CTkImage(dark_image=Image.open("imgs/eye.png"),size=(20, 20))
                    eye_hide_icon = customtkinter.CTkImage(dark_image=Image.open("imgs/eye_hide.png"),size=(20, 20))
                    fill_icon = customtkinter.CTkImage(dark_image=Image.open("imgs/fill.png"),size=(20, 20))
                    annotate_icon = customtkinter.CTkImage(dark_image=Image.open("imgs/annotate.png"),size=(20, 20))
                    
                    def eye_hide(class_name):
                        if self.master.class_data[class_name]['visible'] == True:
                            self.master.class_data[class_name]['visible'] = False
                            if class_name=="class1":
                                self.eye_class1.configure(image=eye_hide_icon)                        
                            elif class_name=="class2":
                                self.eye_class2.configure(image=eye_hide_icon)    
                            elif class_name=="class3":
                                self.eye_class3.configure(image=eye_hide_icon)
                            elif class_name=="class4":
                                self.eye_class4.configure(image=eye_hide_icon)
                            elif class_name=="class5":
                                self.eye_class5.configure(image=eye_hide_icon)
                            elif class_name=="class6":
                                self.eye_class6.configure(image=eye_hide_icon)
                            elif class_name=="class7":
                                self.eye_class7.configure(image=eye_hide_icon)
                            elif class_name=="class8":
                                self.eye_class8.configure(image=eye_hide_icon)
                            elif class_name=="class9":
                                self.eye_class9.configure(image=eye_hide_icon)
                            elif class_name=="class10":
                                self.eye_class10.configure(image=eye_hide_icon)
                            elif class_name=="class11":
                                self.eye_class11.configure(image=eye_hide_icon)
                        
                        else:
                            self.master.class_data[class_name]['visible'] = True
                            if class_name=="class1":
                                self.eye_class1.configure(image=eye_icon)                        
                            elif class_name=="class2":
                                self.eye_class2.configure(image=eye_icon)    
                            elif class_name=="class3":
                                self.eye_class3.configure(image=eye_icon)
                            elif class_name=="class4":
                                self.eye_class4.configure(image=eye_icon)
                            elif class_name=="class5":
                                self.eye_class5.configure(image=eye_icon)
                            elif class_name=="class6":
                                self.eye_class6.configure(image=eye_icon)
                            elif class_name=="class7":
                                self.eye_class7.configure(image=eye_icon)
                            elif class_name=="class8":
                                self.eye_class8.configure(image=eye_icon)
                            elif class_name=="class9":
                                self.eye_class9.configure(image=eye_icon)
                            elif class_name=="class10":
                                self.eye_class10.configure(image=eye_icon)
                            elif class_name=="class11":
                                self.eye_class11.configure(image=eye_icon)

                    # class1
                    self.eye_class1 = customtkinter.CTkButton(master=self.regions_frame, text="", image=eye_hide_icon, width=30, height=30, command=lambda : eye_hide(class_name="class1"))
                    self.eye_class1.grid(row=1, column=0, padx=(10,0))
                    self.fill_class1 = customtkinter.CTkButton(master=self.regions_frame, text="", image=fill_icon, width=30, height=30)
                    self.fill_class1.grid(row=1, column=1)
                    self.annotate_class1 = customtkinter.CTkButton(master=self.regions_frame, text="", image=annotate_icon, width=30, height=30)
                    self.annotate_class1.grid(row=1, column=2)
                    self.btn_class1 = customtkinter.CTkButton(master=self.regions_frame, text=self.region_list_vn[0], fg_color=self.master.second_color)
                    self.btn_class1.grid(row=1, column=3, sticky='n') 
                    
                    # class2
                    self.eye_class2 = customtkinter.CTkButton(master=self.regions_frame, text="", image=eye_hide_icon, width=30, height=30, command=lambda : eye_hide(class_name="class2"))
                    self.eye_class2.grid(row=1, column=6, padx=(10,0))
                    self.fill_class2 = customtkinter.CTkButton(master=self.regions_frame, text="", image=fill_icon, width=30, height=30)
                    self.fill_class2.grid(row=1, column=7)
                    self.annotate_class2 = customtkinter.CTkButton(master=self.regions_frame, text="", image=annotate_icon, width=30, height=30)
                    self.annotate_class2.grid(row=1, column=8)
                    self.btn_class2 = customtkinter.CTkButton(master=self.regions_frame, text=self.region_list_vn[1], fg_color=self.master.second_color)
                    self.btn_class2.grid(row=1, column=9, sticky='n') 
                    
                    # class3
                    self.eye_class3 = customtkinter.CTkButton(master=self.regions_frame, text="", image=eye_hide_icon, width=30, height=30, command=lambda : eye_hide(class_name="class3"))
                    self.eye_class3.grid(row=2, column=0, padx=(10,0))
                    self.fill_class3 = customtkinter.CTkButton(master=self.regions_frame, text="", image=fill_icon, width=30, height=30)
                    self.fill_class3.grid(row=2, column=1)
                    self.annotate_class3 = customtkinter.CTkButton(master=self.regions_frame, text="", image=annotate_icon, width=30, height=30)
                    self.annotate_class3.grid(row=2, column=2)
                    self.btn_class3 = customtkinter.CTkButton(master=self.regions_frame, text=self.region_list_vn[2], fg_color=self.master.second_color)
                    self.btn_class3.grid(row=2, column=3, sticky='n') 
                    
                    # class4
                    self.eye_class4 = customtkinter.CTkButton(master=self.regions_frame, text="", image=eye_hide_icon, width=30, height=30, command=lambda : eye_hide(class_name="class4"))
                    self.eye_class4.grid(row=2, column=6, padx=(10,0))
                    self.fill_class4 = customtkinter.CTkButton(master=self.regions_frame, text="", image=fill_icon, width=30, height=30)
                    self.fill_class4.grid(row=2, column=7)
                    self.annotate_class4 = customtkinter.CTkButton(master=self.regions_frame, text="", image=annotate_icon, width=30, height=30)
                    self.annotate_class4.grid(row=2, column=8)
                    self.btn_class4 = customtkinter.CTkButton(master=self.regions_frame, text=self.region_list_vn[3], fg_color=self.master.second_color)
                    self.btn_class4.grid(row=2, column=9, sticky='n')
                    
                    # class5
                    self.eye_class5 = customtkinter.CTkButton(master=self.regions_frame, text="", image=eye_hide_icon, width=30, height=30, command=lambda : eye_hide(class_name="class5"))
                    self.eye_class5.grid(row=3, column=0, padx=(10,0))
                    self.fill_class5 = customtkinter.CTkButton(master=self.regions_frame, text="", image=fill_icon, width=30, height=30)
                    self.fill_class5.grid(row=3, column=1)
                    self.annotate_class5 = customtkinter.CTkButton(master=self.regions_frame, text="", image=annotate_icon, width=30, height=30)
                    self.annotate_class5.grid(row=3, column=2)
                    self.btn_class5 = customtkinter.CTkButton(master=self.regions_frame, text=self.region_list_vn[4], fg_color=self.master.second_color)
                    self.btn_class5.grid(row=3, column=3, sticky='n')
                    
                    # class6
                    self.eye_class6 = customtkinter.CTkButton(master=self.regions_frame, text="", image=eye_hide_icon, width=30, height=30, command=lambda : eye_hide(class_name="class6"))
                    self.eye_class6.grid(row=3, column=6, padx=(10,0))
                    self.fill_class6 = customtkinter.CTkButton(master=self.regions_frame, text="", image=fill_icon, width=30, height=30)
                    self.fill_class6.grid(row=3, column=7)
                    self.annotate_class6 = customtkinter.CTkButton(master=self.regions_frame, text="", image=annotate_icon, width=30, height=30)
                    self.annotate_class6.grid(row=3, column=8)
                    self.btn_class6 = customtkinter.CTkButton(master=self.regions_frame, text=self.region_list_vn[5], fg_color=self.master.second_color)
                    self.btn_class6.grid(row=3, column=9, sticky='n')
                    
                    # class7
                    self.eye_class7 = customtkinter.CTkButton(master=self.regions_frame, text="", image=eye_hide_icon, width=30, height=30, command=lambda : eye_hide(class_name="class7"))
                    self.eye_class7.grid(row=4, column=0, padx=(10,0))
                    self.fill_class7 = customtkinter.CTkButton(master=self.regions_frame, text="", image=fill_icon, width=30, height=30)
                    self.fill_class7.grid(row=4, column=1)
                    self.annotate_class7 = customtkinter.CTkButton(master=self.regions_frame, text="", image=annotate_icon, width=30, height=30)
                    self.annotate_class7.grid(row=4, column=2)
                    self.btn_class7 = customtkinter.CTkButton(master=self.regions_frame, text=self.region_list_vn[6], fg_color=self.master.second_color)
                    self.btn_class7.grid(row=4, column=3, sticky='n')
                    
                    # class8
                    self.eye_class8 = customtkinter.CTkButton(master=self.regions_frame, text="", image=eye_hide_icon, width=30, height=30, command=lambda : eye_hide(class_name="class8"))
                    self.eye_class8.grid(row=4, column=6, padx=(10,0))
                    self.fill_class8 = customtkinter.CTkButton(master=self.regions_frame, text="", image=fill_icon, width=30, height=30)
                    self.fill_class8.grid(row=4, column=7)
                    self.annotate_class8 = customtkinter.CTkButton(master=self.regions_frame, text="", image=annotate_icon, width=30, height=30)
                    self.annotate_class8.grid(row=4, column=8)
                    self.btn_class8 = customtkinter.CTkButton(master=self.regions_frame, text=self.region_list_vn[7], fg_color=self.master.second_color)
                    self.btn_class8.grid(row=4, column=9, sticky='n')
                    
                    # class9
                    self.eye_class9 = customtkinter.CTkButton(master=self.regions_frame, text="", image=eye_hide_icon, width=30, height=30, command=lambda : eye_hide(class_name="class9"))
                    self.eye_class9.grid(row=5, column=0, padx=(10,0))
                    self.fill_class9 = customtkinter.CTkButton(master=self.regions_frame, text="", image=fill_icon, width=30, height=30)
                    self.fill_class9.grid(row=5, column=1)
                    self.annotate_class9 = customtkinter.CTkButton(master=self.regions_frame, text="", image=annotate_icon, width=30, height=30)
                    self.annotate_class9.grid(row=5, column=2)
                    self.btn_class9 = customtkinter.CTkButton(master=self.regions_frame, text=self.region_list_vn[8], fg_color=self.master.second_color)
                    self.btn_class9.grid(row=5, column=3, sticky='n')
                    
                    # class10
                    self.eye_class10 = customtkinter.CTkButton(master=self.regions_frame, text="", image=eye_hide_icon, width=30, height=30, command=lambda : eye_hide(class_name="class10"))
                    self.eye_class10.grid(row=5, column=6, padx=(10,0))
                    self.fill_class10 = customtkinter.CTkButton(master=self.regions_frame, text="", image=fill_icon, width=30, height=30)
                    self.fill_class10.grid(row=5, column=7)
                    self.annotate_class10 = customtkinter.CTkButton(master=self.regions_frame, text="", image=annotate_icon, width=30, height=30)
                    self.annotate_class10.grid(row=5, column=8)
                    self.btn_class10 = customtkinter.CTkButton(master=self.regions_frame, text=self.region_list_vn[9], fg_color=self.master.second_color)
                    self.btn_class10.grid(row=5, column=9, sticky='n')
                    
                    # class11
                    self.eye_class11 = customtkinter.CTkButton(master=self.regions_frame, text="", image=eye_hide_icon, width=30, height=30, command=lambda : eye_hide(class_name="class11"))
                    self.eye_class11.grid(row=6, column=0, padx=(10,0))
                    self.fill_class11 = customtkinter.CTkButton(master=self.regions_frame, text="", image=fill_icon, width=30, height=30)
                    self.fill_class11.grid(row=6, column=1)
                    self.annotate_class11 = customtkinter.CTkButton(master=self.regions_frame, text="", image=annotate_icon, width=30, height=30)
                    self.annotate_class11.grid(row=6, column=2)
                    self.btn_class11 = customtkinter.CTkButton(master=self.regions_frame, text=self.region_list_vn[10], fg_color=self.master.second_color)
                    self.btn_class11.grid(row=6, column=3, sticky='n')

                               
                frame()
                if self.master.add_seg == True:
                    load_seg()
                    widgets()
            
            start_seg()
            opacity()
            regions()
            
        create_tabs()
        Segmentation()
    
class App(customtkinter.CTk):
    def __init__(self, title, logo_path):
        super().__init__()
        self.title(title)
        self.width = int(self.winfo_screenwidth()/1.05)
        self.height = int(self.winfo_screenheight()/1.1)
        self.geometry(f"{self.width}x{self.height}")
        self.minsize(500, 500)
        self.iconbitmap(logo_path)
        
        self.first_color = "#2b2b2b"
        self.second_color = "#3b3b3b"
        self.text_disabled_color = "#dce4e2"
        self.text_canvas_color = "yellow"
        
        self.img = None
        self.img_raw = None

        self.seg = None
        self.seg_raw = None
        self.add_seg = False
        
        self.dict_info = {
            "Organization": "Benh vien Cho Ray",
            "Patient's name": "Ton That Hung",
            "Modality": "MRI",
            "Patient ID": "0000097031",
            "Body Part Examined": "CHEST_TO_PELVIS",
            "Acquisition Date": "20231019"
        }
        self.pixel_spacing = 0.858
        self.path = ''
        self.path_seg = ''
        
        # Data
        self.class_data = {
            'class1':{
                'visible': False,
                'color': '#FFFFFF',
            },
            'class2':{
                'visible': False,
                'color': '#FFFFFF',
            },
            'class3':{
                'visible': False,
                'color': '#FFFFFF',
            },
            'class4':{
                'visible': False,
                'color': '#FFFFFF',
            },
            'class5':{
                'visible': False,
                'color': '#FFFFFF',
            },
            'class6':{
                'visible': False,
                'color': '#FFFFFF',
            },
            'class7':{
                'visible': False,
                'color': '#FFFFFF',
            },
            'class8':{
                'visible': False,
                'color': '#FFFFFF',
            },
            'class9':{
                'visible': False,
                'color': '#FFFFFF',
            },
            'class10':{
                'visible': False,
                'color': '#FFFFFF',
            },
            'class11':{
                'visible': False,
                'color': '#FFFFFF',
            }
        }
        
        self.ROI_data = {
            'axial': {
                'rec': {
                    'x1': 50,
                    'y1': 50,
                    'x2': 500,
                    'y2': 500,
                },
                'nw': {
                    'x': 0,
                    'y': 0,
                },
                'ne': {
                    'x': 0,
                    'y': 0,
                },
                'sw': {
                    'x': 0,
                    'y': 0,
                },
                'se': {
                    'x': 0,
                    'y': 0,
                }
            },
            'sagittal': {
                'rec': {
                'x1': 50,
                'y1': 50,
                'x2': 500,
                'y2': 500,
                },
                'nw': {
                    'x': 0,
                    'y': 0,
                },
                'ne': {
                    'x': 0,
                    'y': 0,
                },
                'sw': {
                    'x': 0,
                    'y': 0,
                },
                'se': {
                    'x': 0,
                    'y': 0,
                }
            },
            'coronal': {
                'rec': {
                'x1': 50,
                'y1': 50,
                'x2': 500,
                'y2': 500,
                },
                'nw': {
                    'x': 0,
                    'y': 0,
                },
                'ne': {
                    'x': 0,
                    'y': 0,
                },
                'sw': {
                    'x': 0,
                    'y': 0,
                },
                'se': {
                    'x': 0,
                    'y': 0,
                }
            }
        }
        self.analysis_data = {
            'number': 0,
        }
        self.draw_data = {}
        
        
        # column and rows
        for i in range(15):
            self.rowconfigure(i, weight=1, uniform='a')
            
        for i in range(18):
            self.columnconfigure(i, weight=1, uniform='a')
            
        for i in range(15):
            for j in range(18):
                label = customtkinter.CTkFrame(self, fg_color="transparent")
                label.grid(row=i, column=j, sticky='nsew')

        # create menu
        self.menu_bar = MenuBar(self)
        self.tools = Tools(self)
        
        def update_app(event):
            
            self.draw_data = {
                'number_of_elements': 1, 
                'Bất thường 1': {
                    'canvas': 'axial',
                    'type': 'rectangle',
                    'slice': 100,
                    'x1': 100,
                    'y1': 100,
                    'x2': 300,
                    'y2': 300,
                    'color': 'red',
                    'note': "default analysis",
                }
            }
            
            def update_hounsfield():
                self.tools.hounsfield_slider.configure(from_=np.min(self.img))
                self.tools.hounsfield_slider.configure(to=np.max(self.img))
                self.tools.hounsfield_slider.set([np.min(self.img), np.max(self.img)])
                self.tools.btn_left_entry.configure(placeholder_text=np.min(self.img))
                self.tools.btn_right_entry.configure(placeholder_text=np.max(self.img))
    
            self.axial = CanvasAxial(self)
            self.sagittal = CanvasSagittal(self)
            self.coronal = CanvasCoronal(self)
            self.tools = Tools(self)
            update_hounsfield()
            
        def update_app_2(event):
            self.draw_data = {
                'number_of_elements': 1, 
                'Bất thường 1': {
                    'canvas': 'axial',
                    'type': 'rectangle',
                    'slice': 100,
                    'x1': 100,
                    'y1': 100,
                    'x2': 300,
                    'y2': 300,
                    'color': 'red',
                    'note': "default analysis",
                }
            }
            
            def update_hounsfield():
                self.tools.hounsfield_slider.configure(from_=np.min(self.img))
                self.tools.hounsfield_slider.configure(to=np.max(self.img))
                self.tools.hounsfield_slider.set([np.min(self.img), np.max(self.img)])
                self.tools.btn_left_entry.configure(placeholder_text=np.min(self.img))
                self.tools.btn_right_entry.configure(placeholder_text=np.max(self.img))
                
            self.tools = Tools(self)
            self.axial = CanvasAxial(self)
            self.sagittal = CanvasSagittal(self)
            self.coronal = CanvasCoronal(self)
            update_hounsfield()  
            
        self.bind("<<UpdateApp>>", update_app)
        self.bind("<<UpdateApp2>>", update_app_2)
        self.mainloop()
        
        # Save latest data here
        print(self.ROI_data)
        print(self.draw_data)
        print(self.class_data)
        print(self.analysis_data)

app = App(
    title='VasculAR software',
    logo_path='imgs/logo.ico'
)


'''
        Data saved into .vas:
            patient_data.json --> dict into
            draw_data.json --> draw_data
            ROI_data.json --> ROI_data
            Photo_data.json --> analysis_data
                save into pdf (if on that slice there is a analysis box text --> write on the pdf too + 1 page for patient info)
        Database on firebase:
            4 files of json + 1 pdf
            1 for databse management:
            'patient_name':
            'date'
            'modality'
            'times': 
            'path_to_file_vas -> clicked --> automate open the zip vas with analysis
'''