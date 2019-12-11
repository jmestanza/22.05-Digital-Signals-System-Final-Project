import cv2
import imutils
from PIL import Image
import time
from utilsDifusion import *

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


def getGradient(image):
    gx = np.zeros_like(image)
    gy = np.zeros_like(image)
    gx = gx.astype(np.float64)
    gy = gy.astype(np.float64)
    for i in range(3):
        channel = image[:, :, i]
        sobel_x = cv2.Sobel(channel, cv2.CV_64F, 1, 0, ksize=5)
        sobel_y = cv2.Sobel(channel, cv2.CV_64F, 0, 1, ksize=5)
        gx[:, :, i] = sobel_x
        gy[:, :, i] = sobel_y

    return gx, gy

def get_Laplacian(imagen):
    Laplacian = np.zeros_like(imagen)
    Laplacian = Laplacian.astype(np.float64)
    for i in range(3):
        src = imagen[:, :, i].copy()
        ddepth = cv2.CV_16S
        kernel_size = 3
        src = cv2.GaussianBlur(src, (3, 3), 0)
        dst = cv2.Laplacian(src, ddepth, ksize=kernel_size)
        Laplacian[:, :, i] = cv2.convertScaleAbs(dst)
    return Laplacian

def evolve_pixel(i,j,imagen, delta_t, epsilon, aux_copy_mat, Ln, gx, gy, alpha):
    comp1 = Ln[i+1, j] - Ln[i-1, j]
    comp2 = Ln[i, j + 1] - Ln[i, j - 1]
    It_n = []
    for k in range(3):  # 3 componentes de color (no nec. RGB)
        dLnvector = np.array([comp1[k], comp2[k]])
        aux_norm = np.sqrt(np.square(gx[i, j, k]) + np.square(gy[i, j, k]) + epsilon)
        Nvectorunit = np.array([-gy[i, j, k] / aux_norm, gx[i, j, k] / aux_norm])
        beta_n = np.dot(dLnvector, Nvectorunit)
        grad_module_n = np.sqrt(gx[i, j, k]**2 + gy[i, j, k]**2)
        # para ver como poner delta t deberiamos hacer algo como un histograma con el gradiente
        It_n.append(beta_n * grad_module_n * np.exp(-grad_module_n/alpha))
        #print(It_n[k])
        if (imagen[i, j, k] + delta_t * It_n[k]) > 254:
            print("se zarpo por arriba")
            It_n[k] = 255
        if (imagen[i, j, k] + delta_t * It_n[k]) < 1:
            print("zarpado por abajo")
            It_n[k] = 0
    It_n = np.array(It_n)
    aux_copy_mat[i, j] = imagen[i, j] + delta_t * It_n

def procesar(imagen, mask, iteraciones):
    # re-mapeamos a 0 y 255 la mascara. 255: zona a retocar, 0 a no retocar.
    shapeMask = jpeg2MatrixMask(mask)
    imagen = anisoDiffusion(imagen, 10, 'BGR')
    max_masks = 1
    cnt_mask = 0
    delta_t = 0.01 # tunear este parametro segun la imagen
    epsilon = 0.01
    alpha = 0.01

    #imagen = imagen.astype(np.float64)
    aux_copy_mat = imagen.copy()

    for iteracion in range(iteraciones):
        shapeMask = jpeg2MatrixMask(mask)
        # detectamos el borde de la mascara y conseguimos un arreglo con todos los contornos
        # cnts me da los contornos cerrados (los que se van achicando segun el algoritmo)
        cnts = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cnts = imutils.grab_contours(cnts)

        if len(cnts) == 0:
            if cnt_mask < max_masks:
                cnt_mask += 1
                mask = cv2.imread("output3/mask.jpeg")
            else:
                print("No hay mas bordes. Fin")
                break
        for borde in cnts:
            Ln = get_Laplacian(imagen)
            gx, gy = getGradient(imagen)
            for border_point in borde:
                j, i = border_point[0]
                evolve_pixel(i, j, imagen, delta_t, epsilon, aux_copy_mat, Ln, gx, gy, alpha)
                mask[i, j] = np.array([255, 255, 255]) #este punto del borde ya fue procesado
            # una vez que complete un borde, hago que imagen sea la copia
            imagen = aux_copy_mat.copy()
        if iteracion % 10 == 0:
            print("Iteracion ", iteracion)
            im = Image.fromarray(cv2.cvtColor(imagen.astype(np.uint8), cv2.COLOR_BGR2RGB))
            im.save("output3/imagen" + str(iteracion) + ".jpeg")

start_time = time.time()
iteraciones = 1000
procesar(img, mask,iteraciones)
end_time = time.time()
print("se calculo en:", (end_time-start_time)/60, " minutos")

