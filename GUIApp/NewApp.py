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
        self.MenuBar()

    def login(self):
        self.login_page = LoginPage(
            parent=self,
            title='VasculAR login',
            auth=auth
        )

    def MenuBar(self):
        self.current_menu = None

        def file_dropdown_options(master):
            self.add_nifti_file_btn = customtkinter.CTkButton(
                master=master, text="Add Nifti file", fg_color='transparent', hover_color=self.second_color)
            self.add_nifti_file_btn.pack(padx=5, pady=5)
            self.add_nifti_file_btn.configure(anchor="w")

            self.add_dcm_series_btn = customtkinter.CTkButton(
                master=master, text="Add DCM series",  fg_color='transparent', hover_color=self.second_color)
            self.add_dcm_series_btn.pack(padx=5, pady=5)
            self.add_dcm_series_btn.configure(anchor="w")
            
            self.save_case_btn = customtkinter.CTkButton(
                master=master, text="Save case",  fg_color='transparent', hover_color=self.second_color)
            self.save_case_btn.pack(padx=5, pady=5)
            self.save_case_btn.configure(anchor="w")
            
            self.export_analysis_btn = customtkinter.CTkButton(
                master=master, text="Export analysis",  fg_color='transparent', hover_color=self.second_color)
            self.export_analysis_btn.pack(padx=5, pady=5)
            self.export_analysis_btn.configure(anchor="w")

        def setting_dropdown_options(master):
            self.theme_setting_btn = customtkinter.CTkButton(
                master=master, text="Theme color", fg_color='transparent', hover_color=self.second_color)
            self.theme_setting_btn.pack(padx=5, pady=5)
            self.theme_setting_btn.configure(anchor="w")

            self.language_setting_btn = customtkinter.CTkButton(
                master=master, text="Language",  fg_color='transparent', hover_color=self.second_color)
            self.language_setting_btn.pack(padx=5, pady=5)
            self.language_setting_btn.configure(anchor="w")

        def dropdown(widget_option, col):
            hide_all_menu()
            self.dropdown = customtkinter.CTkFrame(master=self)

            if widget_option.cget("text") == 'File':
                file_dropdown_options(master=self.dropdown)
            elif widget_option.cget("text") == 'Setting':
                setting_dropdown_options(master=self.dropdown)

            x = widget_option.winfo_x() - 10*col
            self.dropdown.place(
                x=x,
                y=30
            )
            self.current_menu = self.dropdown

        def hide_all_menu():
            if self.current_menu:
                self.current_menu.place_forget()
                self.current_menu = None

        self.menu_frame = customtkinter.CTkFrame(
            master=self, fg_color='transparent')
        self.menu_frame.grid(row=0, column=0, columnspan=15, sticky='w')
        self.menu_frame.rowconfigure((0, 1, 2), weight=1, uniform='a')

        self.file_btn = customtkinter.CTkButton(
            master=self.menu_frame,
            text='File',
            fg_color='transparent',
            width=10,
            command=lambda: dropdown(widget_option=self.file_btn, col=0)
        )
        self.file_btn.grid(row=0, column=0, padx=(5, 0), sticky='w')

        self.setting_btn = customtkinter.CTkButton(
            master=self.menu_frame,
            text='Setting',
            fg_color='transparent',
            width=10,
            command=lambda: dropdown(widget_option=self.setting_btn, col=1)
        )
        self.setting_btn.grid(row=0, column=1, padx=(5, 0), sticky='w')

        self.help_btn = customtkinter.CTkButton(
            master=self.menu_frame,
            text='Help',
            fg_color='transparent',
            width=10,
            command=lambda: dropdown(widget_option=self.help_btn, col=2)
        )
        self.help_btn.grid(row=0, column=2, padx=(5, 0), sticky='w')

        self.about_btn = customtkinter.CTkButton(
            master=self.menu_frame,
            text='About',
            fg_color='transparent',
            width=10,
            command=lambda: dropdown(widget_option=self.about_btn, col=3)
        )
        self.about_btn.grid(row=0, column=3, padx=(5, 0), sticky='w')
        self.bind("<Double-Button-1>", lambda event: hide_all_menu())


app = App(
    title='VasculAR software',
    logo_path='imgs/logo.ico'
)
app.mainloop()
