"""Lámina A11 - ESCALERA: planta, corte y detalles de escalera, baranda y pasamanos.

Organización y textos de baranda/pasamanos tomados de la lámina ARQ_11 de la referencia
por indicación del usuario ("usar la misma lámina del proyecto de referencia"): se marcan
[PR]. La geometría es la de esta vivienda: escalera en U de 17 contrahuellas de 0.176 y
huella de 0.28, tramos de 1.10, ojo de 0.30, descanso de 1.10 x 2.50, vestíbulo cerrado en
N1 (A2 rev3), piso a piso 3.00, entrepiso de 0.30 (A6).
Model Space en metros. Planta en marco local (x a la derecha, y hacia abajo).
"""
import cadlib as cl
import hoja as H

REV = "rev1"
OUT = cl.ROOT / "planos" / "A11_escalera"
NAME = f"SR-A11_ESCALERA_{REV}"

E = H.E
ESC = H.ESC
X0, X1 = ESC["x"]                       # 1.35 / 4.69
Y0, Y1 = ESC["y"]                       # 16.98 / 19.48
R = 3.00 / 17
TH = 0.28
X_DES = X0 + 8 * TH                     # 3.59
yA1 = Y0 + 1.10                         # 18.08
yB0 = Y1 - 1.10                         # 18.38
XC1 = H.P2["x"][0]                      # 4.81
TV = 0.12
LOSA, VIGA = 0.10, 0.20
BAR, PAS, BARRAS = 1.07, 0.90, 0.92     # alturas [PR]

doc = cl.new_doc()
msp = doc.modelspace()
for name, col, lw, lt in (("S-CORTE", 7, 50, "Continuous"), ("S-VISTA", 7, 25, "Continuous"),
                          ("S-OCULTO", 8, 13, "DASHED"), ("S-TRAMA", 8, 9, "Continuous"),
                          ("S-BARANDA", 7, 25, "Continuous"), ("S-TXT", 7, 18, "Continuous"),
                          ("S-COTA", 7, 18, "Continuous")):
    doc.layers.add(name, color=col, linetype=lt, lineweight=lw)
for sc in (10, 25):
    if f"COTA-{sc}" not in doc.dimstyles:
        cl._dimstyle(doc, f"COTA-{sc}", sc)


class V:
    """Vista en Model Space con origen propio y escala de dibujo."""

    def __init__(self, ox, oy, scale, flip_y=False):
        self.ox, self.oy, self.sc, self.fy = ox, oy, scale, flip_y
        self.k = scale / 1000.0

    def p(self, x, y):
        return (self.ox + x, self.oy + (-y if self.fy else y))

    def line(self, a, b, layer="S-VISTA", lts=None):
        e = msp.add_line(self.p(*a), self.p(*b), dxfattribs={"layer": layer})
        if lts:
            e.dxf.ltscale = lts
        return e

    def poly(self, pts, layer="S-VISTA", close=False):
        return msp.add_lwpolyline([self.p(*q) for q in pts], close=close, dxfattribs={"layer": layer})

    def rect(self, x0, y0, x1, y1, layer="S-VISTA"):
        return self.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], layer, True)

    def fill(self, x0, y0, x1, y1, pattern=None, scale=1.0, color=7, layer="S-CORTE"):
        pts = [self.p(x0, y0), self.p(x1, y0), self.p(x1, y1), self.p(x0, y1)]
        ht = msp.add_hatch(color=color, dxfattribs={"layer": "S-TRAMA" if pattern else layer})
        ht.paths.add_polyline_path(pts)
        if pattern:
            ht.set_pattern_fill(pattern, scale=scale)
        msp.add_lwpolyline(pts, close=True, dxfattribs={"layer": layer})

    def fillpoly(self, pts, pattern=None, scale=1.0, color=8):
        q = [self.p(*a) for a in pts]
        ht = msp.add_hatch(color=color, dxfattribs={"layer": "S-TRAMA" if pattern else "S-CORTE"})
        ht.paths.add_polyline_path(q)
        if pattern:
            ht.set_pattern_fill(pattern, scale=scale)
        msp.add_lwpolyline(q, close=True, dxfattribs={"layer": "S-CORTE"})

    def text(self, s, x, y, size_mm=2.0, align="MIDDLE_CENTER", rot=0):
        return cl.text(msp, s, self.p(x, y), size_mm * self.k, "S-TXT", align, rot)

    def dim(self, a, b, base, horizontal, style):
        if horizontal:
            d = msp.add_linear_dim(base=self.p(0, base), p1=self.p(a, base), p2=self.p(b, base),
                                   angle=0, dimstyle=style, dxfattribs={"layer": "S-COTA"})
        else:
            d = msp.add_linear_dim(base=self.p(base, 0), p1=self.p(base, a), p2=self.p(base, b),
                                   angle=90, dimstyle=style, dxfattribs={"layer": "S-COTA"})
        d.render()


