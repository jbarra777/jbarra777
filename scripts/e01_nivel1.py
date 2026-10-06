"""Lámina E01 - PLANTA ELÉCTRICA NIVEL 1: iluminación, tomacorrientes y voz/datos.

Base: planta A2 rev3 aprobada (muros, puertas, escalera, ejes, columnas). Simbología, alturas
de montaje y notas de la referencia (RIVERGRAND EL01-EL08) [PR]. Esquema de tableros del
usuario: medidor en el frente, tablero principal TP en el vestíbulo del N1 y subtableros TN2 y
TN3. Circuitos del N1 en el TP. Conductores y disyuntores de la referencia [PR] (ver E04).
"""
import ezdxf

import cadlib as cl
import elec as EL
import hoja as H
import planta as pl

REV = "rev1"
OUT = cl.ROOT / "planos" / "E01_nivel1"
NAME = f"SR-E01_NIVEL1_{REV}"
LAYOUT = "E01-NIVEL1"
SRC = cl.ROOT / "planos/A2_nivel1/SR-A2_NIVEL1_rev3.dxf"
KEEP = {"A-MURO", "A-MURO-TRAMA", "A-PUERTA", "A-VENTANA", "A-ESCALERA", "A-ESPACIOS",
        "E-COLUMNA", "A-EJES", "A-EJES-TXT", "T-LINDERO", "T-VERTICE", "A-PROYECCION",
        "A-DEMARCACION"}

doc = cl.new_doc()
cl.north_block(doc)
msp = doc.modelspace()
north_ang = pl.add_crtm_ucs(doc, H.FRAME)
EL.layers(doc)
src = ezdxf.readfile(SRC)
for e in src.modelspace():
    if e.dxf.layer in KEEP:
        msp.add_entity(e.copy())
for name in KEEP:                                   # base arquitectónica en gris
    if name in doc.layers and name not in ("A-ESPACIOS", "A-EJES-TXT"):
        doc.layers.get(name).color = 8
H.general_dims(msp)
E = EL.Plan(msp)

# ---------------------------------------------------------------- acometida, medidor y tablero
E.s("M", 1.41, 1.80)
E.note(1.41, 1.30, "MEDIDOR", 0.11)
E.run([(1.41, -1.20), (1.41, 1.62)], bulge=0.0)
E.note(3.40, -0.75, "ACOMETIDA SUBTERRÁNEA (VER E04)", 0.11, rot=90)
E.s("TAB", 0.24, 18.15)
E.note(0.62, 17.95, "TP", 0.14)
E.s("TVD", 0.24, 15.90)
E.note(0.62, 15.90, "PVD", 0.13)
E.run([(1.41, 1.98), (0.55, 2.60), (0.55, 17.70), (0.40, 18.15)], bulge=0.0)
E.note(1.12, 5.60, "ALIMENTADOR TP SUBTERRÁNEO (VER E04)", 0.10)
E.run([(1.41, 1.98), (0.40, 2.75), (0.40, 15.90)], bulge=0.0)
E.note(1.12, 10.20, "PREVISTA VOZ Y DATOS (VER E04)", 0.10)

# ---------------------------------------------------------------- iluminación (circuito TP-1)
# a: pasillo peatonal (tres vías: acceso y vestíbulo)
pas = [(0.85, 3.30), (0.85, 7.20), (0.85, 11.20), (0.85, 15.20)]
for x, y in pas:
    E.s("LUZ", x, y, "a")
E.s("S3", 0.32, 2.55, "a")
E.s("S3", 0.32, 16.50, "a")
E.run([(0.32, 2.55), pas[0], pas[1], pas[2], pas[3], (0.32, 16.50)])
# b: estacionamientos
est = [(2.60, 6.10), (5.10, 6.10), (7.60, 6.10)]
for x, y in est:
    E.s("LUZ", x, y, "b")
E.s("S", 0.32, 3.10, "b")
E.run([(0.32, 3.10), est[0], est[1], est[2]])
# c: jardín seco frontal (bajo el entrepiso)
jf = [(3.30, 13.60), (6.90, 13.60)]
for x, y in jf:
    E.s("LUZ", x, y, "c")
E.s("S", 0.32, 13.60, "c")
E.run([(0.32, 13.60), jf[0], jf[1]])
# d: vestíbulo; e: gradas (tres vías con el N2)
E.s("LUZ", 0.80, 18.25, "d")
E.s("S", 0.32, 17.15, "d")
E.run([(0.32, 17.15), (0.80, 18.25)])
E.s("LUZ", 2.60, 18.23, "e")
E.s("S3", 0.32, 17.45, "e")
E.run([(0.32, 17.45), (2.60, 18.23)], bulge=-0.25)
E.note(3.60, 17.55, "S3 'e' EN LLEGADA N2 (E02)", 0.10)
# f: jardín seco posterior
jp = [(2.60, 22.30), (6.60, 22.30)]
for x, y in jp:
    E.s("LUZ", x, y, "f")
E.s("S", 0.80, 19.75, "f")
E.run([(0.80, 19.75), jp[0], jp[1]])
# g: aplique exterior en la fachada (acceso peatonal)
E.s("APL", 0.75, 1.90, "g")
E.s("S", 0.32, 3.50, "g")
E.run([(0.32, 3.50), (0.75, 1.90)], bulge=-0.35)
E.home(0.85, 15.20, 0.0, 1.10, "TP-1")

