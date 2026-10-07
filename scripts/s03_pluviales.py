"""Lámina S03 - AGUAS PLUVIALES: planta de techo y planta del nivel 1 a 1:100, detalle de canoa,
caja pluvial y descarga a cuneta, áreas tributarias, simbología y notas.

Decisiones del usuario: aguas pluviales a la cuneta pública; canoas en los bordes frontal y posterior
con 2 bajantes cada una (uno en cada extremo) conducidos a la cuneta del frente; bajantes frontales
ocultos en el N1; canoas hacia los patios P1 y P2; canoas y bajantes metálicos en negro; detalle de
canoa en esta lámina. Cubierta de la C04 (lámina cal. 26, dos aguas, 13 %, alero +9,20, cumbrera
+10,70 en y = 13,62). Caja pluvial, cajas de registro de 30 x 30 y malla protectora de la referencia
[PR]. Trazado bajo el N1 coordinado con S01 rev1, S02 rev1, E01 y C01 (placas F1/F2 de 1,65 m).
"""
import ezdxf

import cadlib as cl
import hoja as H
import sanit as S

REV = "rev0"
OUT = cl.ROOT / "planos" / "S03_pluviales"
NAME = f"SR-S03_PLUVIALES_{REV}"
LAYOUT = "S03-PLUVIALES"
W = 9.0
EY0, EY1, YC = 2.06, 25.18, 13.62                 # envolvente y cumbrera
P1x, P1y = (1.47, 8.85), (7.76, 10.26)
P2x, P2y = (4.81, 8.85), (16.98, 19.48)
CAN = 0.20                                          # ancho de canoa (PD)

doc = cl.new_doc()
msp = doc.modelspace()
for name, col, lw, lt in S.LAYERS:
    if name not in doc.layers:
        doc.layers.add(name, color=col, linetype=lt, lineweight=lw)
for name, col, lw, lt in (("S-TECHO", 7, 35, "Continuous"), ("S-CUMB", 8, 25, "DASHDOT")):
    if name not in doc.layers:
        doc.layers.add(name, color=col, linetype=lt, lineweight=lw)
# base: N1 aprobado (A2 rev3) y ejes / lindero para la planta de techo (A4 rev4)
for e in ezdxf.readfile(S.SRC["N1"]).modelspace():
    if e.dxftype() in ("TEXT", "MTEXT"):
        t = e.dxf.text if e.dxftype() == "TEXT" else e.text
        if "TANQUE SÉPTICO" in t:
            continue
    if e.dxf.layer in S.KEEP:
        msp.add_entity(e.copy())
for e in ezdxf.readfile(S.SRC["N3"]).modelspace():
    if e.dxf.layer in ("A-EJES", "A-EJES-TXT", "T-LINDERO"):
        c = e.copy()
        c.translate(0, S.OFF["N2"], 0)
        msp.add_entity(c)
for name in S.GRIS:
    if name in doc.layers:
        doc.layers.get(name).color = 8


def bp(L, x, y, tag=None, dx=0.0, dy=0.0):
    """Bajante pluvial: doble círculo; rótulo opcional."""
    cx, cy = L.Q(x, y)
    msp.add_circle((cx, cy), 0.11, dxfattribs={"layer": "S-AP"})
    msp.add_circle((cx, cy), 0.05, dxfattribs={"layer": "S-AP"})
    if tag:
        L.label(tag, x, y, dx, dy)


def flecha(L, x, y, d, largo=1.2, txt=None):
    """Flecha de pendiente en planta (d = +1 hacia el fondo, -1 hacia el frente)."""
    a, b = L.Q(x, y), L.Q(x, y + d * largo)
    msp.add_line(a, (b[0] - d * 0.25, b[1]), dxfattribs={"layer": "S-TXT"})
    h = msp.add_hatch(color=7, dxfattribs={"layer": "S-TXT"})
    h.paths.add_polyline_path([b, (b[0] - d * 0.28, b[1] + 0.09), (b[0] - d * 0.28, b[1] - 0.09)])
    if txt:
        L.text(txt, x + 0.22, y + d * largo / 2, S.TH, "MIDDLE_CENTER")


# ================================================================ planta de techo
T = S.Lv(msp, "N2")
T.rect(0.0, EY0, W, EY1, "S-TECHO")
for (x0, x1), (y0, y1), tag in ((P1x, P1y, "PATIO P1"), (P2x, P2y, "PATIO P2")):
    T.rect(x0, y0, x1, y1, "S-TECHO")
    msp.add_line(T.Q(x0, y0), T.Q(x1, y1), dxfattribs={"layer": "S-FINO"})
    msp.add_line(T.Q(x0, y1), T.Q(x1, y0), dxfattribs={"layer": "S-FINO"})
    T.text(tag, (x0 + x1) / 2 + 0.30, (y0 + y1) / 2, S.TH, "MIDDLE_CENTER")
    T.text("(ABIERTO)", (x0 + x1) / 2 + 0.05, (y0 + y1) / 2, 0.13, "MIDDLE_CENTER")