# ================================================================ PLANTA (1:25), nivel 1
PL = V(0.0, 0.0, 25, flip_y=True)
# muros
PL.fill(0.0, Y0 - 0.40, E, Y1 + 0.40, "ANSI31", 0.6 * 0.008)                  # lindero (mampostería)
for x0, x1, y0, y1 in ((E, 0.25, Y0 - TV, Y0), (1.25, XC1, Y0 - TV, Y0),       # eje 4
                       (X1, XC1, Y0, Y1), (E, XC1, Y1, Y1 + TV)):              # eje C / eje 5
    PL.rect(x0, y0, x1, y1, "S-CORTE")
    PL.line(((x0 + x1) / 2 if x1 - x0 < 0.2 else x0 + 0.03, (y0 + y1) / 2 if y1 - y0 < 0.2 else y0 + 0.03),
            ((x0 + x1) / 2 if x1 - x0 < 0.2 else x1 - 0.03, (y0 + y1) / 2 if y1 - y0 < 0.2 else y1 - 0.03),
            "S-OCULTO", 0.3 * PL.k)
for yc in (H.EJES_Y["4"], H.EJES_Y["5"]):                                       # columnas C4, C5
    PL.fill(X1, yc - 0.15, X1 + 0.30, yc + 0.15)
# puerta principal P-01
PL.line((0.25, Y0), (0.25, Y0 + 1.00), "S-BARANDA")
arc = msp.add_arc(PL.p(0.25, Y0), 1.00, 270, 360, dxfattribs={"layer": "S-VISTA"})
# tramo 1 (sube hacia el este) y tramo 2 (regresa al oeste)
for k in range(9):
    PL.line((X0 + k * TH, Y0), (X0 + k * TH, yA1))
PL.line((X0, yA1), (X_DES, yA1))
for k in range(8):
    PL.line((X_DES - k * TH, yB0), (X_DES - k * TH, Y1))
PL.line((X_DES - 7 * TH, yB0), (X_DES, yB0))
PL.line((X_DES, Y0), (X_DES, Y1))
# barandas del ojo y pasamanos a pared (a 0.08 de la pared)
for yy in (yA1 + 0.03, yB0 - 0.03):
    PL.line((X0 + 0.15 if yy < 18.2 else X_DES - 7 * TH, yy), (X_DES, yy), "S-BARANDA")
PL.line((X_DES, yA1 + 0.03), (X_DES, yB0 - 0.03), "S-BARANDA")
for (a, b) in (((X0, Y0 + 0.08), (X1 - 0.08, Y0 + 0.08)), ((X1 - 0.08, Y0 + 0.08), (X1 - 0.08, Y1 - 0.08)),
               ((X1 - 0.08, Y1 - 0.08), (X_DES - 7 * TH, Y1 - 0.08))):
    PL.line(a, b, "S-OCULTO", 0.3 * PL.k)
# flecha sube
PL.line((X0 + 0.15, (Y0 + yA1) / 2), (X_DES - 0.20, (Y0 + yA1) / 2), "S-VISTA")
tip = PL.p(X_DES - 0.20, (Y0 + yA1) / 2)
msp.add_solid([tip, (tip[0] - 0.15, tip[1] + 0.07), (tip[0] - 0.15, tip[1] - 0.07)],
              dxfattribs={"layer": "S-VISTA"})
