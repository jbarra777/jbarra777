"""Lámina S02 - AGUAS RESIDUALES: plantas N1, N2 y N3 a 1:100, tanque séptico con FAFA, drenaje,
caja de registro, trampa de grasa, baño típico, simbología y notas.

Decisiones del usuario (06-10-2026): no hay alcantarillado; tanque séptico y drenaje en el patio
posterior, esquema y dimensiones de la referencia (RIVERGRAND IS4-IS6), sujetos a la prueba de
infiltración y al cálculo. Bajantes según la propuesta aprobada: suite 1 en el muro baño/walk-in con
colector colgado bajo la losa del N2 hasta C2; suite 2 y fregadero en un ducto en la esquina D/4 de la
cocina; suite 3 en un ducto junto a C6 en la sala. Aguas negras 4" y grises 2" separadas.
Base: A2 rev3, A3 rev4 y A4 rev4 aprobadas. Placas F1/F2 de 1,65 m y VA1 según C01 (se evitan).
"""
import cadlib as cl
import hoja as H
import sanit as S

REV = "rev2"
OUT = cl.ROOT / "planos" / "S02_aguas_residuales"
NAME = f"SR-S02_AGUAS_RESIDUALES_{REV}"
LAYOUT = "S02-AGUAS-RESIDUALES"
YM = 2.21 + 25.03                                  # reflejo suite 1 -> suite 3
XG, XN = 6.00, 6.60                                # colectores enterrados: grises / negras
TY = 26.64                                         # eje del tanque en el patio (y 26.00-27.28)

doc = cl.new_doc()
msp = doc.modelspace()
S.base(doc, msp, skip_txt=("TANQUE SÉPTICO",))


def bano_suite(L, mirror, bn, bg, label=True):
    """Ramales del baño de la suite 1 (o 3 en espejo) hacia las bajantes bn (AN) y bg (AG)."""
    m = (lambda y: YM - y) if mirror else (lambda y: y)
    wc, sp, lm = (4.95, m(3.43)), (4.50, m(2.64)), (5.15, m(4.05))
    L.pipe([wc, bn], "S-AN")
    L.pipe([sp, bg], "S-AJ")
    L.pipe([lm, (5.30, m(3.88)), (5.30, bg[1] + (0.15 if mirror else -0.15)), bg], "S-AJ")
    L.coladera(*sp)
    for p in (wc, lm):
        L.salida(*p)
    if label:
        s = -1 if mirror else 1
        L.label("WC 4\"", *wc, -0.55, 0.0)
        L.label("SP 2\"", *sp, -0.45, -0.55 * s)
        L.label("LM 2\"", *lm, 0.45, 0.45 * s)


# ================================================================ nivel 3
N3 = S.Lv(msp, "N3")
# suite 1: bajantes en el forro del muro baño / walk-in
BN1, BG1 = (5.45, 3.55), (5.45, 2.85)
bano_suite(N3, False, BN1, BG1)
N3.bajante(*BN1, "S-AN")
N3.bajante(*BG1, "S-AJ")
N3.label("VENT. 2\"", 5.45, 3.20, 0.75, 0.10)
# suite 3: bajantes en el ducto junto a C6
BN3, BG3 = (5.14, 24.73), (5.14, 24.93)
bano_suite(N3, True, BN3, BG3)
N3.bajante(*BN3, "S-AN")
N3.bajante(*BG3, "S-AJ")
N3.label("VENT. 2\"", 5.14, 24.83, 1.06, -0.43)
# suite 2: piezas sobre el muro D, bajantes en la esquina D/4
BN2, BG2 = (8.70, 16.53), (8.70, 16.73)
wc2, sp2, lm2 = (8.55, 15.60), (8.10, 16.40), (8.65, 14.95)
N3.pipe([wc2, BN2], "S-AN")
N3.pipe([sp2, BG2], "S-AJ")
N3.pipe([lm2, (8.80, 15.10), (8.80, 16.60), BG2], "S-AJ")
N3.coladera(*sp2)
for p in (wc2, lm2):
    N3.salida(*p)
N3.bajante(*BN2, "S-AN")
N3.bajante(*BG2, "S-AJ")
N3.label("WC 4\"", *wc2, -1.10, 0.15)
N3.label("LM 2\"", *lm2, -0.45, -0.45)
N3.label("SP 2\"", *sp2, -0.30, 0.80)
N3.label("VENT. 2\"", 8.70, 16.63, -0.30, 0.90)

# ================================================================ nivel 2
N2 = S.Lv(msp, "N2")
bano_suite(N2, False, BN1, BG1)
N2.rect(5.39, 2.65, 5.60, 3.75, "S-FINO")                      # forro del muro (walk-in)
N2.bajante(*BN1, "S-AN")
N2.bajante(*BG1, "S-AJ")
# ducto de la cocina (suite 2 + fregadero)
N2.rect(8.55, 16.43, 8.85, 16.83, "S-ACC")
N2.bajante(*BN2, "S-AN")
N2.bajante(*BG2, "S-AJ")
fr = (6.80, 16.55)
N2.pipe([fr, (8.40, 16.55), (8.55, 16.73), BG2], "S-AJ")
N2.salida(*fr)
N2.label("LP 2\"", *fr, -0.40, 0.85)
N2.label("DUCTO 0.30 x 0.40", 8.55, 16.50, -0.75, -0.80)
# ducto de la sala (suite 3)
N2.rect(4.99, 24.63, 5.29, 25.03, "S-ACC")
N2.bajante(*BN3, "S-AN")
N2.bajante(*BG3, "S-AJ")
N2.label("DUCTO 0.30 x 0.40", 5.14, 24.63, -0.30, -1.40)

