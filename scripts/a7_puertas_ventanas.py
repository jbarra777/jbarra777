"""Lámina A7 - PUERTAS, VENTANAS Y ACABADOS (lámina única para los 3 niveles).

Contenido según la referencia (ARQ_07 a 09): plantas con etiquetas de puertas (P-),
ventanas (V-), acabados de paredes (Pd-) y pisos (PI-); cuadro de puertas; cuadro de
ventanas; acabados en paredes, pisos y cielos; detalle de puertas y de ventanas; notas.
Las plantas se toman de los DXF vigentes (A2 rev3, A3 rev4, A4 rev4) sin mobiliario ni cotas.
Indicaciones del usuario: P-01 acceso principal (vestíbulo N1) de madera; habitaciones,
baños y walk-in de madera; puerta peatonal y portón metálicos; ventanas de aluminio y
vidrio; acabados de paredes de la referencia (interiores, baños, salpicadero, exteriores);
un mismo piso para interiores y baños; "ACABADO EN CIELOS": cielo raso tipo gypsum.
"""
import math

import ezdxf

import cadlib as cl
import hoja as H
from planta import P

REV = "rev2"
OUT = cl.ROOT / "planos" / "A7_puertas_ventanas"
NAME = f"SR-A7_PUERTAS_VENTANAS_{REV}"
SRC = {"N1": cl.ROOT / "planos/A2_nivel1/SR-A2_NIVEL1_rev3.dxf",
       "N2": cl.ROOT / "planos/A3_nivel2/SR-A3_NIVEL2_rev4.dxf",
       "N3": cl.ROOT / "planos/A4_nivel3/SR-A4_NIVEL3_rev4.dxf"}
OFF = {"N1": 0.0, "N2": -20.0, "N3": -40.0}          # desplazamiento en Y del marco de planta
KEEP = {"A-MURO", "A-MURO-TRAMA", "A-PUERTA", "A-VENTANA", "A-ESCALERA", "A-ESPACIOS",
        "E-COLUMNA", "A-EJES", "A-EJES-TXT", "T-LINDERO", "A-PROYECCION"}

doc = cl.new_doc()
msp = doc.modelspace()
for name, col, lw, lt in (("A-ETIQUETA", 7, 25, "Continuous"), ("D-CONTORNO", 7, 35, "Continuous"),
                          ("D-LINEAS", 7, 18, "Continuous"), ("D-OCULTO", 8, 13, "DASHED"),
                          ("D-TRAMA", 8, 9, "Continuous"), ("D-COTA", 7, 18, "Continuous"),
                          ("D-TXT", 7, 18, "Continuous")):
    doc.layers.add(name, color=col, linetype=lt, lineweight=lw)
for sc in (50, 75):
    if f"COTA-{sc}" not in doc.dimstyles:
        cl._dimstyle(doc, f"COTA-{sc}", sc)

# ================================================================ plantas (copiadas de los DXF)
for lv, path in SRC.items():
    src = ezdxf.readfile(path)
    for e in src.modelspace():
        if e.dxf.layer not in KEEP:
            continue
        c = e.copy()
        c.translate(0, OFF[lv], 0)
        msp.add_entity(c)


def Q(lv, x, y):
    p = P(x, y)
    return (p.x, p.y + OFF[lv])


def tag_door(lv, x, y, code):
    c = Q(lv, x, y)
    msp.add_circle(c, 0.36, dxfattribs={"layer": "A-ETIQUETA"})
    cl.text(msp, code, c, 0.15, "A-ETIQUETA", "MIDDLE_CENTER")


def tag_window(lv, x, y, code):
    cx, cy = Q(lv, x, y)
    w, h = 0.80, 0.34
    msp.add_lwpolyline([(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2),
                        (cx - w / 2, cy + h / 2)], close=True, dxfattribs={"layer": "A-ETIQUETA"})
    cl.text(msp, code, (cx, cy), 0.15, "A-ETIQUETA", "MIDDLE_CENTER")


