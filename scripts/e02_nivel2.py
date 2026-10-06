"""Lámina E02 - PLANTA ELÉCTRICA NIVEL 2: iluminación, tomacorrientes y voz/datos.

Base: planta A3 rev4 aprobada (con mobiliario en gris). Simbología común (elec.py) y notas de
la referencia [PR]. Subtablero TN2 en el pasillo junto a la escalera (sobre el TP del N1).
Cargas especiales del usuario: cocina eléctrica y calentador de paso del baño (240 V).
"""
import ezdxf

import cadlib as cl
import elec as EL
import hoja as H
import planta as pl

REV = "rev0"
OUT = cl.ROOT / "planos" / "E02_nivel2"
NAME = f"SR-E02_NIVEL2_{REV}"
LAYOUT = "E02-NIVEL2"
SRC = cl.ROOT / "planos/A3_nivel2/SR-A3_NIVEL2_rev4.dxf"
KEEP = {"A-MURO", "A-MURO-TRAMA", "A-PUERTA", "A-VENTANA", "A-ESCALERA", "A-ESPACIOS",
        "E-COLUMNA", "A-EJES", "A-EJES-TXT", "T-LINDERO", "T-VERTICE", "A-PROYECCION",
        "A-MOBILIARIO", "A-TXT-50"}

doc = cl.new_doc()
cl.north_block(doc)
msp = doc.modelspace()
north_ang = pl.add_crtm_ucs(doc, H.FRAME)
EL.layers(doc)
for e in ezdxf.readfile(SRC).modelspace():
    if e.dxf.layer in KEEP:
        msp.add_entity(e.copy())
for name in KEEP:
    if name in doc.layers and name not in ("A-ESPACIOS", "A-EJES-TXT"):
        doc.layers.get(name).color = 8
H.general_dims(msp)
E = EL.Plan(msp)
TB = (0.24, 18.20)                                   # TN2

# ---------------------------------------------------------------- tablero
E.s("TAB", *TB)
E.note(1.10, 18.20, "TN2", 0.14)

# ---------------------------------------------------------------- iluminación (TN2-1)
# a: suite (dormitorio y estar)
sa = [(1.90, 3.50), (2.50, 6.40), (5.20, 6.60)]
for p in sa:
    E.s("LUZE", *p, "a")
E.s("S", 1.40, 7.45, "a")
E.run([(1.40, 7.45), sa[1], sa[0]])
E.run([sa[1], sa[2]])
# b: baño suite
E.s("LUZE", 4.50, 3.30, "b")
E.s("S", 4.90, 4.58, "b")
E.run([(4.90, 4.58), (4.50, 3.30)], bulge=-0.3)
# c: walk-in
E.s("LUZE", 7.90, 4.85, "c")
E.s("S", 5.80, 5.62, "c")
E.run([(5.80, 5.62), (7.90, 4.85)])
# d: galería y pasillo (tres vías: suite y sala)
sd = [(0.40, 9.00), (0.40, 12.00), (0.40, 15.20)]
for p in sd:
    E.s("LUZE", *p, "d")
E.s("S3", 0.32, 8.00, "d")
E.s("S3", 0.32, 19.25, "d")
E.run([(0.32, 8.00), sd[0], sd[1], sd[2], (0.32, 19.25)], bulge=0.15)
# e: tres vías de la luz de gradas del N1 (ver E01); i: gradas N2-N3 (tres vías con N3)
E.s("S3", 0.32, 17.15, "e")
E.s("LUZE", 2.60, 18.23, "i")
E.s("S3", 0.32, 17.55, "i")
E.run([(0.32, 17.55), (2.60, 18.23)], bulge=-0.25)
# f: comedor y zona general; g: cocina
sf = [(4.40, 12.20), (3.60, 16.20)]
for p in sf:
    E.s("LUZE", *p, "f")
sg = [(5.50, 14.85), (6.60, 14.85), (7.70, 13.40)]
for p in sg:
    E.s("LUZE", *p, "g")
E.s("S", 1.65, 10.56, "f")
E.s("S", 2.00, 10.56, "g")
E.run([(1.65, 10.56), sf[0], sf[1]])
E.run([(2.00, 10.56), sg[0], sg[1], sg[2]], bulge=-0.2)
# h: sala familiar
sh = [(2.60, 22.30), (6.60, 22.30), (4.60, 24.20)]
for p in sh:
    E.s("LUZE", *p, "h")
