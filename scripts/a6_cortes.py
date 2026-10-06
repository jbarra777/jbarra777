"""Lámina A6 - CORTES A-A y B-B (Esc. 1:75).

Trazos según plantas A2-A4: A-A longitudinal en x = 3.0 (vista hacia el este, frente a la
izquierda); B-B transversal en y = 18.25 (vista hacia el fondo, este a la izquierda).
Datos del usuario: piso a piso 3.00; estructura principal de marcos rígidos de acero con
columnas continuas N1-N3 (eje C; ejes A y D según estructural, no se dibujan); entrepiso de
sobrelosa 0.10 sobre lámina colaborante y vigas de acero; cielo de gypsum regular plano a 2.70
en N2 y N3, acero expuesto en N1; forro del edificio en paredes livianas Steel Tech (0.15 ext. /
0.12 int.); muros de lindero, tapia posterior y frente del N1 (portón) en mampostería; N1 con
contrapiso en estacionamientos, pasillo y gradas, el resto en grava; cubierta de lámina cal. 26
al 13 % sobre clavadores y cerchas metálicas en la dirección de la pendiente (cordón inferior
+9.00). Sin cimentación dibujada (según estructural).
PD: peralte de vigas 0.20, espesor de contrapiso 0.10, puertas 2.10, ventanas a patios
0.90-2.20, geometría de cerchas y clavadores.
Model Space en metros: cada corte en su propio origen (H horizontal, V = altura).
"""
import math

import cadlib as cl
import hoja as H

REV = "rev1"
OUT = cl.ROOT / "planos" / "A6_cortes"
NAME = f"SR-A6_CORTES_{REV}"

W, E = H.W, H.E
EY0, EY1, Y_LP = H.EY0, H.EY1, H.Y_LP
P1, P2, ESC = H.P1, H.P2, H.ESC
R = 3.00 / 17                                   # contrahuella
TH = 0.28                                       # huella
X0, X1 = ESC["x"]                               # 1.35 / 4.69
X_DES = X0 + 8 * TH                             # inicio del descanso 3.59
LOSA, VIGA = 0.10, 0.20                         # sobrelosa (usuario) / peralte viga (PD)
CONTRA, GRAVA = 0.10, 0.25                      # contrapiso (PD) / espesor gráfico de grava
CIELO = 2.70
PEND = 0.13
Y_CUM = (EY0 + EY1) / 2
CUB, CUM = 9.00, 9.00 + PEND * (Y_CUM - EY0)
CLAV = 0.08                                     # clavador (representación)
SILL, HEAD, PUERTA = 0.90, 2.20, 2.10           # PD
XA = 3.0                                        # trazo corte A-A
YB = 18.25                                      # trazo corte B-B
X_CERCHAS = (0.30, H.EJES_X["B"], H.EJES_X["C"], W - 0.30)   # cerchas en la pendiente (PD)
K = 0.075                                       # m de modelo por mm de papel (1:75)


def roof_h(y):
    return CUB + PEND * ((y - EY0) if y <= Y_CUM else (EY1 - y))


doc = cl.new_doc()
msp = doc.modelspace()
for name, col, lw, lt in (("S-CORTE", 7, 70, "Continuous"), ("S-VISTA", 7, 25, "Continuous"),
                          ("S-OCULTO", 8, 13, "DASHED"), ("S-CIELO", 8, 18, "Continuous"),
                          ("S-CUBIERTA", 7, 70, "Continuous"), ("S-VIDRIO", 8, 13, "Continuous"),
                          ("S-TRAMA", 8, 9, "Continuous"), ("S-TERRENO", 7, 50, "Continuous"),
                          ("S-TXT", 7, 18, "Continuous"), ("S-COTA", 7, 18, "Continuous"),
                          ("S-NIVEL", 7, 18, "Continuous")):
    doc.layers.add(name, color=col, linetype=lt, lineweight=lw)
if "COTA-75" not in doc.dimstyles:
    cl._dimstyle(doc, "COTA-75", 75)