def tag_finish(lv, x, y, code, target=None):
    """Etiqueta de acabado (Pd = pared, con flecha a la pared; PI = piso)."""
    cx, cy = Q(lv, x, y)
    w, h = 0.70, 0.28
    msp.add_lwpolyline([(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2),
                        (cx - w / 2, cy + h / 2)], close=True, dxfattribs={"layer": "A-ETIQUETA"})
    cl.text(msp, code, (cx, cy), 0.13, "A-ETIQUETA", "MIDDLE_CENTER")
    if target:
        tx, ty = Q(lv, *target)
        d = math.hypot(tx - cx, ty - cy)
        ux, uy = (tx - cx) / d, (ty - cy) / d
        sx = cx + ux * (w / 2 if abs(ux) > abs(uy) else 0)
        sy = cy + uy * (h / 2 if abs(uy) >= abs(ux) else 0)
        msp.add_line((sx, sy), (tx, ty), dxfattribs={"layer": "A-ETIQUETA"})
        a, s = 0.18, 0.07
        msp.add_solid([(tx, ty), (tx - ux * a + uy * s, ty - uy * a - ux * s),
                       (tx - ux * a - uy * s, ty - uy * a + ux * s)],
                      dxfattribs={"layer": "A-ETIQUETA"})


E, W = H.E, H.W
YF0, YR1 = H.YF0, H.YR1
# ---------------------------------------------------------------- nivel 1
tag_door("N1", 3.0, 1.0, "P-06")
tag_door("N1", 0.70, 0.75, "P-05")
tag_door("N1", 0.75, 16.25, "P-01")
tag_finish("N1", 7.6, 1.0, "PI-C")
tag_finish("N1", 3.85, 6.6, "PI-B")
tag_finish("N1", 0.75, 9.0, "PI-B")
tag_finish("N1", 2.35, 18.23, "PI-B")
tag_finish("N1", 6.0, 12.6, "PI-D")
tag_finish("N1", 6.5, 22.0, "PI-D")
tag_finish("N1", 6.0, 26.8, "PI-D")
tag_finish("N1", 7.6, 9.0, "Pd-D", (8.85, 9.0))
tag_finish("N1", 2.2, 14.0, "Pd-D", (E, 14.0))
tag_finish("N1", 2.4, 20.6, "Pd-D", (2.4, 19.60))
tag_finish("N1", 3.75, 18.23, "Pd-A", (4.69, 18.23))
# ---------------------------------------------------------------- niveles 2 y 3 (comunes)
for lv in ("N2", "N3"):
    tag_window(lv, 1.80, 1.45, "V-01")
    tag_window(lv, 4.21, 1.45, "V-03")
    tag_window(lv, 7.30, 1.45, "V-02")
    tag_window(lv, 1.80, 25.80, "V-04")
    tag_window(lv, 4.22, 25.80, "V-05")
    tag_window(lv, 7.30, 25.80, "V-06")
    tag_window(lv, 3.20, 8.25, "V-07")
    tag_window(lv, 6.90, 8.25, "V-08")
    tag_window(lv, 2.15, 9.45, "V-13")
    tag_window(lv, 6.90, 19.05, "V-12")
    tag_door(lv, 0.75, 8.45, "P-02")
    tag_door(lv, 4.15, 5.00, "P-03")
    tag_door(lv, 6.40, 6.00, "P-04")
    tag_finish(lv, 2.6, 2.8, "PI-A")
    tag_finish(lv, 4.15, 3.05, "PI-A")
    tag_finish(lv, 4.80, 3.05, "Pd-B", (5.27, 3.05))
    tag_finish(lv, 2.6, 6.6, "Pd-A", (2.6, 7.61))
    tag_finish(lv, 3.0, 1.45, "Pd-D", (3.0, YF0))
    tag_finish(lv, 3.05, 25.80, "Pd-D", (3.05, YR1))
    tag_finish(lv, 5.6, 9.45, "Pd-D", (5.6, 10.26))
    tag_finish(lv, 8.15, 18.25, "Pd-D", (8.85, 18.25))
    tag_finish(lv, 0.75, 13.95, "PI-A")
