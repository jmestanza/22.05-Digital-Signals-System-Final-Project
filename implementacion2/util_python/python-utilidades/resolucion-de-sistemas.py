import sympy as sp


def get_rational_coeffs(expr,var):
    expr = sp.expand(expr)
    #print(expr)
    num, denom = expr.as_numer_denom()

    return [sp.Poly(num, var).all_coeffs(), sp.Poly(denom, var).all_coeffs()]



v1, v2, vx, vfeed, vout1, vout2, vout, vd, vd1, vd2, s, a0, wp = sp.symbols("v1 v2 vx vfeed vout1 vout2 vout vd vd1 vd2 s a0 wp")


r1, r2, r3, r4, r5, r6, r7, r8, r9 = sp.symbols("r1 r2 r3 r4 r5 r6 r7 r8 r9")


h = sp.solve([
    (vout2-vd-vout)/r2 - (vout1-(vout2-vd))/r1,
    vd*(a0/(1+s/wp))-vout,
    (vout1-(v1-vd1))/r3-((v1-vd1)-vx)/r4,
    vd1*(a0/(1+s/wp))-vout1,
    (vfeed-vx)/r5-(vx-(v1-vd1))/r4-(vx-(v2-vd2))/r6,
    (vx-(v2-vd2))/r6-((v2-vd2)-vout2)/r7,
    vd2*(a0/(1+s/wp))-vout2,
    vout2*(a0/(1+s/wp))-vfeed],
    (vx, vfeed, vout1, vout2, vout, vd, vd1, vd2))

print(h)

print(h[vout])

h = get_rational_coeffs(h[vout], s)
print(h)
