# from tkinter import *

# root = Tk()
# root.title('VasculAR software')
# root.iconbitmap('imgs/logo.ico')
# root.geometry("500x550")

# my_label = Label(root)
# my_label.pack(pady=20)

# def hello():
# 	my_label.config(text="Hello World!")

# def goodbye():
# 	my_label.config(text="Goodbye World!")

# def my_popup(e):
# 	my_menu.tk_popup(e.x_root, e.y_root)

# # Create a Menu
# my_menu = Menu(root, tearoff=False)
# my_menu.add_command(label="Say Hello", command=hello)
# my_menu.add_command(label="Say Goodbye", command=goodbye)
# my_menu.add_separator()
# my_menu.add_command(label="Exit", command=root.quit)

# root.bind("<Button-3>", my_popup)


# root.mainloop()


import customtkinter
customtkinter.set_appearance_mode("dark")  
customtkinter.set_default_color_theme("blue") 
app = customtkinter.CTk()
app.title('VasculAR software')
app.geometry("500x500")
app.iconbitmap('imgs/logo.ico')


canvas = customtkinter.CTkFrame(app, width=700, height=700)
canvas.pack()

def on_mousewheel (event):
    label.configure(text = f"{event.delta / 120} units")

label = customtkinter.CTkLabel(app, text='')
label.pack()
# bind the mouse wheel event to the canvas
canvas.bind("<MouseWheel>", on_mousewheel)


# def tool_popups(e):
#     label.configure(text=e.x)
#     label2.configure(text=e.y)
#     pos_x = e.x
#     if e.x > 500 and e.x < 700:
#         pos_x -= 100
#     frame.place(x=pos_x-100, y=e.y-120, anchor="nw")
#     option1.grid(column=0, row=0, padx=5, pady=5)
#     option2.grid(column=0, row=1, padx=5, pady=5)
    

# def hide_tool_popups(e):
#     frame.place_forget()

# label = customtkinter.CTkLabel(app, text='')
# label.pack()
# label2 = customtkinter.CTkLabel(app, text='')
# label2.pack()

# canvas.bind("<Button-3>", tool_popups)
# canvas.bind("<Button-1>", hide_tool_popups)

app.mainloop()



# # ======= POPUPS RIGHT CLICK =======
#     frame_right_click = customtkinter.CTkFrame(master=tab_1, width=200, height=200, fg_color='red')
#     frame_right_click.grid_columnconfigure(0, weight=1)
#     frame_right_click.grid_rowconfigure((0,1,2), weight=1)
#     option1 = customtkinter.CTkButton(frame_right_click, text='rotation', fg_color='transparent')
#     option2 = customtkinter.CTkButton(frame_right_click, text='highlight', fg_color='transparent')

#     def tool_popups(e):
#         print(e.x, e.y)
#         label.configure(text=e.x)
#         label2.configure(text=e.y)
#         pos_x = e.x
#         if e.x > 500 and e.x < 700:
#             pos_x -= 100
#         frame_right_click.place(x=pos_x-100, y=e.y-120, anchor="nw")
#         option1.grid(column=0, row=0, padx=5, pady=5)
#         option2.grid(column=0, row=1, padx=5, pady=5)
    

#     def hide_tool_popups(e):
#         frame_right_click.place_forget()
    
#     label = customtkinter.CTkLabel(app, text='')
#     label.grid(column=3, row=3)
#     label2 = customtkinter.CTkLabel(app, text='')
#     label2.grid(column=3, row=3)
#     tab_1.bind("<Button-3>", tool_popups)
#     tab_1.bind("<Button-1>", hide_tool_popups)


