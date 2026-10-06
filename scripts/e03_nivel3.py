"""Lámina E03 - PLANTA ELÉCTRICA NIVEL 3: iluminación, tomacorrientes y voz/datos.

Base: planta A4 rev4 aprobada (con mobiliario en gris). Simbología común (elec.py) y notas de
la referencia [PR]. Subtablero TN3 en el pasillo junto a la escalera (sobre TN2 y TP).
Cargas especiales del usuario: un calentador de paso por baño (3 baños, 240 V).
Criterios de ubicación aprobados en E01 y E02 (suites con el mismo esquema que la suite 1 del N2).
"""
import ezdxf

import cadlib as cl
import elec as EL
import hoja as H
import planta as pl

REV = "rev0"
OUT = cl.ROOT / "planos" / "E03_nivel3"
NAME = f"SR-E03_NIVEL3_{REV}"
LAYOUT = "E03-NIVEL3"
SRC = cl.ROOT / "planos/A4_nivel3/SR-A4_NIVEL3_rev4.dxf"
KEEP = {"A-MURO", "A-MURO-TRAMA", "A-PUERTA", "A-VENTANA", "A-ESCALERA", "A-ESPACIOS",
        "E-COLUMNA", "A-EJES", "A-EJES-TXT", "T-LINDERO", "T-VERTICE", "A-PROYECCION",
        "A-MOBILIARIO", "A-TXT-50"}
YM = 2.21 + 25.03                                    # reflejo suite 1 -> suite 3: y' = YM - y

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

# ---------------------------------------------------------------- tablero
E.s("TAB", 0.24, 18.20)
E.note(1.10, 18.20, "TN3", 0.14)


def suite_ext(mirror, la, lb, lc):
    """Suite de fachada (1 o 3): iluminación, tomas, baño, TV y datos. Devuelve puntos clave."""
    m = (lambda y: YM - y) if mirror else (lambda y: y)
    sa = [(1.90, m(3.50)), (2.50, m(6.40)), (5.20, m(6.60))]
    for p in sa:
        E.s("LUZE", *p, la)
    E.s("S", 1.40, m(7.45), la)
    E.run([(1.40, m(7.45)), sa[1], sa[0]], bulge=0.25 if not mirror else -0.25)
    E.run([sa[1], sa[2]], bulge=0.25 if not mirror else -0.25)
    E.s("LUZE", 4.50, m(3.30), lb)
    E.s("S", 4.90, m(4.58), lb)
    E.run([(4.90, m(4.58)), (4.50, m(3.30))], bulge=-0.3 if not mirror else 0.3)
    E.s("LUZE", 7.90, m(4.85), lc)
    E.s("S", 5.80, m(5.62), lc)
    E.run([(5.80, m(5.62)), (7.90, m(4.85))], bulge=0.25 if not mirror else -0.25)
    tg = [(8.72, m(4.90)), (6.70, m(7.48)), (0.30, m(5.80)), (0.30, m(4.55)), (0.30, m(2.45))]
    for p in tg:
        E.s("TC", *p)
    E.run(tg, bulge=0.15 if not mirror else -0.15)
    E.s("GFCI", 5.15, m(3.86))
    E.s("T240", 3.84, m(2.60))
    E.s("TV", 3.48, m(3.50))
    E.s("DAT", 7.40, m(7.48))
    return tg


# ---------------------------------------------------------------- suite 1 (a, b, c)
tg1 = suite_ext(False, "a", "b", "c")
E.home(5.15, 3.86, 0.0, 0.80, "TN3-7")
E.home(3.84, 2.60, -0.70, 0.0, "TN3-9/11 CALENTADOR")
# ---------------------------------------------------------------- suite 3 (n, o, p)
tg3 = suite_ext(True, "n", "o", "p")
E.home(5.15, YM - 3.86, 0.0, -0.80, "TN3-7")
E.home(3.84, YM - 2.60, -0.70, 0.0, "TN3-17/19 CALENTADOR")
E.home(0.30, YM - 5.80, 0.0, -0.90, "TN3-5")

# ---------------------------------------------------------------- galería y pasillo (d), gradas (i, j)
sd = [(0.40, 9.00), (0.40, 12.00), (0.40, 15.20)]
for p in sd:
    E.s("LUZE", *p, "d")
E.s("S3", 0.32, 8.00, "d")
E.s("S3", 0.32, 19.30, "d")
E.run([(0.32, 8.00), sd[0], sd[1], sd[2], (0.32, 19.30)], bulge=0.15)
E.s("S3", 0.32, 17.15, "i")
E.s("LUZE", 2.60, 18.23, "j")
E.s("S", 0.32, 17.55, "j")
E.run([(0.32, 17.55), (2.60, 18.23)], bulge=-0.25)
E.home(0.40, 15.20, 0.0, 1.15, "TN3-1")
E.s("TC", 0.30, 13.40)
E.run([tg1[2], (0.30, 13.40)], bulge=-0.08)
E.home(0.30, 13.40, 0.0, 0.60, "TN3-3")

# ---------------------------------------------------------------- suite 2 (k, l, m)
sk = [(2.60, 12.20), (3.80, 15.20)]
for p in sk:
    E.s("LUZE", *p, "k")
