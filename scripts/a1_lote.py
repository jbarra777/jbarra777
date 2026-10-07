"""Lámina A1 - LOTE DE TERRENO (ubicación, poligonal, retiros y huella, derrotero).

Genera:
  planos/A1_lote/SR-A1_LOTE_rev0.dxf  (editable, AutoCAD 2018)
  planos/A1_lote/SR-A1_LOTE_rev0.pdf  (revisión, A1 a escala)
  planos/A1_lote/SR-A1_LOTE_rev0.png  (vista rápida)

Model Space: metros, marco local con origen en el vértice 1 del catastro,
X hacia el este a lo largo del frente (V1->V3), Y hacia el norte a lo largo
del lindero V5->V1. El UCS "CRTM05" del dibujo devuelve coordenadas CRTM05.
"""
import json
import math
import os
from pathlib import Path

from ezdxf.math import Vec2

import cadlib as cl

REV = "rev2"
OUT = cl.ROOT / "planos" / "A1_lote"
NAME = f"SR-A1_LOTE_{REV}"

lote = json.loads((cl.ROOT / "datos" / "lote_catastro.json").read_text(encoding="utf-8"))
prj = cl.load_project()
G = prj["geometria_m"]

# ---------------------------------------------------------------- geometría
V = {int(k): tuple(v) for k, v in lote["vertices_crtm05"].items()}
O = Vec2(V[1])
d15 = Vec2(V[5]) - O
v_s = d15.normalize()            # hacia el sur (a lo largo del lindero 1-5)
u_e = Vec2(-v_s.y, v_s.x)        # perpendicular
if u_e.x < 0:
    u_e = -u_e


def to_model(p):
    """CRTM05 -> modelo (X este local, Y norte local)."""
    d = Vec2(p) - O
    return Vec2(d.dot(u_e), -d.dot(v_s))


def loc(x, y):
    """Marco de diseño (x este, y hacia el sur desde el frente) -> modelo."""
    return Vec2(x, -y)


VM = {k: to_model(p) for k, p in V.items()}
lot_pts = [VM[k] for k in (1, 2, 3, 4, 5)]


def poly_area(pts):
    a = 0.0
    for i in range(len(pts)):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % len(pts)]
        a += x1 * y2 - x2 * y1
    return abs(a) / 2


A_coord = poly_area([V[k] for k in (1, 2, 3, 4, 5)])
A_cat = lote["area_catastro_m2"]
ex0, ex1 = G["envolvente_x"]
ey0, ey1 = G["envolvente_y"]
P1, P2 = G["patio_P1"], G["patio_P2"]
A_env = (ex1 - ex0) * (ey1 - ey0)
A_p1 = (P1["x"][1] - P1["x"][0]) * (P1["y"][1] - P1["y"][0])
A_p2 = (P2["x"][1] - P2["x"][0]) * (P2["y"][1] - P2["y"][0])
A_huella = A_env - A_p1 - A_p2
cob = A_huella / A_cat * 100
A_libre = A_cat - A_huella

# rotación del norte respecto al eje Y del modelo (positivo = antihorario)
az_15 = cl.azimuth(V[5], V[1])           # dirección del eje +Y del modelo
north_rot = az_15 - 360.0 if az_15 > 180 else az_15   # ~ -2.71°

# chequeo: la envolvente cabe dentro del lote (lado este)
x3, y3 = VM[3]
x4, y4 = VM[4]


def x_east(Y):
    return x3 + (x4 - x3) * (Y - y3) / (y4 - y3)


assert min(x_east(-ey0), x_east(-ey1)) >= ex1 - 1e-6, "la envolvente invade el lindero este"

# ---------------------------------------------------------------- documento
doc = cl.new_doc()
cl.north_block(doc)
cl.vertex_block(doc)
msp = doc.modelspace()

# UCS CRTM05 (origen en el (0,0) CRTM05 expresado en el modelo)
ux = to_model(O + Vec2(1, 0)) - to_model(O)
uy = to_model(O + Vec2(0, 1)) - to_model(O)
org = to_model((0.0, 0.0))
doc.ucs.new("CRTM05", dxfattribs={"origin": (org.x, org.y, 0),
                                  "xaxis": (ux.x, ux.y, 0),
                                  "yaxis": (uy.x, uy.y, 0)})

