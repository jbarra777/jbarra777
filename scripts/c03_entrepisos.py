"""Lámina C03 - PLANTA DE ENTREPISO 1 Y 2 (nivel 2 y nivel 3, armado idéntico) y detalle.

rev1 (usuario): una sola lámina para ambos entrepisos; solo cambia la leyenda.

Secciones de la referencia (RIVERGRAND C03-C05) por indicación expresa del usuario [PR]:
viguetas de tubo rectangular 2x6" en 2,38 mm @0,60 m, lámina ondulada de hierro galvanizado,
losa colada en sitio con malla #3 electrosoldada, vigas V1 4x8" en 3,17 mm, columnas C1 6x6".
Geometría propia: marcos transversales en los ejes 1 a 6 (A-C-D), vigas V1 longitudinales en
A, C y D, bordes de vacío en el eje B; vacíos de patios P1 y P2 y de escalera (A2-A4, A11).
Paquete de entrepiso 0,30 = V1 0,20 + losa 0,10 (A6). Marco de planta de planta.py.
"""
import math

import cadlib as cl
import hoja as H
import planta as pl
from planta import P

SHEET = "C03"
NIVEL = "ENTREPISO 1: NIVEL 2 (NPT +3.00) / ENTREPISO 2: NIVEL 3 (NPT +6.00)"
REV = "rev2"
OUT = cl.ROOT / "planos" / "C03_entrepiso_n2"
NAME = f"SR-{SHEET}_ENTREPISOS_{REV}"
LAYOUT = f"{SHEET}-ENTREPISO"

W = H.W
EY0, EY1 = H.EY0, H.EY1
YA = H.EJES_Y
XA, XB, XC, XD = (H.EJES_X[k] for k in "ABCD")
TUBO = 0.15                    # C1 6x6" [PR]
BV = 0.10                      # V1 4x8" (ancho 0,10; peralte 0,20) [PR]
SEP = 0.60                     # viguetas @0,60 m [PR]
P1x, P1y = H.P1["x"], H.P1["y"]
P2x, P2y = H.P2["x"], H.P2["y"]
ESx, ESy = H.ESC["x"], H.ESC["y"]

doc = cl.new_doc()
cl.north_block(doc)
msp = doc.modelspace()
north_ang = pl.add_crtm_ucs(doc, H.FRAME)
for name, col, lw, lt in (("E-VIGA", 7, 35, "Continuous"), ("E-VIGUETA", 7, 18, "Continuous"),
                          ("E-LOSA", 7, 25, "Continuous"), ("E-VACIO", 8, 13, "Continuous"),
                          ("E-FORRO", 8, 13, "DASHED"), ("E-TXT", 7, 18, "Continuous"),
                          ("E-DET", 7, 50, "Continuous"), ("E-REF", 7, 25, "Continuous"),
                          ("E-ACERO", 7, 35, "Continuous"), ("E-TRAMA", 8, 9, "Continuous"),
                          ("E-COTA", 7, 18, "Continuous")):
    doc.layers.add(name, color=col, linetype=lt, lineweight=lw)
if "COTA-10" not in doc.dimstyles:
    cl._dimstyle(doc, "COTA-10", 10)
H.lot(msp)


def rect(x0, y0, x1, y1, layer):
    return pl.poly(msp, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], layer)


# ---------------------------------------------------------------- borde de losa y vacíos
rect(0.0, EY0, W, EY1, "E-LOSA")
VOIDS = [((P1x[0], P1y[0], P1x[1], P1y[1]), "VACÍO PATIO P1"),
         ((ESx[0], ESy[0], ESx[1], ESy[1]), "VACÍO DE ESCALERA (VER A11)"),
         ((P2x[0], P2y[0], P2x[1], P2y[1]), "VACÍO PATIO P2")]
for (x0, y0, x1, y1), lab in VOIDS:
    rect(x0, y0, x1, y1, "E-LOSA")
    pl.line(msp, (x0, y0), (x1, y1), "E-VACIO")
    pl.line(msp, (x1, y0), (x0, y1), "E-VACIO")