# ================================================================ nivel 1
N1 = S.Lv(msp, "N1")
# suite 1: colectores colgados bajo la losa del N2 y bajada junto a C2
D1N, D1G = (5.10, 7.45), (5.10, 7.92)
N1.pipe([BN1, (5.45, 7.40), D1N], "S-AN")
N1.pipe([BG1, (5.70, 3.05), (5.70, 7.92), D1G], "S-AJ")
N1.bajante(*BN1, "S-AN")
N1.bajante(*BG1, "S-AJ")
N1.bajante(*D1N, "S-AN")
N1.bajante(*D1G, "S-AJ")
N1.text("COLECTORES AN / AG COLGADOS", 6.40, 2.55, S.TH)
N1.text("BAJO LA LOSA DEL N2, CON FORRO", 6.15, 2.55, S.TH)
N1.label("BAJAN JUNTO A C2", 5.10, 7.45, -0.75, -0.55)
CR1G, CR1N = (XG, 8.10), (XN, 8.10)
N1.pipe([D1N, (XN, 7.45), (XN, 7.875)], "S-AN")
N1.pipe([D1G, (XG - 0.225, 8.10)], "S-AJ")
# suite 2: bajantes en la esquina D/4
CR2N, CR2G = (7.05, 16.30), (7.05, 17.40)
N1.bajante(*BN2, "S-AN")
N1.bajante(*BG2, "S-AJ")
N1.pipe([BN2, (7.275, 16.40)], "S-AN")
N1.pipe([BG2, (7.275, 17.40)], "S-AJ")
N1.pipe([(6.825, 16.30), (XN, 16.30)], "S-AN")
N1.pipe([(6.825, 17.40), (XG, 17.40)], "S-AJ")
N1.label("BAJANTES SUITE 2 Y FREGADERO", 8.70, 16.63, -0.95, 1.10)
# suite 3: bajantes junto a C6
CR3G, CR3N = (XG, 24.40), (XN, 24.40)
N1.bajante(*BN3, "S-AN")
N1.bajante(*BG3, "S-AJ")
N1.pipe([BG3, (XG - 0.225, 24.50)], "S-AJ")
N1.pipe([BN3, (5.40, 24.05), (6.45, 24.05), (6.45, 24.175)], "S-AN")
N1.label("BAJANTES SUITE 3 (JUNTO A C6)", 5.14, 24.83, -1.44, -0.23)
# trampa de grasa en el colector de aguas grises
TG = (XG, 23.20)
N1.rect(TG[0] - 0.42, TG[1] - 0.42, TG[0] + 0.42, TG[1] + 0.42, "S-ACC")
N1.rect(TG[0] - 0.30, TG[1] - 0.30, TG[0] + 0.30, TG[1] + 0.30, "S-FINO")
N1.text("TG", TG[0], TG[1], 0.12, "MIDDLE_CENTER")
N1.label("TG (DET. 1 Y 3)", TG[0] - 0.42, TG[1] - 0.20, -0.58, -0.70)
# colectores principales
N1.pipe([(XN, 8.325), (XN, 16.30), (XN, 24.175)], "S-AN")
N1.pipe([(XG, 8.325), (XG, 17.40), (XG, TG[1] - 0.42)], "S-AJ")
N1.pipe([(XG, TG[1] + 0.42), (XG, 24.175)], "S-AJ")
for c in (CR1G, CR1N, CR2N, CR2G, CR3G, CR3N):
    N1.caja(*c)
N1.text("COLECTOR AN 4\" (PVC SDR-26)", XN + 0.20, 9.00, S.TH)
N1.text("COLECTOR AG 4\" (PVC SDR-26)", XG - 0.25, 9.00, S.TH)
# patio posterior: CR de entrada, tanque, cilindro, FAFA, CR de distribución y drenaje
CRU, CRD = (7.80, TY), (0.80, 27.85)
N1.pipe([(XN, 24.625), (XN, 25.30), (7.90, 25.55), (7.90, TY - 0.225)], "S-AN")
N1.pipe([(XG, 24.625), (XG, 25.40), (7.70, 25.70), (7.70, TY - 0.225)], "S-AJ")
N1.caja(*CRU)
N1.caja(*CRD)
N1.pipe([(CRU[0] - 0.225, TY), (7.24, TY)], "S-AN")
N1.rect(5.00, 26.00, 7.24, 27.28)                               # tanque (exterior)
N1.rect(5.12, 26.12, 7.12, 27.16, "S-FINO")
N1.rect(5.67, 26.12, 5.79, 27.16, "S-FINO")                     # división 2/3 - 1/3
for t, yy in (("TANQUE", 26.38), ("SÉPTICO", 26.62), ("(DET. 1)", 26.90)):
    N1.text(t, 6.45, yy, 0.12, "MIDDLE_CENTER", rot=90.0)
q = N1.Q(4.65, TY)
msp.add_circle(q, 0.25, dxfattribs={"layer": "S-ACC"})          # cilindro de inspección
N1.pipe([(5.00, TY), (4.90, TY)], "S-AN")
N1.pipe([(4.40, TY), (4.24, TY)], "S-AN")
N1.rect(3.20, 26.00, 4.24, 27.28)                               # FAFA
N1.rect(3.32, 26.12, 4.12, 27.16, "S-FINO")
N1.text("FAFA", 3.72, TY, 0.13, "MIDDLE_CENTER", rot=90.0)
N1.text("CI", 4.65, TY, 0.12, "MIDDLE_CENTER")
N1.pipe([(3.20, TY), (CRD[0], TY), (CRD[0], CRD[1] - 0.225)], "S-AN")
N1.rect(CRD[0] + 0.225, 27.60, 8.40, 28.10, "S-FINO")           # zanja de drenaje
N1.pipe([(CRD[0] + 0.225, CRD[1]), (8.40, CRD[1])], "S-AN")
N1.text("DRENAJE: TUBO PERFORADO 4\" EN ZANJA 0.50, L = 7.40 - DET. 2", 1.25, 27.44, 0.12,
        rot=90.0)
N1.text("PATIO POSTERIOR - JARDÍN SECO", 0.35, 25.45, 0.13, rot=90.0)

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
for lv, yc, title in (("N3", 512.0, "AGUAS RESIDUALES - NIVEL 3"), ("N2", 362.0, "AGUAS RESIDUALES - NIVEL 2"),
                      ("N1", 212.0, "AGUAS RESIDUALES - NIVEL 1")):
    vp((PX, yc), (316.0, 136.0), 100, (14.8, 3.75 + S.OFF[lv]))
    cl.text(psp, title, (30.0, yc - 68.0), 4.5, "A-TITULOS", "TOP_LEFT")
    cl.text(psp, "Esc. 1:100", (30.0, yc - 74.5), 2.5, "A-TEXTO", "TOP_LEFT")


def L(a, b, layer="S-DET"):
    return psp.add_line(a, b, dxfattribs={"layer": layer})


def R(x0, y0, x1, y1, layer="S-DET"):
    return psp.add_lwpolyline([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], close=True,
                              dxfattribs={"layer": layer})


def T(s, p, h=1.7, al="MIDDLE_LEFT"):
    cl.text(psp, s, p, h, "A-TEXTO", al)


