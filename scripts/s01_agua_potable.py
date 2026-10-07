"""Lámina S01 - AGUA POTABLE: plantas N1, N2 y N3 a 1:100, diagrama vertical, detalles y notas.

Decisiones del usuario (06-10-2026): conexión directa a la red de la ESPH sin tanque ni bomba;
agua caliente solo en duchas desde el calentador de paso de cada baño (E02/E03); diámetros,
llaves y notas de la referencia (RIVERGRAND IS1-IS3) [PR]: acometida y montante 3/4",
ramales y salidas 1/2", llave de paso por baño. Base: A2 rev3, A3 rev4 y A4 rev4 aprobadas.
"""
import cadlib as cl
import hoja as H
import sanit as S

REV = "rev1"
OUT = cl.ROOT / "planos" / "S01_agua_potable"
NAME = f"SR-S01_AGUA_POTABLE_{REV}"
LAYOUT = "S01-AGUA"
MX, MY = 4.75, 17.30                               # montante AF en el muro del eje C (escalera/P2)
YM = 2.21 + 25.03                                  # reflejo suite 1 -> suite 3

doc = cl.new_doc()
msp = doc.modelspace()
S.base(doc, msp, skip_txt=("TANQUE SÉPTICO",))


def bano_fachada(L, mirror, entrada):
    """Baño de suite 1 (o suite 3 en espejo): llave, LM, WC y ducha con calentador de paso."""
    m = (lambda y: YM - y) if mirror else (lambda y: y)
    ex, ey = entrada                                 # punto de llegada del ramal al baño
    L.llave(ex, ey)
    L.pipe([(ex, ey), (5.18, ey), (5.18, m(3.43))])
    L.pipe([(ex, ey), (3.86, ey), (3.86, m(2.60))])
    L.calentador(3.86, m(2.60))
    L.pipe([(3.86, m(2.60)), (4.45, m(2.33))], "S-AC")
    for x, y in ((5.18, m(4.10)), (5.18, m(3.43)), (4.45, m(2.33))):
        L.salida(x, y)
    L.label("LM 1/2\"", 5.18, m(4.10), *((0.30, 0.45) if not mirror else (0.75, 0.15)))
    L.label("WC 1/2\"", 5.18, m(3.43), 0.30, 0.0)
    L.label("DUCHA 1/2\" (AC)", 4.45, m(2.33), 0.45, -0.70 if not mirror else 0.70)
    L.label("CALENTADOR DE PASO", 3.86, m(2.60), -0.45, -0.75 if not mirror else 0.75)
    L.label("LLAVE DE PASO 1/2\"", ex, ey, -0.50, 0.55 if not mirror else -0.55)


# ================================================================ nivel 1
N1 = S.Lv(msp, "N1")
N1.medidor(0.75, 0.35)
N1.llave(0.75, 0.80)
N1.pipe([(0.75, -1.20), (0.75, 0.20)])
N1.pipe([(0.75, 0.50), (0.75, 2.40), (1.10, 2.60), (1.10, MY), (MX, MY)])
N1.label("ACOMETIDA ESPH 3/4\"", 0.75, -0.80, 1.10, 0.0)
N1.label("MEDIDOR (SEGÚN ESPH)", 0.75, 0.35, 1.40, 0.0)
N1.label("LLAVE DE PASO 3/4\"", 0.75, 0.80, 1.90, 0.0)
N1.text("AF 3/4\" BAJO CONTRAPISO", 1.20, 9.00, S.TH)
N1.montante(MX, MY)
N1.label("MONTANTE AF 3/4\" (N1 A N3)", MX, MY, 0.55, 0.60)
# puntos de jardín
N1.pipe([(0.75, 1.30), (8.40, 1.30)])
N1.salida(8.40, 1.30)
N1.label("PUNTO DE JARDÍN 1/2\"", 8.40, 1.30, -0.45, 0.60)
JP = (1.50, 25.40)                                 # punto de jardín posterior (rev1: fuera del tanque séptico)
N1.pipe([(MX, MY), (MX, 25.30), (JP[0], 25.30), JP])
N1.salida(*JP)
N1.label("PUNTO DE JARDÍN 1/2\"", *JP, 0.90, -0.45)
N1.text("PATIO POSTERIOR - JARDÍN SECO", 4.50, 26.50, 0.13, "MIDDLE_CENTER", rot=90.0)
N1.text("TANQUE SÉPTICO Y DRENAJE: VER S02", 4.50, 26.85, 0.13, "MIDDLE_CENTER", rot=90.0)
N1.text("AF 1/2\" ENTERRADA", MX + 0.30, 22.40, S.TH)

