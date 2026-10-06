"""Lámina C05 - DETALLE DE PÓRTICOS (eje longitudinal A, C, D y eje transversal 1 a 6).

rev1 (usuario): C05 y C06 unificadas en una sola lámina a 1:100; se eliminan C2 y A1 de la
referencia (no se usan); columna C1 del eje C en el eje 1 en los niveles 2 y 3, apoyada en una
viga de transferencia VT-1 (diseño especial) en el entrepiso del eje 1; sin columna en el N1
(portón).

Presentación de la referencia (RIVERGRAND C08/C09) [PR]: elevaciones esquemáticas de columnas,
vigas por nivel, vigas riostra y placas. Geometría según C01-C04 aprobadas: V1 de entrepiso
(cara superior a -0,10 del NPT; paquete 0,30), V1 de corona a +9,00, VA1 0,20 x 0,40, placas
F1/F2 con pedestal 0,80.
"""
import cadlib as cl
import hoja as H

SHEET = "C05"
REV = "rev2"
OUT = cl.ROOT / "planos" / "C05_porticos"
NAME = f"SR-{SHEET}_PORTICOS_{REV}"
LAYOUT = f"{SHEET}-PORTICOS"

W = H.W
YA = H.EJES_Y
XA, XC, XD = H.EJES_X["A"], H.EJES_X["C"], H.EJES_X["D"]
TUBO, BV, HV, LOSA = 0.15, 0.10, 0.20, 0.10
FB, PED, HP, TP = 1.65, 0.30, 0.80, 0.25
VAH = 0.40
NIV = [3.00, 6.00]                                 # NPT de entrepisos
COR = 9.00                                         # cara superior V1 de corona
SC = 100

doc = cl.new_doc()
msp = doc.modelspace()
for name, col, lw, lt in (("E-COL", 7, 35, "Continuous"), ("E-VIGA", 7, 35, "Continuous"),
                          ("E-LOSA", 8, 18, "Continuous"), ("E-CIM", 7, 25, "Continuous"),
                          ("E-TERRENO", 7, 50, "Continuous"), ("E-TXT", 7, 18, "Continuous"),
                          ("E-EJE", 8, 13, "DASHDOT"), ("E-COTA", 7, 18, "Continuous"),
                          ("E-REF", 8, 18, "Continuous")):
    doc.layers.add(name, color=col, linetype=lt, lineweight=lw)
if f"COTA-{SC}" not in doc.dimstyles:
    cl._dimstyle(doc, f"COTA-{SC}", SC)
TH = 0.18                                          # texto (1,8 mm a 1:100)
K = SC / 75.0                                      # factor de rótulos


