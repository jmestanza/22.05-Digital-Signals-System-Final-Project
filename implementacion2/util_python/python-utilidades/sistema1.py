import sympy as sp
import numpy as np

def get_rational_coeffs(expr,var):
    expr = sp.expand(expr)
    #print(expr)
    num, denom = expr.as_numer_denom()

    return [sp.Poly(num, var).all_coeffs(), sp.Poly(denom, var).all_coeffs()]



vg, vout, s = sp.symbols("vg vout s")

r1, r2, r3, r4, c1, c2 = sp.symbols("r1 r2 r3 r4 c1 c2")

h = sp.solve([
    vg*(1/r2 + s * c2) - (vg-vout)*(1/(r1 + (1/(c1*s)))) ],
    (vg))

print(h)

h = get_rational_coeffs(h[vg], s)

#print(h)
factor = h[1][0]

for i in range(len(h[0])):
    h[0][i] /= factor
for i in range(len(h[1])):
    h[1][i] /= factor

print(h)