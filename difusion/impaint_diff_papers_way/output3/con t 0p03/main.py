import cv2
import imutils
from PIL import Image
import time
from utilsDifusion import *
import matplotlib.pyplot as plt


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


#def Ln(i,j, imagen):
#    Iyy_n = imagen[i - 1, j] - 2 * imagen[i,j] + imagen[i+1, j]
#    Ixx_n = imagen[i, j-1] - 2 * imagen[i,j] + imagen[i, j+1]
#    Ln = Ixx_n + Iyy_n
#    #imagen[340,323-1] dice que tiene algo con e87
#    return Ln
def get_Laplacian(imagen):
    src = imagen.copy()
    ddepth = cv2.CV_16S
    kernel_size = 3
    src = cv2.GaussianBlur(src, (3, 3), 0)
    src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    dst = cv2.Laplacian(src_gray, ddepth, ksize=kernel_size)
    return cv2.convertScaleAbs(dst)


def evolve_pixel(i,j,LUV_img, delta_t, epsilon, aux_copy_mat, Ln):
    # faltaria pasarlo a las otras coordenadas (no RGB)

    comp1 = Ln[i + 1, j].astype(np.float64) - Ln[i - 1, j].astype(np.float64)
    comp2 = Ln[i, j + 1].astype(np.float64) - Ln[i, j - 1].astype(np.float64)
    #---------
    Ix_n_b = LUV_img[i, j] - LUV_img[i, j - 1]  # esta es la backwards
    #---------

    Iy_n_b = LUV_img[i, j] - LUV_img[i - 1, j]
    Ix_n_f = LUV_img[i, j + 1] - LUV_img[i, j]  # esta es la forward
    Iy_n_f = LUV_img[i + 1, j] - LUV_img[i, j]
    It_n = []
    g = []
    beta = []
    for k in range(3):  # 3 componentes de color (no nec. RGB)
        dLnvector = np.array([comp1, comp2])
        aux_norm = np.sqrt(np.square(Ix_n_b[k]) + np.square(Iy_n_b[k]) + epsilon)
        Nvectorunit = np.array([-Iy_n_b[k] / aux_norm, Ix_n_b[k] / aux_norm])
        beta_n = np.dot(dLnvector, Nvectorunit)
        component_list = []
        if beta_n > 0:
            component_list.append(min(Ix_n_b[k], 0))
            component_list.append(max(Ix_n_f[k], 0))
            component_list.append(min(Iy_n_b[k], 0))
            component_list.append(max(Iy_n_f[k], 0))

        else:
            component_list.append(max(Ix_n_b[k], 0))
            component_list.append(min(Ix_n_f[k], 0))
            component_list.append(max(Iy_n_b[k], 0))
            component_list.append(min(Iy_n_f[k], 0))
        comp_vec = np.array(component_list)
        grad_module_n = np.sqrt(np.sum(np.square(comp_vec)))
        g.append(grad_module_n)
        beta.append(beta_n)
        # para ver como poner delta t deberiamos hacer algo como un histograma con el gradiente
        It_n.append(beta_n * grad_module_n)
    It_n = np.array(It_n)
    aux_copy_mat[i, j] = LUV_img[i, j] + delta_t * It_n
    #me aseguro de que ro no tenga datos invalidos
    # if aux_copy_mat[i,j,0] > 400:
    #     aux_copy_mat[i, j, 0] = 400
    #     print("sature ro")
    # if aux_copy_mat[i,j,0] < 0:
    #     aux_copy_mat[i, j, 0] = 0
    #     print("sature ro")

def setColorInOmega(imagen,aux_mask,color=[255, 255, 255]):
    finished = False
    while not finished:
        shapeMask = jpeg2MatrixMask(aux_mask)
        cnts = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cnts = imutils.grab_contours(cnts)
        if len(cnts) == 0:
            finished = True
        for contorno in range(len(cnts)):
            ## necesitamos generar las normales de cada punto del contorno
            borde = cnts[contorno]
            # FILA: +y (i) COLUMNA: +x (j) (lo mismo con el gradiente)
            for index, border_point in enumerate(borde):
                x, y = border_point[0]
                i, j = y, x
                imagen[i, j] = np.array(color)
                aux_mask[i, j] = np.array([255, 255, 255])  # este punto del borde ya fue procesado
    im = Image.fromarray(imagen)
    im.save("output3/imagen" + "concolordeomega" + ".jpeg")


def procesar(imagen, mask, iteraciones):
    # re-mapeamos a 0 y 255 la mascara. 255: zona a retocar, 0 a no retocar.
    shapeMask = jpeg2MatrixMask(mask)

    imagen = anisoDiffusion(imagen, 10, 'BGR')
    # matriz de confianza, 0 o 1, si no se retoca es 1
    c = shapeMask[:, :] == 0
    #setColorInOmega(imagen,mask.copy(), color=[127, 127, 127])
    max_masks = 10
    cnt_mask = 0
    delta_t = 0.03 # tunear este parametro segun la imagen
    epsilon = 0.01



    # con esto genere mi nuevo eje de coordenadas
    color_model = BGR_to_color_model(imagen, epsilon)
    imagen = color_model_to_RGB(color_model, 'BGR')
    #np.seterr(all='raise')
    aux_copy_mat = color_model.copy()

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
            for border_point in borde:
                j, i = border_point[0]
                evolve_pixel(i, j, color_model, delta_t, epsilon, aux_copy_mat, Ln)
                #ro_aux = aux_copy_mat[:,:,0]
                #aux_copy_mat[i,j] = np.array([0,0,0])
                mask[i, j] = np.array([255, 255, 255]) #este punto del borde ya fue procesado
            # una vez que complete un borde, hago que imagen sea la copia
            color_model = aux_copy_mat.copy()
            imagen = color_model_to_RGB(color_model,'BGR')
        if iteracion % 50 == 0:
            print("Iteracion ", iteracion)
            RGB_img = color_model_to_RGB(color_model, 'RGB')
            im = Image.fromarray(RGB_img)
            im.save("output3/imagen" + str(iteracion) + ".jpeg")


start_time = time.time()
iteraciones = 1000
procesar(img, mask,iteraciones)
end_time = time.time()
print("se calculo en:", (end_time-start_time)/60, " minutos")

