"""Lámina A4 - PLANTA NIVEL 3 (tres suites).

Base: planta A-202 con los mismos ajustes aprobados en A3: accesos al final del pasillo
(ejes 2 y 5 y muro B), escalera en U, baños en línea 1.55 x 2.20 con puerta de 0.80
hacia el dormitorio, pasillo cerrado con vidrio hacia P1 y columnas sobre el eje C.
Ajuste adicional: el baño de la suite 2 se ubica sobre la zona húmeda de la cocina
del nivel 2 (alineación de instalaciones).
"""
from ezdxf.math import Vec2

import cadlib as cl
import hoja as H
import planta as pl
from planta import P

REV = "rev6"
OUT = cl.ROOT / "planos" / "A4_nivel3"
NAME = f"SR-A4_NIVEL3_{REV}"
E, I, W = H.E, H.I, H.W
XB0, XB1 = H.XB0, H.XB1
YF0, YF1, YR0, YR1 = H.YF0, H.YF1, H.YR0, H.YR1
Y2a, Y2b, Y3a, Y3b = H.Y2a, H.Y2b, H.Y3a, H.Y3b
Y4a, Y4b, Y5a, Y5b = H.Y4a, H.Y4b, H.Y5a, H.Y5b
P1, P2, ESC = H.P1, H.P2, H.ESC
X0, X1 = ESC["x"]
XC0, XC1 = X1, P2["x"][0]
NPT = "NPT +6.00"

doc = cl.new_doc()
cl.north_block(doc)
msp = doc.modelspace()
north_ang = pl.add_crtm_ucs(doc, H.FRAME)
H.lot(msp)


def wall_with_openings(axis, c0, c1, a, b, openings, windows=()):
    cuts = sorted(list(openings) + list(windows))
    pos = a
    for s0, s1 in cuts:
        if s0 > pos:
            (pl.wall(msp, pos, s0, c0, c1) if axis == "x" else pl.wall(msp, c0, c1, pos, s0))
        pos = s1
    if pos < b:
        (pl.wall(msp, pos, b, c0, c1) if axis == "x" else pl.wall(msp, c0, c1, pos, b))
    for s0, s1 in windows:
        (pl.window_y(msp, s0, s1, c0, c1) if axis == "x" else pl.window_x(msp, s0, s1, c0, c1))


# ---------------------------------------------------------------- muros perimetrales
pl.wall(msp, 0.0, E, YF0, YR1)
pl.wall(msp, W - E, W, YF0, YR1)
wall_with_openings("x", YF0, YF1, E, W - E, [], [(0.70, 2.90), (3.76, 4.66), (6.40, 8.20)])
wall_with_openings("x", YR0, YR1, E, W - E, [], [(0.70, 2.90), (3.85, 4.60), (6.40, 8.20)])
D_S1 = (0.25, 1.15)
wall_with_openings("x", Y2a, Y2b, E, W - E, [D_S1], [(2.00, 4.40), (5.60, 8.20)])
wall_with_openings("x", Y3a, Y3b, XB1, W - E, [], [(2.70, 4.30), (6.60, 8.40)])
D_S2 = (15.55, 16.45)
pl.window_x(msp, Y2b + 0.10, Y3a - 0.10, XB0, XB1)
pl.wall(msp, XB0, XB1, Y2b, Y2b + 0.10)
pl.wall(msp, XB0, XB1, Y3a - 0.10, Y3b)
wall_with_openings("y", XB0, XB1, Y3b, Y4a, [D_S2])
wall_with_openings("x", Y4a, Y4b, XB0, W - E, [], [(5.40, 7.00), (7.50, 8.60)])
pl.wall(msp, XC0, XC1, Y4b, Y5a)
D_S3 = (0.25, 1.15)
wall_with_openings("x", Y5a, Y5b, E, W - E, [D_S3], [(5.40, 8.40)])