# Lindero y vértices
msp.add_lwpolyline(lot_pts, close=True, dxfattribs={"layer": "T-LINDERO"})
centro = Vec2(sum(p.x for p in lot_pts) / 5, sum(p.y for p in lot_pts) / 5)
for k, p in VM.items():
    msp.add_blockref("VERTICE", p, dxfattribs={"layer": "T-VERTICE"})
    dirv = (p - centro).normalize()
    off = Vec2(1 if dirv.x > 0 else -1, 1 if dirv.y > 0 else -1)
    if k == 2:
        off = Vec2(0.9, -1.0)
    cl.text(msp, str(k), p + off * 0.75, 0.40, "T-TXT-200", "MIDDLE_CENTER")
    cl.text(msp, str(k), p + off * 0.50, 0.25, "T-TXT-100", "MIDDLE_CENTER")

# ---- Vista POLIGONAL (1:200): cotas de lados, colindantes
for a, b, dist in ((1, 2, 1.6), (2, 3, 1.6), (4, 3, -1.6), (5, 4, -1.6), (5, 1, 1.6)):
    d = msp.add_aligned_dim(p1=VM[a], p2=VM[b], distance=dist, dimstyle="COTA-200",
                            dxfattribs={"layer": "T-COTA-200"})
    d.render()

cl.text(msp, "CALLE PÚBLICA", loc(4.5, -4.2), 0.70, "T-TXT-200", "MIDDLE_CENTER")
col = "COLINDA: ID. PREDIAL " + lote["identificador_predial"]
cl.text(msp, col, loc(-3.4, 14.26), 0.45, "T-TXT-200", "MIDDLE_CENTER", rot=90)
cl.text(msp, col, loc(12.4, 14.26), 0.45, "T-TXT-200", "MIDDLE_CENTER", rot=90)
cl.text(msp, col, loc(4.5, 31.2), 0.45, "T-TXT-200", "MIDDLE_CENTER")
cl.mtext(msp, "LOTE\\PÁREA SEGÚN CATASTRO: 256 m²\\PÁREA POR COORDENADAS: "
         f"{A_coord:.2f} m²".replace(".", ","), loc(4.5, 14.26), 0.45, 8.5,
         layer="T-TXT-200", attach=5)

# ---- Vista RETIROS Y HUELLA (1:100)
env = [loc(ex0, ey0), loc(ex1, ey0), loc(ex1, ey1), loc(ex0, ey1)]
msp.add_lwpolyline(env, close=True, dxfattribs={"layer": "A-HUELLA"})


def prect(P):
    return [loc(P["x"][0], P["y"][0]), loc(P["x"][1], P["y"][0]),
            loc(P["x"][1], P["y"][1]), loc(P["x"][0], P["y"][1])]


for P in (P1, P2):
    msp.add_lwpolyline(prect(P), close=True, dxfattribs={"layer": "A-PATIO"})
    # diagonales de vacío (abierto a cielo)
    r = prect(P)
    msp.add_line(r[0], r[2], dxfattribs={"layer": "A-PATIO", "linetype": "DASHED2",
                                         "ltscale": 0.25})
    msp.add_line(r[1], r[3], dxfattribs={"layer": "A-PATIO", "linetype": "DASHED2",
                                         "ltscale": 0.25})

h = msp.add_hatch(dxfattribs={"layer": "A-HUELLA-TRAMA"})
h.paths.add_polyline_path(env, is_closed=True, flags=1)
h.paths.add_polyline_path(prect(P1), is_closed=True, flags=16)
h.paths.add_polyline_path(prect(P2), is_closed=True, flags=16)
h.set_pattern_fill("ANSI31", scale=0.06)

