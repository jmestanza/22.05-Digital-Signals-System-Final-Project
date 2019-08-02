from tkinter import *
from PIL import Image, ImageDraw
import math as mth

class Test:
    def __init__(self):
        self.xi, self.yi = 0, 0
        self.xf, self.yf = 0, 0

    def callback(self, eventP):
        print("clicked at", eventP.x, eventP.y)
        print("Evento: ", eventP.type)
        self.xi, self.yi = eventP.x, eventP.y

    def callback2(self, eventR):
        print("released at", eventR.x, eventR.y)
        print("Evento: ", eventR.type)
        self.xf, self.yf = eventR.x, eventR.y

        frame.create_oval(self.xi, self.yi, self.xf, self.yf, fill = "black") #Funciona OK
        #En vez de esto, hacer poligono con varios puntos
        image1 = Image.new("RGB", (frame.w_orig, frame.h_orig), "white")
        draw = ImageDraw.Draw(image1)
        self.xi = self.xi - frame.delta_X
        self.xf = self.xf - frame.delta_X
        self.yi = self.yi - frame.delta_Y
        self.yf = self.yf - frame.delta_Y
        print(self.xi, " ", self.xf, " ", self.yi, " ", self.yf)
        # El error que me tiraba ellipse era que faltaban los parentesis adicionales de las coordenadas
        draw.ellipse((self.xi*frame.downsampler, self.yi*frame.downsampler,
                      self.xf*frame.downsampler, self.yf*frame.downsampler), fill='black')
        image1.save('example.png') #Funciona OK

root = Tk()
root.config(width=200, height=200)
root.resizable(0, 0)
bkgImage = PhotoImage(file="bridge.png")

frame = Canvas(root, width=200, height=200)
test_class = Test()
frame.bind("<ButtonPress-1>", test_class.callback)
frame.bind("<ButtonRelease-1>", test_class.callback2)
frame.pack()

if (bkgImage.width()>200) or (bkgImage.height()>200):
    A = mth.ceil(bkgImage.width()/200)
    B = mth.ceil(bkgImage.height()/200)
    if A>B:
        downsampler = A
    else:
        downsampler = B
else:
    downsampler = 1

frame.w_orig = bkgImage.width()
frame.h_orig = bkgImage.height()
frame.downsampler = downsampler
bkgImage = bkgImage.subsample(downsampler,downsampler)
frame.delta_X = (200-bkgImage.width())/2
frame.delta_Y = (200-bkgImage.height())/2
frame.create_image((200/2), (200/2), image=bkgImage) #Funciona OK es transparente

root.mainloop()
