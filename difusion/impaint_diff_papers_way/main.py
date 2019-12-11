import cv2
import imutils
from PIL import Image
import time
from utilsDifusion import *
import matplotlib.pyplot as plt


img = cv2.imread('output3/testimage2.jpeg', 3)# matriz, cada el es un RGB
# mascara con area a remover. Zona negra (0,0,0) se remueve, Blanca se deja(255,255,255)
mask = cv2.imread("output3/testmask.jpeg")

#lado de los cuadrados que utilizaremos para rellenar la imagen
square_size = 5
# guardamos en un arreglo las coordenadas que describen al cuadrado
square = genSquare(square_size)

# tamanio del cuadrado de busqueda para el parche que reemplaza la posicion a rellenear
search_square_size = 500

# cuantas veces buscamos al azar por un parche
search_times = 100

def ortho(gradient_point):
    gx, gy = gradient_point
    # en este caso, no importa orientacion asi que elegimos una cualquiera
    return -gy, gx

def Ln(i,j, imagen):
    #if i == 340 and j == 323:
    #    print("error")
    Ixx_n = np.zeros_like(imagen[i,j])
    Iyy_n = np.zeros_like(imagen[i, j])

    Ixx_n.astype(np.int32)
    Iyy_n.astype(np.int32)

    Iyy_n = imagen[i - 1, j] - 2 * imagen[i,j] + imagen[i+1, j]
    Ixx_n = imagen[i, j-1] - 2 * imagen[i,j] + imagen[i, j+1]
    Ln = Ixx_n + Iyy_n
    #imagen[340,323-1] dice que tiene algo con e87
    return Ln

# def get_Laplacian(imagen):
#     src = imagen.copy()
#     ddepth = cv2.CV_16S
#     kernel_size = 3
#     src = cv2.GaussianBlur(src, (3, 3), 0)
#     src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
#     dst = cv2.Laplacian(src_gray, ddepth, ksize=kernel_size)
#     return cv2.convertScaleAbs(dst)


def evolve_pixel(i,j,LUV_img, delta_t, epsilon, aux_copy_mat):
    # faltaria pasarlo a las otras coordenadas (no RGB)

    #comp1 = Ln[i + 1, j].astype(np.float64) - Ln[i - 1, j].astype(np.float64)
    #comp2 = Ln[i, j + 1].astype(np.float64) - Ln[i, j - 1].astype(np.float64)
    comp1 = Ln(i + 1, j, LUV_img) - Ln(i - 1, j, LUV_img)
    comp2 = Ln(i, j + 1, LUV_img) - Ln(i, j - 1,LUV_img)

    #---------
    Ix_n_b = np.zeros_like(LUV_img[i, j])
    Ix_n_b.astype(np.int32)
    Ix_n_b = LUV_img[i, j] - LUV_img[i, j - 1]  # esta es la backwards

    Iy_n_b = np.zeros_like(LUV_img[i, j])
    Iy_n_b.astype(np.int32)
    Iy_n_b = LUV_img[i, j] - LUV_img[i - 1, j]

    Ix_n_f = np.zeros_like(LUV_img[i, j])
    Ix_n_f.astype(np.int32)
    Ix_n_f = LUV_img[i, j + 1] - LUV_img[i, j]  # esta es la forward

    Iy_n_f = np.zeros_like(LUV_img[i, j])
    Iy_n_f.astype(np.int32)
    Iy_n_f = LUV_img[i + 1, j] - LUV_img[i, j]


    It_n = []
    g = []
    beta = []
    for k in range(3):  # 3 componentes de color (no nec. RGB)
#        dLnvector = np.array([comp1, comp2])
        dLnvector = np.array([comp1[k], comp2[k]])

        aux_norm = np.sqrt(np.square(Ix_n_b[k]) + np.square(Iy_n_b[k]) + epsilon)
        Nvectorunit = np.array([-Iy_n_b[k] / aux_norm, Ix_n_b[k] / aux_norm])
        #aux_norm = np.sqrt(np.square(gx[i,j]) + np.square(gy[i,j]) + epsilon)
        #Nvectorunit = np.array([-gy[i,j] / aux_norm, gx[i,j] / aux_norm])

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
        #grad_module_n = np.sqrt(gx[i,j]**2 + gy[i,j]**2)
        g.append(grad_module_n)
        beta.append(beta_n)
        # para ver como poner delta t deberiamos hacer algo como un histograma con el gradiente
        It_n.append(beta_n * grad_module_n)
    It_n = np.array(It_n)
    aux_copy_mat[i, j] = LUV_img[i, j] + delta_t * It_n
    #me aseguro de que ro no tenga datos invalidos
    # if aux_copy_mat[i,j,0] > 442:
    #     aux_copy_mat[i, j, 0] = 442
    #     print("sature ro")
    # if aux_copy_mat[i,j,0] < 0:
    #     aux_copy_mat[i, j, 0] = 0
    #     print("sature ro")