# ================================================================ nivel 2
N2 = S.Lv(msp, "N2")
N2.montante(MX, MY)
N2.label("MONTANTE AF 3/4\"", MX, MY, 0.45, -0.70)
N2.pipe([(MX, MY), (MX, 16.70), (6.80, 16.70)])
N2.llave(6.20, 16.70)
N2.salida(6.80, 16.70)
N2.label("LP 1/2\" (FREGADERO)", 6.80, 16.70, 0.60, -0.55)
N2.label("LLAVE DE PASO 1/2\"", 6.20, 16.70, -0.50, 1.00)
N2.pipe([(MX, 16.70), (1.00, 16.70), (1.00, 4.55), (3.85, 4.55)])
N2.text("AF 1/2\" POR ENTREPISO", 1.10, 12.40, S.TH)
bano_fachada(N2, False, (3.85, 4.55))

# ================================================================ nivel 3
N3 = S.Lv(msp, "N3")
N3.montante(MX, MY)
N3.label("MONTANTE AF 3/4\"", MX, MY, 0.95, 0.40)
# suite 2 (baño sobre la cocina)
N3.pipe([(MX, MY), (MX, 16.45), (7.45, 16.45)])
N3.llave(7.05, 16.45)
N3.pipe([(7.45, 16.45), (7.45, 15.30), (8.72, 15.30), (8.72, 15.60)])
N3.pipe([(8.72, 15.30), (8.72, 14.93)])
N3.pipe([(7.45, 16.45), (7.45, 16.58)])
N3.calentador(7.45, 16.60)
N3.pipe([(7.45, 16.60), (8.10, 16.72)], "S-AC")
for x, y in ((8.72, 15.60), (8.72, 14.93), (8.10, 16.72)):
    N3.salida(x, y)
N3.label("WC 1/2\"", 8.72, 15.60, -0.40, 0.45)
N3.label("LM 1/2\"", 8.72, 14.93, -0.40, -0.45)
N3.label("DUCHA 1/2\" (AC)", 8.10, 16.72, -0.75, 0.55)
N3.label("CALENTADOR DE PASO", 7.45, 16.60, -1.00, 1.10)
N3.label("LLAVE DE PASO 1/2\"", 7.05, 16.45, -1.00, 1.25)
# suite 1 (por la suite 2 y el pasillo)
N3.pipe([(MX, 16.45), (1.00, 16.45), (1.00, 4.55), (3.85, 4.55)])
N3.text("AF 1/2\" POR ENTREPISO", 1.10, 12.40, S.TH)
bano_fachada(N3, False, (3.85, 4.55))
# suite 3 (por el muro del eje C)
N3.pipe([(MX, MY), (MX, 23.00)])
bano_fachada(N3, True, (MX, 23.00))

# ================================================================ hoja
psp = doc.layouts.new(LAYOUT)
psp.page_setup(size=(cl.A1_W, cl.A1_H), margins=(0, 0, 0, 0), units="mm")
doc.layouts.set_active_layout(LAYOUT)
cl.frame(psp)


def vp(center, size, scale, mc):
    v = psp.add_viewport(center=center, size=size, view_center_point=mc,
                         view_height=size[1] * scale / 1000.0, dxfattribs={"layer": "A-VIEWPORT"})
    v.dxf.flags = v.dxf.flags | 16384


PX = 186.0
for lv, yc, title in (("N3", 512.0, "AGUA POTABLE - NIVEL 3"), ("N2", 362.0, "AGUA POTABLE - NIVEL 2"),
                      ("N1", 212.0, "AGUA POTABLE - NIVEL 1")):
    vp((PX, yc), (316.0, 136.0), 100, (14.8, 3.75 + S.OFF[lv]))
    cl.text(psp, title, (30.0, yc - 68.0), 4.5, "A-TITULOS", "TOP_LEFT")
    cl.text(psp, "Esc. 1:100", (30.0, yc - 74.5), 2.5, "A-TEXTO", "TOP_LEFT")


def L(a, b, layer="S-AF"):
    psp.add_line(a, b, dxfattribs={"layer": layer})


def T(s, p, h=1.8, al="MIDDLE_LEFT"):
    cl.text(psp, s, p, h, "A-TEXTO", al)


# ---------------------------------------------------------------- diagrama vertical (esquemático)
X0 = 360.0
cl.text(psp, "DIAGRAMA VERTICAL DE AGUA POTABLE (ESQUEMÁTICO)", (X0, 575.0), 3.5, "A-TITULOS", "TOP_LEFT")
k = 11.0                                           # mm por metro de altura
yb = 470.0
xm = X0 + 70.0
for z, lab in ((0, "N1 ±0.00"), (3, "N2 +3.00"), (6, "N3 +6.00")):
    psp.add_line((X0, yb + z * k), (X0 + 330, yb + z * k), dxfattribs={"layer": "S-FINO"})
    T(lab, (X0, yb + z * k + 2.0), 1.8)