# nivel 2
tag_window("N2", 3.50, 9.85, "V-09")
tag_window("N2", 6.80, 9.85, "V-04")
tag_window("N2", 6.80, 17.45, "V-10")
tag_finish("N2", 3.7, 13.6, "PI-A")
tag_finish("N2", 7.9, 13.3, "Pd-C", (8.85, 13.3))
tag_finish("N2", 2.4, 12.2, "Pd-A", (2.4, 10.41))
tag_finish("N2", 3.0, 22.0, "PI-A")
tag_finish("N2", 3.0, 24.4, "Pd-A", (3.0, 25.03))
# nivel 3
tag_window("N3", 3.50, 9.85, "V-09")
tag_window("N3", 7.50, 9.85, "V-06")
tag_window("N3", 6.20, 17.45, "V-09")
tag_window("N3", 8.05, 17.45, "V-11")
tag_door("N3", 0.75, 16.00, "P-02")
tag_door("N3", 0.75, 19.10, "P-02")
tag_door("N3", 6.75, 15.50, "P-03")
tag_door("N3", 4.15, 22.20, "P-03")
tag_door("N3", 5.65, 12.70, "P-04")
tag_door("N3", 6.40, 21.25, "P-04")
tag_finish("N3", 3.7, 13.6, "PI-A")
tag_finish("N3", 2.4, 12.2, "Pd-A", (2.4, 10.41))
tag_finish("N3", 7.75, 16.35, "PI-A")
tag_finish("N3", 8.40, 16.35, "Pd-B", (8.85, 16.35))
tag_finish("N3", 3.6, 22.0, "PI-A")
tag_finish("N3", 4.15, 24.2, "PI-A")
tag_finish("N3", 4.80, 24.2, "Pd-B", (5.27, 24.2))
tag_finish("N3", 2.4, 21.0, "Pd-A", (2.4, 19.63))

# ================================================================ detalle de puertas (1:50)
DX, DY = 200.0, 0.0


def dpt(x, y):
    return (DX + x, DY + y)


def dline(a, b, layer="D-LINEAS", lts=None):
    e = msp.add_line(dpt(*a), dpt(*b), dxfattribs={"layer": layer})
    if lts:
        e.dxf.ltscale = lts


def drect(x0, y0, x1, y1, layer="D-CONTORNO"):
    msp.add_lwpolyline([dpt(x0, y0), dpt(x1, y0), dpt(x1, y1), dpt(x0, y1)], close=True,
                       dxfattribs={"layer": layer})


def dtext(s, x, y, h, align="MIDDLE_CENTER", rot=0):
    cl.text(msp, s, dpt(x, y), h, "D-TXT", align, rot)


def ddim(a, b, base, horizontal, style):
    if horizontal:
        d = msp.add_linear_dim(base=dpt(0, base), p1=dpt(a, base), p2=dpt(b, base), angle=0,
                               dimstyle=style, dxfattribs={"layer": "D-COTA"})
    else:
        d = msp.add_linear_dim(base=dpt(base, 0), p1=dpt(base, a), p2=dpt(base, b), angle=90,
                               dimstyle=style, dxfattribs={"layer": "D-COTA"})
    d.render()


def swing(x0, x1, h):
    """Indicación de abatimiento en elevación: bisagra a la izquierda."""
    dline((x1 - 0.06, 0.06), (x0 + 0.06, h / 2), "D-OCULTO", 0.4 * 0.05)
    dline((x1 - 0.06, h - 0.06), (x0 + 0.06, h / 2), "D-OCULTO", 0.4 * 0.05)


DOORS = [("P-01", "ACCESO PPAL.", 1.00, 2.10, "madera_paneles"),
         ("P-02", "HABITACIONES", 0.90, 2.10, "madera"),
         ("P-03", "BAÑOS", 0.80, 2.10, "romanilla"),
         ("P-04", "WALK-IN", 0.80, 2.10, "madera"),
         ("P-05", "PUERTA PEATONAL", 1.00, 2.40, "metal"),
         ("P-06", "PORTÓN VEHICULAR", 7.29, 2.40, "porton")]
