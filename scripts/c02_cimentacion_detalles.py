"""Lámina C02 - DETALLES DE CIMENTACIÓN: placas F1 y F2 (corte y planta), pedestal y pletina.

Secciones de la referencia (RIVERGRAND C02) por indicación del usuario [PR]:
placa 1,65 x 1,65 x 0,25 con malla #4 @20 cm; pedestal 0,30 x 0,30 x 0,80 con 4 #4 y
estribos #3 @10 cm; tubo estructural 150 x 150 mm en 3,17 mm; pletina de unión 270 x 270 mm.
F2 (lindero): pedestal y tubo a paño del lindero, como en la C01 (tubo en el muro de 0,15).
"""
import math

import cadlib as cl
import hoja as H

REV = "rev0"
OUT = cl.ROOT / "planos" / "C02_cimentacion_detalles"
NAME = f"SR-C02_CIMENTACION_DETALLES_{REV}"

FB, TP, PED, HP, TUBO, PLT = 1.65, 0.25, 0.30, 0.80, 0.15, 0.27
RC = 0.05                                       # recubrimiento placa (C08 ref.: 50 mm)
RB = 0.0064                                     # radio varilla #4 (12,7 mm)

doc = cl.new_doc()
msp = doc.modelspace()
for name, col, lw, lt in (("E-DET", 7, 50, "Continuous"), ("E-REF", 7, 35, "Continuous"),
                          ("E-ACERO", 7, 50, "Continuous"), ("E-TRAMA", 8, 9, "Continuous"),
                          ("E-TXT", 7, 18, "Continuous"), ("E-COTA", 7, 18, "Continuous"),
                          ("E-TERRENO", 7, 35, "Continuous")):
    doc.layers.add(name, color=col, linetype=lt, lineweight=lw)
for sc in (5, 10, 15):
    if f"COTA-{sc}" not in doc.dimstyles:
        cl._dimstyle(doc, f"COTA-{sc}", sc)


def L(a, b, layer="E-REF"):
    msp.add_line(a, b, dxfattribs={"layer": layer})


def R(x0, y0, x1, y1, layer="E-DET", hatch=None, scale=0.004, color=7):
    pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    if hatch:
        ht = msp.add_hatch(color=color, dxfattribs={"layer": "E-TRAMA" if hatch != "SOLID" else layer})
        ht.paths.add_polyline_path(pts)
        if hatch != "SOLID":
            ht.set_pattern_fill(hatch, scale=scale)
    msp.add_lwpolyline(pts, close=True, dxfattribs={"layer": layer})


def dot(x, y, r=RB):
    msp.add_circle((x, y), r, dxfattribs={"layer": "E-REF"})
    ht = msp.add_hatch(color=7, dxfattribs={"layer": "E-REF"})
    ht.paths.add_edge_path().add_arc((x, y), r, 0, 360)


def dim(a, b, base, hor, style):
    if hor:
        d = msp.add_linear_dim(base=(0, base), p1=a, p2=b, angle=0, dimstyle=style,
                               dxfattribs={"layer": "E-COTA"})
    else:
        d = msp.add_linear_dim(base=(base, 0), p1=a, p2=b, angle=90, dimstyle=style,
                               dxfattribs={"layer": "E-COTA"})
    d.render()


