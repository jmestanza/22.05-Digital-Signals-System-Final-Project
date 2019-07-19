import tkinter as tk
from Globals import config
from PIL import ImageTk, Image


class ConfigureImage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, height=2, text="Imagen seleccionada", font=config.LARGE_FONT)
        label.pack(side=tk.TOP, fill=tk.BOTH)

        self.canvas = tk.Canvas(
            self,
            width=500,
            height=400
        )
        self.canvas.pack(expand=1, fill=tk.BOTH)

    def focus(self):
        print("focus")
        print(config.imageFilename)

        im = tk.PhotoImage(config.imageFilename)

        self.canvas.create_image(
            0, 0,
            image=im,
            anchor=tk.NW
        )
        self.canvas.update()