x = 0.0
for code, lab, w, h, kind in DOORS:
    drect(x - 0.05, 0.0, x + w + 0.05, h + 0.05)                      # marco
    drect(x, 0.0, x + w, h, "D-LINEAS")                               # hoja
    if kind == "madera_paneles":
        for y0, y1 in ((0.15, 0.95), (1.10, 1.95)):
            drect(x + 0.15, y0, x + w - 0.15, y1, "D-LINEAS")
    if kind == "romanilla":
        for i in range(7):
            yy = 0.15 + i * 0.05
            dline((x + 0.12, yy), (x + w - 0.12, yy))
        drect(x + 0.12, 0.15, x + w - 0.12, 0.50, "D-LINEAS")
    if kind in ("metal", "porton"):
        nleaf = 4 if kind == "porton" else 1
        for i in range(1, nleaf):
            dline((x + w * i / nleaf, 0.0), (x + w * i / nleaf, h), "D-CONTORNO")
        for i in range(1, 12):
            dline((x + 0.04, h * i / 12), (x + w - 0.04, h * i / 12))
    if kind != "porton":
        dline((x + w - 0.12, 0.95), (x + w - 0.12, 1.15), "D-CONTORNO")   # jaladera
        swing(x, x + w, h)
    ddim(x, x + w, h + 0.35, True, "COTA-50")
    ddim(0.0, h, x - 0.30, False, "COTA-50")
    dtext(lab, x + w / 2, -0.30, 0.10)
    dtext(code, x + w / 2, -0.52, 0.10)
    x += w + 0.95
DOOR_W = x - 0.95
dline((-0.6, 0.0), (DOOR_W + 0.3, 0.0), "D-CONTORNO")

# ================================================================ detalle de ventanas (1:75)
VX, VY = 230.0, 0.0


def vpt(x, y):
    return (VX + x, VY + y)


def vline(a, b, layer="D-LINEAS", lts=None):
    e = msp.add_line(vpt(*a), vpt(*b), dxfattribs={"layer": layer})
    if lts:
        e.dxf.ltscale = lts


def vrect(x0, y0, x1, y1, layer="D-CONTORNO"):
    msp.add_lwpolyline([vpt(x0, y0), vpt(x1, y0), vpt(x1, y1), vpt(x0, y1)], close=True,
                       dxfattribs={"layer": layer})


def vdim(a, b, base, horizontal):
    if horizontal:
        d = msp.add_linear_dim(base=vpt(0, base), p1=vpt(a, base), p2=vpt(b, base), angle=0,
                               dimstyle="COTA-75", dxfattribs={"layer": "D-COTA"})
    else:
        d = msp.add_linear_dim(base=vpt(base, 0), p1=vpt(base, a), p2=vpt(base, b), angle=90,
                               dimstyle="COTA-75", dxfattribs={"layer": "D-COTA"})
    d.render()


# código, ancho, alto, paños, travesaño fijo inferior, fija, arenado
WINDOWS = [("V-01", 2.20, 2.20, 2, 0.90, False, False),
           ("V-02", 1.80, 2.20, 2, 0.90, False, False),
           ("V-03", 0.90, 2.20, 1, 0.90, False, True),
           ("V-04", 2.20, 1.30, 2, None, False, False),
           ("V-05", 0.75, 1.30, 1, None, False, True),
           ("V-06", 1.80, 1.30, 2, None, False, False),
           ("V-07", 2.40, 1.30, 2, None, False, False),
           ("V-08", 2.60, 1.30, 2, None, False, False),
           ("V-09", 1.60, 1.30, 2, None, False, False),
           ("V-10", 2.80, 1.30, 3, None, False, False),
           ("V-11", 1.10, 1.30, 1, None, False, True),
           ("V-12", 3.00, 1.30, 3, None, False, False),
           ("V-13", 2.30, 2.70, 2, None, True, False)]
