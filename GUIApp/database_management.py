import customtkinter
import customtkinter as ctk
import pyrebase
from PIL import Image, ImageTk
import os
import sys
from io import BytesIO
from datetime import datetime
import requests
import calendar

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


class CTkCalendar(ctk.CTkFrame):
    """
    Calendar widget to display certain month, each day is rendered as Label.

    If you do not define today_fg_color and today_text_color it will be rendered as other days
    """

    def __init__(self, master,
                 today_fg_color=None,
                 today_text_color=None,
                 width=250,
                 height=250,
                 fg_color=None,
                 corner_radius=8,
                 border_width=None,
                 border_color=None,
                 bg_color="transparent",
                 background_corner_colors=None,
                 title_bar_fg_color=None,
                 title_bar_border_width=None,
                 title_bar_border_color=None,
                 title_bar_corner_radius=None,
                 title_bar_text_color=None,
                 title_bar_button_fg_color=None,
                 title_bar_button_hover_color=None,
                 title_bar_button_text_color=None,
                 title_bar_button_border_width=None,
                 title_bar_button_border_color=None,
                 calendar_fg_color=None,
                 calendar_border_width=None,
                 calendar_border_color=None,
                 calendar_corner_radius=None,
                 calendar_text_color=None,
                 calendar_text_fg_color=None,
                 calendar_label_pad=1):

        super().__init__(master=master,
                         width=width,
                         height=height,
                         fg_color=fg_color,
                         corner_radius=corner_radius,
                         border_width=border_width,
                         border_color=border_color,
                         bg_color=bg_color,
                         background_corner_colors=background_corner_colors)

        # data
        self.today_text_color = today_text_color
        self.today_fg_color = today_fg_color
        self.today = self.current_date()
        self.day, self.month, self.year = self.today[:]
        self.labels_by_date = dict()
        self.month_label = ctk.StringVar(value=calendar.month_name[self.month])
        self.year_label = ctk.IntVar(value=self.year)

        # data for title bar
        self.title_bar_fg_color = title_bar_fg_color
        self.title_bar_border_width = title_bar_border_width
        self.title_bar_border_color = title_bar_border_color
        self.title_bar_text_color = title_bar_text_color
        self.title_bar_button_fg_color = title_bar_button_fg_color
        self.title_bar_button_hover_color = title_bar_button_hover_color
        self.title_bar_button_text_color = title_bar_button_text_color
        self.title_bar_button_border_width = title_bar_button_border_width
        self.title_bar_button_border_color = title_bar_button_border_color
        self.title_bar_corner_radius = title_bar_corner_radius

        # data for calendar frame
        self.calendar_fg_color = calendar_fg_color
        self.calendar_border_width = calendar_border_width
        self.calendar_border_color = calendar_border_color
        self.calendar_corner_radius = calendar_corner_radius
        self.calendar_text_fg_color = calendar_text_fg_color
        self.calendar_text_color = calendar_text_color
        self.calendar_label_pad = calendar_label_pad
        self.btn_color = '#2b2b2b'
        self.hover_color = '#242424'
        self.selected_date = ''

        # creating header and calendar frames
        self.content_frame = ctk.CTkFrame(
            self, fg_color="transparent", width=width, height=height)
        self.content_frame.pack(expand=True, fill="both",
                                padx=corner_radius/3, pady=corner_radius/3)
        self.setup_header_frame()
        self.create_calendar_frame()

    def setup_button_normal(self, frame, day, row, column):
        def on_day_click():
            selected_date = (day, self.month, self.year)
            self.close_window(selected_date)

        if self.today_fg_color is not None and self.date_is_today((day, self.month, self.year)):
            button = ctk.CTkButton(frame, text=str(day), corner_radius=5,
                                   fg_color=self.btn_color, font=ctk.CTkFont(
                                       "Arial", 11),
                                   hover_color=self.hover_color, command=on_day_click)
        else:
            button = ctk.CTkButton(frame, text=str(day), corner_radius=5,
                                   fg_color=self.btn_color, font=ctk.CTkFont(
                                       "Arial", 11),
                                   hover_color=self.hover_color, command=on_day_click)

        button.grid(row=row, column=column, sticky="nsew",
                    padx=self.calendar_label_pad, pady=self.calendar_label_pad)

    # setting up the header frame
    def setup_header_frame(self):
        header_frame = ctk.CTkFrame(self.content_frame, fg_color=self.title_bar_fg_color,
                                    corner_radius=self.title_bar_corner_radius,
                                    border_color=self.title_bar_border_color, border_width=self.title_bar_border_width)

        ctk.CTkButton(header_frame, text="<", width=25, fg_color=self.title_bar_button_fg_color,
                      hover_color=self.title_bar_button_hover_color, border_color=self.title_bar_button_border_color,
                      border_width=self.title_bar_button_border_width, font=ctk.CTkFont(
                          "Arial", 11, "bold"),
                      command=lambda: self.change_month(-1)).pack(side="left", padx=10)
        ctk.CTkLabel(header_frame, textvariable=self.month_label, font=ctk.CTkFont("Arial", 16, "bold"),
                     fg_color="transparent").pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(header_frame, textvariable=self.year_label, font=ctk.CTkFont("Arial", 16, "bold"),
                     fg_color="transparent").pack(side="left", fill="x")
        ctk.CTkButton(header_frame, text=">", width=25, fg_color=self.title_bar_button_fg_color,
                      hover_color=self.title_bar_button_hover_color, border_color=self.title_bar_button_border_color,
                      border_width=self.title_bar_button_border_width, font=ctk.CTkFont(
                          "Arial", 11, "bold"),
                      command=lambda: self.change_month(1)).pack(side="right", padx=10)

        header_frame.place(relx=0.5, rely=0.02, anchor="n",
                           relheight=0.18, relwidth=0.95)

    def create_calendar_frame(self):
        # "updating" frames
        calendar_frame = ctk.CTkFrame(self.content_frame, fg_color=self.calendar_fg_color,
                                      corner_radius=self.calendar_corner_radius,
                                      border_width=self.calendar_border_width, border_color=self.calendar_border_color)
        current_month = calendar.monthcalendar(self.year, self.month)

        # grid
        calendar_frame.columnconfigure(
            (0, 1, 2, 3, 4, 5, 6), weight=1, uniform="b")
        rows = tuple([i for i in range(len(current_month))])
        calendar_frame.rowconfigure(rows, weight=1, uniform="b")

        # labels for days
        for row in range(len(current_month)):
            for column in range(7):
                if current_month[row][column] != 0:
                    self.setup_button_normal(
                        calendar_frame, current_month[row][column], row, column)

        calendar_frame.place(relx=0.5, rely=0.97, anchor="s",
                             relheight=0.75, relwidth=0.95)

    def change_month(self, amount):
        self.month += amount
        if self.month < 1:
            self.year -= 1
            self.month = 12
            self.day = 1
        elif self.month > 12:
            self.year += 1
            self.month = 1
            self.day = 1

        self.month_label.set(calendar.month_name[self.month])
        self.year_label.set(self.year)

        self.create_calendar_frame()

    def current_date(self) -> tuple[int, int, int]:
        date = str(datetime.now()).split()
        year, month, day = date[0].split("-")
        return int(day), int(month), int(year)

    def date_is_today(self, date: tuple) -> bool:
        if date[2] == self.today[2] and date[1] == self.today[1] and date[0] == self.today[0]:
            return True
        return False

    # creating normal date labels for normal calendar
    def setup_label_normal(self, frame, day, row, column):
        if self.today_fg_color is not None and self.date_is_today((day, self.month, self.year)):
            ctk.CTkLabel(frame, text=str(day), corner_radius=5,
                         fg_color=self.today_fg_color, font=ctk.CTkFont(
                             "Arial", 11),
                         text_color=self.today_text_color).grid(row=row, column=column, sticky="nsew",
                                                                padx=self.calendar_label_pad,
                                                                pady=self.calendar_label_pad)
        else:
            ctk.CTkLabel(frame, text=str(day), corner_radius=5,
                         fg_color=self.calendar_text_fg_color, font=ctk.CTkFont(
                             "Arial", 11),
                         text_color=self.calendar_text_color).grid(row=row, column=column, sticky="nsew",
                                                                   padx=self.calendar_label_pad,
                                                                   pady=self.calendar_label_pad)

        def on_day_click():
            selected_date = (day, self.month, self.year)
            self.close_window(selected_date)

        if self.today_fg_color is not None and self.date_is_today((day, self.month, self.year)):
            label = ctk.CTkLabel(frame, text=str(day), corner_radius=5,
                                 fg_color=self.today_fg_color, font=ctk.CTkFont(
                                     "Arial", 11),
                                 text_color=self.today_text_color)
        else:
            label = ctk.CTkLabel(frame, text=str(day), corner_radius=5,
                                 fg_color=self.calendar_text_fg_color, font=ctk.CTkFont(
                                     "Arial", 11),
                                 text_color=self.calendar_text_color)

        label.grid(row=row, column=column, sticky="nsew",
                   padx=self.calendar_label_pad, pady=self.calendar_label_pad)

        # Bind the click event to the label
        label.bind("<Button-1>", lambda event: on_day_click())

    def close_window(self, selected_date):
        self.selected_date = selected_date
        self.master.destroy()


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
        self.frame.columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.frame.rowconfigure(2, weight=1)

        self.label = customtkinter.CTkLabel(
            master=self.frame, text="Cloud Database Management", font=(self.font, 25, "bold"))
        self.label.grid(row=0, column=0, padx=20, pady=10, sticky='w')

        calendar_icon = customtkinter.CTkImage(
            dark_image=Image.open("imgs/calendar.png"), size=(20, 20))
        self.calender_entry = customtkinter.CTkButton(
            master=self.frame, text='', image=calendar_icon, width=30, height=30, command=self.open_calender)
        self.calender_entry.grid(row=0, column=2, padx=(20, 0), sticky='w')

        self.entry = customtkinter.CTkEntry(
            master=self.frame, placeholder_text="search", width=200)
        self.entry.grid(row=0, column=2, padx=(0, 20), pady=10, sticky="e")
        self.entry.bind("<KeyRelease>", lambda e: self.search_data(
            name_patient=self.entry.get()))

        self.about_button = customtkinter.CTkButton(
            master=self.frame, text="?", hover=False, width=30, command=self.open_about_window)
        self.about_button.grid(row=0, column=4, padx=10, pady=10, sticky="e")

        self.scrollable_frame = customtkinter.CTkScrollableFrame(self.frame)
        self.scrollable_frame.grid(
            row=2, column=0, columnspan=3, padx=10, pady=(0, 10), sticky="nsew")

        self.info_frame = customtkinter.CTkScrollableFrame(self.frame)
        self.info_frame.grid(row=2, column=3, columnspan=2,
                             padx=10, pady=(0, 10), sticky="nsew")

        self.item_frame = {}
        self.read_cloud_database()

    def add_item(self, key, value):
        self.item_frame[key] = customtkinter.CTkFrame(self.scrollable_frame)
        self.item_frame[key].pack(expand=True, fill="x", padx=5, pady=5)
        self.item_frame[key].columnconfigure((0, 1, 2, 3, 4), weight=1)

        # case
        item_name = customtkinter.CTkButton(self.item_frame[key], fg_color="transparent",
                                            text_color=customtkinter.ThemeManager.theme[
                                                "CTkLabel"]["text_color"],
                                            height=50, anchor="w", font=(self.font, 15, "bold"), width=250,
                                            text=f'Case {key[5:]}', hover=False, command=lambda: self.info_window(key, value))
        item_name.grid(row=0, column=0, sticky="ew", pady=5, padx=5)

        # patient name
        patient_name = customtkinter.CTkLabel(
            self.item_frame[key], width=250, justify="left", text=value["dict_info"]["Patient's name"], anchor="w", wraplength=250)
        patient_name.grid(row=0, column=1, padx=5)

        # Modality
        modality_name = customtkinter.CTkLabel(
            self.item_frame[key], width=250, justify="left", text=value["dict_info"]["Modality"], anchor="w", wraplength=250)
        modality_name.grid(row=0, column=2, padx=5)

        # Acquisition date
        date = datetime.strptime(
            value["dict_info"]["Acquisition Date"], "%Y%m%d").strftime("%d/%m/%Y")
        date_name = customtkinter.CTkLabel(
            self.item_frame[key], width=250, justify="left", text=date, anchor="w", wraplength=250)
        date_name.grid(row=0, column=3, padx=5)

        # Body part
        body_part = customtkinter.CTkLabel(
            self.item_frame[key], width=250, justify="left", text=value["dict_info"]["Body Part Examined"], anchor="w", wraplength=250)
        body_part.grid(row=0, column=4, padx=5)

    def info_window(self, key, value):

        for widget in self.info_frame.winfo_children():
            widget.destroy()

        for (analysis_key, analysis_value), (canvas, image_url) in zip(value['analysis_data'].items(), value['folder_imgs'][key].items()):

            if analysis_key == canvas:
                # display image
                response = requests.get(image_url)
                img_data = BytesIO(response.content)
                my_image = customtkinter.CTkImage(
                    dark_image=Image.open(img_data), size=(350, 350))

                image_label = customtkinter.CTkLabel(
                    self.info_frame, image=my_image, text="")
                image_label.pack()
                image_label.image = my_image

                # display description
                key_label = customtkinter.CTkLabel(self.info_frame, text=list(
                    analysis_value.keys())[0], wraplength=300, font=(self.font, 15, "bold"))
                key_label.pack(padx=10, pady=(10, 5))

                des_label = customtkinter.CTkLabel(self.info_frame, text=list(
                    analysis_value.values())[0], wraplength=300)
                des_label.pack(padx=10)

    def search_data(self, name_patient):
        for key, value in self.data_snapshot.items():
            if name_patient in value["dict_info"]["Patient's name"]:
                self.item_frame[key].pack(
                    expand=True, fill="x", padx=5, pady=5)
            else:
                self.item_frame[key].pack_forget()
        self.scrollable_frame._parent_canvas.yview_moveto(0.0)

    def open_about_window(self):
        print("open about window")

    def read_cloud_database(self):
        self.data_snapshot = db.get().val()
        for key, value in self.data_snapshot.items():
            self.add_item(key, value)

    def open_calender(self):
        toplevel = customtkinter.CTkToplevel(self)
        toplevel.title("Calendar")
        toplevel.transient(self)
        toplevel.resizable(False, False)

        calendar_widget = CTkCalendar(toplevel)
        calendar_widget.pack(side="left")
        toplevel.wait_window()
        self.filter_date(calendar_widget.selected_date)

    def filter_date(self, date):
        for key, value in self.data_snapshot.items():
            if str(date[0]) == value["dict_info"]["Acquisition Date"][6:8] and str(date[1]) == value["dict_info"]["Acquisition Date"][4:6]:
                self.item_frame[key].pack(
                    expand=True, fill="x", padx=5, pady=5)
            else:
                self.item_frame[key].pack_forget()
        self.scrollable_frame._parent_canvas.yview_moveto(0.0)
