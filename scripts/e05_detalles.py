"""Lámina E05 - DETALLES ELÉCTRICOS (agregada por el usuario).

Detalles constructivos de la referencia (RIVERGRAND EL07), sin marcas comerciales:
conexión de apagador, de tomacorriente y de caja octogonal de paso; ubicación de accesorios en
pared; previstas para TV en pared. Detalles propios con datos ya aprobados en E01-E04:
alturas de montaje (simbología), zanja de acometida subterránea (notas de canalizaciones y
unifilar) y puesta a tierra (unifilar). Dibujos esquemáticos, sin escala.
"""
import cadlib as cl
import elec as EL
import hoja as H

REV = "rev1"
OUT = cl.ROOT / "planos" / "E05_detalles"
NAME = f"SR-E05_DETALLES_{REV}"
LAYOUT = "E05-DETALLES"

doc = cl.new_doc()
EL.layers(doc)
for name, col, lw, lt in (("D-LINEAS", 7, 25, "Continuous"), ("D-FINO", 8, 13, "Continuous"),
                          ("D-TRAMA", 8, 9, "Continuous"), ("D-COND", 7, 35, "Continuous")):
    doc.layers.add(name, color=col, linetype=lt, lineweight=lw)
psp = doc.layouts.new(LAYOUT)
psp.page_setup(size=(cl.A1_W, cl.A1_H), margins=(0, 0, 0, 0), units="mm")
doc.layouts.set_active_layout(LAYOUT)
cl.frame(psp)


def L(a, b, layer="D-LINEAS"):
    psp.add_line(a, b, dxfattribs={"layer": layer})


def R(x0, y0, x1, y1, layer="D-LINEAS"):
    psp.add_lwpolyline([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], close=True,
                       dxfattribs={"layer": layer})


def C(c, r, layer="D-LINEAS"):
    psp.add_circle(c, r, dxfattribs={"layer": layer})


def T(s, p, h=1.9, al="MIDDLE_LEFT"):
    cl.text(psp, s, p, h, "A-TEXTO", al)


def call(target, pos, txt, w=48.0, h=1.8):
    """Rótulo con línea guía (texto a la derecha o a la izquierda de pos)."""
    L(pos, target, "D-FINO")
    psp.add_circle(target, 0.5, dxfattribs={"layer": "D-FINO"})
    right = pos[0] >= target[0]
    cl.mtext(psp, txt, (pos[0] + (1.5 if right else -1.5), pos[1]), h, w, layer="A-TEXTO",
             attach=4 if right else 6)


def hatch(pts, pattern="ANSI31", scale=0.6):
    ht = psp.add_hatch(dxfattribs={"layer": "D-TRAMA"})
    ht.paths.add_polyline_path(pts)
    ht.set_pattern_fill(pattern, scale=scale)


def cell(x, y, w, h, title, sub="S/E"):
    R(x, y, x + w, y + h, "D-FINO")
    cl.text(psp, title, (x + 4, y + 10.0), 3.0, "A-TITULOS", "BOTTOM_LEFT")
    cl.text(psp, sub, (x + 4, y + 5.0), 2.2, "A-TEXTO", "BOTTOM_LEFT")


W_, H_ = 166.0, 272.0
COLS = [33.0, 33.0 + W_ + 3, 33.0 + 2 * (W_ + 3), 33.0 + 3 * (W_ + 3)]
ROWS = [305.0, 28.0]


# ================================================================ 1. alturas de montaje
def det_alturas(x, y):
    cell(x, y, W_, H_, "DET. 1 - ALTURAS DE MONTAJE", "ELEVACIÓN DE PARED - S/E")
    k = 40.0                                              # mm por metro
    x0, y0 = x + 22, y + 40
    L((x0, y0), (x0 + 120, y0), "D-COND")                 # piso
    hatch([(x0, y0 - 3), (x0 + 120, y0 - 3), (x0 + 120, y0), (x0, y0)], "ANSI31", 0.5)
    T("NPT", (x0 + 122, y0), 1.9)
    items = [(15, 0.30, "TC", "TOMACORRIENTE 0,30 m"),
             (45, 1.50, "TC150", "TOMACORRIENTE 1,50 m"),
             (75, 1.30, "S", "APAGADOR 1,30 m"),
             (105, 1.90, "M", "MEDIDOR 1,90 m (EXTERIOR)")]
    for dx, hgt, kind, lab in items:
        cx, cy = x0 + dx, y0 + hgt * k
        EL.sym(psp, kind, cx, cy, 3.0)
        L((cx + 6, y0), (cx + 6, cy), "D-FINO")
        for yy in (y0, cy):
            L((cx + 4.5, yy), (cx + 7.5, yy), "D-FINO")
        cl.text(psp, f"{hgt:.2f}".replace(".", ","), (cx + 7.5, (y0 + cy) / 2), 1.9, "A-TEXTO",
                "MIDDLE_LEFT", 90)
        cl.mtext(psp, lab, (cx, cy + 9), 1.7, 26, layer="A-TEXTO", attach=8)
    cl.mtext(psp, "ALTURAS AL CENTRO DE LA CAJA, SOBRE EL NIVEL DE PISO TERMINADO (S.N.P.T.), "
             "SEGÚN LA SIMBOLOGÍA (E01-E04). TOMAS DE 1,50 m SOBRE MUEBLES DE COCINA Y DESPENSA. "
             "SALIDAS DE 240 V SEGÚN FABRICANTE.", (x + 6, y + 30), 1.8, W_ - 12, layer="A-TEXTO", attach=7)


