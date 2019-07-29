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
        image1 = Image.new("RGB", (frame.wdata, frame.hdata), "white")
        draw = ImageDraw.Draw(image1)
        #El error que me tiraba ellipse era que faltaban los parentesis adicionales de las coordenadas
        draw.ellipse((self.xi, self.yi, self.xf, self.yf), fill='black')
        image1.save('example.png') #Funciona OK

root = Tk()

bkgImage = PhotoImage(file="bridge.png")

frame = Canvas(root, width=100, height=100)
test_class = Test()
frame.bind("<ButtonPress-1>", test_class.callback)
frame.bind("<ButtonRelease-1>", test_class.callback2)
frame.pack()

if (bkgImage.width()>100) or (bkgImage.height()>100):
    A = mth.ceil(bkgImage.width()/100)
    B = mth.ceil(bkgImage.height()/100)
    if A>B:
        downsampler = A
    else:
        downsampler = B
else:
    downsampler = 1

bkgImage = bkgImage.subsample(downsampler,downsampler)
frame.create_image((100/2), (100/2), image=bkgImage) #Funciona OK es transparente
frame.wdata = bkgImage.width()
frame.hdata = bkgImage.height()

root.mainloop()