def hatch(pts, pattern="ANSI31", sc=0.6):
    h = psp.add_hatch(color=8, dxfattribs={"layer": "S-FINO"})
    h.set_pattern_fill(pattern, scale=sc)
    h.paths.add_polyline_path(pts)


def dim_h(x0, x1, y, txt, tick=1.2):
    L((x0, y), (x1, y), "S-FINO")
    for x in (x0, x1):
        L((x - tick * 0.5, y - tick * 0.5), (x + tick * 0.5, y + tick * 0.5), "S-FINO")
        L((x, y - tick), (x, y + tick), "S-FINO")
    T(txt, ((x0 + x1) / 2, y + 1.3), 1.6, "BOTTOM_CENTER")


def dim_v(x, y0, y1, txt, tick=1.2, side=1):
    L((x, y0), (x, y1), "S-FINO")
    for y in (y0, y1):
        L((x - tick * 0.5, y - tick * 0.5), (x + tick * 0.5, y + tick * 0.5), "S-FINO")
        L((x - tick, y), (x + tick, y), "S-FINO")
    T(txt, (x + 1.3 * side, (y0 + y1) / 2), 1.6, "MIDDLE_LEFT" if side > 0 else "MIDDLE_RIGHT")


def leader(a, b, s, h=1.6):
    L(a, b, "S-FINO")
    T(s, (b[0] + (1.0 if b[0] >= a[0] else -1.0), b[1]), h, "MIDDLE_LEFT" if b[0] >= a[0] else "MIDDLE_RIGHT")


# ---------------------------------------------------------------- detalle 1: tanque séptico + FAFA
# Presentación según la referencia (IS4): vista superior y vista lateral con trampa de grasa, tanque de
# dos cámaras en bloque, cilindro de inspección y FAFA. Niveles según las notas 11 y 12.
k = 100.0 / 3.0                                    # 1:30
X0 = 384.0
cl.text(psp, "DETALLE 1 - TANQUE SÉPTICO", (362.0, 580.0), 3.0, "A-TITULOS", "TOP_LEFT")
cl.text(psp, "Esc. 1:30 - COTAS EN METROS", (362.0, 575.5), 2.0, "A-TEXTO", "TOP_LEFT")


def U(u):
    return X0 + u * k


def arrow(p, d, size=1.6, layer="S-DET"):
    """Flecha de flujo: punta en p, dirección d = (dx, dy) unitaria."""
    dx, dy = d
    b = (p[0] - dx * size, p[1] - dy * size)
    h = psp.add_hatch(color=7, dxfattribs={"layer": layer})
    h.paths.add_polyline_path([p, (b[0] - dy * size * 0.3, b[1] + dx * size * 0.3),
                               (b[0] + dy * size * 0.3, b[1] - dx * size * 0.3)])


def tubo(x0, y0, x1, y1, layer="S-DET"):
    """Tubería dibujada a doble línea (rectángulo)."""
    R(min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1), layer)


def bloques_h(x0, x1, y0, y1, paso=0.40):
    """Muro de bloque visto en planta: tramado y juntas cada 'paso' (m)."""
    hatch([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], "ANSI37", 0.35)
    R(x0, y0, x1, y1)
    n = int(round(abs(x1 - x0) / (paso * k)))
    for i in range(1, max(n, 1)):
        L((x0 + (x1 - x0) * i / n, y0), (x0 + (x1 - x0) * i / n, y1), "S-FINO")


def bloques_v(x0, x1, y0, y1, paso=0.20):
    """Muro de bloque en elevación/planta vertical: tramado y juntas cada 'paso' (m)."""
    hatch([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], "ANSI37", 0.35)
    R(x0, y0, x1, y1)
    n = int(round(abs(y1 - y0) / (paso * k)))
    for i in range(1, max(n, 1)):
        L((x0, y0 + (y1 - y0) * i / n), (x1, y0 + (y1 - y0) * i / n), "S-FINO")


def tapa_planta(uc, vc, a=0.36):
    x0, x1, y0, y1 = U(uc - a / 2), U(uc + a / 2), Vt(vc - a / 2), Vt(vc + a / 2)
    hatch([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], "ANSI31", 0.8)
    R(x0, y0, x1, y1, "S-FINO")
    psp.add_lwpolyline([(U(uc - 0.11), Vt(vc + 0.04)), (U(uc + 0.11), Vt(vc + 0.04)),
                        (U(uc + 0.11), Vt(vc + 0.07)), (U(uc - 0.11), Vt(vc + 0.07))], close=True,
                       dxfattribs={"layer": "S-DET", "const_width": 0.0})
    h = psp.add_hatch(color=7, dxfattribs={"layer": "S-DET"})
    h.paths.add_polyline_path([(U(uc - 0.11), Vt(vc + 0.04)), (U(uc + 0.11), Vt(vc + 0.04)),
                               (U(uc + 0.11), Vt(vc + 0.07)), (U(uc - 0.11), Vt(vc + 0.07))])


# geometría a lo largo del flujo (u, m): trampa, tanque, cilindro y FAFA
TG0, TG1 = 0.00, 0.76                              # trampa (0.60 interior + bordes)
TQ0, TQ1 = 1.05, 3.29                              # tanque: interior 2.00 + muros 0.12
DV0, DV1 = TQ0 + 0.12 + 1.33, TQ0 + 0.12 + 1.45    # división 2/3 - 1/3
CI = 3.62                                          # cilindro de inspección (eje)
FA0, FA1 = 3.95, 4.99                              # FAFA: interior 0.80 + muros 0.12

# ------------------------------------------------ vista superior
V0 = 516.0


def Vt(v):
    return V0 + v * k


cl.text(psp, "VISTA SUPERIOR", (362.0, 569.0), 2.2, "A-TEXTO", "TOP_LEFT")
R(U(-0.22), Vt(-0.10), U(5.12), Vt(1.38), "S-FINO")                  # área de instalación
T("ÁREA DE INSTALACIÓN", (U(-0.15), Vt(1.38) + 1.4), 1.3)
# trampa de grasa
R(U(TG0), Vt(0.26), U(TG1), Vt(1.02))
tapa_planta((TG0 + TG1) / 2, 0.64, 0.68)
T("TRAMPA DE", (U(0.38), Vt(0.86)), 1.4, "MIDDLE_CENTER")
T("GRASA", (U(0.38), Vt(0.78)), 1.4, "MIDDLE_CENTER")
# tanque
for a, b in ((TQ0, TQ1),):
    bloques_h(U(a), U(b), Vt(1.16), Vt(1.28))
    bloques_h(U(a), U(b), Vt(0.00), Vt(0.12))
