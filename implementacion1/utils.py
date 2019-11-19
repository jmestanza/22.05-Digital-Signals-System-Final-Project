import numpy as np
import random
import cv2
import numba
from numba import jit

def genSquare(square_size):
    first = True
    for i in range(square_size):
        for j in range(square_size):
            aux = np.array([i - square_size // 2, j - square_size // 2])
            if first:
                square = np.array([aux])
                first = False
            else:
                square = np.append(square, np.array([aux]), axis=0)
    return square


def jpeg2MatrixMask(mask):
    # lower y upper son bounds para buscar el color negro con la funcion inRange
    lower = np.array([0, 0, 0])
    upper = np.array([15, 15, 15])
    # re-mapeamos a 0 y 255 la mascara. 255: zona a retocar, 0 a no retocar.
    shapeMask = cv2.inRange(mask, lower, upper)
    return shapeMask


def getGradient(grey_scale):
    # gradiente en x e y de la escala de grises, sobel suaviza el gradiente
    sobel_x = cv2.Sobel(grey_scale, cv2.CV_64F, 1, 0, ksize=5)
    sobel_y = cv2.Sobel(grey_scale, cv2.CV_64F, 0, 1, ksize=5)

    return sobel_x, sobel_y


def getOrthogonalComponentOf(gradient_point):
    gx, gy = gradient_point
    # en este caso, no importa orientacion asi que elegimos una cualquiera
    return -gy, gx


def drawRect(image, pos, sq_sz, color):
    x, y = pos
    for i in range(-sq_sz // 2, sq_sz // 2):
        for j in range(-sq_sz // 2, sq_sz // 2):
            image[y + i][x + j] = color
    return

@jit(nopython=True)
def getMaxGrad(square, shapeMask, x, y, gx, gy, grad_norm, square_size):
    max_grad_norm = -1e10
#     hs = square_size // 2 #half-square
#     arr = shapeMask == 0
#     sh_mask = arr[(y-hs):(y+hs),(x-hs):(x+hs)] # me quede con los bools que me dicen si esta ne ShapeMask
#     indexes = sh_mask == 0
#     sub_mat = grad_norm[(y-hs):(y+hs),(x-hs):(x+hs)][indexes]
#     gx_aux = gx[(y-hs):(y+hs),(x-hs):(x+hs)][indexes]
#     gy_aux = gy[(y-hs):(y+hs),(x-hs):(x+hs)][indexes]
#
#     ind = np.unravel_index(np.argmax(sub_mat, axis=None), sub_mat.shape)
#     max_grad = gx_aux[ind] , gy_aux[ind] # me devuelve el maximo gradiente
    for i in range(len(square[0, :])):
       dx = square[i][0]
       dy = square[i][1]
#        solo sumamos si esta fuera de la zona a retocar
       if shapeMask[y + dy][x + dx] == 0:
            p = grad_norm[y+dy][x+dx]
            if p > max_grad_norm:  # buscamos el mayor gradiente en norma
                max_grad_norm = p
                max_grad = gx[y + dy][x + dx], gy[y + dy][x + dx]
    return max_grad


@jit(nopython=True)
def getTotalSum(imagen,sq_sz,x,y,px,py):
    return np.sum(np.square(imagen[y-sq_sz//2: y+sq_sz//2][x-sq_sz//2: x+sq_sz//2]-
           imagen[py-sq_sz//2: py+sq_sz//2][px-sq_sz//2: px+sq_sz//2]))

@jit(nopython=True)
def copyPattern(imagen, square_size, best_benefit_point, minDistPatch, c, mask):
    px, py = best_benefit_point
    bx, by = minDistPatch
    # copia patch a zona reemplazar (el patron)
    half_sq = square_size // 2
    imagen[py - half_sq: py + half_sq, px - half_sq: px + half_sq] = \
        imagen[by - half_sq: by + half_sq, bx - half_sq: bx + half_sq]

    ## copiamos la confianza del parche elegido a la la confianza del lugar donde copiamos el parche
    c[py - half_sq: py + half_sq, px - half_sq: px + half_sq] = \
        c[by - half_sq: by + half_sq, bx - half_sq: bx + half_sq] * 0.99

    ## marcamos la zona reemplazada como blanca
    mask[py - half_sq: py + half_sq, px - half_sq: px + half_sq] = np.array([255, 255, 255])
    return

@jit(nopython=True)
def getBorderNormal(borde):
    n = len(borde)
    border_normal_list = []
    for i in range(n):
        dx = borde[i][0][0] - borde[(i - 1) % n][0][0]
        dy = borde[i][0][1] - borde[(i - 1) % n][0][1]
        border_normal_list.append((dy, -dx))
        # esta formula nos da la normal. no le damos importancia a la orientacion
    return border_normal_list.copy()


def getMinDistPatch(best_benefit_point,search_times,search_square_size,shapeMask,imagen,square_size):
    px, py = best_benefit_point

    best_patch = px, py  # default
    patch_distance = np.Infinity

    for i in range(search_times):
        x = random.randint(px - search_square_size // 2, px + search_square_size // 2)
        y = random.randint(py - search_square_size // 2, py + search_square_size // 2)
        if shapeMask[y, x] == 255:
            continue  # no es de interes ya que esta en la region blanca

        total_sum = getTotalSum(imagen, square_size, x, y, px, py)

        if total_sum < patch_distance:
            patch_distance = total_sum
                #last_patch_distance
            best_patch = x, y

    return best_patch


#def getOrthogonalComponentOf(gradient_point):
#    gx, gy = gradient_point
#    # en este caso, no importa orientacion asi que elegimos una cualquiera
#    return -gy, gx

@jit(nopython=True)
def getBenefit(border_point_pos, border_normal, gx,gy , square, shapeMask, confidence,grad_norm, square_size):
    x, y = border_point_pos
    nx, ny = border_normal
    max_grad = getMaxGrad(square, shapeMask, x, y, gx, gy,grad_norm, square_size)
    # producto escalar del gradiente con la normal acorde a la formula
    perpy, perpx = max_grad
    perpy = -perpy
    #nablaIpperp = getOrthogonalComponentOf(max_grad)

    #d = nablaIpperp[0] * nx + nablaIpperp[1] * ny
    d = perpx * nx + perpy * ny
    # el beneficio es la confianza por el factor d

    benefit = abs(d * confidence)

    return benefit
