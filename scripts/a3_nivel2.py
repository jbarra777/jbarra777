"""Lámina A3 - PLANTA NIVEL 2 (suite al frente, cocina-comedor, sala familiar).

Base: plantas A-201 (anteproyecto) con las correcciones acordadas: accesos al final
del pasillo (ejes 2 y 5), escalera en U, baño en línea 1.55 x 2.20, pasillo cerrado
con vidrio hacia P1, cocina en L con isla y columnas sobre el eje C.
"""
from ezdxf.math import Vec2

import cadlib as cl
import hoja as H
import planta as pl
from planta import P

REV = "rev0"
OUT = cl.ROOT / "planos" / "A3_nivel2"
NAME = f"SR-A3_NIVEL2_{REV}"
E, I, W = H.E, H.I, H.W
XB0, XB1 = H.XB0, H.XB1
YF0, YF1, YR0, YR1 = H.YF0, H.YF1, H.YR0, H.YR1
Y2a, Y2b, Y3a, Y3b = H.Y2a, H.Y2b, H.Y3a, H.Y3b
Y4a, Y4b, Y5a, Y5b = H.Y4a, H.Y4b, H.Y5a, H.Y5b
P1, P2, ESC = H.P1, H.P2, H.ESC
X0, X1 = ESC["x"]                                  # escalera 1.35 / 4.69
XC0, XC1 = X1, P2["x"][0]                          # muro escalera/P2 (4.69-4.81)
NPT = "NPT +3.00"

doc = cl.new_doc()
cl.north_block(doc)
msp = doc.modelspace()
north_ang = pl.add_crtm_ucs(doc, H.FRAME)
H.lot(msp)


def wall_with_openings(axis, c0, c1, a, b, openings, windows=()):
    """Muro paralelo a x (axis='x': de x=a a x=b entre y=c0..c1) o a y (axis='y').

    openings/windows: lista de (s0, s1) a lo largo del muro. Las ventanas se dibujan.
    """
    cuts = sorted(list(openings) + list(windows))
    pos = a
    for s0, s1 in cuts:
        if s0 > pos:
            (pl.wall(msp, pos, s0, c0, c1) if axis == "x" else pl.wall(msp, c0, c1, pos, s0))
        pos = s1
    if pos < b:
        (pl.wall(msp, pos, b, c0, c1) if axis == "x" else pl.wall(msp, c0, c1, pos, b))
    for s0, s1 in windows:
        (pl.window_y(msp, s0, s1, c0, c1) if axis == "x" else pl.window_x(msp, s0, s1, c0, c1))


# ---------------------------------------------------------------- muros perimetrales
pl.wall(msp, 0.0, E, YF0, YR1)                       # colindancia oeste (ciega)
pl.wall(msp, W - E, W, YF0, YR1)                     # colindancia este (ciega)
# fachada frontal: dormitorio / baño / walk-in
wall_with_openings("x", YF0, YF1, E, W - E, [], [(0.70, 2.90), (3.95, 4.95), (6.40, 8.20)])
# fachada posterior: sala familiar
wall_with_openings("x", YR0, YR1, E, W - E, [], [(0.90, 3.90), (5.00, 8.00)])
# eje 2: suite / pasillo-P1 (puerta de suite al final del pasillo)
D_SUI = (0.25, 1.15)
wall_with_openings("x", Y2a, Y2b, E, W - E, [D_SUI], [(2.00, 4.40), (5.60, 8.20)])
# eje 3: P1 / cocina-comedor (ventanas desfasadas respecto a la suite)
wall_with_openings("x", Y3a, Y3b, XB1, W - E, [], [(2.70, 4.30), (5.70, 7.90)])
# eje B: pasillo / P1 (vidrio fijo) y pasillo / cocina (puerta)
D_COC = (15.55, 16.45)
pl.window_x(msp, Y2b + 0.10, Y3a - 0.10, XB0, XB1)
pl.wall(msp, XB0, XB1, Y2b, Y2b + 0.10, hatch=True)
pl.wall(msp, XB0, XB1, Y3a - 0.10, Y3b, hatch=True)
wall_with_openings("y", XB0, XB1, Y3b, Y4a, [D_COC])
# eje 4: cocina / escalera-P2 (ventana sobre fregadero)
wall_with_openings("x", Y4a, Y4b, XB0, W - E, [], [(5.40, 8.20)])
# eje C: escalera / P2
pl.wall(msp, XC0, XC1, Y4b, Y5a)
# eje 5: escalera-P2 / sala (puerta de sala al final del pasillo)
D_SAL = (0.25, 1.15)
wall_with_openings("x", Y5a, Y5b, E, W - E, [D_SAL], [(5.40, 8.40)])