# ---------------------------------------------------------------- tomacorrientes (circuito TP-3)
tomas = [("GFCI", 8.72, 4.70), ("TC", 0.30, 9.20), ("GFCI", 8.72, 13.60), ("TC", 1.20, 19.38),
         ("GFCI", 8.72, 22.30)]
for k, x, y in tomas:
    E.s(k, x, y)
E.run([(8.72, 4.70), (8.72, 13.60), (8.72, 22.30)], bulge=0.12)
E.home(8.72, 22.30, -0.90, -0.60, "TP-3")
E.run([(0.30, 9.20), (1.20, 19.38)], bulge=-0.08)
E.home(1.20, 19.38, -0.30, 0.55, "TP-3")
E.note(7.60, 21.60, "TOMAS EXTERIORES CON GFCI Y TAPA A PRUEBA DE INTEMPERIE", 0.10)

# ================================================================ hoja
psp = H.sheet(doc, LAYOUT, "PLANTA ELÉCTRICA NIVEL 1", "")
H.north(psp, north_ang)
cl.view_title(psp, 35.0, 262.0, "PLANTA ELÉCTRICA NIVEL 1",
              "ILUMINACIÓN, TOMACORRIENTES Y VOZ/DATOS", "Esc. 1:50", 150)
cl.scale_bar(psp, 35.0, 236.0, 50, 5, 1)
EL.simbologia(psp, 35.0, 222.0, w_txt=128.0, row_h=6.6)

X2, y = 205.0, 262.0
cl.text(psp, "CIRCUITOS DEL NIVEL 1 (TABLERO TP)", (X2, y), 3.5, "A-TITULOS", "TOP_LEFT")
rows = [["CIRC.", "DESCRIPCIÓN", "DISYUNTOR", "CONDUCTORES THHN [PR]"],
        ["TP-1", "ILUMINACIÓN NIVEL 1 (a-g)", "1P-20 A", "2 #12 + #12 T"],
        ["TP-3", "TOMACORRIENTES NIVEL 1 (GFCI EN EXTERIOR)", "1P-20 A", "2 #12 + #12 T"]]
y = cl.table(psp, X2, y - 6.0, [18, 92, 26, 44], rows, row_h=6.5, h=2.1,
             aligns=["MIDDLE_CENTER", "MIDDLE_LEFT", "MIDDLE_CENTER", "MIDDLE_CENTER"])
cl.text(psp, "LETRAS a-g: AGRUPACIÓN DE LUMINARIAS POR APAGADOR. ALIMENTADORES DE TN2 Y TN3, "
        "DEMÁS CIRCUITOS DEL TP: VER E04.", (X2, y - 2.5), 1.9, "A-TEXTO", "TOP_LEFT")

X3, y = 400.0, 262.0
cl.text(psp, "NOTAS:", (X3, y), 3.5, "A-TITULOS", "TOP_LEFT")
notas = [
    "TODAS LAS MEDIDAS ESTÁN DADAS EN METROS. [PR]",
    "LAS MEDIDAS DEBEN SER VERIFICADAS EN SITIO. [PR]",
    "TODA LA INSTALACIÓN SE REALIZARÁ EN TUBERÍA SEGÚN SE INDICA EN EL TABLERO. EN EL NIVEL 1 "
    "(ESTRUCTURA EXPUESTA, SIN CIELO) LA TUBERÍA EXPUESTA A MENOS DE 2,5 m DE ALTURA SERÁ "
    "METÁLICA (EMT). [PR]",
    "TODAS LAS SALIDAS, TANTO ELÉCTRICAS COMO DE TV Y DATOS, SERÁN POR MEDIO DE CAJAS DE CONEXIÓN "
    "RECTANGULARES U OCTOGONALES CON SUS RESPECTIVAS TAPAS. [PR]",
    "SE IDENTIFICARÁN EN EL TABLERO LOS DIFERENTES CIRCUITOS Y SE DEJARÁN AL MENOS DOS TUBOS "
    "PREVISTOS COMO ADICIONALES. [PR]",
    "TOMACORRIENTES EN ESTACIONAMIENTOS Y EXTERIORES CON PROTECCIÓN GFCI Y TAPA A PRUEBA DE "
    "INTEMPERIE.",
    "UBICACIÓN EXACTA DEL MEDIDOR SEGÚN LA EMPRESA DISTRIBUIDORA (PD). DIAGRAMA UNIFILAR, "
    "CUADROS DE TABLEROS, NOTAS GENERALES Y DETALLES EN LA LÁMINA E04.",
]
cl.notes_block(psp, X3, y - 6, [f"{i}.- {t}" for i, t in enumerate(notas, 1)] + [cl.NOTA_PR], 2.1, 300)

H.titleblock(doc, psp, "E01", "ELECTRICIDAD",
             ["PLANTA ELÉCTRICA NIVEL 1.", "ILUMINACIÓN Y TOMACORRIENTES.", "VOZ Y DATOS.",
              "SIMBOLOGÍA.", "NOTAS.", ""],
             [("0", "06-10-2026", "VERSIÓN DE TRABAJO PARA REVISIÓN"),
              ("1", "06-10-2026", "SIN MENCIÓN A SECADORA")], escalas="1:50")

OUT.mkdir(parents=True, exist_ok=True)
doc.saveas(OUT / f"{NAME}.dxf")
cl.render_pdf(doc, LAYOUT, OUT / f"{NAME}.pdf")
print("DXF:", OUT / f"{NAME}.dxf")