E.s("S", 1.62, 15.30, "k")
E.run([(1.62, 15.30), sk[1], sk[0]])
E.s("LUZE", 8.35, 14.95, "l")
E.s("S", 7.05, 14.95, "l")
E.run([(7.05, 14.95), (8.35, 14.95)], bulge=0.3)
E.s("LUZE", 7.60, 13.30, "m")
E.s("S", 5.85, 13.25, "m")
E.run([(5.85, 13.25), (7.60, 13.30)], bulge=0.3)
t2 = [(8.72, 12.00), (5.00, 10.56), (1.60, 11.15), (1.60, 13.25), (2.40, 16.70)]
for p in t2:
    E.s("TC", *p)
E.run(t2, bulge=0.15)
E.home(2.40, 16.70, -0.55, 0.0, "TN3-5")
E.s("GFCI", 8.72, 15.40)
E.home(8.72, 15.40, -0.70, 0.30, "TN3-7")
E.s("T240", 7.42, 16.55)
E.home(7.42, 16.55, -0.60, -0.35, "TN3-13/15")
E.s("TV", 5.86, 11.60)
E.s("DAT", 5.86, 11.10)

# ================================================================ hoja
psp = H.sheet(doc, LAYOUT, "PLANTA ELÉCTRICA NIVEL 3", "")
H.north(psp, north_ang)
cl.view_title(psp, 35.0, 262.0, "PLANTA ELÉCTRICA NIVEL 3",
              "ILUMINACIÓN, TOMACORRIENTES Y VOZ/DATOS", "Esc. 1:50", 150)
cl.scale_bar(psp, 35.0, 236.0, 50, 5, 1)
EL.simbologia(psp, 35.0, 222.0, w_txt=128.0, row_h=6.6)

X2, y = 205.0, 262.0
cl.text(psp, "CIRCUITOS DEL NIVEL 3 (SUBTABLERO TN3)", (X2, y), 3.5, "A-TITULOS", "TOP_LEFT")
rows = [["CIRC.", "DESCRIPCIÓN", "DISYUNTOR", "CONDUCTORES THHN [PR]"],
        ["TN3-1", "ILUMINACIÓN NIVEL 3 (a-p)", "1P-20 A", "2 #12 + #12 T"],
        ["TN3-3", "TOMAS GENERALES SUITE 1 Y PASILLO", "1P-20 A", "2 #12 + #12 T"],
        ["TN3-5", "TOMAS GENERALES SUITES 2 Y 3", "1P-20 A", "2 #12 + #12 T"],
        ["TN3-7", "TOMAS DE BAÑOS (GFCI)", "1P-20 A", "2 #12 + #12 T"],
        ["TN3-9/11", "CALENTADOR DE PASO BAÑO SUITE 1, 240 V", "2P-40 A", "2 #10 + #10 T"],
        ["TN3-13/15", "CALENTADOR DE PASO BAÑO SUITE 2, 240 V", "2P-40 A", "2 #10 + #10 T"],
        ["TN3-17/19", "CALENTADOR DE PASO BAÑO SUITE 3, 240 V", "2P-40 A", "2 #10 + #10 T"]]
y = cl.table(psp, X2, y - 6.0, [22, 96, 24, 42], rows, row_h=6.3, h=2.0,
             aligns=["MIDDLE_CENTER", "MIDDLE_LEFT", "MIDDLE_CENTER", "MIDDLE_CENTER"])
cl.text(psp, "LETRAS a-p: AGRUPACIÓN DE LUMINARIAS POR APAGADOR. CARGAS, CAÍDAS DE TENSIÓN Y "
        "ALIMENTADOR DEL TN3: VER E04.", (X2, y - 2.5), 1.9, "A-TEXTO", "TOP_LEFT")

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
    "TOMACORRIENTES DE BAÑO CON PROTECCIÓN GFCI.",
    "SALIDAS ESPECIALES 240 V: UN CALENTADOR DE PASO POR BAÑO; ALTURA Y CONEXIÓN SEGÚN EL "
    "FABRICANTE DEL EQUIPO.",
    "GRADAS: EL S3 'i' CONTROLA, CON EL DEL NIVEL 2, LA LUZ DE GRADAS DEL NIVEL 2 (E02); LA LUZ "
    "'j' ILUMINA LA LLEGADA AL NIVEL 3.",
    "SALIDAS DE TV Y DATOS CON TUBERÍA INDEPENDIENTE DESDE EL PVD DEL NIVEL 1.",
    "DIAGRAMA UNIFILAR, ALIMENTADOR DEL TN3, CUADROS DE TABLEROS, NOTAS GENERALES Y DETALLES EN "
    "LA LÁMINA E04.",
]
cl.notes_block(psp, X3, y - 6, [f"{i}.- {t}" for i, t in enumerate(notas, 1)] + [cl.NOTA_PR], 2.1, 300)

H.titleblock(doc, psp, "E03", "ELECTRICIDAD",
             ["PLANTA ELÉCTRICA NIVEL 3.", "ILUMINACIÓN Y TOMACORRIENTES.", "VOZ Y DATOS.",
              "SIMBOLOGÍA.", "NOTAS.", ""],
             [("0", "06-10-2026", "VERSIÓN DE TRABAJO PARA REVISIÓN")], escalas="1:50")

OUT.mkdir(parents=True, exist_ok=True)
doc.saveas(OUT / f"{NAME}.dxf")
cl.render_pdf(doc, LAYOUT, OUT / f"{NAME}.pdf")
print("DXF:", OUT / f"{NAME}.dxf")
