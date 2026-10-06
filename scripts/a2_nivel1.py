"""Lámina A2 - PLANTA NIVEL 1 (parqueos, acceso y circulación vertical).

Model Space en metros, marco de PLANTA (ver planta.py): X = fondo desde la
línea de frente (calle a la izquierda), Y = ancho desde el lindero oeste.
UCS "CRTM05" incluido.
"""
import os

from ezdxf.math import Vec2

import cadlib as cl
import planta as pl
from planta import P

REV = "rev0"
OUT = cl.ROOT / "planos" / "A2_nivel1"
NAME = f"SR-A2_NIVEL1_{REV}"

prj = cl.load_project()
G = prj["geometria_m"]
lote, V, LOC, frame = pl.lot_model()

E, I = G["muro_ext"], G["muro_int"]
ey0, ey1 = G["envolvente_y"]          # 2.06 / 25.18
c = G["cadena_y"]
P1, P2, ESC = G["patio_P1"], G["patio_P2"], G["escalera"]
W = 9.0
XB0, XB1 = 1.35, 1.47                  # muro eje B (pasillo)
XC0, XC1 = ESC["x"][1], P2["x"][0]     # muro eje C (4.69-4.81)
Y_P1a, Y_P1b = P1["y"]                 # 7.76 / 10.26
Y4a, Y4b = c["sba"] - E, c["sba"]      # muro eje 4 (16.83-16.98)
Y5a, Y5b = c["sbb"], c["sbb"] + E      # muro eje 5 (19.48-19.63)
Y_ROW = ey0 + E                        # cara interior fachada 2.21
Y_BOD = Y_ROW + 10.0                   # fin de 2 filas de 5.00 m -> 12.21
# Fachada frontal N1
X_PED0, X_PED1 = E, 1.26               # acceso peatonal libre 1.11
X_PIL0, X_PIL1 = 1.26, 1.56            # pilastra en eje B
X_VEH0, X_VEH1 = 1.56, W - E           # portón vehicular libre 7.29

doc = cl.new_doc()
cl.north_block(doc)
msp = doc.modelspace()
north_ang = pl.add_crtm_ucs(doc, frame)

# ---------------------------------------------------------------- lindero
lot_pts = [LOC[k] for k in (1, 2, 3, 4, 5)]
pl.poly(msp, lot_pts, "T-LINDERO")
for k, (x, y) in LOC.items():
    msp.add_circle(P(x, y), 0.18, dxfattribs={"layer": "T-VERTICE"})
    off = {1: (-0.35, -0.35), 2: (-0.35, -0.35), 3: (9.35, -0.35), 4: (9.35, 28.85),
           5: (-0.35, 28.85)}[k]
    pl.text(msp, str(k), off[0], off[1], 0.18, "T-VERTICE")

# ---------------------------------------------------------------- muros
pl.wall(msp, 0.0, E, ey0, ey1)                       # colindancia oeste
pl.wall(msp, W - E, W, ey0, ey1)                     # colindancia este
pl.wall(msp, X_PIL0, X_PIL1, ey0, Y_ROW)             # pilastra frontal (eje B)
# bodega
pl.wall(msp, XB1, W - E, Y_BOD, Y_BOD + I)           # muro norte bodega
DB0, DB1 = 15.75, 16.65                              # puerta bodega 0.90
pl.wall(msp, XB0, XB1, Y_BOD, DB0)
pl.wall(msp, XB0, XB1, DB1, Y4a)
# eje 4 (bodega / escalera-P2) con ventana hacia P2
VB0, VB1 = 6.00, 8.00
pl.wall(msp, XB0, VB0, Y4a, Y4b)
pl.wall(msp, VB1, W - E, Y4a, Y4b)
pl.window_y(msp, VB0, VB1, Y4a, Y4b)
# eje C (escalera / P2)
pl.wall(msp, XC0, XC1, Y4b, Y5a)
# eje 5 (escalera-P2 / espacio posterior): puertas a pasillo y a P2
D5a0, D5a1 = 0.25, 1.15
D5b0, D5b1 = 6.20, 7.10
pl.wall(msp, E, D5a0, Y5a, Y5b)
pl.wall(msp, D5a1, D5b0, Y5a, Y5b)
pl.wall(msp, D5b1, W - E, Y5a, Y5b)
# fachada posterior con puerta y ventanas
YR0, YR1 = ey1 - E, ey1
DR0, DR1 = 0.60, 1.50
VR = [(2.60, 4.40), (5.60, 7.80)]
pl.wall(msp, E, DR0, YR0, YR1)
pl.wall(msp, DR1, VR[0][0], YR0, YR1)
pl.wall(msp, VR[0][1], VR[1][0], YR0, YR1)
pl.wall(msp, VR[1][1], W - E, YR0, YR1)
for a, b in VR:
    pl.window_y(msp, a, b, YR0, YR1)