E.s("S", 1.50, 19.76, "h")
E.run([(1.50, 19.76), sh[0], sh[2], sh[1]])
E.home(0.40, 15.20, 0.0, 1.15, "TN2-1")

# ---------------------------------------------------------------- tomacorrientes generales (TN2-3)
tg = [(0.30, 2.45), (0.30, 4.55), (0.30, 5.80), (6.70, 7.48), (8.72, 4.90)]
for p in tg:
    E.s("TC", *p)
E.run([(8.72, 4.90), (6.70, 7.48), (0.30, 5.80), (0.30, 4.55), (0.30, 2.45)], bulge=0.15)
E.run([(0.30, 5.80), (0.30, 13.40)], bulge=-0.08)
E.s("TC", 0.30, 13.40)
ts = [(0.30, 21.50), (5.50, 24.90), (8.72, 23.80), (8.72, 20.00)]
for p in ts:
    E.s("TC", *p)
E.run([(8.72, 20.00), (8.72, 23.80), (5.50, 24.90), (0.30, 21.50)], bulge=0.15)
E.home(0.30, 13.40, 0.0, 0.60, "TN2-3")
E.home(0.30, 21.50, 0.0, -1.10, "TN2-3")

# ---------------------------------------------------------------- cocina (TN2-5 GFCI, TN2-7)
tc1 = [(8.72, 13.90), (8.72, 15.70), (7.80, 16.70), (5.90, 16.70)]
for p in tc1:
    E.s("GFCI", *p)
E.run(tc1, bulge=0.15)
E.home(5.90, 16.70, -0.70, 0.0, "TN2-5")
E.s("TC", 8.72, 12.90)
E.s("TC150", 7.90, 10.56)
E.s("TC", 2.90, 10.56)
E.run([(8.72, 12.90), (7.90, 10.56), (2.90, 10.56)], bulge=0.15)
E.home(2.90, 10.56, -0.70, 0.40, "TN2-7")
# ---------------------------------------------------------------- baño (TN2-9 GFCI)
E.s("GFCI", 5.15, 3.86)
E.home(5.15, 3.86, 0.0, 0.80, "TN2-9")
# ---------------------------------------------------------------- salidas especiales 240 V
E.s("T240", 8.72, 14.60)
E.home(8.72, 14.60, -0.75, 0.0, "TN2-11/13 COCINA")
E.s("T240", 3.84, 2.60)
E.home(3.84, 2.60, -0.70, 0.0, "TN2-15/17 CALENTADOR")

# ---------------------------------------------------------------- voz, datos y TV (desde el PVD)
E.s("TV", 3.48, 3.50)
E.s("TV", 0.30, 22.30)
E.s("DAT", 0.30, 23.00)
E.s("DAT", 7.40, 7.48)
E.note(1.05, 22.65, "TV Y DATOS DESDE EL PVD (N1)", 0.09)

# ================================================================ hoja
psp = H.sheet(doc, LAYOUT, "PLANTA ELÉCTRICA NIVEL 2", "")
H.north(psp, north_ang)
cl.view_title(psp, 35.0, 262.0, "PLANTA ELÉCTRICA NIVEL 2",
              "ILUMINACIÓN, TOMACORRIENTES Y VOZ/DATOS", "Esc. 1:50", 150)
cl.scale_bar(psp, 35.0, 236.0, 50, 5, 1)
EL.simbologia(psp, 35.0, 222.0, w_txt=128.0, row_h=6.6)

X2, y = 205.0, 262.0
cl.text(psp, "CIRCUITOS DEL NIVEL 2 (SUBTABLERO TN2)", (X2, y), 3.5, "A-TITULOS", "TOP_LEFT")
rows = [["CIRC.", "DESCRIPCIÓN", "DISYUNTOR", "CONDUCTORES THHN [PR]"],
        ["TN2-1", "ILUMINACIÓN NIVEL 2 (a-i)", "1P-20 A", "2 #12 + #12 T"],
        ["TN2-3", "TOMACORRIENTES GENERALES NIVEL 2", "1P-20 A", "2 #12 + #12 T"],
        ["TN2-5", "TOMAS DE COCINA 1 (GFCI)", "1P-20 A", "2 #12 + #12 T"],
        ["TN2-7", "TOMAS DE COCINA 2 (REFRIGERADORA Y OTROS)", "1P-20 A", "2 #12 + #12 T"],
        ["TN2-9", "TOMAS DE BAÑO (GFCI)", "1P-20 A", "2 #12 + #12 T"],
        ["TN2-11/13", "COCINA ELÉCTRICA 240 V", "2P-40 A", "2 #8 + #10 T"],
        ["TN2-15/17", "CALENTADOR DE PASO BAÑO SUITE 1, 240 V", "2P-40 A", "2 #10 + #10 T"]]
