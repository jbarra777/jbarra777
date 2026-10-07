"""Lámina C01 - PLANTA DE CIMENTACIONES y detalle de viga riostra.

Secciones tomadas de la referencia (RIVERGRAND C01/C02/C03) por indicación expresa del usuario
(ingeniero responsable): se marcan. Ubicación propia de esta vivienda: columnas C1 en
los ejes A y D (ejes 1 a 6) y en el eje C (ejes 2 a 6; sin C1 en el eje 1); placas F1
centradas (eje C) y F2 excéntricas (linderos A y D); vigas riostra VA1 en ejes longitudinales
y transversales. Columnas del eje C: tubo forrado a 0.30 x 0.30 (plantas aprobadas).
Marco de planta de planta.py (X = y, Y = x).
"""
import cadlib as cl
import hoja as H
import planta as pl
from planta import P

REV = "rev2"
OUT = cl.ROOT / "planos" / "C01_cimentaciones"
NAME = f"SR-C01_CIMENTACIONES_{REV}"

W = H.W
FB = 1.65                      # placa 1,65 x 1,65
TUBO, PED = 0.15, 0.30         # tubo 6x6" y pedestal 0,30
VA = 0.20                      # viga riostra 0,20 x 0,40
Y_LP = H.Y_LP
YA = H.EJES_Y                  # ejes 1..6
XA, XC, XD = H.EJES_X["A"], H.EJES_X["C"], H.EJES_X["D"]

doc = cl.new_doc()
cl.north_block(doc)
msp = doc.modelspace()
north_ang = pl.add_crtm_ucs(doc, H.FRAME)
for name, col, lw, lt in (("E-CIMIENTO", 7, 35, "Continuous"), ("E-RIOSTRA", 7, 25, "Continuous"),
                          ("E-PEDESTAL", 7, 25, "Continuous"), ("E-TXT", 7, 18, "Continuous"),
                          ("E-DET", 7, 35, "Continuous"), ("E-DET-TRAMA", 8, 9, "Continuous")):
    doc.layers.add(name, color=col, linetype=lt, lineweight=lw)
H.lot(msp)
if "COTA-10" not in doc.dimstyles:
    cl._dimstyle(doc, "COTA-10", 10)


def rect(x0, y0, x1, y1, layer):
    return pl.poly(msp, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], layer)


# ---------------------------------------------------------------- columnas y placas
COLS = []                                           # (x, y, tipo de placa, x0 placa, x1 placa)
for k, y in YA.items():
    COLS.append((XA, y, "F2", 0.0, FB))
    COLS.append((XD, y, "F2", W - FB, W))
for k, y in H.COLS.items():
    COLS.append((XC, y, "F1", XC - FB / 2, XC + FB / 2))
for x, y, f, x0, x1 in COLS:
    rect(x0, y - FB / 2, x1, y + FB / 2, "E-CIMIENTO")                      # placa
    xp0 = min(max(x - PED / 2, 0.0), W - PED)
    rect(xp0, y - PED / 2, xp0 + PED, y + PED / 2, "E-PEDESTAL")             # pedestal
    pts = [P(x - TUBO / 2, y - TUBO / 2), P(x + TUBO / 2, y - TUBO / 2),
           P(x + TUBO / 2, y + TUBO / 2), P(x - TUBO / 2, y + TUBO / 2)]
    msp.add_lwpolyline(pts, close=True, dxfattribs={"layer": "E-COLUMNA"})
    ht = msp.add_hatch(color=7, dxfattribs={"layer": "E-COLUMNA"})
    ht.paths.add_polyline_path(pts)
    tx = (x1 - 0.30) if (f == "F2" and x0 == 0.0) else (x0 + 0.30)
    pl.text(msp, f, tx, y + FB / 2 - 0.22, 0.16, "E-TXT")
    pl.text(msp, "C1", x + 0.28 if x < W / 2 else x - 0.28, y - 0.30, 0.12, "E-TXT")
# ---------------------------------------------------------------- vigas riostra VA1
ys = list(YA.values())
for x0, x1, ya, yb in ((0.0, VA, ys[0], ys[-1]), (W - VA, W, ys[0], ys[-1]),
                       (XC - VA / 2, XC + VA / 2, H.COLS["2"], H.COLS["6"])):
    rect(x0, ya, x1, yb, "E-RIOSTRA")
for k, y in YA.items():
    rect(0.0, y - VA / 2, W, y + VA / 2, "E-RIOSTRA")
rect(0.0, Y_LP - VA, W, Y_LP, "E-RIOSTRA")                                    # tapia posterior
for y in (5.0, 13.6, 22.3):
    pl.text(msp, "VA1", 0.42, y, 0.13, "E-TXT", rot=0)
    pl.text(msp, "VA1", W - 0.42, y, 0.13, "E-TXT", rot=0)
pl.text(msp, "VA1", XC + 0.35, 13.6, 0.13, "E-TXT")
pl.text(msp, "VA1 (CIMIENTO DE TAPIA POSTERIOR)", 4.5, Y_LP - 0.40, 0.12, "E-TXT", rot=90)
pl.text(msp, "SIN COLUMNA EN EL EJE C (PORTÓN)", XC, YA["1"] + 0.55, 0.11, "E-TXT")

