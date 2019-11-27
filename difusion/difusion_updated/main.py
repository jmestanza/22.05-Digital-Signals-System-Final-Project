import cv2
import imutils
from PIL import Image
import time
import numpy as np
import itertools
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

def belongsToNeighbourhood(pixel,i,j):
    ans = False
    neighbours_index = [element for element in itertools.product([1,-1],[1,-1])]
    x, y = pixel
    pos = [x, y]
    possible_nh = [i,j]
    for ng_index in neighbours_index:
        if np.array_equal(np.add(pos,ng_index),possible_nh):
            ans = True
    return ans

def gfactor(grad_xy, K=10000):
    return 1/(1 + (np.linalg.norm(grad_xy))**2/K)

def getMatrixA(pixel, tau, grad):
    A = np.zeros((9, 9))
    x, y = pixel
    gx, gy = grad
    for i in range(9):
        for j in range(9):
            if belongsToNeighbourhood(pixel, i, j): #estoy en la vecindad
                A[i][j] = -tau*gfactor(grad[y][x])
            elif j == i: #estoy en el centro
                suma = 1
                neighbours_index = [element for element in itertools.product([1, -1], [1, -1])]
                for ng_index in neighbours_index:
                    di, dj = ng_index
                    grad_xy = [gx[x+dj], gy[y+di]]
                    suma += tau*gfactor(grad_xy)
                A[i][i] = suma
            else:
                A[i][j] = 0
    return A

def procesar(imagen, mask, iteraciones):
    # re-mapeamos a 0 y 255 la mascara. 255: zona a retocar, 0 a no retocar.
    shapeMask = jpeg2MatrixMask(mask)
    # matriz de confianza, 0 o 1, si no se retoca es 1
    c = shapeMask[:, :] == 0
    aux_img = imagen.copy()
    for iteracion in range(iteraciones):

        # shapeMask = jpeg2MatrixMask(mask)
        # detectamos el borde de la mascara y conseguimos un arreglo con todos los contornos
        # cnts me da los contornos cerrados (los que se van achicando segun el algoritmo)
        cnts = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cnts = imutils.grab_contours(cnts)

        tau = 10
        for contorno in range(len(cnts)):
            memory = {}
            for index, border_point in enumerate(cnts[contorno]):
                grey_scale = cv2.cvtColor(aux_img, cv2.COLOR_BGR2GRAY)
                grey_scale_gradient = getGradient(grey_scale)
                x, y = border_point[0]
                u, v = getMinimumNeighbours(shapeMask, x, y)
                pixel = [u, v]
                I = [[], [], []]
                I_0 = imagen[u][v]
                A = np.asarray(getMatrixA(pixel, tau, grey_scale_gradient))
                for k in range(3): #R,G,B la siguiente linea es I[k] (t+1)
                    if not I[k]:
                        b = [I_0[k]]*9 # si no hay ninguno empiezo con I_0
                    else:
                        b = I[k][-1] #agarro el ultimo

                    I[k] = np.linalg.solve(A, b)

                for i in range(9):
                    aux_img[u][v+i] = [I[0][i], I[1][i], I[2][i]]
                # # updateo la confianza
                    shapeMask[u][v+i] = 0
                    pos = u, v+i
                    drawRect(imagen, pos, 1, [0, 0, 255])

        #if iteracion % 100 == 0:
        print("Iteracion ", iteracion)
        im = Image.fromarray(cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB))
        im.save("output3/imagen" + str(iteracion) + ".jpeg")


start_time = time.time()
iteraciones = 10
procesar(img, mask,iteraciones)
end_time = time.time()
print("se calculo en:", (end_time-start_time)/60, " minutos")