class Frame:
    """Elevación de pórtico en model space: X = ox + s (posición a lo largo del pórtico), Y = oy + z."""

    def __init__(self, ox, oy):
        self.ox, self.oy = ox, oy

    def R(self, s0, z0, s1, z1, layer):
        o, p = self.ox, self.oy
        msp.add_lwpolyline([(o + s0, p + z0), (o + s1, p + z0), (o + s1, p + z1), (o + s0, p + z1)],
                           close=True, dxfattribs={"layer": layer})

    def L(self, a, b, layer):
        msp.add_line((self.ox + a[0], self.oy + a[1]), (self.ox + b[0], self.oy + b[1]),
                     dxfattribs={"layer": layer})

    def T(self, s, z, txt, h=TH, align="MIDDLE_CENTER", rot=0.0, layer="E-TXT"):
        cl.text(msp, txt, (self.ox + s, self.oy + z), h, layer, align, rot)

    def dim(self, a, b, base, hor):
        o, p = self.ox, self.oy
        pa, pb = (o + a[0], p + a[1]), (o + b[0], p + b[1])
        val = abs((b[0] - a[0]) if hor else (b[1] - a[1]))
        kw = dict(dimstyle=f"COTA-{SC}", dxfattribs={"layer": "E-COTA"},
                  text=f"{round(val + 1e-9, 2):.2f}")
        if hor:
            d = msp.add_linear_dim(base=(pa[0], p + base), p1=pa, p2=pb, angle=0, **kw)
        else:
            d = msp.add_linear_dim(base=(o + base, pa[1]), p1=pa, p2=pb, angle=90, **kw)
        d.render()

    def draw(self, axes, cols, spans, va_spans, footings, beam_supports=(), truss=(), notes=()):
        s_min, s_max = min(axes.values()), max(axes.values())
        # terreno
        self.L((s_min - 1.2, 0.0), (s_max + 0.30, 0.0), "E-TERRENO")
        # vigas riostra VA1
        for s0, s1 in va_spans:
            self.R(s0, -VAH, s1, 0.0, "E-CIM")
            pts = sorted([s0, s1] + [f[0] for f in footings if s0 < f[0] < s1])
            a, b = max(zip(pts[:-1], pts[1:]), key=lambda g: g[1] - g[0])
            self.T((a + b) / 2, -VAH - 0.20, "VA1")
        # pedestales y placas
        for s, typ, p0, p1 in footings:
            q0 = min(max(s - PED / 2, p0), p1 - PED)
            self.R(q0, -HP, q0 + PED, 0.0, "E-CIM")
            self.R(p0, -HP - TP, p1, -HP, "E-CIM")
            self.T((p0 + p1) / 2, -HP - TP - 0.25, typ)
        # columnas C1 (N1 a corona)
        for c in cols:
            s, zc = c if isinstance(c, tuple) else (c, 0.0)
            self.R(s - TUBO / 2, zc, s + TUBO / 2, COR, "E-COL")
            for z0, z1 in ((0.0, NIV[0] - LOSA - HV), (NIV[0], NIV[1] - LOSA - HV), (NIV[1], COR - HV)):
                if z0 >= zc - 0.15:
                    self.T(s + (0.22 if s < s_max - 0.5 else -0.22) * K, (z0 + z1) / 2, "C1", rot=90)
        # vigas V1 por nivel (entrepisos con losa; corona sin losa)
        for lev, top in (("N2", NIV[0] - LOSA), ("N3", NIV[1] - LOSA), ("COR", COR)):
            for sp in spans[lev]:
                s0, s1, lab = sp if len(sp) == 3 else (*sp, "V1")
                self.R(s0, top - HV, s1, top, "E-VIGA")
                if lev != "COR":
                    self.R(s0, top, s1, top + LOSA, "E-LOSA")
                self.T((s0 + s1) / 2, top - HV - 0.18 * K, lab)
        # extremos de viga apoyados en la V1 perpendicular (sección)
        for s, tops in beam_supports:
            for top in tops:
                self.R(s - BV / 2, top - HV, s + BV / 2, top, "E-REF")
        # cerchas de cubierta cortadas (cordón inferior plano)
        for s in truss:
            self.R(s - 0.075, COR, s + 0.075, COR + 0.05, "E-REF")
        if truss:
            self.T((s_min + s_max) / 2, COR + 0.45, "CERCHAS CE-1 CORTADAS (VER C04)", 0.13 * K)
        # ejes, burbujas y cotas
        for k, s in axes.items():
            self.L((s, COR + 0.30), (s, COR + 1.30), "E-EJE")
            msp.add_circle((self.ox + s, self.oy + COR + 1.55), 0.25, dxfattribs={"layer": "E-TXT"})
            self.T(s, COR + 1.55, k, 0.22)
        ss = list(axes.values())
        for a, b in zip(ss[:-1], ss[1:]):
            self.dim((a, COR + 0.30), (b, COR + 0.30), COR + 0.95, True)
        sl = s_min - 1.0
        for z0, z1 in ((-HP - TP, 0.0), (0.0, NIV[0]), (NIV[0], NIV[1]), (NIV[1], COR)):
            self.dim((s_min - 0.30, z0), (s_min - 0.30, z1), sl, False)
        for z, lab in ((0.0, "N1 ±0.00"), (NIV[0], "N2 +3.00"), (NIV[1], "N3 +6.00"),
                       (COR, "V1 CORONA +9.00")):
            self.L((s_max + 0.35, z), (s_max + 0.95, z), "E-TXT")
            self.T(s_max + 1.05, z, lab, 0.14 * K, "MIDDLE_LEFT")
        for s, z, txt in notes:
            self.T(s, z, txt, 0.13 * K)


# ================================================================ definición de pórticos
FR = []                                            # (título, subtítulo, frame, span)
ax = dict(YA)
full = [(a, b) for a, b in zip(list(ax.values())[:-1], list(ax.values())[1:])]
SPAN_L = (YA["1"] - 2.6, YA["6"] + 4.3)
fAD = Frame(0.0, 0.0)
fAD.draw(ax, list(ax.values()), {"N2": full, "N3": full, "COR": full}, [(YA["1"], YA["6"])],
         [(s, "F2", s - FB / 2, s + FB / 2) for s in ax.values()])