# ================================================================ 2 y 3. conexión de apagador / tomacorriente
def caja_rect(x, y, w=26.0, h=40.0):
    R(x, y, x + w, y + h, "D-LINEAS")
    R(x + 2, y + 2, x + w - 2, y + h - 2, "D-FINO")


def det_conexion(x, y, kind):
    tit = "DET. 2 - CONEXIÓN DE APAGADOR" if kind == "S" else "DET. 3 - CONEXIÓN DE TOMACORRIENTE"
    cell(x, y, W_, H_, tit, "VISTA FRONTAL - S/E")
    bx, by = x + 45, y + 120
    caja_rect(bx, by)
    R(bx + 9, by + 40, bx + 17, by + 70, "D-LINEAS")                 # tubería
    R(bx + 7, by + 40, bx + 19, by + 46, "D-LINEAS")                 # conector
    # dispositivo
    R(bx + 34, by + 4, bx + 50, by + 36, "D-LINEAS")
    if kind == "S":
        R(bx + 39, by + 15, bx + 45, by + 25, "D-LINEAS")
    else:
        for yy in (by + 10, by + 22):
            C((bx + 42, yy + 3), 3.2)
    # conductores
    c1 = "RETORNO (AZUL)" if kind == "S" else "NEUTRO (BLANCO)"
    psp.add_lwpolyline([(bx + 12, by + 60), (bx + 12, by + 30), (bx + 36, by + 28)],
                       dxfattribs={"layer": "D-COND"})
    psp.add_lwpolyline([(bx + 14, by + 60), (bx + 14, by + 22), (bx + 36, by + 14)],
                       dxfattribs={"layer": "D-COND"})
    psp.add_lwpolyline([(bx + 10, by + 60), (bx + 6, by + 8), (bx + 36, by + 6)],
                       dxfattribs={"layer": "D-FINO"})
    call((bx + 13, by + 66), (x + 105, by + 92), "TUBERÍA ELÉCTRICA")
    call((bx + 18, by + 43), (x + 105, by + 80), "CONECTOR DE PRESIÓN")
    call((bx + 26, by + 36), (x + 105, by + 68), "CAJA RECTANGULAR CERTIFICADA")
    call((bx + 24, by + 29), (x + 105, by + 54), "FASE (ROJO)")
    call((bx + 24, by + 18), (x + 105, by + 42), c1)
    call((bx + 20, by + 7), (x + 105, by + 20), "TIERRA (VERDE)")
    call((bx + 42, by + 33), (x + 105, by + 6),
         "APAGADOR" if kind == "S" else "TOMACORRIENTE DOBLE POLARIZADO")
    cl.mtext(psp, "NOTAS: DEJAR COLAS DE CABLE DE 15 cm. EL BORDE FRONTAL DE LA CAJA RECTANGULAR "
             "DEBERÁ QUEDAR A MÁXIMO 6 mm DEL REPELLO TERMINADO EN MATERIALES NO INFLAMABLES, Y A RAS "
             "DE PARED TERMINADA EN MATERIALES INFLAMABLES.", (x + 6, y + 75), 1.8, W_ - 12,
             layer="A-TEXTO", attach=7)