# ---------------------------------------------------------------- suite 1 (igual que N2)
XBA0, XBA1 = 3.72, 5.27
YBA1 = YF1 + 2.20
XWI0 = XBA1 + I
YWI1 = YF1 + 3.25
pl.wall(msp, XBA0 - I, XBA0, YF1, YBA1 + I)
wall_with_openings("x", YBA1, YBA1 + I, XBA0, XBA1, [(XBA0, XBA0 + 0.80)])
pl.wall(msp, XBA1, XWI0, YF1, YWI1 + I)
wall_with_openings("x", YWI1, YWI1 + I, XWI0, W - E, [(6.00, 6.80)])
pl.door(msp, (D_S1[1], Y2a), 0.90, (-1, 0), (0, -1))
pl.door(msp, (XBA0, YBA1 + I), 0.80, (1, 0), (0, 1))
pl.door(msp, (6.00, YWI1), 0.80, (1, 0), (0, -1))
pl.bed(msp, E, 2.70, E + 2.00, 4.30, head="x0")
pl.rect(msp, E, 2.22, E + 0.45, 2.65)
pl.rect(msp, E, 4.35, E + 0.45, 4.78)
pl.sofa(msp, 2.00, 6.72, 4.00, 7.57, back="y1")
pl.rect(msp, 2.50, 5.85, 3.50, 6.35)
pl.sofa(msp, 0.55, 5.35, 1.35, 6.15, back="x0")
pl.rect(msp, 6.40, 7.00, 7.60, 7.58)
pl.chair(msp, 7.00, 6.70, (0, 1))
pl.shower(msp, XBA0, YF1, XBA1, YF1 + 0.85)
pl.wc(msp, XBA1, YF1 + 0.85 + 0.375, (-1, 0))
pl.lav(msp, XBA1 - 0.50, YF1 + 1.65, XBA1, YF1 + 2.15)
pl.closet(msp, W - E - 0.60, YF1, W - E, YWI1, "y")
pl.closet(msp, XWI0, YF1, XWI0 + 0.60, 4.60, "y")

# ---------------------------------------------------------------- suite 2 (módulo central)
XK1 = W - E
XB2_0, XB2_1 = 7.30, XK1                 # baño 1.55 (sobre zona húmeda de la cocina)
YB2_0, YB2_1 = Y4a - 2.20, Y4a           # 14.63 - 16.83
XW2_0, YW2_0, YW2_1 = 6.10, Y3b, YB2_0 - I     # walk-in 2.75 x 4.10 (con ventana a P1)
pl.wall(msp, XB2_0 - I, XB2_0, YB2_0 - I, YB2_0)
wall_with_openings("y", XB2_0 - I, XB2_0, YB2_0, Y4a, [(15.10, 15.90)])
wall_with_openings("x", YW2_1, YB2_0, XW2_0 - I, XK1, [])         # muro walk-in / baño
wall_with_openings("y", XW2_0 - I, XW2_0, YW2_0, YW2_1, [(12.30, 13.10)])
pl.door(msp, (XB1, D_S2[1]), 0.90, (0, -1), (1, 0))               # acceso suite 2
pl.door(msp, (XB2_0 - I, 15.10), 0.80, (0, 1), (-1, 0))           # baño -> dormitorio
pl.door(msp, (XW2_0, 13.10), 0.80, (0, -1), (1, 0))               # walk-in
pl.shower(msp, XB2_0, Y4a - 0.85, XB2_1, Y4a)
pl.wc(msp, XB2_1, Y4a - 0.85 - 0.375, (-1, 0))
pl.lav(msp, XB2_1 - 0.50, YB2_0 + 0.05, XB2_1, YB2_0 + 0.55)
pl.closet(msp, XK1 - 0.60, YW2_0, XK1, YW2_1, "y")
pl.closet(msp, XW2_0, YW2_1 - 0.60, XK1 - 0.60, YW2_1, "x")
pl.bed(msp, XB1, 11.40, XB1 + 2.00, 13.00, head="x0")
pl.rect(msp, XB1, 10.92, XB1 + 0.45, 11.35)
pl.rect(msp, XB1, 13.05, XB1 + 0.45, 13.48)
pl.sofa(msp, 2.60, Y4a - 0.85, 4.60, Y4a, back="y1")
pl.rect(msp, 3.10, 15.00, 4.10, 15.50)
pl.sofa(msp, 5.10, 14.90, 5.90, 15.70, back="x1")

