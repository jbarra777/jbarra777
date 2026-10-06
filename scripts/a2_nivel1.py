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

REV = "rev3"
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

# ---------------------------------------------------------------- muros / tapias
# rev2: los muros de colindancia de la vivienda son la división en lindero (N1 incluido,
# hasta el entrepiso +3.00). Sin tapias laterales en los retiros.
pl.wall(msp, 0.0, E, ey0, ey1)                       # colindancia oeste
pl.wall(msp, W - E, W, ey0, ey1)                     # colindancia este
pl.wall(msp, X_PIL0, X_PIL1, ey0, Y_ROW)             # pilastra frontal (eje B)
Y_LP = LOC[5][1]                                      # lindero posterior (~28.51)
pl.wall(msp, 0.0, W, Y_LP - E, Y_LP)                 # tapia posterior (se mantiene de rev1)

# ---------------------------------------------------------------- columnas eje C
XC = 4.84                                             # eje C = centro de columnas
XCOL0, XCOL1 = XC - 0.15, XC + 0.15                   # cara oeste alineada con escalera
COLS = {"2": Y_P1a - E / 2, "3": Y_P1b + E / 2, "4": (Y4a + Y4b) / 2,
        "5": (Y5a + Y5b) / 2, "6": ey1 - 0.15}        # C-6 al ras de la fachada
for k, yc in COLS.items():
    pts = [P(XCOL0, yc - 0.15), P(XCOL1, yc - 0.15), P(XCOL1, yc + 0.15), P(XCOL0, yc + 0.15)]
    msp.add_lwpolyline(pts, close=True, dxfattribs={"layer": "E-COLUMNA"})
    hh = msp.add_hatch(color=7, dxfattribs={"layer": "E-COLUMNA"})
    hh.paths.add_polyline_path(pts)
    pl.text(msp, f"C{k}", XCOL1 + 0.12, yc + 0.25, 0.11, "E-COLUMNA", "MIDDLE_LEFT")
pl.text(msp, "COLUMNAS 0.30 x 0.30 (PRELIMINAR)", XCOL1 + 0.12, COLS["3"] + 0.75, 0.085,
        "E-COLUMNA", "MIDDLE_LEFT")

# ---------------------------------------------------------------- accesos
# portón vehicular abatible de 4 hojas plegables (2 por lado) hacia el retiro frontal
LEAF = (X_VEH1 - X_VEH0) / 4
pl.line(msp, (X_VEH0, ey0 + 0.03), (X_VEH1, ey0 + 0.03), "A-PROYECCION", pl.LT_DASH)
for hx, sgn in ((X_VEH0, 1), (X_VEH1, -1)):
    tip = ey0 - LEAF
    pl.line(msp, (hx, ey0), (hx, tip), "A-PUERTA")                       # hoja 1 abierta
    pl.line(msp, (hx + sgn * 0.06, tip), (hx + sgn * 0.06, ey0), "A-PUERTA")  # hoja 2 plegada
    pl.door(msp, (hx, ey0), LEAF, (sgn, 0), (0, -1))
pl.door(msp, (X_PED1, ey0), 1.00, (-1, 0), (0, 1))   # portón peatonal 1.00 hacia adentro

# ---------------------------------------------------------------- proyecciones superiores
for ya, yb in ((Y_P1a - E, Y_P1a), (Y_P1b, Y_P1b + E)):
    pl.poly(msp, [(E, ya), (W - E, ya), (W - E, yb), (E, yb)], "A-PROYECCION",
            ltscale=pl.LT_DASH)
for PP in (P1, P2):
    (xa, xb), (ya, yb) = PP["x"], PP["y"]
    pl.poly(msp, [(xa, ya), (xb, ya), (xb, yb), (xa, yb)], "A-PROYECCION", ltscale=pl.LT_DASH)
    pl.line(msp, (xa, ya), (xb, yb), "A-PROYECCION", pl.LT_DASH)
    pl.line(msp, (xb, ya), (xa, yb), "A-PROYECCION", pl.LT_DASH)
pl.line(msp, (E, ey1), (W - E, ey1), "A-PROYECCION", pl.LT_DASH)
pl.text(msp, "PROYECCIÓN BORDE NIVEL 2", 2.4, ey1 - 0.12, 0.085, "A-TXT-50", "MIDDLE_LEFT",
        rot=0)

