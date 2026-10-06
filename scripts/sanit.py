"""Piezas comunes de las láminas sanitarias (S01-S03): plantas N1-N3 a 1:100 copiadas de los
DXF aprobados (A2 rev3, A3 rev4, A4 rev4), en gris, y símbolos de instalaciones sanitarias."""
import math

import ezdxf

import cadlib as cl
from planta import P

SRC = {"N1": cl.ROOT / "planos/A2_nivel1/SR-A2_NIVEL1_rev3.dxf",
       "N2": cl.ROOT / "planos/A3_nivel2/SR-A3_NIVEL2_rev4.dxf",
       "N3": cl.ROOT / "planos/A4_nivel3/SR-A4_NIVEL3_rev4.dxf"}
OFF = {"N1": 0.0, "N2": -20.0, "N3": -40.0}            # desplazamiento en Y del marco de planta
KEEP = {"A-MURO", "A-MURO-TRAMA", "A-PUERTA", "A-VENTANA", "A-ESCALERA", "A-ESPACIOS",
        "E-COLUMNA", "A-EJES", "A-EJES-TXT", "T-LINDERO", "A-PROYECCION", "A-MOBILIARIO"}
GRIS = KEEP - {"A-ESPACIOS", "A-EJES-TXT"}
LAYERS = (("S-AF", 5, 35, "Continuous"), ("S-AC", 1, 35, "DASHED"), ("S-AN", 3, 35, "Continuous"),
          ("S-AJ", 4, 35, "DASHED"), ("S-AP", 6, 35, "Continuous"), ("S-ACC", 7, 25, "Continuous"),
          ("S-TXT", 7, 18, "Continuous"), ("S-DET", 7, 35, "Continuous"), ("S-FINO", 8, 13, "Continuous"))
TH = 0.17                                               # texto de planta (1,7 mm a 1:100)


def base(doc, msp):
    for name, col, lw, lt in LAYERS:
        if name not in doc.layers:
            doc.layers.add(name, color=col, linetype=lt, lineweight=lw)
    for lv, path in SRC.items():
        for e in ezdxf.readfile(path).modelspace():
            if e.dxf.layer in KEEP:
                c = e.copy()
                c.translate(0, OFF[lv], 0)
                msp.add_entity(c)
    for name in GRIS:
        if name in doc.layers:
            doc.layers.get(name).color = 8


class Lv:
    """Dibujo sobre la planta de un nivel (coordenadas locales x, y)."""

    def __init__(self, msp, lv):
        self.msp, self.lv = msp, lv

    def Q(self, x, y):
        p = P(x, y)
        return (p.x, p.y + OFF[self.lv])

    def pipe(self, pts, layer="S-AF", lts=0.02):
        e = self.msp.add_lwpolyline([self.Q(*p) for p in pts], dxfattribs={"layer": layer})
        if layer in ("S-AC", "S-AJ"):
            e.dxf.ltscale = lts
        return e

    def text(self, s, x, y, h=TH, al="MIDDLE_LEFT", rot=0.0):
        cl.text(self.msp, s, self.Q(x, y), h, "S-TXT", al, rot)

    def label(self, s, x, y, dx=0.35, dy=0.35):
        """Rótulo con línea guía corta desde el punto (x, y)."""
        a = self.Q(x, y)
        b = self.Q(x + dx, y + dy)
        self.msp.add_line(a, b, dxfattribs={"layer": "S-FINO"})
        cl.text(self.msp, s, (b[0] + (0.08 if b[0] >= a[0] else -0.08), b[1]), TH, "S-TXT",
                "MIDDLE_LEFT" if b[0] >= a[0] else "MIDDLE_RIGHT")

    # ------------------------------------------------------------ símbolos
    def llave(self, x, y):
        """Llave de paso: dos triángulos opuestos."""
        cx, cy = self.Q(x, y)
        r = 0.14
        for s in (-1, 1):
            h = self.msp.add_hatch(color=7, dxfattribs={"layer": "S-ACC"})
            h.paths.add_polyline_path([(cx, cy), (cx + s * r, cy + r * 0.8), (cx + s * r, cy - r * 0.8)])

    def salida(self, x, y):
        cx, cy = self.Q(x, y)
        self.msp.add_circle((cx, cy), 0.07, dxfattribs={"layer": "S-ACC"})
        h = self.msp.add_hatch(color=7, dxfattribs={"layer": "S-ACC"})
        h.paths.add_edge_path().add_arc((cx, cy), 0.07, 0, 360)

    def montante(self, x, y):
        cx, cy = self.Q(x, y)
        self.msp.add_circle((cx, cy), 0.16, dxfattribs={"layer": "S-ACC"})
        self.msp.add_circle((cx, cy), 0.06, dxfattribs={"layer": "S-ACC"})

    def medidor(self, x, y):
        cx, cy = self.Q(x, y)
        self.msp.add_lwpolyline([(cx - 0.25, cy - 0.15), (cx + 0.25, cy - 0.15), (cx + 0.25, cy + 0.15),
                                 (cx - 0.25, cy + 0.15)], close=True, dxfattribs={"layer": "S-ACC"})
        h = self.msp.add_hatch(color=7, dxfattribs={"layer": "S-ACC"})
        h.paths.add_polyline_path([(cx - 0.25, cy - 0.15), (cx, cy - 0.15), (cx, cy + 0.15),
                                   (cx - 0.25, cy + 0.15)])

    def calentador(self, x, y):
        cx, cy = self.Q(x, y)
        self.msp.add_lwpolyline([(cx - 0.13, cy - 0.13), (cx + 0.13, cy - 0.13), (cx + 0.13, cy + 0.13),
                                 (cx - 0.13, cy + 0.13)], close=True, dxfattribs={"layer": "S-ACC"})
        cl.text(self.msp, "CP", (cx, cy), 0.10, "S-ACC", "MIDDLE_CENTER")