for (x0, y0, x1, y1), lab in VOIDS:
    xm, ym = (x0 + x1) / 2, (y0 + y1) / 2
    dx = {"P1": 0.55, "P2": -0.75}.get(lab[-2:], 0.0)
    pl.text(msp, lab, xm + dx, ym - 0.45, 0.13, "E-TXT")

# ---------------------------------------------------------------- columnas C1
COLS = [(XA, y) for y in YA.values()] + [(XD, y) for y in YA.values()] + \
       [(XC, y) for y in H.COLS.values()] + [(XC, EY0 + 0.15)]      # C-1: N2-N3 sobre VT-1
for x, y in COLS:
    pts = [P(x - TUBO / 2, y - TUBO / 2), P(x + TUBO / 2, y - TUBO / 2),
           P(x + TUBO / 2, y + TUBO / 2), P(x - TUBO / 2, y + TUBO / 2)]
    msp.add_lwpolyline(pts, close=True, dxfattribs={"layer": "E-COLUMNA"})
    ht = msp.add_hatch(color=7, dxfattribs={"layer": "E-COLUMNA"})
    ht.paths.add_polyline_path(pts)
    if x == XC:
        rect(x - 0.15, y - 0.15, x + 0.15, y + 0.15, "E-FORRO")       # forro 0,30 (A2-A4)
    pl.text(msp, "C1", x + 0.30 if x < W / 2 else x - 0.30, y - 0.32, 0.12, "E-TXT")

# ---------------------------------------------------------------- vigas V1 (doble línea)
BEAMS = []                                          # (x0, y0, x1, y1) eje de la viga


def beam_x(y, xa, xb):                              # viga a lo largo de x (eje de número)
    rect(xa, y - BV / 2, xb, y + BV / 2, "E-VIGA")
    BEAMS.append((xa, y, xb, y))


def beam_y(x, ya, yb):                              # viga a lo largo de y (eje de letra)
    rect(x - BV / 2, ya, x + BV / 2, yb, "E-VIGA")
    BEAMS.append((x, ya, x, yb))


for y in YA.values():
    beam_x(y, XA, XD)
for x in (XA, XD):
    beam_y(x, YA["1"], YA["6"])
beam_y(XC, YA["1"], YA["2"])                        # entre 2 y 3: vacío del patio P1
beam_y(XC, YA["3"], YA["6"])
beam_y(XB, YA["2"], YA["3"])                        # borde del patio P1
beam_y(XB, YA["4"], YA["5"])                        # borde del vacío de escalera

for y in (4.6, 13.3, 22.6):
    pl.text(msp, "V1", XA + 0.30, y, 0.13, "E-TXT")
    pl.text(msp, "V1", XD - 0.30, y, 0.13, "E-TXT")
for y in (4.6, 13.3, 22.6):
    pl.text(msp, "V1", XC + 0.30, y, 0.13, "E-TXT")
pl.text(msp, "V1", XB + 0.30, (YA["2"] + YA["3"]) / 2, 0.13, "E-TXT")
pl.text(msp, "V1", XB - 0.30, (YA["4"] + YA["5"]) / 2 + 0.95, 0.13, "E-TXT")
for k, y in YA.items():
    pl.text(msp, "V1", 7.70, y + (0.24 if k != "6" else -0.24), 0.13, "E-TXT")
pl.text(msp, "V1 / VT-1 EN ENTREPISO 1 (VER C05)", XC / 2, YA["1"] + 0.25, 0.11, "E-TXT", rot=90)

# ---------------------------------------------------------------- viguetas 2x6" @0,60 (en x)
def joists(xa, xb, ya, yb):
    """Viguetas en x entre las caras de las vigas xa / xb, repartidas entre los ejes ya-yb."""
    n = math.ceil((yb - ya) / SEP - 1e-6)
    for i in range(1, n):
        y = ya + i * (yb - ya) / n
        pl.line(msp, (xa + BV / 2, y), (xb - BV / 2, y), "E-VIGUETA")


ys = list(YA.values())
for ya, yb in zip(ys[:-1], ys[1:]):
    if (ya, yb) in ((YA["2"], YA["3"]), (YA["4"], YA["5"])):
        joists(XA, XB, ya, yb)                       # franja del pasillo
    else:
        joists(XA, XC, ya, yb)
        joists(XC, XD, ya, yb)