class Sec:
    def __init__(self, ox, flip=False):
        self.ox = ox
        self.flip = flip            # B-B: h = W - x
        self.k = K

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
        h0, h1 = sorted((h0, h1))
        return self.poly([(h0, v0), (h1, v0), (h1, v1), (h0, v1)], layer, close=True)

    def _fill(self, h0, v0, h1, v1, pattern=None, scale=1.0, color=7, solid=True):
        h0, h1 = sorted((h0, h1))
        pts = [self.p(h0, v0), self.p(h1, v0), self.p(h1, v1), self.p(h0, v1)]
        ht = msp.add_hatch(color=color, dxfattribs={"layer": "S-TRAMA" if pattern else "S-CORTE"})
        ht.paths.add_polyline_path(pts)
        if pattern:
            ht.set_pattern_fill(pattern, scale=scale)
        return pts

    # ---- materiales cortados
    def steel(self, h0, v0, h1, v1):
        """Acero cortado: relleno negro."""
        self._fill(h0, v0, h1, v1)
        self.rect(h0, v0, h1, v1, "S-CORTE")

    def concrete(self, h0, v0, h1, v1):
        """Concreto cortado (sobrelosa / contrapiso): relleno gris."""
        self._fill(h0, v0, h1, v1, color=8)
        self.rect(h0, v0, h1, v1, "S-CORTE")

    def masonry(self, h0, v0, h1, v1):
        """Mampostería cortada: trama diagonal."""
        self._fill(h0, v0, h1, v1, "ANSI31", 0.6 * 0.024)
        self.rect(h0, v0, h1, v1, "S-CORTE")

    def steeltech(self, h0, v0, h1, v1):
        """Forro Steel Tech cortado: contorno y eje de perfiles (trazo)."""
        self.rect(h0, v0, h1, v1, "S-CORTE")
        hc = (h0 + h1) / 2
        self.line((hc, v0 + 0.05), (hc, v1 - 0.05), "S-OCULTO", 0.3 * K)

    def partition(self, h0, v0, h1, v1):
        """Pared interior cortada (sistema según indicación): contorno."""
        self.rect(h0, v0, h1, v1, "S-CORTE")

    def wall(self, kind, h0, v0, h1, v1):
        {"m": self.masonry, "s": self.steeltech, "i": self.partition}[kind](h0, v0, h1, v1)

    def wall_window(self, kind, ha, hb, v, top):
        self.wall(kind, ha, v, hb, v + SILL)
        self.wall(kind, ha, v + HEAD, hb, top)
        for hh in (ha + 0.04, hb - 0.04):
            self.line((hh, v + SILL), (hh, v + HEAD), "S-VIDRIO")

    def gravel(self, h0, h1):
        self._fill(h0, -GRAVA, h1, 0.0, "GRAVEL", 0.045)
        self.line((h0, 0.0), (h1, 0.0), "S-TERRENO")
        self.line((h0, -GRAVA), (h1, -GRAVA), "S-VISTA")

    def slab_on_grade(self, h0, h1):
        self.concrete(h0, -CONTRA, h1, 0.0)

    def cielo(self, h0, h1, v):
        self.line((h0, v), (h1, v), "S-CIELO")
        self.line((h0, v + 0.0125), (h1, v + 0.0125), "S-CIELO")

    # ---- textos y cotas
    def text(self, s, h, v, size_mm=2.2, align="MIDDLE_CENTER", rot=0, layer="S-TXT"):
        return cl.text(msp, s, self.p(h, v), size_mm * K, layer, align, rot)

    def label(self, lines, h, v, size_mm=2.0, align="MIDDLE_CENTER"):
        for i, t in enumerate(lines):
            self.text(t, h, v - i * size_mm * 1.6 * K, size_mm, align)

    def callout(self, lines, h_txt, v_txt, target, size_mm=1.7, align="MIDDLE_LEFT"):
        """Rótulo con línea guía y punto en el elemento."""
        self.label(lines, h_txt, v_txt, size_mm, align)
        dx = -0.10 if align == "MIDDLE_LEFT" else 0.10
        a = self.p(h_txt + dx, v_txt)
        b = self.p(*target)
        msp.add_line(a, b, dxfattribs={"layer": "S-TXT"})
        msp.add_circle(b, 0.45 * K, dxfattribs={"layer": "S-TXT"})

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
        s = 1.6 * K
        x, y = self.p(h, v)
        msp.add_lwpolyline([(x - s, y + s), (x + s, y + s), (x, y)], close=True,
                           dxfattribs={"layer": "S-NIVEL"})
        msp.add_line((x - s, y + s), (x + 26 * K, y + s), dxfattribs={"layer": "S-NIVEL"})
        cl.text(msp, label, (x + 2.5 * K, y + s + 0.6 * K), 1.9 * K, "S-NIVEL", "BOTTOM_LEFT")

    def axis(self, h, label, v_bot, v_top):
        e = msp.add_line(self.p(h, v_bot), self.p(h, v_top), dxfattribs={"layer": "A-EJES"})
        e.dxf.ltscale = 0.05
        r = 3.5 * K
        c = self.p(h, v_top + r)
        msp.add_circle(c, r, dxfattribs={"layer": "A-EJES-TXT"})
        cl.text(msp, label, c, 3.0 * K, "A-EJES-TXT", "MIDDLE_CENTER")

    def canoa(self, h_wall, v, out):
        a, b = sorted((h_wall, h_wall + out * 0.20))
        self.poly([(a, v + 0.15), (a, v - 0.05), (b, v - 0.05), (b, v + 0.15)], "S-CORTE",
                  width=0.012)