e = msp.add_line(T.Q(0.0, YC), T.Q(W, YC), dxfattribs={"layer": "S-CUMB"})
e.dxf.ltscale = 0.03
T.text("CUMBRERA +10.70", 0.55, YC + 0.12, 0.15, "MIDDLE_LEFT", rot=90.0)
# canoas (doble línea)
T.rect(0.0, EY0 - CAN, W, EY0, "S-AP")                         # frontal
T.rect(0.0, EY1, W, EY1 + CAN, "S-AP")                         # posterior
T.rect(P1x[0], P1y[1] - CAN, P1x[1], P1y[1], "S-AP")           # hacia P1
T.rect(P2x[0], P2y[0], P2x[1], P2y[0] + CAN, "S-AP")           # hacia P2
# bajantes pluviales
BPS = {"BP-1": (0.24, EY0 - 0.10), "BP-2": (8.76, EY0 - 0.10), "BP-3": (8.76, EY1 + 0.10),
       "BP-4": (0.24, EY1 + 0.10), "BP-5": (8.72, P1y[1] - 0.10), "BP-6": (8.72, P2y[0] + 0.10)}
lab_t = {"BP-1": (0.70, -0.75), "BP-2": (-0.70, -0.75), "BP-3": (-0.70, 0.75), "BP-4": (0.70, 0.75),
         "BP-5": (-0.55, -0.80), "BP-6": (-0.55, 0.80)}
for k, (x, y) in BPS.items():
    bp(T, x, y, k, *lab_t[k])
# pendientes de la cubierta (13 %)
flecha(T, 4.5, 6.6, -1, 1.8, "13 %")
flecha(T, 0.75, 9.5, -1, 1.8, "13 %")
flecha(T, 4.5, 13.0, -1, 1.6, "13 %")
flecha(T, 6.8, 14.3, +1, 1.6, "13 %")
flecha(T, 2.5, 15.5, +1, 1.8, "13 %")
flecha(T, 6.0, 21.0, +1, 1.8, "13 %")
# pendiente de las canoas hacia los bajantes
for x0, x1, y in ((3.6, 1.2, EY0 - 0.55), (5.4, 7.8, EY0 - 0.55), (3.6, 1.2, EY1 + 0.55), (5.4, 7.8, EY1 + 0.55),
                  (4.0, 7.6, P1y[1] - 0.45), (6.2, 7.8, P2y[0] + 0.45)):
    a, b = T.Q(x0, y), T.Q(x1, y)
    msp.add_line(a, b, dxfattribs={"layer": "S-FINO"})
    s = 1 if b[1] > a[1] else -1
    h = msp.add_hatch(color=7, dxfattribs={"layer": "S-FINO"})
    h.paths.add_polyline_path([b, (b[0] - 0.07, b[1] - s * 0.22), (b[0] + 0.07, b[1] - s * 0.22)])
T.text("CANOA FRONTAL (DET. 1) - PEND. PD", 4.5, EY0 - 0.80, S.TH, "MIDDLE_CENTER", rot=90.0)
T.text("CANOA POSTERIOR (DET. 1) - PEND. PD", 4.5, EY1 + 0.80, S.TH, "MIDDLE_CENTER", rot=90.0)
T.text("CANOA HACIA P1", 3.0, P1y[1] - 0.75, 0.14, "MIDDLE_CENTER", rot=90.0)
T.text("CANOA HACIA P2", 5.9, P2y[0] + 0.75, 0.14, "MIDDLE_CENTER", rot=90.0)
T.text("LÁMINA CAL. 26 (C04)", 3.2, 5.0, S.TH)
T.text("ALERO +9.20", 7.6, EY0 + 0.45, 0.14)
T.text("ALERO +9.20", 7.6, EY1 - 0.45, 0.14, "MIDDLE_RIGHT")
T.text("BORDE +10.26", 2.2, P1y[1] + 0.40, 0.13)
T.text("BORDE +10.26", 6.0, P2y[0] - 0.40, 0.13, "MIDDLE_RIGHT")

# ================================================================ nivel 1: colectores y cajas
N = S.Lv(msp, "N1")
N.text("PATIO POSTERIOR - JARDÍN SECO", 4.50, 27.95, 0.13, "MIDDLE_CENTER", rot=90.0)
for k, (x, y) in BPS.items():
    bp(N, x, y)
