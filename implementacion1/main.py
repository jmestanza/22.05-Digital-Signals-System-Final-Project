import cv2
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import imutils
from numpy import random
import scipy.misc
from PIL import Image
from numpy import sqrt
import time
from utils import genSquare
from utils import getMaxGrad
from utils import getBorderNormal
from utils import getTotalSum
from utils import copyPattern

# imagen a procesar
img = cv2.imread('output3/imagen.jpeg', 3)
# mascara con area a remover.
# la zona negra (0,0,0) es la que se remueve, la blanca se deja como esta (255,255,255)
mask = cv2.imread("output3/mask.jpeg")
# imagen pasada a escala de grises se guarda en esta variable
grey_scale = np.zeros(img.shape, dtype=np.uint8) #uint8

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

    lower = np.array([0, 0, 0])
    upper = np.array([15, 15, 15])
    # re-mapeamos a 0-1 la mascara. 1 es para la zona retocada, 0 para la que no
    shapeMask = cv2.inRange(mask, lower, upper)

    c = shapeMask[:, :] == 0 # maxima confianza en la zona que no se retoca

    for iteracion in range(iteraciones):
        # primero detectamos el borde de la mascara
        # conseguimos un arreglo con todos los contornos

        cnts = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cnts = imutils.grab_contours(cnts)
        # cada contorno cerrado forma un arreglo

        # luego tenemos que calcular la funcion de costos
        best_benefit = 0
        best_benefit_point = None

        # conseguimos la escala de grises
        grey_scale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # conseguimos el gradiente en x e y de la escala de grises, la funcion sobel no solo hace gradiente
        # sino que suaviza
        sobel_x = cv2.Sobel(grey_scale, cv2.CV_64F, 1, 0, ksize=5)
        sobel_y = cv2.Sobel(grey_scale, cv2.CV_64F, 0, 1, ksize=5)
        sobel_x, sobel_y = -sobel_y,sobel_x

        # por cada contorno cerrado
        for contorno in range(len(cnts)):

            ## necesitamos generar las normales de cada punto del contorno
            border_normal = getBorderNormal(cnts, contorno)

            index = 0

            for border_point in cnts[contorno]:
                x, y = border_point[0]

                # consigo la confianza del punto del contorno actual
                confidence = 0

                for dx, dy in square:
                    if shapeMask[y + dy, x + dx] == 0: # si fuera de la region a retocar
                        confidence += c[y + dy, x + dx]

                confidence /= len(square)

                # consigo la componente normal del gradiente
                nx, ny = border_normal[index]
                index = index + 1

                # consigo el gradiente mas grande de la region

                max_grad, max_grad_value = getMaxGrad(square, shapeMask, x, y, sobel_x, sobel_y)

                # producto escalar del gradiente con la normal acorde a la formula

                d = max_grad_value[0] * nx + max_grad_value[1] * ny

                # el beneficio es la confianza por el factor d

                benefit = abs(d * confidence)

                # buscamos maximizar el beneficio
                if benefit > best_benefit:
                    best_benefit = benefit
                    best_benefit_point = x, y

        if not best_benefit_point:
            print("No hay mas borde. Fin")
            break

        # ahora vamos a calcular el parche que minimize la distancia

        px, py = best_benefit_point

        best_patch = px, py # default
        patch_distance = np.Infinity

        for i in range(search_times):
            x = random.randint(px - search_square_size//2, px + search_square_size//2)
            y = random.randint(py - search_square_size//2, py + search_square_size//2)
#            x = int(random.normal(px, search_square_size//2**5,1))
#            y = int(random.normal(py, search_square_size//2**5,1))

            if shapeMask[y, x] == 255:
                continue # no es de interes ya que esta en la region blanca

            total_sum, last_patch_distance = getTotalSum(imagen, square_size, x, y, px, py)

            if total_sum < patch_distance:
                patch_distance = last_patch_distance
                best_patch = x, y

        bx, by = best_patch # best_patch_x, best_patch_y

        copyPattern(imagen, square_size, px, py, bx, by, c, mask)

        im2 = np.copy(imagen)

        if iteracion % 20 == 0:
            print("Iteracion ", iteracion)
            im = Image.fromarray(cv2.cvtColor(im2, cv2.COLOR_BGR2RGB))
            im.save("output3/imagen" + str(iteracion) + ".jpeg")

start_time = time.time()
procesar(img, mask)
end_time = time.time()
print("se calculo en:", (end_time-start_time)/60, " minutos")