# cotas lado oeste (desde la línea de propiedad en x=0)
yr_w = -VM[5].y
yr_e = -VM[4].y
dims = []
for ya, yb in ((0.0, ey0), (ey0, ey1), (ey1, yr_w)):
    dims.append(msp.add_linear_dim(base=loc(-1.2, 0), p1=loc(0, ya), p2=loc(0, yb),
                                   angle=90, dimstyle="COTA-100",
                                   dxfattribs={"layer": "T-COTA-100"}))
# cadena lado este
cad = G["cadena_y"]
chain = [-VM[3].y, cad["f0"], cad["p1a"], cad["p1b"], cad["sba"], cad["sbb"], cad["r0"], yr_e]
for ya, yb in zip(chain[:-1], chain[1:]):
    dims.append(msp.add_linear_dim(base=loc(10.4, 0), p1=loc(9.0, ya), p2=loc(9.0, yb),
                                   angle=90, dimstyle="COTA-100",
                                   dxfattribs={"layer": "T-COTA-100"}))
# anchos
for P, yb in ((P1, P1["y"][0] + 0.55), (P2, P2["y"][0] + 0.55)):
    dims.append(msp.add_linear_dim(base=loc(0, yb), p1=loc(P["x"][0], P["y"][0]),
                                   p2=loc(P["x"][1], P["y"][0]), angle=0,
                                   dimstyle="COTA-100", dxfattribs={"layer": "T-COTA-100"}))
dims.append(msp.add_linear_dim(base=loc(0, ey1 + 0.6), p1=loc(ex0, ey1), p2=loc(ex1, ey1),
                               angle=0, dimstyle="COTA-100",
                               dxfattribs={"layer": "T-COTA-100"}))
for d in dims:
    d.render()


def lbl(s, x, y, hgt=0.30, w=6.5, attach=5, layer="T-TXT-100"):
    return cl.mtext(msp, s, loc(x, y), hgt, w, layer=layer, attach=attach)


lbl("CALLE PÚBLICA", 4.5, -2.2, 0.40)
lbl("LÍNEA DE PROPIEDAD", 2.2, -0.45, 0.22)
lbl("RETIRO FRONTAL\\P(ACCESO VEHICULAR Y PEATONAL)", 4.5, 1.15, 0.22, 7.5)
lbl("HUELLA CONSTRUCTIVA\\PNIVEL 1", 4.5, 4.6, 0.32)
lbl(f"PATIO DE LUZ P1 (ABIERTO)\\P"
    f"{P1['x'][1]-P1['x'][0]:.2f} x {P1['y'][1]-P1['y'][0]:.2f} = {A_p1:.2f} m²",
    (P1["x"][0] + P1["x"][1]) / 2, (P1["y"][0] + P1["y"][1]) / 2 + 0.25, 0.24, 5.5)
lbl("HUELLA CONSTRUCTIVA\\PNIVEL 1", 4.5, 13.6, 0.32)
lbl(f"PATIO P2 (ABIERTO)\\P"
    f"{P2['x'][1]-P2['x'][0]:.2f} x {P2['y'][1]-P2['y'][0]:.2f} = {A_p2:.2f} m²",
    (P2["x"][0] + P2["x"][1]) / 2, (P2["y"][0] + P2["y"][1]) / 2 + 0.25, 0.21, 3.9)
lbl("HUELLA CONSTRUCTIVA\\PNIVEL 1", 4.5, 22.3, 0.32)
lbl(f"HUELLA: {A_huella:.2f} m²\\PCOBERTURA: {cob:.2f} %".replace(".", ","),
    4.5, 9.0 + 4.1 + 2.2, 0.26, 6.0)
lbl("PATIO POSTERIOR\\PTANQUE SÉPTICO Y DRENAJE\\P(VER S02)",
    4.5, (ey1 + yr_w) / 2 + 0.25, 0.22, 8.0)
lbl("COLINDANCIA - FACHADA CIEGA", -0.1, 14.0, 0.22, 12, attach=8)
cl.text(msp, "COLINDANCIA - FACHADA CIEGA", loc(-0.35, 14.0), 0.22, "T-TXT-100",
        "MIDDLE_CENTER", rot=90)
cl.text(msp, "COLINDANCIA - FACHADA CIEGA", loc(9.35, 14.0), 0.22, "T-TXT-100",
        "MIDDLE_CENTER", rot=90)
