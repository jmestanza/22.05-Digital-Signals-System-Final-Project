import cv2
import imutils
from numpy import random
from PIL import Image
import time
import numpy as np
from utils import *
import matplotlib.pyplot as plt

img = cv2.imread('output3/imagen.jpeg', 3) #esto devuelve una matriz de RGB
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
    for iteracion in range(iteraciones):
        # detectamos el borde de la mascara y conseguimos un arreglo con todos los contornos
        cnts = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cnts = imutils.grab_contours(cnts)
        # cada contorno cerrado forma un arreglo
        # luego tenemos que calcular la funcion de costos
        best_benefit = 0
        best_benefit_point = None

        # conseguimos la escala de grises de la imagen
        grey_scale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # gradiente en x e y de la escala de grises, sobel suaviza el gradiente
        sobel_x = cv2.Sobel(grey_scale, cv2.CV_64F, 1, 0, ksize=5)
        sobel_y = cv2.Sobel(grey_scale, cv2.CV_64F, 0, 1, ksize=5)
        # el gradiente siempre apunta en la dirección de máximo crecimiento
        # y en la curva de nivel, es perpendicular a la tangencial
        # => nos quedamos con la tangencial (no importa la orientacion)
        sobel_x, sobel_y = -sobel_y, sobel_x

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