def deck(S, h0, h1, v):
    """Entrepiso: sobrelosa 0.10 sobre lámina colaborante (línea inferior)."""
    S.concrete(h0, v - LOSA, h1, v)
    S.line((h0, v - LOSA + 0.012), (h1, v - LOSA + 0.012), "S-CORTE")


def beam(S, hc, v, w=0.15):
    """Viga de acero cortada (perfil I) bajo la sobrelosa."""
    t = 0.025
    S.steel(hc - w / 2, v - LOSA - t, hc + w / 2, v - LOSA)
    S.steel(hc - w / 2, v - LOSA - VIGA, hc + w / 2, v - LOSA - VIGA + t)
    S.steel(hc - 0.012, v - LOSA - VIGA, hc + 0.012, v - LOSA)


def truss_elev(S, y0, y1):
    """Cercha metálica en vista (dirección de la pendiente): cordón inferior a +9.00,
    cordón superior bajo los clavadores, montantes y diagonales. Geometría PD."""
    top = lambda y: roof_h(y) - CLAV
    # recortar donde el peralte es muy pequeño (apoyo de clavadores sobre la viga corona)
    ya, yb = y0, y1
    if top(ya) < CUB + 0.05:
        ya = y0 + (CUB + 0.05 - top(y0)) / PEND if roof_h(y0 + 0.01) > roof_h(y0) else ya
    if top(yb) < CUB + 0.05:
        yb = y1 - (CUB + 0.05 - top(y1)) / PEND if roof_h(y1 - 0.01) > roof_h(y1) else yb
    S.line((y0, CUB), (y1, CUB))                                     # cordón inferior
    pts = [(ya, top(ya))] + ([(Y_CUM, top(Y_CUM))] if ya < Y_CUM < yb else []) + [(yb, top(yb))]
    S.poly(pts)                                                       # cordón superior
    S.line((ya, CUB), (ya, top(ya)))
    S.line((yb, CUB), (yb, top(yb)))
    n = max(1, round((yb - ya) / 1.15))
    ps = [ya + (yb - ya) * i / n for i in range(n + 1)]
    if ya < Y_CUM < yb and all(abs(q - Y_CUM) > 0.3 for q in ps):
        ps = sorted(ps + [Y_CUM])
    for q in ps[1:-1]:
        S.line((q, CUB), (q, top(q)))                                 # montantes
    for a, b in zip(ps[:-1], ps[1:]):
        # diagonales tipo Pratt: bajan hacia los apoyos
        if (a + b) / 2 < Y_CUM:
            S.line((a, CUB), (b, top(b)))
        else:
            S.line((a, top(a)), (b, CUB))


