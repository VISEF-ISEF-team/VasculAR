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
from draw import draw_canvas
from PIL import Image, ImageTk
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
                    'add_dcm_series_btn': 'Add DCM series',
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
            
    def choose_file(self):
        self.master.path = filedialog.askopenfilename()
        
        if self.master.path.endswith('.nii.gz') or self.master.path.endswith('.nii'):
            self.master.img_raw = sitk.ReadImage(self.master.path, sitk.sitkFloat32)
            self.master.img = sitk.GetArrayFromImage(self.master.img_raw)
            print("read niftifile")
        
        elif self.master.path.endswith('.dcm'):
            parent_dir = os.path.dirname(self.master.path)
            instance = ReadDCM(parent_dir)
            self.master.img_raw, self.master.img, self.master.dict_info, self.master.pixel_spacing = instance.read_file_dcm()
            print(self.master.dict_info)
            
        self.master.event_generate("<<UpdateApp>>")
        
    def dropdown_options(self, instance, master):            
        for row, (instance_name, label_name) in enumerate(self.data[instance]['sub_menu'].items()):
            if instance_name == 'add_nifti_file_btn':
                self.menu_item['sub_menu'][instance_name] = customtkinter.CTkButton(
                    master=master, 
                    text=label_name,
                    fg_color='transparent', 
                    hover_color=self.master.second_color,
                    command = lambda: self.choose_file(),
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
            x = widget_option.winfo_x() - 10*col
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
    

class CanvasViews:
    def __init__(self, master):
        self.master = master
        self.create_frames()
        self.create_canvas_axial()
        
    def create_frames(self):
        self.frame_axial = customtkinter.CTkFrame(master=self.master, fg_color=self.master.second_color)
        self.frame_axial.grid(row=1, column=0, rowspan=9, columnspan=6, padx=5, sticky='news')
        
        self.frame_sagittal = customtkinter.CTkFrame(master=self.master, fg_color=self.master.second_color)
        self.frame_sagittal.grid(row=1, column=6, rowspan=9, columnspan=6, padx=5, sticky='news')
        
        self.frame_coronal = customtkinter.CTkFrame(master=self.master, fg_color=self.master.second_color)
        self.frame_coronal.grid(row=1, column=12, rowspan=9, columnspan=6, padx=5, sticky='news')
        
    def create_canvas_axial(self):    
        def create_crosshair():
            self.horizontal_line = self.canvas_axial.create_line(0, self.canvas_axial.winfo_height() // 2, self.canvas_axial.winfo_width(), self.canvas_axial.winfo_height() // 2, fill="red")
            self.vertical_line = self.canvas_axial.create_line(self.canvas_axial.winfo_width() // 2, 0, self.canvas_axial.winfo_width() // 2, self.canvas_axial.winfo_height(), fill="red")
            
            def move_crosshair(event):
                x, y = event.x, event.y
                self.canvas_axial.coords(self.horizontal_line, 0, y, self.canvas_axial.winfo_width(), y)
                self.canvas_axial.coords(self.vertical_line, x, 0, x, self.canvas_axial.winfo_height())

            def on_mouse_press(event):
                self.canvas_axial.bind("<Motion>", move_crosshair)

            def on_mouse_release(event):
                self.canvas_axial.unbind("<Motion>")

            self.canvas_axial.bind("<ButtonPress-1>", on_mouse_press)
            self.canvas_axial.bind("<ButtonRelease-1>", on_mouse_release)                
            
        def image_display(index_slice):
            height = int(self.label_zoom.cget("text"))
            image = self.master.img[int(index_slice), :, :]
            plt.imsave("temp.jpg", image, cmap='gray')
            image_display = Image.open("temp.jpg").resize((height, height))
            my_image = ImageTk.PhotoImage(image_display)
            x_cord, y_cord = image_position()
            self.canvas_item_axial = self.canvas_axial.create_image(x_cord, y_cord, image=my_image, anchor="center")
            self.canvas_axial.image = my_image
            
            create_crosshair()
            
            
        def image_position():
            try:
                image_position = self.canvas_axial.coords(self.canvas_item_axial)
                return image_position[0], image_position[1]
            except:
                return 400, 400
            
        def movement_binding():
            self.canvas_axial.focus_set() 
            self.canvas_axial.bind('<Left>', lambda event: self.canvas_axial.move(self.canvas_item_axial, -10, 0))
            self.canvas_axial.bind('<Right>', lambda event: self.canvas_axial.move(self.canvas_item_axial, 10, 0))
            self.canvas_axial.bind('<Up>', lambda event: self.canvas_axial.move(self.canvas_item_axial, 0, -10))
            self.canvas_axial.bind('<Down>', lambda event: self.canvas_axial.move(self.canvas_item_axial, 0, 10))   
            
        def display_info():
            text = "Patient info"
            text_item = self.canvas_axial.create_text(50, 10, text=text)
            self.canvas_axial.itemconfig(text_item,  fill=self.master.white_color) 
        
        def zoom(event):
            current_value = self.label_zoom.cget("text")
            new_value = int(current_value) + (event.delta/120)*6
            self.label_zoom.configure(text=new_value)
            image_display(self.slider_volume.get())   
            
        def slider_volume_show(value):
            index_slice = round(value, 0)
            self.text_show_volume.configure(text=int(index_slice))
            image_display(index_slice)

        def slider_widget():        
            self.slider_volume = customtkinter.CTkSlider(self.master, from_=0, to=620, command=slider_volume_show)
            self.slider_volume.grid(column=0, row=0, columnspan=2, rowspan=1, padx=(5,0), pady=(25,0), sticky='ew')
            self.text_show_volume = customtkinter.CTkLabel(self.master, text="")
            self.text_show_volume.grid(column=2, row=0, rowspan=1, pady=(25,0), sticky='ew')
            
 

        self.canvas_axial = Canvas(master=self.frame_axial)
        self.canvas_axial.pack(fill='both', expand=True)
        
        self.label_zoom = customtkinter.CTkLabel(master=self.frame_axial, text="800")
        self.canvas_axial.bind("<MouseWheel>", zoom)

        
        movement_binding()
        display_info()
        slider_widget()
        
    def create_canvas_sagittal(self):
        self.canvas_sagittal = Canvas(master=self.frame_sagittal)
        self.canvas_sagittal.pack(fill='both', expand=True)
       
    def create_canvas_coronal(self): 
        self.canvas_coronal = Canvas(master=self.frame_coronal)
        self.canvas_coronal.pack(fill='both', expand=True)
        
class Tools:
    def __init__(self, master):
        self.master = master

        self.tabview_1 = customtkinter.CTkTabview(master=self.master)
        self.tabview_1.grid(column=0, row=10, columnspan=9, rowspan=5, padx=5, pady=5, sticky="nsew")
        self.tab_1 = self.tabview_1.add("Basic tools")    
        self.tab_2 = self.tabview_1.add("Image processing")
        self.tab_3 = self.tabview_1.add("Defect Detection")
        self.tabview_1.set("Basic tools") 
        
        self.tabview_2 = customtkinter.CTkTabview(master=self.master)
        self.tabview_2.grid(column=9, row=10, columnspan=9, rowspan=5, padx=5, pady=5, sticky="nsew")
        self.tab_1 = self.tabview_2.add("Segmentation")    
        self.tab_2 = self.tabview_2.add("3D reconstruction")
        self.tab_3 = self.tabview_2.add("VR/AR connection")
        self.tabview_2.set("Segmentation") 
    
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
        self.white_color = 'white'
        
        self.img = None
        self.img_raw = None
        self.dict_info = {}
        self.pixel_spacing = 0.858
        self.path = ''

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
            self.canvas_view = CanvasViews(self)
            
            
        self.bind("<<UpdateApp>>", update_app)
        self.mainloop()

app = App(
    title='VasculAR software',
    logo_path='imgs/logo.ico'
)
