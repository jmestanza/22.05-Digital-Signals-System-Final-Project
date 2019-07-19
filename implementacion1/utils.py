import numpy as np


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
    return square.copy()


def getMaxGrad(square,shapeMask,x,y,sobel_x,sobel_y):

    max_grad = 0
    max_grad_value = 0, 0

    for dx, dy in square:
        # solo sumamos si esta fuera de la zona a retocar
        if shapeMask[y + dy, x + dx] == 0:

            vx = np.sum(sobel_x[y][x]) / 3  # promediamos los tres componentes del gradiente
            vy = np.sum(sobel_y[y][x]) / 3

            p = vx ** 2 + vy ** 2
            if p > max_grad:  # buscamos el mayor gradiente en norma
                max_grad = p
                max_grad_value = vx, vy

    return max_grad, max_grad_value

def getTotalSum(imagen,square_size,x,y,px,py):
    terms = []
    for yi in range(-square_size // 2, square_size // 2):
        for xi in range(-square_size // 2, square_size // 2):
            for cmp in range(3):
                patch = int(imagen[y + yi][x + xi][cmp])
                original = int(imagen[py + yi][px + xi][cmp])
                terms.append((patch - original) ** 2)
    return sum(terms), terms[-1]

def copyPattern(imagen,square_size,px,py,bx,by,c,mask):
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

def getBorderNormal(cnts,contorno):
    n = len(cnts[contorno])
    border_normal = []
    for i in range(n):
        dx = cnts[contorno][i][0][0] - cnts[contorno][(i - 1) % n][0][0]
        dy = cnts[contorno][i][0][1] - cnts[contorno][(i - 1) % n][0][1]
        border_normal.append((dy, -dx))
        # esta formula nos da la normal. no le damos importancia a la orientacion
    return border_normal.copy()
