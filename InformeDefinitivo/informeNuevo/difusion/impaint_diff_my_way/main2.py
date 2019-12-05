import cv2
import imutils
from PIL import Image
import time
from utilsDifusion import *
import matplotlib.pyplot as plt

img = cv2.imread('output3/imagen_reconstruir.jpeg', 3)# matriz, cada el es un RGB
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

def Ln(i,j, imagen):
    Iyy_n = imagen[i - 1, j] - 2 * imagen[i,j] + imagen[i+1, j]
    Ixx_n = imagen[i, j-1] - 2 * imagen[i,j] + imagen[i, j+1]
    Ln = Ixx_n + Iyy_n
    return Ln

def procesar(imagen, mask, iteraciones):
    # re-mapeamos a 0 y 255 la mascara. 255: zona a retocar, 0 a no retocar.
    shapeMask = jpeg2MatrixMask(mask)
    cnt_mask = 0
    max_masks = 100

    for iteracion in range(iteraciones):

        shapeMask = jpeg2MatrixMask(mask)
        # detectamos el borde de la mascara y conseguimos un arreglo con todos los contornos
        # cnts me da los contornos cerrados (los que se van achicando segun el algoritmo)
        cnts = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cnts = imutils.grab_contours(cnts)

        if iteracion%10 == 0:
            imagen = anisoDiffusion(imagen, 1, 'BGR')

        # conseguimos la escala de grises de la imagen (intensidad)
        grey_scale = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

        gradient = getGradient(grey_scale)
        gx, gy = gradient
        grad_norm = np.square(gx) + np.square(gy)
        cnt_diff = 0
        delta_t = 0.01
        epsilon = 0.01

        aux_img = imagen.copy()


        if len(cnts) == 0:
            if cnt_mask < max_masks:
                cnt_mask += 1
                mask = cv2.imread("output3/mask.jpeg")
            else:
                print("No hay mas bordes. Fin")
                break
        for contorno in range(len(cnts)):

            ## necesitamos generar las normales de cada punto del contorno
            borde = cnts[contorno]
            #border_normal = getBorderNormal(borde)

            #imagen[:,10] = [0,0,255] # pinta la columna 10 de rojo
            # a imagen accedo por FILA y despues COLUMNA, por ende
            # FILA: +y (i) COLUMNA: +x (j)
            # Lo mismo con el gradiente
            for index,border_point in enumerate(cnts[contorno]):
                x, y = border_point[0]
                i ,j = y, x
                #algoritmo que hace cosas con el borde va acá!
                #faltaria pasarlo a las otras coordenadas (no RGB)
                #border_norm = border_normal[index]
                comp1 = Ln(i+1,j,imagen) - Ln(i-1,j,imagen)
                comp2 = Ln(i,j+1,imagen) - Ln(i,j-1,imagen)
                for k in range(3): #BGR
                    dLnvector= np.array([comp1[k],comp2[k]])
                    aux_norm = np.sqrt( np.square(gy[i,j])+ np.square(gx[i,j]) + epsilon)
                    Nvectorunit = np.array([-gy[i,j]/aux_norm, gx[i,j]/aux_norm])
                    beta_n= np.dot(dLnvector, Nvectorunit)
                    It_n = beta_n * np.sqrt(np.square(gx[i,j] + np.square(gy[i,j])))
                aux_img[i,j] = imagen[i,j] + delta_t * It_n

                mask[y, x] = np.array([255, 255, 255]) #este punto del borde ya fue procesado
        imagen = aux_img.copy()
        if iteracion % 50 == 0:
            print("Iteracion ", iteracion)
            im = Image.fromarray(cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB))
            im.save("output3/imagen" + str(iteracion) + ".jpeg")

start_time = time.time()
iteraciones = 1000
procesar(img, mask,iteraciones)
end_time = time.time()
print("se calculo en:", (end_time-start_time)/60, " minutos")