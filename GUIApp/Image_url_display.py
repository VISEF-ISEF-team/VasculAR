# To display the image in Tkinter, you can use a library like PIL
from PIL import Image, ImageTk
import requests
from io import BytesIO
import tkinter as tk

image_url = "https://firebasestorage.googleapis.com/v0/b/vascular-68223.appspot.com/o/case_013%2Fcanvas_0?alt=media"

# Fetch the image from the URL
response = requests.get(image_url)
img_data = BytesIO(response.content)
image = Image.open(img_data)

# Display the image in a Tkinter window
root = tk.Tk()
tk_image = ImageTk.PhotoImage(image)
label = tk.Label(root, image=tk_image)
label.pack()
root.mainloop()