# ================================================================ 4. caja octogonal de paso
def det_octogonal(x, y):
    cell(x, y, W_, H_, "DET. 4 - CAJA OCTOGONAL DE PASO", "CONEXIÓN DE LUMINARIA - S/E")
    import math
    cx, cy, r = x + 60, y + 150, 24.0
    pts = [(cx + r * math.cos(math.radians(22.5 + 45 * i)), cy + r * math.sin(math.radians(22.5 + 45 * i)))
           for i in range(8)]
    psp.add_lwpolyline(pts, close=True, dxfattribs={"layer": "D-LINEAS"})
    for sx in (-1, 1):
        R(cx + sx * r, cy - 4, cx + sx * (r + 22), cy + 4, "D-LINEAS")
    R(cx - 4, cy + r - 2, cx + 4, cy + r + 18, "D-LINEAS")
    psp.add_lwpolyline([(cx - r - 18, cy + 1), (cx - 4, cy + 4), (cx, cy + r + 14)],
                       dxfattribs={"layer": "D-COND"})
    psp.add_lwpolyline([(cx - r - 18, cy - 1), (cx + 4, cy - 4), (cx + r + 18, cy - 1)],
                       dxfattribs={"layer": "D-COND"})
    psp.add_lwpolyline([(cx - r - 18, cy - 3), (cx, cy - 14), (cx + r + 18, cy - 3)],
                       dxfattribs={"layer": "D-FINO"})
    call((cx, cy + r + 16), (x + 100, cy + 70), "COLA PARA LUMINARIA, CABLE 3 x 14 AWG", 44)
    call((cx - r - 12, cy + 4), (x + 45, cy + 45), "TUBERÍA ELÉCTRICA", 30)
    call((cx - 2, cy + 6), (x + 45, cy + 33), "FASE (ROJO)", 30)
    call((cx + 10, cy - 3), (x + 110, cy + 30), "NEUTRO (BLANCO)", 40)
    call((cx, cy - 13), (x + 45, cy - 36), "TIERRA (VERDE)", 30)
    call((cx + r + 10, cy + 4), (x + 110, cy + 12), "CONECTOR DE PRESIÓN", 40)
    call((cx + r * 0.7, cy - r * 0.7), (x + 110, cy - 40), "CAJA OCTOGONAL CERTIFICADA", 40)
    cl.mtext(psp, "EMPALMES ÚNICAMENTE DENTRO DE CAJAS, CON CONECTORES DE EMPALME. LOS CONDUCTORES "
             "VIAJAN CONTINUOS ENTRE CAJA Y CAJA.", (x + 6, y + 50), 1.8, W_ - 12,
             layer="A-TEXTO", attach=7)


# ================================================================ 5. ubicación de accesorios en pared
def det_ubicacion(x, y):
    cell(x, y, W_, H_, "DET. 5 - UBICACIÓN DE ACCESORIOS EN PARED", "ELEVACIONES - S/E")
    ys = y + 40
    subs = [("EN PARED", x + 10), ("EN MOCHETA", x + 62), ("ACCESORIOS ADYACENTES", x + 114)]
    for lab, sx in subs:
        L((sx, ys), (sx + 46, ys), "D-COND")
        cl.text(psp, lab, (sx + 23, ys - 6), 1.8, "A-TEXTO", "MIDDLE_CENTER")
    # en pared: borde de pared, apagador y toma
    sx = subs[0][1]
    L((sx + 4, ys), (sx + 4, ys + 170), "D-LINEAS")
    R(sx + 12, ys + 120, sx + 18, ys + 130)
    R(sx + 12, ys + 15, sx + 20, ys + 21)
    call((sx + 4, ys + 90), (sx + 30, ys + 160), "BORDE DE PARED", 18, 1.6)
    # mocheta
    sx = subs[1][1]
    L((sx + 14, ys), (sx + 14, ys + 170), "D-LINEAS")
    L((sx + 30, ys), (sx + 30, ys + 170), "D-LINEAS")
    R(sx + 19, ys + 120, sx + 25, ys + 130)
    R(sx + 18, ys + 15, sx + 26, ys + 21)
    call((sx + 30, ys + 150), (sx + 36, ys + 182), "MOCHETA MENOR A 40 cm: ACCESORIO CENTRADO", 22, 1.6)
    # adyacentes
    sx = subs[2][1]
    L((sx + 4, ys), (sx + 4, ys + 170), "D-LINEAS")
    R(sx + 10, ys + 120, sx + 30, ys + 130)
    for i in range(3):
        R(sx + 12 + i * 6, ys + 122, sx + 16 + i * 6, ys + 128, "D-FINO")
    for i in range(3):
        R(sx + 10 + i * 12, ys + 15, sx + 18 + i * 12, ys + 21)
    call((sx + 30, ys + 125), (sx + 34, ys + 150), "APAGADORES ADYACENTES EN CAJA DE MÚLTIPLES GANGS", 16, 1.6)
    cl.mtext(psp, "ALTURAS SEGÚN DET. 1.", (x + 6, y + 22), 1.8, W_ - 12, layer="A-TEXTO", attach=7)