bloques_v(U(TQ0), U(TQ0 + 0.12), Vt(0.12), Vt(1.16), 0.26)
bloques_v(U(TQ1 - 0.12), U(TQ1), Vt(0.12), Vt(1.16), 0.26)
bloques_v(U(DV0), U(DV1), Vt(0.12), Vt(1.16), 0.26)
tapa_planta(1.83, 0.92)
tapa_planta(2.89, 0.92)
for ut in (1.30, 2.36, 2.73, 3.06):                                    # tees
    psp.add_circle((U(ut), Vt(0.64)), 0.06 * k, dxfattribs={"layer": "S-DET"})
T("CÁMARA 1", (U(1.83), Vt(0.46)), 1.5, "MIDDLE_CENTER")
T("DIGESTIÓN", (U(1.83), Vt(0.36)), 1.5, "MIDDLE_CENTER")
T("(2/3 DEL LARGO)", (U(1.83), Vt(0.26)), 1.3, "MIDDLE_CENTER")
T("CÁMARA 2", (U(2.89), Vt(0.46)), 1.3, "MIDDLE_CENTER")
T("CLARIFICACIÓN", (U(2.89), Vt(0.36)), 1.1, "MIDDLE_CENTER")
T("(1/3 DEL LARGO)", (U(2.89), Vt(0.26)), 1.1, "MIDDLE_CENTER")
# cilindro y FAFA
psp.add_circle((U(CI), Vt(0.64)), 0.25 * k, dxfattribs={"layer": "S-DET"})
psp.add_circle((U(CI), Vt(0.64)), 0.22 * k, dxfattribs={"layer": "S-FINO"})
T("CILINDRO DE", (U(CI), Vt(1.08)), 1.3, "MIDDLE_CENTER")
T("INSPECCIÓN", (U(CI), Vt(1.00)), 1.3, "MIDDLE_CENTER")
bloques_h(U(FA0), U(FA1), Vt(1.16), Vt(1.28))
bloques_h(U(FA0), U(FA1), Vt(0.00), Vt(0.12))
bloques_v(U(FA0), U(FA0 + 0.12), Vt(0.12), Vt(1.16), 0.26)
bloques_v(U(FA1 - 0.12), U(FA1), Vt(0.12), Vt(1.16), 0.26)
tapa_planta(4.47, 0.92)
psp.add_circle((U(4.72), Vt(0.34)), 0.07 * k, dxfattribs={"layer": "S-DET"})    # respiradero
T("FAFA", (U(4.47), Vt(0.52)), 1.5, "MIDDLE_CENTER")
# tuberías (doble línea) y flechas
for a, b in ((-0.55, 0.12), (0.64, TQ0 + 0.20), (TQ1 - 0.20, CI - 0.25), (CI + 0.25, FA0 + 0.18),
             (FA1 - 0.18, 5.45)):
    tubo(U(a), Vt(0.60), U(b), Vt(0.68))
arrow((U(-0.02), Vt(0.64)), (1, 0))
arrow((U(5.45) + 4, Vt(0.64)), (1, 0))
T("ENTRADA", (U(-0.55), Vt(0.64) + 2.4), 1.5)
T("SALIDA", (U(5.18), Vt(0.64) + 2.4), 1.5)
dim_h(U(TQ0 + 0.12), U(TQ1 - 0.12), Vt(1.38) + 3.5, "2.00")
dim_h(U(FA0 + 0.12), U(FA1 - 0.12), Vt(1.38) + 3.5, "0.80")
dim_h(U(TG0 + 0.08), U(TG1 - 0.08), Vt(1.02) + 2.0, "0.60")
dim_v(U(0.92), Vt(0.12), Vt(1.16), "")
cl.text(psp, "1.04", (U(0.92) - 1.4, Vt(0.92)), 1.6, "A-TEXTO", "MIDDLE_CENTER", 90.0)

# ------------------------------------------------ vista lateral (w = 0 terreno)
W0 = 474.0


def Wz(w):
    return W0 + w * k


cl.text(psp, "VISTA LATERAL", (362.0, 506.0), 2.2, "A-TEXTO", "TOP_LEFT")
L((U(-0.60), Wz(0)), (U(5.45), Wz(0)), "S-DET")
T("NIVEL DEL TERRENO", (U(-0.60), Wz(0) + 1.6), 1.3)
# relleno junto al tanque (excavación)
exc = [(U(-0.30), Wz(0)), (U(-0.25), Wz(-0.40)), (U(-0.15), Wz(-0.80)), (U(0.20), Wz(-0.95)),
       (U(0.45), Wz(-1.10)), (U(0.55), Wz(-1.35)), (U(0.85), Wz(-1.55)), (U(TQ0), Wz(-1.70))]
sp = psp.add_spline(exc, dxfattribs={"layer": "S-FINO"})
curva = [(p[0], p[1]) for p in sp.flattening(0.2)]
fill = [(U(-0.30), Wz(0)), (U(TG0), Wz(0)), (U(TG0), Wz(-0.75)), (U(TG1), Wz(-0.75)), (U(TG1), Wz(0)),
        (U(TQ0), Wz(0))] + curva[::-1]
hatch(fill, "CROSS", 0.9)
for a, b in ((TQ1, CI - 0.25), (CI + 0.25, FA0)):                      # relleno entre unidades
    hatch([(U(a), Wz(0)), (U(b), Wz(0)), (U(b), Wz(-1.70)), (U(a), Wz(-1.70))], "CROSS", 0.9)
# trampa de grasa
R(U(TG0), Wz(-0.75), U(TG1), Wz(0))
R(U(TG0 + 0.04), Wz(-0.71), U(TG1 - 0.04), Wz(-0.04), "S-FINO")
T("TRAMPA DE", (U(0.38), Wz(-0.13)), 1.4, "MIDDLE_CENTER")
T("GRASA", (U(0.38), Wz(-0.21)), 1.4, "MIDDLE_CENTER")


def tapa_alzado(uc, a=0.40):
    x0, x1 = U(uc - a / 2), U(uc + a / 2)
    hatch([(x0, Wz(0)), (x1, Wz(0)), (x1, Wz(0.05)), (x0, Wz(0.05))], "ANSI31", 0.8)
    R(x0, Wz(0), x1, Wz(0.05), "S-FINO")
    psp.add_lwpolyline([(U(uc - 0.11), Wz(0.05)), (U(uc - 0.11), Wz(0.13)), (U(uc + 0.11), Wz(0.13)),
                        (U(uc + 0.11), Wz(0.05))], dxfattribs={"layer": "S-DET", "const_width": 0.5})