# puertas
pl.door(msp, (DB0, XB1), 0.90, (0, 1), (1, 0)) if False else None
pl.door(msp, (XB1, DB1), 0.90, (0, -1), (1, 0))      # bodega, abre hacia dentro
pl.door(msp, (D5a1, Y5b), 0.90, (-1, 0), (0, 1))     # espacio posterior
pl.door(msp, (D5b0, Y5a), 0.90, (1, 0), (0, -1))     # hacia P2
pl.door(msp, (DR0, YR1), 0.90, (1, 0), (0, 1))       # patio posterior
# portón y acceso peatonal (indicativos)
pl.line(msp, (X_VEH0, ey0 + 0.07), (X_VEH1, ey0 + 0.07), "A-PUERTA")
pl.line(msp, (X_VEH0, ey0 + 0.03), (X_VEH1, ey0 + 0.03), "A-PUERTA")
pl.door(msp, (X_PED1, ey0), 1.00, (-1, 0), (0, 1))   # portón peatonal 1.00

# ---------------------------------------------------------------- proyecciones superiores
for ya, yb in ((Y_P1a - E, Y_P1a), (Y_P1b, Y_P1b + E)):
    pl.poly(msp, [(E, ya), (W - E, ya), (W - E, yb), (E, yb)], "A-PROYECCION",
            ltscale=pl.LT_DASH)
pl.poly(msp, [(P1["x"][0], Y_P1a), (P1["x"][1], Y_P1a), (P1["x"][1], Y_P1b),
              (P1["x"][0], Y_P1b)], "A-PROYECCION", ltscale=pl.LT_DASH)
pl.line(msp, (P1["x"][0], Y_P1a), (P1["x"][1], Y_P1b), "A-PROYECCION", pl.LT_DASH)
pl.line(msp, (P1["x"][1], Y_P1a), (P1["x"][0], Y_P1b), "A-PROYECCION", pl.LT_DASH)
# muro del pasillo en nivel 2 (proyección)
pl.poly(msp, [(XB0, Y_P1a), (XB1, Y_P1a), (XB1, Y_BOD), (XB0, Y_BOD)], "A-PROYECCION",
        ltscale=pl.LT_DASH)
# P2 abierto (diagonales)
pl.line(msp, (P2["x"][0], P2["y"][0]), (P2["x"][1], P2["y"][1]), "A-PROYECCION", pl.LT_DASH)
pl.line(msp, (P2["x"][1], P2["y"][0]), (P2["x"][0], P2["y"][1]), "A-PROYECCION", pl.LT_DASH)

# ---------------------------------------------------------------- estacionamientos
pl.line(msp, (XB0, Y_ROW), (XB0, Y_BOD), "A-DEMARCACION", pl.LT_DASH)
for xs in (XB0 + 2.5, XB0 + 5.0):
    pl.line(msp, (xs, Y_ROW), (xs, Y_BOD), "A-DEMARCACION", pl.LT_DASH)
