import cv2
import imutils
from PIL import Image
import time
from utils import *
import matplotlib.pyplot as plt


img = cv2.imread('output3/imgred.jpeg', 3)# matriz, cada el es un RGB
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
    Iyy_n = np.zeros_like(imagen[i, j])
    Ixx_n = np.zeros_like(imagen[i, j])
    L_n = np.zeros_like(imagen[i, j])
    Iyy_n = Iyy_n.astype(np.float64)
    Ixx_n = Ixx_n.astype(np.float64)
    L_n = L_n.astype(np.float64)

    Iyy_n = imagen[i - 1, j] - 2 * imagen[i,j] + imagen[i+1, j]
    Ixx_n = imagen[i, j-1] - 2 * imagen[i,j] + imagen[i, j+1]
    Ln = Ixx_n + Iyy_n

    return Ln

def color_model_to_RGB(color_model):
    ro = color_model[:, :, 0]
    sin_phi = color_model[:, :, 1]
    sin_psi = color_model[:, :, 2]
    G = ro*sin_psi # good
    R = np.sqrt( np.square(sin_phi) * (np.square(ro) - np.square(G)))
    B = np.sqrt( np.square(ro) - (np.square(R)+np.square(G)))
    ans = np.zeros_like(color_model)
    ans[:, :, 0] = R
    ans[:, :, 1] = G
    ans[:, :, 2] = B
    ans = ans.astype(np.uint8)
    return ans


def evolve_pixel(i,j,LUV_img, delta_t, epsilon, aux_copy_mat):
    # faltaria pasarlo a las otras coordenadas (no RGB)

    comp1 = Ln(i + 1, j, LUV_img) - Ln(i - 1, j, LUV_img)
    asd = LUV_img[:, :, 0]
    asd2 = LUV_img[339][309]
    if i == 339 and j == 308:
        a = LUV_img[339][309]
        Ln(i, j + 1, LUV_img)
        Ln(i, j - 1, LUV_img)
    comp2 = Ln(i, j + 1, LUV_img) - Ln(i, j - 1, LUV_img)
    Ix_n_b = LUV_img[i, j] - LUV_img[i, j - 1]  # esta es la backwards
    Iy_n_b = LUV_img[i, j] - LUV_img[i - 1, j]
    Ix_n_f = LUV_img[i, j + 1] - LUV_img[i, j]  # esta es la forward
    Iy_n_f = LUV_img[i + 1, j] - LUV_img[i, j]
    It_n = []
    for k in range(3):  # 3 componentes de color (no nec. RGB)
        dLnvector = np.array([comp1[k], comp2[k]])
        aux_norm = np.sqrt(np.square(Ix_n_b[k]) + np.square(Iy_n_b[k]) + epsilon)
        Nvectorunit = np.array([-Iy_n_b[k] / aux_norm, Ix_n_b[k] / aux_norm])
        beta_n = np.dot(dLnvector, Nvectorunit)
        if(beta_n>0):
            component_list = []
            component_list.append(min(Ix_n_b[k],0))
            component_list.append(max(Ix_n_f[k],0))
            component_list.append(min(Iy_n_b[k], 0))
            component_list.append(max(Iy_n_f[k], 0))
            comp_vec = np.array(component_list)
        else:
            component_list = []
            component_list.append(max(Ix_n_b[k], 0))
            component_list.append(min(Ix_n_f[k], 0))
            component_list.append(max(Iy_n_b[k], 0))
            component_list.append(min(Iy_n_f[k], 0))
            comp_vec = np.array(component_list)
        try:
            grad_module_n = np.sqrt(np.sum(np.square(comp_vec)))
        except:
            print("asd")
        It_n.append(beta_n * grad_module_n)
    It_n = np.array(It_n)
    aux_copy_mat[i, j] = LUV_img[i, j] + delta_t * It_n


def BGR_to_color_model(imagen, eps):
    B = imagen[:, :, 0]
    B = B.astype(np.float64)
    G = imagen[:, :, 1]
    G = G.astype(np.float64)
    R = imagen[:, :, 2]
    R = R.astype(np.float64)
    ro = np.sqrt(np.square(R) + np.square(G) + np.square(B) + eps)
    sin_phi = R / (np.sqrt(np.square(B) + np.square(R) + eps))
    sin_psi = G / ro
    color_model = np.zeros_like(imagen)
    color_model = color_model.astype(np.float64)
    color_model[:, :, 0] = ro
    color_model[:, :, 1] = sin_phi
    color_model[:, :, 2] = sin_psi
    return color_model

def procesar(imagen, mask, iteraciones):
    # re-mapeamos a 0 y 255 la mascara. 255: zona a retocar, 0 a no retocar.
    shapeMask = jpeg2MatrixMask(mask)
    # matriz de confianza, 0 o 1, si no se retoca es 1
    c = shapeMask[:, :] == 0
    # con esto genere mi nuevo eje de coordenadas
    color_model = BGR_to_color_model(imagen,eps=10)
    #np.seterr(all='raise')

    aux_copy_mat = color_model.copy()
    max_masks = 10
    cnt_mask = 0
    for iteracion in range(iteraciones):

        shapeMask = jpeg2MatrixMask(mask)
        # detectamos el borde de la mascara y conseguimos un arreglo con todos los contornos
        # cnts me da los contornos cerrados (los que se van achicando segun el algoritmo)
        cnts = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cnts = imutils.grab_contours(cnts)

        delta_t = 0.1
        epsilon = 10

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
            # FILA: +y (i) COLUMNA: +x (j) (lo mismo con el gradiente)
            for index,border_point in enumerate(borde):
                x, y = border_point[0]
                i, j = y, x
                #algoritmo que hace cosas con el borde va acá!
                #bROther = color_model[:,:,0]
                evolve_pixel(i, j, color_model, delta_t, 10, aux_copy_mat)
                mask[i, j] = np.array([255, 255, 255]) #este punto del borde ya fue procesado

            # una vez que complete un borde, hago que imagen sea la copia
            color_model = aux_copy_mat.copy()
        if iteracion % 1 == 0:
            print("Iteracion ", iteracion)
            #im = Image.fromarray(cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB))
            RGB_img = color_model_to_RGB(color_model)
            im = Image.fromarray(RGB_img)
            # IMPORTANTE: imagen esta en BGR
            im.save("output3/imagen" + str(iteracion) + ".jpeg")

start_time = time.time()
iteraciones = 1000
procesar(img, mask,iteraciones)
end_time = time.time()
print("se calculo en:", (end_time-start_time)/60, " minutos")

