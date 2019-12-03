import cv2
import imutils
from numpy import random
from PIL import Image
import time
from utils import *
import numpy as np

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
    iteraciones = 50
    #lower y upper son bounds para buscar el color negro con la funcion inRange
    lower = np.array([0, 0, 0])
    upper = np.array([15, 15, 15])
    # re-mapeamos a 0 y 255 la mascara. 255: zona a retocar, 0 a no retocar.
    shapeMask = cv2.inRange(mask, lower, upper)
    # conseguimos la escala de grises de la imagen
    #grey_scale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # matriz de confianza, 0 o 1, si no se retoca es 1
    c = shapeMask[:, :] == 0
    #I = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    I = img
    rows = len(I)
    cols = len(I[0])
    w = [[0]*cols]*rows

    for iteracion in range(iteraciones):
        # conseguimos la escala de grises de la imagen (intensidad)
        k = 10# esto es heuristico
        # imagen[i][j] = [0, 0, 255] # esta en BGR
        #lowerbound = {'x':4*(rows//10),'y':5*(cols//10)}
        #upperbound = {'x':6*(rows//10),'y':7*(cols//10)}
        lowerbound = {'x': 45 * (rows // 100), 'y': 30 * (cols // 100)}
        upperbound = {'x': 60 * (rows // 100), 'y': 50 * (cols // 100)}

        for x in range(lowerbound['x'], upperbound['x']):
            for y in range(lowerbound['y'], upperbound['y']):
                sumanum = 0
                sumaden = 0
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        w[i][j] = np.exp(-k*abs(I[x][y]-I[x+i][y+j]))
                        sumaden += w[i][j]
                        sumanum += w[i][j]*I[x+i][y+j]

                I[x][y] = sumanum/sumaden
                #I[x][y] = [0, 0, 255]
        if iteracion % 5 == 0:
            print("Iteracion ", iteracion)
            im = Image.fromarray(cv2.cvtColor(I, cv2.COLOR_BGR2RGB))
            im.save("output3/imagen" + str(iteracion) + ".jpeg")

start_time = time.time()
procesar(img, mask)
end_time = time.time()
print("se calculo en:", (end_time-start_time)/60, " minutos")





