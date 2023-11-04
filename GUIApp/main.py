import customtkinter
import tkinter
from PIL import Image, ImageEnhance, ImageTk
import SimpleITK as sitk
import matplotlib.pyplot as plt
import cv2 
import numpy as np
from tkinter import filedialog, Canvas
from helpers import *
from draw import draw_canvas
from color_picker_customized import Colorpicker
import os
from readdcm import ReadDCM
from CTkRangeSlider import *

# ====== 1. WINDOW CONFIGURATION SECTION ======
# 1.1 Window Theme
customtkinter.set_appearance_mode("dark")  
customtkinter.set_default_color_theme("blue") 
app = customtkinter.CTk()
app.title('VasculAR software')
app.geometry("1650x900")
app.iconbitmap('imgs/logo.ico')

img = None
img_raw = None
img_info = False
dict_info = {}
pixel_spacing = 0.858

# 1.2 Window Grid
for i in range(12): 
    app.rowconfigure(i, weight=1, uniform='a') 
    app.columnconfigure(i, weight=1, uniform='a') 
    
for i in range(12):
    for j in range(12):
        label = customtkinter.CTkFrame(app, fg_color="transparent")
        label.grid(column=i, row=j, sticky='nsew')
        
# ====== 2. FILE UPLOADER SECTION ======
def choose_file():
    global img, img_raw, img_info, dict_info
    img_info = True
    path = filedialog.askopenfilename()
    
    if path.endswith('.nii.gz') or path.endswith('.nii'):
        file_path.configure(placeholder_text=path)
        img_raw = sitk.ReadImage(path, sitk.sitkFloat32)
        img = sitk.GetArrayFromImage(img_raw)
    
    elif path.endswith('.dcm'):
        parent_dir = os.path.dirname(path)
        instance = ReadDCM(parent_dir)
        img_raw, img, dict_info, pixel_spacing = instance.read_file_dcm()
        print(dict_info)
    
    app.event_generate("<<UpdateApp>>")
   
# 2.1 Uploader Frame
uploader_frame = customtkinter.CTkFrame(app)
uploader_frame.grid(column=0, row=0, columnspan=2, rowspan=2, sticky='nsew', padx=5)
uploader_frame.grid_columnconfigure(0, weight=1)
uploader_frame.grid_rowconfigure((0, 1, 2), weight=1) 

# 2.2 Uploader Content
label_text = customtkinter.CTkButton(uploader_frame, text='File uploader', state='disabled', fg_color='#3b3b3b', text_color_disabled='#dce4e2')
label_text.grid(column=0, row=0, sticky="ew", padx=10, pady=0.5)
file_path = customtkinter.CTkEntry(uploader_frame, placeholder_text="File path here")
file_path.grid(column=0, row=1, sticky="ew",  padx=10)
choose_button = customtkinter.CTkButton(uploader_frame, text="Choose File", command=choose_file)
choose_button.grid(column=0, row=2, sticky="ew", padx=10)
    