for uc in (0.38, 1.83, 2.89, 4.47):
    tapa_alzado(uc, 0.70 if uc == 0.38 else 0.40)
# tanque: losa superior, muros de bloque y losa inferior
R(U(TQ0), Wz(-0.10), U(TQ1), Wz(0))
for a, b in ((TQ0, TQ0 + 0.12), (DV0, DV1), (TQ1 - 0.12, TQ1)):
    bloques_v(U(a), U(b), Wz(-1.60), Wz(-0.10))
h = psp.add_hatch(color=7, dxfattribs={"layer": "S-DET"})
h.paths.add_polyline_path([(U(TQ0), Wz(-1.70)), (U(TQ1), Wz(-1.70)), (U(TQ1), Wz(-1.60)), (U(TQ0), Wz(-1.60))])
e = L((U(TQ0 + 0.12), Wz(-0.40)), (U(TQ1 - 0.12), Wz(-0.40)), "S-FINO")
T("NIVEL DE LÍQUIDOS", (U(1.95), Wz(-0.40) + 1.3), 1.3, "MIDDLE_CENTER")


def tee(uc, lado, w_ent):
    """Tee sanitaria: tubo vertical de -0.10 a -0.80 y ramal horizontal hacia 'lado' (-1/+1)."""
    tubo(U(uc - 0.05), Wz(-0.80), U(uc + 0.05), Wz(-0.10))
    x_end = uc + lado * 0.22
    tubo(U(min(uc, x_end)), Wz(w_ent - 0.05), U(max(uc, x_end)), Wz(w_ent + 0.05))


tee(1.30, -1, -0.35)                                                  # entrada
tee(2.36, +1, -0.45)                                                  # paso a cámara 2
tee(2.73, -1, -0.45)
tee(3.06, +1, -0.45)                                                  # salida al cilindro
for ut, sgn in ((1.30, -1), (2.36, +1), (2.73, -1), (3.06, +1)):     # flujo bajo las tees
    L((U(ut), Wz(-0.86)), (U(ut), Wz(-1.04)), "S-FINO")
    arrow((U(ut), Wz(-1.04) if sgn < 0 else Wz(-0.86)), (0, -1) if sgn < 0 else (0, 1), 1.3)
T("CÁMARA 1", (U(1.83), Wz(-1.02)), 1.5, "MIDDLE_CENTER")
T("DIGESTIÓN", (U(1.83), Wz(-1.12)), 1.5, "MIDDLE_CENTER")
T("(2/3 DEL LARGO)", (U(1.83), Wz(-1.22)), 1.3, "MIDDLE_CENTER")
T("CÁMARA 2", (U(2.89), Wz(-1.18)), 1.3, "MIDDLE_CENTER")
T("CLARIFICACIÓN", (U(2.89), Wz(-1.28)), 1.1, "MIDDLE_CENTER")
T("(1/3 DEL LARGO)", (U(2.89), Wz(-1.38)), 1.1, "MIDDLE_CENTER")
# tuberías entre unidades
tubo(U(-0.55), Wz(-0.40), U(0.25), Wz(-0.30))                         # entrada a la trampa
arrow((U(0.25) + 0.2, Wz(-0.35)), (1, 0))
tubo(U(0.55), Wz(-0.50), U(TQ0 + 0.12), Wz(-0.40))                    # trampa -> tanque (esquema)
tubo(U(TQ1), Wz(-0.50), U(CI - 0.25), Wz(-0.40))
arrow((U(CI - 0.25), Wz(-0.45)), (1, 0))
# cilindro de inspección
R(U(CI - 0.25), Wz(-1.70), U(CI + 0.25), Wz(0))
psp.add_lwpolyline([(U(CI - 0.29), Wz(0)), (U(CI - 0.29), Wz(0.08)), (U(CI + 0.29), Wz(0.08)),
                    (U(CI + 0.29), Wz(0))], dxfattribs={"layer": "S-DET"})
psp.add_arc((U(CI), Wz(0.08) - 0.29 * k * 1.6), 0.29 * k * 1.65, 80, 100, dxfattribs={"layer": "S-DET"})
tubo(U(CI + 0.18), Wz(-1.40), U(FA0 + 0.16), Wz(-1.30))               # al fondo del FAFA
arrow((U(FA0 + 0.16) + 0.2, Wz(-1.35)), (1, 0))
leader((U(CI), Wz(0.12)), (U(CI) - 6, Wz(0.40)), "CILINDRO DE INSPECCIÓN", 1.4)
# FAFA
R(U(FA0), Wz(-0.10), U(FA1), Wz(0))
for a, b in ((FA0, FA0 + 0.12), (FA1 - 0.12, FA1)):
    bloques_v(U(a), U(b), Wz(-1.70), Wz(-0.10))
h = psp.add_hatch(color=7, dxfattribs={"layer": "S-DET"})
h.paths.add_polyline_path([(U(FA0), Wz(-1.80)), (U(FA1), Wz(-1.80)), (U(FA1), Wz(-1.70)), (U(FA0), Wz(-1.70))])
hatch([(U(FA0 + 0.12), Wz(-1.50)), (U(FA1 - 0.12), Wz(-1.50)), (U(FA1 - 0.12), Wz(-0.70)),
       (U(FA0 + 0.12), Wz(-0.70))], "GRAVEL", 0.35)
L((U(FA0 + 0.12), Wz(-1.50)), (U(FA1 - 0.12), Wz(-1.50)), "S-DET")    # falso fondo
L((U(FA0 + 0.12), Wz(-0.70)), (U(FA1 - 0.12), Wz(-0.70)), "S-FINO")
tubo(U(FA1 - 0.30), Wz(-0.55), U(5.45), Wz(-0.45))                    # salida
arrow((U(5.45) + 4, Wz(-0.50)), (1, 0))
tubo(U(4.67), Wz(-0.25), U(4.77), Wz(0.30))                           # respiradero
psp.add_lwpolyline([(U(4.62), Wz(0.30)), (U(4.72), Wz(0.38)), (U(4.82), Wz(0.30))], close=True,
                   dxfattribs={"layer": "S-DET"})