ROWS = [(WINDOWS[:7], 3.95), (WINDOWS[7:], 0.0)]
for row, y0 in ROWS:
    x = 0.0
    for code, w, h, n, tr, fixed, sand in row:
        vrect(x, y0, x + w, y0 + h)
        vrect(x + 0.04, y0 + 0.04, x + w - 0.04, y0 + h - 0.04, "D-LINEAS")
        xs = [x + w * i / n for i in range(n + 1)]
        for xm in xs[1:-1]:
            vline((xm, y0), (xm, y0 + h), "D-CONTORNO")
        ya = y0
        if tr:
            ya = y0 + tr
            vline((x, ya), (x + w, ya), "D-CONTORNO")
            for a, b in zip(xs[:-1], xs[1:]):
                cl.text(msp, "F", vpt((a + b) / 2, (y0 + ya) / 2), 0.17, "D-TXT", "MIDDLE_CENTER")
        for a, b in zip(xs[:-1], xs[1:]):
            if fixed:
                cl.text(msp, "F", vpt((a + b) / 2, y0 + h / 2), 0.17, "D-TXT", "MIDDLE_CENTER")
            else:                                     # ventila: triángulo invertido (bisagra arriba)
                vline((a + 0.06, y0 + h - 0.06), ((a + b) / 2, ya + 0.06), "D-OCULTO", 0.03)
                vline((b - 0.06, y0 + h - 0.06), ((a + b) / 2, ya + 0.06), "D-OCULTO", 0.03)
        if sand:
            ht = msp.add_hatch(dxfattribs={"layer": "D-TRAMA"})
            ht.paths.add_polyline_path([vpt(x + 0.04, y0 + 0.04), vpt(x + w - 0.04, y0 + 0.04),
                                        vpt(x + w - 0.04, y0 + h - 0.04),
                                        vpt(x + 0.04, y0 + h - 0.04)])
            ht.set_pattern_fill("DOTS", scale=0.07)
        vdim(x, x + w, y0 + h + 0.30, True)
        vdim(y0, y0 + h, x - 0.25, False)
        cl.text(msp, code, vpt(x + w / 2, y0 - 0.35), 0.15, "D-TXT", "MIDDLE_CENTER")
        x += w + 0.95

# ================================================================ hoja
psp = doc.layouts.new("A7-PUERTAS-VENTANAS")
psp.page_setup(size=(cl.A1_W, cl.A1_H), margins=(0, 0, 0, 0), units="mm")
doc.layouts.set_active_layout("A7-PUERTAS-VENTANAS")
cl.frame(psp)


def vp(center, size, scale, mc):
    v = psp.add_viewport(center=center, size=size, view_center_point=mc,
                         view_height=size[1] * scale / 1000.0, dxfattribs={"layer": "A-VIEWPORT"})
    v.dxf.flags = v.dxf.flags | 16384
    return v


PX = 186.0
for lv, yc, title in (("N3", 512.0, "PLANTA NIVEL 3"), ("N2", 362.0, "PLANTA NIVEL 2"),
                      ("N1", 212.0, "PLANTA NIVEL 1")):
    vp((PX, yc), (316.0, 136.0), 100, (14.8, 3.75 + OFF[lv]))
    cl.text(psp, title, (30.0, yc - 68.0), 4.5, "A-TITULOS", "TOP_LEFT")
    cl.text(psp, "PUERTAS, VENTANAS Y ACABADOS - Esc. 1:100", (30.0, yc - 74.5), 2.5, "A-TEXTO",
            "TOP_LEFT")
# detalle de ventanas
vp((186.0, 72.0), (316.0, 104.0), 75, (VX + 8.6, 3.30))
cl.text(psp, "DETALLE VENTANAS", (232.0, 128.0), 4.5, "A-TITULOS", "TOP_LEFT")
cl.text(psp, "Esc. 1:75 - VISTA EXTERIOR", (232.0, 121.5), 2.5, "A-TEXTO", "TOP_LEFT")

# ---------------------------------------------------------------- cuadros
XR = 352.0


def table2(x0, y_top, col_w, rows, row_hs, h=2.0, aligns=None):
    """Tabla con celdas de varias líneas (separadas por '\\n')."""
    total_w = sum(col_w)
    xs = [x0]
    for w in col_w:
        xs.append(xs[-1] + w)
    y = y_top
    ys = [y]
    for rh in row_hs:
        y -= rh
        ys.append(y)
    cl.rect(psp, x0, ys[-1], x0 + total_w, y_top, "A-TABLAS")
    for i, row in enumerate(rows):
        yt, yb = ys[i], ys[i + 1]
        if i > 0:
            psp.add_line((x0, yt), (x0 + total_w, yt), dxfattribs={"layer": "A-TABLAS"})
        for j, s in enumerate(row):
            if j > 0:
                psp.add_line((xs[j], yt), (xs[j], yb), dxfattribs={"layer": "A-TABLAS"})
            lines = s.split("\n")
            a = aligns[j] if aligns and i > 0 else "MIDDLE_CENTER"
            for k, t in enumerate(lines):
                yy = (yt + yb) / 2 + (len(lines) - 1) * h * 0.75 - k * h * 1.5
                if a == "MIDDLE_LEFT":
                    p = (xs[j] + 1.5, yy)
                else:
                    p = ((xs[j] + xs[j + 1]) / 2, yy)
                cl.text(psp, t, p, h, "A-TEXTO", a)
    return ys[-1]