def g(delta_i_2, alpha):
    return np.exp(-delta_i_2 / alpha**2)

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
    mcopy = mask.copy()

    mask_value = np.where(mcopy[:, :, 0] > 127, np.zeros(imagen[:,:,0].shape), np.ones(imagen[:,:,0].shape))

    # = jpeg2MatrixMask(mask)

    imagen = anisoDiffusion(imagen, 10, 'BGR')
    # matriz de confianza, 0 o 1, si no se retoca es 1
    #c = shapeMask[:, :] == 0
    #setColorInOmega(imagen,mask.copy(), color=[127, 127, 127])
    max_masks = 10
    cnt_mask = 0
    delta_t = 0.03 # tunear este parametro segun la imagen
    epsilon = 0.01

    # con esto genere mi nuevo eje de coordenadas
    #color_model = BGR_to_color_model(imagen, epsilon)
    #imagen = color_model_to_RGB(color_model, 'BGR')
    #np.seterr(all='raise')
    imagen = imagen.astype(np.float64)
    #aux_copy_mat = color_model.copy()
    #aux_copy_mat = imagen.copy()



    for iteracion in range(iteraciones):
        if iteracion == 50:
            print("hello")
        #shapeMask = jpeg2MatrixMask(mask)
        # detectamos el borde de la mascara y conseguimos un arreglo con todos los contornos
        # cnts me da los contornos cerrados (los que se van achicando segun el algoritmo)
        #cnts = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        #cnts = imutils.grab_contours(cnts)

        # if len(cnts) == 0:
        #     if cnt_mask < max_masks:
        #         cnt_mask += 1
        #         mask = cv2.imread("output3/mask.jpeg")
        #     else:
        #         print("No hay mas bordes. Fin")
        #         break

        for channel in range(3):
            canal = imagen[:, :, channel]

            sobel_x = cv2.Sobel(canal, cv2.CV_64F, 1, 0, ksize=3)
            sobel_y = cv2.Sobel(canal, cv2.CV_64F, 0, 1, ksize=3)

            sobel_xx = cv2.Sobel(sobel_x, cv2.CV_64F, 1, 0, ksize=3)
            sobel_yy = cv2.Sobel(sobel_y, cv2.CV_64F, 0, 1, ksize=3)

            laplaciano = sobel_xx + sobel_yy

            laplaciano_dx = cv2.Sobel(laplaciano, cv2.CV_64F, 1, 0, ksize=3)
            laplaciano_dy = cv2.Sobel(laplaciano, cv2.CV_64F, 0, 1, ksize=3)

            dt = 0.000001
            alpha = 0.0001

            try:
                #norma_delta_i_2 = np.sqrt(sobel_x * sobel_x + sobel_y * sobel_y)
                di = dt * (laplaciano_dx * sobel_y + laplaciano_dy * sobel_x)

                fix_value = np.where((canal < 5) | (canal > 251) | (mask_value == 0), np.zeros(canal.shape), np.ones(canal.shape)*di)

                canal += fix_value

            except FloatingPointError:
                print("hola")
                #norma_delta_i_2 = np.sqrt(sobel_x * sobel_x + sobel_y * sobel_y)
                #di = dt * (laplaciano_dx * sobel_y + laplaciano_dy * sobel_x)
                pass

        if iteracion % 50 == 0:
            im = Image.fromarray(cv2.cvtColor(imagen.astype(np.uint8), cv2.COLOR_BGR2RGB))
            im.save("output5/image%d.png" % iteracion)
            print("Iteracion %d terminada" % iteracion)
                # im = Image.fromarray(sobel_yy).convert('RGB')
                # im.save("output_yy%d.png" % channel)

        #print("hello world")

#         for borde in cnts:
# #            Ln = get_Laplacian(imagen)
# #            gx, gy = getGradient(cv2.cvtColor(imagen, cv2.COLOR_RGB2GRAY))
#
#             for border_point in borde:
#                 j, i = border_point[0]
#                 evolve_pixel(i, j, imagen, delta_t, epsilon, aux_copy_mat)
#                 #evolve_pixel(i, j, color_model, delta_t, epsilon, aux_copy_mat, Ln, gx, gy)
#                 #ro_aux = aux_copy_mat[:,:,0]
#                 #aux_copy_mat[i,j] = np.array([0,0,0])
#                 mask[i, j] = np.array([255, 255, 255]) #este punto del borde ya fue procesado
#             # una vez que complete un borde, hago que imagen sea la copia
#             #color_model = aux_copy_mat.copy()
#             imagen = aux_copy_mat.copy()
#             #imagen = color_model_to_RGB(color_model,'BGR')
#         if iteracion % 50 == 0:
#             print("Iteracion ", iteracion)
#             #RGB_img = color_model_to_RGB(color_model, 'RGB')
#             im = Image.fromarray(imagen, cv2.COLOR_BGR2RGB)
#             im.save("output3/imagen" + str(iteracion) + ".jpeg")


start_time = time.time()
iteraciones = 10000
procesar(img, mask,iteraciones)
end_time = time.time()
print("se calculo en:", (end_time-start_time)/60, " minutos")