def update_app(event):
    global img, img_info, img_raw, dict_info
    print(img.shape)
    
    # ====== 3. IMAGE INFO SECTION ======
    # 3.1 Image info frame
    info_frame = customtkinter.CTkScrollableFrame(app, orientation='horizontal', label_text='Image info')
    info_frame.grid(column=0, row=2, columnspan=2, rowspan=4, sticky='nsew', pady=5, padx=5)
    info_frame.grid_columnconfigure(0, weight=1)
    info_frame.grid_columnconfigure(1, weight=2)
    info_frame.grid_rowconfigure((0, 1, 2, 3), weight=1)

    # 3.2 Show info
    info = show_sitk_img_info(img_raw)
    for i, (k, v) in enumerate(info.items()):
        label1 = customtkinter.CTkLabel(info_frame, text=k)
        label1.grid(column=0, row=i, sticky="w", padx=5)
                    
        label2 = customtkinter.CTkLabel(info_frame, text=v)
        label2.grid(column=1, row=i, sticky="w", padx=5)
        

    # 3.3 When choosed -> change img_raw, img
    def supporting_functions_callback(choice):
        global img, img_info, img_raw
        if choice == 'None':
            img_raw_supported = img_raw
        if choice == 'Denoise':
            img_raw_supported = sitk.CurvatureFlow(img_raw)
        elif choice == 'Blurring':
            img_raw_supported = sitk.DiscreteGaussian(img_raw)
        elif choice == 'GrayscaleErode':
            img_raw_supported = sitk.GrayscaleErode(img_raw)
        elif choice == 'OtsuThreshold':
            img_raw_supported = sitk.OtsuThreshold(img_raw, 0, 1)
        elif choice == 'LiThreshold':
            img_raw_supported = sitk.LiThreshold(img_raw, 0, 1)
        elif choice == 'MomentsThreshold':
            img_raw_supported = sitk.MomentsThreshold(img_raw, 0, 1)
            
        img = sitk.GetArrayFromImage(img_raw_supported)
    
    
    # ====== 4. MAIN CANVAS ======      
    # 4.1 Tab View    
    tabview = customtkinter.CTkTabview(master=app) # add command argument here
    tabview.grid(column=2, row=1, columnspan=8, rowspan=8, sticky="nsew", pady=(5, 0))
    tab_1 = tabview.add("axial")    
    tab_2 = tabview.add("sagittal")
    tab_3 = tabview.add("coronal")
    tabview.set("axial") 

    # 4.2 Slider Control
    # 4.2.1 Slider Control Function
    def slider_volume_show(value):
        index_slice = round(value, 0)
        text_show_volume.configure(text=int(index_slice))
        slice_control(index_slice, flip=flip_text_option.cget("text"))

    # 4.2.2 Slider Control Frame
    slider_control = customtkinter.CTkFrame(app)
    slider_control.grid(column=2, row=0, columnspan=2, rowspan=1, sticky='nsew')
    slider_control.grid_rowconfigure((0, 1), weight=1)
    slider_control.grid_columnconfigure(0, weight=2)
    slider_control.grid_columnconfigure(1, weight=1)

    # 4.2.3 Slider Control Content
    label_text = customtkinter.CTkButton(slider_control, text='View slice', state='disabled', fg_color='#3b3b3b', text_color_disabled='#dce4e2')
    label_text.grid(column=0, row=0, columnspan=2, sticky="ew", padx=10, pady=0.5)
    slider_volume = customtkinter.CTkSlider(slider_control, from_=0, to=img.shape[0]-1, command=slider_volume_show, bg_color='#2b2b2b')
    slider_volume.grid(column=0, row=1, sticky='ew', padx=5)
    text_show_volume = customtkinter.CTkLabel(slider_control, text="", bg_color='#2b2b2b')
    text_show_volume.grid(column=1, row=1, sticky='ew')
        
    # 4.3 Color Picker
    # 4.3.1 Color Picker Frame
    color_picker_frame = customtkinter.CTkFrame(app)
    color_picker_frame.grid(column=4, row=0, columnspan=2, rowspan=1, sticky='nsew', padx=5)
    color_picker_frame.grid_rowconfigure((0, 1), weight=1)
    color_picker_frame.grid_columnconfigure(0, weight=1)

    # 4.3.2 Color Picker Content
    label_text = customtkinter.CTkButton(color_picker_frame, text='Color picker', state='disabled', fg_color='#3b3b3b', text_color_disabled='#dce4e2')
    label_text.grid(column=0, row=0, columnspan=2, sticky="ew", padx=10, pady=0.5)
    colors = ["gray", "nipy_spectral", "viridis", "plasma", "inferno", "magma", "cividis", "Greys", "Purples", "Blues", "Greens", "Reds", "YlOrBr", "YlOrRd", "OrRd", "PuRd", "GnBu"]
    color_picker_default = customtkinter.StringVar(value="gray")
    color_picker = customtkinter.CTkComboBox(color_picker_frame, values=colors, variable=color_picker_default)
    color_picker.grid(column=0, row=1, sticky='ew', padx=10)

    # 4.4 Drawing Canvas
    # 4.4.1 Draw Control Frame
    draw_control = customtkinter.CTkFrame(app)
    draw_control.grid(column=6, row=0, columnspan=2, rowspan=1, sticky='nsew')
    draw_control.grid_rowconfigure((0, 1), weight=1)
    draw_control.grid_columnconfigure(0, weight=2)

    # 4.4.2 Show Distance Control Frame
    distance_control = customtkinter.CTkFrame(app, fg_color='#242424')
    distance_control.grid(column=8, row=1, columnspan=2, rowspan=3, pady=35)
    distance_control.grid_rowconfigure((0, 1), weight=1)
    distance_control.grid_columnconfigure(0, weight=1)

    # 4.4.3 General Setup
    radio_var = tkinter.IntVar(value=0)
    line_distance = customtkinter.CTkLabel(distance_control, text="")
    coordinate_label = customtkinter.CTkLabel(distance_control, text="")
    header_calculation = customtkinter.CTkLabel(distance_control, text="Calculation", fg_color="#3b3b3b", corner_radius=5)
    header_calculation.grid(row=0, column=0, padx=10, sticky='nsew', pady=5)
    line_distance.grid(row=1, column=0, padx=10, sticky='w')
    coordinate_label.grid(row=2, column=0, padx=10, sticky='w')
    res_list = []

    # ======= 5. AXIAL VIEW =======
    # 5.1 Axial Canvas
    my_canvas_axial = Canvas(tab_1, width=800, height=800, bg='#2b2b2b', border=0)
    my_canvas_axial.place(relx=0.5, rely=0.5, anchor="center")
    draw_canvas_axial = draw_canvas(my_canvas_axial, radio_var, line_distance, coordinate_label, res_list, pixel_spacing)

    # 5.2 Mouse Bind Function Axial
    my_canvas_axial.bind("<Button-1>", draw_canvas_axial.on_press)
    my_canvas_axial.bind("<ButtonRelease-1>", draw_canvas_axial.on_release)
    my_canvas_axial.bind("<Motion>", draw_canvas_axial.show_coords)

    # 5.3 Redo & Clear Buttons
    clear_button = customtkinter.CTkButton(draw_control, text="Clear", command=draw_canvas_axial.clear)
    clear_button.grid(column=0, row=1, padx=5)
    redo_button = customtkinter.CTkButton(draw_control, text="Redo", command=draw_canvas_axial.redo)
    redo_button.grid(column=1, row=1, padx=5)

    # 5.4 Rectangle & Line Display 
    Rectangle_axial = customtkinter.CTkRadioButton(draw_control, text="Rectangle", command=draw_canvas_axial.radiobutton_event, variable=radio_var, value=1)
    line_axial = customtkinter.CTkRadioButton(draw_control, text="Line", command=draw_canvas_axial.radiobutton_event, variable=radio_var, value=2)
    Rectangle_axial.grid(column=0, row=0)
    line_axial.grid(column=1, row=0)


    # ======= 6. SAGITTAL VIEW =======
    my_canvas_sagittal = Canvas(tab_2, width=800, height=800, bg='#2b2b2b', border=0)
    my_canvas_sagittal.place(relx=0.5, rely=0.5, anchor="center")
    draw_canvas_sagittal = draw_canvas(my_canvas_sagittal, radio_var, line_distance, coordinate_label, res_list, pixel_spacing)

    # 6.2 Mouse Bind Function Sagittal
    my_canvas_sagittal.bind("<Button-1>", draw_canvas_sagittal.on_press)
    my_canvas_sagittal.bind("<ButtonRelease-1>", draw_canvas_sagittal.on_release)
    my_canvas_sagittal.bind("<Motion>", draw_canvas_sagittal.show_coords)

    # 6.3 Redo & Clear Buttons
    clear_button = customtkinter.CTkButton(draw_control, text="Clear", command=draw_canvas_sagittal.clear)
    clear_button.grid(column=0, row=1, padx=5)
    redo_button = customtkinter.CTkButton(draw_control, text="Redo", command=draw_canvas_sagittal.redo)
    redo_button.grid(column=1, row=1, padx=5)

    # 6.4 Rectangle & Line Display 
    Rectangle_sagittal = customtkinter.CTkRadioButton(draw_control, text="Rectangle", command=draw_canvas_sagittal.radiobutton_event, variable=radio_var, value=1)
    line_sagittal = customtkinter.CTkRadioButton(draw_control, text="Line", command=draw_canvas_sagittal.radiobutton_event, variable=radio_var, value=2)
    Rectangle_sagittal.grid(column=0, row=0)
    line_sagittal.grid(column=1, row=0)

    # ======= 7. CORONAL VIEW =======
    my_canvas_coronal = Canvas(tab_3, width=800, height=800, bg='#2b2b2b', border=0)
    my_canvas_coronal.place(relx=0.5, rely=0.5, anchor="center")
    draw_canvas_coronal = draw_canvas(my_canvas_coronal, radio_var, line_distance, coordinate_label, res_list, pixel_spacing)

    # 7.2 Mouse Bind Function Coronal
    my_canvas_coronal.bind("<Button-1>", draw_canvas_coronal.on_press)
    my_canvas_coronal.bind("<ButtonRelease-1>", draw_canvas_coronal.on_release)
    my_canvas_coronal.bind("<Motion>", draw_canvas_coronal.show_coords)

    # 7.3 Redo & Clear Buttons
    clear_button = customtkinter.CTkButton(draw_control, text="Clear", command=draw_canvas_coronal.clear)
    clear_button.grid(column=0, row=1, padx=5)
    redo_button = customtkinter.CTkButton(draw_control, text="Redo", command=draw_canvas_coronal.redo)
    redo_button.grid(column=1, row=1, padx=5)

    # 7.4 Rectangle & Line Display 
    Rectangle_coronal = customtkinter.CTkRadioButton(draw_control, text="Rectangle", command=draw_canvas_coronal.radiobutton_event, variable=radio_var, value=1)
    line_coronal = customtkinter.CTkRadioButton(draw_control, text="Line", command=draw_canvas_coronal.radiobutton_event, variable=radio_var, value=2)
    Rectangle_coronal.grid(column=0, row=0)
    line_coronal.grid(column=1, row=0)
    
    # ======= BRIGHTNESS & CONTRAST CONTROL =======
    alpha_frame = customtkinter.CTkFrame(app)
    alpha_frame.grid(column=8, row=5, columnspan=2, rowspan=2, pady=5)    
    alpha_text = customtkinter.StringVar(value="1")
    alpha_control = customtkinter.CTkEntry(alpha_frame, placeholder_text="1", textvariable=alpha_text)
    alpha_control.grid(row=0, column=0, padx=5)

    def update_range_slider(value):
        btn_left_entry.configure(state='normal')
        btn_right_entry.configure(state='normal')
        btn_left_entry.configure(placeholder_text=value[0])
        btn_right_entry.configure(placeholder_text=value[1])
        btn_left_entry.configure(state='disabled')
        btn_right_entry.configure(state='disabled')
        slice_control(slider_volume.get(), flip=flip_text_option.cget("text"))
        
    def left_increase_hf():
        hf1, hf2 = int(round(range_slider.get()[0], 0)), int(round(range_slider.get()[1], 0))
        hf1 += 50
        range_slider.set([hf1, hf2])
        btn_left_entry.configure(state='normal')
        btn_right_entry.configure(state='normal')
        btn_left_entry.configure(placeholder_text=hf1)
        btn_right_entry.configure(placeholder_text=hf2)
        btn_left_entry.configure(state='disabled')
        btn_right_entry.configure(state='disabled')
        
    def left_decrease_hf():
        hf1, hf2 = int(round(range_slider.get()[0], 0)), int(round(range_slider.get()[1], 0))
        hf1 -= 50
        range_slider.set([hf1, hf2])
        btn_left_entry.configure(state='normal')
        btn_right_entry.configure(state='normal')
        btn_left_entry.configure(placeholder_text=hf1)
        btn_right_entry.configure(placeholder_text=hf2)
        btn_left_entry.configure(state='disabled')
        btn_right_entry.configure(state='disabled')
    
    def right_increase_hf():
        hf1, hf2 = int(round(range_slider.get()[0], 0)), int(round(range_slider.get()[1], 0))
        hf2 += 50
        range_slider.set([hf1, hf2])
        btn_left_entry.configure(state='normal')
        btn_right_entry.configure(state='normal')
        btn_left_entry.configure(placeholder_text=hf1)
        btn_right_entry.configure(placeholder_text=hf2)
        btn_left_entry.configure(state='disabled')
        btn_right_entry.configure(state='disabled')
        
    def right_decrease_hf():
        hf1, hf2 = int(round(range_slider.get()[0], 0)), int(round(range_slider.get()[1], 0))
        hf2 -= 50
        range_slider.set([hf1, hf2])
        btn_left_entry.configure(state='normal')
        btn_right_entry.configure(state='normal')
        btn_left_entry.configure(placeholder_text=hf1)
        btn_right_entry.configure(placeholder_text=hf2)
        btn_left_entry.configure(state='disabled')
        btn_right_entry.configure(state='disabled')
        
        
    # ======= POPUPS RIGHT CLICK =======
    # ======= Axial =======
    def flip_horizontal():
        flip_text_option.configure(text="horizontal")
        frame_right_click.place_forget()
        frame_right_click_2.place_forget()
        frame_right_click_3.place_forget()
        
    def flip_vertical():
        flip_text_option.configure(text="vertical")
        frame_right_click.place_forget()
        frame_right_click_2.place_forget()
        frame_right_click_3.place_forget()
        
        
    flip_text_option = customtkinter.CTkLabel(app, text="")
    frame_right_click = customtkinter.CTkFrame(master=my_canvas_axial, width=200, height=200, fg_color='transparent')
    flip_horizontal_option = customtkinter.CTkButton(frame_right_click, text='flip horizontal', fg_color='transparent', command=flip_horizontal)
    flip_vertical_option = customtkinter.CTkButton(frame_right_click, text='flip vertical', fg_color='transparent', command=flip_vertical)

    def tool_popups(e):
        pos_x = e.x
        if e.x > 500 and e.x < 700:
            pos_x -= 100
        frame_right_click.place(x=e.x-100, y=e.y-120, anchor="nw")
        flip_horizontal_option.grid(column=0, row=0, padx=5, pady=5)
        flip_vertical_option.grid(column=0, row=1, padx=5, pady=5)
    
    def hide_tool_popups(e):
        frame_right_click.place_forget()
    
    my_canvas_axial.bind("<Button-3>", tool_popups)
    my_canvas_axial.bind("<Double-Button-1>", hide_tool_popups)
    
    # ======= Sagittal =======
    frame_right_click_2 = customtkinter.CTkFrame(master=my_canvas_sagittal, width=200, height=200, fg_color='transparent')
    flip_horizontal_option_2 = customtkinter.CTkButton(frame_right_click_2, text='flip horizontal', fg_color='transparent', command=flip_horizontal)
    flip_vertical_option_2 = customtkinter.CTkButton(frame_right_click_2, text='flip vertical', fg_color='transparent', command=flip_vertical)

    def tool_popups_2(e):
        pos_x = e.x
        if e.x > 500 and e.x < 700:
            pos_x -= 100
        frame_right_click_2.place(x=e.x-100, y=e.y-120, anchor="nw")
        flip_horizontal_option_2.grid(column=0, row=0, padx=5, pady=5)
        flip_vertical_option_2.grid(column=0, row=1, padx=5, pady=5)
    
    def hide_tool_popups_2(e):
        frame_right_click_2.place_forget()
    
    my_canvas_sagittal.bind("<Button-3>", tool_popups_2)
    my_canvas_sagittal.bind("<Double-Button-1>", hide_tool_popups_2)
    
    # ======= Coronal =======
    frame_right_click_3 = customtkinter.CTkFrame(master=my_canvas_coronal, width=200, height=200, fg_color='transparent')
    flip_horizontal_option_3 = customtkinter.CTkButton(frame_right_click_3, text='flip horizontal', fg_color='transparent', command=flip_horizontal)
    flip_vertical_option_3 = customtkinter.CTkButton(frame_right_click_3, text='flip vertical', fg_color='transparent', command=flip_vertical)

    def tool_popups_3(e):
        pos_x = e.x
        if e.x > 500 and e.x < 700:
            pos_x -= 100
        frame_right_click_3.place(x=e.x-100, y=e.y-120, anchor="nw")
        flip_horizontal_option_3.grid(column=0, row=0, padx=5, pady=5)
        flip_vertical_option_3.grid(column=0, row=1, padx=5, pady=5)
    
    def hide_tool_popups_3(e):
        frame_right_click_3.place_forget()
    
    my_canvas_coronal.bind("<Button-3>", tool_popups_3)
    my_canvas_coronal.bind("<Double-Button-1>", hide_tool_popups_3)
    
    
    # ======= ZOOMING =======
    def zoom_axial(event):
        current_value = label_zoom.cget("text")
        new_value = int(current_value) + (event.delta/120)*6
        label_zoom.configure(text=new_value)
        slice_control(slider_volume.get(), flip=flip_text_option.cget("text"))
        
        
    label_zoom = customtkinter.CTkLabel(app, text="800")
    my_canvas_axial.bind("<MouseWheel>", zoom_axial)
    
    # ======= MOVING =======
    # def move(event):
    #     my_canvas_axial.moveto(my_image_temp,event.x-50,event.y-50)
    
    # img_temp = Image.open("D:/Documents/GitHub/VascuIAR/imgs/image.png")
    # resized_image = img_temp.resize((500,500))
    # image_temp = ImageTk.PhotoImage(resized_image)
    
    # my_image_temp = my_canvas_axial.create_image(0, 0, image=image_temp, anchor="nw")
    # my_canvas_axial.tag_bind(my_image_temp,"<Button1-Motion>", move, add="+")
    # my_canvas_axial.configure(scrollregion=my_canvas_axial.bbox(my_image_temp))
    
    # ======= 8. MAIN DISPLAY CONTROL =======
    def slice_control(index_slice, flip=None):
        view_axis = tabview.get()
        color_choice = plt.cm.bone if color_picker.get() == 'gray' else  color_picker.get()
        hf1, hf2 = int(round(range_slider.get()[0], 0)), int(round(range_slider.get()[1], 0))
        height = int(label_zoom.cget("text"))
        if view_axis == "axial":
            image = img[int(index_slice), :, :]
            image = np.where((image >= hf1) & (image <= hf2), image, 0)
            plt.imsave("temp.jpg", image, cmap=color_choice)
            image_display = cv2.imread("temp.jpg")
            brightness_image = cv2.convertScaleAbs(image_display, alpha=float(alpha_control.get()), beta=0)
            cv2.imwrite("temp.jpg", brightness_image)
            image_display = Image.open("temp.jpg").resize((height, height))
            
            if flip == 'vertical':
                image_display = image_display.transpose(Image.FLIP_TOP_BOTTOM)
            elif flip == 'horizontal':
                image_display = image_display.transpose(Image.FLIP_LEFT_RIGHT)
            
            my_image = ImageTk.PhotoImage(image_display)
            my_canvas_axial.create_image(400, 400, image=my_image, anchor="center")  
            my_canvas_axial.image = my_image
        
            
            my_canvas_axial.configure(bg='black')
            
        elif view_axis == "sagittal":
            image = img[:,int(index_slice), :]
            image = np.where((image >= hf1) & (image <= hf2), image, 0)
            plt.imsave("temp.jpg", image, cmap=color_choice)
            image_display = cv2.imread("temp.jpg")
            brightness_image = cv2.convertScaleAbs(image_display, alpha=float(alpha_control.get()), beta=0)
            cv2.imwrite("temp.jpg", brightness_image)
            image_display = Image.open("temp.jpg")
            
            if flip == 'vertical':
                image_display = image_display.transpose(Image.FLIP_TOP_BOTTOM)
            elif flip == 'horizontal':
                image_display = image_display.transpose(Image.FLIP_LEFT_RIGHT)
            
            image_display = image_display.resize((image_display.size[0] * height // image_display.size[1], height))
            my_image = ImageTk.PhotoImage(image_display)
            my_canvas_sagittal.create_image(400, 400, image=my_image, anchor="center")  
            my_canvas_sagittal.image = my_image
            my_canvas_sagittal.configure(bg='black')
            
        else:
            image = img[:, :, int(index_slice)]
            image = np.where((image >= hf1) & (image <= hf2), image, 0)
            plt.imsave("temp.jpg", image, cmap=color_choice)
            image_display = cv2.imread("temp.jpg")
            brightness_image = cv2.convertScaleAbs(image_display, alpha=float(alpha_control.get()), beta=0)
            cv2.imwrite("temp.jpg", brightness_image)
            image_display = Image.open("temp.jpg")
            
            if flip == 'vertical':
                image_display = image_display.transpose(Image.FLIP_TOP_BOTTOM)
            elif flip == 'horizontal':
                image_display = image_display.transpose(Image.FLIP_LEFT_RIGHT)
                
            image_display = image_display.resize((image_display.size[0] * height // image_display.size[1], height))
            my_image = ImageTk.PhotoImage(image_display)
            my_canvas_coronal.create_image(400, 400, image=my_image, anchor="center")  
            my_canvas_coronal.image = my_image
            my_canvas_coronal.configure(bg='black')


    # ======= 9. ANALYSIS TAKENOTE =======
    # 9.1 Analysis Takenote Frame
    note_frame = customtkinter.CTkFrame(app)
    note_frame.grid(column=10, row=3, columnspan=2, rowspan=9, sticky='nsew', padx=5, pady=10)
    note_frame.grid_columnconfigure(0, weight=1)
    note_frame.grid_rowconfigure((0,1,2,3,4,5,6,7,8), weight=1)

    # 9.2 Analysis Takenote Function
    def add_note():
        note = textbox.get("0.0", "end")
        label_note.configure(state='normal')
        label_note.insert("0.0", note)
        label_note.grid(column=0, row=1, stick='ew', padx=5, pady=5)
        label_note.configure(state='disabled')
        textbox.delete("0.0", "end")
        
    def clear_note():
        label_note.configure(state='normal')
        label_note.delete("0.0", "end")
        label_note.configure(state='disabled')

    # 9.3 Analysis Takenote Content
    header_note_frame = customtkinter.CTkButton(note_frame, text='Analysis note', state='disabled', fg_color='#3b3b3b', text_color_disabled='#dce4e2')
    header_note_frame.grid(column=0, row=0, sticky="new", padx=10, pady=5)

    label_note = customtkinter.CTkTextbox(note_frame) 
    label_note.grid(column=0, row=1, stick='ew', padx=5, pady=5) 
    label_note.configure(state='disabled')

    textbox = customtkinter.CTkTextbox(note_frame)
    textbox.grid(column=0, row=4, rowspan=5, stick='sew', padx=5, pady=5)
    btn_entry = customtkinter.CTkButton(note_frame, text="Save note", command=add_note)
    btn_entry.grid(column=0, row=9, stick='ew', padx=5, pady=5)

    btn_clear_entry = customtkinter.CTkButton(note_frame, text="Clear note", command=clear_note)
    btn_clear_entry.grid(column=0, row=3, stick='ew', padx=5, pady=5)

    # ======= 10. Automate Diseases Detector =======
    detector_frame = customtkinter.CTkFrame(app)
    detector_frame.grid(column=10, row=0, columnspan=2, rowspan=3, sticky='nsew', padx=5)
    detector_frame.grid_columnconfigure(0, weight=1)
    detector_frame.grid_rowconfigure((0,1,2,3), weight=1)

    # 10.2 Diseases Detector Takenote Function
    def switch_event():
        pass
        
    # 10.3 Diseases Detector Takenote Content
    header_detector_frame = customtkinter.CTkButton(detector_frame, text='Automate Detector', state='disabled', fg_color='#3b3b3b', text_color_disabled='#dce4e2')
    header_detector_frame.grid(column=0, row=0, sticky="new", padx=10, pady=5)

    detector_switch_var_1 = customtkinter.StringVar(value="on")
    detector_switch_1 = customtkinter.CTkSwitch(detector_frame, text="Coronary Artery Stenosis", command=switch_event, variable=detector_switch_var_1, onvalue="on", offvalue="off")
    detector_switch_1.grid(column=0, row=1, stick='we', padx=15)

    detector_switch_var_2 = customtkinter.StringVar(value="on")
    detector_switch_2 = customtkinter.CTkSwitch(detector_frame, text="Tetralogy of Fallot", command=switch_event, variable=detector_switch_var_2, onvalue="on", offvalue="off")
    detector_switch_2.grid(column=0, row=2, stick='we', padx=15)

    detector_switch_var_3 = customtkinter.StringVar(value="on")
    detector_switch_3 = customtkinter.CTkSwitch(detector_frame, text="Ventricular septal defect", command=switch_event, variable=detector_switch_var_3, onvalue="on", offvalue="off")
    detector_switch_3.grid(column=0, row=3, stick='we', padx=15)

    # ======= 11. Save Files Section =======
    # 11.1 Save File Frame
    save_frame = customtkinter.CTkFrame(app)
    save_frame.grid(column=0, row=6, columnspan=2, rowspan=3, sticky='nsew', padx=5)
    save_frame.grid_columnconfigure((0, 1), weight=1)
    save_frame.grid_rowconfigure(0, weight=1)
    save_frame.grid_rowconfigure((1,2,3), weight=2)

    # 11.2 Save Files Functions
    def choose_folder():
        filename = filedialog.askopenfilename()
        path_to_save.configure(placeholder_text=filename)

    # 11.3 Save File Content
    header_save_file = customtkinter.CTkButton(save_frame, text='Save files', state='disabled', fg_color='#3b3b3b', text_color_disabled='#dce4e2')
    header_save_file.grid(column=0, row=0, columnspan=2, rowspan=1, sticky="new", padx=10, pady=5)
    path_to_save = customtkinter.CTkEntry(save_frame, placeholder_text="Path to save")
    path_to_save.grid(column=0, row=1, columnspan=1, sticky="ew",  padx=10)
    button_folder = customtkinter.CTkButton(save_frame, text="Choose Folder", command=choose_folder)
    button_folder.grid(column=1, row=1, columnspan=1, sticky="ew", padx=10)


    check_var_1 = customtkinter.StringVar(value=".nii.gz")
    checkbox_1 = customtkinter.CTkCheckBox(save_frame, text="Main.nii.gz", variable=check_var_1, onvalue=".nii.gz", offvalue=".nii.gz off")
    checkbox_1.grid(column=0, row=2, padx=10)

    check_var_2 = customtkinter.StringVar(value=".txt")
    checkbox_2 = customtkinter.CTkCheckBox(save_frame, text="Analysis.txt", variable=check_var_1, onvalue=".txt", offvalue=".txt off")
    checkbox_2.grid(column=1, row=2, padx=10)

    check_var_3 = customtkinter.StringVar(value=".nii")
    checkbox_3 = customtkinter.CTkCheckBox(save_frame, text="Seg.nii.gz", variable=check_var_1, onvalue=".nii", offvalue=".nii off")
    checkbox_3.grid(column=0, row=3, padx=10)

    check_var_4 = customtkinter.StringVar(value=".stl")
    checkbox_4 = customtkinter.CTkCheckBox(save_frame, text="3D.stl", variable=check_var_1, onvalue=".stl", offvalue=".stl off")
    checkbox_4.grid(column=1, row=3, padx=10)

    # ======= 12. COLOR PICKER =======
    # 12.1 Color Picker Frame
    color_frame = customtkinter.CTkFrame(app)
    color_frame.grid(column=8, row=0, columnspan=2, rowspan=1, sticky='nsew', padx=5)
    color_frame.grid_columnconfigure((0), weight=1)
    color_frame.grid_rowconfigure((0, 1), weight=1)

    # 12.2 Color Picker Frame
    def open_color_picker(): 
        # create a new root window for the color picker 
        color_root = customtkinter.CTk() 
        customtkinter.set_appearance_mode("dark") 
        customtkinter.set_default_color_theme("blue") 
        Colorpicker(color_root) 
        color_root.mainloop()
        
    # 11.3 Save File Content
    header_color = customtkinter.CTkButton(color_frame, text='Color picker', state='disabled', fg_color='#3b3b3b', text_color_disabled='#dce4e2')
    header_color.grid(column=0, row=0, sticky="new", padx=10, pady=5)
    btn_color_picker = customtkinter.CTkButton(color_frame, text='Choose color', command=open_color_picker)
    btn_color_picker.grid(column=0, row=1, sticky="ew", padx=10, pady=5)


    # ======= 13. SEGMENTATION =======
    # 13.1 Segmentation Frame
    deep_frame = customtkinter.CTkFrame(app)
    deep_frame.grid(column=2, row=9, columnspan=4, rowspan=3, sticky='nsew', pady=10, padx=(0, 5))
    deep_frame.grid_columnconfigure((0,1,2,3), weight=1)
    deep_frame.grid_rowconfigure((0,1,2,3), weight=1)

    # 13.2 Segmentation Functions
    def start_segmentation():
        segmentation_progress_bar.start()

    def start_reeconstruction():
        reconstruction_progress_bar.start()
        
    # 13.3 Segmentation Content
    header_seg = customtkinter.CTkButton(deep_frame, text='Automate Segmentation & 3D Reconstruction', state='disabled', fg_color='#3b3b3b', text_color_disabled='#dce4e2')
    header_seg.grid(column=0, row=0, columnspan=4, sticky='new')

    models = ["Unet", "Unet Attention", "U-Resnet"]
    model_picker_default = customtkinter.StringVar(value="Unet")
    model_picker = customtkinter.CTkComboBox(deep_frame, values=models, variable=model_picker_default)
    model_picker.grid(column=0, row=1, columnspan=1, sticky='ew', padx=10, pady=10)

    segmentation_progress_bar = customtkinter.CTkProgressBar(deep_frame, orientation="horizontal")
    segmentation_progress_bar.set(0)
    segmentation_progress_bar.grid(column=1, row=2, sticky='ew', pady=5)

    seg_btn = customtkinter.CTkButton(deep_frame, text="Start segmentation", command=start_segmentation)
    seg_btn.grid(column=0, row=2, sticky='nw', padx=10, pady=10)

    reconstruction_progress_bar = customtkinter.CTkProgressBar(deep_frame, orientation="horizontal")
    reconstruction_progress_bar.set(0)
    reconstruction_progress_bar.grid(column=1, row=3, sticky='ew', pady=5)

    seg_btn = customtkinter.CTkButton(deep_frame, text="Start 3D reconstruction", command=start_reeconstruction)
    seg_btn.grid(column=0, row=3, sticky='nw', padx=10)


    # ======= 14. AI ASSISTANT =======
    # 14.1 Asistant Frame
    assitant_frame = customtkinter.CTkFrame(app)
    assitant_frame.grid(column=6, row=9, columnspan=4, rowspan=3, sticky='nsew', pady=10, padx=(5,0))
    assitant_frame.grid_columnconfigure((0,1,2,3), weight=1)
    assitant_frame.grid_rowconfigure((0,1,2,3), weight=1)

    # 14.3 Segmentation Content
    header_assitant = customtkinter.CTkButton(assitant_frame, text='AI assistant', state='disabled', fg_color='#3b3b3b', text_color_disabled='#dce4e2')
    header_assitant.grid(column=0, row=0, columnspan=4, sticky='new')

    # ======= 15. SUPPORTING FUNCTIONS =======
    support_function_control = customtkinter.CTkFrame(app)
    support_function_control.grid(column=8, row=3, columnspan=2, rowspan=2, pady=5)
    support_function_control.grid_rowconfigure((0, 1), weight=1)
    support_function_control.grid_columnconfigure(0, weight=1)

    support_function_header = customtkinter.CTkButton(support_function_control, text='support functions', state='disabled', fg_color='#3b3b3b', text_color_disabled='#dce4e2')
    support_function_header.grid(column=0, row=0, sticky='new', padx=10, pady=5)


    support_options_values = ["None", 'Denoise', 'Blurring', 'GrayscaleErode','OtsuThreshold', 'LiThreshold', 'MomentsThreshold']
    support_options_default = customtkinter.StringVar(value="None")
    support_options = customtkinter.CTkComboBox(support_function_control, values=support_options_values, variable=support_options_default, command=supporting_functions_callback)
    support_options.grid(column=0, row=1, padx=10, pady=15)

    # # ======= 16. DCM INFO =======
    for i, (k, v) in enumerate(dict_info.items()):
        info_dcm = customtkinter.CTkLabel(tab_1, text=str(k) + ': ' + str(v), fg_color="transparent", font=("",12))
        info_dcm.grid(column=0, row=i, sticky="w")
        
    for i, (k, v) in enumerate(dict_info.items()):
        info_dcm = customtkinter.CTkLabel(tab_2, text=str(k) + ': ' + str(v), fg_color="transparent", font=("",12))
        info_dcm.grid(column=0, row=i, sticky="w")
        
    for i, (k, v) in enumerate(dict_info.items()):
        info_dcm = customtkinter.CTkLabel(tab_3, text=str(k) + ': ' + str(v), fg_color="transparent", font=("",12))
        info_dcm.grid(column=0, row=i, sticky="w")
    
    
    # ======= 17. SlIDER PIXEL FILTERING =======
    # 17.1 Slider Pixel Filtering Frame
    range_slider_frame = customtkinter.CTkFrame(app, fg_color='#2b2b2b')
    range_slider_frame.grid(column=2, row=7, columnspan=2, rowspan=2, padx=5, sticky='nsew')
    range_slider_frame.grid_columnconfigure(0, weight=1)
    range_slider_frame.grid_rowconfigure((0, 1, 2), weight=1)
    
    # 17.2 Slider Pixel Filtering Content
    range_slider_header = customtkinter.CTkButton(range_slider_frame, text='HounsField Window', state='disabled', fg_color='#3b3b3b', text_color_disabled='#dce4e2')
    range_slider_header.grid(column=0, row=0, sticky='new', padx=5)
    
    range_slider = CTkRangeSlider(range_slider_frame, from_=np.min(img), to=np.max(img), border_color='#3b3b3b', command=update_range_slider)
    range_slider.grid(column=0, row=2, columnspan=2, sticky='new', padx=5)
    
    btn_left_increase = customtkinter.CTkButton(range_slider_frame, text="+", width=20, command=left_increase_hf)
    btn_left_increase.grid(column=0, row=1, sticky='nw', padx=(30,0))
    
    btn_left_decrease = customtkinter.CTkButton(range_slider_frame, text="-", width=20, command=left_decrease_hf)
    btn_left_decrease.grid(column=0, row=1, sticky='nw', padx=(5,0))
    
    btn_left_entry = customtkinter.CTkEntry(range_slider_frame, placeholder_text=range_slider.get()[0], width=50, state='normal')
    btn_left_entry.configure(state='disabled')
    btn_left_entry.grid(column=0, row=1, sticky='nw', padx=(60,0))
    
    btn_right_increase = customtkinter.CTkButton(range_slider_frame, text="+", width=20, command=right_increase_hf)
    btn_right_increase.grid(column=0, row=1, sticky='ne', padx=(0,5))
    
    btn_right_decrease = customtkinter.CTkButton(range_slider_frame, text="-", width=20, command=right_decrease_hf)
    btn_right_decrease.grid(column=0, row=1, sticky='ne', padx=(0,30))
    
    btn_right_entry = customtkinter.CTkEntry(range_slider_frame, placeholder_text=range_slider.get()[1], width=50, state='normal')
    btn_right_entry.configure('normal')
    btn_right_entry.grid(column=0, row=1, sticky='ne', padx=(0,60))
    
    

    

app.bind("<<UpdateApp>>", update_app)
app.mainloop()