pl.line(msp, (XB0, Y_ROW + 5.0), (W - E, Y_ROW + 5.0), "A-DEMARCACION", pl.LT_DASH)
n = 1
for row in (0, 1):
    for k in range(3):
        xc = XB0 + 1.25 + 2.5 * k
        yc = Y_ROW + 2.5 + 5.0 * row
        pl.car(msp, xc, yc + 0.10, front_dir=-1)
        pl.text(msp, f"E-{n}", xc, yc - 0.20 + (0.0), 0.20, "A-ESPACIOS")
        n += 1

# ---------------------------------------------------------------- escalera en U
X0, X1 = ESC["x"]                      # 1.35 / 4.69
TH = 0.28
yA0, yA1 = Y4b, Y4b + 1.10             # tramo 1 (sube hacia el este)
yB0, yB1 = Y5a - 1.10, Y5a             # tramo 2 (regresa al oeste)
X_DES = X0 + 8 * TH                    # inicio del descanso 3.59
CUT = X0 + 6 * TH                      # línea de corte del plano
for k in range(0, 9):
    x = X0 + k * TH
    if x <= CUT + 1e-6:
        pl.line(msp, (x, yA0), (x, yA1), "A-ESCALERA")
    else:
        pl.line(msp, (x, yA0), (x, yA1), "A-PROYECCION", pl.LT_DASH)
pl.line(msp, (X0, yA1), (CUT, yA1), "A-ESCALERA")
pl.line(msp, (CUT, yA1), (X_DES, yA1), "A-PROYECCION", pl.LT_DASH)
pl.line(msp, (CUT - 0.25, yA0), (CUT + 0.25, yA1), "A-ESCALERA")   # quiebre
for k in range(0, 8):
    x = X_DES - k * TH
    pl.line(msp, (x, yB0), (x, yB1), "A-PROYECCION", pl.LT_DASH)
pl.line(msp, (X_DES - 7 * TH, yB0), (X_DES, yB0), "A-PROYECCION", pl.LT_DASH)
pl.line(msp, (X_DES, yA0), (X_DES, yB1), "A-PROYECCION", pl.LT_DASH)
# flecha "SUBE"
a = P(X0 + 0.15, (yA0 + yA1) / 2)
b = P(CUT - 0.15, (yA0 + yA1) / 2)
msp.add_line(a, b, dxfattribs={"layer": "A-ESCALERA"})
msp.add_solid([b + Vec2(0.0, 0.0), b + Vec2(-0.12, -0.20), b + Vec2(0.12, -0.20)],
              dxfattribs={"layer": "A-ESCALERA"})
pl.text(msp, "SUBE", X0 + 0.55, (yA0 + yA1) / 2 + 0.18, 0.13, "A-ESCALERA")
pl.mtext(msp, "ESCALERA EN U\\P17 CH = 0.176 / H = 0.28", (X0 + X1) / 2,
         (yB0 + yB1) / 2, 0.11, 2.6, "A-ESPACIOS")

# ---------------------------------------------------------------- textos de espacios
pl.mtext(msp, "ESTACIONAMIENTOS\\P6 ESPACIOS DE 2.50 x 5.00\\P(3 INDEPENDIENTES + 3 EN TÁNDEM)",
         5.1, Y_ROW + 5.0, 0.15, 4.5, "A-ESPACIOS")
pl.mtext(msp, "PASILLO PEATONAL", 0.75, 6.0, 0.13, 2.0, "A-ESPACIOS")
pl.text(msp, "PASILLO PEATONAL", 0.75, 6.0, 0.13, "A-ESPACIOS", rot=0)
for e in list(msp.query("MTEXT")):
    if e.text == "PASILLO PEATONAL":
        msp.delete_entity(e)
pl.text(msp, "PASILLO", 0.75, 14.5, 0.13, "A-ESPACIOS")
pl.mtext(msp, "BORDILLO DE DEMARCACIÓN", XB0 + 0.12, 3.6, 0.09, 1.0, "A-TXT-50", attach=4)
A_bod = (W - E - XB1) * (Y4a - Y_BOD - I)
pl.mtext(msp, f"BODEGA\\P(USO POR DEFINIR)\\P{A_bod:.2f} m²", 5.2, 14.6, 0.15, 3.5,
         "A-ESPACIOS")