CR = {"CR-P1": (0.30, 0.70), "CR-P2": (8.60, 0.70), "CR-P3": (8.55, 26.05), "CR-P4": (0.85, 26.05),
      "CR-P5": (8.55, 9.00), "CR-P6": (8.55, 17.90), "CR-P7": (0.85, 21.00), "CR-P8": (0.85, 13.40),
      "CR-P9": (0.85, 6.30)}
for k, c in CR.items():
    N.caja(*c, a=0.30, txt="")
h = 0.15
# colector este: BP-3 -> CR-P3 -> CR-P6 (+BP-6) -> CR-P5 (+BP-5) -> CR-P2 (+BP-2) -> cuneta
N.pipe([BPS["BP-3"], (8.70, 26.05)], "S-AP")
N.pipe([(8.55, 26.05 - h), (8.55, 17.90 + h)], "S-AP")
N.pipe([BPS["BP-6"], (8.62, 17.90 - h)], "S-AP")
N.pipe([(8.55, 17.90 - h), (8.55, 9.00 + h)], "S-AP")
N.pipe([BPS["BP-5"], (8.62, 9.00 + h)], "S-AP")
N.pipe([(8.55, 9.00 - h), (8.60, 0.70 + h)], "S-AP")
N.pipe([BPS["BP-2"], (8.70, 0.70 + h)], "S-AP")
N.pipe([(8.60, 0.70 - h), (8.60, -1.10)], "S-AP")
# colector oeste: BP-4 -> CR-P4 -> CR-P7 -> CR-P8 -> CR-P9 -> CR-P1 (+BP-1) -> cuneta
N.pipe([BPS["BP-4"], (0.70, 26.05)], "S-AP")
N.pipe([(0.85, 26.05 - h), (0.85, 21.00 + h), ], "S-AP")
N.pipe([(0.85, 21.00 - h), (0.85, 13.40 + h)], "S-AP")
N.pipe([(0.85, 13.40 - h), (0.85, 6.30 + h)], "S-AP")
N.pipe([(0.85, 6.30 - h), (0.85, 3.20), (0.30, 0.70 + h)], "S-AP")
N.pipe([BPS["BP-1"], (0.36, 0.70 + h)], "S-AP")
N.pipe([(0.30, 0.70 - h), (0.30, -1.10)], "S-AP")
for x in (0.30, 8.60):                                            # flechas de descarga
    a = N.Q(x, -1.10)
    hh = msp.add_hatch(color=7, dxfattribs={"layer": "S-AP"})
    hh.paths.add_polyline_path([(a[0] - 0.25, a[1]), (a[0], a[1] + 0.09), (a[0], a[1] - 0.09)])
N.text("A CUNETA (DET. 3)", 0.50, -1.30, 0.15, "MIDDLE_LEFT", rot=90.0)
N.text("A CUNETA (DET. 3)", 8.40, -1.30, 0.15, "MIDDLE_RIGHT", rot=90.0)
# rótulos
N.label("CR-P4", 0.85, 26.20, 0.55, 0.40)
N.label("CR-P7", 0.85, 21.15, 0.45, 0.35)
N.label("CR-P8", 0.85, 13.55, 0.45, 0.35)
N.label("CR-P9", 0.85, 6.45, 0.45, 0.35)
N.label("CR-P1", 0.30, 0.85, 0.55, 0.50)
N.label("CR-P3", 8.55, 26.20, -0.45, 0.40)
N.label("CR-P6", 8.55, 18.05, -0.45, 0.40)
N.label("CR-P5", 8.55, 8.85, -0.45, -0.40)
N.label("CR-P2", 8.60, 0.85, -0.55, 0.50)
N.label("BP-6", 8.72, P2y[0] + 0.10, -0.45, -0.60)
N.label("BP-5", 8.72, P1y[1] - 0.10, -0.45, 0.50)
N.label("BP-1 OCULTO EN MURO (PD)", 0.24, EY0 - 0.10, 1.70, 0.35)
N.label("BP-2 OCULTO EN MURO (PD)", 8.76, EY0 - 0.10, -0.66, 0.64)
N.text("COLECTOR OESTE Ø 4\" (PD)", 1.05, 8.70, S.TH)
N.text("COLECTOR ESTE Ø 4\" (PD)", 8.30, 12.00, S.TH)

# ================================================================ hoja
psp = doc.layouts.new(LAYOUT)
psp.page_setup(size=(cl.A1_W, cl.A1_H), margins=(0, 0, 0, 0), units="mm")
doc.layouts.set_active_layout(LAYOUT)
cl.frame(psp)