PL.text("SUBE", X0 + 0.55, (Y0 + yA1) / 2 - 0.18, 2.2)
PL.text("DESCANSO +1.59", (X_DES + X1) / 2, (Y0 + Y1) / 2, 2.2, rot=90)
PL.text("VESTÍBULO", 0.75, 18.40, 2.4, rot=90)
PL.text("P-01", 0.75, Y0 - 0.45, 2.2)
PL.text("TRAMO 1: 9 CH", 2.45, yA1 - 0.22, 1.8)
PL.text("TRAMO 2: 8 CH", 2.45, yB0 + 0.22, 1.8)
PL.text("OJO 0.30 - BARANDA", 2.45, (yA1 + yB0) / 2, 1.6)
# cotas
for k in range(8):
    PL.dim(X0 + k * TH, X0 + (k + 1) * TH, Y0 - 0.55, True, "COTA-25")
PL.dim(X_DES, X1, Y0 - 0.55, True, "COTA-25")
PL.dim(X0, X1, Y0 - 0.95, True, "COTA-25")
PL.dim(E, X0, Y1 + 0.50, True, "COTA-25")
for a, b in ((Y0, yA1), (yA1, yB0), (yB0, Y1)):
    PL.dim(a, b, XC1 + 0.45, False, "COTA-25")
PL.dim(Y0, Y1, XC1 + 0.85, False, "COTA-25")

# ================================================================ CORTE (1:25), vista al eje 4
CO = V(10.0, 0.0, 25)
NOS = lambda x: R + (x - X0) * R / TH                       # línea de narices del tramo 1
CO.line((-0.3, 0.0), (5.3, 0.0), "S-CORTE")
CO.fill(0.0, -0.10, X1 + 0.30, 0.0, color=8)                # contrapiso (corte)
CO.fill(0.0, -0.10, E, 4.20, "ANSI31", 0.6 * 0.008)         # lindero oeste (mampostería)
CO.rect(X1, 0.0, XC1, 3.00 - LOSA, "S-CORTE")               # pared eje C (Steel Tech)
CO.rect(X1, 3.00, XC1, 4.20, "S-CORTE")
CO.fill(E, 3.00 - LOSA, X0, 3.00, color=8)                  # losa N2 (pasillo, corte)
CO.fill(X0 - 0.15, 3.00 - LOSA - VIGA, X0, 3.00 - LOSA)     # viga de borde
CO.rect(E, 0.0, X1, 3.00 - LOSA - VIGA, "S-VISTA")          # pared del eje 4 en vista (fondo)
# tramo 1 en vista
pts = [(X0, 0.0)]
for k in range(9):
    x = X0 + k * TH
    pts += [(x, (k + 1) * R), (x + TH if k < 8 else X_DES, (k + 1) * R)]
pts += [(X_DES, 9 * R - 0.15), (X0 + 0.04, 0.0)]
CO.fillpoly(pts, color=8)
CO.fill(X_DES, 9 * R - 0.15, X1, 9 * R, color=8)            # descanso (corte)
# tramo 2 detrás del plano de corte (oculto)
pts = [(X_DES, 9 * R)]
x = X_DES
for j in range(8):
    pts.append((x, (10 + j) * R))
    if j < 7:
        x -= TH
        pts.append((x, (10 + j) * R))
pts.append((X0, 17 * R))
CO.poly(pts, "S-OCULTO").dxf.ltscale = 0.3 * CO.k
# baranda del tramo 1 (lado del ojo)
for x in (X0 + 0.10, X0 + 1.05, X0 + 2.00, X_DES + 0.05):
    v0 = NOS(min(x, X_DES - 0.01)) if x < X_DES else 9 * R
    vt = (NOS(x) if x < X_DES else 9 * R) + BAR
    CO.rect(x - 0.025, v0, x + 0.025, vt, "S-BARANDA")       # tubo pedestal Ø50.8
