import tkinter as tk
from PIL import Image, ImageTk
import math as mth


class ImageFrame:
    def __init__(self, frame_win, row_pos):
        self.width = 600
        self.height = 300
        self.imgFrame = tk.Canvas(frame_win, width=self.width, height=self.height, bg="grey")
        self.imgFrame.grid(row=row_pos, columnspan=3)

        self.imgOriginal = None
        self.img_original_aux = None
        self.img_aux = None

    def save_img_original(self, img_file):
        self.img_original_aux = Image.open(img_file)
        self.imgOriginal = ImageTk.PhotoImage(self.img_original_aux)

    def show_img(self):
        if (self.imgOriginal.width() > self.width) or (self.imgOriginal.height() > self.height):
            a = mth.ceil(self.imgOriginal.width() / self.width)
            b = mth.ceil(self.imgOriginal.height() / self.height)
            if a > b:
                downsampler = a
            else:
                downsampler = b
        else:
            downsampler = 1

        img_original_resized = self.img_original_aux.resize((mth.ceil(self.imgOriginal.width()/downsampler),
                                                            mth.ceil(self.imgOriginal.height()/downsampler)))
        self.img_aux = ImageTk.PhotoImage(img_original_resized)
        self.imgFrame.create_image(self.width/2, self.height/2, image=self.img_aux)
        #Cuando haya que convertir las coordenadas tengo que hacer regla de 3