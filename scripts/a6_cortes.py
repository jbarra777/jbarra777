"""Lámina A6 - CORTES A-A y B-B (Esc. 1:75).

Trazos según plantas A2-A4: A-A longitudinal en x = 3.0 (vista hacia el este, frente a la
izquierda); B-B transversal en y = 18.25 (vista hacia el fondo, este a la izquierda).
Datos del usuario: piso a piso 3.00, cielo raso a 2.70 en N2 y N3, entrepiso de estructura
metálica (vigas de acero + lámina colaborante con sobrelosa), cubierta de lámina cal. 26 a
dos aguas al 13 %, tapia posterior hasta la viga corona (+9.00).
Espesores de entrepiso (0.10 sobrelosa / 0.20 viga), alturas de puertas (2.10) y de
ventanas a patios (0.90-2.20) son PD.
Model Space en metros: cada corte en su propio origen (H horizontal, V = altura).
"""
import math

import cadlib as cl
import hoja as H

REV = "rev0"
OUT = cl.ROOT / "planos" / "A6_cortes"
NAME = f"SR-A6_CORTES_{REV}"

W, E = H.W, H.E
EY0, EY1, Y_LP = H.EY0, H.EY1, H.Y_LP
P1, P2, ESC = H.P1, H.P2, H.ESC
R = 3.00 / 17                                   # contrahuella
TH = 0.28                                       # huella
X0, X1 = ESC["x"]                               # 1.35 / 4.69
X_DES = X0 + 8 * TH                             # inicio del descanso 3.59
LOSA, VIGA = 0.10, 0.20                         # sobrelosa / peralte viga (PD)
CIELO = 2.70
PEND = 0.13
Y_CUM = (EY0 + EY1) / 2
CUB, CUM = 9.00, 9.00 + PEND * (Y_CUM - EY0)
SILL, HEAD, PUERTA = 0.90, 2.20, 2.10           # PD
XA = 3.0                                        # trazo corte A-A
YB = 18.25                                      # trazo corte B-B


def roof_h(y):
    return CUB + PEND * ((y - EY0) if y <= Y_CUM else (EY1 - y))


doc = cl.new_doc()
msp = doc.modelspace()
for name, col, lw, lt in (("S-CORTE", 7, 50, "Continuous"), ("S-VISTA", 8, 18, "Continuous"),
                          ("S-CIELO", 8, 13, "DASHED"), ("S-CUBIERTA", 7, 60, "Continuous"),
                          ("S-VIDRIO", 8, 13, "Continuous"), ("S-TERRENO", 7, 70, "Continuous"),
                          ("S-TXT", 7, 18, "Continuous"), ("S-COTA", 7, 18, "Continuous"),
                          ("S-NIVEL", 7, 18, "Continuous")):
    doc.layers.add(name, color=col, linetype=lt, lineweight=lw)
if "COTA-75" not in doc.dimstyles:
    cl._dimstyle(doc, "COTA-75", 75)