for i in range(1, 10):
    dv = i * BARRAS / 9.2 if i < 9 else BARRAS
    dv = round(0.10 * i, 2) if 0.10 * i <= BARRAS else BARRAS
    CO.poly([(X0 + 0.10, NOS(X0 + 0.10) + dv), (X_DES, NOS(X_DES) + dv), (X1 - 0.05, 9 * R + dv)],
            "S-BARANDA")
CO.poly([(X0 + 0.10, NOS(X0 + 0.10) + BAR), (X_DES, NOS(X_DES) + BAR), (X1 - 0.05, 9 * R + BAR)],
        "S-CORTE")                                          # barandal 1.07
CO.poly([(X0 - 0.10, NOS(X0) + PAS - 0.15), (X0, NOS(X0) + PAS), (X_DES, NOS(X_DES) + PAS),
         (X1 - 0.05, 9 * R + PAS)], "S-BARANDA")             # pasamanos 0.90 (remate al piso)
# baranda en el borde del pasillo N2 (vista de canto)
CO.rect(X0 - 0.025, 3.00, X0 + 0.025, 3.00 + BAR, "S-BARANDA")
# niveles y cotas
for v, lab in ((0.0, "NPT ±0.00"), (9 * R, "DESCANSO +1.59"), (3.00, "NPT +3.00")):
    CO.line((XC1 + 0.10, v), (XC1 + 0.90, v), "S-VISTA")
    CO.text(lab, XC1 + 0.15, v + 0.10, 2.0, "BOTTOM_LEFT")
CO.dim(0.0, 9 * R, -0.30, False, "COTA-25")
CO.dim(9 * R, 3.00, -0.30, False, "COTA-25")
CO.dim(0.0, 3.00, -0.62, False, "COTA-25")
CO.dim(X0, X0 + TH, -0.30, True, "COTA-25")
CO.dim(X0 + TH, X0 + 2 * TH, -0.30, True, "COTA-25")
CO.dim(X0, X_DES, -0.65, True, "COTA-25")
CO.dim(X_DES, X1, -0.65, True, "COTA-25")
CO.dim(0.0, R, X0 - 0.25, False, "COTA-25")

# ================================================================ DETALLE ESCALÓN (1:10)
DE = V(20.0, 0.0, 10)
pts = [(0.0, 0.0), (0.0, 0.15)]
for k in range(3):
    pts += [(0.30 + k * TH, 0.15 + k * R), (0.30 + k * TH, 0.15 + (k + 1) * R)]
pts += [(0.30 + 3 * TH + 0.10, 0.15 + 3 * R), (0.30 + 3 * TH + 0.10, 0.15 + 3 * R - 0.12),
        (0.30, 0.15 - 0.12 - 0.05), (0.30, 0.0)]
DE.fillpoly(pts, "AR-CONC", 0.004, color=8)
DE.line((0.05, 0.05), (0.30 + 3 * TH, 0.15 + 3 * R - 0.08), "S-CORTE")      # refuerzo esquemático
for k in range(3):
    x0 = 0.30 + k * TH
    DE.line((x0 - 0.015, 0.15 + (k + 1) * R + 0.015), (x0 + TH, 0.15 + (k + 1) * R + 0.015), "S-VISTA")
DE.dim(0.30, 0.30 + TH, 0.15 + 3 * R + 0.25, True, "COTA-10")
DE.dim(0.15 + 2 * R, 0.15 + 3 * R, 0.30 + 3 * TH + 0.25, False, "COTA-10")

# ================================================================ DETALLE ANCLAJE PASAMANOS (1:10)
AN = V(23.0, 0.25, 10)
msp.add_circle(AN.p(0, 0), 0.050, dxfattribs={"layer": "S-CORTE"})
msp.add_circle(AN.p(0, 0), 0.045, dxfattribs={"layer": "S-VISTA"})
ht = msp.add_hatch(dxfattribs={"layer": "S-TRAMA"})
ht.paths.add_edge_path().add_arc(AN.p(0, 0), 0.020, 0, 360)
ht.set_pattern_fill("ANSI31", scale=0.002)
msp.add_circle(AN.p(0, 0), 0.020, dxfattribs={"layer": "S-CORTE"})
for ang in (90, 210, 330):
    import math
    c = AN.p(0.033 * math.cos(math.radians(ang)), 0.033 * math.sin(math.radians(ang)))
    msp.add_circle(c, 0.005, dxfattribs={"layer": "S-VISTA"})

