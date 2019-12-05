import tkinter as tk
from PIL import Image, ImageTk
import math as mth


class ProgressFrame:
    def __init__(self, frame_win, row_pos):
        self.width = 600
        self.height = 350
        self.row_pos = row_pos
        self.inpaintFrame = tk.Canvas(frame_win, width=self.width, height=self.height, bg="grey")
        self.inpaintFrame.grid(row=row_pos, columnspan=3)

        self.bkgImage_aux = None
        self.bkgImage = None
        self.bkgLabel = None
        self.imgAux = None

        self.img_resized_w = 0
        self.img_resized_h = 0

    def update_image(self, img_address):
        self.bkgImage_aux = Image.open(img_address)
        self.bkgImage = ImageTk.PhotoImage(self.bkgImage_aux)

        #Adaptar coordenadas para saber el subsample
        if (self.bkgImage.width() > self.width) or (self.bkgImage.height() > self.height):
            a = mth.ceil(self.bkgImage.width() / self.width)
            b = mth.ceil(self.bkgImage.height() / self.height)
            if a > b:
                downsample = a
            else:
                downsample = b
        else:
            downsample = 1

        self.img_resized_w = mth.ceil(self.bkgImage.width()/downsample)
        self.img_resized_h = mth.ceil(self.bkgImage.height()/downsample)
        img_resized = self.bkgImage_aux.resize((self.img_resized_w, self.img_resized_h))
        self.imgAux = ImageTk.PhotoImage(img_resized)
        self.inpaintFrame.create_image(self.width/2, self.height/2, image=self.imgAux)