# ================================================================ 6. previstas para TV en pared
def det_tv(x, y):
    cell(x, y, W_, H_, "DET. 6 - PREVISTAS PARA TV EN PARED", "ELEVACIÓN - S/E")
    x0, y0 = x + 12, y + 50
    L((x0, y0), (x0 + 100, y0), "D-COND")
    R(x0 + 5, y0 + 120, x0 + 95, y0 + 185, "D-LINEAS")                   # TV
    cl.text(psp, "TV EN PARED", (x0 + 50, y0 + 178), 1.9, "A-TEXTO", "MIDDLE_CENTER")
    boxes = [(x0 + 25, "TC"), (x0 + 50, "TC"), (x0 + 75, "TV")]
    for bxx, kind in boxes:
        R(bxx - 4, y0 + 150, bxx + 4, y0 + 158)
        L((bxx, y0 + 150), (bxx, y0 + 18), "D-FINO")
        R(bxx - 4, y0 + 10, bxx + 4, y0 + 18)
    call((x0 + 29, y0 + 154), (x0 + 106, y0 + 205), "CAJA CUADRADA CON ARO DE REPELLO DE 1 GANG", 40, 1.6)
    call((x0 + 25, y0 + 90), (x0 + 106, y0 + 105), "TOMACORRIENTES: C. 13 mm Ø", 40, 1.6)
    call((x0 + 75, y0 + 70), (x0 + 106, y0 + 80), "SALIDA DE TV: C. 25 mm Ø", 40, 1.6)
    call((x0 + 50, y0 + 50), (x0 + 106, y0 + 55), "C. 19 mm Ø", 40, 1.6)
    call((x0 + 79, y0 + 14), (x0 + 106, y0 + 30), "SALIDAS INFERIORES A 0,30 m (DET. 1)", 40, 1.6)


# ================================================================ 7. zanja de acometida subterránea
def det_zanja(x, y):
    cell(x, y, W_, H_, "DET. 7 - ZANJA DE ACOMETIDA SUBTERRÁNEA", "CORTE - S/E")
    k = 160.0                                         # mm por metro (esquemático)
    x0, y0 = x + 15, y + 200
    L((x0 - 8, y0), (x0 + 95, y0), "D-COND")           # terreno
    zw = 70.0
    zb = y0 - 0.65 * k
    psp.add_lwpolyline([(x0, y0), (x0, zb), (x0 + zw, zb), (x0 + zw, y0)],
                       dxfattribs={"layer": "D-LINEAS"})
    # eléctrica a 0,50 m sobre cama de 5 cm; arena 10 cm sobre el tubo
    ye = y0 - 0.50 * k
    hatch([(x0, zb), (x0 + zw, zb), (x0 + zw, zb + 0.05 * k), (x0, zb + 0.05 * k)], "AR-SAND", 0.3)
    C((x0 + 20, ye + 4), 4.5)
    hatch([(x0, zb + 0.05 * k), (x0 + zw, zb + 0.05 * k), (x0 + zw, ye + 0.10 * k + 8),
           (x0, ye + 0.10 * k + 8)], "DOTS", 0.4)
    # telefónica a 0,25 m
    yt = y0 - 0.25 * k
    C((x0 + 50, yt + 3), 3.0)
    L((x0 + 20, ye + 4), (x0 + 50, ye + 4), "D-FINO")
    cl.text(psp, "≥ 15 cm", (x0 + 35, ye + 6), 1.6, "A-TEXTO", "BOTTOM_CENTER")
    for yy, lab, dx in ((ye + 4, "0,50 m MÍN.", 20), (yt + 3, "0,25 m MÍN.", 6)):
        L((x0 + zw + dx, y0), (x0 + zw + dx, yy), "D-FINO")
        L((x0 + zw + dx - 2, yy), (x0 + zw + dx + 2, yy), "D-FINO")
        cl.text(psp, lab, (x0 + zw + dx + 1.5, (y0 + yy) / 2), 1.7, "A-TEXTO", "MIDDLE_CENTER", 90)
    call((x0 + 20, ye + 4), (x + 105, ye - 22), "ACOMETIDA ELÉCTRICA: PVC SCH-40 Ø 2\"", 52, 1.6)
    call((x0 + 50, yt + 3), (x + 105, y0 + 25), "VOZ Y DATOS: 2 C. 1\" PVC", 52, 1.6)
    call((x0 + 10, zb + 2), (x + 105, zb - 12), "CAMA DE LASTRE COMPACTADO 5 cm", 52, 1.6)
    call((x0 + 60, ye + 12), (x + 105, ye + 12), "ARENA LIMPIA 10 cm SOBRE EL TUBO", 52, 1.6)
    cl.mtext(psp, "CANALIZACIONES ELÉCTRICAS A 50 cm MÍNIMO CUBIERTAS CON 10 cm DE ARENA LIMPIA; "
             "TELEFÓNICAS A 25 cm MÍNIMO CON 5 cm DE ARENA; SEPARACIÓN ENTRE DUCTOS 15 cm MÍNIMO "
             "(E04).", (x + 6, y + 50), 1.8, W_ - 12, layer="A-TEXTO", attach=7)