A_esp = (W - 2 * E) * (YR0 - Y5b)
pl.mtext(msp, f"ESPACIO CUBIERTO\\P(USO POR DEFINIR)\\P{A_esp:.2f} m²", 4.5, 22.3, 0.15, 4.0,
         "A-ESPACIOS")
pl.mtext(msp, "PATIO P2\\P(ABIERTO)", (P2["x"][0] + P2["x"][1]) / 2, 18.0, 0.15, 2.5,
         "A-ESPACIOS")
pl.mtext(msp, "PROYECCIÓN PATIO DE LUZ P1\\P(ABIERTO A CIELO)",
         (P1["x"][0] + P1["x"][1]) / 2, 9.0, 0.11, 4.0, "A-TXT-50")
pl.mtext(msp, "PATIO POSTERIOR\\PTANQUE SÉPTICO Y DRENAJE\\P(UBICACIÓN Y DIMENSIONES POR DISEÑAR)",
         4.5, 26.85, 0.13, 6.5, "A-ESPACIOS")
pl.mtext(msp, "RETIRO FRONTAL\\PACCESO", 4.5, 1.05, 0.12, 3.0, "A-ESPACIOS")
pl.mtext(msp, "CALLE PÚBLICA", 4.5, -2.6, 0.22, 4.0, "A-ESPACIOS")
pl.mtext(msp, "ACCESO\\PPEATONAL", 0.70, -0.75, 0.10, 1.2, "A-TXT-50")
pl.mtext(msp, "ACCESO VEHICULAR\\PPORTÓN (TIPO POR DEFINIR)", 5.2, -0.75, 0.10, 4.0,
         "A-TXT-50")
pl.mtext(msp, "COLINDANCIA - FACHADA CIEGA", 0.0 - 0.35, 14.0, 0.10, 6.0, "A-TXT-50")
pl.mtext(msp, "COLINDANCIA - FACHADA CIEGA", W + 0.35, 14.0, 0.10, 6.0, "A-TXT-50")
pl.mtext(msp, "PILASTRA\\P(EJE B)", 1.41, 1.55, 0.08, 1.0, "A-TXT-50")

# niveles
pl.level(msp, 3.0, 5.6, "NPT ±0.00")
pl.level(msp, 2.4, 22.6, "NPT ±0.00")
pl.level(msp, 6.4, 13.6, "NPT ±0.00")
pl.level(msp, 2.4, 0.6, "NIVEL DE ACERA ±0.00 (REF.)")

# ---------------------------------------------------------------- ejes
ejes_x = {"A": E / 2, "B": (XB0 + XB1) / 2, "C": (XC0 + XC1) / 2, "D": W - E / 2}
ejes_y = {"1": ey0 + E / 2, "2": Y_P1a - E / 2, "3": Y_P1b + E / 2, "4": (Y4a + Y4b) / 2,
          "5": (Y5a + Y5b) / 2, "6": ey1 - E / 2}
for k, x in ejes_x.items():
    pl.axis(msp, k, "x", x, -0.2, 30.0, "end")
for k, y in ejes_y.items():
    pl.axis(msp, k, "y", y, -3.0, 12.0, "both")

# ---------------------------------------------------------------- cotas
# oeste (abajo en planta): retiro / envolvente / retiro
for ya, yb in ((0.0, ey0), (ey0, ey1), (ey1, LOC[5][1])):
    pl.dim(msp, (0, ya), (0, yb), (-1.75, 0), False)
# ejes 1-6
ys = list(ejes_y.values())
for ya, yb in zip(ys[:-1], ys[1:]):
    pl.dim(msp, (E / 2, ya), (E / 2, yb), (-1.15, 0), False)
