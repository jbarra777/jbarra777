"""Lámina C04 - PLANTA DE TECHO (estructura de cubierta), cercha típica y sección típica.

Decisiones del usuario (06-10-2026): clavadores RT 2x4" en 1,50 mm @0,90 m máx.; cerchas con
cordones 2x6" en 2,38 mm (planos) y diagonales/montantes 2x2" en 1,50 mm, peralte 0,10 en el
alero a ~1,60 en la cumbrera, montantes @~1,0 m; vigas de corona V1 4x8" a +9,00 en los ejes
1 a 6 y A, C y D (como entrepisos); cercha del eje C continua sobre el patio P1; detalle de
canoa en la lámina pluvial. Cubierta: lámina cal. 26 a dos aguas, 13 % (A5/A6).
Cerchas en x 0,30 / eje B / eje C / x 8,70 (A6). C1 y V1: secciones de la referencia [PR].
"""
import math

import cadlib as cl
import hoja as H
import planta as pl
from planta import P

REV = "rev0"
OUT = cl.ROOT / "planos" / "C04_techo"
NAME = f"SR-C04_TECHO_{REV}"
LAYOUT = "C04-TECHO"

W = H.W
EY0, EY1 = H.EY0, H.EY1
YA = H.EJES_Y
XA, XB, XC, XD = (H.EJES_X[k] for k in "ABCD")
TUBO, BV = 0.15, 0.10
PEND = 0.13
Y_CUM = (EY0 + EY1) / 2
X_CE = (0.30, XB, XC, W - 0.30)                      # cerchas (A6)
SEP_CL = 0.90                                       # clavadores @0,90 máx.
P1x, P1y = H.P1["x"], H.P1["y"]
P2x, P2y = H.P2["x"], H.P2["y"]
CAN = 0.20

doc = cl.new_doc()
cl.north_block(doc)
msp = doc.modelspace()
north_ang = pl.add_crtm_ucs(doc, H.FRAME)
for name, col, lw, lt in (("E-VIGA", 7, 35, "Continuous"), ("E-CERCHA", 7, 35, "Continuous"),
                          ("E-CLAVADOR", 7, 13, "Continuous"), ("E-CUBIERTA", 7, 25, "Continuous"),
                          ("E-CUMBRERA", 7, 18, "DASHDOT"), ("E-VACIO", 8, 13, "Continuous"),
                          ("E-PLUVIAL", 7, 18, "Continuous"), ("E-FORRO", 8, 13, "DASHED"),
                          ("E-TXT", 7, 18, "Continuous"), ("E-DET", 7, 50, "Continuous"),
                          ("E-REF", 7, 25, "Continuous"), ("E-TRAMA", 8, 9, "Continuous"),
                          ("E-COTA", 7, 18, "Continuous")):
    doc.layers.add(name, color=col, linetype=lt, lineweight=lw)
for sc in (10, 75):
    if f"COTA-{sc}" not in doc.dimstyles:
        cl._dimstyle(doc, f"COTA-{sc}", sc)
H.lot(msp)


def rect(x0, y0, x1, y1, layer):
    return pl.poly(msp, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], layer)


# ---------------------------------------------------------------- cubierta, cumbrera y patios
rect(0.0, EY0, W, EY1, "E-CUBIERTA")
pl.line(msp, (0.0, Y_CUM), (W, Y_CUM), "E-CUMBRERA", ltscale=0.02)
pl.text(msp, "CUMBRERA", 0.85, Y_CUM + 0.22, 0.13, "E-TXT", rot=90)
for (x0, x1), (y0, y1), lab in ((P1x, P1y, "PATIO P1 (ABIERTO, SIN CUBIERTA)"),
                                (P2x, P2y, "PATIO P2 (ABIERTO, SIN CUBIERTA)")):
    rect(x0, y0, x1, y1, "E-CUBIERTA")
    pl.line(msp, (x0, y0), (x1, y1), "E-VACIO")
    pl.line(msp, (x1, y0), (x0, y1), "E-VACIO")
    pl.text(msp, lab, (x0 + x1) / 2 - 1.10, (y0 + y1) / 2, 0.12, "E-TXT")

# ---------------------------------------------------------------- columnas C1 y vigas de corona V1
COLS = [(XA, y) for y in YA.values()] + [(XD, y) for y in YA.values()] + \
       [(XC, y) for y in H.COLS.values()]