def span_arrow(xa, xb, y, label=True):
    """Flecha de sentido de apoyo de las viguetas con rótulo."""
    pl.line(msp, (xa + 0.20, y), (xb - 0.20, y), "E-TXT")
    for xe, s in ((xa + 0.20, 1), (xb - 0.20, -1)):
        pl.poly(msp, [(xe, y), (xe + s * 0.25, y - 0.07), (xe + s * 0.25, y + 0.07)], "E-TXT")
    if label:
        pl.mtext(msp, "TUBO RECTANGULAR DE\\PACERO 2x6\" EN 2,38 mm\\P@0,60 m [PR]",
                 (xa + xb) / 2, y - 1.65, 0.12, 2.6, "E-TXT", attach=5)


for ya, yb in ((YA["1"], YA["2"]), (YA["3"], YA["4"]), (YA["5"], YA["6"])):
    ym = (ya + yb) / 2 + 0.30
    span_arrow(XA, XC, ym)
    span_arrow(XC, XD, ym)
span_arrow(XA, XB, (YA["2"] + YA["3"]) / 2 - 0.55, label=False)
span_arrow(XA, XB, (YA["4"] + YA["5"]) / 2 - 0.55, label=False)
pl.text(msp, "LOSA COLADA e = 0,10 (VER DETALLE)", XC + 0.75, (YA["3"] + YA["4"]) / 2 + 1.90,
        0.12, "E-TXT")

# ---------------------------------------------------------------- ejes y cotas
H.axes(msp)
H.general_dims(msp)
pl.text(msp, "CALLE PÚBLICA", 4.5, -2.15, 0.22, "A-ESPACIOS", rot=90)
pl.mtext(msp, "COLINDANCIA", -0.35, 14.0, 0.10, 6.0, "A-TXT-50")
pl.mtext(msp, "COLINDANCIA", W + 0.35, 14.0, 0.10, 6.0, "A-TXT-50")

# ================================================================ detalles 1:10 (model space)
LOSA, VIGA, VG = 0.10, 0.20, 0.15                  # losa / V1 / vigueta 2x6"
T1, T2 = 0.00317, 0.00238


def L(a, b, layer="E-REF"):
    msp.add_line(a, b, dxfattribs={"layer": layer})


def R(x0, y0, x1, y1, layer="E-DET", hatch=None):
    pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    if hatch:
        ht = msp.add_hatch(color=7, dxfattribs={"layer": "E-TRAMA"})
        ht.paths.add_polyline_path(pts)
        ht.set_pattern_fill(hatch, scale=0.004)
    msp.add_lwpolyline(pts, close=True, dxfattribs={"layer": layer})


def tube(x0, y0, w, h, t):
    R(x0, y0, x0 + w, y0 + h, "E-DET")
    R(x0 + t * 2, y0 + t * 2, x0 + w - t * 2, y0 + h - t * 2, "E-REF")


def ddim(a, b, base, hor):
    kw = dict(dimstyle="COTA-10", dxfattribs={"layer": "E-COTA"})
    if hor:
        d = msp.add_linear_dim(base=(0, base), p1=a, p2=b, angle=0, **kw)
    else:
        d = msp.add_linear_dim(base=(base, 0), p1=a, p2=b, angle=90, **kw)
    d.render()


def dots(x0, x1, y, step):
    x = x0
    while x <= x1 + 1e-6:
        msp.add_circle((x, y), 0.0048, dxfattribs={"layer": "E-ACERO"})
        h = msp.add_hatch(color=7, dxfattribs={"layer": "E-ACERO"})
        h.paths.add_edge_path().add_arc((x, y), 0.0048, 0, 360)
        x += step


