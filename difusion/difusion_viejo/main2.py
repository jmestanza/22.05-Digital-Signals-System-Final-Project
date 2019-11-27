import cv2
import imutils
from numpy import random
from PIL import Image
import time
import numpy as np
from utils import *
import matplotlib.pyplot as plt

img = cv2.imread('output3/imagen.jpeg', 3) #esto devuelve una matriz donde cada elemento es un RGB
# mascara con area a remover. la zona negra (0,0,0) se remueve, la blanca se deja como esta (255,255,255)
mask = cv2.imread("output3/mask.jpeg")


#lado de los cuadrados que utilizaremos para rellenar la imagen
square_size = 5

# guardamos en un arreglo las coordenadas que describen al cuadrado
square = genSquare(square_size)

# tamanio del cuadrado de busqueda para el parche que reemplaza la posicion a rellenear
search_square_size = 500

# cuantas veces buscamos al azar por un parche
search_times = 100


def procesar(imagen, mask):
    iteraciones = 1000
    #lower y upper son bounds para buscar el color negro con la funcion inRange
    lower = np.array([0, 0, 0])
    upper = np.array([15, 15, 15])
    # re-mapeamos a 0 y 255 la mascara. 255: zona a retocar, 0 a no retocar.
    shapeMask = cv2.inRange(mask, lower, upper)
    # conseguimos la escala de grises de la imagen
    grey_scale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # matriz de confianza, 0 o 1, si no se retoca es 1
    c = shapeMask[:, :] == 0

    I = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rows = len(I)
    cols = len(I[0])
    w = [[0]*cols]*rows
    k = 10
    for iteracion in range(iteraciones):
        # detectamos el borde de la mascara y conseguimos un arreglo con todos los contornos
        cnts = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cnts = imutils.grab_contours(cnts)
        # por cada contorno cerrado
        for contorno in range(len(cnts)):
            for border_point in cnts[contorno]:
                x, y = border_point[0]
                sumanum = 0
                sumaden = 0
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        w[i][j] = np.exp(-k * abs(I[x][y] - I[x + i][y + j]))
                        sumaden += w[i][j]
                        sumanum += w[i][j] * I[x + i][y + j]
                I[x][y] = sumanum / sumaden
        if iteracion % 50 == 0:
            print("Iteracion ", iteracion)
            im = Image.fromarray(cv2.cvtColor(I, cv2.COLOR_BGR2RGB))
            im.save("output3/imagen" + str(iteracion) + ".jpeg")


start_time = time.time()
procesar(img, mask)
end_time = time.time()
print("se calculo en:", (end_time-start_time)/60, " minutos")