leader((U(4.77), Wz(0.34)), (U(5.10), Wz(0.52)), "RESPIRADERO 4\"", 1.4)
T("SALIDA A DRENAJE", (U(5.45) + 6.0, Wz(-0.50)), 1.4)
T("FAFA", (U(4.47), Wz(-0.40)), 1.5, "MIDDLE_CENTER")
T("PIEDRA CUARTA", (U(4.47), Wz(-1.05)), 1.2, "MIDDLE_CENTER")
T("FALSO FONDO", (U(4.47), Wz(-1.60)), 1.1, "MIDDLE_CENTER")
# cotas
dim_v(U(-0.48), Wz(-1.70), Wz(0), "1.70", side=-1)
T("PROF. TOTAL", (U(-0.48) - 1.3, Wz(-0.85) - 2.6), 1.2, "MIDDLE_RIGHT")
dim_v(U(2.25), Wz(-0.40), Wz(-0.10), "0.30", side=-1)
dim_v(U(2.25), Wz(-1.60), Wz(-0.40), "", side=-1)
T("1.20", (U(2.25) - 1.3, Wz(-0.70)), 1.6, "MIDDLE_RIGHT")
dim_v(U(FA1 + 0.10), Wz(-1.50), Wz(-0.70), "0.80")
dim_v(U(FA1 + 0.10), Wz(-1.70), Wz(-1.50), "0.20")
dim_h(U(TQ0 + 0.12), U(TQ1 - 0.12), Wz(0.20) + 2.0, "2.00")
dim_h(U(FA0 + 0.12), U(FA1 - 0.12), Wz(0.20) + 2.0, "0.80")
T("ESQUEMA: LA TRAMPA DE GRASA SE UBICA EN EL COLECTOR AG Y LAS AGUAS NEGRAS ENTRAN POR LA CR DE ENTRADA "
  "(VER PLANTA N1).", (362.0, Wz(-1.80) - 3.0), 1.3)

# ---------------------------------------------------------------- detalle 2: sección de drenaje
X5, Y5, k5 = 630.0, 563.0, 100.0                    # 1:10
cl.text(psp, "DETALLE 2 - SECCIÓN DE DRENAJE", (600.0, 580.0), 3.0, "A-TITULOS", "TOP_LEFT")
cl.text(psp, "Esc. 1:10", (600.0, 575.0), 2.0, "A-TEXTO", "TOP_LEFT")
w5 = 0.50 * k5
capas = [(0.00, -0.10, "TIERRA", "EARTH"), (-0.10, -0.15, "GRAVA FINA, ARENA O ARROCILLO", "AR-SAND"),
         (-0.15, -0.20, "PIEDRA QUINTA", "GRAVEL"), (-0.20, -0.30, "", "GRAVEL"),
         (-0.30, -0.60, "PIEDRA TERCERA", "GRAVEL")]
for a, b, s, pat in capas:
    pts = [(X5, Y5 + a * k5), (X5 + w5, Y5 + a * k5), (X5 + w5, Y5 + b * k5), (X5, Y5 + b * k5)]
    R(*pts[0], *pts[2])
    hatch(pts, pat, 0.25 if pat != "EARTH" else 0.6)
    if s:
        leader((X5 + 3, Y5 + (a + b) / 2 * k5), (X5 - 6, Y5 + (a + b) / 2 * k5 + (4 if a == 0 else 0)), s, 1.4)
psp.add_circle((X5 + w5 / 2, Y5 - 0.25 * k5), 0.05 * k5, dxfattribs={"layer": "S-AN"})
leader((X5 + w5 / 2 + 5, Y5 - 0.25 * k5), (X5 - 6, Y5 - 0.25 * k5), "TUBO PERFORADO 100 mm", 1.4)
L((X5 - 8, Y5), (X5 + w5 + 8, Y5), "S-DET")
T("NIVEL DE TERRENO", (X5 + w5 + 1, Y5 + 2.0), 1.4)
dim_h(X5, X5 + w5, Y5 - 0.60 * k5 - 7, "0.50")
dim_v(X5 + w5 + 6, Y5 + -0.20 * k5, Y5, "0.30-0.60")
dim_v(X5 + w5 + 6, Y5 - 0.60 * k5, Y5 - 0.20 * k5, "")
T("0.60-0.90", (X5 + w5 + 7.3, Y5 - 0.42 * k5), 1.6)

# ---------------------------------------------------------------- detalle 3: caja de registro y trampa
Y6 = 405.0
cl.text(psp, "DETALLE 3 - CAJA DE REGISTRO Y TRAMPA DE GRASA", (362.0, Y6), 3.0, "A-TITULOS", "TOP_LEFT")
cl.text(psp, "SECCIONES - S/E", (362.0, Y6 - 5), 2.0, "A-TEXTO", "TOP_LEFT")
xa, ya = 394.0, 352.0                                # caja de registro
R(xa - 22, ya - 28, xa + 22, ya + 6)
R(xa - 17, ya - 23, xa + 17, ya + 6, "S-FINO")
hatch([(xa - 22, ya - 28), (xa + 22, ya - 28), (xa + 22, ya + 6), (xa + 17, ya + 6), (xa + 17, ya - 23),
       (xa - 17, ya - 23), (xa - 17, ya + 6), (xa - 22, ya + 6)])
R(xa - 20, ya + 6, xa + 20, ya + 9)                                   # tapa
psp.add_arc((xa, ya - 18), 5, 180, 360, dxfattribs={"layer": "S-AN"})  # media caña
L((xa - 34, ya - 15), (xa - 17, ya - 15), "S-AN")
L((xa + 17, ya - 15), (xa + 34, ya - 15), "S-AN")
L((xa - 4, ya + 9), (xa - 4, ya + 12), "S-DET")
L((xa + 4, ya + 9), (xa + 4, ya + 12), "S-DET")
L((xa - 4, ya + 12), (xa + 4, ya + 12), "S-DET")
leader((xa + 3, ya + 11), (xa + 26, ya + 16), "AGARRADERA VARILLA #3 LISA")
leader((xa + 18, ya + 7.5), (xa + 26, ya + 10), "TAPA Y MARCO CON ANGULAR")
leader((xa + 15, ya - 5), (xa + 26, ya - 2), "REPELLO FINO")
leader((xa, ya - 18), (xa + 26, ya - 22), "MEDIA CAÑA (FONDO)")
leader((xa + 10, ya - 26), (xa + 26, ya - 30), "LOSA CON MALLA #3 @0.15")
T("TUBERÍA PVC", (xa - 34, ya - 12.5), 1.4)
T("CAJA DE REGISTRO (CR)", (xa, ya - 34), 1.8, "MIDDLE_CENTER")
xb, yb = 487.0, 352.0                                # trampa de grasa
R(xb - 17, yb - 28, xb + 17, yb + 6)
R(xb - 12, yb - 23, xb + 12, yb + 6, "S-FINO")
hatch([(xb - 17, yb - 28), (xb + 17, yb - 28), (xb + 17, yb + 6), (xb + 12, yb + 6), (xb + 12, yb - 23),
       (xb - 12, yb - 23), (xb - 12, yb + 6), (xb - 17, yb + 6)])