# ---------------------------------------------------------------- suite 1
XBA0, XBA1 = 3.72, 5.27            # baño libre 1.55
YBA1 = YF1 + 2.20                  # 4.41
XWI0 = XBA1 + I                    # walk-in libre desde 5.39
YWI1 = YF1 + 3.25                  # 5.46
pl.wall(msp, XBA0 - I, XBA0, YF1, YBA1 + I)                    # muro oeste baño
D_BA = (XBA0, XBA0 + 0.80)
wall_with_openings("x", YBA1, YBA1 + I, XBA0, XBA1, [D_BA])    # muro sur baño
pl.wall(msp, XBA1, XWI0, YF1, YWI1 + I)                        # muro baño / walk-in
D_WI = (6.00, 6.80)
wall_with_openings("x", YWI1, YWI1 + I, XWI0, W - E, [D_WI])   # muro sur walk-in

# puertas
pl.door(msp, (D_SUI[1], Y2a), 0.90, (-1, 0), (0, -1))          # suite (abre hacia adentro)
pl.door(msp, (D_BA[0], YBA1 + I), 0.80, (1, 0), (0, 1))        # baño (abre al dormitorio)
pl.door(msp, (D_WI[0], YWI1), 0.80, (1, 0), (0, -1))           # walk-in
pl.door(msp, (XB1, D_COC[1]), 0.90, (0, -1), (1, 0))           # cocina-comedor
pl.door(msp, (D_SAL[1], Y5b), 0.90, (-1, 0), (0, 1))           # sala familiar

# mobiliario suite
pl.bed(msp, E, 2.70, E + 2.00, 4.30, head="x0")
pl.rect(msp, E, 2.22, E + 0.45, 2.65)
pl.rect(msp, E, 4.35, E + 0.45, 4.78)
pl.sofa(msp, 2.00, 6.72, 4.00, 7.57, back="y1")
pl.rect(msp, 2.50, 5.85, 3.50, 6.35)
pl.sofa(msp, 0.55, 5.35, 1.35, 6.15, back="x0")
pl.rect(msp, 6.40, 7.00, 7.60, 7.58)                            # escritorio
pl.chair(msp, 7.00, 6.70, (0, 1))
# baño en línea: ducha / inodoro / lavatorio
pl.shower(msp, XBA0, YF1, XBA1, YF1 + 0.85)
pl.wc(msp, XBA1, YF1 + 0.85 + 0.375, (-1, 0))
pl.lav(msp, XBA1 - 0.50, YF1 + 1.65, XBA1, YF1 + 2.15)
# walk-in
pl.closet(msp, W - E - 0.60, YF1, W - E, YWI1, "y")
pl.closet(msp, XWI0, YF1, XWI0 + 0.60, 4.60, "y")

# ---------------------------------------------------------------- cocina - comedor
XK1 = W - E                                                     # 8.85
pl.rect(msp, XK1 - 0.60, 12.60, XK1, 13.40)                     # refrigeradora
pl.text(msp, "REF", XK1 - 0.30, 13.00, 0.10, "A-MOBILIARIO")
pl.counter(msp, XK1 - 0.60, 13.40, XK1, Y4a)                    # mueble este
pl.stove(msp, XK1 - 0.58, 14.30, XK1 - 0.02, 14.90)
pl.counter(msp, 5.60, Y4a - 0.60, XK1 - 0.60, Y4a)              # mueble sur
pl.sink(msp, 6.40, Y4a - 0.55, 7.20, Y4a - 0.08)
pl.rect(msp, 4.90, 14.40, 7.20, 15.30)                          # isla
pl.text(msp, "ISLA", 6.05, 14.85, 0.10, "A-MOBILIARIO")
pl.closet(msp, 7.00, Y3b, XK1, Y3b + 0.60, "x")                 # despensa
pl.text(msp, "DESPENSA", 7.92, Y3b + 0.30, 0.08, "A-MOBILIARIO")
pl.rect(msp, 2.00, Y3b, 3.80, Y3b + 0.45)                       # aparador
pl.text(msp, "APARADOR", 2.90, Y3b + 0.22, 0.08, "A-MOBILIARIO")
pl.rect(msp, 3.30, 11.70, 5.50, 12.70)                          # mesa 8 puestos
for xc in (3.65, 4.40, 5.15):
    pl.chair(msp, xc, 11.43, (0, 1))
    pl.chair(msp, xc, 12.97, (0, -1))
