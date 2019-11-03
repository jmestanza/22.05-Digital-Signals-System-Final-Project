import numpy as np
import random
import cv2

def genSquare(square_size):
    square = []
    for i in range(square_size):
        for j in range(square_size):
            square.append(
                [
                    i - square_size // 2,
                    j - square_size // 2
                ]
            )
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


def getOrthogonalComponentOf(gradient):
    gx, gy = gradient
    # en este caso, no importa orientacion asi que elegimos una cualquiera
    return -gy, gx


def drawRect(image, pos, sq_sz, color):
    x, y = pos
    for i in range(-sq_sz // 2, sq_sz // 2):
        for j in range(-sq_sz // 2, sq_sz // 2):
            image[y + i][x + j] = color
    return

def getMaxGrad(square, shapeMask, x, y, gradient):
    max_grad = 0
    max_grad_value = 0, 0
    gx, gy = gradient

    for dx, dy in square:
        # solo sumamos si esta fuera de la zona a retocar
        if shapeMask[y + dy, x + dx] == 0:
            vx = gx[y][x]
            vy = gy[y][x]

            p = vx ** 2 + vy ** 2
            if p > max_grad:  # buscamos el mayor gradiente en norma
                max_grad = p
                max_grad_value = vx, vy

    return max_grad_value

def getTotalSum(imagen,sq_sz,x,y,px,py):
    return np.sum(np.square(imagen[y-sq_sz//2: y+sq_sz//2][x-sq_sz//2: x+sq_sz//2]-
           imagen[py-sq_sz//2: py+sq_sz//2][px-sq_sz//2: px+sq_sz//2]))

def copyPattern(imagen, square_size, best_benefit_point, minDistPatch, c, mask):
    px, py = best_benefit_point
    bx, by = minDistPatch
    # copia patch a zona reemplazar (el patron)
    imagen[py - square_size // 2: py + square_size // 2, px - square_size // 2: px + square_size // 2] = \
        imagen[by - square_size // 2: by + square_size // 2, bx - square_size // 2: bx + square_size // 2]

    ## copiamos la confianza del parche elegido a la la confianza del lugar donde copiamos el parche
    c[py - square_size // 2: py + square_size // 2, px - square_size // 2: px + square_size // 2] = \
        c[by - square_size // 2: by + square_size // 2, bx - square_size // 2: bx + square_size // 2] * 0.99

    ## marcamos la zona reemplazada como blanca
    mask[py - square_size // 2: py + square_size // 2, px - square_size // 2: px + square_size // 2] = \
        [255, 255, 255]
    return


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


def getBenefit(border_point_pos, border_normal, gradient, square, shapeMask, confidence):
    x, y = border_point_pos
    nx, ny = border_normal
    max_grad_value = getMaxGrad(square, shapeMask, x, y, gradient)
    # producto escalar del gradiente con la normal acorde a la formula
    nablaIpperp = getOrthogonalComponentOf(max_grad_value)

    d = nablaIpperp[0] * nx + nablaIpperp[1] * ny

    # el beneficio es la confianza por el factor d

    benefit = abs(d * confidence)

    return benefit


def contourAlgorithm(borde_actual, square, shapeMask, c, gradient):
    best_benefit = 0
    best_benefit_point = None
    ## necesitamos generar las normales de cada punto del contorno
    border_normal_list = getBorderNormal(borde_actual)
    for index, border_point in enumerate(borde_actual):
        border_point_pos = border_point[0]
        x, y = border_point_pos
        confidence = 0
        # consigo la confianza del punto del contorno actual
        for dx, dy in square:
            if shapeMask[y + dy, x + dx] == 0:  # si fuera de la region a retocar
                confidence += c[y + dy, x + dx]

        confidence /= len(square)

        # consigo la componente normal del gradiente
        border_normal = border_normal_list[index]
        benefit = getBenefit(border_point_pos, border_normal, gradient, square, shapeMask, confidence)

        # buscamos maximizar el beneficio
        if benefit > best_benefit:
            best_benefit = benefit
            best_benefit_point = x, y

    return best_benefit, best_benefit_point