def table_title(x, y, w, title):
    cl.text(psp, title, (x + w / 2, y), 3.2, "A-TITULOS", "TOP_CENTER")
    cl.text(psp, "(UNIDADES EN METROS)", (x + w / 2, y - 4.6), 2.0, "A-TEXTO", "TOP_CENTER")


# puertas
cw = [20, 16, 14, 52, 13, 132, 101]
y = 580.0
table_title(XR, y, sum(cw), "CUADRO DE PUERTAS")
rows = [["PUERTA", "ANCHO", "ALTO", "TIPO", "CANT", "UBICACIÓN", "MATERIAL"],
        ["P-01", "1,00", "2,10", "BATIENTE", "1", "ACCESO PPAL. (VESTÍBULO NIVEL 1)", "MADERA"],
        ["P-02", "0,90", "2,10", "BATIENTE", "4", "HABITACIONES (SUITES 1, 2 Y 3)", "MADERA"],
        ["P-03", "0,80", "2,10", "BATIENTE", "4", "BAÑOS", "MADERA CON ROMANILLA INFERIOR"],
        ["P-04", "0,80", "2,10", "BATIENTE", "4", "WALK-IN CLOSET", "MADERA"],
        ["P-05", "1,00", "2,40", "BATIENTE", "1", "PUERTA PEATONAL (FRENTE NIVEL 1)", "METAL (ACERO)"],
        ["P-06", "7,29", "2,40", "ABATIBLE 4 HOJAS", "1", "PORTÓN VEHICULAR (FRENTE NIVEL 1)",
         "METAL (ACERO)"]]
y = table2(XR, y - 8.5, cw, rows, [5.2] * len(rows),
           aligns=["MIDDLE_CENTER"] * 5 + ["MIDDLE_LEFT", "MIDDLE_LEFT"])
# ventanas
cw = [20, 16, 14, 60, 13, 173, 52]
y -= 5.0
table_title(XR, y, sum(cw), "CUADRO DE VENTANAS")
VEN = "VENTILA ABATIBLE"
rows = [["VENTANA", "ANCHO", "ALTO", "TIPO", "CANT", "UBICACIÓN", "MATERIAL"],
        ["V-01", "2,20", "2,20", "FIJA INF. + " + VEN, "2", "DORMITORIO SUITE 1, FACHADA PRINCIPAL (N2 Y N3)", "ALUMINIO Y VIDRIO"],
        ["V-02", "1,80", "2,20", "FIJA INF. + " + VEN, "2", "WALK-IN SUITE 1, FACHADA PRINCIPAL (N2 Y N3)", "ALUMINIO Y VIDRIO"],
        ["V-03", "0,90", "2,20", "FIJA INF. + " + VEN, "2", "BAÑO SUITE 1, FACHADA PRINCIPAL (VIDRIO ARENADO)", "ALUMINIO Y VIDRIO"],
        ["V-04", "2,20", "1,30", VEN, "3", "SALA Y SUITE 3, FACHADA POSTERIOR; COCINA A P1 (N2)", "ALUMINIO Y VIDRIO"],
        ["V-05", "0,75", "1,30", VEN, "2", "FACHADA POSTERIOR: SALA (N2) Y BAÑO SUITE 3 (VIDRIO ARENADO)", "ALUMINIO Y VIDRIO"],
        ["V-06", "1,80", "1,30", VEN, "3", "FACHADA POSTERIOR (N2 Y N3); WALK-IN SUITE 2 A P1", "ALUMINIO Y VIDRIO"],
        ["V-07", "2,40", "1,30", VEN, "2", "SUITE 1 HACIA PATIO P1 (N2 Y N3)", "ALUMINIO Y VIDRIO"],
        ["V-08", "2,60", "1,30", VEN, "2", "WALK-IN SUITE 1 HACIA PATIO P1 (N2 Y N3)", "ALUMINIO Y VIDRIO"],
        ["V-09", "1,60", "1,30", VEN, "3", "COCINA (N2) Y SUITE 2 (N3) A P1; SUITE 2 A P2", "ALUMINIO Y VIDRIO"],
        ["V-10", "2,80", "1,30", VEN, "1", "COCINA HACIA PATIO P2 (N2)", "ALUMINIO Y VIDRIO"],
        ["V-11", "1,10", "1,30", VEN, "1", "BAÑO SUITE 2 HACIA PATIO P2 (N3, VIDRIO ARENADO)", "ALUMINIO Y VIDRIO"],
        ["V-12", "3,00", "1,30", VEN, "2", "SALA (N2) Y SUITE 3 (N3) HACIA PATIO P2", "ALUMINIO Y VIDRIO"],
        ["V-13", "2,30", "2,70", "FIJA", "2", "GALERÍA DEL PASILLO HACIA PATIO P1 (N2 Y N3)", "ALUMINIO Y VIDRIO"]]
