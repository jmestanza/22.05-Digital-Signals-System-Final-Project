import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import math as mth


class ImageFrame:
    def __init__(self, frame_win, row_pos):
        self.width = 600
        self.height = 350
        self.imgFrame = tk.Canvas(frame_win, width=self.width, height=self.height, bg="grey")
        self.imgFrame.grid(row=row_pos, columnspan=3)

        self.imgFrame.bind("<ButtonPress-1>", self.start_coord)
        frame_win.focus_set()
        frame_win.bind("<Return>", self.plot_poly)

        self.imgOriginal = None
        self.img_original_aux = None
        self.imgAux = None
        self.image1 = None
        self.draw = None
        self.img_resized_w = 0
        self.img_resized_h = 0
        self.downsample = 0

        self.pointList = []  # Lista inicial, por lo menos va a haber 3 puntos
        self.pointShowList = []  # Conjunto de los puntos creados con circulos

    def start_coord(self, event):
        if self.imgOriginal:
            self.pointShowList.append(self.imgFrame.create_oval(event.x-2, event.y-2,
                                                                event.x+2, event.y+2, fill="black"))
            self.pointList.append(event.x)
            self.pointList.append(event.y)

    def plot_poly(self, event):
        if len(self.pointList) >= 6:
            self.imgFrame.create_polygon(self.pointList, fill="black")
            self.fix_coord()
            self.draw.polygon(self.pointList, fill='black')

        for i in range(0, len(self.pointShowList), 1):
            self.imgFrame.delete(self.pointShowList[i])

        self.pointList.clear()
        self.pointShowList.clear()

    def create_mask(self):
        self.image1.save('OutJobs/testmask.jpeg')

    def fix_coord(self):
        for i in range(0, len(self.pointList), 1):
            if i % 2 == 0:
                self.pointList[i] = mth.ceil((self.pointList[i] -
                                              ((self.width - self.img_resized_w)/2))*self.downsample)
            else:
                self.pointList[i] = mth.ceil((self.pointList[i] -
                                              ((self.height - self.img_resized_h)/2))*self.downsample)

    def save_img_original(self, img_file):
        self.img_original_aux = Image.open(img_file)
        self.imgOriginal = ImageTk.PhotoImage(self.img_original_aux)
        self.image1 = Image.new("RGB", (self.imgOriginal.width(), self.imgOriginal.height()), "white")
        self.draw = ImageDraw.Draw(self.image1)

    def show_img(self):
        if (self.imgOriginal.width() > self.width) or (self.imgOriginal.height() > self.height):
            a = mth.ceil(self.imgOriginal.width() / self.width)
            b = mth.ceil(self.imgOriginal.height() / self.height)
            if a > b:
                self.downsample = a
            else:
                self.downsample = b
        else:
            self.downsample = 1

        self.img_resized_w = mth.ceil(self.imgOriginal.width()/self.downsample)
        self.img_resized_h = mth.ceil(self.imgOriginal.height()/self.downsample)
        img_resized = self.img_original_aux.resize((self.img_resized_w, self.img_resized_h))
        self.imgAux = ImageTk.PhotoImage(img_resized)
        self.imgFrame.create_image(self.width/2, self.height/2, image=self.imgAux)