def purlins(S, h0, h1, step=1.0):
    """Clavadores cortados bajo la lámina (A-A)."""
    n = max(1, int((h1 - h0) / step))
    for i in range(n + 1):
        h = h0 + (h1 - h0) * i / n
        v = roof_h(h)
        S.steel(h - 0.03, v - CLAV, h + 0.03, v - 0.01)


# ================================================================ CORTE A-A (x = 3.0)
A = Sec(0.0)
Y_EST1 = EY0 + E + 5.0                                          # fin de estacionamientos 7.21
# nivel 1: contrapiso (estacionamiento y gradas) y grava (jardín seco y retiros)
A.slab_on_grade(EY0, Y_EST1)
A.slab_on_grade(ESC["y"][0], ESC["y"][1])
for a, b in ((0.0, EY0), (Y_EST1, ESC["y"][0]), (ESC["y"][1], Y_LP - E)):
    A.gravel(a, b)
A.line((-2.0, 0.0), (0.0, 0.0), "S-TERRENO")
A.line((Y_LP, 0.0), (Y_LP + 1.0, 0.0), "S-TERRENO")
# entrepisos
SPANS = [(EY0, P1["y"][0]), (P1["y"][1], ESC["y"][0]), (ESC["y"][1], EY1)]
for v in (3.00, 6.00):
    for ya, yb in SPANS:
        deck(A, ya, yb, v)
    for k, yc in H.EJES_Y.items():
        if k == "1" and v == 3.00:
            continue
        beam(A, yc, v)
# frente del N1 sobre el portón (mampostería) y portón
A.masonry(EY0, 2.40, EY0 + E, 3.00 - LOSA)
A.rect(EY0 - 0.03, 0.0, EY0 + 0.03, 2.40, "S-CORTE")
# muros N2 y N3: fachadas y muros a patio = forro Steel Tech; ejes 4 y 5 = interiores
WALLS = [(EY0, EY0 + E, "s", False), (P1["y"][0] - E, P1["y"][0], "s", True),
         (P1["y"][1], P1["y"][1] + E, "s", True), (ESC["y"][0] - E, ESC["y"][0], "i", False),
         (ESC["y"][1], ESC["y"][1] + E, "i", False), (EY1 - E, EY1, "s", False)]
for v in (3.00, 6.00):
    for ya, yb, kind, win in WALLS:
        if v == 3.00:
            top = 6.00 - LOSA
        elif kind == "s" and win:
            top = roof_h((ya + yb) / 2) - CLAV                    # culata hacia el patio
        else:
            top = CUB
        if win:
            A.wall_window(kind, ya, yb, v, top)
        else:
            A.wall(kind, ya, v, yb, top)
# tapia del lindero posterior (mampostería) hasta la viga corona
A.masonry(Y_LP - E, -GRAVA, Y_LP, CUB)
# columnas del eje C continuas N1-N3 (en vista, a plomo)
for k, yc in H.COLS.items():
    A.rect(yc - 0.15, 0.0, yc + 0.15, CUB)
# cubierta: lámina (corte), clavadores (corte), cercha del eje C (vista), canoas
for ya, yb in ((EY0, P1["y"][0]), (P1["y"][1], EY1)):
    pts = [(ya, roof_h(ya))] + ([(Y_CUM, CUM)] if ya < Y_CUM < yb else []) + [(yb, roof_h(yb))]
    A.poly(pts, "S-CUBIERTA", width=0.025)
    if ya < Y_CUM < yb:
        purlins(A, ya, Y_CUM)
        purlins(A, Y_CUM, yb)
    else:
        purlins(A, ya, yb)
