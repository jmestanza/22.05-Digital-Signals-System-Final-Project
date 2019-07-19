from numpy import exp
from numpy import array


def simplify(arr):
    simple_arr = []
    for el in arr:
        simple_arr.append(el)

    return simple_arr


def sigmoid(x):
    return 1 / (1 + exp(-x))


def windsigmoid(x):
    return 1 - sigmoid((x-5)*10)


def sigmoidToEnd(x, end):
    return 1 - sigmoid( (x-end)*50 )


def normalize(input):
    maxval = 0

    for vi in input:
        maxval = max(maxval , abs(vi))

    for i in range(len(input)):
        input[i] /= maxval

    suma = 0
    for vi in input:
        suma += vi
    suma /= len(input)
    for i in range(len(input)):
        input[i] -= suma

    return input
