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
# from readdcm import ReadDCM
import cv2 
import numpy as np
import matplotlib.pyplot as plt
import webbrowser
from cloud_database import LoginPage

customtkinter.set_appearance_mode("dark")  
customtkinter.set_default_color_theme("blue") 

class App(customtkinter.CTk):
    def __init__(self, title, logo_path):
        super().__init__()
        self.title(title)
        self.width = int(self.winfo_screenwidth()/1.05)
        self.height = int(self.winfo_screenheight()/1.1)
        self.geometry(f"{self.width}x{self.height}")
        self.minsize(500, 500)
        self.iconbitmap(logo_path)
        
        self.login_btn = customtkinter.CTkButton(master=self, text='login', command=self.login)
        self.login_btn.pack()
        
    def login(self):
        self.login_page = LoginPage(
            parent=self,
            title='VasculAR login'
        )
        
app = App(
    title='VasculAR software',
    logo_path='imgs/logo.ico'
)
app.mainloop()