class Sec:
    def __init__(self, ox, scale=75):
        self.ox = ox
        self.k = scale / 1000.0

    def p(self, h, v):
        return (self.ox + h, v)

    def line(self, a, b, layer="S-VISTA", lts=None):
        e = msp.add_line(self.p(*a), self.p(*b), dxfattribs={"layer": layer})
        if lts:
            e.dxf.ltscale = lts
        return e

    def poly(self, pts, layer="S-VISTA", close=False, width=None):
        e = msp.add_lwpolyline([self.p(*q) for q in pts], close=close,
                               dxfattribs={"layer": layer})
        if width:
            e.dxf.const_width = width
        return e

    def rect(self, h0, v0, h1, v1, layer="S-VISTA"):
        return self.poly([(h0, v0), (h1, v0), (h1, v1), (h0, v1)], layer, close=True)

    def cut(self, h0, v0, h1, v1):
        """Elemento cortado: contorno y relleno sólido."""
        h0, h1 = sorted((h0, h1))
        pts = [self.p(h0, v0), self.p(h1, v0), self.p(h1, v1), self.p(h0, v1)]
        msp.add_lwpolyline(pts, close=True, dxfattribs={"layer": "S-CORTE"})
        ht = msp.add_hatch(color=7, dxfattribs={"layer": "S-CORTE"})
        ht.paths.add_polyline_path(pts)

    def cielo(self, h0, h1, v):
        self.line((h0, v), (h1, v), "S-CIELO", 0.5 * self.k)

    def text(self, s, h, v, size_mm=2.2, align="MIDDLE_CENTER", rot=0, layer="S-TXT"):
        return cl.text(msp, s, self.p(h, v), size_mm * self.k, layer, align, rot)

    def label(self, lines, h, v, size_mm=2.0):
        for i, t in enumerate(lines):
            self.text(t, h, v - i * size_mm * 1.6 * self.k, size_mm)

    def hdim(self, a, b, v_base):
        d = msp.add_linear_dim(base=self.p(0, v_base), p1=self.p(a, v_base),
                               p2=self.p(b, v_base), angle=0, dimstyle="COTA-75",
                               dxfattribs={"layer": "S-COTA"})
        d.render()

    def vdim(self, a, b, h_base, h_pt=None):
        hp = h_base if h_pt is None else h_pt
        d = msp.add_linear_dim(base=self.p(h_base, 0), p1=self.p(hp, a), p2=self.p(hp, b),
                               angle=90, dimstyle="COTA-75", dxfattribs={"layer": "S-COTA"})
        d.render()

    def level(self, h, v, label):
        s = 1.6 * self.k
        x, y = self.p(h, v)
        msp.add_lwpolyline([(x - s, y + s), (x + s, y + s), (x, y)], close=True,
                           dxfattribs={"layer": "S-NIVEL"})
        msp.add_line((x - s, y + s), (x + 24 * self.k, y + s), dxfattribs={"layer": "S-NIVEL"})
        cl.text(msp, label, (x + 2.5 * self.k, y + s + 0.6 * self.k), 1.9 * self.k, "S-NIVEL",
                "BOTTOM_LEFT")

    def axis(self, h, label, v_bot, v_top):
        e = msp.add_line(self.p(h, v_bot), self.p(h, v_top), dxfattribs={"layer": "A-EJES"})
        e.dxf.ltscale = 0.05
        r = 3.5 * self.k
        c = self.p(h, v_top + r)
        msp.add_circle(c, r, dxfattribs={"layer": "A-EJES-TXT"})
        cl.text(msp, label, c, 3.0 * self.k, "A-EJES-TXT", "MIDDLE_CENTER")

    def canoa(self, h_wall, v, out):
        """Canoa esquemática al pie del faldón; out = +1/-1 hacia donde sobresale."""
        a, b = sorted((h_wall, h_wall + out * 0.20))
        self.poly([(a, v + 0.15), (a, v - 0.05), (b, v - 0.05), (b, v + 0.15)], "S-CORTE",
                  width=0.012)

    def window_cut(self, ha, hb, v, top):
        """Muro cortado con ventana: antepecho, vidrio y dintel."""
        self.cut(ha, v, hb, v + SILL)
        self.cut(ha, v + HEAD, hb, top)
        for hh in (ha + 0.05, hb - 0.05):
            self.line((hh, v + SILL), (hh, v + HEAD), "S-VIDRIO")


def deck(S, h0, h1, v):
    """Entrepiso metálico (sobrelosa sobre lámina colaborante) cortado."""
    S.cut(h0, v - LOSA, h1, v)


def beam(S, hc, v, w=0.15):
    """Viga de acero cortada (perfil I esquemático bajo la sobrelosa)."""
    t = 0.025
    S.cut(hc - w / 2, v - LOSA - t, hc + w / 2, v - LOSA)
    S.cut(hc - w / 2, v - LOSA - VIGA, hc + w / 2, v - LOSA - VIGA + t)
    S.cut(hc - 0.012, v - LOSA - VIGA, hc + 0.012, v - LOSA)


# ================================================================ CORTE A-A (x = 3.0)
A = Sec(0.0)
A.line((-2.0, 0.0), (Y_LP + 1.0, 0.0), "S-TERRENO")
WALLS = [(EY0, EY0 + E, "f"), (P1["y"][0] - E, P1["y"][0], "w"), (P1["y"][1], P1["y"][1] + E, "w"),
         (ESC["y"][0] - E, ESC["y"][0], "f"), (ESC["y"][1], ESC["y"][1] + E, "f"),
         (EY1 - E, EY1, "f")]