for x, y in COLS:
    pts = [P(x - TUBO / 2, y - TUBO / 2), P(x + TUBO / 2, y - TUBO / 2),
           P(x + TUBO / 2, y + TUBO / 2), P(x - TUBO / 2, y + TUBO / 2)]
    msp.add_lwpolyline(pts, close=True, dxfattribs={"layer": "E-COLUMNA"})
    ht = msp.add_hatch(color=7, dxfattribs={"layer": "E-COLUMNA"})
    ht.paths.add_polyline_path(pts)
    if x == XC:
        rect(x - 0.15, y - 0.15, x + 0.15, y + 0.15, "E-FORRO")
for y in YA.values():
    rect(XA, y - BV / 2, XD, y + BV / 2, "E-VIGA")
for x in (XA, XD):
    rect(x - BV / 2, YA["1"], x + BV / 2, YA["6"], "E-VIGA")
rect(XC - BV / 2, YA["1"], XC + BV / 2, YA["2"], "E-VIGA")
rect(XC - BV / 2, YA["3"], XC + BV / 2, YA["6"], "E-VIGA")
for k, y in YA.items():
    pl.text(msp, "V1", 7.70, y + (0.24 if k != "6" else -0.24), 0.13, "E-TXT")

# ---------------------------------------------------------------- cerchas CE-1 (a lo largo de y)
for x in X_CE:
    rect(x - 0.075, EY0, x + 0.075, EY1, "E-CERCHA")
for x, dx in zip(X_CE, (0.32, 0.32, 0.32, -0.32)):
    for y in (5.0, 21.9):
        pl.text(msp, "CE-1", x + dx, y, 0.13, "E-TXT")

# ---------------------------------------------------------------- clavadores RT 2x4" @0,90 máx.
def in_patio(y):
    for (x0, x1), (y0, y1) in ((P1x, P1y), (P2x, P2y)):
        if y0 < y < y1:
            return (x0, x1)
    return None


def purlin_rows(ya, yb):
    n = math.ceil((yb - ya) / SEP_CL - 1e-6)
    return [ya + i * (yb - ya) / n for i in range(n + 1)]


ROWS = purlin_rows(EY0 + 0.05, Y_CUM - 0.10) + purlin_rows(Y_CUM + 0.10, EY1 - 0.05)
for y in ROWS:
    gap = in_patio(y)
    if gap:
        if gap[0] > 0.6:
            pl.line(msp, (0.15, y), (gap[0], y), "E-CLAVADOR")
    else:
        pl.line(msp, (0.15, y), (W - 0.15, y), "E-CLAVADOR")

# ---------------------------------------------------------------- pendientes, canoas y bajantes
def slope_arrow(x, y, d):
    """Flecha de pendiente en el sentido d (+1 hacia el fondo, -1 hacia el frente)."""
    pl.line(msp, (x, y), (x, y + d * 1.6), "E-TXT")
    ye = y + d * 1.6
    pl.poly(msp, [(x, ye), (x - 0.08, ye - d * 0.28), (x + 0.08, ye - d * 0.28)], "E-TXT")
    pl.text(msp, "PENDIENTE 13 %", x - 0.22, y + d * 0.80, 0.11, "E-TXT")


for x in (3.10, 6.70):
    slope_arrow(x, Y_CUM - 0.60, -1)
    slope_arrow(x, Y_CUM + 0.60, +1)
for y0, y1, x0, x1 in ((EY0 - CAN, EY0, 0.0, W), (EY1, EY1 + CAN, 0.0, W),
                       (P1y[1] - CAN, P1y[1], P1x[0], P1x[1]),
                       (P2y[0], P2y[0] + CAN, P2x[0], P2x[1])):
    rect(x0, y0, x1, y1, "E-PLUVIAL")
for y in (EY0 - CAN / 2, EY1 + CAN / 2):
    for x in (0.24, W - 0.24):
        msp.add_circle(P(x, y), 0.06, dxfattribs={"layer": "E-PLUVIAL"})