# ---------------------------------------------------------------- suite 3 (reflejo de suite 1)
YB3_0 = YR0 - 2.20                       # 22.83
YW3_0 = YR0 - 3.25                       # 21.78
pl.wall(msp, XBA0 - I, XBA0, YB3_0 - I, YR0)
wall_with_openings("x", YB3_0 - I, YB3_0, XBA0, XBA1, [(XBA0, XBA0 + 0.80)])
pl.wall(msp, XBA1, XWI0, YW3_0 - I, YR0)
wall_with_openings("x", YW3_0 - I, YW3_0, XWI0, W - E, [(6.00, 6.80)])
pl.door(msp, (D_S3[1], Y5b), 0.90, (-1, 0), (0, 1))
pl.door(msp, (XBA0, YB3_0 - I), 0.80, (1, 0), (0, -1))
pl.door(msp, (6.00, YW3_0), 0.80, (1, 0), (0, 1))
pl.bed(msp, E, 22.90, E + 2.00, 24.50, head="x0")
pl.rect(msp, E, 22.42, E + 0.45, 22.85)
pl.rect(msp, E, 24.55, E + 0.45, 24.98)
pl.sofa(msp, 2.00, Y5b, 4.00, Y5b + 0.85, back="y0")
pl.rect(msp, 2.50, 20.95, 3.50, 21.45)
pl.rect(msp, 6.40, Y5b, 7.60, Y5b + 0.58)
pl.chair(msp, 7.00, Y5b + 0.90, (0, -1))
pl.shower(msp, XBA0, YR0 - 0.85, XBA1, YR0)
pl.wc(msp, XBA1, YR0 - 0.85 - 0.375, (-1, 0))
pl.lav(msp, XBA1 - 0.50, YB3_0 + 0.05, XBA1, YB3_0 + 0.55)
pl.closet(msp, W - E - 0.60, YW3_0, W - E, YR0, "y")
pl.closet(msp, XWI0, 22.64, XWI0 + 0.60, YR0, "y")

# ---------------------------------------------------------------- escalera (llegada a N3)
TH = 0.28
yA0, yA1 = Y4b, Y4b + 1.10
yB0, yB1 = Y5a - 1.10, Y5a
X_DES = X0 + 8 * TH
for k in range(0, 9):
    pl.line(msp, (X0 + k * TH, yA0), (X0 + k * TH, yA1), "A-ESCALERA")
pl.line(msp, (X0, yA1), (X_DES, yA1), "A-ESCALERA")
for k in range(0, 8):
    pl.line(msp, (X_DES - k * TH, yB0), (X_DES - k * TH, yB1), "A-ESCALERA")
pl.line(msp, (X_DES - 7 * TH, yB0), (X_DES, yB0), "A-ESCALERA")
pl.line(msp, (X_DES, yA0), (X_DES, yB1), "A-ESCALERA")
pl.line(msp, (X_DES - 7 * TH, yA1 + 0.15), (X_DES, yA1 + 0.15), "A-ESCALERA")
pl.poly(msp, [(X0, Y4b), (X0, yB0), (X_DES - 7 * TH, yB0)], "A-ESCALERA", close=False)
pl.poly(msp, [(X0 + 0.05, Y4b), (X0 + 0.05, yB0 - 0.05), (X_DES - 7 * TH, yB0 - 0.05)],
        "A-ESCALERA", close=False)
pl.text(msp, "BARANDA", X0 + 0.16, 17.6, 0.08, "A-TXT-50", rot=90)
a, b = P(X_DES - 7 * TH + 0.15, (yB0 + yB1) / 2), P(X_DES - 0.15, (yB0 + yB1) / 2)
msp.add_line(a, b, dxfattribs={"layer": "A-ESCALERA"})
d = (b - a).normalize()
n = Vec2(-d.y, d.x)
msp.add_solid([b, b - d * 0.20 + n * 0.12, b - d * 0.20 - n * 0.12],
              dxfattribs={"layer": "A-ESCALERA"})
pl.text(msp, "BAJA", (X_DES - 7 * TH + X_DES) / 2, (yB0 + yB1) / 2 + 0.18, 0.12, "A-ESCALERA")

# ---------------------------------------------------------------- columnas y patios
H.columns(msp, upper=True)
for PP in (P1, P2):
    (xa, xb), (ya, yb) = PP["x"], PP["y"]
    pl.line(msp, (xa, ya), (xb, yb), "A-PROYECCION", pl.LT_DASH)
    pl.line(msp, (xb, ya), (xa, yb), "A-PROYECCION", pl.LT_DASH)