FR.append(("PÓRTICOS A Y D", "EJES 1 A 6 (COLINDANCIAS)", fAD, SPAN_L))
cC = [ax[k] for k in "23456"]
spC = [(YA["1"], YA["2"]), (YA["3"], YA["4"]), (YA["4"], YA["5"]), (YA["5"], YA["6"])]
fC = Frame(0.0, -16.0)
fC.draw(ax, [(YA["1"], NIV[0] - LOSA)] + cC, {"N2": spC, "N3": spC, "COR": spC},
        [(YA["2"], YA["6"])], [(s, "F1", s - FB / 2, s + FB / 2) for s in cC],
        beam_supports=[(YA["1"], [NIV[0] - LOSA - HV])],
        notes=[((YA["2"] + YA["3"]) / 2 + 0.15, 5.0, "PATIO P1"),
               ((YA["2"] + YA["3"]) / 2 + 0.15, 4.65, "SIN VIGAS"),
               ((YA["2"] + YA["3"]) / 2 + 0.15, 4.30, "(CERCHA"),
               ((YA["2"] + YA["3"]) / 2 + 0.15, 3.95, "CONTINUA)"),
               (YA["1"] + 2.6, 1.6, "SIN COLUMNA EN EL N1 (PORTÓN)"),
               (YA["1"] + 2.6, 1.15, "C1 DE N2 Y N3 SOBRE LA VT-1 DEL EJE 1")])
FR.append(("PÓRTICO C", "EJES 1 A 6 (COLUMNAS FORRADAS A 0,30 x 0,30)", fC, SPAN_L))

axT = {"A": XA, "C": XC, "D": XD}
SPAN_T = (XA - 2.6, XD + 4.3)
foot = [(XA, "F2", 0.0, FB), (XC, "F1", XC - FB / 2, XC + FB / 2), (XD, "F2", W - FB, W)]
sp = [(XA, XD)]
TR = (0.30, H.EJES_X["B"], XC, W - 0.30)
f26 = Frame(40.0, 0.0)
f26.draw(axT, [XA, XC, XD], {"N2": sp, "N3": sp, "COR": sp}, [(XA, XD)], foot, truss=TR)
FR.append(("PÓRTICOS 2 A 6", "EJES A, C Y D", f26, SPAN_T))
f1 = Frame(60.0, 0.0)
f1.draw(axT, [XA, XD, (XC, NIV[0] - LOSA)], {"N2": [(XA, XD, "VT-1")], "N3": sp, "COR": sp},
        [(XA, XD)], [foot[0], foot[2]], truss=TR,
        notes=[(XC, 1.6, "SIN COLUMNA EN EL N1 (PORTÓN)"),
               (XC, 1.15, "VT-1: DISEÑO ESPECIAL (PD)")])
FR.append(("PÓRTICO 1", "EJES A, C Y D (FACHADA FRONTAL)", f1, SPAN_T))

# ================================================================ hoja
psp = doc.layouts.new(LAYOUT)
psp.page_setup(size=(cl.A1_W, cl.A1_H), margins=(0, 0, 0, 0), units="mm")
doc.layouts.set_active_layout(LAYOUT)
cl.frame(psp)
f = 1000.0 / SC
ZLO, ZHI = -HP - TP - 0.70, COR + 2.00
vh = (ZHI - ZLO) * f
wL, wT = (SPAN_L[1] - SPAN_L[0]) * f, (SPAN_T[1] - SPAN_T[0]) * f
places = [(35.0, 568.0), (35.0, 395.0), (35.0 + wL + 12.0, 568.0), (35.0 + wL + wT + 24.0, 568.0)]
for (tit, sub, fr, span), (px, py) in zip(FR, places):
    vw = (span[1] - span[0]) * f
    mc = (fr.ox + (span[0] + span[1]) / 2, fr.oy + (ZLO + ZHI) / 2)
    v = psp.add_viewport(center=(px + vw / 2, py - vh / 2), size=(vw, vh), view_center_point=mc,
                         view_height=vh * SC / 1000.0, dxfattribs={"layer": "A-VIEWPORT"})
    v.dxf.flags = v.dxf.flags | 16384
    cl.text(psp, tit, (px, py - vh - 4.0), 4.5, "A-TITULOS", "TOP_LEFT")
    cl.text(psp, f"{sub} - Esc. 1:{SC}", (px, py - vh - 10.5), 2.5, "A-TEXTO", "TOP_LEFT")

