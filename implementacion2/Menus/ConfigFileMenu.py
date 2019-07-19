import tkinter as tk
from PIL import ImageTk, Image
from tkinter import filedialog
from Globals import config
import ntpath


class ConfigureMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        label = tk.Label(self, height=2, text="Seleccionar imagen", font=config.LARGE_FONT)
        label.pack(side=tk.TOP, fill=tk.BOTH)

        self.buttonSelectImage = tk.Button(
            self,
            height=2,
            width=44,
            text="Seleccionar imagen",
            background="dodger blue",
            font=config.SMALL_FONT,
            command=self.searchFile
        )
        self.buttonSelectImage.pack(
            side=tk.TOP,
            fill=tk.BOTH
        )

        self.buttonContinuar = tk.Button(
            self,
            height=2,
            width=44,
            text="Continuar",
            background="green",
            font=config.SMALL_FONT,
            command=self.continuar
        )
        self.buttonContinuar.pack(
            side=tk.TOP,
            fill=tk.BOTH
        )
        self.filename = None

    def searchFile(self):
        tk.Tk().withdraw()
        self.filename = filedialog.askopenfilename()
        config.imageFilename = self.filename

        self.buttonSelectImage.configure(
            text="Seleccionar imagen [" + ntpath.basename(self.filename) + "]"
        )

    def continuar(self):
        from Menus.ConfigureImage import ConfigureImage

        self.controller.showFrame(ConfigureImage)