SPANS = [(EY0, P1["y"][0]), (P1["y"][1], ESC["y"][0]), (ESC["y"][1], EY1)]
for v in (3.00, 6.00):
    for ya, yb in SPANS:
        deck(A, ya, yb, v)
    for k, yc in H.EJES_Y.items():
        if k == "1" and v == 3.00:
            continue
        beam(A, yc, v)
A.cut(EY0, 2.40, EY0 + E, 3.00 - LOSA)                           # viga / fascia sobre portón
for v, top in ((3.00, 6.00 - LOSA), (6.00, None)):
    for ya, yb, kind in WALLS:
        t = top if top is not None else (CUB if kind == "f" and ya in (EY0, EY1 - E)
                                         else roof_h((ya + yb) / 2))
        if kind == "w":
            A.window_cut(ya, yb, v, t)
        else:
            A.cut(ya, v, yb, t)
# portón (cortado, hoja metálica) y tapia del lindero posterior
A.rect(EY0 - 0.03, 0.0, EY0 + 0.03, 2.40, "S-CORTE")
A.cut(Y_LP - E, 0.0, Y_LP, CUB)
# cubierta (corte) con hueco en P1, canoas
for ya, yb in ((EY0, P1["y"][0]), (P1["y"][1], EY1)):
    pts = [(ya, roof_h(ya))] + ([(Y_CUM, CUM)] if ya < Y_CUM < yb else []) + [(yb, roof_h(yb))]
    A.poly(pts, "S-CUBIERTA", width=0.03)
A.canoa(EY0, CUB, -1)
A.canoa(EY1, CUB, +1)
A.canoa(P1["y"][1], roof_h(P1["y"][1]), -1)
# muros de colindancia (este, en vista al fondo): perfil del remate
A.poly([(EY0, CUB), (Y_CUM, CUM), (EY1, CUB)], "S-VISTA")
# cielos rasos
for v in (3.00, 6.00):
    segs = [(EY0 + E, P1["y"][0] - E), (P1["y"][1] + E, ESC["y"][0] - E),
            (ESC["y"][1] + E, EY1 - E)]
    if v == 6.00:
        segs.insert(2, (ESC["y"][0], ESC["y"][1]))
    for a, b in segs:
        A.cielo(a, b, v + CIELO)
# escalera (corte transversal de los tramos en x = 3.0 y vista del resto)
yA0, yA1 = ESC["y"][0], ESC["y"][0] + 1.10
yB0, yB1 = ESC["y"][1] - 1.10, ESC["y"][1]
kA = int((XA - X0) / TH)                                        # huella cortada tramo 1
kB = int((X_DES - XA) / TH)                                     # huella cortada tramo 2
for v in (0.0, 3.00):
    tA, tB = v + (kA + 1) * R, v + (9 + kB + 1) * R
    A.cut(yA0, tA - 0.30, yA1, tA)
    A.cut(yB0, tB - 0.30, yB1, tB)
    for j in range(kA + 2, 10):
        A.line((yA0, v + j * R), (yA1, v + j * R))
    for j in range(10, 9 + kB + 1):
        A.line((yB0, v + j * R), (yB1, v + j * R))
    A.rect(yA0, v + 9 * R - 0.15, yB1, v + 9 * R)                 # descanso (vista)
# columnas del eje C en vista (nivel 1)
for k, yc in H.COLS.items():
    A.rect(yc - 0.15, 0.0, yc + 0.15, 3.00 - LOSA - VIGA)
# rótulos
for txt, h, v in ((["ESTACIONAMIENTO"], 4.70, 1.40), (["JARDÍN SECO"], 9.01, 1.40),
                  (["JARDÍN SECO"], 13.6, 1.40), (["GRADAS"], 18.23, 0.40),
                  (["JARDÍN SECO"], 22.3, 1.40), (["RETIRO", "FRONTAL"], 1.03, 1.40),
                  (["RETIRO", "POSTERIOR"], 26.85, 1.40),
                  (["SUITE 1"], 4.90, 4.40), (["PATIO P1"], 9.01, 4.40),
                  (["COCINA - COMEDOR"], 13.6, 4.40), (["SALA FAMILIAR"], 22.3, 4.40),
                  (["SUITE 1"], 4.90, 7.40), (["PATIO P1"], 9.01, 7.40),
                  (["SUITE 2"], 13.6, 7.40), (["SUITE 3"], 22.3, 7.40)):
    A.label(txt, h, v)
