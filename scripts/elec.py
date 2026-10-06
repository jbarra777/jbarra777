"""Simbología eléctrica común (láminas E01-E04).

Símbolos según la simbología de la referencia (RIVERGRAND EL08) [PR]. Cada símbolo se dibuja
alrededor de su centro (cx, cy) en coordenadas de dibujo con tamaño u (radio base):
u = 0.13 m en model space de las plantas 1:50, u = 2.6 mm en paper space (cuadros).
"""
import math

import cadlib as cl
from planta import P

LAYERS = (("E-LUM", 7, 25, "Continuous"), ("E-TOMA", 7, 25, "Continuous"),
          ("E-APAG", 7, 25, "Continuous"), ("E-CIRC", 7, 13, "Continuous"),
          ("E-TABLERO", 7, 35, "Continuous"), ("E-VD", 7, 25, "Continuous"),
          ("E-TXT-EL", 7, 18, "Continuous"))
U = 0.13


def layers(doc):
    for name, col, lw, lt in LAYERS:
        if name not in doc.layers:
            doc.layers.add(name, color=col, linetype=lt, lineweight=lw)


def _circle(sp, c, r, layer):
    sp.add_circle(c, r, dxfattribs={"layer": layer})


def _line(sp, a, b, layer):
    sp.add_line(a, b, dxfattribs={"layer": layer})


def _solid(sp, pts, layer):
    h = sp.add_hatch(color=7, dxfattribs={"layer": layer})
    h.paths.add_polyline_path(pts)


def sym(sp, kind, cx, cy, u, label=None):
    """Dibuja el símbolo `kind` centrado en (cx, cy)."""
    c = (cx, cy)
    if kind == "LUZ":                      # luminaria en superficie de cielo
        _circle(sp, c, u, "E-LUM")
        _circle(sp, c, u * 0.6, "E-LUM")
    elif kind == "LUZE":                   # luminaria empotrada en cielo (gypsum)
        _circle(sp, c, u, "E-LUM")
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            _line(sp, (cx + dx * u * 0.55, cy + dy * u * 0.55), (cx + dx * u, cy + dy * u), "E-LUM")
    elif kind == "APL":                    # luminaria en pared (aplique)
        _circle(sp, c, u * 0.8, "E-LUM")
        _line(sp, (cx - u * 1.2, cy), (cx + u * 1.2, cy), "E-LUM")
        _line(sp, (cx, cy - u * 0.8), (cx, cy - u * 1.6), "E-LUM")
        _line(sp, (cx - u * 0.8, cy - u * 1.6), (cx + u * 0.8, cy - u * 1.6), "E-LUM")
    elif kind in ("S", "S3"):              # apagador sencillo / tres vías
        cl.text(sp, "$", c, u * 1.9, "E-APAG", "MIDDLE_CENTER")
        if kind == "S3":
            cl.text(sp, "3", (cx + u * 0.9, cy - u * 0.8), u * 0.8, "E-APAG", "MIDDLE_CENTER")
    elif kind in ("TC", "GFCI", "TC150"):  # tomacorriente doble polarizado 120 V
        _circle(sp, c, u * 0.8, "E-TOMA")
        for dx in (-0.3, 0.3):
            _line(sp, (cx + dx * u, cy - u * 0.8), (cx + dx * u, cy + u * 1.3), "E-TOMA")
        if kind == "TC150":
            _solid(sp, [(cx - u * 0.3, cy - u * 0.75), (cx + u * 0.3, cy - u * 0.75),
                        (cx + u * 0.3, cy + u * 0.75), (cx - u * 0.3, cy + u * 0.75)], "E-TOMA")
        if kind == "GFCI":
            cl.text(sp, "GFCI", (cx + u * 0.9, cy - u * 0.9), u * 0.55, "E-TOMA", "MIDDLE_LEFT")
    elif kind == "T240":                   # salida especial 240 V
        _circle(sp, c, u * 0.8, "E-TOMA")
        _solid(sp, [(cx - u * 0.55, cy - u * 0.45), (cx + u * 0.55, cy - u * 0.45),
                    (cx, cy + u * 0.6)], "E-TOMA")
    elif kind == "TV":
        _circle(sp, c, u * 0.8, "E-VD")
        cl.text(sp, "TV", c, u * 0.6, "E-VD", "MIDDLE_CENTER")
    elif kind == "DAT":                    # salida de voz y datos
        _solid(sp, [(cx - u * 0.8, cy - u * 0.6), (cx + u * 0.8, cy - u * 0.6), (cx, cy + u * 0.8)],
               "E-VD")
    elif kind == "M":                      # medidor
        _circle(sp, c, u * 1.2, "E-TABLERO")
        cl.text(sp, "M", c, u * 1.1, "E-TABLERO", "MIDDLE_CENTER")
    elif kind in ("TAB", "TVD"):           # tablero eléctrico / de voz y datos
        w, h = u * 4.4, u * 1.4
        pts = [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2),
               (cx - w / 2, cy + h / 2)]
        sp.add_lwpolyline(pts, close=True, dxfattribs={"layer": "E-TABLERO"})
        if kind == "TAB":
            _solid(sp, [pts[0], pts[1], pts[2]], "E-TABLERO")
        else:
            _solid(sp, [pts[0], (cx, cy), pts[3]], "E-TABLERO")
            _solid(sp, [pts[1], (cx, cy), pts[2]], "E-TABLERO")
    if label:
        cl.text(sp, label, (cx + u * 1.1, cy + u * 1.0), u * 0.75, "E-TXT-EL", "MIDDLE_LEFT")