# Se borró el mtext duplicado de colindancia (usar textos girados)
for e in list(msp.query("MTEXT")):
    if e.text.startswith("COLINDANCIA"):
        msp.delete_entity(e)

# ---------------------------------------------------------------- hoja A1
psp = doc.layouts.new("A1-LOTE")
psp.page_setup(size=(cl.A1_W, cl.A1_H), margins=(0, 0, 0, 0), units="mm")
doc.layouts.set_active_layout("A1-LOTE")
cl.frame(psp)

FROZEN_POLIG = ["T-TXT-100", "T-COTA-100", "A-HUELLA", "A-HUELLA-TRAMA", "A-PATIO",
                "A-RETIRO"]
FROZEN_RETIRO = ["T-TXT-200", "T-COTA-200"]


def viewport(cx, cy, w, hgt, scale, mcx, mcy, frozen):
    vp = psp.add_viewport(center=(cx, cy), size=(w, hgt),
                          view_center_point=(mcx, mcy),
                          view_height=hgt * scale / 1000.0,
                          dxfattribs={"layer": "A-VIEWPORT"})
    vp.frozen_layers = frozen
    vp.dxf.flags = vp.dxf.flags | 16384  # bloquear zoom (display locked)
    return vp


# Columna 1: ubicación geográfica (imagen del catastro) + poligonal 1:200
img_file = "A1_ubicacion_catastro.png"
from PIL import Image  # noqa: E402

iw, ih = Image.open(OUT / img_file).size
idef = doc.add_image_def(filename=img_file, size_in_pixel=(iw, ih))
img_w = 185.0
img_h = img_w * ih / iw
psp.add_image(idef, insert=(42.0, 402.0), size_in_units=(img_w, img_h),
              dxfattribs={"layer": "A-IMAGEN-REF"})
cl.view_title(psp, 42.0, 389.0, "UBICACIÓN GEOGRÁFICA", "LOTE DE TERRENO",
              "Esc. S/E  (imagen tomada del plano catastrado 4-57389-2023)", 125)

viewport(140.0, 232.0, 200.0, 240.0, 200, 4.5, -14.0, FROZEN_POLIG)
cl.view_title(psp, 42.0, 90.0, "POLIGONAL TERRENO", "LOTE DE TERRENO", "Esc. 1:200", 125)
cl.scale_bar(psp, 42.0, 58.0, 200, 10, 2)
psp.add_blockref("NORTE", (215.0, 330.0), dxfattribs={"layer": "A-NORTE",
                                                       "rotation": north_rot})

# Columna 2: retiros y huella 1:100
viewport(364.0, 345.0, 210.0, 400.0, 100, 4.5, -13.9, FROZEN_RETIRO)
cl.view_title(psp, 262.0, 128.0, "RETIROS Y HUELLA", "LOTE DE TERRENO - NIVEL 1",
              "Esc. 1:100", 125)
cl.scale_bar(psp, 262.0, 96.0, 100, 5, 1)
psp.add_blockref("NORTE", (450.0, 520.0), dxfattribs={"layer": "A-NORTE",
                                                       "rotation": north_rot})
cl.text(psp, "NORTE SEGÚN PLANO CATASTRADO (CRTM05)", (450.0, 500.0), 1.8, "A-TEXTO",
        "TOP_CENTER")

# Columna 3: cuadros y notas
X3 = 482.0
WC = 222.0
y = 576.0
cl.text(psp, "D E R R O T E R O", (X3 + WC / 2, y), 6.0, "A-TITULOS", "TOP_CENTER")
y -= 10
rows = cl.derrotero_rows(V)
y = cl.table(psp, X3, y, [44.4] * 5, rows, row_h=7.0, h=2.8)
cl.mtext(psp, "Acimutes y distancias calculados con las coordenadas CRTM05 del plano "
         "catastrado 4-57389-2023 (redondeo al minuto y al centímetro). Amarre al punto "
         "de intersección (P.I.) según el mismo plano.", (X3, y - 2.0), 2.0, WC, attach=1)