def vp(center, size, scale, mc):
    v = psp.add_viewport(center=center, size=size, view_center_point=mc,
                         view_height=size[1] * scale / 1000.0, dxfattribs={"layer": "A-VIEWPORT"})
    v.dxf.flags = v.dxf.flags | 16384


PX = 186.0
for lv, yc, title in (("N2", 512.0, "AGUAS PLUVIALES - PLANTA DE TECHO"),
                      ("N1", 362.0, "AGUAS PLUVIALES - NIVEL 1")):
    vp((PX, yc), (316.0, 136.0), 100, (14.8, 3.75 + S.OFF[lv]))
    cl.text(psp, title, (30.0, yc - 68.0), 4.5, "A-TITULOS", "TOP_LEFT")
    cl.text(psp, "Esc. 1:100", (30.0, yc - 74.5), 2.5, "A-TEXTO", "TOP_LEFT")


def L(a, b, layer="S-DET"):
    return psp.add_line(a, b, dxfattribs={"layer": layer})


def R(x0, y0, x1, y1, layer="S-DET"):
    return psp.add_lwpolyline([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], close=True,
                              dxfattribs={"layer": layer})


def Tx(s, p, h=1.7, al="MIDDLE_LEFT", rot=0.0):
    cl.text(psp, s, p, h, "A-TEXTO", al, rot)


def hatch(pts, pattern="ANSI31", sc=0.6, color=8):
    hh = psp.add_hatch(color=color, dxfattribs={"layer": "S-FINO"})
    if pattern == "SOLID":
        hh.set_solid_fill(color=color)
    else:
        hh.set_pattern_fill(pattern, scale=sc)
    hh.paths.add_polyline_path(pts)


def leader(a, b, s, h=1.5):
    L(a, b, "S-FINO")
    Tx(s, (b[0] + (1.0 if b[0] >= a[0] else -1.0), b[1]), h, "MIDDLE_LEFT" if b[0] >= a[0] else "MIDDLE_RIGHT")


def dim_h(x0, x1, y, txt):
    L((x0, y), (x1, y), "S-FINO")
    for x in (x0, x1):
        L((x - 0.6, y - 0.6), (x + 0.6, y + 0.6), "S-FINO")
        L((x, y - 1.2), (x, y + 1.2), "S-FINO")
    Tx(txt, ((x0 + x1) / 2, y + 1.3), 1.5, "BOTTOM_CENTER")


def dim_v(x, y0, y1, txt, side=1):
    L((x, y0), (x, y1), "S-FINO")
    for y in (y0, y1):
        L((x - 0.6, y - 0.6), (x + 0.6, y + 0.6), "S-FINO")
        L((x - 1.2, y), (x + 1.2, y), "S-FINO")
    Tx(txt, (x + 1.3 * side, (y0 + y1) / 2), 1.5, "MIDDLE_LEFT" if side > 0 else "MIDDLE_RIGHT")


def flecha_p(p, d, size=1.8):
    dx, dy = d
    b = (p[0] - dx * size, p[1] - dy * size)
    hh = psp.add_hatch(color=7, dxfattribs={"layer": "S-DET"})
    hh.paths.add_polyline_path([p, (b[0] - dy * size * 0.35, b[1] + dx * size * 0.35),
                                (b[0] + dy * size * 0.35, b[1] - dx * size * 0.35)])


# ---------------------------------------------------------------- detalle 1: canoa (sección)
cl.text(psp, "DETALLE 1 - CANOA (SECCIÓN TÍPICA)", (30.0, 280.0), 3.2, "A-TITULOS", "TOP_LEFT")
cl.text(psp, "Esc. 1:10 - FRONTAL, POSTERIOR Y HACIA PATIOS", (30.0, 275.0), 2.0, "A-TEXTO", "TOP_LEFT")
k1, sx, sz = 100.0, 140.0, 200.0                    # 1:10; s = 0 cara exterior del muro; z = 9.00 en sz


def C(s, z):
    return (sx + s * k1, sz + (z - 9.00) * k1)