pl.chair(msp, 3.03, 12.20, (1, 0))
pl.chair(msp, 5.77, 12.20, (-1, 0))

# ---------------------------------------------------------------- sala familiar
pl.rect(msp, E, 21.40, E + 0.45, 23.20)                         # mueble TV
pl.text(msp, "TV", E + 0.22, 22.30, 0.10, "A-MOBILIARIO")
pl.sofa(msp, 3.10, 21.00, 3.95, 23.60, back="x1")
pl.rect(msp, 1.80, 21.80, 2.60, 22.80)
pl.sofa(msp, 1.80, 23.75, 2.60, 24.55, back="y1")
pl.round_table(msp, 6.60, 23.30, 0.45, 4)
pl.rect(msp, XK1 - 0.40, 20.30, XK1, 22.80)                     # librero
pl.text(msp, "LIBRERO", XK1 - 0.20, 21.55, 0.08, "A-MOBILIARIO", rot=90)

# ---------------------------------------------------------------- escalera (nivel 2)
TH = 0.28
yA0, yA1 = Y4b, Y4b + 1.10             # tramo que sube a N3
yB0, yB1 = Y5a - 1.10, Y5a             # tramo que llega desde N1 (baja)
X_DES = X0 + 8 * TH                    # 3.59
CUT = X0 + 6 * TH
for k in range(0, 9):
    x = X0 + k * TH
    lay = "A-ESCALERA" if x <= CUT + 1e-6 else "A-PROYECCION"
    pl.line(msp, (x, yA0), (x, yA1), lay, None if lay == "A-ESCALERA" else pl.LT_DASH)
pl.line(msp, (X0, yA1), (CUT, yA1), "A-ESCALERA")
pl.line(msp, (CUT, yA1), (X_DES, yA1), "A-PROYECCION", pl.LT_DASH)
pl.line(msp, (CUT - 0.25, yA0), (CUT + 0.25, yA1), "A-ESCALERA")
for k in range(0, 8):
    x = X_DES - k * TH
    pl.line(msp, (x, yB0), (x, yB1), "A-ESCALERA")
pl.line(msp, (X_DES - 7 * TH, yB0), (X_DES, yB0), "A-ESCALERA")
pl.line(msp, (X_DES, yA0), (X_DES, yB1), "A-PROYECCION", pl.LT_DASH)
pl.line(msp, (X_DES - 7 * TH, yA1 + 0.15), (X_DES, yA1 + 0.15), "A-ESCALERA")  # pasamanos ojo


def arrow(xa, xb, y, label):
    a, b = P(xa, y), P(xb, y)
    msp.add_line(a, b, dxfattribs={"layer": "A-ESCALERA"})
    d = (b - a).normalize()
    n = Vec2(-d.y, d.x)
    msp.add_solid([b, b - d * 0.20 + n * 0.12, b - d * 0.20 - n * 0.12],
                  dxfattribs={"layer": "A-ESCALERA"})
    pl.text(msp, label, (xa + xb) / 2, y + 0.18, 0.12, "A-ESCALERA")


arrow(X0 + 0.15, CUT - 0.15, (yA0 + yA1) / 2, "SUBE")
arrow(X0 + 0.45, X_DES - 0.15, (yB0 + yB1) / 2, "BAJA")

# ---------------------------------------------------------------- columnas y proyecciones
H.columns(msp)
for PP in (P1, P2):
    (xa, xb), (ya, yb) = PP["x"], PP["y"]
    pl.line(msp, (xa, ya), (xb, yb), "A-PROYECCION", pl.LT_DASH)
    pl.line(msp, (xb, ya), (xa, yb), "A-PROYECCION", pl.LT_DASH)