L((xm, yb - 6), (xm, yb + 6 * k + 4 + 2 * 5.5))
T("MONTANTE AF 3/4\"", (xm - 2, yb + 4.5 * k), 1.8, "MIDDLE_RIGHT")
L((X0 + 5, yb - 6), (xm, yb - 6))
S.leyenda_simbolo(psp, "MED", X0 + 14, yb - 6)
S.leyenda_simbolo(psp, "LL", X0 + 26, yb - 6)
T("ACOMETIDA ESPH, MEDIDOR Y LLAVE 3/4\"", (X0 + 4, yb - 11), 1.7)
ramas = [(0, ["PUNTO DE JARDÍN FRONTAL 1/2\"", "PUNTO DE JARDÍN POSTERIOR 1/2\""]),
         (3, ["COCINA: LP 1/2\"", "BAÑO SUITE 1: LM, WC, DUCHA + CP"]),
         (6, ["BAÑO SUITE 1: LM, WC, DUCHA + CP", "BAÑO SUITE 2: LM, WC, DUCHA + CP",
              "BAÑO SUITE 3: LM, WC, DUCHA + CP"])]
for z, items in ramas:
    for i, txt in enumerate(items):
        yy = yb + z * k + 4 + i * 5.5
        L((xm, yy), (xm + 40, yy))
        S.leyenda_simbolo(psp, "LL", xm + 12, yy)
        T(txt, (xm + 42, yy), 1.7)
T("CP: CALENTADOR DE PASO ELÉCTRICO (240 V, VER E02 Y E03); AGUA CALIENTE SOLO EN DUCHAS.",
  (X0, yb - 18), 1.7)

# ---------------------------------------------------------------- detalles
Y1 = 425.0
cl.text(psp, "DETALLE 1 - ACOMETIDA Y MEDIDOR [PR]", (X0, Y1), 3.0, "A-TITULOS", "TOP_LEFT")
cl.text(psp, "S/E", (X0, Y1 - 5), 2.0, "A-TEXTO", "TOP_LEFT")
yd = Y1 - 35
L((X0 + 5, yd), (X0 + 150, yd), "S-DET")                 # terreno
psp.add_lwpolyline([(X0 + 40, yd), (X0 + 40, yd - 14), (X0 + 80, yd - 14), (X0 + 80, yd)],
                   dxfattribs={"layer": "S-DET"})
L((X0 + 10, yd - 10), (X0 + 140, yd - 10))
S.leyenda_simbolo(psp, "MED", X0 + 52, yd - 10)
S.leyenda_simbolo(psp, "LL", X0 + 68, yd - 10)
T("RED ESPH", (X0 + 8, yd - 6), 1.7)
T("CAJA DE MEDIDOR SEGÚN ESPH (PD)", (X0 + 40, yd + 4), 1.7)
T("LLAVE DE PASO 3/4\"", (X0 + 84, yd - 6), 1.7)
T("AF 3/4\" A LA VIVIENDA", (X0 + 108, yd - 14), 1.7)

X2 = X0 + 175
cl.text(psp, "DETALLE 2 - CALENTADOR DE PASO EN DUCHA", (X2, Y1), 3.0, "A-TITULOS", "TOP_LEFT")
cl.text(psp, "ELEVACIÓN - S/E", (X2, Y1 - 5), 2.0, "A-TEXTO", "TOP_LEFT")
yf = Y1 - 70
L((X2 + 10, yf), (X2 + 150, yf), "S-DET")                 # piso
L((X2 + 20, yf), (X2 + 20, yf + 55), "S-DET")             # pared
L((X2 + 60, yf), (X2 + 60, yf + 40))                      # AF sube
S.leyenda_simbolo(psp, "LL", X2 + 60, yf + 20)
S.leyenda_simbolo(psp, "CP", X2 + 60, yf + 44)
e = psp.add_line((X2 + 62.2, yf + 44), (X2 + 90, yf + 44), dxfattribs={"layer": "S-AC"})
e.dxf.ltscale = 0.4
psp.add_line((X2 + 90, yf + 44), (X2 + 90, yf + 38), dxfattribs={"layer": "S-AC"})
psp.add_circle((X2 + 90, yf + 36), 2.0, dxfattribs={"layer": "S-ACC"})
T("AF 1/2\"", (X2 + 62, yf + 8), 1.7)
T("LLAVE DE PASO 1/2\"", (X2 + 64, yf + 20), 1.7)
T("CALENTADOR DE PASO 240 V", (X2 + 30, yf + 51), 1.7)
T("AC A LA REGADERA", (X2 + 93, yf + 36), 1.7)
cl.mtext(psp, "ALTURA, CONEXIÓN HIDRÁULICA Y ELÉCTRICA SEGÚN EL FABRICANTE DEL EQUIPO; "
         "CIRCUITO SEGÚN E02/E03.", (X2 + 10, yf - 4), 1.7, 150, layer="A-TEXTO", attach=1)