# muro / forro y viga de corona
R(*C(-0.15, 8.55), *C(0.0, 8.80), "S-DET")
hatch([C(-0.15, 8.55), C(0.0, 8.55), C(0.0, 8.80), C(-0.15, 8.80)], "ANSI31", 0.5)
R(*C(-0.13, 8.80), *C(-0.03, 9.00), "S-DET")                      # V1 4x8"
L(C(-0.13, 8.81), C(-0.03, 8.99), "S-FINO")
L(C(-0.13, 8.99), C(-0.03, 8.81), "S-FINO")
# cercha: cordón inferior y superior
L(C(-0.60, 9.00), C(-0.03, 9.00), "S-DET")
L(C(-0.60, 9.06), C(-0.03, 9.06), "S-DET")
L(C(-0.60, 9.10 + 0.13 * 0.57), C(-0.03, 9.10), "S-DET")
L(C(-0.60, 9.16 + 0.13 * 0.57), C(-0.03, 9.16), "S-DET")
for sc in (-0.40, -0.16):                                            # clavadores RT 2x4"
    z0 = 9.16 + 0.13 * (-sc - 0.03)
    R(*C(sc - 0.025, z0), *C(sc + 0.025, z0 + 0.10), "S-DET")
# lámina de cubierta (cal. 26), prolonga 0.10 sobre la canoa
zl = lambda s: 9.27 + 0.13 * (-s)
psp.add_lwpolyline([C(-0.60, zl(-0.60)), C(0.10, zl(0.10))], dxfattribs={"layer": "S-DET", "const_width": 0.5})
# precinta / tapichel
R(*C(0.0, 9.02), *C(0.02, 9.27), "S-DET")
# canoa metálica (perfil esquemático) y soporte
psp.add_lwpolyline([C(0.02, 9.25), C(0.02, 9.02), C(0.04, 9.00), C(0.20, 9.00), C(0.22, 9.02), C(0.22, 9.17),
                    C(0.25, 9.17)], dxfattribs={"layer": "S-AP", "const_width": 0.4})
psp.add_lwpolyline([C(0.0, 9.10), C(0.03, 9.10), C(0.03, 8.98), C(0.23, 8.98), C(0.23, 9.15)],
                   dxfattribs={"layer": "S-DET"})
e = L(C(0.04, 9.22), C(0.22, 9.17), "S-AP")                         # malla protectora
e.dxf.linetype = "DASHED"
e.dxf.ltscale = 0.25
psp.add_lwpolyline([C(0.10, 9.00), C(0.10, 8.70)], dxfattribs={"layer": "S-AP"})
psp.add_lwpolyline([C(0.16, 9.00), C(0.16, 8.70)], dxfattribs={"layer": "S-AP"})
Tx("+9.20", (C(0.0, 9.27)[0] - 9.0, C(0.0, 9.27)[1] + 2.4), 1.5)
Tx("+9.00", (C(-0.60, 9.00)[0] - 1.0, C(-0.60, 9.00)[1]), 1.5, "MIDDLE_RIGHT")
dim_h(C(0.02, 0)[0], C(0.22, 0)[0], C(0, 8.88)[1] - 3.0, "0.20 (PD)")
dim_v(C(0.30, 0)[0], C(0, 9.00)[1], C(0, 9.17)[1], "0.15 (PD)")
leader(C(-0.30, zl(-0.30)), (C(-0.30, 0)[0] - 4, C(0, 9.55)[1]), "LÁMINA CAL. 26 (13 %)")
leader(C(-0.16, 9.25), (C(-0.16, 0)[0] - 12, C(0, 9.42)[1]), "CLAVADOR RT 2x4\" (C04)")
leader(C(-0.45, 9.10), (C(-0.60, 0)[0] - 3, C(0, 9.10)[1]), "CERCHA (C04)")
leader(C(-0.08, 8.90), (C(-0.60, 0)[0] - 3, C(0, 8.88)[1]), "VIGA V1 4x8\" (C04)")
leader(C(-0.07, 8.65), (C(-0.60, 0)[0] - 3, C(0, 8.66)[1]), "MURO / FORRO")
leader(C(0.13, 9.20), (C(0.40, 0)[0], C(0, 9.45)[1]), "MALLA PROTECTORA [PR]")
leader(C(0.22, 9.10), (C(0.40, 0)[0], C(0, 9.28)[1]), "CANOA METÁLICA, NEGRA")
leader(C(0.23, 8.99), (C(0.40, 0)[0], C(0, 8.95)[1]), "SOPORTE @ PD")
leader(C(0.13, 8.75), (C(0.40, 0)[0], C(0, 8.75)[1]), "BAJANTE METÁLICO Ø PD")
Tx("CALIBRE, DESARROLLO Y SOPORTES DE LA CANOA: PD", (30.0, 148.0), 1.6)

# ---------------------------------------------------------------- detalle 2: caja pluvial [PR]
cl.text(psp, "DETALLE 2 - CAJA PLUVIAL [PR]", (362.0, 445.0), 3.2, "A-TITULOS", "TOP_LEFT")
cl.text(psp, "S/E - INTERIOR 0.30 x 0.30 [PR]", (362.0, 440.0), 2.0, "A-TEXTO", "TOP_LEFT")
xa, ya = 400.0, 385.0                               # sección
L((xa - 30, ya + 22), (xa + 30, ya + 22), "S-DET")
for xx in range(-29, 30, 4):
    L((xa + xx, ya + 22), (xa + xx + 1.5, ya + 24.5), "S-FINO")