A.label(["PORTÓN"], EY0 - 0.55, 2.05, 1.7)
A.label(["TAPIA LINDERO POSTERIOR", "HASTA VIGA CORONA (+9.00)"], 26.85, 6.0, 1.7)
A.line((26.85 + 1.0, 6.25), (Y_LP - E, 7.0), "S-TXT")
A.label(["CUBIERTA LÁMINA CAL. 26 - PENDIENTE 13 %"], 13.6, CUM + 0.55, 1.9)
A.label(["CANOA HACIA P1"], P1["y"][1] - 0.15, roof_h(P1["y"][1]) + 0.55, 1.6)
A.label(["ENTREPISO METÁLICO (PD)"], 13.6, 3.00 - 0.62, 1.6)
# niveles
for v, lab in ((0.0, "NPT ±0.00"), (3.00, "NPT +3.00"), (5.70, "CIELO +5.70"),
               (6.00, "NPT +6.00"), (8.70, "CIELO +8.70"), (CUB, "VIGA CORONA +9.00"),
               (CUM, "CUMBRERA +10.50")):
    A.level(Y_LP + 0.6, v, lab)
# cotas
cv = [0.0, 3.00 - LOSA - VIGA, 3.00, 3.00 + CIELO, 6.00, 6.00 + CIELO, CUB, CUM]
for a, b in zip(cv[:-1], cv[1:]):
    A.vdim(a, b, -0.9, EY0)
A.vdim(0.0, CUM, -1.6, EY0)
for a, b in ((0.0, EY0), (EY0, EY1), (EY1, Y_LP)):
    A.hdim(a, b, -0.75)
ys = list(H.EJES_Y.values())
for a, b in zip(ys[:-1], ys[1:]):
    A.hdim(a, b, CUM + 1.35)
for lab, y in H.EJES_Y.items():
    A.axis(y, lab, -0.2, CUM + 1.75)
A.text("FRENTE (CALLE)", -1.2, -1.45, 2.0)
A.text("FONDO", Y_LP, -1.45, 2.0)


# ================================================================ CORTE B-B (y = 18.25)
B = Sec(45.0)


def hx(x):
    """Vista hacia el fondo: el este queda a la izquierda."""
    return W - x


RB = roof_h(YB)
B.line((-1.5, 0.0), (W + 1.5, 0.0), "S-TERRENO")
B.cut(hx(0.0), 0.0, hx(E), RB)                                   # colindancia oeste
B.cut(hx(W - E), 0.0, hx(W), RB)                                 # colindancia este
XC0, XC1 = X1, P2["x"][0]
for v in (3.00, 6.00):
    deck(B, hx(E), hx(X0), v)                                    # pasillo
    beam(B, hx(X0 - 0.075), v)                                   # viga de borde (escalera)
    deck(B, hx(XC0), hx(XC1), v)
    beam(B, hx((XC0 + XC1) / 2), v, w=0.12)
    B.cut(hx(XC1), v, hx(XC0), (6.00 - LOSA) if v == 3.00 else RB)   # muro eje C
    # baranda del pasillo hacia el vacío de la escalera
    B.line((hx(X0), v), (hx(X0), v + 0.90))
    B.line((hx(X0) - 0.05, v + 0.90), (hx(X0) + 0.05, v + 0.90))
# descansos (cortados) y tramo 2 en vista
for v in (0.0, 3.00):
    B.cut(hx(X_DES), v + 9 * R - 0.15, hx(X1), v + 9 * R)
    pts = [(hx(X_DES), v + 9 * R)]
    x = X_DES
    for j in range(8):
        pts.append((hx(x), v + (10 + j) * R))
        if j < 7:
            x -= TH
            pts.append((hx(x), v + (10 + j) * R))
    pts.append((hx(X0), v + 17 * R))
    B.poly(pts)
    B.line((hx(X_DES), v + 9 * R - 0.15), (hx(X0), v + 3.00 - LOSA - VIGA))