# ---------------------------------------------------------------- rótulos
A_SUI = (W - 2 * E) * (Y2a - YF1)
A_BA = (XBA1 - XBA0) * (YBA1 - YF1)
A_WI = (W - E - XWI0) * (YWI1 - YF1)
A_COC = (W - E - XB1) * (Y4a - Y3b)
A_SAL = (W - 2 * E) * (YR0 - Y5b)
L_PAS = Y5a - Y2b
A_PAS = (XB0 - E) * L_PAS
A_GRA = (X1 - X0) * (Y5a - Y4b)
pl.room_label(msp, "SUITE 1\\PDORMITORIO Y ESTAR", 1.95, 5.25, None, None, 0.15)
pl.room_label(msp, "BAÑO", 4.12, 3.75, None, A_BA, 0.10)
pl.room_label(msp, "WALK-IN CLOSET", 7.10, 3.85, "3.46 x 3.25", A_WI, 0.12)
pl.room_label(msp, "COCINA - COMEDOR", 2.90, 14.90, "7.38 x 6.42", A_COC, 0.15)
pl.room_label(msp, "SALA FAMILIAR", 6.20, 20.70, "8.70 x 5.40", A_SAL, 0.15)
pl.text(msp, "PASILLO", 0.75, 13.00, 0.13, "A-ESPACIOS")
pl.text(msp, "GALERÍA - VIDRIO FIJO A P1", 0.75, 9.0, 0.085, "A-TXT-50")
pl.mtext(msp, "PATIO DE LUZ P1\\P(ABIERTO)", 5.16, 9.0, 0.14, 3.0, "A-ESPACIOS")
pl.mtext(msp, "PATIO P2\\P(ABIERTO)", 6.83, 18.25, 0.14, 3.0, "A-ESPACIOS")
pl.text(msp, "GRADAS EN U: 17 CH = 0.176 / H = 0.28", 0.75, Y4b + 0.05, 0.085, "A-TXT-50",
        "MIDDLE_LEFT")
pl.text(msp, "CALLE PÚBLICA", 4.5, -2.15, 0.22, "A-ESPACIOS", rot=90)
pl.mtext(msp, "COLINDANCIA - FACHADA CIEGA", -0.35, 14.0, 0.10, 6.0, "A-TXT-50")
pl.mtext(msp, "COLINDANCIA - FACHADA CIEGA", W + 0.35, 14.0, 0.10, 6.0, "A-TXT-50")
for (x, y) in ((2.6, 3.6 - 0.8), (0.45, 11.0), (2.0, 15.9), (5.2, 24.4)):
    pl.level(msp, x, y, NPT)

# ---------------------------------------------------------------- ejes y cotas
H.axes(msp)
H.general_dims(msp)
chain = [YF0, YF1, Y2a, Y2b, Y3a, Y3b, Y4a, Y4b, Y5a, Y5b, YR0, YR1]
for ya, yb in zip(chain[:-1], chain[1:]):
    pl.dim(msp, (W - E, ya), (W - E, yb), (W + 0.95, 0), False)
for xa, xb in ((XBA0 - I, XBA0), (XBA0, XBA1), (XBA1, XWI0), (XWI0, W - E)):
    pl.dim(msp, (xa, YF1), (xb, YF1), (0, 5.02), True)
pl.dim(msp, (XBA0, YF1), (XBA0, YBA1), (XBA0 + 0.25, 0), False)
pl.dim(msp, (6.10, YF1), (6.10, YWI1), (6.10, 0), False)
for xa, xb in ((E, XB0), (XB0, XB1), (XB1, W - E)):
    pl.dim(msp, (xa, 13.65), (xb, 13.65), (0, 13.65), True)
pl.dim(msp, (X0, Y5b), (X1, Y5b), (0, Y5b + 0.35), True)
pl.dim(msp, (XC1, Y4b), (W - E, Y4b), (0, Y4b + 0.45), True)
pl.dim(msp, (E, YR0), (W - E, YR0), (0, YR0 - 0.40), True)
H.sections(msp)

# ---------------------------------------------------------------- hoja
psp = H.sheet(doc, "A3-NIVEL2", "PLANTA NIVEL 2", "")
H.north(psp, north_ang)
H.title_and_derrotero(psp, "PLANTA NIVEL 2", "SUITE 1, COCINA - COMEDOR Y SALA FAMILIAR")

X2 = 240.0
y = 262.0
cl.text(psp, "CUADRO DE ÁREAS NIVEL 2", (X2 + 100, y), 4.5, "A-TITULOS", "TOP_CENTER")
rows = [["ESPACIO (MEDIDAS LIBRES)", "ÁREA"],
        ["SUITE 1 (DORMITORIO-ESTAR, BAÑO Y WALK-IN) 8,70 x 5,40", cl.m2(A_SUI)],
        ["      BAÑO 1,55 x 2,20", cl.m2(A_BA)],
        ["      WALK-IN CLOSET 3,46 x 3,25", cl.m2(A_WI)],
        ["COCINA - COMEDOR 7,38 x 6,42", cl.m2(A_COC)],
        ["SALA FAMILIAR 8,70 x 5,40", cl.m2(A_SAL)],
        [f"PASILLO 1,20 x {L_PAS:.2f}".replace(".", ","), cl.m2(A_PAS)],
        ["GRADAS 3,34 x 2,50", cl.m2(A_GRA)],
        ["ÁREA CONSTRUIDA NIVEL 2 (ENVOLVENTE - PATIOS)", cl.m2(H.A_HUELLA)]]
