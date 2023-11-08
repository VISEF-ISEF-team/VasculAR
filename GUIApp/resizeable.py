import tkinter as tk
import json

class ResizableRectangle:
    def __init__(self, canvas, x, y, width, height, border_width=1):
        self.canvas = canvas
        self.rect = canvas.create_rectangle(x, y, x + width, y + height, outline='black', width=border_width)
        self.start_x, self.start_y = x, y
        self.width, self.height = width, height
        self.drag_data = {'x': 0, 'y': 0, 'item': None}
        
        self.canvas.tag_bind(self.rect, '<ButtonPress-1>', self.on_press)
        self.canvas.tag_bind(self.rect, '<B1-Motion>', self.on_drag)
        self.canvas.tag_bind(self.rect, '<ButtonRelease-1>', self.on_release)

    def on_press(self, event):
        self.drag_data['item'] = self.rect
        self.drag_data['x'] = event.x
        self.drag_data['y'] = event.y

    def on_drag(self, event):
        delta_x = event.x - self.drag_data['x']
        delta_y = event.y - self.drag_data['y']
        self.canvas.move(self.drag_data['item'], delta_x, delta_y)
        self.drag_data['x'] = event.x
        self.drag_data['y'] = event.y

    def on_release(self, event):
        self.drag_data['item'] = None

def save_drag_data(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file)

def load_drag_data(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {'x': 0, 'y': 0, 'item': None}
    return data

def main():
    data_file = 'drag_data.json'

    try:
        drag_data = load_drag_data(data_file)
    except FileNotFoundError:
        drag_data = {'x': 0, 'y': 0, 'item': None}

    root = tk.Tk()
    root.title("Resizable Rectangle")
    canvas = tk.Canvas(root, width=800, height=800)
    canvas.pack()

    x, y, width, height = 50, 50, 600, 600
    border_width = 3
    resizable_rect = ResizableRectangle(canvas, x, y, width, height, border_width)
    
    root.protocol("WM_DELETE_WINDOW", lambda: save_drag_data(resizable_rect.drag_data, data_file))
    root.mainloop()

if __name__ == "__main__":
    main()