outer = [(xa - 18, ya - 20), (xa + 18, ya - 20), (xa + 18, ya + 19), (xa - 18, ya + 19)]
R(xa - 18, ya - 20, xa + 18, ya + 19)
R(xa - 13, ya - 15, xa + 13, ya + 16, "S-FINO")
hatch(outer + [outer[0], (xa - 13, ya - 15), (xa - 13, ya + 16), (xa + 13, ya + 16), (xa + 13, ya - 15),
               (xa - 13, ya - 15)], "AR-CONC", 0.08)
psp.add_lwpolyline([(xa - 15, ya + 22), (xa - 11, ya + 18), (xa + 11, ya + 18), (xa + 15, ya + 22)], close=True,
                   dxfattribs={"layer": "S-DET"})                     # tapa
for xx in (-8, -3, 2, 7):
    psp.add_circle((xa + xx, ya + 20), 0.5, dxfattribs={"layer": "S-DET"})
for yy in (-10, -2, 6, 14):
    for xx in (-15.5, 15.5):
        psp.add_circle((xa + xx, ya + yy), 0.5, dxfattribs={"layer": "S-DET"})
R(xa - 32, ya + 2, xa - 13, ya + 7, "S-AP")                       # entrada
flecha_p((xa - 34, ya + 4.5), (1, 0))
psp.add_circle((xa, ya - 11), 3.0, dxfattribs={"layer": "S-AP"})  # salida
psp.add_arc((xa, ya - 11), 2.0, 200, 340, dxfattribs={"layer": "S-AP"})
leader((xa, ya + 21), (xa + 24, ya + 30), "TAPA ARMADA VAR. #2 @0.15 A.D.")
leader((xa + 15.5, ya + 6), (xa + 24, ya + 6), "VAR. #3 @0.17 A.D.")
leader((xa + 2.5, ya - 12), (xa + 24, ya - 16), "TUBO PVC Ø INDICADO")
Tx("SECCIÓN", (xa, ya - 26), 1.8, "MIDDLE_CENTER")
xb, yb = 500.0, 385.0                               # planta
R(xb - 18, yb - 18, xb + 18, yb + 18)
R(xb - 13, yb - 13, xb + 13, yb + 13, "S-FINO")
for a, b in (((xb - 13, yb + 13), (xb - 3, yb - 13)), ((xb + 13, yb + 13), (xb + 3, yb - 13))):
    L(a, b, "S-FINO")
L((xb - 3, yb - 13), (xb + 3, yb - 13), "S-FINO")
R(xb - 34, yb - 2.5, xb - 13, yb + 2.5, "S-AP")
R(xb - 2.5, yb - 34, xb + 2.5, yb - 13, "S-AP")
R(xb - 2.5, yb + 13, xb + 2.5, yb + 30, "S-AP")
flecha_p((xb - 34, yb), (1, 0))
flecha_p((xb, yb + 32), (0, -1))
flecha_p((xb, yb - 36), (0, -1))
Tx("ENTRADA", (xb - 34, yb + 4.5), 1.4)
Tx("BAJANTE", (xb + 4, yb + 26), 1.4)
Tx("SALIDA", (xb + 4, yb - 30), 1.4)
Tx("PLANTA", (xb, yb - 42), 1.8, "MIDDLE_CENTER")

