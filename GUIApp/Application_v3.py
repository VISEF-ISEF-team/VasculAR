'''
VasculAR software
Author: Nguyen Le Quoc Bao & Le Tuan Hy
Version: 0.3
Competition: Visef & Isef
'''

import customtkinter
import tkinter
from tkinter import filedialog, Canvas
from CTkRangeSlider import *
from CTkColorPicker import *
from NoteAnalysis import NoteWindow 
from pdf_save import create_pdf
from data_manager import DataManager
from defect_detection import DiseaseDectection
from defect_education import defectEducation
from PIL import Image, ImageTk, ImageGrab
import SimpleITK as sitk
from readdcm import ReadDCM
import cv2
import numpy as np
import matplotlib.pyplot as plt
from cloud_database import LoginPage
import pyrebase
import os
import webcolors
import json
import subprocess
import sys

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
data_manager = DataManager()

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
                    'open_vas_file': 'Open Vas File',
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
            'Database': {
                'main_menu': {
                    'instance_name': 'database_btn',
                    'label_name': 'Database', 
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
    
    def open_vas(self):
        vas_file_path = filedialog.askopenfilename()
        if vas_file_path.endswith('.vas'):
            
            loaded_default_data = self.master.data_manager.load_saved_vas_data(vas_file_path)
            self.master.dict_info = loaded_default_data["dict_info.json"]
            self.master.analysis_data = loaded_default_data["analysis_data.json"]
            self.master.class_data = loaded_default_data["class_data.json"]
            self.master.draw_data = loaded_default_data["draw_data.json"]
            self.master.ROI_data = loaded_default_data["ROI_data.json"]
            self.master.paths = loaded_default_data["paths.json"]
            self.master.folder_imgs = loaded_default_data["folder_imgs.json"]
            
            # Load image
            self.master.img_raw = sitk.ReadImage(self.master.paths['image_path'], sitk.sitkFloat32)
            self.master.img = sitk.GetArrayFromImage(self.master.img_raw)
            
            # Load segmentation
            self.master.specified_data = os.path.basename(self.master.paths['image_path']).split('_')[1]
            self.master.paths['folder_seg'] 
            self.master.add_seg = True
            for file in os.listdir(self.master.paths['folder_seg']):
                if file.endswith('.nii.gz'):
                    img_raw = sitk.ReadImage( self.master.paths['folder_seg'] + '/' + file, sitk.sitkFloat32)
                    self.master.seg_imgs.append(sitk.GetArrayFromImage(img_raw))
            self.master.event_generate("<<UpdateApp2>>") 

            
    def choose_file(self):
        self.master.paths['image_path'] = filedialog.askopenfilename()
        self.master.specified_data = os.path.basename(self.master.paths['image_path']).split('_')[1]
        
        if self.master.paths['image_path'].endswith('.nii.gz') or self.master.paths['image_path'].endswith('.nii'):
            par_dir = os.path.dirname(self.master.paths['image_path'])
            self.master.dict_info = self.master.data_manager.load_dict_info_data(par_dir + '/dict_info.json')
            self.master.img_raw = sitk.ReadImage(self.master.paths['image_path'], sitk.sitkFloat32)
            self.master.img = sitk.GetArrayFromImage(self.master.img_raw)
        
        elif self.master.paths['image_path'].endswith('.dcm'):
            parent_dir = os.path.dirname(self.master.paths['image_path'])
            instance = ReadDCM(parent_dir)
            self.master.img_raw, self.master.img, self.master.dict_info, self.master.pixel_spacing = instance.read_file_dcm()
            print(self.master.dict_info)
            
        self.hide_all_menu()
        self.master.event_generate("<<UpdateApp>>")
        
    def export_analysis(self):
        print(self.master.analysis_data)
        create_pdf(package=self.master.analysis_data)
        
    def save_case(self):
        # save local
        directory = filedialog.askdirectory()
        if directory != None:
            self.master.data_manager.save_after_data(
                file_name=f'ct_{self.master.specified_data}_saved',
                directory=directory,
                ROI_data=self.master.ROI_data,
                draw_data=self.master.draw_data,
                class_data=self.master.class_data,
                analysis_data=self.master.analysis_data,
                dict_info=self.master.dict_info,
                paths=self.master.paths,
                folder_imgs=self.master.folder_imgs,
            )
            
        # auto save on cloud
        case = {
            "file_name" : f'ct_{self.master.specified_data}_saved',
            "directory" : directory,
            "ROI_data" : self.master.ROI_data,
            "draw_data" : self.master.draw_data,
            "class_data" : self.master.class_data,
            "analysis_data" : self.master.analysis_data,
            "dict_info" : self.master.dict_info,
            "paths" : self.master.paths,
            "folder_imgs": self.master.folder_imgs,
        }
        db.child(f"case_{self.master.specified_data}").set(case)
    
        
    def dropdown_options(self, instance, master):            
        for row, (instance_name, label_name) in enumerate(self.data[instance]['sub_menu'].items()):
            if instance_name == 'open_vas_file':
                self.menu_item['sub_menu'][instance_name] = customtkinter.CTkButton(
                    master=master, 
                    text=label_name,
                    fg_color='transparent', 
                    hover_color=self.master.second_color,
                    command = lambda: self.open_vas(),
                )
            elif instance_name == 'add_nifti_file_btn': 
                self.menu_item['sub_menu'][instance_name] = customtkinter.CTkButton(
                    master=master, 
                    text=label_name,
                    fg_color='transparent', 
                    hover_color=self.master.second_color,
                    command = lambda: self.choose_file(),
                )
            elif instance_name == 'save_case_btn': 
                self.menu_item['sub_menu'][instance_name] = customtkinter.CTkButton(
                    master=master, 
                    text=label_name,
                    fg_color='transparent', 
                    hover_color=self.master.second_color,
                    command = lambda: self.save_case(),
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
        if widget_option.cget("text") != 'Database' and widget_option.cget("text") != 'Account':
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

        
        elif widget_option.cget("text") == 'Database':
            # run command line 
            venv_activate_script = os.path.join('D:/Documents/GitHub/VascuIAR/.venv/Scripts', 'activate')
            if sys.platform.startswith('win'):
                activation_command = f"call {venv_activate_script}"
                start_command = "start"
            else:
                activation_command = f"source {venv_activate_script}"
                start_command = "x-terminal-emulator -e"

            command = f"{activation_command} && python run_database.py"
            subprocess.run(command, shell=True)
            
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
            if element != 'number_of_elements' and data['slice'] == int(round(self.slider_volume.get(), 0)) and data['canvas'] == 'axial':
                if (f'canvas_{index}' not in self.master.analysis_data):
                    self.master.analysis_data[f'canvas_{index}'] = {}
                self.master.analysis_data[f'canvas_{index}'][element] = data['note']
                print(self.master.analysis_data)

        # save file
        x = self.master.winfo_rootx() + self.canvas.winfo_x() + 7 
        y = self.master.winfo_rooty() + self.canvas.winfo_y() + 100 
        x1 = x + self.canvas.winfo_width()*1.255 
        y1 = y + self.canvas.winfo_height()*1.255  
        ImageGrab.grab().crop((x,y,x1,y1)).save(f"canvas_{index}.png")
        self.master.analysis_data['number'] = index + 1
        
        # save on cloud
        filename = f"case_{self.master.specified_data}/canvas_{index}"
        storage.child(filename).put(f"D:/Documents/GitHub/VascuIAR/GUIApp/canvas_{index}.png")

        # save link to database
        print(self.master.folder_imgs)
        image_url = storage.child(filename).get_url(None)
        if f"case_{self.master.specified_data}" not in self.master.folder_imgs:
            self.master.folder_imgs[f"case_{self.master.specified_data}"] = {}
        self.master.folder_imgs[f"case_{self.master.specified_data}"][f"canvas_{index}"] = image_url
        print(self.master.folder_imgs)
    
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
                image_position = self.canvas.coords(self.canvas_item_1)
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
        def transparent_background(image, index):
            hex_color = self.master.class_data[f'class{index+1}']['color']
            rgba_color = webcolors.hex_to_rgb(hex_color) + (255,)
            alpha_channel = (image != 0).astype(np.uint8) * 255
            RGBimage = np.stack([np.ones_like(image) * rgba_color[0],
                                np.ones_like(image) * rgba_color[1],
                                np.ones_like(image) * rgba_color[2]], axis=-1)
            RGBAimage = np.concatenate([RGBimage, alpha_channel[..., np.newaxis]], axis=-1)
            img = Image.fromarray(RGBAimage, 'RGBA')
            return img
        
        def create_image_alpha(x, y, image, image_seg):
            if self.master.add_seg == False:
                self.images.append(ImageTk.PhotoImage(image))
                self.canvas_item_1 = self.canvas.create_image(x, y, image=self.images[-1], anchor='center')
            else:
                # xử lý segmentation
                seg = []
                for index in range(len(image_seg)):
                    gray = np.array(image_seg[index][0].convert('L')) 
                    seg.append(transparent_background(gray, index=image_seg[index][1]))
                 
                self.images.append(ImageTk.PhotoImage(image))
                self.canvas_item_1 = self.canvas.create_image(x, y, image=self.images[-1], anchor='center')

                self.canvas_item_seg = []
                for item in seg:
                    self.images.append(ImageTk.PhotoImage(item))
                    self.canvas_item_seg.append(self.canvas.create_image(x, y, image=self.images[-1], anchor='center'))             
                
        def return_img_seg(image, index, color_choice, height):
            image_seg = image[int(index_slice),:, :]
            image_seg = np.where(image_seg == 1., image_seg, 0)
            image_seg = Image.fromarray(image_seg * 255).convert('L')
            image_seg.save(f"temp{index}.png", "PNG", transparency=0)
            plt.imsave(f"temp{index}.png", image_seg, cmap=color_choice)
            image_display_seg = cv2.imread(f"temp{index}.png")
            brightness_image_seg = cv2.convertScaleAbs(image_display_seg, alpha=float(self.master.tools.entry_brightness_value.get()), beta=0)
            cv2.imwrite(f"temp{index}.png", brightness_image_seg)
            image_display_seg = Image.open(f"temp{index}.png").resize((height, height))
            image_display_seg = image_display_seg.rotate(rotation_angle)
            
            if horizontal == "horizontal":
                image_display = image_display.transpose(Image.FLIP_LEFT_RIGHT)
                image_display_seg = image_display_seg.transpose(Image.FLIP_LEFT_RIGHT)
            if vertical == "vertical":
                image_display = image_display.transpose(Image.FLIP_TOP_BOTTOM)
                image_display_seg = image_display_seg.transpose(Image.FLIP_TOP_BOTTOM)
                
            return image_display_seg

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
            image_seg = []
            for index in range(0,12,1):
                if self.master.class_data[f"class{index+1}"]['visible'] == True:
                    image_seg.append((return_img_seg(self.master.seg_imgs[index], index=index, height=height, color_choice=color_choice), index))
            
            x_cord, y_cord = image_position()
            create_image_alpha(x_cord, y_cord, image_display, image_seg)

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
                for item in self.canvas_item_seg:
                    self.canvas.move(item, -10, 0)     
            def right():
                self.canvas.move(self.canvas_item_1, 10, 0)
                for item in self.canvas_item_seg:
                    self.canvas.move(item, 10, 0)     
            def up():
                self.canvas.move(self.canvas_item_1, 0, -10)
                for item in self.canvas_item_seg:
                    self.canvas.move(item, 0, -10)     
            def down():
                self.canvas.move(self.canvas_item_1, 0, 10)
                for item in self.canvas_item_seg:
                    self.canvas.move(item, 0, 10)     
                
                
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
        # save into database
        index = self.master.analysis_data['number']
        for element, data in self.master.draw_data.items():
            if element != 'number_of_elements' and data['slice'] == int(round(self.slider_volume.get(), 0)) and data['canvas'] == 'sagittal':
                if (f'canvas_{index}' not in self.master.analysis_data):
                    self.master.analysis_data[f'canvas_{index}'] = {}
                self.master.analysis_data[f'canvas_{index}'][element] = data['note']

        # save file
        x = self.master.winfo_rootx() + self.canvas.winfo_x() + 860
        y = self.master.winfo_rooty() + self.canvas.winfo_y() + 100 
        x1 = x + self.canvas.winfo_width()*1.255 
        y1 = y + self.canvas.winfo_height()*1.255  
        ImageGrab.grab().crop((x,y,x1,y1)).save(f"canvas_{index}.png")
        self.master.analysis_data['number'] = index + 1
        
        # save on cloud
        filename = f"case_{self.master.specified_data}/canvas_{index}"
        storage.child(filename).put(f"D:/Documents/GitHub/VascuIAR/GUIApp/canvas_{index}.png")

        # save link to database
        print(self.master.folder_imgs)
        image_url = storage.child(filename).get_url(None)
        if f"case_{self.master.specified_data}" not in self.master.folder_imgs:
            self.master.folder_imgs[f"case_{self.master.specified_data}"] = {}
        self.master.folder_imgs[f"case_{self.master.specified_data}"][f"canvas_{index}"] = image_url
        
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
                image_position = self.canvas.coords(self.canvas_item_1)
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
        def transparent_background(image, index):
            hex_color = self.master.class_data[f'class{index+1}']['color']
            rgba_color = webcolors.hex_to_rgb(hex_color) + (255,)
            alpha_channel = (image != 0).astype(np.uint8) * 255
            RGBimage = np.stack([np.ones_like(image) * rgba_color[0],
                                np.ones_like(image) * rgba_color[1],
                                np.ones_like(image) * rgba_color[2]], axis=-1)
            RGBAimage = np.concatenate([RGBimage, alpha_channel[..., np.newaxis]], axis=-1)
            img = Image.fromarray(RGBAimage, 'RGBA')
            return img
        
        def create_image_alpha(x, y, image, image_seg):
            if self.master.add_seg == False:
                self.images.append(ImageTk.PhotoImage(image))
                self.canvas_item_1 = self.canvas.create_image(x, y, image=self.images[-1], anchor='center')
            else:
                # opacity = int(round(self.master.tools.slider_opacity.get(), 0)) / 100
                # alpha_seg = int(opacity * 255)
                # image_seg[3] = image_seg[3].convert('RGBA')
                # image_seg[3].putalpha(alpha_seg)
                
                # xử lý segmentation
                seg = []
                for index in range(len(image_seg)):
                    gray = np.array(image_seg[index][0].convert('L')) 
                    seg.append(transparent_background(gray, index=image_seg[index][1]))
                 
                self.images.append(ImageTk.PhotoImage(image))
                self.canvas_item_1 = self.canvas.create_image(x, y, image=self.images[-1], anchor='center')

                self.canvas_item_seg = []
                for item in seg:
                    self.images.append(ImageTk.PhotoImage(item))
                    self.canvas_item_seg.append(self.canvas.create_image(x, y, image=self.images[-1], anchor='center'))             
                
        def return_img_seg(image, index, color_choice, height):
            image_seg = image[:, int(index_slice), :]
            image_seg = np.where(image_seg == 1., image_seg, 0)
            image_seg = Image.fromarray(image_seg * 255).convert('L')
            image_seg.save(f"temp{index}.png", "PNG", transparency=0)
            plt.imsave(f"temp{index}.png", image_seg, cmap=color_choice)
            image_display_seg = cv2.imread(f"temp{index}.png")
            brightness_image_seg = cv2.convertScaleAbs(image_display_seg, alpha=float(self.master.tools.entry_brightness_value.get()), beta=0)
            cv2.imwrite(f"temp{index}.png", brightness_image_seg)
            image_display_seg = Image.open(f"temp{index}.png").resize((height, height))
            image_display_seg = image_display_seg.rotate(rotation_angle)
            
            if horizontal == "horizontal":
                image_display = image_display.transpose(Image.FLIP_LEFT_RIGHT)
                image_display_seg = image_display_seg.transpose(Image.FLIP_LEFT_RIGHT)
            if vertical == "vertical":
                image_display = image_display.transpose(Image.FLIP_TOP_BOTTOM)
                image_display_seg = image_display_seg.transpose(Image.FLIP_TOP_BOTTOM)
                
            return image_display_seg


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
            image_seg = []
            for index in range(0,12,1):
                if self.master.class_data[f"class{index+1}"]['visible'] == True:
                    image_seg.append((return_img_seg(self.master.seg_imgs[index], index=index, height=height, color_choice=color_choice), index))
            
            x_cord, y_cord = image_position()
            create_image_alpha(x_cord, y_cord, image_display, image_seg)

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
                for item in self.canvas_item_seg:
                    self.canvas.move(item, -10, 0)     
            def right():
                self.canvas.move(self.canvas_item_1, 10, 0)
                for item in self.canvas_item_seg:
                    self.canvas.move(item, 10, 0)     
            def up():
                self.canvas.move(self.canvas_item_1, 0, -10)
                for item in self.canvas_item_seg:
                    self.canvas.move(item, 0, -10)     
            def down():
                self.canvas.move(self.canvas_item_1, 0, 10)
                for item in self.canvas_item_seg:
                    self.canvas.move(item, 0, 10) 
                
                
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
        # save into database
        index = self.master.analysis_data['number']
        for element, data in self.master.draw_data.items():
            if element != 'number_of_elements' and data['slice'] == int(round(self.slider_volume.get(), 0)) and data['canvas'] == 'coronal':
                if (f'canvas_{index}' not in self.master.analysis_data):
                    self.master.analysis_data[f'canvas_{index}'] = {}
                self.master.analysis_data[f'canvas_{index}'][element] = data['note']

        # save file
        x = self.master.winfo_rootx() + self.canvas.winfo_x() + 1710
        y = self.master.winfo_rooty() + self.canvas.winfo_y() + 100 
        x1 = x + self.canvas.winfo_width()*1.255 
        y1 = y + self.canvas.winfo_height()*1.255  
        ImageGrab.grab().crop((x,y,x1,y1)).save(f"canvas_{index}.png")
        self.master.analysis_data['number'] = index + 1
        
        # save on cloud
        filename = f"case_{self.master.specified_data}/canvas_{index}"
        storage.child(filename).put(f"D:/Documents/GitHub/VascuIAR/GUIApp/canvas_{index}.png")

        # save link to database
        print(self.master.folder_imgs)
        image_url = storage.child(filename).get_url(None)
        if f"case_{self.master.specified_data}" not in self.master.folder_imgs:
            self.master.folder_imgs[f"case_{self.master.specified_data}"] = {}
        self.master.folder_imgs[f"case_{self.master.specified_data}"][f"canvas_{index}"] = image_url

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
                image_position = self.canvas.coords(self.canvas_item_1)
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
        def transparent_background(image, index):
            hex_color = self.master.class_data[f'class{index+1}']['color']
            rgba_color = webcolors.hex_to_rgb(hex_color) + (255,)
            alpha_channel = (image != 0).astype(np.uint8) * 255
            RGBimage = np.stack([np.ones_like(image) * rgba_color[0],
                                np.ones_like(image) * rgba_color[1],
                                np.ones_like(image) * rgba_color[2]], axis=-1)
            RGBAimage = np.concatenate([RGBimage, alpha_channel[..., np.newaxis]], axis=-1)
            img = Image.fromarray(RGBAimage, 'RGBA')
            return img
        
        def create_image_alpha(x, y, image, image_seg):
            if self.master.add_seg == False:
                self.images.append(ImageTk.PhotoImage(image))
                self.canvas_item_1 = self.canvas.create_image(x, y, image=self.images[-1], anchor='center')
            else:
                # opacity = int(round(self.master.tools.slider_opacity.get(), 0)) / 100
                # alpha_seg = int(opacity * 255)
                # image_seg[3] = image_seg[3].convert('RGBA')
                # image_seg[3].putalpha(alpha_seg)
                
                # xử lý segmentation
                seg = []
                for index in range(len(image_seg)):
                    gray = np.array(image_seg[index][0].convert('L')) 
                    seg.append(transparent_background(gray, index=image_seg[index][1]))
                 
                self.images.append(ImageTk.PhotoImage(image))
                self.canvas_item_1 = self.canvas.create_image(x, y, image=self.images[-1], anchor='center')

                self.canvas_item_seg = []
                for item in seg:
                    self.images.append(ImageTk.PhotoImage(item))
                    self.canvas_item_seg.append(self.canvas.create_image(x, y, image=self.images[-1], anchor='center'))            
                
        def return_img_seg(image, index, color_choice, height):
            image_seg = image[:,:, int(index_slice)]
            image_seg = np.where(image_seg == 1., image_seg, 0)
            image_seg = Image.fromarray(image_seg * 255).convert('L')
            image_seg.save(f"temp{index}.png", "PNG", transparency=0)
            plt.imsave(f"temp{index}.png", image_seg, cmap=color_choice)
            image_display_seg = cv2.imread(f"temp{index}.png")
            brightness_image_seg = cv2.convertScaleAbs(image_display_seg, alpha=float(self.master.tools.entry_brightness_value.get()), beta=0)
            cv2.imwrite(f"temp{index}.png", brightness_image_seg)
            image_display_seg = Image.open(f"temp{index}.png").resize((height, height))
            image_display_seg = image_display_seg.rotate(rotation_angle)
            
            if horizontal == "horizontal":
                image_display = image_display.transpose(Image.FLIP_LEFT_RIGHT)
                image_display_seg = image_display_seg.transpose(Image.FLIP_LEFT_RIGHT)
            if vertical == "vertical":
                image_display = image_display.transpose(Image.FLIP_TOP_BOTTOM)
                image_display_seg = image_display_seg.transpose(Image.FLIP_TOP_BOTTOM)
                
            return image_display_seg

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
            image_seg = []
            for index in range(0,12,1):
                if self.master.class_data[f"class{index+1}"]['visible'] == True:
                    image_seg.append((return_img_seg(self.master.seg_imgs[index], index=index, height=height, color_choice=color_choice), index))
            
            x_cord, y_cord = image_position()
            create_image_alpha(x_cord, y_cord, image_display, image_seg)

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
                for item in self.canvas_item_seg:
                    self.canvas.move(item, -10, 0)     
            def right():
                self.canvas.move(self.canvas_item_1, 10, 0)
                for item in self.canvas_item_seg:
                    self.canvas.move(item, 10, 0)     
            def up():
                self.canvas.move(self.canvas_item_1, 0, -10)
                for item in self.canvas_item_seg:
                    self.canvas.move(item, 0, -10)     
            def down():
                self.canvas.move(self.canvas_item_1, 0, 10)
                for item in self.canvas_item_seg:
                    self.canvas.move(item, 0, 10) 
                
                
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
                self.check_ROI_frame = customtkinter.CTkFrame(master=self.tabview_1_tab_1, fg_color=self.master.third_color)
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
                self.hounsfield_frame = customtkinter.CTkFrame(master=self.tabview_1_tab_1, fg_color=self.master.third_color)
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
                self.layer_frame = customtkinter.CTkScrollableFrame(self.tabview_1_tab_1, label_text='Layer elements', fg_color=self.master.third_color)
                self.layer_frame.grid(row=0, column=2, columnspan=1, rowspan=6, padx=(5,0), sticky='news')
                self.layer_frame.columnconfigure((0,1,2,3,4,5,6), weight=1)
                
                self.draw_frame = customtkinter.CTkFrame(self.tabview_1_tab_1, fg_color=self.master.third_color)
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
                self.thres_frame = customtkinter.CTkFrame(self.tabview_1_tab_1, fg_color=self.master.third_color)
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
            self.tabview_1_tab_2.rowconfigure((0,1,2,3,4,5), weight=1)
            self.tabview_1_tab_2.columnconfigure((0,1,2,3,4,5), weight=1)
            self.tabview_1.set("Image Processing") 
            
        def Defects():
            # defect frame and header
            self.defect_frame = customtkinter.CTkFrame(master=self.tabview_1_tab_2, fg_color=self.master.third_color)
            self.defect_frame.grid(column=0, row=0, columnspan=3, rowspan=3, pady=(0,5), sticky='news')
            self.defect_frame.rowconfigure((0,1,2,3,4,5), weight=1)
            self.defect_frame.columnconfigure((0,1,2), weight=1)
            self.defect_header = self.title_toolbox(frame=self.defect_frame, title='Types all structural diseases')
            
            
            def open_defect_info(value):
                # https://www.rch.org.au/cardiology/heart_defects/Patent_Ductus_Arteriosus_PDA/
                self.defect_info_window = defectEducation(parent=self.master, info=self.master.data_defects[value])
                

            self.defect_var = tkinter.IntVar(value=0)
            defect_1 = customtkinter.CTkRadioButton(self.defect_frame, text="Thông liên thất", variable= self.defect_var, value=1)
            defect_1.grid(row=1, column=0, padx=(10,0), pady=10, sticky='w')
            defect_info_1 = customtkinter.CTkButton(self.defect_frame, text="i", width=20, height=20, command=lambda: open_defect_info(value=1))
            defect_info_1.grid(row=1, column=0, padx=(0,5), pady=10, sticky='e')
            
            defect_2 = customtkinter.CTkRadioButton(self.defect_frame, text="Còn ống động mạch", variable= self.defect_var, value=2)
            defect_2.grid(row=1, column=1, padx=(10,0), pady=10, sticky='w')
            defect_info_2 = customtkinter.CTkButton(self.defect_frame, text="i", width=20, height=20, command=lambda: open_defect_info(value=2))
            defect_info_2.grid(row=1, column=1, padx=(0,5), pady=10, sticky='e')
            
            defect_3 = customtkinter.CTkRadioButton(self.defect_frame, text="Thân chung động mạch", variable= self.defect_var, value=3)
            defect_3.grid(row=1, column=2, padx=(10,0), pady=10, sticky='w')
            defect_info_3 = customtkinter.CTkButton(self.defect_frame, text="i", width=20, height=20, command=lambda: open_defect_info(value=3))
            defect_info_3.grid(row=1, column=2, padx=(0,5), pady=10, sticky='e')
            
            defect_4 = customtkinter.CTkRadioButton(self.defect_frame, text="Bất thường động mạch vành", variable= self.defect_var, value=4)
            defect_4.grid(row=2, column=0, padx=(10,0), pady=10, sticky='w')
            defect_info_4 = customtkinter.CTkButton(self.defect_frame, text="i", width=20, height=20, command=lambda: open_defect_info(value=4))
            defect_info_4.grid(row=2, column=0, padx=(0,5), pady=10, sticky='e')
            
            defect_5 = customtkinter.CTkRadioButton(self.defect_frame, text="Phình động mạch", variable= self.defect_var, value=5)
            defect_5.grid(row=2, column=1, padx=(10,0), pady=10, sticky='w')
            defect_info_5 = customtkinter.CTkButton(self.defect_frame, text="i", width=20, height=20, command=lambda: open_defect_info(value=5))
            defect_info_5.grid(row=2, column=1, padx=(0,5), pady=10, sticky='e')
            
            defect_6 = customtkinter.CTkRadioButton(self.defect_frame, text="Tĩnh mạch chủ kép", variable= self.defect_var, value=6)
            defect_6.grid(row=2, column=2, padx=(10,0), pady=10, sticky='w')
            defect_info_6 = customtkinter.CTkButton(self.defect_frame, text="i", width=20, height=20, command=lambda: open_defect_info(value=6))
            defect_info_6.grid(row=2, column=2, padx=(0,5), pady=10, sticky='e')
            
            defect_7 = customtkinter.CTkRadioButton(self.defect_frame, text="Tĩnh mạch phổi trở về tuần hoàn", variable= self.defect_var, value=7)
            defect_7.grid(row=3, column=0, padx=(10,0), pady=10, sticky='w')
            defect_info_7 = customtkinter.CTkButton(self.defect_frame, text="i", width=20, height=20, command=lambda: open_defect_info(value=7))
            defect_info_7.grid(row=3, column=0, padx=(0,5), pady=10, sticky='e')
            
            defect_8 = customtkinter.CTkRadioButton(self.defect_frame, text="Đảo gốc động mạch", variable= self.defect_var, value=8)
            defect_8.grid(row=3, column=1, padx=(10,0), pady=10, sticky='w')
            defect_info_8 = customtkinter.CTkButton(self.defect_frame, text="i", width=20, height=20, command=lambda: open_defect_info(value=8))
            defect_info_8.grid(row=3, column=1, padx=(0,5), pady=10, sticky='e')
            
            defect_9 = customtkinter.CTkRadioButton(self.defect_frame, text="Vòng thắt động mạch phổi", variable= self.defect_var, value=9)
            defect_9.grid(row=3, column=2, padx=(10,0), pady=10, sticky='w')
            defect_info_9 = customtkinter.CTkButton(self.defect_frame, text="i", width=20, height=20, command=lambda: open_defect_info(value=9))
            defect_info_9.grid(row=3, column=2, padx=(0,5), pady=10, sticky='e')
            
            defect_10 = customtkinter.CTkRadioButton(self.defect_frame, text="Hẹp eo động mạch chủ", variable= self.defect_var, value=10)
            defect_10.grid(row=4, column=0, padx=(10,0), pady=10, sticky='w')
            defect_info_10 = customtkinter.CTkButton(self.defect_frame, text="i", width=20, height=20, command=lambda: open_defect_info(value=10))
            defect_info_10.grid(row=4, column=0, padx=(0,5), pady=10, sticky='e')
            
            defect_11 = customtkinter.CTkRadioButton(self.defect_frame, text="Cung động mạch chủ đôi", variable= self.defect_var, value=11)
            defect_11.grid(row=4, column=1, padx=(10,0), pady=10, sticky='w')
            defect_info_11 = customtkinter.CTkButton(self.defect_frame, text="i", width=20, height=20, command=lambda: open_defect_info(value=11))
            defect_info_11.grid(row=4, column=1, padx=(0,5), pady=10, sticky='e')
            
            defect_12 = customtkinter.CTkRadioButton(self.defect_frame, text="Thất phải hai đường ra", variable= self.defect_var, value=12)
            defect_12.grid(row=4, column=2, padx=(10,0), pady=10, sticky='w')
            defect_info_12 = customtkinter.CTkButton(self.defect_frame, text="i", width=20, height=20, command=lambda: open_defect_info(value=12))
            defect_info_12.grid(row=4, column=2, padx=(0,5), pady=10, sticky='e')
            
            
            # Start button
            def start_defect():
                defect_dectection = DiseaseDectection()
                defect_ratio, normal_ratio = defect_dectection.main_process(specified_data=self.master.specified_data, defect_var=self.defect_var.get())
                defect_ratio_label = customtkinter.CTkLabel(master=self.res_frame, text=f'Tỉ lệ có bệnh lý thất phải 2 đường ra: {defect_ratio}', wraplength=200, font=(customtkinter.ThemeManager.theme["CTkFont"]["family"], 15, "bold"))
                defect_ratio_label.grid(row=1, column=0, padx=5, pady=5)
                normal_ratio_label = customtkinter.CTkLabel(master=self.res_frame, text=f'Tỉ lệ bình thường: {normal_ratio}', wraplength=200, font=(customtkinter.ThemeManager.theme["CTkFont"]["family"], 15, "bold"))
                normal_ratio_label.grid(row=2, column=0, padx=5, pady=5)
                
            
            self.defect_progress_bar = customtkinter.CTkProgressBar(self.defect_frame, orientation="horizontal")
            self.defect_progress_bar.set(0)
            self.defect_progress_bar.grid(column=1, row=5, columnspan=5, padx=10, pady=10, sticky='swe')
            self.start_defect_btn = customtkinter.CTkButton(self.defect_frame, text="Start", width=50, command=start_defect)
            self.start_defect_btn.grid(column=0, row=5, pady=10, sticky='s')
            
            # results frame and header
            self.res_frame = customtkinter.CTkFrame(master=self.tabview_1_tab_2, fg_color=self.master.third_color)
            self.res_frame.grid(column=3, row=0, columnspan=3, rowspan=3, padx=(10,0), sticky='news')
            self.res_frame.columnconfigure(0, weight=1)
            self.res_header = self.title_toolbox(frame=self.res_frame, title='Results')
            
            
        create_tabs()
        ROI()
        HounsField()
        DrawingTools()
        Thresholding()
        Defects()
        
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
                    self.start_seg_frame = customtkinter.CTkFrame(master=self.tabview_2_tab_1, fg_color=self.master.third_color)
                    self.start_seg_frame.grid(row=0, column=0, rowspan=4, columnspan=2, pady=(0,10), sticky='news')
                    self.start_seg_frame.columnconfigure(0, weight=1)
                    self.start_seg_frame.rowconfigure((0, 1, 2), weight=1)
                    self.start_seg_frame_header = self.title_toolbox(frame=self.start_seg_frame, title="Deep Segmentation")
                    
                def start_seg_callback():
                    self.seg_progress_bar.start()
                    seg_path = f"D:/Documents/GitHub/VascuIAR/DeepLearning/data/VnRawData/VHSCDD_sep_labels/VHSCDD_{self.master.specified_data}_label/ct_{self.master.specified_data}_label_1.nii.gz"
                    self.master.paths['folder_seg'] = os.path.dirname(seg_path)
                    self.master.add_seg = True
                    for file in os.listdir(self.master.paths['folder_seg']):
                        if file.endswith('.nii.gz'):
                            img_raw = sitk.ReadImage( self.master.paths['folder_seg'] + '/' + file, sitk.sitkFloat32)
                            self.master.seg_imgs.append(sitk.GetArrayFromImage(img_raw))
                    self.master.event_generate("<<UpdateApp2>>") 
                    
                def widgets():
                    self.seg_progress_bar = customtkinter.CTkProgressBar(self.start_seg_frame, orientation="horizontal")
                    if self.master.add_seg == False:
                        self.seg_progress_bar.set(0)
                    else: 
                        self.seg_progress_bar.set(100)
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
                    self.opacity_frame = customtkinter.CTkFrame(master=self.tabview_2_tab_1, fg_color=self.master.third_color)
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
                    self.regions_frame = customtkinter.CTkFrame(master=self.tabview_2_tab_1, fg_color=self.master.third_color)
                    self.regions_frame.grid(row=0, column=2, rowspan=8, columnspan=4, padx=(5,0), sticky='news')
                    self.regions_frame.columnconfigure((0,1,2,3,4,5,6,7,8,9,10,11), weight=1)
                    self.regions_frame.rowconfigure((0,1,2,3,4,5,6,7,8), weight=1)
                    self.regions_frame_header = self.title_toolbox(frame=self.regions_frame, title="Regions Control")
                        
                def widgets():
                    self.region_list_vn = ['Phông nền', 'Tĩnh mạch chủ', 'Tiểu nhĩ', 'Động mạch vành', 'Tâm thất trái', 'Tâm thất phải', 'Tâm nhĩ trái', 'Tâm nhĩ phải', 'Màng cơ tim', 'Cung động mạch', 'Động mạch phổi', 'Động mạch chủ trên'] 
                    self.region_list_en = ['Background', 'Vena cava', 'Auricle', 'Coronary Artery', 'Left ventricle', 'Right ventricle', 'left atrium', 'right atrium', 'Myocardium', 'Aortic Arch', 'Pulmonary trunk', 'Coronary Artery']
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
                            elif class_name=="class12":
                                self.eye_class12.configure(image=eye_hide_icon)
                            
                        
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
                            elif class_name=="class12":
                                self.eye_class12.configure(image=eye_icon)
                                
                    def change_color(class_name):
                        color_choosed = AskColor() .get()
                        self.master.class_data[class_name]['color'] = color_choosed

                    # class1
                    self.eye_class1 = customtkinter.CTkButton(master=self.regions_frame, text="", image=eye_hide_icon, width=30, height=30, command=lambda : eye_hide(class_name="class1"))
                    self.eye_class1.grid(row=1, column=0, padx=(10,0))
                    self.fill_class1 = customtkinter.CTkButton(master=self.regions_frame, text="", image=fill_icon, width=30, height=30, command=lambda : change_color(class_name="class1"))
                    self.fill_class1.grid(row=1, column=1)
                    self.annotate_class1 = customtkinter.CTkButton(master=self.regions_frame, text="", image=annotate_icon, width=30, height=30)
                    self.annotate_class1.grid(row=1, column=2)
                    self.btn_class1 = customtkinter.CTkButton(master=self.regions_frame, text=self.region_list_vn[0], fg_color=self.master.second_color)
                    self.btn_class1.grid(row=1, column=3) 
                    
                    # class2
                    self.eye_class2 = customtkinter.CTkButton(master=self.regions_frame, text="", image=eye_hide_icon, width=30, height=30, command=lambda : eye_hide(class_name="class2"))
                    self.eye_class2.grid(row=1, column=6, padx=(10,0))
                    self.fill_class2 = customtkinter.CTkButton(master=self.regions_frame, text="", image=fill_icon, width=30, height=30, command=lambda : change_color(class_name="class2"))
                    self.fill_class2.grid(row=1, column=7)
                    self.annotate_class2 = customtkinter.CTkButton(master=self.regions_frame, text="", image=annotate_icon, width=30, height=30)
                    self.annotate_class2.grid(row=1, column=8)
                    self.btn_class2 = customtkinter.CTkButton(master=self.regions_frame, text=self.region_list_vn[1], fg_color=self.master.second_color)
                    self.btn_class2.grid(row=1, column=9) 
                    
                    # class3
                    self.eye_class3 = customtkinter.CTkButton(master=self.regions_frame, text="", image=eye_hide_icon, width=30, height=30, command=lambda : eye_hide(class_name="class3"))
                    self.eye_class3.grid(row=2, column=0, padx=(10,0))
                    self.fill_class3 = customtkinter.CTkButton(master=self.regions_frame, text="", image=fill_icon, width=30, height=30, command=lambda : change_color(class_name="class3"))
                    self.fill_class3.grid(row=2, column=1)
                    self.annotate_class3 = customtkinter.CTkButton(master=self.regions_frame, text="", image=annotate_icon, width=30, height=30)
                    self.annotate_class3.grid(row=2, column=2)
                    self.btn_class3 = customtkinter.CTkButton(master=self.regions_frame, text=self.region_list_vn[2], fg_color=self.master.second_color)
                    self.btn_class3.grid(row=2, column=3) 
                    
                    # class4
                    self.eye_class4 = customtkinter.CTkButton(master=self.regions_frame, text="", image=eye_hide_icon, width=30, height=30, command=lambda : eye_hide(class_name="class4"))
                    self.eye_class4.grid(row=2, column=6, padx=(10,0))
                    self.fill_class4 = customtkinter.CTkButton(master=self.regions_frame, text="", image=fill_icon, width=30, height=30, command=lambda : change_color(class_name="class4"))
                    self.fill_class4.grid(row=2, column=7)
                    self.annotate_class4 = customtkinter.CTkButton(master=self.regions_frame, text="", image=annotate_icon, width=30, height=30)
                    self.annotate_class4.grid(row=2, column=8)
                    self.btn_class4 = customtkinter.CTkButton(master=self.regions_frame, text=self.region_list_vn[3], fg_color=self.master.second_color)
                    self.btn_class4.grid(row=2, column=9)
                    
                    # class5
                    self.eye_class5 = customtkinter.CTkButton(master=self.regions_frame, text="", image=eye_hide_icon, width=30, height=30, command=lambda : eye_hide(class_name="class5"))
                    self.eye_class5.grid(row=3, column=0, padx=(10,0))
                    self.fill_class5 = customtkinter.CTkButton(master=self.regions_frame, text="", image=fill_icon, width=30, height=30, command=lambda : change_color(class_name="class5"))
                    self.fill_class5.grid(row=3, column=1)
                    self.annotate_class5 = customtkinter.CTkButton(master=self.regions_frame, text="", image=annotate_icon, width=30, height=30)
                    self.annotate_class5.grid(row=3, column=2)
                    self.btn_class5 = customtkinter.CTkButton(master=self.regions_frame, text=self.region_list_vn[4], fg_color=self.master.second_color)
                    self.btn_class5.grid(row=3, column=3)
                    
                    # class6
                    self.eye_class6 = customtkinter.CTkButton(master=self.regions_frame, text="", image=eye_hide_icon, width=30, height=30, command=lambda : eye_hide(class_name="class6"))
                    self.eye_class6.grid(row=3, column=6, padx=(10,0))
                    self.fill_class6 = customtkinter.CTkButton(master=self.regions_frame, text="", image=fill_icon, width=30, height=30, command=lambda : change_color(class_name="class6"))
                    self.fill_class6.grid(row=3, column=7)
                    self.annotate_class6 = customtkinter.CTkButton(master=self.regions_frame, text="", image=annotate_icon, width=30, height=30)
                    self.annotate_class6.grid(row=3, column=8)
                    self.btn_class6 = customtkinter.CTkButton(master=self.regions_frame, text=self.region_list_vn[5], fg_color=self.master.second_color)
                    self.btn_class6.grid(row=3, column=9)
                    
                    # class7
                    self.eye_class7 = customtkinter.CTkButton(master=self.regions_frame, text="", image=eye_hide_icon, width=30, height=30, command=lambda : eye_hide(class_name="class7"))
                    self.eye_class7.grid(row=4, column=0, padx=(10,0))
                    self.fill_class7 = customtkinter.CTkButton(master=self.regions_frame, text="", image=fill_icon, width=30, height=30, command=lambda : change_color(class_name="class7"))
                    self.fill_class7.grid(row=4, column=1)
                    self.annotate_class7 = customtkinter.CTkButton(master=self.regions_frame, text="", image=annotate_icon, width=30, height=30)
                    self.annotate_class7.grid(row=4, column=2)
                    self.btn_class7 = customtkinter.CTkButton(master=self.regions_frame, text=self.region_list_vn[6], fg_color=self.master.second_color)
                    self.btn_class7.grid(row=4, column=3)
                    
                    # class8
                    self.eye_class8 = customtkinter.CTkButton(master=self.regions_frame, text="", image=eye_hide_icon, width=30, height=30, command=lambda : eye_hide(class_name="class8"))
                    self.eye_class8.grid(row=4, column=6, padx=(10,0))
                    self.fill_class8 = customtkinter.CTkButton(master=self.regions_frame, text="", image=fill_icon, width=30, height=30, command=lambda : change_color(class_name="class8"))
                    self.fill_class8.grid(row=4, column=7)
                    self.annotate_class8 = customtkinter.CTkButton(master=self.regions_frame, text="", image=annotate_icon, width=30, height=30)
                    self.annotate_class8.grid(row=4, column=8)
                    self.btn_class8 = customtkinter.CTkButton(master=self.regions_frame, text=self.region_list_vn[7], fg_color=self.master.second_color)
                    self.btn_class8.grid(row=4, column=9)
                    
                    # class9
                    self.eye_class9 = customtkinter.CTkButton(master=self.regions_frame, text="", image=eye_hide_icon, width=30, height=30, command=lambda : eye_hide(class_name="class9"))
                    self.eye_class9.grid(row=5, column=0, padx=(10,0))
                    self.fill_class9 = customtkinter.CTkButton(master=self.regions_frame, text="", image=fill_icon, width=30, height=30, command=lambda : change_color(class_name="class9"))
                    self.fill_class9.grid(row=5, column=1)
                    self.annotate_class9 = customtkinter.CTkButton(master=self.regions_frame, text="", image=annotate_icon, width=30, height=30)
                    self.annotate_class9.grid(row=5, column=2)
                    self.btn_class9 = customtkinter.CTkButton(master=self.regions_frame, text=self.region_list_vn[8], fg_color=self.master.second_color)
                    self.btn_class9.grid(row=5, column=3)
                    
                    # class10
                    self.eye_class10 = customtkinter.CTkButton(master=self.regions_frame, text="", image=eye_hide_icon, width=30, height=30, command=lambda : eye_hide(class_name="class10"))
                    self.eye_class10.grid(row=5, column=6, padx=(10,0))
                    self.fill_class10 = customtkinter.CTkButton(master=self.regions_frame, text="", image=fill_icon, width=30, height=30, command=lambda : change_color(class_name="class10"))
                    self.fill_class10.grid(row=5, column=7)
                    self.annotate_class10 = customtkinter.CTkButton(master=self.regions_frame, text="", image=annotate_icon, width=30, height=30)
                    self.annotate_class10.grid(row=5, column=8)
                    self.btn_class10 = customtkinter.CTkButton(master=self.regions_frame, text=self.region_list_vn[9], fg_color=self.master.second_color)
                    self.btn_class10.grid(row=5, column=9)
                    
                    # class11
                    self.eye_class11 = customtkinter.CTkButton(master=self.regions_frame, text="", image=eye_hide_icon, width=30, height=30, command=lambda : eye_hide(class_name="class11"))
                    self.eye_class11.grid(row=6, column=0, padx=(10,0))
                    self.fill_class11 = customtkinter.CTkButton(master=self.regions_frame, text="", image=fill_icon, width=30, height=30, command=lambda : change_color(class_name="class11"))
                    self.fill_class11.grid(row=6, column=1)
                    self.annotate_class11 = customtkinter.CTkButton(master=self.regions_frame, text="", image=annotate_icon, width=30, height=30)
                    self.annotate_class11.grid(row=6, column=2)
                    self.btn_class11 = customtkinter.CTkButton(master=self.regions_frame, text=self.region_list_vn[10], fg_color=self.master.second_color)
                    self.btn_class11.grid(row=6, column=3)

                    # class12
                    self.eye_class12 = customtkinter.CTkButton(master=self.regions_frame, text="", image=eye_hide_icon, width=30, height=30, command=lambda : eye_hide(class_name="class12"))
                    self.eye_class12.grid(row=6, column=6, padx=(10,0))
                    self.fill_class12 = customtkinter.CTkButton(master=self.regions_frame, text="", image=fill_icon, width=30, height=30, command=lambda : change_color(class_name="class12"))
                    self.fill_class12.grid(row=6, column=7)
                    self.annotate_class12 = customtkinter.CTkButton(master=self.regions_frame, text="", image=annotate_icon, width=30, height=30)
                    self.annotate_class12.grid(row=6, column=8)
                    self.btn_class12 = customtkinter.CTkButton(master=self.regions_frame, text=self.region_list_vn[11], fg_color=self.master.second_color)
                    self.btn_class12.grid(row=6, column=9)
                               
                frame()
                if self.master.add_seg == True:
                    widgets()
            
            start_seg()
            opacity()
            regions()
            
        def Reconstruction():
            def start_reconstruction():
                venv_activate_script = os.path.join('D:/Documents/GitHub/VascuIAR/.venv/Scripts', 'activate')
                if sys.platform.startswith('win'):
                    activation_command = f"call {venv_activate_script}"
                    start_command = "start"
                else:
                    activation_command = f"source {venv_activate_script}"
                    start_command = "x-terminal-emulator -e"

                command = f"{activation_command} && {start_command} python automatic_reconstruction_2.py {self.master.specified_data}"
                subprocess.run(command, shell=True)
            
            self.reconstruction_frame = customtkinter.CTkFrame(master=self.tabview_2_tab_2, fg_color=self.master.third_color)
            self.reconstruction_frame.pack()
            self.btn_reconstruction = customtkinter.CTkButton(master=self.reconstruction_frame, text="3D reconstruction", command=start_reconstruction)
            self.btn_reconstruction.pack()
            
        
        create_tabs()
        Segmentation()
        Reconstruction()
    
class App(customtkinter.CTk):
    def __init__(self, title, logo_path):
        super().__init__()
        self.title(title)
        self.width = int(self.winfo_screenwidth()/1.05)
        self.height = int(self.winfo_screenheight()/1.1)
        self.geometry(f"{self.width}x{self.height}")
        self.minsize(500, 500)
        self.iconbitmap(logo_path)
        
        # Color specification
        self.first_color = "#2b2b2b"
        self.second_color = "#3b3b3b"
        self.third_color = "#303030"
        self.text_disabled_color = "#dce4e2"
        self.text_canvas_color = "yellow"
        
        # Image variables
        self.specified_data = ''
        self.img = None
        self.img_raw = None
        self.pixel_spacing = 0.858

        # Segmentaion variables
        self.seg = None
        self.seg_raw = None
        self.add_seg = False
        self.seg_imgs = []
        
        # Data
        self.data_manager = DataManager()
        self.dict_info = {}
        loaded_default_data = self.data_manager.load_default_data()
        self.analysis_data = loaded_default_data["analysis_data.json"]
        self.class_data = loaded_default_data["class_data.json"]
        self.draw_data = loaded_default_data["draw_data.json"]
        self.ROI_data = loaded_default_data["ROI_data.json"]
        self.paths = {
            'image_path': '',
            'folder_seg': '',
        }
        self.folder_imgs = {}
        self.data_defects = {
            1: {
                'defect': 'Thông liên thất',
                'description': 'Là một dị tật của vách liên thất, là vách ngăn giữa hai buồng tâm thất của tim. Vách liên thất là một cấu trúc phức tạp gồm: phần cơ, phần màng, phần phễu, phần buồng nhận. Thông thường khi trẻ sinh ra, vách này không có lỗ thông, vì vậy không cho phép máu của hai tâm thất hòa trộn với nhau. Thông liên thất lớn gây shunt trái sang phải lớn, gây khó thở khi ăn uống và chậm tăng cân. Triệu chứng: Da, môi và móng tay xanh tím, ăn kém, chậm lớn, thở nhanh hoặc khó thở, mệt mỏi, sưng phù chân, bàn chân hoặc bụng, tim đập nhanh. Đôi khi dị tật vách liên thất không được phát hiện cho đến khi tới tuổi trưởng thành và phát triển các triệu chứng của suy tim như khó thở.',
                'image': {
                    1: 'D:/Documents/GitHub/VascuIAR/GUIApp/imgs/Thông liên thất.png',
                    2: 'D:/Documents/GitHub/VascuIAR/GUIApp/imgs/Thông liên thất 2.jpg',
                }
            },
            2: {
                'defect' : 'Còn ống động mạch',
                'description': 'Còn ống động mạch (Patent ductus arteriosus - PDA) là là sự tồn tại dai dẳng sau sinh của cấu trúc trong thời kỳ bào thai liên kết động mạch chủ và động mạch phổi. Ống động mạch nhỏ có thể tự đóng. Đối với những ống động mạch lớn gây ra các vấn đề về lưu thông máu ở trẻ. Nếu không có các bất thường về cấu trúc tim hoặc tăng sức cản mạch phổi thì dòng máu đi qua ống động mạch sẽ theo chiều từ trái sang phải (từ động mạch chủ đến động mạch phổi). Máu sẽ lưu thông trực tiếp từ động mạch chủ qua động mạch phổi, dẫn đến gia tăng dòng máu vào hệ tuần hoàn phổi, tăng lượng máu trở về tim trái. Nếu còn ống động mạch lớn, áp lực trong mạch máu phổi cũng tăng theo. Hệ quả là trẻ có nguy cơ bị suy tim khi chỉ mới vài tuần tuổi. Ống động mạch lớn không được điều trị có thể khiến dòng máu chảy bất thường từ các động mạch lớn trong tim, tăng áp lực trong buồng tim, làm suy yếu cơ tim và gây ra các biến chứng khác. Triệu chứng có thể bao gồm chậm lớn, ăn kém, nhịp tim nhanh, và thở nhanh. Một tiếng thổi liên tục ở phía trên bên trái xương ức là phổ biến. Chẩn đoán bằng siêu âm tim, CT, MRI. Sử dụng thuốc ức chế cyclooxygenase (ibuprofen lysine hoặc indomethacin) có hoặc không hạn chế dịch có thể được thử ở trẻ sinh non có luồng thông đáng kể, nhưng liệu pháp này không hiệu quả ở trẻ đủ tháng hoặc trẻ lớn hơn mắc PDA. Nếu vẫn còn tồn tại ống động mạch, chỉ định phẫu thuật hoặc thông tim được đặt ra.',
                'image': {
                    1: 'D:/Documents/GitHub/VascuIAR/GUIApp/imgs/Còn ống động mạch.png',
                    2: 'D:/Documents/GitHub/VascuIAR/GUIApp/imgs/Còn ống động mạch 2.jpg',
                    3: 'D:/Documents/GitHub/VascuIAR/GUIApp/imgs/Còn ống động mạch 3.jpg',
                }
            },
            3: {
                'defect': 'Thân chung động mạch',
                'description': 'Tồn tại thân chung động mạch xảy ra khi, trong quá trình phát triển của bào thai, thân động mạch nguyên thủy không phân chia thành động mạch chủ và động mạch phổi, kết quả là một thân động mạch lớn, đơn độc, cưỡi ngựa lên thông liên thất phần màng hoặc quanh màng. Do đó, máu trộn giữa máu giàu oxy và máu khử oxy đi nuôi cơ thể, phổi, và hệ thống động mạch vành. Bệnh lý này thường đi kèm với khuyết tật vách liên thất. Triệu chứng bao gồm tím và suy tim, ăn uống khó khăn, vã mồ hôi, và thở nhanh. Tiếng tim thứ nhất bình thường (S1) và tiếng tim thứ hai lớn, đơn lẻ (S2) là phổ biến; tiếng thổi có thể khác nhau. Trước khi suy tim sâu phát triển, các xung ngoại vi sẽ bị ràng buộc vì dòng chảy lớn từ động mạch chủ gần đến động mạch phổi. Chẩn đoán bằng siêu âm tim, chụp cộng hưởng từ, chụp mạch CT, hoặc thông tim. Điều trị nội khoa cho suy tim, sau đó phẫu thuật sửa chữa sớm.',
                'image':{
                    1: 'D:/Documents/GitHub/VascuIAR/GUIApp/imgs/Thân chung động mạch.png',
                    2: 'D:/Documents/GitHub/VascuIAR/GUIApp/imgs/Thân chung động mạch 2.jpg',
                    3: 'D:/Documents/GitHub/VascuIAR/GUIApp/imgs/Thân chung động mạch 3.jpg',
                }
            },
            4: {
                'defect': 'Bất thường động mạch vành',
                'description': 'Các bệnh động mạch vành là một trong những nguyên nhân gây tử vong hàng đầu trên thế giới, là một nguyên nhân phổ biến thứ hai gây đột quỵ cho các vận động viên. Động mạch vành có hai nhánh chính là động mạch vành trái (Left Coronary Artery - LCA) xuất phát từ xoang vành trái (left sinus of Valsalva) và động mạch vành phải (Right Coronary Artery - RCA) xuất phát từ xoang vành phải (right sinus of Valsalva) [29]. Bất kì sự xuất phát sai vị trí nào của hai nhánh động mạch vành này đều được xem là bất thường động mạch vành. Ví dụ: Động mạch vành phải xuất phát từ xoang vành trái hoặc xuất phát từ xoang không mạch vành (non-coronary sinus). Bộ dữ liệu có thể phân vùng chi tiết động mạch vành đến các vi mạch, nhưng không thể phản ánh chính xác độ dày hẹp cũng như gán nhãn các mảng xơ vữa hoặc vôi hóa.',
                 'image' : {
                     1: 'D:/Documents/GitHub/VascuIAR/GUIApp/imgs/Bất thường động mạch vành.jpg',
                 }
            },
            5: {
                'defect' : 'Phình động mạch',
                'description': 'Phình động mạch là một bất thường hiếm gặp của hệ động mạch, khi động mạch bị giãn khu trú do sự suy yếu của thành mạch. Phình động mạch có thể xuất hiện ở bất kỳ vị trí nào của động mạch, nhưng thường gặp ở động mạch trung tâm và bên trái. Phình động mạch có thể gây ra các triệu chứng như ho, khó thở, đau ngực, ho ra máu, tím tái, chóng mặt hoặc ngất xỉu. Phình động mạch có thể được phát hiện bằng chụp cộng hưởng từ, chụp CT hay siêu âm. Điều trị phình động mạch phụ thuộc vào nguyên nhân, vị trí, kích thước và triệu chứng của bệnh. Có thể sử dụng các phương pháp nội khoa, can thiệp nội mạch hoặc phẫu thuật.',
                'image' : {
                    1: 'D:/Documents/GitHub/VascuIAR/GUIApp/imgs/Phình động mạch.png',
                }
            },
            6: {
                'defect' : 'Tĩnh mạch chủ kép',
                'description':  'Là một biến thể giải phẫu hiếm gặp xuất phát từ tĩnh mạch chủ trên bên trái dai dẳng, do sự thoái lui của tĩnh mạch chính trước về mặt phôi thai đã thất bại. SVC bên trái dẫn lưu vào tâm nhĩ phải trong 90% trường hợp qua xoang vành giãn, các vị trí thay thế bao gồm tĩnh mạch chủ dưới, tĩnh mạch gan và tâm nhĩ trái. Sự dẫn lưu SVC trái không điển hình vào tâm nhĩ trái dẫn đến shunt phải sang trái, có thể gây tím tái và có liên quan đến các trường hợp tắc mạch nhiễm trùng. SVC bên phải được thấy trong 82-90% trường hợp SVC kép. Sự vắng mặt của SVC phải hoặc SVC trái dẫn lưu vào tâm nhĩ trái có liên quan đến việc tăng tỷ lệ mắc các bệnh tim bẩm sinh như ASD, VSD và TOF.'
                ''
            },
            7: {
                'defect' : 'Bất thường tĩnh mạch phổi trở về tuần hoàn',
                'description': 'Bất thường tĩnh mạch phổi trở về hoàn toàn (Total Anomalous Pulmonary Venous Return - TAPVR) là một dị tật bẩm sinh của tim. Ở trẻ mắc TAPVR, máu giàu oxy không trở về tâm nhĩ trái từ phổi. Thay vào đó, máu giàu oxy sẽ quay trở lại bên phải tim. Ở đây, máu giàu oxy trộn lẫn với máu nghèo oxy. Điều này khiến em bé nhận được ít oxy hơn mức cần thiết cho cơ thể. Để sống sót với khiếm khuyết này, trẻ sơ sinh mắc TAPVR thường có một lỗ giữa tâm nhĩ phải và tâm nhĩ trái (khiếm khuyết thông liên nhĩ) cho phép máu hỗn hợp đi đến bên trái tim và bơm ra phần còn lại của cơ thể. Một số trẻ có thể bị các khuyết tật tim khác cùng với TAPVR, ngoài khuyết tật thông liên nhĩ. Vì em bé bị khuyết tật này có thể cần phẫu thuật hoặc các thủ tục khác ngay sau khi sinh nên TAPVR được coi là một khuyết tật tim bẩm sinh nghiêm trọng.',
                'image': {
                    1: 'D:/Documents/GitHub/VascuIAR/GUIApp/imgs/Bất thường tĩnh mạch phổi trở về tuần hoàn.jpg',
                    2: 'D:/Documents/GitHub/VascuIAR/GUIApp/imgs/Bất thường tĩnh mạch phổi trở về tuần hoàn 2.jpg',
                    3: 'D:/Documents/GitHub/VascuIAR/GUIApp/imgs/Bất thường tĩnh mạch phổi trở về tuần hoàn 3.jpg',
                }
            },
            8: {
                'defect' : 'Đảo gốc động mạch',
                'description': 'Là sự thay đổi vị trí của các động mạch lớn (TGA), khi các động mạch “lớn”, động mạch chủ và tâm thất phải, bị đảo ngược về phần gốc từ tim. Động mạch chủ được kết nối với tâm thất phải và động mạch phổi được kết nối với tâm thất trái - hoàn toàn trái ngược với giải phẫu của tim bình thường. Khi các động mạch này đảo ngược, máu ít oxy (màu xanh lam) từ cơ thể trở về tâm nhĩ phải, đi vào tâm thất phải, sau đó đi vào động mạch chủ và trở lại cơ thể. Máu giàu oxy (màu đỏ) trở lại tâm nhĩ trái từ phổi và đi vào tâm thất trái, bơm máu trở lại phổi - ngược lại với cách máu lưu thông bình thường.',
                'image': {
                    1: 'D:/Documents/GitHub/VascuIAR/GUIApp/imgs/Đảo gốc động mạch.png',
                    2: 'D:/Documents/GitHub/VascuIAR/GUIApp/imgs/Còn ống động mạch 2.jpg',
                    3: 'D:/Documents/GitHub/VascuIAR/GUIApp/imgs/Còn ống động mạch 3.jpg',
                }
            },
            9: {
                'defect' : 'Vòng thắt động mạch phổi',
                'description': 'Là một bệnh lý hiếm gặp, được xác định là một dạng vòng mạch máu phổi. Bệnh này gây ra sự chèn ép khí quản do vòng thắt mạch máu phổi bị bóp nghẹt. Bệnh này thường được phát hiện ở trẻ em và có thể gây ra các triệu chứng như khò khè, thở khò khè, ho, thở nhanh và khó thở. Để điều trị bệnh này, các bác sĩ có thể sử dụng phẫu thuật tái tạo khí quản hoặc đặt một ống nong động mạch chủ vào khí quản để giúp nông khí quản.',
                'image': {
                    1: 'D:/Documents/GitHub/VascuIAR/GUIApp/imgs/Đảo gốc động mạch.png',
                    2: 'D:/Documents/GitHub/VascuIAR/GUIApp/imgs/Còn ống động mạch 2.jpg',
                    3: 'D:/Documents/GitHub/VascuIAR/GUIApp/imgs/Còn ống động mạch 3.jpg',
                }
            },
            10: {
                'defect' : 'Hẹp eo động mạch chủ',
                'description': 'Hẹp eo động mạch chủ là một tình trạng bẩm sinh mà động mạch chủ bị hẹp, thường tập trung ở vùng ống động mạch chủ, gọi là dây chằng động mạch. Một trường hợp phổ biến là hẹp ở vòm động mạch chủ (Aortic Arch), có thể xuất hiện kích thước nhỏ ở trẻ sơ sinh gặp vấn đề với eo. Khi có hẹp eo, tâm thất trái phải làm việc hơn bình thường, tạo ra áp lực cao để đẩy máu qua động mạch chủ thu hẹp, đưa máu đến phần dưới của cơ thể. Nếu hẹp eo nghiêm trọng, tâm thất trái có thể không đủ mạnh để vượt qua chỗ hẹp, dẫn đến tình trạng thiếu máu ở phần dưới cơ thể. Tình trạng này có thể gây ra các vấn đề khác nhau, bao gồm tăng huyết áp ở chi trên, phì đại thất trái, và thậm chí gây rối loạn tưới máu cho các cơ quan trong ổ bụng và chi dưới. Triệu chứng của hẹp eo động mạch chủ đa dạng, phụ thuộc vào mức độ hẹp, bao gồm đau đầu, đau ngực, lạnh chân, mệt mỏi, và yếu chân. Tiếng thổi nhẹ có thể nghe được qua khu vực hẹp eo. Chẩn đoán thường được thực hiện bằng siêu âm tim, chụp CT, hoặc chụp MRI. Để điều trị hẹp eo động mạch chủ, các phương pháp bao gồm nong mạch bằng bóng với đặt stent hoặc phẫu thuật. Quá trình này có thể giúp mở rộng đường động mạch chủ và cải thiện lưu thông máu, giảm bớt các vấn đề liên quan đến hẹp eo.',
                'image':{
                    1:'D:/Documents/GitHub/VascuIAR/GUIApp/imgs/Hẹp eo động mạch chủ.jpg'
                }
            },
            11: {
                'defect' : 'Cung động mạch chủ đôi',
                'description': 'Vòm/Cung động mạch chủ đôi là một dị thường của vòm động mạch chủ, trong đó hai vòm động mạch chủ tạo thành một vòng mạch hoàn chỉnh có thể chèn ép khí quản và/hoặc thực quản. Cung động mạch chủ là đoạn đầu tiên của động mạch chủ rời khỏi tim để cấp máu cho các cơ quan của cơ thể. Vòng mạch máu do cung động mạch chủ đôi là dị dạng của cung động mạch chủ. Vòng mạch máu do cung động mạch chủ đôi bao bọc một phần hoặc hoàn toàn khí quản hoặc thực quản. Có những trường hợp là cả hai. Những dị tật này có ngay từ lúc mới sinh (bẩm sinh). Nhưng các triệu chứng có thể xảy ra ở giai đoạn sơ sinh hoặc sau này ở độ tuổi thiếu nhi, thanh thiếu niên.',
                'image': {
                    1: 'D:/Documents/GitHub/VascuIAR/GUIApp/imgs/Cung động mạch chủ đôi.png'
                }
            },
            12: {
                'defect' : 'Thất phải hai đường ra',
                'description': 'Trong tâm thất phải hai lối ra, cả động mạch chủ và van động mạch phổi đều kết nối với tâm thất phải. Thông liên thất hầu như luôn đi kèm với dị dạng này và các biểu hiện lâm sàng được xác định bởi vị trí của lỗ thông và có hay không có hẹp van động mạch phổi. Trong trái tim bình thường, động mạch chủ kết nối với buồng tim trái dưới. Động mạch phổi kết nối với buồng tim phải dưới. Tuy nhiên, ở trẻ em bị DORV, cả động mạch chủ và động mạch phổi kết nối một phần hoặc hoàn toàn với buồng tim phải dưới. Trẻ em bị DORV cũng có lỗ giữa hai buồng tim dưới. Lỗ này được gọi là khuyết tán giữa hai buồng tim. Lỗ này gây ra sự trộn lẫn giữa máu giàu oxy và máu nghèo oxy. Trẻ em bị bệnh này có thể không đủ oxy trong tuần hoàn máu. Da có thể trở nên xám hoặc xanh. Nếu quá nhiều máu chảy qua động mạch phổi đến phổi, nó có thể dẫn đến suy tim và tăng nguy cơ suy dinh dưỡng. Chẩn đoán bằng điện tâm đồ, chẩn đoán hình ảnh và thông tim. Điều trị nội khoa là hữu ích, nhưng can thiệp phẫu thuật luôn cần thiết.',
                'image':{
                    1: 'D:/Documents/GitHub/VascuIAR/GUIApp/imgs/Thất phải hai đường ra.jpg'
                }
                
            },
        }
        
        
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
        
        # Auto save when closing window
        
        
        
    def save_to_json(self, filename):
        with open(filename, 'w') as json_file:
            json.dump(self.dict_info, json_file, indent=4)

    def load_from_json(self, filename):
        with open(filename, 'r') as json_file:
            return json.load(json_file) 

app = App(
    title='VasculAR software',
    logo_path='imgs/logo.ico'
)


'''
Khi tải phần mềm về thì luôn có một file mặc định default.vas 
Trong default.vas sẽ chứa các file thông tin như sau: 
Nếu người dùng chọn file .nii.gz kèm theo một file json chưa dict_info thì ta dùng cái default.vas

    1. class_data  --> default
    2. ROI_data --> default
    paths
        3. self.path = '' --> rỗng --> phải bấm start_seg mới thực hiện segmentation
        4. self.folder_seg
    5. self.add_seg = False --> trong default.vas là false vì chưa có segmentation 
    6. self.draw_data
    7. analysis_data = rỗng
    

Chỉ được lưu file nếu như đã login thành công
Trong fiel saved.vas chưa casc file sau:
Nếu người dùng chọn file.vas thì ta sử dụng cái này
    1. class_data  --> đã saved
    2. ROI_data --> đã saved
    paths
        3. self.path = '' --> link của data trước đó đã load trong máy tính 
        4. self.folder_seg = '' --> đã lưu --> --> thực hiện segmentation khi mởi mở lại luôn
    5. self.add_seg = False/true --> tùy lúc trước đã thực hiện segmentation hay chưa 
    6. self.draw_data --> đã được lưu lại
    7. analysis_data
    
--> file này được đẩy lên firebase nếu như save lại 
--> các ảnh/output.pdf/ảnh 3d xuất ra thì được lưu vào một folder tên analyis trên firebase 
'''