for ya, yb in ((EY0, P1["y"][0]), (P1["y"][1], ESC["y"][0]), (ESC["y"][1], EY1)):
    truss_elev(A, ya, yb)
A.canoa(EY0, CUB, -1)
A.canoa(EY1, CUB, +1)
A.canoa(P1["y"][1], roof_h(P1["y"][1]), -1)
A.poly([(EY0, CUB), (Y_CUM, CUM), (EY1, CUB)], "S-OCULTO")       # remate muro de lindero
# cielos de gypsum (N2 y N3)
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
kA = int((XA - X0) / TH)
kB = int((X_DES - XA) / TH)
for v in (0.0, 3.00):
    tA, tB = v + (kA + 1) * R, v + (9 + kB + 1) * R
    A.concrete(yA0, tA - 0.30, yA1, tA)
    A.concrete(yB0, tB - 0.30, yB1, tB)
    for j in range(kA + 2, 10):
        A.line((yA0, v + j * R), (yA1, v + j * R))
    for j in range(10, 9 + kB + 1):
        A.line((yB0, v + j * R), (yB1, v + j * R))
    A.rect(yA0, v + 9 * R - 0.15, yB1, v + 9 * R)
# rótulos de recintos
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
# rótulos de sistemas (con línea guía)
A.callout(["LÁMINA ESTRUCTURAL CAL. 26 SOBRE CLAVADORES"], 14.4, CUM + 0.75, (13.0, roof_h(13.0)))
A.callout(["CERCHA METÁLICA EJE C (EN VISTA, PD)"], 17.6, 10.55, (17.0, CUB + 0.30))
A.callout(["CIELO GYPSUM REGULAR PLANO +8.70"], 20.0, 8.45, (19.9, 8.70))
A.callout(["FORRO STEEL", "TECH 0.15"], 1.75, 6.0 + 1.55, (EY0 + 0.075, 6.0 + 1.30), align="MIDDLE_RIGHT")
A.callout(["SOBRELOSA 0.10 / LÁMINA COLABORANTE"], 11.2, 6.0 - 0.55, (10.9, 6.0 - 0.05))
A.callout(["VIGA DE ACERO (PD)"], 11.2, 3.0 - 0.75, (H.EJES_Y["3"] + 0.08, 3.0 - 0.20))
A.callout(["COLUMNA DE ACERO EJE C", "CONTINUA N1-N3"], 7.10, 2.10, (H.COLS["2"] - 0.15, 2.0), align="MIDDLE_RIGHT")
A.callout(["ACERO EXPUESTO (SIN CIELO)"], 11.2, 1.90, (11.0, 2.70))
A.callout(["CONTRAPISO"], 4.2, 0.55, (4.0, -0.05))
A.callout(["GRAVA"], 11.6, 0.55, (11.4, -0.07))
A.callout(["FRENTE N1", "MAMPOSTERÍA"], 1.75, 3.75, (EY0 + 0.07, 2.70), align="MIDDLE_RIGHT")
A.callout(["TAPIA POSTERIOR", "MAMPOSTERÍA", "HASTA +9.00"], 25.75, 6.2, (Y_LP - E, 7.0))
A.label(["CANOA HACIA P1"], P1["y"][1] - 0.15, roof_h(P1["y"][1]) + 0.55, 1.6)
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
    A.hdim(a, b, -0.85)
ys = list(H.EJES_Y.values())
for a, b in zip(ys[:-1], ys[1:]):
    A.hdim(a, b, CUM + 1.55)
for lab, y in H.EJES_Y.items():
    A.axis(y, lab, -0.3, CUM + 1.95)
A.text("FRENTE (CALLE)", -1.2, -1.55, 2.0)
A.text("FONDO", Y_LP, -1.55, 2.0)


# ================================================================ CORTE B-B (y = 18.25)
B = Sec(45.0)


def hx(x):
    """Vista hacia el fondo: el este queda a la izquierda."""
    return W - x