# ---------------------------------------------------------------- detalle 3: descarga a cuneta
cl.text(psp, "DETALLE 3 - DESCARGA A CUNETA (ESQUEMÁTICO)", (362.0, 325.0), 3.2, "A-TITULOS", "TOP_LEFT")
cl.text(psp, "S/E", (362.0, 320.0), 2.0, "A-TEXTO", "TOP_LEFT")
yg = 285.0
X6 = 332.0
L((X6 + 40, yg), (X6 + 165, yg), "S-DET")                                     # terreno / retiro
L((X6 + 165, yg), (X6 + 165, yg + 2), "S-DET")
L((X6 + 165, yg + 2), (X6 + 225, yg + 2), "S-DET")                            # acera
L((X6 + 225, yg + 2), (X6 + 225, yg - 10), "S-DET")                           # cordón
psp.add_lwpolyline([(X6 + 225, yg - 10), (X6 + 232, yg - 14), (X6 + 250, yg - 14), (X6 + 262, yg - 9)], dxfattribs={"layer": "S-DET"})
L((X6 + 262, yg - 9), (X6 + 300, yg - 9), "S-DET")                             # calzada
hatch([(X6 + 165, yg + 2), (X6 + 225, yg + 2), (X6 + 225, yg - 6), (X6 + 165, yg - 6)], "AR-CONC", 0.06)
R(X6 + 55, yg - 22, X6 + 70, yg, "S-DET")                                     # CR frontal
hatch([(X6 + 55, yg - 22), (X6 + 70, yg - 22), (X6 + 70, yg), (X6 + 55, yg)], "ANSI31", 0.4)
R(X6 + 57, yg - 20, X6 + 68, yg, "S-FINO")
psp.add_lwpolyline([(X6 + 68, yg - 16), (X6 + 225, yg - 11.5)], dxfattribs={"layer": "S-AP", "const_width": 0.6})
flecha_p((X6 + 229, yg - 11.4), (1, 0))
L((X6 + 165, yg + 8), (X6 + 165, yg - 26), "S-FINO")
Tx("LÍNEA DE PROPIEDAD", (X6 + 166, yg + 9), 1.4)
Tx("RETIRO FRONTAL (ZACATE BLOCK)", (X6 + 95, yg + 3), 1.5)
Tx("ACERA", (X6 + 195, yg + 5), 1.5, "MIDDLE_CENTER")
Tx("CUNETA", (X6 + 241, yg - 18), 1.5, "MIDDLE_CENTER")
Tx("CR-P1 / CR-P2 (DET. 2)", (X6 + 62.5, yg - 27), 1.5, "MIDDLE_CENTER")
leader((X6 + 140, yg - 15.3), (X6 + 140, yg - 32), "TUBO PVC Ø 4\" (PD), PENDIENTE PD")
Tx("SALIDA AL CORDÓN Y CUNETA SEGÚN DISPOSICIÓN MUNICIPAL (PD).", (X6 + 40, yg - 40), 1.6)

# ---------------------------------------------------------------- áreas tributarias
X3 = 362.0
cl.text(psp, "ÁREAS TRIBUTARIAS DE CUBIERTA (PROYECCIÓN HORIZONTAL)", (X3, 580.0), 3.0, "A-TITULOS", "TOP_LEFT")
A_P1 = (P1x[1] - P1x[0]) * (YC - P1y[1])
A_P2 = (P2x[1] - P2x[0]) * (P2y[0] - YC)
A_FR = W * (YC - EY0) - (P1x[1] - P1x[0]) * (P1y[1] - P1y[0]) - A_P1
A_PO = W * (EY1 - YC) - (P2x[1] - P2x[0]) * (P2y[1] - P2y[0]) - A_P2
rows = [["CANOA", "ÁREA (m²)", "BAJANTES", "m² POR BAJANTE"],
        ["FRONTAL", f"{A_FR:.2f}", "BP-1, BP-2", f"{A_FR / 2:.2f}"],
        ["HACIA P1", f"{A_P1:.2f}", "BP-5", f"{A_P1:.2f}"],
        ["HACIA P2", f"{A_P2:.2f}", "BP-6", f"{A_P2:.2f}"],
        ["POSTERIOR", f"{A_PO:.2f}", "BP-3, BP-4", f"{A_PO / 2:.2f}"],
        ["TOTAL CUBIERTA", f"{A_FR + A_P1 + A_P2 + A_PO:.2f}", "6", ""]]
y = cl.table(psp, X3, 573.0, [40, 30, 34, 36], rows, row_h=6.3, h=2.0,
             aligns=["MIDDLE_LEFT", "MIDDLE_CENTER", "MIDDLE_CENTER", "MIDDLE_CENTER"])
cl.text(psp, "ÁREAS CALCULADAS CON LA GEOMETRÍA DE LA C04 (CUMBRERA EN y = 13.62). LOS PATIOS P1 (18.45 m²) Y "
        "P2 (10.10 m²)", (X3, y - 2.5), 1.6, "A-TEXTO", "TOP_LEFT")
cl.text(psp, "SON ABIERTOS: LA LLUVIA DIRECTA CAE SOBRE LA GRAVA DEL NIVEL 1.", (X3, y - 5.0), 1.6, "A-TEXTO",
        "TOP_LEFT")

# ---------------------------------------------------------------- simbología
y = S.cuadro_simbologia(psp, 530.0, 580.0, [
    ("CAN", "CANOA METÁLICA (DET. 1)"),
    ("BP", "BAJANTE PLUVIAL (BP-n)"),
    ("AP", "COLECTOR PLUVIAL ENTERRADO (PVC)"),
    ("CR", "CAJA PLUVIAL 0.30 x 0.30 (DET. 2) [PR]"),
    ("PEND", "PENDIENTE DE CUBIERTA / CANOA")], w_txt=78.0, row_h=6.0, title="SIMBOLOGÍA")