# ---------------------------------------------------------------- estacionamientos E-1 a E-3
Y_E = Y_ROW + 5.0                                      # 7.21
pl.line(msp, (XB0, Y_ROW), (XB0, Y5a), "A-DEMARCACION", pl.LT_DASH)     # bordillo pasillo
pl.line(msp, (E, Y5a), (XB0, Y5a), "A-DEMARCACION", pl.LT_DASH)
pl.line(msp, (XB0, Y_E), (W - E, Y_E), "A-DEMARCACION", pl.LT_DASH)     # límite parqueo
for xs in (XB0 + 2.5, XB0 + 5.0):
    pl.line(msp, (xs, Y_ROW), (xs, Y_E), "A-DEMARCACION", pl.LT_DASH)
for k in range(3):
    xc = XB0 + 1.25 + 2.5 * k
    pl.car(msp, xc, Y_ROW + 2.6, front_dir=-1)
    pl.text(msp, f"E-{k + 1}", xc, Y_ROW + 2.3, 0.20, "A-ESPACIOS")

# ---------------------------------------------------------------- jardín seco
JS = [(XB0, Y_E), (W - E, Y_E), (W - E, ey1), (W, ey1), (W, Y_LP - E), (0.0, Y_LP - E),
      (0.0, ey1), (E, ey1), (E, Y5a), (XB0, Y5a)]
hole = [(XB0, Y4b), (X1 := ESC["x"][1], Y4b), (X1, Y5a), (XB0, Y5a)]
js = msp.add_hatch(dxfattribs={"layer": "A-JARDIN"})
js.paths.add_polyline_path([P(*q) for q in JS], flags=1)
js.paths.add_polyline_path([P(*q) for q in hole], flags=16)
js.set_pattern_fill("GRAVEL", scale=0.12)
for lab_y in (12.6, 22.0):
    pl.mtext(msp, "JARDÍN SECO\\P(NO CONSTRUIDO)", 3.0 if lab_y < 20 else 4.5, lab_y, 0.17,
             3.5, "A-ESPACIOS")

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
# rev3: vestíbulo de escalera cerrado (paredes Steel Tech 0.12) y puerta principal P-01
TV = 0.12
D_P01 = (0.25, 1.25)                                  # puerta principal 1.00 en el pasillo
pl.wall(msp, E, D_P01[0], Y4b - TV, Y4b)
pl.wall(msp, D_P01[1], XC1, Y4b - TV, Y4b)            # eje 4
pl.wall(msp, XC0, XC1, Y4b, Y5a)                      # eje C
pl.wall(msp, E, XC1, Y5a, Y5a + TV)                   # eje 5
pl.door(msp, (D_P01[0], Y4b), 1.00, (1, 0), (0, 1))
pl.text(msp, "VESTÍBULO", 0.45, 18.60, 0.12, "A-ESPACIOS")
pl.text(msp, "PUERTA PRINCIPAL (VER A7)", 0.75, Y4b - 0.40, 0.085, "A-TXT-50", "MIDDLE_RIGHT")
# flecha "SUBE"
a = P(X0 + 0.15, (yA0 + yA1) / 2)
b = P(CUT - 0.15, (yA0 + yA1) / 2)
msp.add_line(a, b, dxfattribs={"layer": "A-ESCALERA"})
msp.add_solid([b + Vec2(0.0, 0.0), b + Vec2(-0.12, -0.20), b + Vec2(0.12, -0.20)],
              dxfattribs={"layer": "A-ESCALERA"})
pl.text(msp, "SUBE", X0 + 0.55, (yA0 + yA1) / 2 + 0.18, 0.13, "A-ESCALERA")
pl.text(msp, "GRADAS EN U: 17 CH = 0.176 / H = 0.28", 5.10, Y4b + 0.05, 0.085, "A-TXT-50",
        "MIDDLE_LEFT")

# ---------------------------------------------------------------- textos
pl.text(msp, "PASILLO PEATONAL", 0.75, 4.6, 0.13, "A-ESPACIOS")
pl.text(msp, "PASILLO", 0.75, 12.0, 0.13, "A-ESPACIOS")
pl.mtext(msp, "BORDILLO DE DEMARCACIÓN", XB0 + 0.12, 3.6, 0.09, 1.0, "A-TXT-50", attach=4)
pl.text(msp, "PATIO P1 (ABIERTO A CIELO)", 8.67, Y_P1a + 0.1, 0.085, "A-TXT-50", "MIDDLE_LEFT")
pl.text(msp, "PATIO P2 (ABIERTO A CIELO)", 8.67, P2["y"][0] + 0.1, 0.085, "A-TXT-50",
        "MIDDLE_LEFT")
pl.mtext(msp, "PATIO POSTERIOR - JARDÍN SECO\\PTANQUE SÉPTICO Y DRENAJE (POR DISEÑAR)",
         4.5, 26.85, 0.13, 6.5, "A-ESPACIOS")