y = table2(XR, y - 8.5, cw, rows, [5.2] * len(rows),
           aligns=["MIDDLE_CENTER"] * 5 + ["MIDDLE_LEFT", "MIDDLE_CENTER"])
# acabados en paredes
cw = [20, 262, 66]
y -= 5.0
cl.text(psp, "ACABADO EN PAREDES", (XR + sum(cw) / 2, y), 3.2, "A-TITULOS", "TOP_CENTER")
rows = [["ITEM", "TIPO DE ACABADO", "COLOR"],
        ["Pd - A", "PAREDES INTERNAS: REPELLO GRUESO, ACABADO LISO, CON DOS MANOS DE\n"
         "PINTURA CLASE A, CON BASE SATINADO.", "REFERENCIA: PANTONE,\nALMOND MILK"],
        ["Pd - B", "BAÑOS: REPELLO GRUESO, ACABADO CON CERÁMICA O PORCELANATO.\n"
         "1,80 m EN DUCHAS.", "BLANCO"],
        ["Pd - C", "COCINA: REPELLO GRUESO, ACABADO CON CERÁMICA O PORCELANATO\n"
         "EN SALPICADERO.", "BLANCO"],
        ["Pd - D", "PAREDES EXTERNAS: REPELLO GRUESO, ACABADO ESTUCO PULIDO.", "GRIS CONCRETO"]]
y = table2(XR, y - 5.0, cw, rows, [5.2, 8.0, 8.0, 8.0, 6.0],
           aligns=["MIDDLE_CENTER", "MIDDLE_LEFT", "MIDDLE_CENTER"])
# acabados en pisos
y -= 5.0
cl.text(psp, "ACABADO EN PISOS", (XR + sum(cw) / 2, y), 3.2, "A-TITULOS", "TOP_CENTER")
rows = [["ITEM", "TIPO DE ACABADO", "COLOR"],
        ["PI - A", "PISO PARA INTERIORES Y BAÑOS, PORCELANATO 60x60CM BLANCO O COLOR\n"
         "CLARO CON RODAPIÉ DE PORCELANATO.", "BLANCO"],
        ["PI - B", "CONTRAPISO DE CONCRETO DE 0,10 m (ESTACIONAMIENTOS, PASILLO,\n"
         "VESTÍBULO Y GRADAS DEL NIVEL 1).", "GRIS CONCRETO"],
        ["PI - C", "ZACATE BLOCK (PERMEABLE) EN RETIRO FRONTAL.", "NATURAL"],
        ["PI - D", "GRAVA (JARDÍN SECO).", "NATURAL"]]
y = table2(XR, y - 5.0, cw, rows, [5.2, 8.0, 8.0, 5.5, 5.5],
           aligns=["MIDDLE_CENTER", "MIDDLE_LEFT", "MIDDLE_CENTER"])