# ================================================================ DETALLE BARANDA (1:10)
BD = V(26.0, 0.0, 10)
BD.fill(-0.10, -0.06, 1.40, 0.0, "AR-CONC", 0.004, color=8)
for x in (0.10, 1.20):
    BD.rect(x - 0.025, 0.0, x + 0.025, BAR, "S-BARANDA")
for i in range(1, 10):
    v = min(round(0.10 * i, 2), BARRAS)
    BD.line((0.125, v), (1.175, v), "S-BARANDA")
BD.rect(0.075, BAR - 0.02, 1.225, BAR + 0.02, "S-CORTE")                    # barandal
BD.rect(-0.05, PAS - 0.02, 1.35, PAS + 0.02, "S-BARANDA")                    # pasamanos
BD.dim(0.0, BAR, -0.25, False, "COTA-10")
BD.dim(0.0, PAS, -0.12, False, "COTA-10")
BD.dim(0.0, 0.10, 1.32, False, "COTA-10")

# ================================================================ hoja
psp = doc.layouts.new("A11-ESCALERA")
psp.page_setup(size=(cl.A1_W, cl.A1_H), margins=(0, 0, 0, 0), units="mm")
doc.layouts.set_active_layout("A11-ESCALERA")
cl.frame(psp)
VPS = {}


def vp(key, view, center, size, mc):
    v = psp.add_viewport(center=center, size=size, view_center_point=mc,
                         view_height=size[1] * view.sc / 1000.0, dxfattribs={"layer": "A-VIEWPORT"})
    v.dxf.flags = v.dxf.flags | 16384
    VPS[key] = (view, center, mc)


def to_paper(key, x, y):
    view, c, mc = VPS[key]
    mx, my = view.p(x, y)
    f = 1000.0 / view.sc
    return (c[0] + (mx - mc[0]) * f, c[1] + (my - mc[1]) * f)


def callout(key, target, txt_pos, lines, h=1.9, width=95.0):
    tx, ty = to_paper(key, *target)
    psp.add_line((txt_pos[0] - 2.0, txt_pos[1]), (tx, ty), dxfattribs={"layer": "A-TEXTO"})
    psp.add_circle((tx, ty), 0.6, dxfattribs={"layer": "A-TEXTO"})
    cl.mtext(psp, lines, txt_pos, h, width, layer="A-TEXTO", attach=4)


vp("PL", PL, (165.0, 490.0), (270.0, 175.0), PL.p(2.60, 18.10))
cl.view_title(psp, 35.0, 395.0, "PLANTA DE ESCALERA", "NIVEL 1 (VESTÍBULO); NIVELES 2 Y 3 IGUALES",
              "Esc. 1:25", 150)
vp("CO", CO, (165.0, 262.0), (270.0, 215.0), (10.0 + 2.50, 1.75))
cl.view_title(psp, 35.0, 143.0, "CORTE DE ESCALERA (EN EL OJO, VISTA HACIA EL EJE 4)",
              "TRAMO NIVEL 1 A NIVEL 2; TRAMO NIVEL 2 A NIVEL 3 IGUAL", "Esc. 1:25", 190)
