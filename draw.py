import tkinter as tk
from PIL import Image, ImageDraw
import numpy as np

CANVAS_SIZE = 280
IMG_SIZE = 28
SCALE = CANVAS_SIZE // IMG_SIZE

class DrawApp:
    def __init__(self, root):
        self.root = root
        self.canceled = False

        self.canvas = tk.Canvas(root, width=CANVAS_SIZE, height=CANVAS_SIZE, bg='white')
        self.canvas.pack()

        self.image = Image.new("L", (IMG_SIZE, IMG_SIZE), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<Button-1>", self.paint)

        btn = tk.Button(root, text="Done", command=self.finish)
        root.bind("<space>", lambda _: self.finish())
        root.bind("<q>", lambda _: self.reset())
        root.bind("<Escape>", lambda _: self.cancel())
        btn.pack(pady=10)

    def paint(self, event):
        x, y = event.x, event.y
        r = SCALE // 2
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill='black', outline='black')

        img_x, img_y = x // SCALE, y // SCALE
        if 0 <= img_x < IMG_SIZE and 0 <= img_y < IMG_SIZE:
            self.draw.rectangle([img_x, img_y, img_x, img_y], fill=0)

    def reset(self):
        self.canvas.delete("all")

    def cancel(self):
        self.canceled = True
        self.root.quit()

    def finish(self):
        self.root.quit()

def get_drawn_image(label=None):
    root = tk.Tk()
    root.title(label if label else "Draw 28x28 Image")
    app = DrawApp(root)
    root.mainloop()
    root.destroy()

    if app.canceled:
        return None

    arr = np.array(app.image).astype('float32') / 255
    arr = arr.flatten()
    arr = 1 - arr
    arr = np.expand_dims(arr, 0)
    return arr

