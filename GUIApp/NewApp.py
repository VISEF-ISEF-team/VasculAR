'''
VasculAR software
Author: Nguyen Le Quoc Bao
Version: 0.2
Competition: Visef & Isef
'''

import customtkinter
import tkinter
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
        self.create_widget()
        self.layout_widget()
        
    def file_dropdown_options(self, master):
        self.add_nifti_file_btn = customtkinter.CTkButton(
            master=master, text="Add Nifti file", fg_color='transparent', hover_color=self.master.second_color)
        self.add_nifti_file_btn.pack(padx=5, pady=5)
        self.add_nifti_file_btn.configure(anchor="w")

        self.add_dcm_series_btn = customtkinter.CTkButton(
            master=master, text="Add DCM series",  fg_color='transparent', hover_color=self.master.second_color)
        self.add_dcm_series_btn.pack(padx=5, pady=5)
        self.add_dcm_series_btn.configure(anchor="w")
            
        self.save_case_btn = customtkinter.CTkButton(
            master=master, text="Save case",  fg_color='transparent', hover_color=self.master.second_color)
        self.save_case_btn.pack(padx=5, pady=5)
        self.save_case_btn.configure(anchor="w")
            
        self.export_analysis_btn = customtkinter.CTkButton(
            master=master, text="Export analysis",  fg_color='transparent', hover_color=self.master.second_color)
        self.export_analysis_btn.pack(padx=5, pady=5)
        self.export_analysis_btn.configure(anchor="w")

    def setting_dropdown_options(self, master):
        self.theme_setting_btn = customtkinter.CTkButton(
                master=master, text="Theme color", fg_color='transparent', hover_color=self.master.second_color)
        self.theme_setting_btn.pack(padx=5, pady=5)
        self.theme_setting_btn.configure(anchor="w")

        self.language_setting_btn = customtkinter.CTkButton(
                master=master, text="Language",  fg_color='transparent', hover_color=self.master.second_color)
        self.language_setting_btn.pack(padx=5, pady=5)
        self.language_setting_btn.configure(anchor="w")
        
    def help_dropdown_options(self, master):
        self.basic_functions_btn = customtkinter.CTkButton(
                master=master, text="Basic Functions", fg_color='transparent', hover_color=self.master.second_color)
        self.basic_functions_btn.pack(padx=5, pady=5)
        self.basic_functions_btn.configure(anchor="w")
        
        self.reconstruction_btn = customtkinter.CTkButton(
                master=master, text="3D reconstruction", fg_color='transparent', hover_color=self.master.second_color)
        self.reconstruction_btn.pack(padx=5, pady=5)
        self.reconstruction_btn.configure(anchor="w")
        
        self.connection_btn = customtkinter.CTkButton(
                master=master, text="VR & AR connection", fg_color='transparent', hover_color=self.master.second_color)
        self.connection_btn.pack(padx=5, pady=5)
        self.connection_btn.configure(anchor="w")
        
    def about_dropdown_options(self, master):
        self.about_window = AboutWindow(
            parent=self.master,
            title='About VasculAR Software',
        )
    
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
                self.file_dropdown_options(master=self.dropdown)
            elif widget_option.cget("text") == 'Setting':
                self.setting_dropdown_options(master=self.dropdown)
            elif widget_option.cget("text") == 'Help':
                self.help_dropdown_options(master=self.dropdown)

        
        elif widget_option.cget("text") == 'About':
            self.about_dropdown_options(master=self.dropdown)
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

        self.file_btn = customtkinter.CTkButton(
            master=self.menu_frame,
            text='File',
            fg_color='transparent',
            width=10,
            command=lambda: self.dropdown_frame(widget_option=self.file_btn, col=0)
        )

        self.setting_btn = customtkinter.CTkButton(
            master=self.menu_frame,
            text='Setting',
            fg_color='transparent',
            width=10,
            command=lambda: self.dropdown_frame(widget_option=self.setting_btn, col=1)
        )

        self.help_btn = customtkinter.CTkButton(
            master=self.menu_frame,
            text='Help',
            fg_color='transparent',
            width=10,
            command=lambda: self.dropdown_frame(widget_option=self.help_btn, col=2)
        )

        self.about_btn = customtkinter.CTkButton(
            master=self.menu_frame,
            text='About',
            fg_color='transparent',
            width=10,
            command=lambda: self.dropdown_frame(widget_option=self.about_btn, col=3)
        )
        
        self.account_btn = customtkinter.CTkButton(
            master=self.menu_frame,
            text='Account',
            fg_color='transparent',
            width=10,
            command=lambda: self.dropdown_frame(widget_option=self.account_btn, col=4)
        )
        
        self.master.bind("<Double-Button-1>", lambda event: self.hide_all_menu())
        
    def layout_widget(self):
        self.file_btn.grid(row=0, column=0, padx=(5, 0), sticky='w')
        self.setting_btn.grid(row=0, column=1, padx=(5, 0), sticky='w')
        self.help_btn.grid(row=0, column=2, padx=(5, 0), sticky='w')
        self.about_btn.grid(row=0, column=3, padx=(5, 0), sticky='w')
        self.account_btn.grid(row=0, column=4, padx=(5, 0), sticky='w') 
        

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

        # column and rows
        for i in range(15):
            self.rowconfigure(i, weight=1, uniform='a')
            self.columnconfigure(i, weight=1, uniform='a')

        for i in range(15):
            for j in range(15):
                self.label = customtkinter.CTkFrame(
                    self, fg_color='transparent')
                self.label.grid(column=i, row=j, sticky='nsew')

        # create menu
        self.menu_bar = MenuBar(self)
        

        

        

app = App(
    title='VasculAR software',
    logo_path='imgs/logo.ico'
)
app.mainloop()
