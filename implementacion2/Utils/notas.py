
notas = dict()

letras = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'G', 'G#']

standardA4 = 440
A0 = standardA4 / 4


factor = 2**(1/12)

for letra in letras:
    if letra == 'A':
        notas[letra] = [A0]
    else:
        notas[letra] = [anterior * factor]
    anterior = notas[letra][0]

for letra in letras:
    for i in range(10):
        notas[letra].append(notas[letra][i-1]*2)

    notas[letra].append(notas[letra][0]/2)
