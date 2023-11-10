import customtkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

class NoteWindow(customtkinter.CTkToplevel):
    def __init__(self,
                 layer_name,
                 analysis,
                 width: int = 200,
                 title: str = "Note your analysis",
                 initial_color: str = None,
                 bg_color: str = None,
                 fg_color: str = None,
                 button_color: str = None,
                 button_hover_color: str = None,
                 text: str = "Choose this color",
                 corner_radius: int = 24,
                 slider_border: int = 1,
                 **button_kwargs):
    
        super().__init__()
        self.title(title)
        self.WIDTH = width
        self.HEIGHT = self.WIDTH + 10
            
        self.maxsize(self.WIDTH, self.HEIGHT)
        self.minsize(self.WIDTH, self.HEIGHT)
        self.resizable(width=False, height=False)
        self.transient(self.master)
        
        self.layer_name = layer_name
        self.iconbitmap('imgs/logo.ico')
        self.renamed_header = layer_name
        self.analysis = analysis
        self.layer_name_edit()
        
        
    def layer_name_edit(self):
        self.header = customtkinter.CTkEntry(master=self, placeholder_text=self.layer_name, width=190, fg_color='transparent', justify='center')
        self.header.grid(row=0, column=0, padx=5, pady=5, sticky='new')
        self.textbox = customtkinter.CTkTextbox(master=self, width=self.WIDTH-10, height=self.HEIGHT-90)
        self.textbox.insert("0.0", self.analysis)
        self.textbox.grid(column=0, row=1, sticky='sew', padx=5, pady=5)
        self.btn_save = customtkinter.CTkButton(master=self, width=self.WIDTH-10, text="save", command=self.grab_release)
        self.btn_save.grid(column=0, row=2,  sticky='sew', padx=5, pady=5)
        
    def grab_release(self):
        self.renamed_header = self.header.get() if self.header.get() != "" else self.header.cget("placeholder_text")
        self.analysis = self.textbox.get("0.0", "end")
        self.destroy()
        
        
        