XT, YT = 35.0 + wL + 25.0, 395.0
cl.view_title(psp, XT, YT - 6.0, "DETALLE DE PÓRTICOS", "EJES LONGITUDINALES Y TRANSVERSALES",
              f"Esc. 1:{SC}", 170)
y = YT - 34.0
cl.text(psp, "SIMBOLOGÍA ELEMENTOS PORTANTES", (XT, y), 3.5, "A-TITULOS", "TOP_LEFT")
rows = [["C1", "COLUMNA - TUBO DE ACERO 6x6\" EN 3,17 mm [PR]"],
        ["V1", "VIGA - TUBO DE ACERO 4x8\" EN 3,17 mm [PR]"],
        ["VT-1", "VIGA DE TRANSFERENCIA, EJE 1 EN N2 - DISEÑO ESPECIAL (PD)"],
        ["VA1", "VIGA RIOSTRA 0,20 x 0,40, 6 #4, AROS #3 @20 cm [PR]"],
        ["F1 / F2", "PLACA 1,65 x 1,65 x 0,25 CENTRADA / EXCÉNTRICA (C02) [PR]"]]
y = cl.table(psp, XT, y - 6.0, [20, 165], rows, row_h=6.5, h=2.2,
             aligns=["MIDDLE_CENTER", "MIDDLE_LEFT"])
y -= 10.0
cl.text(psp, "NOTAS:", (XT, y), 3.5, "A-TITULOS", "TOP_LEFT")
notas = [
    "TODAS LAS MEDIDAS ESTÁN DADAS EN METROS, SALVO INDICACIÓN CONTRARIA. [PR]",
    "ELEVACIONES ESQUEMÁTICAS. UBICACIÓN DE COLUMNAS Y VIGAS SEGÚN C01, C03 Y C04; PLACAS, "
    "PEDESTALES Y VIGAS RIOSTRA SEGÚN C01 Y C02.",
    "COLUMNAS C1 CONTINUAS DESDE LA PLACA HASTA LA VIGA DE CORONA (+9,00). LAS DEL EJE C VAN "
    "FORRADAS A 0,30 x 0,30 (A2-A4).",
    "EJE C EN EL EJE 1: SIN COLUMNA EN EL NIVEL 1 (PORTÓN). LA C1 DE LOS NIVELES 2 Y 3 ARRANCA "
    "SOBRE LA VIGA DE TRANSFERENCIA VT-1 DEL EJE 1 (ENTREPISO DEL NIVEL 2), DE DISEÑO ESPECIAL "
    "SEGÚN LA MEMORIA DE CÁLCULO (PD).",
    "VIGAS V1 DE ENTREPISO CON LA CARA SUPERIOR A 0,10 BAJO EL NPT (PAQUETE 0,30 = V1 0,20 + "
    "LOSA 0,10, VER C03); V1 DE CORONA CON LA CARA SUPERIOR A +9,00 (VER C04).",
    "UNIONES VIGA-COLUMNA SOLDADAS Y VERIFICACIÓN DE PERFILES SEGÚN MEMORIA DE CÁLCULO (PD).",
    "MATERIALES, PROTECCIÓN ANTICORROSIVA Y ESPECIFICACIONES SEGÚN LÁMINA C06.",
    "LAS SECCIONES SON LAS DEL PROYECTO DE REFERENCIA, POR INDICACIÓN DEL INGENIERO "
    "RESPONSABLE; NO SUSTITUYEN LA MEMORIA DE CÁLCULO.",
]
cl.notes_block(psp, XT, y - 6, [f"{i}.- {t}" for i, t in enumerate(notas, 1)] + [cl.NOTA_PR], 2.1,
               705.0 - XT)

H.titleblock(doc, psp, SHEET, "PÓRTICOS",
             ["PÓRTICOS A Y D.", "PÓRTICO C.", "PÓRTICOS 2 A 6.", "PÓRTICO 1.",
              "SIMBOLOGÍA Y NOTAS.", ""],
             [("0", "06-10-2026", "VERSIÓN DE TRABAJO PARA REVISIÓN"),
              ("1", "06-10-2026", "C05 Y C06 UNIFICADAS; C1 EJE C-1 EN N2-N3 SOBRE VT-1"),
              ("2", "06-10-2026", "REFERENCIA A LÁMINA C06")],
             escalas=f"1:{SC}")

OUT.mkdir(parents=True, exist_ok=True)
doc.saveas(OUT / f"{NAME}.dxf")
cl.render_pdf(doc, LAYOUT, OUT / f"{NAME}.pdf")
print("DXF:", OUT / f"{NAME}.dxf")