y -= 14
cl.text(psp, "CUADRO DE COORDENADAS CRTM05", (X3 + WC / 2, y), 3.5, "A-TITULOS",
        "TOP_CENTER")
y -= 7
rows = [["VÉRTICE", "ESTE (m)", "NORTE (m)"]]
for k in (1, 2, 3, 4, 5):
    e, n = V[k]
    rows.append([str(k), f"{e:,.2f}", f"{n:,.2f}"])
y = cl.table(psp, X3, y, [50, 86, 86], rows, row_h=6.0, h=2.6)
y -= 8
cl.text(psp, "CUADRO DE ÁREAS Y COBERTURA", (X3 + WC / 2, y), 3.5, "A-TITULOS",
        "TOP_CENTER")
y -= 7


def m2(v):
    return f"{v:,.2f} m²".replace(",", " ").replace(".", ",")


rows = [["CONCEPTO", "VALOR"],
        ["ÁREA DEL LOTE SEGÚN CATASTRO", m2(A_cat)],
        ["ÁREA DEL LOTE SEGÚN COORDENADAS", m2(A_coord)],
        [f"ENVOLVENTE DE CONSTRUCCIÓN ({ex1-ex0:.2f} x {ey1-ey0:.2f})".replace(".", ","),
         m2(A_env)],
        ["PATIOS ABIERTOS P1 + P2", m2(A_p1 + A_p2)],
        ["HUELLA CONSTRUCTIVA NIVEL 1", m2(A_huella)],
        ["ÁREA LIBRE DEL LOTE (CATASTRO - HUELLA)", m2(A_libre)],
        ["COBERTURA", f"{cob:.2f} %".replace(".", ",")]]
y = cl.table(psp, X3, y, [150, 72], rows, row_h=6.0, h=2.6,
             aligns=["MIDDLE_LEFT", "MIDDLE_RIGHT"])
cl.text(psp, f"CÁLCULO: HUELLA / ÁREA SEGÚN CATASTRO x 100 = ({A_huella:.2f} / {A_cat:.2f}) "
        f"x 100 = {cob:.2f} %".replace(".", ","), (X3, y - 2.0), 2.0, "A-TEXTO", "TOP_LEFT")
y -= 10
cl.text(psp, "NOTAS:", (X3, y), 3.5, "A-TITULOS", "TOP_LEFT")
y -= 6
notas = cl.notas()
m = cl.mtext(psp, "\\P".join(notas), (X3, y), 2.3, WC, attach=1, spacing=1.0)
y -= 80
# Simbología
cl.text(psp, "SIMBOLOGÍA:", (X3, y), 3.5, "A-TITULOS", "TOP_LEFT")
y -= 9
sx = X3 + 2
items = [("lindero", "LÍNEA DE PROPIEDAD (LINDERO)"),
         ("vertice", "VÉRTICE DEL PLANO CATASTRADO"),
         ("huella", "HUELLA CONSTRUCTIVA (NIVEL 1)"),
         ("patio", "PATIO ABIERTO A CIELO"),
         ("cota", "COTA (m)")]
