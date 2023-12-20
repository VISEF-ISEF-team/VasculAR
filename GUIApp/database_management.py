import customtkinter
import pyrebase
from PIL import Image, ImageTk
import os
import sys
from io import BytesIO
from datetime import datetime
import requests

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


class DatabaseManagment(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("VasculAR - Patient Database Management")
        self.width = int(self.winfo_screenwidth()/1.6)
        self.height = int(self.winfo_screenheight()/1.6)
        self.iconpath = 'imgs/logo.ico'
        self.geometry(f"{self.width}x{self.height}")
        self.minsize(500, 500)
        self.iconbitmap(self.iconpath)
        self.font = customtkinter.ThemeManager.theme["CTkFont"]["family"]
        
        # create layouts
        self.create_layouts()
        
        self.mainloop()
        
    def create_layouts(self):
        self.frame = customtkinter.CTkFrame(master=self)
        self.frame.pack(expand=True, fill="both", padx=10, pady=10)
        self.frame.columnconfigure((0,1,2,3,4), weight=1)
        self.frame.rowconfigure(2, weight=1)
         
        self.label = customtkinter.CTkLabel(master=self.frame, text="Database Management", font=(self.font, 25, "bold"))
        self.label.grid(row=0, column=0, padx=20, pady=10, sticky='w')
        
        self.entry = customtkinter.CTkEntry(master=self.frame, placeholder_text="search", width=200)
        self.entry.grid(row=0, column=2, padx=10, pady=10, sticky="e")
        self.entry.bind("<KeyRelease>", lambda e: self.search_data(self.entry.get()))
        
        self.about_button = customtkinter.CTkButton(master=self.frame, text="i", hover=False, width=30, command=self.open_about_window)
        self.about_button.grid(row=0, column=4, padx=10, pady=10, sticky="e")
        
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self.frame)
        self.scrollable_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=(0,10), sticky="nsew")
        
        self.info_frame = customtkinter.CTkScrollableFrame(self.frame)
        self.info_frame.grid(row=2, column=3, columnspan=2, padx=10, pady=(0,10), sticky="nsew")
        
        self.item_frame = {}
        self.read_cloud_database()
        
    def add_item(self, key, value):
        self.item_frame[key] = customtkinter.CTkFrame(self.scrollable_frame)
        self.item_frame[key].pack(expand=True, fill="x", padx=5, pady=5)
        self.item_frame[key].columnconfigure((0,1,2,3,4), weight=1)
        
        # case
        item_name = customtkinter.CTkButton(self.item_frame[key], fg_color="transparent",
                                            text_color=customtkinter.ThemeManager.theme["CTkLabel"]["text_color"],
                                            height=50, anchor="w", font=(self.font, 15, "bold"), width=250,
                                            text=f'Case {key[5:]}', hover=False, command=lambda: self.info_window(key, value))
        item_name.grid(row=0, column=0, sticky="ew", pady=5, padx=5)
        
        # patient name
        patient_name = customtkinter.CTkLabel(self.item_frame[key], width=250, justify="left", text=value["dict_info"]["Patient's name"], anchor="w", wraplength=250)
        patient_name.grid(row=0, column=1, padx=5)
        
        # Modality
        modality_name = customtkinter.CTkLabel(self.item_frame[key], width=250, justify="left", text=value["dict_info"]["Modality"], anchor="w", wraplength=250)
        modality_name.grid(row=0, column=2, padx=5)
        
        # Acquisition date
        date = datetime.strptime(value["dict_info"]["Acquisition Date"], "%Y%m%d").strftime("%d/%m/%Y")
        date_name = customtkinter.CTkLabel(self.item_frame[key], width=250, justify="left", text=date, anchor="w", wraplength=250)
        date_name.grid(row=0, column=3, padx=5)
        
        # Body part
        body_part = customtkinter.CTkLabel(self.item_frame[key], width=250, justify="left", text=value["dict_info"]["Body Part Examined"], anchor="w", wraplength=250)
        body_part.grid(row=0, column=4, padx=5)
        
    def info_window(self, key, value):
        image_url = value['folder_imgs'][key]['canvas_0']
        response = requests.get(image_url)
        img_data = BytesIO(response.content)
        img = Image.open(img_data).resize((300, 300))
        tk_img = ImageTk.PhotoImage(img)
        label = customtkinter.CTkLabel(self.info_frame, image=tk_img, text='')
        label.pack()
        label.image = tk_img
    
    def search_data(self):
        print("search data")
        
    def open_about_window(self):
        print("open about window")
        
    def read_cloud_database(self):
        data_snapshot = db.get().val()
        for key, value in data_snapshot.items():
            self.add_item(key, value)
        
database_management = DatabaseManagment()