# ---------------------------------------------------------------- ejes, cotas y rótulos
H.axes(msp)
H.general_dims(msp)
pl.dim(msp, (0.0, YA["2"] - FB / 2), (FB, YA["2"] - FB / 2), (0, YA["2"] - FB / 2 - 0.35), True)
pl.dim(msp, (XC - FB / 2, YA["4"] - FB / 2), (XC + FB / 2, YA["4"] - FB / 2),
       (0, YA["4"] - FB / 2 - 0.35), True)
pl.dim(msp, (XC - FB / 2, YA["4"] - FB / 2), (XC - FB / 2, YA["4"] + FB / 2), (XC - FB / 2 - 0.35, 0), False)
pl.dim(msp, (W - FB, YA["5"] - FB / 2), (W, YA["5"] - FB / 2), (0, YA["5"] - FB / 2 - 0.35), True)
pl.text(msp, "CALLE PÚBLICA", 4.5, -2.15, 0.22, "A-ESPACIOS", rot=90)
pl.mtext(msp, "COLINDANCIA", -0.35, 14.0, 0.10, 6.0, "A-TXT-50")
pl.mtext(msp, "COLINDANCIA", W + 0.35, 14.0, 0.10, 6.0, "A-TXT-50")

# ---------------------------------------------------------------- detalle de viga riostra (1:10)
DX, DY = 60.0, 0.0
b, h, rc = 0.20, 0.40, 0.04
pts = [(DX, DY), (DX + b, DY), (DX + b, DY + h), (DX, DY + h)]
msp.add_lwpolyline(pts, close=True, dxfattribs={"layer": "E-DET"})
ht = msp.add_hatch(dxfattribs={"layer": "E-DET-TRAMA"})
ht.paths.add_polyline_path(pts)
ht.set_pattern_fill("AR-CONC", scale=0.004)
msp.add_lwpolyline([(DX + rc, DY + rc), (DX + b - rc, DY + rc), (DX + b - rc, DY + h - rc),
                    (DX + rc, DY + h - rc)], close=True, dxfattribs={"layer": "E-DET"})
for yy in (DY + rc + 0.016, DY + h / 2, DY + h - rc - 0.016):
    for xx in (DX + rc + 0.016, DX + b - rc - 0.016):
        c = msp.add_circle((xx, yy), 0.0064, dxfattribs={"layer": "E-DET"})
        hh = msp.add_hatch(color=7, dxfattribs={"layer": "E-DET"})
        hh.paths.add_edge_path().add_arc((xx, yy), 0.0064, 0, 360)
for a, bb, base, hor in (((DX, DY + h), (DX + b, DY + h), DY + h + 0.06, True),
                          ((DX + b, DY), (DX + b, DY + h), DX + b + 0.06, False)):
    if hor:
        d = msp.add_linear_dim(base=(0, base), p1=a, p2=bb, angle=0, dimstyle="COTA-10" if "COTA-10" in doc.dimstyles else "COTA-50",
                               dxfattribs={"layer": "E-TXT"})
    else:
        d = msp.add_linear_dim(base=(base, 0), p1=a, p2=bb, angle=90, dimstyle="COTA-10" if "COTA-10" in doc.dimstyles else "COTA-50",
                               dxfattribs={"layer": "E-TXT"})
    d.render()

# ================================================================ hoja
psp = H.sheet(doc, "C01-CIMENTACIONES", "PLANTA DE CIMENTACIONES", "")
H.north(psp, north_ang)
cl.view_title(psp, 35.0, 262.0, "PLANTA DE CIMENTACIONES", "PLACAS, PEDESTALES Y VIGAS RIOSTRA",
              "Esc. 1:50", 150)
cl.scale_bar(psp, 35.0, 236.0, 50, 5, 1)
v = psp.add_viewport(center=(80.0, 150.0), size=(70.0, 75.0), view_center_point=(DX + 0.12, DY + 0.22),
                     view_height=75.0 * 10 / 1000.0, dxfattribs={"layer": "A-VIEWPORT"})
v.dxf.flags = v.dxf.flags | 16384
cl.text(psp, "DETALLE DE VIGA RIOSTRA VA1", (35.0, 105.0), 4.0, "A-TITULOS", "TOP_LEFT")
cl.text(psp, "Esc. 1:10", (35.0, 99.0), 2.5, "A-TEXTO", "TOP_LEFT")
cl.mtext(psp, "VIGA VA1: 0,20 x 0,40\\P6 VARILLAS #4\\PAROS VARILLA #3 @20cm\\PRECUBRIMIENTO 4cm",
         (120.0, 175.0), 2.2, 60.0, layer="A-TEXTO", attach=1)