R(xb - 15, yb + 6, xb + 15, yb + 9)
L((xb - 28, yb - 6), (xb - 8, yb - 6), "S-AJ")
L((xb - 8, yb - 2), (xb - 8, yb - 15), "S-AJ")
L((xb + 8, yb - 9), (xb + 28, yb - 9), "S-AJ")
L((xb + 8, yb - 2), (xb + 8, yb - 18), "S-AJ")
e = L((xb - 12, yb - 9), (xb + 12, yb - 9), "S-AJ")
e.dxf.ltscale = 0.4
T("ENTRADA AG", (xb - 28, yb - 3.5), 1.4)
T("SALIDA", (xb + 18, yb - 6.5), 1.4)
T("TRAMPA DE GRASA (TG)", (xb, yb - 34), 1.8, "MIDDLE_CENTER")
T("INTERIOR 0.60 x 0.60", (xb, yb - 37.5), 1.5, "MIDDLE_CENTER")

# ---------------------------------------------------------------- detalle 4: baño típico (suite 1)
Y7, X7, k7 = 405.0, 520.0, 25.0                      # 1:40
cl.text(psp, "DETALLE 4 - BAÑO TÍPICO", (X7, Y7), 3.0, "A-TITULOS", "TOP_LEFT")
cl.text(psp, "SUITE 1 (N2 Y N3), SUITE 3 EN ESPEJO - Esc. 1:40", (X7, Y7 - 5), 2.0, "A-TEXTO", "TOP_LEFT")


def B(x, y):                                       # planta del baño: horizontal = y, vertical = x
    return (X7 + 8 + (y - 2.21) * k7, 318.0 + (x - 3.72) * k7)


R(*B(3.72, 2.21), *B(5.27, 4.41), "S-FINO")
R(*B(3.60, 2.06), *B(5.39, 4.53), "S-FINO")
R(*B(3.72, 2.21), *B(5.27, 3.06), "S-FINO")                       # ducha
R(*B(5.39, 2.65), *B(5.60, 3.75), "S-FINO")                       # forro
psp.add_ellipse(B(4.80, 3.43), major_axis=(0, 0.30 * k7), ratio=0.62, dxfattribs={"layer": "S-FINO"})
R(*B(4.85, 3.83), *B(5.27, 4.30), "S-FINO")                       # lavatorio
for (a, b, lay) in (((4.95, 3.43), BN1, "S-AN"), ((4.50, 2.64), BG1, "S-AJ")):
    e = L(B(*a), B(*b), lay)
    if lay == "S-AJ":
        e.dxf.ltscale = 0.4
pts = [B(5.15, 4.05), B(5.30, 3.88), B(5.30, 3.00), B(*BG1)]
e = psp.add_lwpolyline(pts, dxfattribs={"layer": "S-AJ"})
e.dxf.ltscale = 0.4
for p, kind in ((BN1, "BN"), (BG1, "BG")):
    S.leyenda_simbolo(psp, kind, *B(*p), 0.8)
S.leyenda_simbolo(psp, "SP", *B(4.50, 2.64))
leader(B(4.50, 2.64), (B(4.50, 2.64)[0] + 6, 306.0), "SP 2\"")
leader(B(4.95, 3.43), (B(4.95, 3.43)[0] + 4, 306.0 - 0.1), "WC 4\"")
leader(B(5.15, 4.05), (B(5.15, 4.05)[0] + 10, 362.0), "LM 2\" (SIFÓN)")
leader(B(*BN1), (B(*BN1)[0] - 6, 365.0), "BAJANTE AN 4\"", 1.5)
leader(B(*BG1), (B(*BG1)[0] - 8, 360.0), "BAJANTE AG 2\"", 1.5)
T("VENTILACIÓN 2\" A TECHO EN CADA BAJANTE", (X7, 297.0), 1.5)
T("FACHADA", B(3.60, 2.06)[0:1] + (B(3.60, 2.06)[1] - 2.5,), 1.4)

# ---------------------------------------------------------------- simbología
y = S.cuadro_simbologia(psp, 610.0, 405.0, [
    ("AN", "AGUAS NEGRAS (PVC)"),
    ("AJ", "AGUAS GRISES (PVC)"),
    ("BN", "BAJANTE DE AGUAS NEGRAS 4\""),
    ("BG", "BAJANTE DE AGUAS GRISES 2\""),
    ("SP", "SIFÓN DE PISO (DUCHA) 2\""),
    ("SAL", "SALIDA DE APARATO (WC / LM / LP)"),
    ("CR", "CAJA DE REGISTRO (DET. 3)"),
    ("DREN", "DRENAJE EN ZANJA (DET. 2)")], w_txt=72.0, row_h=6.0, title="SIMBOLOGÍA")
cl.text(psp, "AN / AG: AGUAS NEGRAS / GRISES; TG: TRAMPA", (610.0, y - 2.5), 1.6, "A-TEXTO", "TOP_LEFT")
cl.text(psp, "DE GRASA; FAFA: FILTRO ANAEROBIO DE FLUJO", (610.0, y - 5.0), 1.6, "A-TEXTO", "TOP_LEFT")
cl.text(psp, "ASCENDENTE.", (610.0, y - 7.5), 1.6, "A-TEXTO", "TOP_LEFT")