# rótulos de baranda y pasamanos [PR] (textos de la referencia)
TXT = [
    ((X0 + 2.00, NOS(X0 + 2.0) + BAR), "BARANDAL A 1,07m DE ALTURA CON RESPECTO AL NIVEL DE PISO TERMINADO. [PR]"),
    ((X0 + 1.40, NOS(X0 + 1.40) + PAS), "PASAMANOS A 90cm DE ALTURA CON RESPECTO AL NIVEL DE PISO TERMINADO. [PR]"),
    ((X0 + 1.70, NOS(X0 + 1.70) + 0.50), "BARRAS INTERMEDIAS A CADA 10cm, HASTA UNA ALTURA DE 92cm CON RESPECTO "
     "AL NIVEL DE PISO TERMINADO, EN TUBO REDONDO DE 12,7mm DE DIÁMETRO X 1,5mm DE ESPESOR. [PR]"),
    ((X0 + 1.05, NOS(X0 + 1.05) + 0.30), "TUBO PEDESTAL DE 50,8mm DE DIÁMETRO X 2mm DE ESPESOR, CON SOPORTE "
     "DE PASAMANOS Y FLANGER INFERIOR O SIMILAR. [PR]"),
    ((X0 - 0.08, NOS(X0) + PAS - 0.12), "EL EXTREMO INFERIOR DEL PASAMANOS REMATA HACIA EL PISO. [PR]"),
    ((X1 - 0.30, 9 * R + PAS), "PASAMANOS CONTINUO EN TODO SU RECORRIDO, INCLUIDO EL DESCANSO. [PR]"),
]
ys = [366.0, 352.0, 336.0, 318.0, 302.0, 288.0]
for (target, s), yy in zip(TXT, ys):
    callout("CO", target, (302.0, yy), s, 1.9, 128.0)
cl.mtext(psp, "SISTEMA DE PASAMANOS EN ACERO INOXIDABLE SS 304 ACABADO INOXIDABLE O SIMILAR. DEBE INCLUIR TODOS LOS ACCESORIOS "
         "(CONECTORES, TUBOS, TAPAS, SOPORTES, ETC.) DEL SISTEMA, ASÍ COMO TODOS LOS COMPONENTES "
         "NECESARIOS PARA SU ADECUADA INSTALACIÓN. EL PASAMANOS PERIMETRAL DE FIJACIÓN A PARED DEBE "
         "SER CONTINUO EN TODO SU RECORRIDO, INCLUIDO EL DESCANSO. [PR]",
         (302.0, 274.0), 1.9, 128.0, layer="A-TEXTO", attach=1)
cl.mtext(psp, "PASAMANOS A PARED: TUBO DE 42,4mm DE DIÁMETRO X 1,5mm DE ESPESOR O SIMILAR, SEPARADO "
         "8cm DE LA PARED, CON SOPORTES ANCLADOS A PARED DE 1,5mm DE ESPESOR O SIMILAR. [PR]",
         (302.0, 246.0), 1.9, 128.0, layer="A-TEXTO", attach=1)
# detalles
vp("DE", DE, (520.0, 520.0), (170.0, 100.0), (20.0 + 0.70, 0.42))
cl.text(psp, "DETALLE DE ESCALÓN", (440.0, 470.0), 4.0, "A-TITULOS", "TOP_LEFT")
cl.text(psp, "Esc. 1:10", (440.0, 464.0), 2.5, "A-TEXTO", "TOP_LEFT")
cl.mtext(psp, "LOSA DE ESCALERA DE CONCRETO ARMADO; ESPESOR Y REFUERZO SEGÚN PLANOS ESTRUCTURALES "
         "(PD). CONTRAHUELLA 0,176 m Y HUELLA 0,28 m. ACABADO DE GRADAS: PORCELANATO PI-A "
         "ANTIDESLIZANTE CON NARIZ (VER A7).",
         (440.0, 456.0), 1.9, 140.0, layer="A-TEXTO", attach=1)
vp("AN", AN, (640.0, 520.0), (60.0, 60.0), AN.p(0, 0))
cl.text(psp, "ANCLAJE DE PASAMANOS", (612.0, 486.0), 3.0, "A-TITULOS", "TOP_LEFT")
cl.text(psp, "Esc. 1:10", (612.0, 481.0), 2.2, "A-TEXTO", "TOP_LEFT")
for tgt, pos, s in (((0.0, 0.05), (655.0, 555.0), "ANCLAJE SUPERIOR APROBADO PARA LA FIJACIÓN DEL PASAMANOS [PR]"),
                    ((0.0, 0.0), (668.0, 528.0), "VARILLA [PR]"),
                    ((0.035, -0.035), (655.0, 500.0), "PLACA DE HIERRO NEGRO BISELADO DE 4,8mm DE ESPESOR [PR]")):
    callout("AN", tgt, pos, s, 1.6, 40.0)