pl.text(msp, "CANOA Y BAJANTES (VER LÁMINA PLUVIAL)", 4.5, EY0 - 0.55, 0.12, "E-TXT", rot=90)
pl.text(msp, "CANOA Y BAJANTES (VER LÁMINA PLUVIAL)", 4.5, EY1 + 0.55, 0.12, "E-TXT", rot=90)
pl.text(msp, "CANOA HACIA P1", 6.6, P1y[1] - 0.40, 0.11, "E-TXT", rot=90)
pl.text(msp, "CANOA HACIA P2", 6.65, P2y[0] + 0.40, 0.11, "E-TXT", rot=90)
pl.mtext(msp, "CLAVADORES RT 2x4\" EN 1,50 mm\\P@0,90 m MÁX.", 2.60, 4.0, 0.12, 3.6, "E-TXT")
pl.mtext(msp, "CLAVADORES RT 2x4\" EN 1,50 mm\\P@0,90 m MÁX.", 2.60, 23.0, 0.12, 3.6, "E-TXT")

H.axes(msp)
H.general_dims(msp)
pl.text(msp, "CALLE PÚBLICA", 4.5, -2.15, 0.22, "A-ESPACIOS", rot=90)
pl.mtext(msp, "COLINDANCIA", -0.35, 14.0, 0.10, 6.0, "A-TXT-50")
pl.mtext(msp, "COLINDANCIA", W + 0.35, 14.0, 0.10, 6.0, "A-TXT-50")

# ================================================================ cercha típica (elevación 1:75)
EX = 100.0                                          # X = EX + y ; Y = nivel
ZB = 9.00                                           # cara inferior del cordón inferior
CH = 0.05                                           # cordones 2x6" planos (2" de alto)
CLV = 0.10                                          # clavador 2x4" (4" de alto)
ZT0 = ZB + 0.10                                     # cara superior del cordón superior en el alero


def ztop(y):
    return ZT0 + PEND * min(y - EY0, EY1 - y)


def eL(a, b, layer="E-DET"):
    msp.add_line((EX + a[0], a[1]), (EX + b[0], b[1]), dxfattribs={"layer": layer})


def eP(pts, layer="E-DET", close=False):
    msp.add_lwpolyline([(EX + y, z) for y, z in pts], close=close, dxfattribs={"layer": layer})


eP([(EY0, ZB), (EY1, ZB), (EY1, ZB + CH), (EY0, ZB + CH)], close=True)          # cordón inferior
eP([(EY0, ZT0), (Y_CUM, ztop(Y_CUM)), (EY1, ZT0)])                                # cordón superior
eP([(EY0, ZT0 - CH), (Y_CUM, ztop(Y_CUM) - CH), (EY1, ZT0 - CH)])
eL((EY0, ZB), (EY0, ZT0))
eL((EY1, ZB), (EY1, ZT0))
# montantes @~1,0 m y diagonales tipo Pratt (bajan hacia los apoyos)
nh = round((Y_CUM - EY0) / 1.0)
half = [EY0 + (Y_CUM - EY0) * i / nh for i in range(nh + 1)]
ps = half + [EY1 - (q - EY0) for q in reversed(half[:-1])]
ps = [q for q in ps if ztop(q) - CH - (ZB + CH) >= 0.15]
for q in ps:
    eL((q, ZB + CH), (q, ztop(q) - CH), "E-REF")
for a, b in zip(ps[:-1], ps[1:]):
    if (a + b) / 2 < Y_CUM:
        eL((a, ZB + CH), (b, ztop(b) - CH), "E-REF")
    else:
        eL((a, ztop(a) - CH), (b, ZB + CH), "E-REF")
# clavadores (en sección) y lámina
for y in ROWS:
    z = ztop(y)
    eP([(y - 0.025, z), (y + 0.025, z), (y + 0.025, z + CLV), (y - 0.025, z + CLV)], "E-REF", True)
eP([(EY0, ZT0 + CLV), (Y_CUM, ztop(Y_CUM) + CLV), (EY1, ZT0 + CLV)], "E-DET")
# vigas de corona V1 (sección) en los ejes 1 a 6
for y in YA.values():
    eP([(y - BV / 2, ZB - 0.20), (y + BV / 2, ZB - 0.20), (y + BV / 2, ZB), (y - BV / 2, ZB)],
       "E-DET", True)
    msp.add_circle((EX + y, ZB - 0.75), 0.18, dxfattribs={"layer": "E-REF"})