pl.text(msp, "CALLE PÚBLICA", 4.5, -2.15, 0.22, "A-ESPACIOS", rot=90)
pl.text(msp, "RETIRO FRONTAL", 6.4, 1.05, 0.12, "A-ESPACIOS", rot=90)
pl.text(msp, "PORTÓN ABATIBLE 4 HOJAS", 5.2, 1.35, 0.10, "A-TXT-50", rot=90)
pl.text(msp, "ACCESO PEATONAL", 0.70, 0.95, 0.08, "A-TXT-50", rot=90)
pl.mtext(msp, "COLINDANCIA - FACHADA CIEGA", 0.0 - 0.35, 14.0, 0.10, 6.0, "A-TXT-50")
pl.mtext(msp, "COLINDANCIA - FACHADA CIEGA", W + 0.35, 14.0, 0.10, 6.0, "A-TXT-50")

# niveles
pl.level(msp, 0.45, 8.3, "NPT ±0.00")
pl.level(msp, 6.2, 14.4, "NT ±0.00")
pl.level(msp, 7.6, 0.25, "ACERA ±0.00 (REF.)")

# ---------------------------------------------------------------- ejes
ejes_x = {"A": E / 2, "B": (XB0 + XB1) / 2, "C": XC, "D": W - E / 2}
ejes_y = {"1": ey0 + E / 2, "2": Y_P1a - E / 2, "3": Y_P1b + E / 2, "4": (Y4a + Y4b) / 2,
          "5": (Y5a + Y5b) / 2, "6": ey1 - E / 2}
for k, x in ejes_x.items():
    pl.axis(msp, k, "x", x, -0.2, 29.85, "end")
for k, y in ejes_y.items():
    pl.axis(msp, k, "y", y, -2.35, 10.2, "start")

# ---------------------------------------------------------------- cotas
for ya, yb in ((0.0, ey0), (ey0, ey1), (ey1, Y_LP)):
    pl.dim(msp, (0, ya), (0, yb), (-1.75, 0), False)
ys = list(ejes_y.values())
for ya, yb in zip(ys[:-1], ys[1:]):
    pl.dim(msp, (E / 2, ya), (E / 2, yb), (-1.15, 0), False)
chain = [ey0, Y_ROW, Y_E, ey1]
for ya, yb in zip(chain[:-1], chain[1:]):
    pl.dim(msp, (W - E, ya), (W - E, yb), (W + 0.95, 0), False)
pl.dim(msp, (W, ey0), (W, ey1), (W + 1.65, 0), False)
fx = [0.0, X_PED0, X_PED1, X_PIL1, X_VEH1, W]
for xa, xb in zip(fx[:-1], fx[1:]):
    pl.dim(msp, (xa, ey0), (xb, ey0), (0, -0.55), True)
pl.dim(msp, (0.0, ey0), (W, ey0), (0, -1.35), True)
for xa, xb in ((E, XB0), (XB0, XB0 + 2.5), (XB0 + 2.5, XB0 + 5.0), (XB0 + 5.0, W - E)):
    pl.dim(msp, (xa, Y_E), (xb, Y_E), (0, Y_E - 0.45), True)
pl.dim(msp, (X0, Y4b), (X1, Y4b), (0, Y4b - 0.45), True)
for ya, yb in ((Y4b, yA1), (yA1, yB0), (yB0, Y5a)):
    pl.dim(msp, (X1, ya), (X1, yb), (X1 - 0.45, 0), False)
xs = list(ejes_x.values())
for xa, xb in zip(xs[:-1], xs[1:]):
    pl.dim(msp, (xa, ey1), (xb, ey1), (0, 29.25), True)

# cortes
pl.section_mark(msp, "A", "A6", (3.0, -1.6), (3.0, 30.2), (1, 0))
pl.section_mark(msp, "B", "A6", (-2.0, 18.25), (11.05, 18.25), (0, 1))

# ---------------------------------------------------------------- hoja
psp = doc.layouts.new("A2-NIVEL1")
psp.page_setup(size=(cl.A1_W, cl.A1_H), margins=(0, 0, 0, 0), units="mm")
doc.layouts.set_active_layout("A2-NIVEL1")
cl.frame(psp)

VP_C = (368.0, 430.0)
VP_S = (668.0, 296.0)
vp = psp.add_viewport(center=VP_C, size=VP_S, view_center_point=(14.05, 4.05),
                      view_height=VP_S[1] * 50 / 1000.0, dxfattribs={"layer": "A-VIEWPORT"})
vp.dxf.flags = vp.dxf.flags | 16384
vp.frozen_layers = ["T-TXT-100", "T-TXT-200", "T-COTA-100", "T-COTA-200"]