RB = roof_h(YB)
XC0, XC1 = X1, P2["x"][0]
# nivel 1: contrapiso en pasillo y gradas, grava en P2 / jardín
B.slab_on_grade(hx(X1), hx(E))
B.gravel(hx(W - E), hx(X1))
B.line((-1.5, 0.0), (0.0, 0.0), "S-TERRENO")
B.line((W, 0.0), (W + 1.5, 0.0), "S-TERRENO")
# muros de lindero (mampostería) hasta la cubierta
B.masonry(hx(0.0), -GRAVA, hx(E), RB)
B.masonry(hx(W - E), -GRAVA, hx(W), RB)
# columna C5 (en vista, continua) y entrepisos
B.rect(hx(4.99), 0.0, hx(4.69), CUB)
for v in (3.00, 6.00):
    deck(B, hx(E), hx(X0), v)
    beam(B, hx(X0 - 0.075), v)
    deck(B, hx(XC0), hx(XC1), v)
    beam(B, hx((XC0 + XC1) / 2), v, w=0.12)
    B.steeltech(hx(XC1), v, hx(XC0), (6.00 - LOSA) if v == 3.00 else RB - CLAV)
    B.line((hx(X0), v), (hx(X0), v + 0.90))                       # baranda
    B.line((hx(X0) - 0.05, v + 0.90), (hx(X0) + 0.05, v + 0.90))
# descansos (cortados) y tramo 2 en vista
for v in (0.0, 3.00):
    B.concrete(hx(X_DES), v + 9 * R - 0.15, hx(X1), v + 9 * R)
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
# cubierta: lámina cortada, clavador en vista, cerchas cortadas (cordones y montante)
B.poly([(hx(E), RB), (hx(XC1), RB)], "S-CUBIERTA", width=0.025)
B.line((hx(E), RB - CLAV), (hx(XC1), RB - CLAV))
for xc in X_CERCHAS[:3]:
    B.steel(hx(xc) - 0.05, RB - CLAV - 0.08, hx(xc) + 0.05, RB - CLAV)
    B.steel(hx(xc) - 0.05, CUB, hx(xc) + 0.05, CUB + 0.08)
    B.line((hx(xc), CUB + 0.08), (hx(xc), RB - CLAV - 0.08))
B.line((hx(XC1), roof_h(P2["y"][1])), (hx(W - E), roof_h(P2["y"][1])))
# cielos de gypsum
B.cielo(hx(E), hx(X0), 3.00 + CIELO)
B.cielo(hx(E), hx(XC0), 6.00 + CIELO)
# en vista: muro del eje 5 (puerta y ventana hacia P2) y viga del eje 5
for v in (3.00, 6.00):
    B.rect(hx(1.15), v, hx(0.25), v + PUERTA)
    B.rect(hx(8.40), v + SILL, hx(5.40), v + HEAD)
    B.line((hx(6.90), v + SILL), (hx(6.90), v + HEAD))
    B.rect(hx(W - E), v - LOSA - VIGA, hx(X0), v)
for txt, h, v in ((["PASILLO"], hx(0.75), 1.40), (["GRADAS"], hx(2.60), 0.40),
                  (["PATIO P2", "(JARDÍN SECO)"], hx(6.83), 1.40),
                  (["PASILLO"], hx(0.75), 5.45), (["GRADAS"], hx(2.60), 4.40),
                  (["PATIO P2", "(ABIERTO)"], hx(6.83), 3.60),
                  (["PASILLO"], hx(0.75), 8.45), (["LLEGADA GRADAS"], hx(2.85), 7.40),
                  (["PATIO P2", "(ABIERTO)"], hx(6.83), 6.60)):
    B.label(txt, h, v, 1.9)
B.label(["BARANDA (VER A11)"], hx(X0) - 1.05, 6.00 + 0.55, 1.6)
B.callout(["MURO DE LINDERO", "MAMPOSTERÍA"], hx(W - 0.15) + 0.35, 2.45,
          (hx(W - 0.075), 2.25), align="MIDDLE_LEFT")