def section(ox, xp0):
    """Corte de placa con pedestal; xp0 = borde izquierdo del pedestal respecto a la placa."""
    yb = -(HP + TP)
    R(ox, yb, ox + FB, yb + TP, hatch="AR-CONC")                         # placa
    R(ox + xp0, -HP, ox + xp0 + PED, 0.0, hatch="AR-CONC")              # pedestal
    xt = ox + (xp0 if xp0 == 0.0 else xp0 + (PED - TUBO) / 2)
    R(xt, 0.012, xt + TUBO, 0.38, "E-DET")                               # tubo
    L((xt + 0.004, 0.012), (xt + 0.004, 0.38), "E-REF")
    L((xt + TUBO - 0.004, 0.012), (xt + TUBO - 0.004, 0.38), "E-REF")
    xpl = ox + xp0 + PED / 2 - PLT / 2 if xp0 > 0 else ox
    R(xpl, 0.0, xpl + PLT, 0.012, "E-DET", hatch="SOLID")                # pletina
    # malla inferior (#4 @20) con ganchos
    ym = yb + RC
    L((ox + RC, ym + 0.15), (ox + RC, ym), "E-ACERO")
    L((ox + RC, ym), (ox + FB - RC, ym), "E-ACERO")
    L((ox + FB - RC, ym), (ox + FB - RC, ym + 0.15), "E-ACERO")
    n = int((FB - 2 * RC) / 0.20)
    for i in range(n + 1):
        dot(ox + RC + 0.02 + i * (FB - 2 * RC - 0.04) / n, ym + 2 * RB)
    # pedestal: 4 #4 (2 en corte) con pata, estribos #3 @10
    for xv, s in ((ox + xp0 + 0.05, 1), (ox + xp0 + PED - 0.05, -1)):
        L((xv, -0.04), (xv, ym + 0.02), "E-ACERO")
        L((xv, ym + 0.02), (xv + s * 0.25 if xp0 > 0 else xv + 0.25, ym + 0.02), "E-ACERO")
    for k in range(int((HP - 0.08) / 0.10) + 1):
        yy = -0.06 - k * 0.10
        L((ox + xp0 + 0.035, yy), (ox + xp0 + PED - 0.035, yy), "E-ACERO")
    # terreno y cotas
    L((ox - 0.25, 0.0), (ox + FB + 0.25, 0.0), "E-TERRENO")
    dim((ox, 0.40), (ox + FB, 0.40), 0.55, True, "COTA-15")
    if xp0 > 0:
        dim((ox, 0.40), (ox + xp0, 0.40), 0.47, True, "COTA-15")
        dim((ox + xp0, 0.40), (ox + xp0 + PED, 0.40), 0.47, True, "COTA-15")
        dim((ox + xp0 + PED, 0.40), (ox + FB, 0.40), 0.47, True, "COTA-15")
    else:
        dim((ox, 0.40), (ox + PED, 0.40), 0.47, True, "COTA-15")
        dim((ox + PED, 0.40), (ox + FB, 0.40), 0.47, True, "COTA-15")
    dim((ox, -HP), (ox, 0.0), ox - 0.15, False, "COTA-15")
    dim((ox, yb), (ox, -HP), ox - 0.15, False, "COTA-15")


def plan(ox, oy, cx):
    """Planta de placa con malla #4 @20 cm; cx = centro del pedestal desde el borde de la placa."""
    R(ox, oy, ox + FB, oy + FB, "E-DET")
    n = int((FB - 2 * RC) / 0.20)
    for i in range(n + 1):
        t = RC + 0.02 + i * (FB - 2 * RC - 0.04) / n
        L((ox + t, oy + RC), (ox + t, oy + FB - RC), "E-ACERO")
        L((ox + RC, oy + t), (ox + FB - RC, oy + t), "E-ACERO")
    cy = FB / 2
    R(ox + cx - PED / 2, oy + cy - PED / 2, ox + cx + PED / 2, oy + cy + PED / 2, "E-DET")
    R(ox + cx - PLT / 2 if cx > PED / 2 else ox, oy + cy - PLT / 2,
      ox + cx + PLT / 2 if cx > PED / 2 else ox + PLT, oy + cy + PLT / 2, "E-REF")
    xt = ox + cx - TUBO / 2 if cx > PED / 2 else ox
    R(xt, oy + cy - TUBO / 2, xt + TUBO, oy + cy + TUBO / 2, "E-DET", hatch="SOLID")
    dim((ox, oy + FB), (ox + FB, oy + FB), oy + FB + 0.15, True, "COTA-15")
    dim((ox + FB, oy), (ox + FB, oy + FB), ox + FB + 0.15, False, "COTA-15")


section(0.0, (FB - PED) / 2)                    # F1 corte
section(4.0, 0.0)                               # F2 corte (pedestal a paño del lindero)
plan(0.0, -4.0, FB / 2)                         # F1 planta
plan(4.0, -4.0, PED / 2)                        # F2 planta
# pedestal (corte horizontal) 1:10
PX, PY = 8.0, 0.0
R(PX, PY, PX + PED, PY + PED, hatch="AR-CONC")
R(PX + 0.035, PY + 0.035, PX + PED - 0.035, PY + PED - 0.035, "E-ACERO")
for xx in (PX + 0.05, PX + PED - 0.05):
    for yy in (PY + 0.05, PY + PED - 0.05):
        dot(xx, yy)