# D1: corte perpendicular a las viguetas (lámina plana, viguetas en sección, V1 en vista)
D1X, D1Y = 60.0, 0.0
LW = 1.50
R(D1X, D1Y, D1X + LW, D1Y + LOSA, "E-DET", hatch="AR-CONC")              # losa
L((D1X, D1Y + 0.004), (D1X + LW, D1Y + 0.004), "E-ACERO")                # lámina
L((D1X, D1Y + 0.055), (D1X + LW, D1Y + 0.055), "E-ACERO")                # malla #3
dots(D1X + 0.05, D1X + LW - 0.05, D1Y + 0.050, 0.15)
for xc in (0.15, 0.75, 1.35):
    tube(D1X + xc - 0.025, D1Y - VG, 0.05, VG, T2)                      # viguetas 2x6"
R(D1X, D1Y - VIGA, D1X + LW, D1Y, "E-REF")                               # V1 en vista (fondo)
ddim((D1X + LW, D1Y), (D1X + LW, D1Y + LOSA), D1X + LW + 0.08, False)
ddim((D1X + LW, D1Y - VIGA), (D1X + LW, D1Y), D1X + LW + 0.08, False)
ddim((D1X + LW, D1Y - VIGA), (D1X + LW, D1Y + LOSA), D1X + LW + 0.16, False)
ddim((D1X + 0.15, D1Y - VIGA), (D1X + 0.75, D1Y - VIGA), D1Y - VIGA - 0.06, True)
ddim((D1X + 0.75, D1Y - VIGA), (D1X + 1.35, D1Y - VIGA), D1Y - VIGA - 0.06, True)

# D2: sección A-A a lo largo de la vigueta (V1 en sección, lámina ondulada en sección)
D2X, D2Y = 60.0, -1.0
LV = 0.90
tube(D2X, D2Y - VIGA, BV, VIGA, T1)                                      # V1 4x8"
msp.add_lwpolyline([(D2X + BV, D2Y - VG), (D2X + LV, D2Y - VG), (D2X + LV, D2Y),
                    (D2X + BV, D2Y)], dxfattribs={"layer": "E-DET"})     # vigueta en vista
L((D2X + BV, D2Y - VG + 2 * T2), (D2X + LV, D2Y - VG + 2 * T2))
L((D2X + BV, D2Y - 2 * T2), (D2X + LV, D2Y - 2 * T2))
pts = [(D2X - 0.05, D2Y + LOSA), (D2X + LV, D2Y + LOSA), (D2X + LV, D2Y), (D2X - 0.05, D2Y)]
ht = msp.add_hatch(color=7, dxfattribs={"layer": "E-TRAMA"})
ht.paths.add_polyline_path(pts)
ht.set_pattern_fill("AR-CONC", scale=0.004)
msp.add_lwpolyline(pts, close=True, dxfattribs={"layer": "E-DET"})
wave = [(D2X - 0.05 + i * 0.0095, D2Y + 0.0095 - 0.0095 * math.cos(i * 0.0095 * 2 * math.pi / 0.076))
        for i in range(int((LV + 0.05) / 0.0095) + 1)]
msp.add_lwpolyline(wave, dxfattribs={"layer": "E-ACERO"})               # lámina ondulada
L((D2X - 0.05, D2Y + 0.055), (D2X + LV, D2Y + 0.055), "E-ACERO")         # malla #3
dots(D2X, D2X + LV - 0.05, D2Y + 0.050, 0.15)
msp.add_lwpolyline([(D2X + BV, D2Y - 0.04), (D2X + BV + 0.03, D2Y - 0.04),
                    (D2X + BV, D2Y - 0.01)], close=True, dxfattribs={"layer": "E-REF"})  # soldadura
ddim((D2X + LV, D2Y), (D2X + LV, D2Y + LOSA), D2X + LV + 0.08, False)
ddim((D2X + LV, D2Y - VG), (D2X + LV, D2Y), D2X + LV + 0.08, False)
ddim((D2X, D2Y - VIGA), (D2X, D2Y + LOSA), D2X - 0.10, False)
ddim((D2X, D2Y - VIGA), (D2X + BV, D2Y - VIGA), D2Y - VIGA - 0.06, True)