# acabados en cielos
y -= 5.0
cw2 = [282, 66]
cl.text(psp, "ACABADO EN CIELOS", (XR + sum(cw2) / 2, y), 3.2, "A-TITULOS", "TOP_CENTER")
rows = [["TIPO DE ACABADO", "COLOR"],
        ["CIELO RASO TIPO GYPSUM (REGULAR PLANO, SUSPENDIDO A 2,70 m), NIVELES 2 Y 3.", "BLANCO"],
        ["NIVEL 1: ESTRUCTURA DE ACERO EXPUESTA (SIN CIELO RASO).", "SEGÚN ESTRUCTURAL"]]
y = table2(XR, y - 5.0, cw2, rows, [5.2, 5.5, 5.5], aligns=["MIDDLE_LEFT", "MIDDLE_CENTER"])

# detalle de puertas
yd = y - 12.0
vp((XR + 177.0, yd - 40.0), (354.0, 80.0), 50, (DX + DOOR_W / 2, 1.20))
cl.text(psp, "DETALLE PUERTAS", (XR, yd - 80.0), 4.5, "A-TITULOS", "TOP_LEFT")
cl.text(psp, "Esc. 1:50 - VISTA DESDE EL LADO DE APERTURA", (XR, yd - 86.5), 2.5, "A-TEXTO",
        "TOP_LEFT")
# notas
y = yd - 96.0
cl.text(psp, "NOTAS:", (XR, y), 3.5, "A-TITULOS", "TOP_LEFT")
notas = [
    "TODAS LAS MEDIDAS ESTÁN DADAS EN METROS. [PR]",
    "EL NIVEL ±0.00 ES EL NIVEL DE ACERA (NPT DEL NIVEL 1); N2 +3.00 Y N3 +6.00.",
    "LAS MEDIDAS DEBEN SER VERIFICADAS EN SITIO. [PR]",
    "LOS MARCOS DE LAS VENTANAS SERÁN DE ALUMINIO COLOR NEGRO. [PR]",
    "VENTANAS: VENTILA ABATIBLE HACIA AFUERA (BISAGRA SUPERIOR, TRIÁNGULO INVERTIDO); F = PAÑO "
    "FIJO. FACHADA PRINCIPAL DE 0.00 A 2.20 m CON PAÑO FIJO INFERIOR DE SEGURIDAD HASTA 0.90 m; "
    "LAS DEMÁS CON ANTEPECHO DE 0.90 m Y DINTEL A 2.20 m. VIDRIO ARENADO EN BAÑOS.",
    "PUERTAS DE 2.10 m DE ALTO. P-05 Y P-06 (2.40 m) METÁLICAS SEGÚN FACHADA A5.",
    "PLANTAS SIN MOBILIARIO NI COTAS; DISTRIBUCIÓN Y MEDIDAS SEGÚN LÁMINAS A2, A3 Y A4.",
]
y = cl.notes_block(psp, XR, y - 6, [f"{i}.- {t}" for i, t in enumerate(notas, 1)]
                   + [cl.NOTA_PR], 2.0, 350)

H.titleblock(doc, psp, "A7", "PUERTAS Y VENTANAS",
             ["PLANTAS NIVELES 1, 2 Y 3.", "CUADROS DE PUERTAS Y VENTANAS.",
              "ACABADOS EN PAREDES, PISOS Y CIELOS.", "DETALLE DE PUERTAS Y VENTANAS.", "NOTAS.", ""],
             [("0", "06-10-2026", "VERSIÓN DE TRABAJO PARA REVISIÓN"),
              ("1", "06-10-2026", "V-05 CON VIDRIO ARENADO"),
              ("2", "06-10-2026", "V-03 DE 0,90 (COLUMNA EJE C-1)")],
             escalas="1:100 / INDICADAS")

OUT.mkdir(parents=True, exist_ok=True)
doc.saveas(OUT / f"{NAME}.dxf")
cl.render_pdf(doc, "A7-PUERTAS-VENTANAS", OUT / f"{NAME}.pdf")
print("notas y_fin", round(y, 1), "| detalle puertas ancho", round(DOOR_W, 2))
print("DXF:", OUT / f"{NAME}.dxf")
