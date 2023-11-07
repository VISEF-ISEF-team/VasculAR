import customtkinter
import pyrebase
from tkinter import messagebox

customtkinter.set_appearance_mode("dark")  
customtkinter.set_default_color_theme("blue") 


class LoginPage(customtkinter.CTkToplevel):
    def __init__(self, parent, title, auth):
        super().__init__()
        self.auth=auth
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
        self.frame.columnconfigure((0,1,2), weight=1)
        self.frame.rowconfigure((0,1,2,3), weight=1)
        self.create_widget(self.frame)
        
    def close_toplevel(self):
        self.destroy()
        
    def create_account(self):
        org_id = self.org_id.get()
        password = self.password.get()
        try:
            organization = self.auth.create_user_with_email_and_password(org_id, password)
            messagebox.showinfo("Success", "Successfully account registration")
        except:
            messagebox.showinfo("Failed" ,"Try again")
    
    def login_account(self):
        org_id = self.org_id.get()
        password = self.password.get()
        try:
            organization = self.auth.sign_in_with_email_and_password(org_id, password)
            messagebox.showinfo("Success", "Successfully login account")
        except:
            messagebox.showinfo("Failed" ,"Wrong email or password")
        
    def create_widget(self, parent):        
        self.header = customtkinter.CTkLabel(master=parent, text="Database Login", anchor="w", font=(self.font, 30, "bold"))
        self.header.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='w')
        
        self.org_label = customtkinter.CTkLabel(master=parent, text='Organization ID: ')
        self.org_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.org_id = customtkinter.CTkEntry(master=parent, placeholder_text="organization id", width=int(self.winfo_screenwidth()/5.5))
        self.org_id.grid(row=1, column=1, padx=10, pady=10, sticky='e')
        
        self.password_label = customtkinter.CTkLabel(master=parent, text='Password: ')
        self.password_label.grid(row=2, column=0, padx=10, pady=10, sticky='w')
        self.password = customtkinter.CTkEntry(master=parent, placeholder_text="password", width=int(self.winfo_screenwidth()/5.5))
        self.password.grid(row=2, column=1, padx=10, pady=10, sticky='e')
        
        self.submit_btn = customtkinter.CTkButton(master=parent, text='Submit', command=self.login_account)
        self.submit_btn.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky='we')
        