# ---------------------------------------------------------------- notas
X3, yS = 362.0, 278.0
cl.text(psp, "NOTAS:", (X3, yS), 3.5, "A-TITULOS", "TOP_LEFT")
notas = [
    "TODAS LAS MEDIDAS ESTÁN DADAS EN METROS; LAS DIMENSIONES DEL TANQUE Y DEL FAFA SON INTERIORES, SALVO "
    "INDICACIÓN CONTRARIA.",
    "VERIFICAR EN SITIO LA UBICACIÓN, LOS NIVELES Y LAS CONDICIONES DEL TERRENO ANTES DE INICIAR LA "
    "CONSTRUCCIÓN.",
    "NO HAY ALCANTARILLADO SANITARIO: LAS AGUAS RESIDUALES SE TRATAN EN TANQUE SÉPTICO CON FAFA Y SE "
    "DISPONEN EN EL DRENAJE DEL PATIO POSTERIOR.",
    "AGUAS NEGRAS (INODOROS) EN 4\" Y AGUAS GRISES (LAVATORIOS, DUCHAS Y FREGADERO) EN 2\", CON "
    "BAJANTES Y CAJAS DE REGISTRO SEPARADAS.",
    "TUBERÍA ENTERRADA EN PVC SDR-26 O SUPERIOR, DIÁMETRO MÍNIMO 100 MM (4\"); ACCESORIOS SANITARIOS EN "
    "TODOS LOS CAMBIOS DE DIRECCIÓN.",
    "LAS AGUAS GRISES PASAN POR LA TRAMPA DE GRASA Y SE UNEN A LAS AGUAS NEGRAS EN LA CAJA DE REGISTRO "
    "DE ENTRADA AL TANQUE.",
    "BAJANTES: SUITE 1 EN FORRO DEL MURO BAÑO / WALK-IN, CON COLECTORES COLGADOS BAJO LA LOSA DEL N2 "
    "HASTA C2; SUITE 2 Y FREGADERO EN DUCTO DE LA COCINA (ESQUINA D/4); SUITE 3 EN DUCTO JUNTO A C6 EN "
    "LA SALA. DUCTOS DE 0.30 x 0.40 Y FORRO DE 0.20.",
    "CADA BAJANTE SE PROLONGA COMO VENTILACIÓN DE 2\" SOBRE LA CUBIERTA.",
    "LAS TUBERÍAS PASAN SOBRE LAS PLACAS DE CIMENTACIÓN SIN ATRAVESAR PEDESTALES; CRUCES CON VIGAS "
    "RIOSTRA CON CAMISA. EL TANQUE Y LAS CAJAS SE UBICAN FUERA DE LAS PLACAS (VER C01).",
    "TANQUE Y FAFA: CONCRETO DE 210 KG/CM2; LOSAS INFERIOR Y SUPERIOR DE 0.10 M MÍNIMO CON MALLA #3 "
    "@20 CM; MUROS DE BLOQUE 12x20x40 CON JUNTAS LLENAS Y REPELLO IMPERMEABLE INTERIOR; REFUERZO "
    "VERTICAL #3 @40 CM Y HORIZONTAL #3 CADA DOS HILADAS; RECUBRIMIENTO 4 CM; CURADO 7 DÍAS.",
    "CÁMARA 1 (DIGESTIÓN) = 2/3 Y CÁMARA 2 (CLARIFICACIÓN) = 1/3 DEL LARGO. TEES SANITARIAS DE PVC "
    "100 MM, 0.30 M SOBRE Y 0.40 M BAJO EL NIVEL DE LÍQUIDOS. BORDE LIBRE 0.30 M Y PROFUNDIDAD ÚTIL "
    "1.20 M.",
    "FAFA: 1.04 x 0.80 M INTERIOR, PROFUNDIDAD ÚTIL 1.20 M, FALSO FONDO A 0.20 M CON LOSA PERFORADA, "
    "MEDIO FILTRANTE DE PIEDRA CUARTA LAVADA (5-7 CM) DE 0.80 M SIN COMPACTAR Y ESPACIO LIBRE SUPERIOR "
    "DE 0.20 M.",
    "RESPIRADEROS DE PVC 100 MM, 0.30 M SOBRE EL TERRENO, CON SOMBRERETE. CILINDRO DE INSPECCIÓN DE "
    "CONCRETO, DIÁMETRO INTERIOR MÍNIMO 0.30 M. TAPAS DE CONCRETO REFORZADO DE 0.60 x 0.60 M MÍNIMO, "
    "CON AGARRADERAS.",
    "DRENAJE: TUBO PERFORADO DE 100 MM EN ZANJA DE 0.50 M (DETALLE 2). LONGITUD 7.40 M."
    "",
    "NO RELLENAR HASTA QUE EL CONCRETO ALCANCE SU RESISTENCIA; COMPACTAR EN CAPAS DE 20 CM MÁXIMO Y "
    "EVITAR EL PASO DE VEHÍCULOS SOBRE EL SISTEMA.",
    "ANTES DEL RELLENO, VERIFICAR LA ESTANQUEIDAD DEL TANQUE Y DEL FAFA; LIMPIAR EL SISTEMA ANTES DE "
    "COLOCAR EL MEDIO FILTRANTE Y LLENAR EL FAFA CON AGUA ANTES DE INICIAR LA OPERACIÓN.",
    "MANTENIMIENTO: RETIRAR LOS LODOS DEL TANQUE CUANDO OCUPEN APROXIMADAMENTE 1/3 DEL VOLUMEN DE LA "
    "PRIMERA CÁMARA.",
    "NO SE PERMITE MODIFICAR DIMENSIONES, NIVELES, DIÁMETROS NI MATERIALES SIN AUTORIZACIÓN DEL "
    "PROFESIONAL RESPONSABLE.",
]
cl.notes_block(psp, X3, yS - 6, [f"{i}.- {t}" for i, t in enumerate(notas, 1)] + [cl.NOTA_PR], 1.8, 340)

H.titleblock(doc, psp, "S02", "AGUAS RESIDUALES",
             ["PLANTAS NIVELES 1, 2 Y 3.", "TANQUE SÉPTICO, FAFA Y DRENAJE.", "CAJA DE REGISTRO,",
              "TRAMPA DE GRASA Y BAÑO TÍPICO.", "SIMBOLOGÍA Y NOTAS.", ""],
             [("0", "06-10-2026", "VERSIÓN DE TRABAJO PARA REVISIÓN"),
              ("1", "07-10-2026", "DETALLE DE TANQUE SEGÚN LA REFERENCIA"),
              ("2", "07-10-2026", "LISTA DEFINITIVA (22); PARA TRÁMITE")], escalas="1:100 / INDICADAS")

OUT.mkdir(parents=True, exist_ok=True)
doc.saveas(OUT / f"{NAME}.dxf")
cl.render_pdf(doc, LAYOUT, OUT / f"{NAME}.pdf")
print("DXF:", OUT / f"{NAME}.dxf")