# ---------------------------------------------------------------- simbología y notas
yS = 290.0
y = S.cuadro_simbologia(psp, X0, yS, [
    ("AF", "TUBERÍA DE AGUA FRÍA (PVC A PRESIÓN) [PR]"),
    ("AC", "TUBERÍA DE AGUA CALIENTE (CPVC), SOLO DUCHAS"),
    ("LL", "LLAVE DE PASO"),
    ("SAL", "SALIDA A APARATO (DIÁMETRO INDICADO)"),
    ("MON", "MONTANTE"),
    ("MED", "MEDIDOR DE AGUA (SEGÚN ESPH)"),
    ("CP", "CALENTADOR DE PASO ELÉCTRICO")], w_txt=125.0, row_h=6.0, title="SIMBOLOGÍA")
cl.text(psp, "LM: LAVATORIO; WC: INODORO; LP: FREGADERO; AF / AC: AGUA FRÍA / CALIENTE.",
        (X0, y - 2.5), 1.8, "A-TEXTO", "TOP_LEFT")
X3 = X0 + 155
cl.text(psp, "NOTAS:", (X3, yS), 3.5, "A-TITULOS", "TOP_LEFT")
notas = [
    "TODAS LAS MEDIDAS ESTÁN DADAS EN METROS, SALVO ALGUNA EXCEPCIÓN INDICADA. [PR]",
    "EL AGUA POTABLE PROVIENE DEL SISTEMA PÚBLICO (ESPH), DIRECTAMENTE DE LA CONEXIÓN DE LA "
    "CALLE, SIN TANQUE DE ALMACENAMIENTO NI EQUIPO DE BOMBEO. [PR]",
    "UBICACIÓN Y CARACTERÍSTICAS DEL MEDIDOR Y DE LA CAJA SEGÚN LA ESPH (PD).",
    "DIÁMETROS DE LA REFERENCIA [PR]: ACOMETIDA, TRAMO PRINCIPAL Y MONTANTE 3/4\"; RAMALES Y "
    "SALIDAS 1/2\". LLAVE DE PASO EN CADA BAÑO Y EN LA COCINA.",
    "AGUA CALIENTE ÚNICAMENTE EN LAS DUCHAS, MEDIANTE UN CALENTADOR DE PASO ELÉCTRICO POR BAÑO "
    "(CIRCUITOS EN E02 Y E03).",
    "TUBERÍA DE AGUA FRÍA PVC A PRESIÓN Y DE AGUA CALIENTE CPVC; CLASE O SDR SEGÚN CÁLCULO (PD).",
    "EL MONTANTE SUBE EMBEBIDO EN EL MURO DEL EJE C (ESCALERA / PATIO P2); LOS RAMALES DE LOS "
    "NIVELES 2 Y 3 VIAJAN POR EL ENTREPISO.",
    "PROBAR LA RED A PRESIÓN ANTES DE CERRAR PAREDES Y CIELOS (PD).",
]
cl.notes_block(psp, X3, yS - 6, [f"{i}.- {t}" for i, t in enumerate(notas, 1)] + [cl.NOTA_PR], 1.9, 190)

H.titleblock(doc, psp, "S01", "AGUA POTABLE",
             ["PLANTAS NIVELES 1, 2 Y 3.", "DIAGRAMA VERTICAL.", "DETALLES.", "SIMBOLOGÍA.",
              "NOTAS.", ""],
             [("0", "06-10-2026", "VERSIÓN DE TRABAJO PARA REVISIÓN"),
              ("1", "07-10-2026", "PUNTO DE JARDÍN POSTERIOR TRASLADADO (S02)")], escalas="1:100 / S/E")

OUT.mkdir(parents=True, exist_ok=True)
doc.saveas(OUT / f"{NAME}.dxf")
cl.render_pdf(doc, LAYOUT, OUT / f"{NAME}.pdf")
print("DXF:", OUT / f"{NAME}.dxf")