# cubierta cortada y borde del faldón posterior en vista (más allá de P2)
B.poly([(hx(E), RB), (hx(XC1), RB)], "S-CUBIERTA", width=0.03)
B.line((hx(XC1), roof_h(P2["y"][1])), (hx(W - E), roof_h(P2["y"][1])))
# cielos
B.cielo(hx(E), hx(X0), 3.00 + CIELO)
B.cielo(hx(E), hx(XC0), 6.00 + CIELO)
# en vista: muro del eje 5 (puertas y ventanas hacia P2), bordes de losa y columna C5
for v in (3.00, 6.00):
    B.rect(hx(1.15), v, hx(0.25), v + PUERTA)
    B.rect(hx(8.40), v + SILL, hx(5.40), v + HEAD)
    B.line((hx(6.90), v + SILL), (hx(6.90), v + HEAD))
    B.rect(hx(W - E), v - LOSA - VIGA, hx(X0), v)
B.rect(hx(4.99), 0.0, hx(4.69), 3.00 - LOSA - VIGA)
for txt, h, v in ((["PASILLO"], hx(0.75), 1.40), (["GRADAS"], hx(2.60), 0.40),
                  (["PATIO P2", "(JARDÍN SECO)"], hx(6.83), 1.40),
                  (["PASILLO"], hx(0.75), 5.45), (["GRADAS"], hx(2.60), 4.40),
                  (["PATIO P2", "(ABIERTO)"], hx(6.83), 3.60),
                  (["PASILLO"], hx(0.75), 8.45), (["LLEGADA GRADAS"], hx(2.85), 7.40),
                  (["PATIO P2", "(ABIERTO)"], hx(6.83), 6.60)):
    B.label(txt, h, v, 1.9)
B.label(["COLINDANCIA"], hx(0.075), RB + 0.45, 1.6)
B.label(["COLINDANCIA"], hx(W - 0.075), RB + 0.45, 1.6)
B.label(["BARANDA (VER A11)"], hx(X0) - 1.05, 6.00 + 0.55, 1.6)
for v, lab in ((0.0, "±0.00"), (3.00, "+3.00"), (5.70, "+5.70 CIELO"), (6.00, "+6.00"),
               (8.70, "+8.70 CIELO"), (CUB, "+9.00"), (RB, f"+{RB:.2f} CUBIERTA EN B-B")):
    B.level(W + 0.6, v, lab)
cv = [0.0, 3.00 - LOSA - VIGA, 3.00, 3.00 + CIELO, 6.00, 6.00 + CIELO, RB]
for a, b in zip(cv[:-1], cv[1:]):
    B.vdim(a, b, -0.9, 0.0)
xs = [W, W - E, XC1, XC0, X0, E, 0.0]
for a, b in zip(xs[:-1], xs[1:]):
    B.hdim(hx(a), hx(b), -0.75)
for lab, x in H.EJES_X.items():
    B.axis(hx(x), lab, -0.2, RB + 1.3)

# ================================================================ hoja
psp = doc.layouts.new("A6-CORTES")
psp.page_setup(size=(cl.A1_W, cl.A1_H), margins=(0, 0, 0, 0), units="mm")
doc.layouts.set_active_layout("A6-CORTES")
cl.frame(psp)


def vp(center, size, mc):
    v = psp.add_viewport(center=center, size=size, view_center_point=mc,
                         view_height=size[1] * 75 / 1000.0, dxfattribs={"layer": "A-VIEWPORT"})
    v.dxf.flags = v.dxf.flags | 16384
    return v


vp((360.0, 445.0), (640.0, 230.0), (14.6, 5.4))
cl.view_title(psp, 40.0, 318.0, "CORTE A-A", "CORTE LONGITUDINAL EN x = 3.00 (VISTA HACIA EL ESTE)",
              "Esc. 1:75", 150)