# ================================================================ hoja
psp = H.sheet(doc, LAYOUT, "PLANTA DE ENTREPISO", "")
H.north(psp, north_ang)
cl.view_title(psp, 35.0, 262.0, "PLANTA DE ENTREPISO 1 Y 2", NIVEL, "Esc. 1:50", 165)
cl.scale_bar(psp, 35.0, 236.0, 50, 5, 1)

y = 214.0
cl.text(psp, "SIMBOLOGÍA ELEMENTOS PORTANTES", (35.0, y), 3.5, "A-TITULOS", "TOP_LEFT")
rows = [["C1", "COLUMNA - TUBO DE ACERO 6x6\" EN 3,17 mm [PR]"],
        ["", "(EJE C FORRADA A 0,30 x 0,30)"],
        ["V1", "VIGA - TUBO DE ACERO 4x8\" EN 3,17 mm [PR]"],
        ["VT-1", "VIGA DE TRANSFERENCIA EJE 1, ENTREPISO 1 (PD)"],
        ["VG", "VIGUETA - TUBO 2x6\" EN 2,38 mm @0,60 m [PR]"],
        ["", "VACÍO (PATIO O ESCALERA)"]]
yb = cl.table(psp, 35.0, y - 6.0, [18, 140], rows, row_h=6.5, h=2.2,
              aligns=["MIDDLE_CENTER", "MIDDLE_LEFT"])
# símbolo de vacío en la última fila
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


def callout(key, target, pos, txt, h=2.0, w=72.0):
    tx, ty = tp(key, *target)
    psp.add_line(pos, (tx, ty), dxfattribs={"layer": "A-TEXTO"})
    psp.add_circle((tx, ty), 0.6, dxfattribs={"layer": "A-TEXTO"})
    cl.mtext(psp, txt, (pos[0] + 2.0, pos[1]), h, w, layer="A-TEXTO", attach=4)


vp("D1", (300.0, 222.0), (180.0, 52.0), 10, (D1X + 0.78, D1Y - 0.07))
cl.text(psp, "DETALLE DE ENTREPISO", (215.0, 190.0), 4.5, "A-TITULOS", "TOP_LEFT")
cl.text(psp, "CORTE PERPENDICULAR A LAS VIGUETAS - Esc. 1:10", (215.0, 183.5), 2.5, "A-TEXTO",
        "TOP_LEFT")
vp("D2", (300.0, 140.0), (180.0, 52.0), 10, (D2X + 0.42, D2Y - 0.07))
cl.text(psp, "SECCIÓN A-A", (215.0, 108.0), 4.5, "A-TITULOS", "TOP_LEFT")
cl.text(psp, "A LO LARGO DE LA VIGUETA - Esc. 1:10", (215.0, 101.5), 2.5, "A-TEXTO", "TOP_LEFT")

XR = 395.0
callout("D1", (D1X + 0.45, D1Y + 0.085), (XR, 246.0), "LOSA COLADA EN SITIO e = 0,10 m")
callout("D1", (D1X + 1.05, D1Y + 0.055), (XR, 238.0), "MALLA #3 ELECTROSOLDADA [PR]; SEPARACIÓN SEGÚN CÁLCULO (PD)")
callout("D1", (D1X + 1.20, D1Y + 0.004), (XR, 226.0), "LÁMINA ONDULADA DE HIERRO GALVANIZADO [PR]")
callout("D1", (D1X + 1.35, D1Y - 0.10), (XR, 216.0), "TUBO RECTANGULAR DE ACERO 2x6\" EN 2,38 mm @0,60 m [PR]")
callout("D1", (D1X + 1.05, D1Y - 0.19), (XR, 204.0), "VIGA V1 4x8\" EN 3,17 mm (EN VISTA) [PR]")
callout("D2", (D2X + 0.60, D2Y + 0.085), (XR, 164.0), "LOSA COLADA EN SITIO e = 0,10 m")
callout("D2", (D2X + 0.70, D2Y + 0.012), (XR, 154.0), "LÁMINA ONDULADA DE HIERRO GALVANIZADO [PR]")
callout("D2", (D2X + 0.50, D2Y - 0.075), (XR, 130.0), "VIGUETA 2x6\" EN 2,38 mm, A RAS DEL BORDE SUPERIOR DE LA V1")
callout("D2", (D2X + BV + 0.01, D2Y - 0.03), (XR, 142.0), "UNIÓN SOLDADA VIGUETA - VIGA SEGÚN CÁLCULO (PD)")
callout("D2", (D2X + 0.05, D2Y - 0.15), (XR, 118.0), "VIGA V1 4x8\" EN 3,17 mm [PR]")

