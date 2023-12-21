import customtkinter
from PIL import Image, ImageTk

class defectEducation(customtkinter.CTkToplevel):
    def __init__(self, parent, info):
        super().__init__()
        self.title("Cardiovascular Diseases Information")
        self.transient(parent)
        self.width = int(self.winfo_screenwidth()/4.7)
        self.height = int(self.winfo_screenheight()/2.5)
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)
        self.font = customtkinter.ThemeManager.theme["CTkFont"]["family"]
        self.info = info
        self.display()
        
    def display(self):
        self.defect_frame = customtkinter.CTkScrollableFrame(master=self)
        self.defect_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # image
        for index, img_link in self.info['image'].items():
            original_image = Image.open(img_link)
            desired_width = 350
            aspect_ratio = original_image.width / original_image.height
            desired_height = int(desired_width / aspect_ratio)        
            defect_image = customtkinter.CTkImage(dark_image=Image.open(img_link), size=(desired_width, desired_height))
            image_label = customtkinter.CTkLabel(self.defect_frame, image=defect_image, text="") 
            image_label.pack()
            image_label.image = defect_image
        
        # Defect name
        defect_name = customtkinter.CTkLabel(self.defect_frame, text=self.info['defect'], wraplength=300, font=(self.font, 15, "bold"))
        defect_name.pack(padx=10, pady=(10,5))
                
        # Description
        des_label = customtkinter.CTkLabel(self.defect_frame, text=self.info['description'], wraplength=300, font=(self.font, 12))
        des_label.pack(padx=10)
        
        self.mainloop()