vp((160.0, 190.0), (250.0, 215.0), (45.0 + 4.6, 5.0))
cl.view_title(psp, 40.0, 70.0, "CORTE B-B", "CORTE TRANSVERSAL EN y = 18.25 (VISTA HACIA EL FONDO)",
              "Esc. 1:75", 150)
cl.scale_bar(psp, 40.0, 292.0, 75, 5, 1)
cl.scale_bar(psp, 200.0, 44.0, 75, 5, 1)

X3 = 320.0
y = 300.0
cl.text(psp, "NOTAS:", (X3, y), 3.5, "A-TITULOS", "TOP_LEFT")
notas = [
    "TODAS LAS MEDIDAS ESTÁN DADAS EN METROS, SALVO INDICACIÓN CONTRARIA. [PR]",
    "LA TAPIA COLINDANTE DE MAMPOSTERÍA DEBERÁ PROLONGARSE HASTA EL NIVEL DE LA VIGA CORONA "
    "DEL ÚLTIMO NIVEL, GARANTIZANDO EL APANTALLAMIENTO VISUAL PERMANENTE HACIA LA PROPIEDAD "
    "COLINDANTE.",
    "LOS BAÑOS CONTARÁN CON EXTRACTOR MECÁNICO DE AIRE.",
    "NIVELES: NPT N1 ±0.00 (ACERA), N2 +3.00, N3 +6.00; ALTURA DE PISO A PISO 3.00 m. CIELO "
    "RASO A 2.70 m SOBRE NPT EN LOS NIVELES 2 Y 3. NIVEL 1 SIN CIELO RASO.",
    "ENTREPISOS DE ESTRUCTURA METÁLICA: VIGAS DE ACERO Y LÁMINA COLABORANTE CON SOBRELOSA. "
    "ESPESORES DIBUJADOS (SOBRELOSA 0.10 m, VIGA 0.20 m) PRELIMINARES (PD); PERFILES, "
    "SECCIONES Y REFUERZO SEGÚN PLANOS ESTRUCTURALES.",
    "CUBIERTA DE LÁMINA ESTRUCTURAL CALIBRE 26 A DOS AGUAS, PENDIENTE 13 %, VIGA CORONA +9.00 "
    "Y CUMBRERA +10.50 AL CENTRO. CANOAS EN FRENTE, FONDO Y BORDES HACIA LOS PATIOS DONDE SE "
    "REQUIERA. ESTRUCTURA DE TECHO SEGÚN PLANOS ESTRUCTURALES.",
    "ESCALERA EN U: 17 CONTRAHUELLAS DE 0.176 m Y HUELLA DE 0.28 m POR NIVEL; DESCANSOS A "
    "+1.59 Y +4.59. BARANDAS Y PASAMANOS EN LÁMINA A11.",
    "ALTURAS PRELIMINARES (PD): PUERTAS 2.10 m; VENTANAS HACIA LOS PATIOS CON ANTEPECHO 0.90 m "
    "Y DINTEL 2.20 m. TIPOS EN LÁMINAS A7 A A9.",
    "LA TAPIA DEL LINDERO POSTERIOR LLEGA HASTA LA VIGA CORONA DEL ÚLTIMO NIVEL (+9.00).",
    "CIMENTACIÓN Y CONTRAPISO DEL NIVEL 1 SEGÚN PLANOS ESTRUCTURALES.",
    "TRAZO DE LOS CORTES SEGÚN LÁMINAS A2 A A4.",
]
y = cl.notes_block(psp, X3, y - 6, [f"{i}.- {t}" for i, t in enumerate(notas, 1)]
                   + [cl.NOTA_PR], 2.1, 330)

H.titleblock(doc, psp, "A6", "CORTES", ["CORTE A-A.", "CORTE B-B.", "NOTAS.", "", "", ""],
             [("0", "06-10-2026", "VERSIÓN DE TRABAJO PARA REVISIÓN")], escalas="1:75")

OUT.mkdir(parents=True, exist_ok=True)
doc.saveas(OUT / f"{NAME}.dxf")
cl.render_pdf(doc, "A6-CORTES", OUT / f"{NAME}.pdf")
print("RB", round(RB, 3), "CUM", round(CUM, 3), "kA", kA, "kB", kB)
print("DXF:", OUT / f"{NAME}.dxf")
