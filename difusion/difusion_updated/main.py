import cv2
import imutils
from PIL import Image
import time
from utils import *
import matplotlib.pyplot as plt
from itertools import combinations

img = cv2.imread('output3/imagen.jpeg', 3)# matriz, cada el es un RGB
# mascara con area a remover. Zona negra (0,0,0) se remueve, Blanca se deja(255,255,255)
mask = cv2.imread("output3/mask.jpeg")

#lado de los cuadrados que utilizaremos para rellenar la imagen
square_size = 5
# guardamos en un arreglo las coordenadas que describen al cuadrado
square = genSquare(square_size)

# tamanio del cuadrado de busqueda para el parche que reemplaza la posicion a rellenear
search_square_size = 500

# cuantas veces buscamos al azar por un parche
search_times = 100


def getMinimumNeighbours(shapeMask, x, y):
    # me quedo con el que tiene mas puntos de confianza
    # x, y son puntos en el borde que siempre pertenecen a c
    adyacent_pos = [[x, y - 1], [x + 1, y], [x, y + 1], [x - 1, y]]
    puntos_confiables = 0
    max_uv_conf = 0, 0
    conf = 0
    for pos in adyacent_pos:
        u, v = pos
        ady_pos = [[u, v - 1], [u + 1, v], [u, v + 1], [u - 1, v]]
        for p in ady_pos:
            w, z = p
            if shapeMask[w][z] == 0:  # si es confiable
                conf += 1
        if conf > puntos_confiables:
            max_uv_conf = u, v  # se supone que con esto puntos_confiables solo puede tener 4 de valor max

    return max_uv_conf


def replaceInsideBorder(u, v, shapeMask, image):
    ady_pos = [[u, v - 1], [u + 1, v], [u, v + 1], [u - 1, v]]
    for p in ady_pos:
        w, z = p
        if shapeMask[z][w] == 0:  # si es el unico no confiable su valor es el gradiente
            #gx, gy = grey_scale_gradient
            image[z][w] = [0, 0, 0]
            # (gx[w][z] ** 2 + gy[w][z] ** 2) ** (1 / 2)
    return

def updateInsideBorder(u, v, imagen, k):

    cols = 3
    rows = 3
    rgb_els = 3
    sumanum = [0]*rgb_els
    sumaden = [0]*rgb_els

    w = [[[0] * cols] * rows ]* rgb_els
    for i in range(-1, 2):
        for j in range(-1, 2):
            for l in range(rgb_els):
                w[j][i][l] = np.exp(-k * abs(imagen[v][u][l] - imagen[v + i][u + j][l]))
                sumaden[l] += w[j][i][l]
                sumanum[l] += w[j][i][l] * imagen[v + j][u + i][l]

    for l in range(rgb_els):
        imagen[v][u][l] = sumanum[l] / sumaden[l]
    return

def procesar(imagen, mask, iteraciones):
    # re-mapeamos a 0 y 255 la mascara. 255: zona a retocar, 0 a no retocar.
    shapeMask = jpeg2MatrixMask(mask)
    # matriz de confianza, 0 o 1, si no se retoca es 1
    c = shapeMask[:, :] == 0

    for iteracion in range(iteraciones):

        best_benefit = 0
        best_benefit_point = None

        shapeMask = jpeg2MatrixMask(mask)

        # detectamos el borde de la mascara y conseguimos un arreglo con todos los contornos
        # cnts me da los contornos cerrados (los que se van achicando segun el algoritmo)
        cnts = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cnts = imutils.grab_contours(cnts)

        # conseguimos la escala de grises de la imagen (intensidad)
        grey_scale = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

        #grey_scale_gradient = getGradient(grey_scale)

        for contorno in range(len(cnts)):
            borde = cnts[contorno]
            for index,border_point in enumerate(cnts[contorno]):
                x, y = border_point[0]

                # el borde esta en la zona de confianza
                u, v = getMinimumNeighbours(shapeMask, x, y)

                #lo que esta dentro de la frontera es [0,0,0]
                replaceInsideBorder(u, v, shapeMask, imagen)
                updateInsideBorder(u, v, imagen, k=1)

                # updateo la confianza
                shapeMask[u][v] = 0

        if iteracion % 100 == 0:
            print("Iteracion ", iteracion)
            im = Image.fromarray(cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB))
            im.save("output3/imagen" + str(iteracion) + ".jpeg")


start_time = time.time()
iteraciones = 1000
procesar(img, mask,iteraciones)
end_time = time.time()
print("se calculo en:", (end_time-start_time)/60, " minutos")

