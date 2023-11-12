from tkinter import *
from PIL import Image, ImageTk

root = Tk()

images = []  # to hold the newly created image

def create_image(x, y, image, **kwargs):
    if 'alpha' in kwargs:
        alpha = int(kwargs.pop('alpha') * 255)
        image = image.convert('RGBA')
        image.putalpha(alpha)
        images.append(ImageTk.PhotoImage(image))
        canvas.create_image(x, y, image=images[-1], anchor='nw')

# Example usage
height = 1000
image_display_1 = Image.open("temp.jpg").resize((height, height))
image_display_2 = Image.open("D:/Documents/GitHub/VascuIAR/imgs/Bo tròn bộ dữ liệu.png").resize((height, height))

image_display_3 = Image.open("D:\Documents\GitHub\VascuIAR\imgs\Dựng 3D khung xương ngực.png").resize((height, height))
image_display_4 = Image.open("D:/Documents/GitHub/VascuIAR/imgs/Bo tròn dữ liệu.png").resize((height, height))

canvas = Canvas(width=height, height=height)
canvas.pack()

create_image(10, 10, image_display_1, alpha=1)
create_image(10, 10, image_display_2, alpha=0.5)
create_image(10, 10, image_display_3, alpha=1)
create_image(10, 10, image_display_4, alpha=0.5)

root.mainloop()