B.callout(["FORRO STEEL TECH"], hx(XC0) - 0.35, 8.50, (hx(4.75), 8.35), align="MIDDLE_RIGHT")
B.callout(["CERCHAS CORTADAS (PD)"], hx(2.2), RB + 0.55, (hx(X_CERCHAS[1]), RB - 0.3),
          align="MIDDLE_LEFT")
B.callout(["COLUMNA C5 (EN VISTA)"], hx(4.84) - 0.25, 1.90, (hx(4.90), 1.70),
          align="MIDDLE_RIGHT")
for v, lab in ((0.0, "±0.00"), (3.00, "+3.00"), (5.70, "+5.70 CIELO"), (6.00, "+6.00"),
               (8.70, "+8.70 CIELO"), (CUB, "+9.00"), (RB, f"+{RB:.2f} CUBIERTA EN B-B")):
    B.level(W + 0.6, v, lab)
cv = [0.0, 3.00 - LOSA - VIGA, 3.00, 3.00 + CIELO, 6.00, 6.00 + CIELO, CUB, RB]
for a, b in zip(cv[:-1], cv[1:]):
    B.vdim(a, b, -0.9, 0.0)
xs = [W, W - E, XC1, XC0, X0, E, 0.0]
for a, b in zip(xs[:-1], xs[1:]):
    B.hdim(hx(a), hx(b), -0.85)
for lab, x in H.EJES_X.items():
    B.axis(hx(x), lab, -0.3, RB + 1.3)

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
    "NIVELES: NPT N1 ±0.00 (ACERA), N2 +3.00, N3 +6.00; ALTURA DE PISO A PISO 3.00 m.",
    "ESTRUCTURA PRINCIPAL: MARCOS RÍGIDOS DE ACERO. COLUMNAS DEL EJE C CONTINUAS Y A PLOMO DEL "
    "NIVEL 1 AL NIVEL 3. COLUMNAS DE LOS EJES A Y D, PERFILES, SECCIONES Y CONEXIONES SEGÚN "
    "PLANOS ESTRUCTURALES.",
    "ENTREPISOS: SOBRELOSA DE 0.10 m SOBRE LÁMINA COLABORANTE Y VIGAS DE ACERO (PERALTE 0.20 m "
    "PRELIMINAR, PD).",
    "CIELOS: GYPSUM REGULAR PLANO SUSPENDIDO A 2.70 m SOBRE NPT EN LOS NIVELES 2 Y 3. NIVEL 1 "
    "(ESTACIONAMIENTOS) CON ESTRUCTURA DE ACERO EXPUESTA.",
    "CERRAMIENTOS: FORRO DEL EDIFICIO EN PAREDES LIVIANAS STEEL TECH (0.15 m). MUROS DE LINDERO, "
    "TAPIA POSTERIOR Y FRENTE DEL NIVEL 1 (PORTÓN) EN MAMPOSTERÍA. PAREDES INTERIORES 0.12 m.",
    "CUBIERTA: LÁMINA ESTRUCTURAL CAL. 26 SOBRE CLAVADORES Y CERCHAS METÁLICAS EN LA DIRECCIÓN "
    "DE LA PENDIENTE (13 %), CORDÓN INFERIOR A +9.00 Y CUMBRERA +10.50. GEOMETRÍA Y PERFILES DE "
    "CERCHAS Y CLAVADORES SEGÚN PLANOS ESTRUCTURALES (PD). CANOAS EN FRENTE, FONDO Y BORDES HACIA "
    "LOS PATIOS DONDE SE REQUIERA.",
    "NIVEL 1: CONTRAPISO EN ESTACIONAMIENTOS, PASILLO Y GRADAS (ESPESOR SEGÚN ESTRUCTURAL); EL "
    "RESTO EN GRAVA (JARDÍN SECO).",
    "ESCALERA EN U: 17 CONTRAHUELLAS DE 0.176 m Y HUELLA DE 0.28 m POR NIVEL; DESCANSOS A "
    "+1.59 Y +4.59. BARANDAS Y PASAMANOS EN LÁMINA A11.",
    "ALTURAS PRELIMINARES (PD): PUERTAS 2.10 m; VENTANAS HACIA LOS PATIOS CON ANTEPECHO 0.90 m "
    "Y DINTEL 2.20 m. TIPOS EN LÁMINAS A7 A A9.",
    "CIMENTACIÓN SEGÚN PLANOS ESTRUCTURALES (NO SE DIBUJA EN ESTA LÁMINA).",
    "TRAZO DE LOS CORTES SEGÚN LÁMINAS A2 A A4.",
]
y = cl.notes_block(psp, X3, y - 6, [f"{i}.- {t}" for i, t in enumerate(notas, 1)]
                   + [cl.NOTA_PR], 2.1, 330)