# interiores (lado este)
chain = [ey0, Y_ROW, Y_ROW + 5.0, Y_BOD, Y_BOD + I, Y4a, Y4b, Y5a, Y5b, YR0, YR1]
for ya, yb in zip(chain[:-1], chain[1:]):
    pl.dim(msp, (W - E, ya), (W - E, yb), (W + 0.95, 0), False)
pl.dim(msp, (W, ey0), (W, ey1), (W + 1.65, 0), False)
# fachada frontal (izquierda en planta)
fx = [0.0, X_PED0, X_PED1, X_PIL1, X_VEH1, W]
for xa, xb in zip(fx[:-1], fx[1:]):
    pl.dim(msp, (xa, ey0), (xb, ey0), (0, -0.55), True)
pl.dim(msp, (0.0, ey0), (W, ey0), (0, -1.35), True)
# estacionamientos
for xa, xb in ((E, XB0), (XB0, XB0 + 2.5), (XB0 + 2.5, XB0 + 5.0), (XB0 + 5.0, W - E)):
    pl.dim(msp, (xa, Y_ROW + 5.0), (xb, Y_ROW + 5.0), (0, Y_ROW + 4.55), True)
# bodega, escalera, P2, espacio posterior
pl.dim(msp, (XB1, Y_BOD + I), (W - E, Y_BOD + I), (0, Y_BOD + 0.55), True)
pl.dim(msp, (X0, Y4b), (X1, Y4b), (0, Y4b + 0.0 + 1.25), True)
pl.dim(msp, (XC1, Y4b), (W - E, Y4b), (0, Y4b + 0.40), True)
for ya, yb in ((Y4b, yA1), (yA1, yB0), (yB0, Y5a)):
    pl.dim(msp, (X1, ya), (X1, yb), (X1 - 0.45, 0), False)
pl.dim(msp, (E, Y5b), (W - E, Y5b), (0, Y5b + 0.55), True)
# ejes de letra (lado posterior)
xs = list(ejes_x.values())
for xa, xb in zip(xs[:-1], xs[1:]):
    pl.dim(msp, (xa, ey1), (xb, ey1), (0, 29.25), True)

# cortes
pl.section_mark(msp, "A", "A6", (3.0, -2.2), (3.0, 29.0), (1, 0))
pl.section_mark(msp, "B", "A6", (-2.2, 18.2), (11.2, 18.2), (0, 1))

# ---------------------------------------------------------------- hoja
psp = doc.layouts.new("A2-NIVEL1")
psp.page_setup(size=(cl.A1_W, cl.A1_H), margins=(0, 0, 0, 0), units="mm")
doc.layouts.set_active_layout("A2-NIVEL1")
cl.frame(psp)

VP_C = (368.0, 430.0)
VP_S = (668.0, 296.0)
vp = psp.add_viewport(center=VP_C, size=VP_S, view_center_point=(13.6, 4.4),
                      view_height=VP_S[1] * 50 / 1000.0, dxfattribs={"layer": "A-VIEWPORT"})
vp.dxf.flags = vp.dxf.flags | 16384
vp.frozen_layers = ["T-TXT-100", "T-TXT-200", "T-COTA-100", "T-COTA-200"]

# norte (bloque apunta a +Y en papel)
psp.add_blockref("NORTE", (672.0, 300.0), dxfattribs={"layer": "A-NORTE",
                                                       "rotation": north_ang - 90.0})
cl.text(psp, "NORTE SEGÚN CATASTRO", (672.0, 280.0), 1.8, "A-TEXTO", "TOP_CENTER")

cl.view_title(psp, 35.0, 262.0, "PLANTA NIVEL 1", "PARQUEOS, ACCESO Y CIRCULACIÓN VERTICAL",
              "Esc. 1:50", 150)
cl.scale_bar(psp, 35.0, 236.0, 50, 5, 1)