R(PX + (PED - TUBO) / 2, PY + (PED - TUBO) / 2, PX + (PED + TUBO) / 2, PY + (PED + TUBO) / 2, "E-DET")
dim((PX, PY + PED), (PX + PED, PY + PED), PY + PED + 0.06, True, "COTA-10")
dim((PX + PED, PY), (PX + PED, PY + PED), PX + PED + 0.06, False, "COTA-10")
# pletina 270 x 270 (planta) 1:5
QX, QY = 8.0, -1.0
R(QX, QY, QX + PLT, QY + PLT, "E-DET")
R(QX + (PLT - TUBO) / 2, QY + (PLT - TUBO) / 2, QX + (PLT + TUBO) / 2, QY + (PLT + TUBO) / 2, "E-REF")
for xx in (QX + 0.03, QX + PLT - 0.03):
    for yy in (QY + 0.03, QY + PLT - 0.03):
        msp.add_circle((xx, yy), 0.009, dxfattribs={"layer": "E-REF"})
dim((QX, QY + PLT), (QX + PLT, QY + PLT), QY + PLT + 0.04, True, "COTA-5")
dim((QX + PLT, QY), (QX + PLT, QY + PLT), QX + PLT + 0.04, False, "COTA-5")

# ================================================================ hoja
psp = doc.layouts.new("C02-DETALLES")
psp.page_setup(size=(cl.A1_W, cl.A1_H), margins=(0, 0, 0, 0), units="mm")
doc.layouts.set_active_layout("C02-DETALLES")
cl.frame(psp)
VPS = {}


def vp(key, center, size, scale, mc):
    v = psp.add_viewport(center=center, size=size, view_center_point=mc,
                         view_height=size[1] * scale / 1000.0, dxfattribs={"layer": "A-VIEWPORT"})
    v.dxf.flags = v.dxf.flags | 16384
    VPS[key] = (center, mc, scale)


def tp(key, x, y):
    c, mc, sc = VPS[key]
    f = 1000.0 / sc
    return (c[0] + (x - mc[0]) * f, c[1] + (y - mc[1]) * f)


def callout(key, target, pos, txt, h=2.0, w=60.0, attach=4, dy=0.0):
    tx, ty = tp(key, *target)
    if pos[1] is None:
        pos = (pos[0], ty + dy)
    psp.add_line(pos, (tx, ty), dxfattribs={"layer": "A-TEXTO"})
    psp.add_circle((tx, ty), 0.6, dxfattribs={"layer": "A-TEXTO"})
    cl.mtext(psp, txt, (pos[0] + (2.0 if attach == 4 else -2.0), pos[1]), h, w, layer="A-TEXTO", attach=attach)


def title(x, y, t, s):
    cl.text(psp, t, (x, y), 4.5, "A-TITULOS", "TOP_LEFT")
    cl.text(psp, s, (x, y - 6.5), 2.5, "A-TEXTO", "TOP_LEFT")


vp("S1", (130.0, 480.0), (190.0, 150.0), 15, (0.80, -0.30))
title(40.0, 420.0, "CORTE FUNDACIÓN F1 (CENTRADA)", "Esc. 1:15")
vp("S2", (380.0, 480.0), (190.0, 150.0), 15, (4.80, -0.30))
title(290.0, 420.0, "CORTE FUNDACIÓN F2 (EXCÉNTRICA, LINDERO)", "Esc. 1:15")
vp("P1", (130.0, 320.0), (190.0, 145.0), 15, (0.88, -3.18))
title(40.0, 257.0, "PLANTA FUNDACIÓN F1", "Esc. 1:15")
vp("P2", (380.0, 320.0), (190.0, 145.0), 15, (4.88, -3.18))
title(290.0, 257.0, "PLANTA FUNDACIÓN F2", "Esc. 1:15")
vp("PD", (560.0, 510.0), (70.0, 65.0), 10, (PX + 0.17, PY + 0.16))
title(510.0, 472.0, "SECCIÓN DE PEDESTAL", "Esc. 1:10")
vp("PL", (650.0, 510.0), (75.0, 75.0), 5, (QX + 0.15, QY + 0.15))
title(612.0, 466.0, "PLETINA DE UNIÓN", "Esc. 1:5")