# simbología de materiales
y -= 4
cl.text(psp, "SIMBOLOGÍA:", (X3, y), 3.5, "A-TITULOS", "TOP_LEFT")
y -= 9
items = [("steel", "ACERO CORTADO (COLUMNAS, VIGAS, CERCHAS, CLAVADORES)"),
         ("conc", "CONCRETO CORTADO (SOBRELOSA, CONTRAPISO, GRADAS)"),
         ("mamp", "MAMPOSTERÍA (MUROS DE LINDERO, TAPIA, FRENTE N1)"),
         ("st", "FORRO STEEL TECH"),
         ("int", "PARED INTERIOR"),
         ("grav", "GRAVA (JARDÍN SECO)"),
         ("cielo", "CIELO GYPSUM REGULAR PLANO")]
col_w = 185
for i, (kind, lab) in enumerate(items):
    xx = X3 + (i % 2) * col_w
    yy = y - (i // 2) * 9
    pts = [(xx, yy - 2.5), (xx + 14, yy - 2.5), (xx + 14, yy + 2.5), (xx, yy + 2.5)]
    if kind == "cielo":
        psp.add_line((xx, yy), (xx + 14, yy), dxfattribs={"layer": "S-CIELO"})
        psp.add_line((xx, yy + 0.4), (xx + 14, yy + 0.4), dxfattribs={"layer": "S-CIELO"})
    else:
        psp.add_lwpolyline(pts, close=True, dxfattribs={"layer": "S-CORTE"})
        if kind in ("steel", "conc"):
            hh = psp.add_hatch(color=7 if kind == "steel" else 8, dxfattribs={"layer": "S-CORTE"})
            hh.paths.add_polyline_path(pts)
        elif kind in ("mamp", "grav"):
            hh = psp.add_hatch(dxfattribs={"layer": "S-TRAMA"})
            hh.paths.add_polyline_path(pts)
            hh.set_pattern_fill("ANSI31" if kind == "mamp" else "GRAVEL",
                                scale=0.35 if kind == "mamp" else 1.3)
        elif kind == "st":
            e = psp.add_line((xx + 1, yy), (xx + 13, yy), dxfattribs={"layer": "S-OCULTO"})
            e.dxf.ltscale = 0.3
    cl.text(psp, lab, (xx + 18, yy), 2.2, "A-TEXTO", "MIDDLE_LEFT")

H.titleblock(doc, psp, "A6", "CORTES", ["CORTE A-A.", "CORTE B-B.", "NOTAS.", "SIMBOLOGÍA.", "", ""],
             [("0", "06-10-2026", "VERSIÓN DE TRABAJO PARA REVISIÓN"),
              ("1", "06-10-2026", "SISTEMA CONSTRUCTIVO, CERCHAS, MATERIALES")], escalas="1:75")

OUT.mkdir(parents=True, exist_ok=True)
doc.saveas(OUT / f"{NAME}.dxf")
cl.render_pdf(doc, "A6-CORTES", OUT / f"{NAME}.pdf")
print("RB", round(RB, 3), "CUM", round(CUM, 3), "kA", kA, "kB", kB)
print("DXF:", OUT / f"{NAME}.dxf")