# ---------------------------------------------------------------- planta (marco girado)
class Plan:
    """Símbolos y circuitos en la planta (x, y locales; P las lleva al marco de dibujo)."""

    def __init__(self, msp, u=U):
        self.msp, self.u = msp, u

    def s(self, kind, x, y, label=None):
        p = P(x, y)
        sym(self.msp, kind, p.x, p.y, self.u, label)

    def run(self, pts, bulge=0.25):
        """Conexión (tubería) entre salidas: arcos sucesivos."""
        q = [P(*p) for p in pts]
        self.msp.add_lwpolyline([(a.x, a.y, 0, 0, bulge) for a in q[:-1]] + [(q[-1].x, q[-1].y)],
                                format="xyseb", dxfattribs={"layer": "E-CIRC"})

    def home(self, x, y, dx, dy, label):
        """Retorno al tablero: flecha desde la salida (x, y) en la dirección (dx, dy)."""
        a, b = P(x, y), P(x + dx, y + dy)
        self.msp.add_line(a, b, dxfattribs={"layer": "E-CIRC"})
        ang = math.atan2(b.y - a.y, b.x - a.x)
        L = 0.18
        tip = [(b.x, b.y), (b.x - L * math.cos(ang - 0.35), b.y - L * math.sin(ang - 0.35)),
               (b.x - L * math.cos(ang + 0.35), b.y - L * math.sin(ang + 0.35))]
        _solid(self.msp, tip, "E-CIRC")
        cl.text(self.msp, label, (b.x + 0.12 * math.cos(ang), b.y + 0.12 * math.sin(ang) + 0.12),
                0.14, "E-TXT-EL", "MIDDLE_LEFT" if math.cos(ang) >= -0.1 else "MIDDLE_RIGHT")

    def note(self, x, y, txt, h=0.11, rot=0.0):
        p = P(x, y)
        cl.text(self.msp, txt, (p.x, p.y), h, "E-TXT-EL", "MIDDLE_CENTER", rot)


# ---------------------------------------------------------------- cuadro de simbología (paper)
SIMB = [("M", "MEDIDOR ELÉCTRICO A 1,90 m S.N.P.T. [PR]"),
        ("TAB", "TABLERO DE DISTRIBUCIÓN ELÉCTRICA"),
        ("TVD", "TABLERO DE DISTRIBUCIÓN DE VOZ Y DATOS"),
        ("LUZ", "LUMINARIA EN SUPERFICIE DE CIELO"),
        ("LUZE", "LUMINARIA EMPOTRADA EN CIELO DE GYPSUM"),
        ("APL", "LUMINARIA EN PARED (APLIQUE)"),
        ("S", "APAGADOR SENCILLO 15 A, 120 V, A 1,30 m S.N.P.T. [PR]"),
        ("S3", "APAGADOR DE TRES VÍAS 20 A, 120 V, A 1,30 m S.N.P.T. [PR]"),
        ("TC", "TOMACORRIENTE DOBLE POLARIZADO 120 V, 20 A, A 0,30 m S.N.P.T. [PR]"),
        ("TC150", "TOMACORRIENTE DOBLE POLARIZADO 120 V, 20 A, A 1,50 m S.N.P.T. [PR]"),
        ("GFCI", "TOMACORRIENTE DOBLE 120 V, 20 A, CON PROTECCIÓN GFCI [PR]"),
        ("T240", "SALIDA ESPECIAL 240 V (VER CUADRO DE TABLEROS, E04)"),
        ("TV", "SALIDA DE TELEVISIÓN"),
        ("DAT", "SALIDA DE VOZ Y DATOS")]


def simbologia(psp, x, y_top, kinds=None, w_txt=118.0, row_h=7.0):
    """Cuadro de simbología con los símbolos dibujados. Devuelve y inferior."""
    rows = [r for r in SIMB if kinds is None or r[0] in kinds]
    cl.text(psp, "SIMBOLOGÍA ELÉCTRICA", (x, y_top), 3.5, "A-TITULOS", "TOP_LEFT")
    y = y_top - 6.0
    w0 = 16.0
    for k, txt in rows:
        psp.add_lwpolyline([(x, y), (x + w0 + w_txt, y), (x + w0 + w_txt, y - row_h), (x, y - row_h)],
                           close=True, dxfattribs={"layer": "A-TABLAS"})
        psp.add_line((x + w0, y), (x + w0, y - row_h), dxfattribs={"layer": "A-TABLAS"})
        sym(psp, k, x + w0 / 2, y - row_h / 2, 1.9 if k in ("TAB", "TVD") else 2.2)
        cl.text(psp, txt, (x + w0 + 1.5, y - row_h / 2), 1.9, "A-TEXTO", "MIDDLE_LEFT")
        y -= row_h
    return y