# derrotero
y = 222.0
cl.text(psp, "D E R R O T E R O", (35 + 95, y), 5.0, "A-TITULOS", "TOP_CENTER")
y = cl.table(psp, 35.0, y - 8, [38.0] * 5, cl.derrotero_rows(V), row_h=6.0, h=2.5)
cl.text(psp, "VER CUADRO DE COORDENADAS CRTM05 EN LÁMINA A1.", (35.0, y - 2.0), 2.0,
        "A-TEXTO", "TOP_LEFT")

# cuadro de áreas
X2 = 240.0
y = 262.0
A_env = 9.0 * (ey1 - ey0)
A_pat = (P1["x"][1] - P1["x"][0]) * (Y_P1b - Y_P1a) + (P2["x"][1] - P2["x"][0]) * 2.5
A_niv = A_env - A_pat
A_cat = lote["area_catastro_m2"]
cl.text(psp, "CUADRO DE ÁREAS", (X2 + 100, y), 4.5, "A-TITULOS", "TOP_CENTER")
rows = [["ESPACIO", "ÁREA"],
        ["ÁREA NIVEL 1", cl.m2(A_niv)],
        ["ÁREA NIVEL 2 (PRELIMINAR, VER A3)", cl.m2(A_niv)],
        ["ÁREA NIVEL 3 (PRELIMINAR, VER A4)", cl.m2(A_niv)],
        ["ÁREA DE CONSTRUCCIÓN", cl.m2(3 * A_niv)]]
y = cl.table(psp, X2, y - 8, [140, 60], rows, row_h=6.0, h=2.5,
             aligns=["MIDDLE_LEFT", "MIDDLE_RIGHT"])
cl.mtext(psp, "ÁREA POR NIVEL = ENVOLVENTE 9,00 x 23,12 (208,08 m²) - PATIOS ABIERTOS P1 Y P2 "
         "(28,55 m²). INCLUYE ESCALERA (8,35 m²) Y PASILLO.", (X2, y - 1.5), 2.0, 200)
y -= 12
cl.text(psp, "DESGLOSE NIVEL 1 (ÁREAS LIBRES ENTRE MUROS)", (X2 + 100, y), 3.0, "A-TITULOS",
        "TOP_CENTER")
rows = [["ESTACIONAMIENTOS (6) 7,50 x 10,00 (1)", cl.m2(75.0)],
        ["PASILLO PEATONAL 1,20 x 17,27", cl.m2(1.20 * (Y5a - Y_ROW))],
        [f"BODEGA {W - E - XB1:.2f} x {Y4a - Y_BOD - I:.2f}".replace(".", ","), cl.m2(A_bod)],
        ["ESCALERA 3,34 x 2,50", cl.m2(3.34 * 2.5)],
        [f"ESPACIO CUBIERTO POSTERIOR 8,70 x {YR0 - Y5b:.2f}".replace(".", ","), cl.m2(A_esp)]]
y = cl.table(psp, X2, y - 6, [140, 60], rows, row_h=6.0, h=2.4,
             aligns=["MIDDLE_LEFT", "MIDDLE_RIGHT"])
cl.text(psp, "(1) INCLUYE 18,45 m² BAJO EL PATIO P1, ABIERTO A CIELO.", (X2, y - 1.5), 2.0,
        "A-TEXTO", "TOP_LEFT")
y -= 10
cl.text(psp, "PORCENTAJE DE COBERTURA", (X2 + 100, y), 4.5, "A-TITULOS", "TOP_CENTER")
rows = [["CONCEPTO", "VALOR"],
        ["ÁREA DE LOTE (SEGÚN CATASTRO)", cl.m2(A_cat)],
        ["HUELLA CONSTRUCTIVA NIVEL 1", cl.m2(A_niv)],
        ["% COBERTURA", f"{A_niv / A_cat * 100:.2f} %".replace(".", ",")]]
y = cl.table(psp, X2, y - 8, [140, 60], rows, row_h=6.0, h=2.5,
             aligns=["MIDDLE_LEFT", "MIDDLE_RIGHT"])