for kind, s in items:
    yc = y - 2.0
    if kind == "lindero":
        ln = psp.add_line((sx, yc), (sx + 16, yc), dxfattribs={"layer": "T-LINDERO"})
    elif kind == "vertice":
        psp.add_circle((sx + 8, yc), 1.8, dxfattribs={"layer": "T-VERTICE"})
        cl.text(psp, "1", (sx + 11.5, yc + 1.5), 2.0, "A-TEXTO", "MIDDLE_LEFT")
    elif kind == "huella":
        cl.rect(psp, sx, yc - 2.2, sx + 16, yc + 2.2, "A-HUELLA")
        hh = psp.add_hatch(dxfattribs={"layer": "A-HUELLA-TRAMA"})
        hh.paths.add_polyline_path([(sx, yc - 2.2), (sx + 16, yc - 2.2), (sx + 16, yc + 2.2),
                                    (sx, yc + 2.2)])
        hh.set_pattern_fill("ANSI31", scale=0.6)
    elif kind == "patio":
        cl.rect(psp, sx, yc - 2.2, sx + 16, yc + 2.2, "A-PATIO")
        psp.add_line((sx, yc - 2.2), (sx + 16, yc + 2.2),
                     dxfattribs={"layer": "A-PATIO", "linetype": "DASHED2"})
        psp.add_line((sx, yc + 2.2), (sx + 16, yc - 2.2),
                     dxfattribs={"layer": "A-PATIO", "linetype": "DASHED2"})
    elif kind == "cota":
        psp.add_line((sx, yc), (sx + 16, yc), dxfattribs={"layer": "A-TEXTO"})
        for xx in (sx, sx + 16):
            psp.add_line((xx - 1, yc - 1), (xx + 1, yc + 1), dxfattribs={"layer": "A-TEXTO"})
        cl.text(psp, "5.70", (sx + 8, yc + 0.8), 2.0, "A-TEXTO", "BOTTOM_CENTER")
    cl.text(psp, s, (sx + 22, yc), 2.4, "A-TEXTO", "MIDDLE_LEFT")
    y -= 8

# Cajetín
vals = {
    "EMPRESA": prj["empresa"],
    "EMPRESA_CED": prj["empresa_ced"],
    "PROF_1": prj["profesionales"][0],
    "PROF_2": prj["profesionales"][1],
    "PROF_3": prj["profesionales"][2],
    "PROYECTO": prj["proyecto"],
    "UBIC_1": prj["ubicacion"][0],
    "UBIC_2": prj["ubicacion"][1],
    "UBIC_3": "",
    "REG_1": prj["registro"][0],
    "REG_2": prj["registro"][1],
    "REG_3": prj["registro"][2],
    "CONT_TIT": "LOTE DE TERRENO",
    "CONT_1": "UBICACIÓN GEOGRÁFICA.",
    "CONT_2": "POLIGONAL.",
    "CONT_3": "RETIROS Y HUELLA.",
    "CONT_4": "DERROTERO Y CUADRO DE COORDENADAS.",
    "CONT_5": "CUADRO DE ÁREAS Y COBERTURA.",
    "CONT_6": "NOTAS.",
    "ESCALAS": "INDICADAS",
    "REV0_N": "0", "REV0_F": "06-10-2026", "REV0_D": "VERSIÓN DE TRABAJO PARA REVISIÓN",
    "REV1_N": "1", "REV1_F": "06-10-2026", "REV1_D": "NOTA 2 TAPIA; PATIOS ACEPTADOS (NOTA 12)",
    "REV2_N": "2", "REV2_F": "07-10-2026", "REV2_D": "REFERENCIA AL TANQUE SÉPTICO (S02)",
    "ESTADO_1": "VERSIÓN DE TRABAJO",
    "ESTADO_2": "NO APTA PARA CONSTRUCCIÓN NI TRÁMITE",
    "LUGAR": "COSTA RICA",
    "LAMINA": "A1",
    "FECHA": prj["fecha"],
    "TOTAL": prj["total_laminas"],
}
cl.insert_titleblock(doc, psp, vals)

# ---------------------------------------------------------------- salida
OUT.mkdir(parents=True, exist_ok=True)
dxf_path = OUT / f"{NAME}.dxf"
doc.saveas(dxf_path)
cwd = os.getcwd()
os.chdir(OUT)  # la imagen se referencia por ruta relativa
try:
    cl.render_pdf(doc, "A1-LOTE", OUT / f"{NAME}.pdf", OUT / f"{NAME}.png", dpi=110)
finally:
    os.chdir(cwd)

print(f"Área coordenadas: {A_coord:.2f} m2 | envolvente {A_env:.2f} | patios {A_p1+A_p2:.2f}"
      f" | huella {A_huella:.2f} | cobertura {cob:.2f} % | libre {A_libre:.2f}")
print(f"Rotación norte: {north_rot:.3f}° | retiro post. O {yr_w-ey1:.3f} E {yr_e-ey1:.3f}"
      f" | retiro frontal V3 {ey0 - (-VM[3].y):.3f}")
print("DXF:", dxf_path)