# norte (bloque apunta a +Y en papel)
psp.add_blockref("NORTE", (672.0, 300.0), dxfattribs={"layer": "A-NORTE",
                                                       "rotation": north_ang - 90.0})
cl.text(psp, "NORTE SEGÚN CATASTRO", (672.0, 280.0), 1.8, "A-TEXTO", "TOP_CENTER")

cl.view_title(psp, 35.0, 262.0, "PLANTA NIVEL 1", "PARQUEOS, ACCESO, GRADAS Y JARDÍN SECO",
              "Esc. 1:50", 150)
cl.scale_bar(psp, 35.0, 236.0, 50, 5, 1)

# derrotero
y = 222.0
cl.text(psp, "D E R R O T E R O", (35 + 95, y), 5.0, "A-TITULOS", "TOP_CENTER")
y = cl.table(psp, 35.0, y - 8, [38.0] * 5, cl.derrotero_rows(V), row_h=6.0, h=2.5)
cl.text(psp, "VER CUADRO DE COORDENADAS CRTM05 EN LÁMINA A1.", (35.0, y - 2.0), 2.0,
        "A-TEXTO", "TOP_LEFT")

# cuadro de áreas (solo áreas construidas del nivel 1)
X2 = 240.0
y = 262.0
A_env = 9.0 * (ey1 - ey0)
A_pat = (P1["x"][1] - P1["x"][0]) * (Y_P1b - Y_P1a) + (P2["x"][1] - P2["x"][0]) * 2.5
A_huella = A_env - A_pat
A_cat = lote["area_catastro_m2"]
A_est = (W - E - XB0) * 5.0
L_pas = Y5a - Y_ROW
A_pas = (XB0 - E) * L_pas
A_gra = (X1 - X0) * (Y5a - Y4b)
A_n1 = A_est + A_pas + A_gra
cl.text(psp, "CUADRO DE ÁREAS NIVEL 1", (X2 + 100, y), 4.5, "A-TITULOS", "TOP_CENTER")
rows = [["ESPACIO", "ÁREA"],
        ["ESTACIONAMIENTOS E-1 A E-3 (7,50 x 5,00)", cl.m2(A_est)],
        [f"PASILLO PEATONAL (1,20 x {L_pas:.2f})".replace(".", ","), cl.m2(A_pas)],
        [f"GRADAS ({X1 - X0:.2f} x {Y5a - Y4b:.2f})".replace(".", ","), cl.m2(A_gra)],
        ["ÁREA CONSTRUIDA NIVEL 1", cl.m2(A_n1)]]
y = cl.table(psp, X2, y - 8, [140, 60], rows, row_h=6.0, h=2.5,
             aligns=["MIDDLE_LEFT", "MIDDLE_RIGHT"])
cl.mtext(psp, "EL RESTO DEL NIVEL 1 ES JARDÍN SECO NO CONSTRUIDO. ÁREAS DE LOS NIVELES 2 Y 3 "
         "EN LÁMINAS A3 Y A4.", (X2, y - 1.5), 2.0, 200)
y -= 14
cl.text(psp, "PORCENTAJE DE COBERTURA", (X2 + 100, y), 4.5, "A-TITULOS", "TOP_CENTER")
rows = [["CONCEPTO", "VALOR"],
        ["ÁREA DE LOTE (SEGÚN CATASTRO)", cl.m2(A_cat)],
        ["HUELLA CONSTRUCTIVA (PROYECCIÓN NIVELES 2 Y 3)", cl.m2(A_huella)],
        ["% COBERTURA", f"{A_huella / A_cat * 100:.2f} %".replace(".", ",")]]
y = cl.table(psp, X2, y - 8, [140, 60], rows, row_h=6.0, h=2.5,
             aligns=["MIDDLE_LEFT", "MIDDLE_RIGHT"])
cl.text(psp, f"CÁLCULO: (HUELLA / ÁREA DE LOTE) x 100 = ({A_huella:.2f} / {A_cat:.2f}) x 100 = "
        f"{A_huella / A_cat * 100:.2f} %".replace(".", ","), (X2, y - 1.5), 2.0, "A-TEXTO",
        "TOP_LEFT")