for k, y in YA.items():
    cl.text(msp, k, (EX + y, ZB - 0.75), 0.18, "E-TXT", "MIDDLE_CENTER")
    eL((y, ZB - 0.57), (y, ZB - 0.22), "E-REF")


def edim(a, b, base, hor, style="COTA-75"):
    kw = dict(dimstyle=style, dxfattribs={"layer": "E-COTA"})
    if hor:
        d = msp.add_linear_dim(base=(a[0], base), p1=a, p2=b, angle=0, **kw)
    else:
        d = msp.add_linear_dim(base=(base, a[1]), p1=a, p2=b, angle=90, **kw)
    d.render()


edim((EX + EY0, ZT0 + CLV), (EX + EY1, ZT0 + CLV), ztop(Y_CUM) + CLV + 0.45, True)
edim((EX + EY0, ZB), (EX + EY0, ZT0), EX + EY0 - 0.45, False)
edim((EX + Y_CUM, ZB), (EX + Y_CUM, ztop(Y_CUM)), EX + Y_CUM + 0.55, False)
for z, lab, y, al in ((ZB - 0.40, "+9.00 CARA SUPERIOR V1 / CORDÓN INFERIOR", YA["1"] + 0.6, "MIDDLE_LEFT"),
                      (ZB - 0.40, "+9.20 LÁMINA EN EL ALERO (VER NOTA 6)", YA["5"] + 0.6, "MIDDLE_LEFT"),
                      (ztop(Y_CUM) + CLV, "+10.70 LÁMINA EN LA CUMBRERA (VER NOTA 6)", Y_CUM + 1.0,
                       "MIDDLE_LEFT")):
    cl.text(msp, lab, (EX + y, z + (0.12 if z > ZB + 1 else 0.0)), 0.16, "E-TXT", al)

# ================================================================ sección típica 1:10 (perpendicular)
SX, SZ = 200.0, 0.0
T2, T15 = 0.00238, 0.0015


def sR(x0, z0, x1, z1, layer="E-DET", t=None):
    msp.add_lwpolyline([(SX + x0, SZ + z0), (SX + x1, SZ + z0), (SX + x1, SZ + z1),
                        (SX + x0, SZ + z1)], close=True, dxfattribs={"layer": layer})
    if t:
        msp.add_lwpolyline([(SX + x0 + 2 * t, SZ + z0 + 2 * t), (SX + x1 - 2 * t, SZ + z0 + 2 * t),
                            (SX + x1 - 2 * t, SZ + z1 - 2 * t), (SX + x0 + 2 * t, SZ + z1 - 2 * t)],
                           close=True, dxfattribs={"layer": "E-REF"})


HW = 0.45
sR(-HW, -0.20, HW, 0.0, "E-REF")                                   # V1 corona (en vista)
sR(-0.075, 0.0, 0.075, CH, t=T2)                                   # cordón inferior (sección)
ZM = 0.45                                                          # peralte representativo
sR(-0.025, CH, 0.025, ZM - CH, "E-REF")                            # montante 2x2" (vista)
sR(-0.075, ZM - CH, 0.075, ZM, t=T2)                               # cordón superior (sección)
sR(-HW, ZM, HW, ZM + CLV, "E-REF")                                 # clavador (vista)
# corte de interrupción en el montante
zb = 0.22
for a, b in (((-0.06, zb), (-0.01, zb + 0.02)), ((-0.01, zb + 0.02), (0.01, zb - 0.02)),
             ((0.01, zb - 0.02), (0.06, zb))):
    msp.add_line((SX + a[0], SZ + a[1]), (SX + b[0], SZ + b[1]), dxfattribs={"layer": "E-REF"})
# lámina trapezoidal (sección)
prof, x = [], -HW
while x < HW - 1e-6:
    prof += [(x, ZM + CLV), (x + 0.07, ZM + CLV), (x + 0.10, ZM + CLV + 0.035),
             (x + 0.15, ZM + CLV + 0.035), (x + 0.18, ZM + CLV)]
    x += 0.25
msp.add_lwpolyline([(SX + a, SZ + b) for a, b in prof if a <= HW + 1e-6],
                   dxfattribs={"layer": "E-DET"})


def sdim(a, b, base, hor):
    edim((SX + a[0], SZ + a[1]), (SX + b[0], SZ + b[1]), base, hor, "COTA-10")