y = cl.table(psp, X2, y - 8, [150, 50], rows, row_h=5.6, h=2.3,
             aligns=["MIDDLE_LEFT", "MIDDLE_RIGHT"])
cl.text(psp, "ÁREA CONSTRUIDA INCLUYE MUROS. BAÑO Y WALK-IN ESTÁN INCLUIDOS EN LA SUITE.",
        (X2, y - 1.5), 1.9, "A-TEXTO", "TOP_LEFT")
y -= 9
cl.text(psp, "RESUMEN DE ÁREAS DE CONSTRUCCIÓN", (X2 + 100, y), 3.5, "A-TITULOS", "TOP_CENTER")
A_N3 = H.A_HUELLA
rows = [["NIVEL 1 (VER A2)", cl.m2(H.A_N1)],
        ["NIVEL 2", cl.m2(H.A_HUELLA)],
        ["NIVEL 3 (PRELIMINAR, VER A4)", cl.m2(A_N3)],
        ["ÁREA TOTAL DE CONSTRUCCIÓN", cl.m2(H.A_N1 + H.A_HUELLA + A_N3)]]
y = cl.table(psp, X2, y - 7, [150, 50], rows, row_h=5.6, h=2.3,
             aligns=["MIDDLE_LEFT", "MIDDLE_RIGHT"])
y = H.cobertura(psp, X2, y - 6)

X3 = 455.0
y = 262.0
cl.text(psp, "NOTAS:", (X3, y), 3.5, "A-TITULOS", "TOP_LEFT")
extra = [
    "NIVEL 2: NPT +3.00 (ALTURA PISO A PISO 3.00 m, PROVISIONAL).",
    "SUITE: BAÑO DE 1.55 x 2.20 m CON DUCHA, INODORO Y LAVATORIO EN LÍNEA Y PUERTA DE 0.80 m "
    "ABATIBLE HACIA EL DORMITORIO; WALK-IN CLOSET CON MUEBLES DE 0.60 m. SOLO EL BAÑO Y EL "
    "WALK-IN SON RECINTOS CERRADOS.",
    "PASILLO DE 1.20 m CERRADO HACIA EL PATIO P1 CON VIDRIO FIJO (GALERÍA). ACCESOS A LA SUITE "
    "Y A LA SALA FAMILIAR EN LOS EXTREMOS DEL PASILLO (EJES 2 Y 5).",
    "COCINA EN L CON ISLA; FREGADERO BAJO VENTANA HACIA EL PATIO P2. LA COCINA-COMEDOR Y LA "
    "SALA FAMILIAR NO LLEVAN BAÑO.",
    "VENTANAS HACIA P1 DESFASADAS ENTRE SUITE Y COCINA-COMEDOR PARA REDUCIR VISUALES CRUZADAS.",
    "COLUMNAS SOBRE EL EJE C SEGÚN LÁMINA A2; SECCIONES Y REFUERZO SEGÚN PLANOS ESTRUCTURALES.",
    "DIMENSIONES Y TIPOS DE PUERTAS Y VENTANAS EN LÁMINA A8.",
]
cl.mtext(psp, "\\P".join(cl.notas(extra)), (X3, y - 6), 2.1, 250, attach=1)
H.extractor_detail(psp, X3, 160.0)

H.titleblock(doc, psp, "A3", "PLANTA NIVEL 2",
             ["SUITE 1, COCINA-COMEDOR, SALA.", "DERROTERO.", "CUADRO DE ÁREAS.",
              "PORCENTAJE DE COBERTURA.", "DETALLE EXTRACTOR DE AIRE.", "NOTAS."],
             [("0", "06-10-2026", "VERSIÓN DE TRABAJO PARA REVISIÓN")])

OUT.mkdir(parents=True, exist_ok=True)
doc.saveas(OUT / f"{NAME}.dxf")
cl.render_pdf(doc, "A3-NIVEL2", OUT / f"{NAME}.pdf")
print("suite", round(A_SUI, 2), "baño", round(A_BA, 2), "walk-in", round(A_WI, 2), "cocina",
      round(A_COC, 2), "sala", round(A_SAL, 2), "pasillo", round(A_PAS, 2), "gradas",
      round(A_GRA, 2), "| N2", round(H.A_HUELLA, 2))
print("DXF:", OUT / f"{NAME}.dxf")