y = cl.table(psp, X2, y - 6.0, [22, 96, 24, 42], rows, row_h=6.3, h=2.0,
             aligns=["MIDDLE_CENTER", "MIDDLE_LEFT", "MIDDLE_CENTER", "MIDDLE_CENTER"])
cl.text(psp, "LETRAS a-i: AGRUPACIÓN DE LUMINARIAS POR APAGADOR. CARGAS, CAÍDAS DE TENSIÓN Y "
        "ALIMENTADOR DEL TN2: VER E04.", (X2, y - 2.5), 1.9, "A-TEXTO", "TOP_LEFT")

X3, y = 400.0, 262.0
cl.text(psp, "NOTAS:", (X3, y), 3.5, "A-TITULOS", "TOP_LEFT")
notas = [
    "TODAS LAS MEDIDAS ESTÁN DADAS EN METROS. [PR]",
    "LAS MEDIDAS DEBEN SER VERIFICADAS EN SITIO. [PR]",
    "TODA LA INSTALACIÓN SE REALIZARÁ EN TUBERÍA SEGÚN SE INDICA EN EL TABLERO; EN NINGÚN CASO "
    "SE USARÁ TUBERÍA EXPUESTA (TUBERÍA SOBRE CIELO DE GYPSUM Y EN PAREDES). [PR]",
    "TODAS LAS SALIDAS, TANTO ELÉCTRICAS COMO DE TV Y DATOS, SERÁN POR MEDIO DE CAJAS DE CONEXIÓN "
    "RECTANGULARES U OCTOGONALES CON SUS RESPECTIVAS TAPAS. [PR]",
    "SE IDENTIFICARÁN EN EL TABLERO LOS DIFERENTES CIRCUITOS Y SE DEJARÁN AL MENOS DOS TUBOS "
    "PREVISTOS COMO ADICIONALES. [PR]",
    "TOMACORRIENTES DE COCINA SOBRE MUEBLE Y DE BAÑO CON PROTECCIÓN GFCI.",
    "SALIDAS ESPECIALES 240 V: COCINA ELÉCTRICA Y CALENTADOR DE PASO DEL BAÑO; ALTURA Y "
    "CONEXIÓN SEGÚN EL FABRICANTE DEL EQUIPO (PD).",
    "GRADAS: EL S3 'e' CONTROLA, CON EL DEL VESTÍBULO, LA LUZ DE GRADAS DEL NIVEL 1 (E01); EL "
    "S3 'i' CONTROLA, CON EL DEL NIVEL 3, LA LUZ DE GRADAS DEL NIVEL 2 (E03).",
    "SALIDAS DE TV Y DATOS CON TUBERÍA INDEPENDIENTE DESDE EL PVD DEL NIVEL 1.",
    "DIAGRAMA UNIFILAR, ALIMENTADOR DEL TN2, CUADROS DE TABLEROS, NOTAS GENERALES Y DETALLES EN "
    "LA LÁMINA E04.",
]
cl.notes_block(psp, X3, y - 6, [f"{i}.- {t}" for i, t in enumerate(notas, 1)] + [cl.NOTA_PR], 2.1, 300)

H.titleblock(doc, psp, "E02", "ELECTRICIDAD",
             ["PLANTA ELÉCTRICA NIVEL 2.", "ILUMINACIÓN Y TOMACORRIENTES.", "VOZ Y DATOS.",
              "SIMBOLOGÍA.", "NOTAS.", ""],
             [("0", "06-10-2026", "VERSIÓN DE TRABAJO PARA REVISIÓN")], escalas="1:50")

OUT.mkdir(parents=True, exist_ok=True)
doc.saveas(OUT / f"{NAME}.dxf")
cl.render_pdf(doc, LAYOUT, OUT / f"{NAME}.pdf")
print("DXF:", OUT / f"{NAME}.dxf")