# ---------------------------------------------------------------- rótulos y áreas
A_S1 = (W - 2 * E) * (Y2a - YF1)
A_BA = (XBA1 - XBA0) * (YBA1 - YF1)
A_WI = (W - E - XWI0) * (YWI1 - YF1)
A_S2 = (W - E - XB1) * (Y4a - Y3b)
A_BA2 = (XB2_1 - XB2_0) * (YB2_1 - YB2_0)
A_WI2 = (XK1 - XW2_0) * (YW2_1 - YW2_0)
A_S3 = (W - 2 * E) * (YR0 - Y5b)
L_PAS = Y5a - Y2b
A_PAS = (XB0 - E) * L_PAS
A_GRA = (X1 - X0) * (Y5a - Y4b)
pl.room_label(msp, "SUITE 1\\PDORMITORIO Y ESTAR", 1.95, 5.25, None, None, 0.15)
pl.room_label(msp, "BAÑO", 4.12, 4.05, None, A_BA, 0.10)
pl.room_label(msp, "WALK-IN CLOSET", 7.10, 3.85, "3.46 x 3.25", A_WI, 0.12)
pl.room_label(msp, "SUITE 2\\PDORMITORIO Y ESTAR", 4.55, 12.00, None, None, 0.15)
pl.room_label(msp, "BAÑO", 7.75, 15.55, None, A_BA2, 0.10)
pl.room_label(msp, "WALK-IN CLOSET", 7.00, 11.30, "2.75 x 4.10", A_WI2, 0.12)
pl.room_label(msp, "SUITE 3\\PDORMITORIO Y ESTAR", 1.95, 21.55, None, None, 0.15)
pl.room_label(msp, "BAÑO", 4.12, 23.15, None, A_BA, 0.10)
pl.room_label(msp, "WALK-IN CLOSET", 7.10, 23.35, "3.46 x 3.25", A_WI, 0.12)
pl.text(msp, "PASILLO", 0.75, 13.00, 0.13, "A-ESPACIOS")
pl.text(msp, "GALERÍA - VIDRIO FIJO A P1", 0.75, 9.0, 0.085, "A-TXT-50")
pl.mtext(msp, "PATIO DE LUZ P1\\P(ABIERTO)", 5.16, 9.0, 0.14, 3.0, "A-ESPACIOS")
pl.mtext(msp, "PATIO P2\\P(ABIERTO)", 6.83, 18.25, 0.14, 3.0, "A-ESPACIOS")
pl.text(msp, "GRADAS EN U (LLEGADA): 17 CH = 0.176 / H = 0.28", 0.75, Y4b + 0.05, 0.085,
        "A-TXT-50", "MIDDLE_LEFT")
pl.text(msp, "CALLE PÚBLICA", 4.5, -2.15, 0.22, "A-ESPACIOS", rot=90)
pl.mtext(msp, "COLINDANCIA - FACHADA CIEGA", -0.35, 14.0, 0.10, 6.0, "A-TXT-50")
pl.mtext(msp, "COLINDANCIA - FACHADA CIEGA", W + 0.35, 14.0, 0.10, 6.0, "A-TXT-50")
for (x, y) in ((2.6, 2.8), (0.45, 11.0), (2.2, 14.3), (5.6, 21.25)):
    pl.level(msp, x, y, NPT)

# ---------------------------------------------------------------- ejes y cotas
H.axes(msp)
H.general_dims(msp)
chain = [YF0, YF1, Y2a, Y2b, Y3a, Y3b, Y4a, Y4b, Y5a, Y5b, YR0, YR1]
for ya, yb in zip(chain[:-1], chain[1:]):
    pl.dim(msp, (W - E, ya), (W - E, yb), (W + 0.95, 0), False)
for xa, xb in ((XBA0 - I, XBA0), (XBA0, XBA1), (XBA1, XWI0), (XWI0, W - E)):
    pl.dim(msp, (xa, YF1), (xb, YF1), (0, 5.02), True)
    pl.dim(msp, (xa, YR0), (xb, YR0), (0, 21.28), True)
pl.dim(msp, (XBA0, YF1), (XBA0, YBA1), (XBA0 + 0.30, 0), False)
pl.dim(msp, (XBA0, YB3_0), (XBA0, YR0), (XBA0 + 0.30, 0), False)
pl.dim(msp, (6.10, YF1), (6.10, YWI1), (6.10, 0), False)
pl.dim(msp, (6.10, YW3_0), (6.10, YR0), (6.10, 0), False)
for xa, xb in ((E, XB0), (XB0, XB1), (XB1, XW2_0 - I), (XW2_0 - I, XW2_0), (XW2_0, XK1)):
    pl.dim(msp, (xa, Y3b), (xb, Y3b), (0, 14.20), True)