# ================================================================ 8. puesta a tierra
def det_tierra(x, y):
    cell(x, y, W_, H_, "DET. 8 - SISTEMA DE PUESTA A TIERRA", "CORTE ESQUEMÁTICO - S/E")
    x0, y0 = x + 25, y + 215
    L((x0 - 10, y0), (x0 + 125, y0), "D-COND")
    for ex in (x0 + 20, x0 + 95):
        R(ex - 8, y0 - 10, ex + 8, y0, "D-LINEAS")               # registro
        L((ex, y0 - 10), (ex, y0 - 140), "D-COND")               # electrodo
    L((x0 + 20, y0 - 6), (x0 + 95, y0 - 6), "D-FINO")
    L((x0 + 20, y0 - 150), (x0 + 95, y0 - 150), "D-FINO")
    for xx in (x0 + 20, x0 + 95):
        L((xx, y0 - 148), (xx, y0 - 152), "D-FINO")
    cl.text(psp, "3,00 m", (x0 + 57, y0 - 148), 1.8, "A-TEXTO", "BOTTOM_CENTER")
    L((x0 + 110, y0), (x0 + 110, y0 - 140), "D-FINO")
    cl.text(psp, "≥ 3,05 m", (x0 + 112, y0 - 70), 1.8, "A-TEXTO", "MIDDLE_LEFT", 90)
    L((x0 + 20, y0), (x0 + 20, y0 + 20), "D-FINO")
    call((x0 + 20, y0 + 15), (x0 + 40, y0 + 30), "CU 1 #6 AWG THHN EN C. 1/2\" PVC AL TABLERO", 50, 1.6)
    call((x0 + 57, y0 - 6), (x0 + 60, y0 - 30), "INTERCONEXIÓN CABLE #6 AWG DESNUDO", 40, 1.6)
    call((x0 + 95, y0 - 80), (x0 + 60, y0 - 100), "ELECTRODO DE PUESTA A TIERRA VERTICAL", 30, 1.6)
    call((x0 + 103, y0 - 5), (x0 + 118, y0 + 14), "REGISTRO", 20, 1.6)
    cl.mtext(psp, "DOS ELECTRODOS SEPARADOS 3 m ENTRE SÍ, INTERCONECTADOS CON CABLE #6 AWG DESNUDO, "
             "ENTERRADOS A NO MENOS DE 3,05 m EN POSICIÓN VERTICAL; UNO A 50 cm DEL BORDE DEL "
             "PEDESTAL. RESISTENCIA DE LA MALLA ≤ 25 OHM (E04).", (x + 6, y + 50), 1.8, W_ - 12,
             layer="A-TEXTO", attach=7)


det_alturas(COLS[0], ROWS[0])
det_conexion(COLS[1], ROWS[0], "S")
det_conexion(COLS[2], ROWS[0], "TC")
det_octogonal(COLS[3], ROWS[0])
det_ubicacion(COLS[0], ROWS[1])
det_tv(COLS[1], ROWS[1])
det_zanja(COLS[2], ROWS[1])
det_tierra(COLS[3], ROWS[1])

H.titleblock(doc, psp, "E05", "ELECTRICIDAD",
             ["DETALLES ELÉCTRICOS.", "CONEXIONES Y ACCESORIOS.", "ALTURAS DE MONTAJE.",
              "ZANJA DE ACOMETIDA.", "PUESTA A TIERRA.", ""],
             [("0", "06-10-2026", "VERSIÓN DE TRABAJO PARA REVISIÓN"),
              ("1", "07-10-2026", "LISTA DEFINITIVA (22); PARA TRÁMITE")], escalas="S/E")

OUT.mkdir(parents=True, exist_ok=True)
doc.saveas(OUT / f"{NAME}.dxf")
cl.render_pdf(doc, LAYOUT, OUT / f"{NAME}.pdf")
print("DXF:", OUT / f"{NAME}.dxf")
