from tkinter import *
import customtkinter
from PIL import Image, ImageTk
import tkinter

class draw_canvas:
    def __init__(self, canvas, radio_var, line_distance, coordinate_label, res_list, pixel_spacing):
        self.canvas = canvas
        self.radio_var = radio_var
        self.rec_list = res_list
        self.line_distance = line_distance
        self.coordinate_label = coordinate_label
        self.start_x = 0
        self.start_y = 0
        self.pixel_spacing = pixel_spacing
    
    # define a function to handle mouse press event
    def on_press(self, event):
        # store the mouse position as the start point of the rectangle
        self.start_x = event.x
        self.start_y = event.y
        
    # define a function to handle mouse release event
    def on_release(self, event):
        # get the mouse position as the end point of the rectangle
        end_x = event.x
        end_y = event.y
        if self.radio_var.get() != 0:
            # draw a rectangle on the canvas using the start and end points
            if self.radio_var.get() == 1:
                rect_id = self.canvas.create_rectangle(self.start_x, self.start_y, end_x, end_y, outline="red", width=3)
                
            elif self.radio_var.get() == 2: 
                rect_id = self.canvas.create_line(self.start_x, self.start_y, end_x, end_y, fill="red", width=3)
                self.show_distance(self.start_x, self.start_y, end_x, end_y)

            # append the rectangle id and coordinates to the list
            self.rec_list.append((rect_id, self.start_x, self.start_y, end_x, end_y))

    # define a function to redo the last rectangle
    def redo(self):
        # check if the list is not empty
        if self.rec_list:
            # pop the last item from the list
            rect_id, _, _, _, _ = self.rec_list.pop()

            # delete the rectangle from the canvas
            self.canvas.delete(rect_id)

        
    # define a function to clear all rectangles
    def clear(self):
        # loop through the list and delete each rectangle from the canvas
        for rect_id, _, _, _, _ in self.rec_list:
            self.canvas.delete(rect_id)

        # clear the list
        self.rec_list.clear()
        self.line_distance.configure(text="")
        

    # define a function to update the label with the mouse coordinates
    def show_coords(self, event):
        # get the mouse position relative to the canvas
        x = event.x
        y = event.y

        # update the label text with the coordinates
        self.coordinate_label.configure(text=f"Coordinates: x={x}, y={y}")
        
    def radiobutton_event(self):
        print("radiobutton toggled, current value:", self.radio_var.get())
        
    def show_distance(self, start_x, start_y, end_x, end_y):
        euclidean_distance = ((end_x - start_x)**2 + (end_y - start_y)**2)**(1/2)
        mm_distance = euclidean_distance * self.pixel_spacing
        self.line_distance.configure(text=f'Distance: {round(mm_distance,3)} mm')