cl.text(psp, f"CÁLCULO: (HUELLA / ÁREA DE LOTE) x 100 = ({A_niv:.2f} / {A_cat:.2f}) x 100 = "
        f"{A_niv / A_cat * 100:.2f} %".replace(".", ","), (X2, y - 1.5), 2.0, "A-TEXTO",
        "TOP_LEFT")

# notas
X3 = 455.0
y = 262.0
cl.text(psp, "NOTAS:", (X3, y), 3.5, "A-TITULOS", "TOP_LEFT")
extra = [
    "NIVEL 1: 6 ESTACIONAMIENTOS DE 2.50 x 5.00 m, E-1 A E-3 INDEPENDIENTES Y E-4 A E-6 EN "
    "TÁNDEM, CON ACCESO RECTO DESDE LA CALLE.",
    "PORTÓN VEHICULAR CON CLARO LIBRE DE 7.29 m Y ACCESO PEATONAL DE 1.00 m; TIPO DE PORTÓN "
    "POR DEFINIR.",
    "COLUMNAS, VIGAS Y PILASTRA DEL EJE B SEGÚN PLANOS ESTRUCTURALES (PENDIENTES DE DISEÑO). "
    "SOBRE LOS ESTACIONAMIENTOS NO SE PREVÉN COLUMNAS INTERMEDIAS.",
    "NPT ±0.00 = NIVEL DE ACERA (TERRENO PLANO). PENDIENTES DE PISO Y DESAGÜES SEGÚN LÁMINAS "
    "SANITARIAS.",
    "LOS USOS DE LA BODEGA Y DEL ESPACIO CUBIERTO POSTERIOR ESTÁN POR DEFINIR.",
]
cl.mtext(psp, "\\P".join(cl.notas(extra)), (X3, y - 6), 2.2, 250, attach=1)

# cajetín
vals = {
    "EMPRESA": prj["empresa"], "EMPRESA_CED": prj["empresa_ced"],
    "PROF_1": prj["profesionales"][0], "PROF_2": prj["profesionales"][1],
    "PROF_3": prj["profesionales"][2],
    "PROYECTO": prj["proyecto"], "UBIC_1": prj["ubicacion"][0], "UBIC_2": prj["ubicacion"][1],
    "UBIC_3": "",
    "REG_1": prj["registro"][0], "REG_2": prj["registro"][1], "REG_3": prj["registro"][2],
    "CONT_TIT": "PLANTA NIVEL 1",
    "CONT_1": "PARQUEOS Y ACCESO.", "CONT_2": "DERROTERO.", "CONT_3": "CUADRO DE ÁREAS.",
    "CONT_4": "PORCENTAJE DE COBERTURA.", "CONT_5": "NOTAS.", "CONT_6": "",
    "ESCALAS": "1:50 / INDICADAS",
    "REV0_N": "0", "REV0_F": "06-10-2026", "REV0_D": "VERSIÓN DE TRABAJO PARA REVISIÓN",
    "REV1_N": "", "REV1_F": "", "REV1_D": "", "REV2_N": "", "REV2_F": "", "REV2_D": "",
    "ESTADO_1": "VERSIÓN DE TRABAJO", "ESTADO_2": "NO APTA PARA CONSTRUCCIÓN NI TRÁMITE",
    "LUGAR": "COSTA RICA", "LAMINA": "A2", "FECHA": prj["fecha"], "TOTAL": prj["total_laminas"],
}
cl.insert_titleblock(doc, psp, vals)

OUT.mkdir(parents=True, exist_ok=True)
doc.saveas(OUT / f"{NAME}.dxf")
cl.render_pdf(doc, "A2-NIVEL1", OUT / f"{NAME}.pdf", OUT / f"{NAME}.png", dpi=110)
print("Área por nivel", round(A_niv, 2), "bodega", round(A_bod, 2), "esp. post.", round(A_esp, 2))
print("DXF:", OUT / f"{NAME}.dxf")