vp("BD", BD, (560.0, 330.0), (230.0, 150.0), (26.0 + 0.65, 0.55))
cl.text(psp, "DETALLE DE BARANDA Y PASAMANOS", (445.0, 250.0), 4.0, "A-TITULOS", "TOP_LEFT")
cl.text(psp, "Esc. 1:10", (445.0, 244.0), 2.5, "A-TEXTO", "TOP_LEFT")
for tgt, pos, s in (((0.60, BAR), (600.0, 405.0), "BARANDAL A 1,07m (PASAMANOS CONTINUO DE SECCIÓN CIRCULAR DE 4cm) [PR]"),
                    ((1.30, PAS), (640.0, 392.0), "PASAMANOS A 0,90m, SEPARADO DE LA BARANDA 5cm [PR]"),
                    ((0.60, 0.50), (640.0, 360.0), "BARRAS INTERMEDIAS A CADA 10cm HASTA 0,92m [PR]"),
                    ((0.10, 0.30), (600.0, 280.0), "TUBO PEDESTAL Ø 50,8mm [PR]")):
    callout("BD", tgt, pos, s, 1.8, 60.0)
cl.mtext(psp, "DISEÑO DE LAS BARANDAS Y PASAMANOS DE FORMA TAL QUE NO HAYA PROYECCIONES QUE PUEDAN "
         "ENGANCHARSE A LAS ROPAS SUELTAS. [PR]", (445.0, 236.0), 1.9, 240.0, layer="A-TEXTO", attach=1)
# notas
X3, y = 445.0, 222.0
cl.text(psp, "NOTAS:", (X3, y), 3.5, "A-TITULOS", "TOP_LEFT")
notas = [
    "TODAS LAS MEDIDAS ESTÁN DADAS EN METROS, SALVO INDICACIÓN CONTRARIA. [PR]",
    "ESCALERA EN U ENTRE EL NIVEL 1 Y EL NIVEL 3: 17 CONTRAHUELLAS DE 0,176 m Y HUELLA DE 0,28 m POR "
    "NIVEL (TRAMO 1: 9 CH; TRAMO 2: 8 CH); ANCHO DE TRAMO 1,10 m; OJO 0,30 m; DESCANSO 1,10 x 2,50 m "
    "A +1,59 (N1-N2) Y +4,59 (N2-N3).",
    "EN EL NIVEL 1 LA ESCALERA QUEDA EN EL VESTÍBULO CERRADO (PAREDES STEEL TECH 0,12 m, PUERTA "
    "PRINCIPAL P-01). BARANDA EN EL OJO DE LA ESCALERA Y EN EL BORDE DEL PASILLO HACIA EL VACÍO EN "
    "LOS NIVELES 2 Y 3; PASAMANOS A PARED EN EL LADO EXTERIOR DE LOS TRAMOS.",
    "GRADAS Y DESCANSOS CON ACABADO DE PORCELANATO PI-A ANTIDESLIZANTE CON NARIZ.",
    "ESTRUCTURA DE LA ESCALERA SEGÚN PLANOS ESTRUCTURALES.",
]
cl.notes_block(psp, X3, y - 6, [f"{i}.- {t}" for i, t in enumerate(notas, 1)] + [cl.NOTA_PR], 2.0, 250)

H.titleblock(doc, psp, "A11", "ESCALERA",
             ["PLANTA.", "CORTE.", "DETALLES DE ESCALÓN, BARANDA", "Y PASAMANOS.", "NOTAS.", ""],
             [("0", "06-10-2026", "VERSIÓN DE TRABAJO PARA REVISIÓN"),
              ("1", "06-10-2026", "ACABADO DE GRADAS; SIN CITAS NI MARCAS")], escalas="INDICADAS")

OUT.mkdir(parents=True, exist_ok=True)
doc.saveas(OUT / f"{NAME}.dxf")
cl.render_pdf(doc, "A11-ESCALERA", OUT / f"{NAME}.pdf")
print("DXF:", OUT / f"{NAME}.dxf")