sdim((HW, -0.20), (HW, 0.0), SX + HW + 0.07, False)
sdim((HW, ZM), (HW, ZM + CLV), SX + HW + 0.07, False)
sdim((-0.075, -0.20), (0.075, -0.20), SZ - 0.27, True)

# ================================================================ hoja
psp = H.sheet(doc, LAYOUT, "PLANTA DE TECHO", "")
H.north(psp, north_ang)
cl.view_title(psp, 35.0, 262.0, "PLANTA DE TECHO", "ESTRUCTURA DE CUBIERTA", "Esc. 1:50", 150)
cl.scale_bar(psp, 35.0, 236.0, 50, 5, 1)

y = 214.0
cl.text(psp, "SIMBOLOGÍA ELEMENTOS PORTANTES", (35.0, y), 3.5, "A-TITULOS", "TOP_LEFT")
rows = [["C1", "COLUMNA - TUBO DE ACERO 6x6\" EN 3,17 mm [PR]"],
        ["V1", "VIGA DE CORONA - TUBO 4x8\" EN 3,17 mm, +9,00 [PR]"],
        ["CE-1", "CERCHA - CORDONES 2x6\" EN 2,38 mm"],
        ["", "DIAGONALES Y MONTANTES 2x2\" EN 1,50 mm"],
        ["CL", "CLAVADOR - TUBO RT 2x4\" EN 1,50 mm @0,90 m MÁX."],
        ["", "PATIO ABIERTO (SIN CUBIERTA)"]]
yb = cl.table(psp, 35.0, y - 6.0, [18, 140], rows, row_h=6.5, h=2.2,
              aligns=["MIDDLE_CENTER", "MIDDLE_LEFT"])
cx0, cy0, cx1, cy1 = 39.0, yb + 1.2, 49.0, yb + 5.3
cl.rect(psp, cx0, cy0, cx1, cy1, "A-TEXTO")
psp.add_line((cx0, cy0), (cx1, cy1), dxfattribs={"layer": "A-TEXTO"})
psp.add_line((cx0, cy1), (cx1, cy0), dxfattribs={"layer": "A-TEXTO"})

VPS = {}


def vp(key, center, size, scale, mc):
    v = psp.add_viewport(center=center, size=size, view_center_point=mc,
                         view_height=size[1] * scale / 1000.0, dxfattribs={"layer": "A-VIEWPORT"})
    v.dxf.flags = v.dxf.flags | 16384
    VPS[key] = (center, mc, scale)


def tp(key, x, y):
    c, mc, sc = VPS[key]
    f = 1000.0 / sc
    return (c[0] + (x - mc[0]) * f, c[1] + (y - mc[1]) * f)


def callout(key, target, pos, txt, h=2.0, w=80.0):
    if key == "ST":                                 # destinos de la sección en coordenadas locales
        target = (SX + target[0], SZ + target[1])
    tx, ty = tp(key, *target)
    psp.add_line(pos, (tx, ty), dxfattribs={"layer": "A-TEXTO"})
    psp.add_circle((tx, ty), 0.6, dxfattribs={"layer": "A-TEXTO"})
    cl.mtext(psp, txt, (pos[0] + 2.0, pos[1]), h, w, layer="A-TEXTO", attach=4)


vp("EL", (378.0, 228.0), (336.0, 52.0), 75, (EX + 13.9, 9.55))
cl.text(psp, "CERCHA TÍPICA CE-1 (ELEVACIÓN)", (212.0, 198.0), 4.5, "A-TITULOS", "TOP_LEFT")
cl.text(psp, "EN x 0,30 / EJE B / EJE C / x 8,70 - Esc. 1:75", (212.0, 191.5), 2.5, "A-TEXTO",
        "TOP_LEFT")
vp("ST", (268.0, 130.0), (112.0, 112.0), 10, (SX + 0.04, SZ + 0.21))
cl.text(psp, "SECCIÓN TÍPICA DE CUBIERTA", (212.0, 68.0), 4.5, "A-TITULOS", "TOP_LEFT")
cl.text(psp, "PERPENDICULAR A LA CERCHA - Esc. 1:10", (212.0, 61.5), 2.5, "A-TEXTO", "TOP_LEFT")