# notas
X3 = 455.0
y = 262.0
cl.text(psp, "NOTAS:", (X3, y), 3.5, "A-TITULOS", "TOP_LEFT")
extra = [
    "NIVEL 1: 3 ESTACIONAMIENTOS INDEPENDIENTES DE 2.50 x 5.00 m (E-1 A E-3), CON ACCESO "
    "RECTO DESDE LA CALLE.",
    "PORTÓN VEHICULAR ABATIBLE DE 4 HOJAS PLEGABLES (2 POR LADO), CLARO LIBRE 7.29 m, CON "
    "APERTURA HACIA EL RETIRO FRONTAL SIN INVADIR LA VÍA PÚBLICA. ACCESO PEATONAL DE 1.00 m.",
    "COLUMNAS SOBRE EL EJE C EN LOS EJES 2 A 6 (SECCIÓN 0.30 x 0.30 PRELIMINAR, CARA OESTE "
    "ALINEADA CON LA ESCALERA; C6 AL RAS DE LA FACHADA POSTERIOR). SIN COLUMNA EN C1 PARA NO "
    "OBSTRUIR EL ACCESO VEHICULAR. SECCIONES Y REFUERZO SEGÚN PLANOS ESTRUCTURALES.",
    "LAS ÁREAS NO INDICADAS COMO ESTACIONAMIENTO, PASILLO O GRADAS SON JARDÍN SECO NO "
    "CONSTRUIDO: BAJO LOS NIVELES 2 Y 3, EN LOS PATIOS P1 Y P2 Y EN EL PATIO POSTERIOR.",
    "NPT ±0.00 = NIVEL DE ACERA (TERRENO PLANO). PENDIENTES Y DESAGÜES SEGÚN LÁMINAS "
    "SANITARIAS.",
    "LOS MUROS DE COLINDANCIA DE LA VIVIENDA SON LA DIVISIÓN CON LOS PREDIOS VECINOS. EN EL "
    "NIVEL 1 SON MUROS CONTINUOS HASTA EL NIVEL DE ENTREPISO (+3.00). NO SE CONSTRUYEN TAPIAS "
    "LATERALES EN LOS RETIROS.",
    "VESTÍBULO DE ESCALERA CERRADO CON PAREDES STEEL TECH DE 0.12 m EN LOS EJES 4, C Y 5; "
    "PUERTA PRINCIPAL P-01 DE MADERA EN EL PASILLO. PUERTAS, VENTANAS Y ACABADOS EN LÁMINA A7.",
]
cl.notes_block(psp, X3, y - 6, cl.notas(extra), 2.1, 250)

# cajetín
vals = {
    "EMPRESA": prj["empresa"], "EMPRESA_CED": prj["empresa_ced"],
    "PROF_1": prj["profesionales"][0], "PROF_2": prj["profesionales"][1],
    "PROF_3": prj["profesionales"][2],
    "PROYECTO": prj["proyecto"], "UBIC_1": prj["ubicacion"][0], "UBIC_2": prj["ubicacion"][1],
    "UBIC_3": "",
    "REG_1": prj["registro"][0], "REG_2": prj["registro"][1], "REG_3": prj["registro"][2],
    "CONT_TIT": "PLANTA NIVEL 1",
    "CONT_1": "PARQUEOS, ACCESO Y GRADAS.", "CONT_2": "DERROTERO.",
    "CONT_3": "CUADRO DE ÁREAS.", "CONT_4": "PORCENTAJE DE COBERTURA.", "CONT_5": "NOTAS.",
    "CONT_6": "",
    "ESCALAS": "1:50 / INDICADAS",
    "REV0_N": "1", "REV0_F": "06-10-2026",
    "REV0_D": "3 PARQUEOS, JARDÍN SECO, PORTÓN, COLUMNAS EJE C",
    "REV1_N": "2", "REV1_F": "06-10-2026", "REV1_D": "SIN TAPIAS LATERALES; MUROS DE COLINDANCIA N1",
    "REV2_N": "3", "REV2_F": "06-10-2026", "REV2_D": "VESTÍBULO DE ESCALERA Y PUERTA PRINCIPAL",
    "ESTADO_1": "VERSIÓN DE TRABAJO", "ESTADO_2": "NO APTA PARA CONSTRUCCIÓN NI TRÁMITE",
    "LUGAR": "COSTA RICA", "LAMINA": "A2", "FECHA": prj["fecha"], "TOTAL": prj["total_laminas"],
}
cl.insert_titleblock(doc, psp, vals)

OUT.mkdir(parents=True, exist_ok=True)
doc.saveas(OUT / f"{NAME}.dxf")
cl.render_pdf(doc, "A2-NIVEL1", OUT / f"{NAME}.pdf", OUT / f"{NAME}.png", dpi=110)
print("N1: est", A_est, "pasillo", round(A_pas, 2), "gradas", round(A_gra, 2), "total",
      round(A_n1, 2), "| huella", round(A_huella, 2), "| hoja portón", round(LEAF, 3))
print("DXF:", OUT / f"{NAME}.dxf")