# ---------------------------------------------------------------- notas
yS = 520.0
cl.text(psp, "NOTAS:", (X3, yS), 3.5, "A-TITULOS", "TOP_LEFT")
notas = [
    "TODAS LAS MEDIDAS ESTÁN DADAS EN METROS, SALVO INDICACIÓN CONTRARIA. [PR]",
    "LAS AGUAS PLUVIALES SE DIRIGEN HACIA LA CUNETA PÚBLICA DEL FRENTE. [PR] NO SE CONECTAN AL TANQUE "
    "SÉPTICO NI AL DRENAJE (S02).",
    "CUBIERTA SEGÚN LA C04: LÁMINA CAL. 26 A DOS AGUAS, PENDIENTE 13 %, ALERO +9.20 Y CUMBRERA +10.70.",
    "CANOAS FRONTAL Y POSTERIOR CON DOS BAJANTES CADA UNA, UNO EN CADA EXTREMO; CANOAS HACIA LOS PATIOS "
    "P1 Y P2 CON UN BAJANTE CADA UNA, EN EL EXTREMO ESTE.",
    "CANOAS Y BAJANTES VISIBLES METÁLICOS, ACABADO NEGRO (A5). BAJANTES FRONTALES BP-1 Y BP-2 OCULTOS "
    "EN EL MURO FRONTAL DEL NIVEL 1 (PD).",
    "LAS CANOAS TENDRÁN MALLA PROTECTORA PARA EVITAR EL ACCESO DE BASURA. [PR]",
    "DIRIGIR LAS PENDIENTES HACIA BAJANTES O CANOAS; EVITAR DEPRESIONES QUE PROVOQUEN EMPOZAMIENTOS. [PR]",
    "DIÁMETROS DE BAJANTES Y COLECTORES, PENDIENTES DE CANOAS Y COLECTORES, CALIBRE Y DESARROLLO DE LAS "
    "CANOAS: PD, SEGÚN CÁLCULO HIDRÁULICO.",
    "COLECTORES ENTERRADOS DE PVC CON CAJAS PLUVIALES DE 0.30 x 0.30 (DETALLE 2) AL PIE DE CADA BAJANTE Y "
    "EN LOS CAMBIOS DE DIRECCIÓN. [PR]",
    "COLECTOR OESTE POR EL PASILLO PEATONAL, ENTRE LOS ALIMENTADORES ELÉCTRICOS (E01) Y LA TUBERÍA DE AGUA "
    "POTABLE (S01); CRUZA BAJO LOS DUCTOS ELÉCTRICOS FRENTE A CR-P9 (PD).",
    "COLECTOR ESTE JUNTO AL MURO D; CRUZA LOS RAMALES SANITARIOS DE LA SUITE 2 (S02) ENTRE CR-P6 Y CR-P5 "
    "(PROFUNDIDADES RELATIVAS PD).",
    "LAS TUBERÍAS PASAN SOBRE LAS PLACAS DE CIMENTACIÓN SIN ATRAVESAR PEDESTALES; CRUCES CON VIGAS RIOSTRA "
    "CON CAMISA (PD). LAS CAJAS SE UBICAN FUERA DE LAS PLACAS (C01).",
    "DESCARGA A LA CUNETA (DETALLE 3): UBICACIÓN, FORMA DE CONEXIÓN Y PERMISO SEGÚN LA MUNICIPALIDAD (PD).",
    "LIMPIAR CANOAS, MALLAS Y CAJAS PLUVIALES PERIÓDICAMENTE.",
]
cl.notes_block(psp, X3, yS - 6, [f"{i}.- {t}" for i, t in enumerate(notas, 1)] + [cl.NOTA_PR], 1.9, 335)

H.titleblock(doc, psp, "S03", "AGUAS PLUVIALES",
             ["PLANTA DE TECHO.", "PLANTA DEL NIVEL 1.", "DETALLE DE CANOA.", "CAJA PLUVIAL Y DESCARGA",
              "A CUNETA. ÁREAS TRIBUTARIAS.", "SIMBOLOGÍA Y NOTAS."],
             [("0", "07-10-2026", "VERSIÓN DE TRABAJO PARA REVISIÓN")], escalas="1:100 / INDICADAS")

OUT.mkdir(parents=True, exist_ok=True)
doc.saveas(OUT / f"{NAME}.dxf")
cl.render_pdf(doc, LAYOUT, OUT / f"{NAME}.pdf")
print("DXF:", OUT / f"{NAME}.dxf")