def leyenda_simbolo(psp, kind, cx, cy, s=1.0):
    """Símbolo para cuadros en paper space (tamaño en mm)."""
    if kind in ("AF", "AC", "AN", "AJ", "AP"):
        lay = {"AF": "S-AF", "AC": "S-AC", "AN": "S-AN", "AJ": "S-AJ", "AP": "S-AP"}[kind]
        e = psp.add_line((cx - 6 * s, cy), (cx + 6 * s, cy), dxfattribs={"layer": lay})
        if kind in ("AC", "AJ"):
            e.dxf.ltscale = 0.4
    elif kind == "LL":
        for sg in (-1, 1):
            h = psp.add_hatch(color=7, dxfattribs={"layer": "S-ACC"})
            h.paths.add_polyline_path([(cx, cy), (cx + sg * 2.4 * s, cy + 1.8 * s), (cx + sg * 2.4 * s, cy - 1.8 * s)])
    elif kind == "SAL":
        psp.add_circle((cx, cy), 1.2 * s, dxfattribs={"layer": "S-ACC"})
        h = psp.add_hatch(color=7, dxfattribs={"layer": "S-ACC"})
        h.paths.add_edge_path().add_arc((cx, cy), 1.2 * s, 0, 360)
    elif kind == "MON":
        psp.add_circle((cx, cy), 2.6 * s, dxfattribs={"layer": "S-ACC"})
        psp.add_circle((cx, cy), 1.0 * s, dxfattribs={"layer": "S-ACC"})
    elif kind == "MED":
        psp.add_lwpolyline([(cx - 4, cy - 2.4), (cx + 4, cy - 2.4), (cx + 4, cy + 2.4), (cx - 4, cy + 2.4)],
                           close=True, dxfattribs={"layer": "S-ACC"})
        h = psp.add_hatch(color=7, dxfattribs={"layer": "S-ACC"})
        h.paths.add_polyline_path([(cx - 4, cy - 2.4), (cx, cy - 2.4), (cx, cy + 2.4), (cx - 4, cy + 2.4)])
    elif kind == "CP":
        psp.add_lwpolyline([(cx - 2.2, cy - 2.2), (cx + 2.2, cy - 2.2), (cx + 2.2, cy + 2.2), (cx - 2.2, cy + 2.2)],
                           close=True, dxfattribs={"layer": "S-ACC"})
        cl.text(psp, "CP", (cx, cy), 1.6, "S-ACC", "MIDDLE_CENTER")


def cuadro_simbologia(psp, x, y_top, rows, w_txt=120.0, row_h=6.0, title="SIMBOLOGÍA"):
    cl.text(psp, title, (x, y_top), 3.5, "A-TITULOS", "TOP_LEFT")
    y = y_top - 6.0
    w0 = 18.0
    for k, txt in rows:
        psp.add_lwpolyline([(x, y), (x + w0 + w_txt, y), (x + w0 + w_txt, y - row_h), (x, y - row_h)],
                           close=True, dxfattribs={"layer": "A-TABLAS"})
        psp.add_line((x + w0, y), (x + w0, y - row_h), dxfattribs={"layer": "A-TABLAS"})
        leyenda_simbolo(psp, k, x + w0 / 2, y - row_h / 2)
        cl.text(psp, txt, (x + w0 + 1.5, y - row_h / 2), 1.9, "A-TEXTO", "MIDDLE_LEFT")
        y -= row_h
    return y