X3 = 482.0
y = 262.0
cl.text(psp, "NOTAS:", (X3, y), 3.5, "A-TITULOS", "TOP_LEFT")
notas = [
    "TODAS LAS MEDIDAS ESTÁN DADAS EN METROS, SALVO INDICACIÓN CONTRARIA. [PR]",
    "ENTREPISO: LOSA COLADA EN SITIO DE 0,10 m CON MALLA #3 ELECTROSOLDADA SOBRE LÁMINA ONDULADA "
    "DE HIERRO GALVANIZADO, APOYADA EN VIGUETAS DE TUBO 2x6\" EN 2,38 mm. [PR]",
    "VIGUETAS EN SENTIDO TRANSVERSAL (ENTRE LAS VIGAS DE LOS EJES A, C Y D, Y A Y B EN LA FRANJA "
    "DEL PASILLO), SEPARACIÓN MÁXIMA 0,60 m REPARTIDA EN CADA PAÑO.",
    "VIGAS V1 4x8\" EN 3,17 mm EN LOS EJES 1 A 6 (MARCOS A-C-D) Y EN LOS EJES A, C Y D; EN EL EJE B "
    "COMO BORDE DE LOS VACÍOS DEL PATIO P1 Y DE LA ESCALERA. [PR]",
    "PAQUETE DE ENTREPISO 0,30 m = VIGA 0,20 + LOSA 0,10 (VER A6). LAS VIGUETAS QUEDAN A RAS DEL "
    "BORDE SUPERIOR DE LAS VIGAS.",
    "COLUMNAS C1 CONTINUAS DEL NIVEL 1 AL NIVEL 3 (VER C01 Y C05). EN EL EJE C DEL EJE 1 LA C1 "
    "ARRANCA EN EL NIVEL 2 SOBRE LA VIGA DE TRANSFERENCIA VT-1 DEL ENTREPISO 1 (DISEÑO ESPECIAL, "
    "PD); SIN COLUMNA EN EL NIVEL 1 (PORTÓN).",
    "UNIONES SOLDADAS, PERFILES DEFINITIVOS Y SEPARACIÓN DE LA MALLA SEGÚN MEMORIA DE CÁLCULO (PD).",
    "MATERIALES, PROTECCIÓN ANTICORROSIVA Y ESPECIFICACIONES SEGÚN LÁMINA C06. [PR]",
    "LAS SECCIONES DE ESTA LÁMINA SON LAS DEL PROYECTO DE REFERENCIA, POR INDICACIÓN DEL "
    "INGENIERO RESPONSABLE; NO SUSTITUYEN LA MEMORIA DE CÁLCULO.",
]
cl.notes_block(psp, X3, y - 6, [f"{i}.- {t}" for i, t in enumerate(notas, 1)] + [cl.NOTA_PR], 2.1, 222)

H.titleblock(doc, psp, SHEET, "ENTREPISO",
             ["PLANTA DE ENTREPISO 1 Y 2.", "DETALLE DE ENTREPISO.", "SECCIÓN A-A.",
              "SIMBOLOGÍA.", "NOTAS.", ""],
             [("0", "06-10-2026", "VERSIÓN DE TRABAJO PARA REVISIÓN"),
              ("1", "06-10-2026", "ENTREPISOS 1 Y 2 EN UNA SOLA LÁMINA"),
              ("2", "06-10-2026", "C1 EJE C-1 SOBRE VT-1; REFERENCIA A C06")], escalas="1:50 / INDICADAS")

OUT.mkdir(parents=True, exist_ok=True)
doc.saveas(OUT / f"{NAME}.dxf")
cl.render_pdf(doc, LAYOUT, OUT / f"{NAME}.pdf")
print("DXF:", OUT / f"{NAME}.dxf")
