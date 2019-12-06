import cv2
import imutils
from PIL import Image
import time
import numpy as np
from Algoritmo import utils as ut


class Algorithm:
    def __init__(self, update_img_callback, orig_img_address):
        self.stop_flag = 0

        self.callback = update_img_callback
        self.orig_img_address = orig_img_address

        self.imagen = cv2.imread(self.orig_img_address, 3)  # matriz, cada el es un RGB
        # mascara con area a remover. Zona negra (0,0,0) se remueve, Blanca se deja(255,255,255)
        self.mask = cv2.imread("OutJobs/testmask.jpeg")

        self.search_times = 100
        self.iteraciones = 4000
        self.square_size = 3
        self.search_square_size = 30

        self.new_address = ""

    def run_algorithm(self):
        start_time = time.time()
        self.procesar()
        end_time = time.time()
        print("se calculo en:", (end_time-start_time)/60, " minutos")

    def procesar(self):
        square = ut.genSquare(self.square_size)

        # re-mapeamos a 0 y 255 la mascara. 255: zona a retocar, 0 a no retocar.
        shapeMask = ut.jpeg2MatrixMask(self.mask)
        # matriz de confianza, 0 o 1, si no se retoca es 1
        c = shapeMask[:, :] == 0

        for iteracion in range(self.iteraciones):

            best_benefit = 0
            best_benefit_point = None

            shapeMask = ut.jpeg2MatrixMask(self.mask)

            # detectamos el borde de la mascara y conseguimos un arreglo con todos los contornos
            # cnts me da los contornos cerrados (los que se van achicando segun el algoritmo)
            cnts = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            cnts = imutils.grab_contours(cnts)

            # conseguimos la escala de grises de la imagen (intensidad)
            grey_scale = cv2.cvtColor(self.imagen, cv2.COLOR_BGR2GRAY)

            gradient = ut.getGradient(grey_scale)
            gx, gy = gradient
            grad_norm = np.square(gx) + np.square(gy)

            # for contorno in range(len(cnts)):
            #     borde = cnts[contorno] #borde tiene los puntos que forman las curvas cerradas
            #     best_benefit, best_benefit_point = contourAlgorithm(borde, square, shapeMask, c, gradient)
            for contorno in range(len(cnts)):

                ## necesitamos generar las normales de cada punto del contorno
                borde = cnts[contorno]
                border_normal = ut.getBorderNormal(borde)

                for index,border_point in enumerate(cnts[contorno]):
                    x, y = border_point[0]

                    # consigo la confianza del punto del contorno actual
                    confidence = 0

                    for dx, dy in square:
                        if shapeMask[y + dy, x + dx] == 0: # si fuera de la region a retocar
                            confidence += c[y + dy, x + dx]

                    confidence /= len(square)

                    border_norm = border_normal[index]
                    benefit = ut.getBenefit(border_point[0],border_norm,gx,gy ,square,shapeMask,confidence,grad_norm, self.square_size)
                    # buscamos maximizar el beneficio
                    if benefit > best_benefit:
                        best_benefit = benefit
                        best_benefit_point = x, y

            if not best_benefit_point:
                print("No hay mas bordes. Fin")
                break

            # ahora vamos a calcular el parche que minimize la distancia
            minDistPatch = ut.getMinDistPatch(best_benefit_point, self.search_times, self.search_square_size, shapeMask,self.imagen, self.square_size)
            ut.copyPattern(self.imagen, self.square_size, best_benefit_point, minDistPatch, c, self.mask)

            if iteracion % 20 == 0:
                print("Iteracion ", iteracion)
                im = Image.fromarray(cv2.cvtColor(self.imagen, cv2.COLOR_BGR2RGB))
                im.save("OutJobs/imagen" + str(iteracion) + ".jpeg")
                self.new_address = "OutJobs/imagen" + str(iteracion) + ".jpeg"
                self.callback()

            if self.stop_flag == 1:
                break

    def stop_processing(self):
        self.stop_flag = 1

    def get_address(self):
        return self.new_address