pl.dim(msp, (XB2_0, YB2_0), (XB2_1, YB2_0), (0, 16.60), True)
pl.dim(msp, (XB2_0, YB2_0), (XB2_0, YB2_1), (XB2_0 - 0.30, 0), False)
pl.dim(msp, (7.70, YW2_0), (7.70, YW2_1), (7.70, 0), False)
pl.dim(msp, (XC1, Y4b), (W - E, Y4b), (0, Y4b + 0.45), True)
H.sections(msp)
RW = [E, 0.70, 2.90, 3.85, 4.60, 6.40, 8.20, W - E]
for xa, xb in zip(RW[:-1], RW[1:]):                 # ventanas fachada posterior
    pl.dim(msp, (xa, YR1), (xb, YR1), (0, YR1 + 0.55), True)

# ---------------------------------------------------------------- hoja
psp = H.sheet(doc, "A4-NIVEL3", "PLANTA NIVEL 3", "")
H.north(psp, north_ang)
H.title_and_derrotero(psp, "PLANTA NIVEL 3", "SUITES 1, 2 Y 3")

X2 = 240.0
y = 262.0
cl.text(psp, "CUADRO DE ÁREAS NIVEL 3", (X2 + 100, y), 4.5, "A-TITULOS", "TOP_CENTER")
rows = [["ESPACIO (MEDIDAS LIBRES)", "ÁREA"],
        ["SUITE 1 (DORMITORIO-ESTAR, BAÑO Y WALK-IN) 8,70 x 5,40", cl.m2(A_S1)],
        ["      BAÑO 1,55 x 2,20 / WALK-IN 3,46 x 3,25",
         f"{A_BA:.2f} / {A_WI:.2f}".replace(".", ",")],
        ["SUITE 2 (DORMITORIO-ESTAR, BAÑO Y WALK-IN) 7,38 x 6,42", cl.m2(A_S2)],
        ["      BAÑO 1,55 x 2,20 / WALK-IN 2,75 x 4,10",
         f"{A_BA2:.2f} / {A_WI2:.2f}".replace(".", ",")],
        ["SUITE 3 (DORMITORIO-ESTAR, BAÑO Y WALK-IN) 8,70 x 5,40", cl.m2(A_S3)],
        ["      BAÑO 1,55 x 2,20 / WALK-IN 3,46 x 3,25",
         f"{A_BA:.2f} / {A_WI:.2f}".replace(".", ",")],
        [f"PASILLO 1,20 x {L_PAS:.2f}".replace(".", ","), cl.m2(A_PAS)],
        ["GRADAS 3,34 x 2,50", cl.m2(A_GRA)],
        ["ÁREA CONSTRUIDA NIVEL 3 (ENVOLVENTE - PATIOS)", cl.m2(H.A_HUELLA)]]
y = cl.table(psp, X2, y - 8, [150, 50], rows, row_h=5.4, h=2.2,
             aligns=["MIDDLE_LEFT", "MIDDLE_RIGHT"])
cl.text(psp, "ÁREA CONSTRUIDA INCLUYE MUROS. BAÑOS Y WALK-IN ESTÁN INCLUIDOS EN CADA SUITE.",
        (X2, y - 1.5), 1.9, "A-TEXTO", "TOP_LEFT")
y -= 9
cl.text(psp, "RESUMEN DE ÁREAS DE CONSTRUCCIÓN", (X2 + 100, y), 3.5, "A-TITULOS", "TOP_CENTER")
rows = [["NIVEL 1 (VER A2)", cl.m2(H.A_N1)],
        ["NIVEL 2 (VER A3)", cl.m2(H.A_HUELLA)],
        ["NIVEL 3", cl.m2(H.A_HUELLA)],
        ["ÁREA TOTAL DE CONSTRUCCIÓN", cl.m2(H.A_N1 + 2 * H.A_HUELLA)]]
y = cl.table(psp, X2, y - 7, [150, 50], rows, row_h=5.4, h=2.2,
             aligns=["MIDDLE_LEFT", "MIDDLE_RIGHT"])
y = H.cobertura(psp, X2, y - 6)

