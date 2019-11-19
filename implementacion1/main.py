import cv2
import imutils
from PIL import Image
import time
from utils import *


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

        gradient = getGradient(grey_scale)
        gx, gy = gradient
        grad_norm = np.square(gx) + np.square(gy)

        # for contorno in range(len(cnts)):
        #     borde = cnts[contorno] #borde tiene los puntos que forman las curvas cerradas
        #     best_benefit, best_benefit_point = contourAlgorithm(borde, square, shapeMask, c, gradient)
        for contorno in range(len(cnts)):

            ## necesitamos generar las normales de cada punto del contorno
            borde = cnts[contorno]
            border_normal = getBorderNormal(borde)

            for index,border_point in enumerate(cnts[contorno]):
                x, y = border_point[0]

                # consigo la confianza del punto del contorno actual
                confidence = 0

                for dx, dy in square:
                    if shapeMask[y + dy, x + dx] == 0: # si fuera de la region a retocar
                        confidence += c[y + dy, x + dx]

                confidence /= len(square)

                border_norm = border_normal[index]
                benefit = getBenefit(border_point[0],border_norm,gx,gy ,square,shapeMask,confidence,grad_norm, square_size)
                # buscamos maximizar el beneficio
                if benefit > best_benefit:
                    best_benefit = benefit
                    best_benefit_point = x, y

        if not best_benefit_point:
            print("No hay mas bordes. Fin")
            break

        # ahora vamos a calcular el parche que minimize la distancia
        minDistPatch = getMinDistPatch(best_benefit_point, search_times, search_square_size, shapeMask,imagen, square_size)
        copyPattern(imagen, square_size, best_benefit_point, minDistPatch, c, mask)

        if iteracion % 20 == 0:
            print("Iteracion ", iteracion)
            im = Image.fromarray(cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB))
            im.save("output3/imagen" + str(iteracion) + ".jpeg")


start_time = time.time()
iteraciones = 500
procesar(img, mask,iteraciones)
end_time = time.time()
print("se calculo en:", (end_time-start_time)/60, " minutos")