X2 = 240.0
y = 262.0
cl.text(psp, "CUADRO DE CIMENTACIONES", (X2 + 100, y), 4.0, "A-TITULOS", "TOP_CENTER")
nF1 = sum(1 for c in COLS if c[2] == "F1")
nF2 = sum(1 for c in COLS if c[2] == "F2")
rows = [["TIPO", "PLACA (m)", "ESPESOR", "REFUERZO", "PEDESTAL", "CANT."],
        ["F1", "1,65 x 1,65 CENTRADA", "0,25", "MALLA #4 @20cm", "0,30x0,30x0,80", str(nF1)],
        ["F2", "1,65 x 1,65 EXCÉNTRICA", "0,25", "MALLA #4 @20cm", "0,30x0,30x0,80", str(nF2)]]
y = cl.table(psp, X2, y - 8, [14, 52, 20, 40, 42, 16], rows, row_h=6.0, h=2.2)
cl.text(psp, "PEDESTAL: 4 VARILLAS #4, ESTRIBOS #3 @10cm; PLETINA DE UNIÓN 270 x 270 mm. "
        "DETALLES EN LÁMINA C02.", (X2, y - 2.0), 2.0, "A-TEXTO", "TOP_LEFT")
y -= 12
cl.text(psp, "SIMBOLOGÍA ELEMENTOS PORTANTES", (X2 + 100, y), 4.0, "A-TITULOS", "TOP_CENTER")
rows = [["C1", "COLUMNA - TUBO DE ACERO 6x6\" EN 3,17mm (EJE C FORRADA A 0,30 x 0,30)"],
        ["VA1", "VIGA RIOSTRA DE CONCRETO 0,20 x 0,40, 6 #4, AROS #3 @20cm"],
        ["F1 / F2", "PLACA AISLADA CENTRADA / EXCÉNTRICA (VER C02)"]]
y = cl.table(psp, X2, y - 8, [24, 160], rows, row_h=6.5, h=2.2, aligns=["MIDDLE_CENTER", "MIDDLE_LEFT"])

X3 = 455.0
y = 262.0
cl.text(psp, "NOTAS:", (X3, y), 3.5, "A-TITULOS", "TOP_LEFT")
notas = [
    "TODAS LAS MEDIDAS ESTÁN DADAS EN METROS, SALVO INDICACIÓN CONTRARIA.",
    "CAPACIDAD SOPORTANTE ADMISIBLE DEL SUELO CONSIDERADA: qadm = 12 t/m².",
    "LAS PLACAS DEBEN APOYARSE SOBRE SUELO NATURAL PREPARADO ADECUADAMENTE. NIVEL DE DESPLANTE "
    "SEGÚN DETALLE C02 (PEDESTAL 0,80 m + PLACA 0,25 m).",
    "COLUMNAS C1 EN LOS EJES A Y D (EJES 1 A 6) Y EN EL EJE C (EJES 2 A 6). SIN COLUMNA EN EL EJE C "
    "DEL EJE 1 PARA NO OBSTRUIR EL PORTÓN (LA C1 DE LOS NIVELES 2 Y 3 EN ESE PUNTO APOYA EN LA VIGA "
    "DE TRANSFERENCIA VT-1, VER C05). LAS PLACAS DE LINDERO (F2) SON EXCÉNTRICAS Y NO "
    "INVADEN EL PREDIO VECINO.",
    "VIGAS RIOSTRA VA1 EN LOS EJES A, C Y D Y EN LOS EJES 1 A 6. LOS MUROS DE LINDERO Y EL FRENTE "
    "DEL NIVEL 1 (MAMPOSTERÍA) APOYAN SOBRE LAS VA1. CIMIENTO DE LA TAPIA POSTERIOR: VA1.",
    "CONTRAPISO DE 0,10 m EN ESTACIONAMIENTOS, PASILLO, VESTÍBULO Y GRADAS (VER A2 Y A6).",
    "MATERIALES, RECUBRIMIENTOS Y ESPECIFICACIONES SEGÚN LÁMINA C06.",
]
cl.notes_block(psp, X3, y - 6, [f"{i}.- {t}" for i, t in enumerate(notas, 1)] + [cl.NOTA_PR], 2.1, 250)

H.titleblock(doc, psp, "C01", "FUNDACIONES",
             ["PLANTA DE CIMENTACIONES.", "DETALLE DE VIGA RIOSTRA.", "CUADRO DE CIMENTACIONES.",
              "SIMBOLOGÍA.", "NOTAS.", ""],
             [("0", "06-10-2026", "VERSIÓN DE TRABAJO PARA REVISIÓN"),
              ("1", "06-10-2026", "REFERENCIA A C06; NOTA C1 EJE C-1 SOBRE VT-1"),
              ("2", "07-10-2026", "LISTA DEFINITIVA (22); PARA TRÁMITE")], escalas="1:50 / INDICADAS")

OUT.mkdir(parents=True, exist_ok=True)
doc.saveas(OUT / f"{NAME}.dxf")
cl.render_pdf(doc, "C01-CIMENTACIONES", OUT / f"{NAME}.pdf")
print("F1", nF1, "F2", nF2)
print("DXF:", OUT / f"{NAME}.dxf")