X3 = 455.0
y = 262.0
cl.text(psp, "NOTAS:", (X3, y), 3.5, "A-TITULOS", "TOP_LEFT")
extra = [
    "NIVEL 3: NPT +6.00 (ALTURA PISO A PISO 3.00 m).",
    "TRES SUITES CON DORMITORIO Y ESTAR ABIERTOS; SOLO EL BAÑO Y EL WALK-IN SON RECINTOS "
    "CERRADOS. BAÑOS DE 1.55 x 2.20 m CON DUCHA, INODORO Y LAVATORIO EN LÍNEA Y PUERTA DE "
    "0.80 m ABATIBLE HACIA EL DORMITORIO.",
    "ALINEACIÓN DE NÚCLEOS HÚMEDOS: BAÑO DE SUITE 1 SOBRE EL BAÑO DEL NIVEL 2; BAÑO DE SUITE 2 "
    "SOBRE LA ZONA HÚMEDA DE LA COCINA; BAÑO DE SUITE 3 SOBRE LA SALA FAMILIAR, CON LAS "
    "BAJANTES EN UN DUCTO JUNTO A C6 EN LA SALA DEL NIVEL 2 (VER S02).",
    "PASILLO DE 1.20 m CERRADO HACIA EL PATIO P1 CON VIDRIO FIJO (GALERÍA). BARANDA EN EL "
    "BORDE DE LA ESCALERA (VER A8). ACCESOS A LAS SUITES DESDE EL PASILLO (EJES 2, B Y 5).",
    "VENTANAS HACIA P1 DESFASADAS ENTRE SUITES PARA REDUCIR VISUALES CRUZADAS.",
    "COLUMNAS SOBRE EL EJE C SEGÚN LÁMINA A2, MÁS LA C1 DEL EJE C EN EL EJE 1 (NIVELES 2 Y 3, "
    "SOBRE VIGA DE TRANSFERENCIA, VER C05); SECCIONES Y REFUERZO EN C01 A C06.",
    "FACHADA FRONTAL: VENTANAS DE PISO A 2.20 m CON PAÑO FIJO INFERIOR DE SEGURIDAD HASTA "
    "0.90 m Y VENTILAS ABATIBLES HACIA AFUERA EN LA PARTE SUPERIOR; BAÑO CON VIDRIO "
    "ARENADO (VER A5).",
    "FACHADA POSTERIOR: VENTANAS CON ANTEPECHO COMÚN DE 0.90 m Y DINTEL A 2.20 m, "
    "ALINEADAS ENTRE LOS NIVELES 2 Y 3 Y OPERABLES EN TODA SU ÁREA (VER A5).",
    "TODAS LAS VENTANAS SON DE VENTILACIÓN: VENTILA ABATIBLE HACIA AFUERA (BISAGRA "
    "SUPERIOR); DONDE INTERFIERA CON UN PASILLO, CORREDIZA DE DOS PAÑOS MÓVIL-MÓVIL.",
    "DIMENSIONES Y TIPOS DE PUERTAS, VENTANAS Y ACABADOS EN LÁMINA A7.",
]
y = cl.notes_block(psp, X3, y - 6, cl.notas(extra), 2.1, 250)
H.extractor_detail(psp, X3, min(y - 6, 165.0))

H.titleblock(doc, psp, "A4", "PLANTA NIVEL 3",
             ["SUITES 1, 2 Y 3.", "DERROTERO.", "CUADRO DE ÁREAS.",
              "PORCENTAJE DE COBERTURA.", "DETALLE EXTRACTOR DE AIRE.", "NOTAS."],
             [("4", "06-10-2026", "COLUMNA C1 EJE C-1; VENTANA BAÑO 0,90"),
              ("5", "07-10-2026", "REFERENCIAS A C01-C06 Y S02"),
              ("6", "07-10-2026", "LISTA DEFINITIVA (22); PARA TRÁMITE")])

OUT.mkdir(parents=True, exist_ok=True)
doc.saveas(OUT / f"{NAME}.dxf")
cl.render_pdf(doc, "A4-NIVEL3", OUT / f"{NAME}.pdf")
print("S1", round(A_S1, 2), "S2", round(A_S2, 2), "baño2", round(A_BA2, 2), "WI2",
      round(A_WI2, 2), "S3", round(A_S3, 2), "| N3", round(H.A_HUELLA, 2))
print("DXF:", OUT / f"{NAME}.dxf")