for key, ox, xp0 in (("S1", 0.0, (FB - PED) / 2), ("S2", 4.0, 0.0)):
    xc = ox + xp0 + PED / 2
    xr = tp(key, ox + FB, 0)[0] + 6.0
    callout(key, (xc + 0.02, 0.20), (xr, None), "TUBO ESTRUCTURAL 150 x 150 mm EN 3,17 mm [PR]")
    callout(key, (xc + 0.10, 0.006), (xr, None), "PLETINA PARA UNIÓN 270 x 270 mm [PR]", dy=4.0)
    callout(key, (ox + xp0 + PED - 0.01, -0.30), (xr, None), "PEDESTAL 30 x 30 cm [PR]")
    callout(key, (ox + xp0 + PED - 0.05, -0.50), (xr, None), "4 VARILLAS #4 [PR]")
    callout(key, (ox + xp0 + 0.15, -0.66), (xr, None), "ESTRIBOS VARILLA #3 @10 cm [PR]")
    callout(key, (ox + FB - 0.30, -(HP + TP) + RC), (xr, None), "MALLA CON VARILLAS #4 @20 cm [PR]", dy=-8.0)
for key in ("P1", "P2"):
    xr = tp(key, 4.0 * (key == "P2") + FB, 0)[0] + 6.0
    callout(key, (4.0 * (key == "P2") + 0.30, -4.0 + 0.30), (xr, 280.0), "MALLA CON VARILLAS #4 @20 cm [PR]")
    callout(key, (4.0 * (key == "P2") + (FB / 2 if key == "P1" else 0.10), -4.0 + FB / 2 + 0.05),
            (xr, 295.0), "TUBO 150 x 150 mm, PLETINA 270 x 270 mm Y PEDESTAL 30 x 30 cm [PR]")
callout("PL", (QX + 0.03, QY + 0.03), (612.0, 557.0), "PERFORACIONES PARA PERNOS DE ANCLAJE (DIÁMETRO SEGÚN CÁLCULO, PD)", 1.8, 55.0)

X3, y = 510.0, 440.0
cl.text(psp, "NOTAS:", (X3, y), 3.5, "A-TITULOS", "TOP_LEFT")
notas = [
    "TODAS LAS MEDIDAS ESTÁN DADAS EN METROS, SALVO INDICACIÓN CONTRARIA. [PR]",
    "UBICACIÓN DE LAS FUNDACIONES F1 Y F2 SEGÚN LÁMINA C01.",
    "F1: PLACA CENTRADA BAJO LAS COLUMNAS DEL EJE C. F2: PLACA EXCÉNTRICA EN LOS LINDEROS (EJES A "
    "Y D), CON PEDESTAL Y TUBO A PAÑO DEL LINDERO; NO INVADE EL PREDIO VECINO.",
    "PLACAS DE 1,65 x 1,65 x 0,25 m CON MALLA DE VARILLAS #4 @20 cm EN AMBAS DIRECCIONES Y GANCHOS "
    "EN LOS EXTREMOS. RECUBRIMIENTO DE 5 cm EN ELEMENTOS COLADOS CONTRA EL TERRENO. [PR]",
    "PEDESTAL DE 30 x 30 cm Y 0,80 m DE ALTO, 4 VARILLAS #4 CON PATA DE 25 cm Y ESTRIBOS #3 @10 cm. [PR]",
    "COLUMNA: TUBO ESTRUCTURAL DE 150 x 150 mm EN 3,17 mm SOLDADO A PLETINA DE 270 x 270 mm ANCLADA "
    "AL PEDESTAL. PERNOS Y SOLDADURA SEGÚN CÁLCULO (PD). [PR]",
    "CAPACIDAD SOPORTANTE CONSIDERADA qadm = 12 t/m² [PR]; VERIFICAR CON ESTUDIO DE SUELOS.",
    "MATERIALES Y ESPECIFICACIONES SEGÚN LÁMINA C08. LAS SECCIONES SON LAS DEL PROYECTO DE "
    "REFERENCIA, POR INDICACIÓN DEL INGENIERO RESPONSABLE; NO SUSTITUYEN LA MEMORIA DE CÁLCULO.",
]
cl.notes_block(psp, X3, y - 6, [f"{i}.- {t}" for i, t in enumerate(notas, 1)] + [cl.NOTA_PR], 2.0, 190)

H.titleblock(doc, psp, "C02", "FUNDACIONES",
             ["DETALLES.", "CORTE Y PLANTA F1 Y F2.", "SECCIÓN DE PEDESTAL.", "PLETINA DE UNIÓN.",
              "NOTAS.", ""],
             [("0", "06-10-2026", "VERSIÓN DE TRABAJO PARA REVISIÓN")], escalas="INDICADAS")

OUT.mkdir(parents=True, exist_ok=True)
doc.saveas(OUT / f"{NAME}.dxf")
cl.render_pdf(doc, "C02-DETALLES", OUT / f"{NAME}.pdf")
print("DXF:", OUT / f"{NAME}.dxf")