XR = 336.0
callout("ST", (0.30, ZM + CLV + 0.035), (XR, 168.0), "LÁMINA ESTRUCTURAL CAL. 26, NATURAL GALVANIZADA (A5)")
callout("ST", (0.33, ZM + 0.05), (XR, 158.0), "CLAVADOR TUBO RT 2x4\" EN 1,50 mm @0,90 m MÁX.")
callout("ST", (0.05, ZM - 0.025), (XR, 148.0), "CORDÓN SUPERIOR TUBO 2x6\" EN 2,38 mm (PLANO)")
callout("ST", (0.0, 0.33), (XR, 138.0), "MONTANTES Y DIAGONALES TUBO 2x2\" EN 1,50 mm; PERALTE VARIABLE 0,10 A 1,60 m")
callout("ST", (0.05, 0.025), (XR, 124.0), "CORDÓN INFERIOR TUBO 2x6\" EN 2,38 mm (PLANO)")
callout("ST", (0.30, -0.10), (XR, 112.0), "VIGA DE CORONA V1 TUBO 4x8\" EN 3,17 mm, CARA SUPERIOR +9,00 [PR]")
cl.mtext(psp, "UNIONES SOLDADAS (CORDONES, MONTANTES, DIAGONALES, CLAVADORES Y APOYO SOBRE V1) "
         "SEGÚN MEMORIA DE CÁLCULO (PD).", (XR, 102.0), 2.0, 80.0, layer="A-TEXTO", attach=1)

X3 = 556.0
y = 262.0
cl.text(psp, "NOTAS:", (X3, y), 3.5, "A-TITULOS", "TOP_LEFT")
notas = [
    "TODAS LAS MEDIDAS ESTÁN DADAS EN METROS, SALVO INDICACIÓN CONTRARIA. [PR]",
    "CUBIERTA DE LÁMINA ESTRUCTURAL CAL. 26 A DOS AGUAS (FRENTE Y FONDO), PENDIENTE 13 %, "
    "SOBRE CLAVADORES Y CERCHAS METÁLICAS EN LA DIRECCIÓN DE LA PENDIENTE (A5, A6).",
    "CERCHAS CE-1 EN x 0,30, EJE B, EJE C Y x 8,70, APOYADAS EN LAS VIGAS DE CORONA V1 DE LOS "
    "EJES 1 A 6. LA CERCHA DEL EJE C ES CONTINUA SOBRE EL PATIO P1.",
    "VIGAS DE CORONA V1 A +9,00 EN LOS EJES 1 A 6 Y EN A, C Y D, SOBRE LAS COLUMNAS C1, IGUAL "
    "QUE EN LOS ENTREPISOS (C03). [PR]",
    "PATIOS P1 Y P2 ABIERTOS, SIN CUBIERTA. CANOAS AL FRENTE, AL FONDO Y HACIA LOS PATIOS; "
    "BAJANTES Y DETALLE DE CANOA SEGÚN LÁMINA PLUVIAL.",
    "NIVELES DE LÁMINA RESULTANTES DE LA CERCHA: +9,20 EN EL ALERO Y +10,70 EN LA CUMBRERA "
    "(A5 Y A6 INDICAN +9,00 Y +10,50). PENDIENTE DE CONFIRMAR (PD).",
    "UNIONES SOLDADAS Y VERIFICACIÓN DE PERFILES SEGÚN MEMORIA DE CÁLCULO (PD).",
    "MATERIALES, PROTECCIÓN ANTICORROSIVA Y ESPECIFICACIONES SEGÚN LÁMINA C07.",
]
cl.notes_block(psp, X3, y - 6, [f"{i}.- {t}" for i, t in enumerate(notas, 1)] + [cl.NOTA_PR], 2.0, 148)

H.titleblock(doc, psp, "C04", "TECHO",
             ["PLANTA DE TECHO.", "CERCHA TÍPICA CE-1.", "SECCIÓN TÍPICA DE CUBIERTA.",
              "SIMBOLOGÍA.", "NOTAS.", ""],
             [("0", "06-10-2026", "VERSIÓN DE TRABAJO PARA REVISIÓN")], escalas="1:50 / INDICADAS")

OUT.mkdir(parents=True, exist_ok=True)
doc.saveas(OUT / f"{NAME}.dxf")
cl.render_pdf(doc, LAYOUT, OUT / f"{NAME}.pdf")
print("DXF:", OUT / f"{NAME}.dxf")
