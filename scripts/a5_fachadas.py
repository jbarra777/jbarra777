"""Lámina A5 - FACHADAS (principal 1:50, posterior 1:75, laterales 1:100).

Criterio acordado: fachadas sencillas; en la principal las ventanas van de piso a
2.20 m sobre NPT y alineadas entre niveles (franja opaca entre ventana y losa), para
modelar luego una fachada moderna. Baños con vidrio arenado (sandblast).
Model Space en metros: cada fachada en su propio origen (H horizontal, V = altura).
"""
import cadlib as cl
import hoja as H

REV = "rev0"
OUT = cl.ROOT / "planos" / "A5_fachadas"
NAME = f"SR-A5_FACHADAS_{REV}"

W = 9.0
NIV = {"N1": 0.0, "N2": 3.00, "N3": 6.00, "CUB": 9.00, "PRE": 9.60}
HEAD = 2.20                                     # dintel de ventanas sobre NPT
POR_H = 2.40                                    # altura portón / puerta peatonal (PR)
EY0, EY1, Y_LP = H.EY0, H.EY1, H.Y_LP

doc = cl.new_doc()
msp = doc.modelspace()
for name, col, lw, lt in (("F-CONTORNO", 7, 50, "Continuous"), ("F-VANOS", 7, 35, "Continuous"),
                          ("F-VIDRIO", 8, 13, "Continuous"), ("F-LINEAS", 8, 18, "Continuous"),
                          ("F-OCULTO", 8, 13, "DASHED"), ("F-TERRENO", 7, 70, "Continuous"),
                          ("F-TRAMA", 8, 9, "Continuous"), ("F-COTA", 7, 18, "Continuous"),
                          ("F-TXT", 7, 18, "Continuous"), ("F-NIVEL", 7, 18, "Continuous")):
    doc.layers.add(name, color=col, linetype=lt, lineweight=lw)


class Elev:
    def __init__(self, ox, scale):
        self.ox = ox
        self.k = scale / 1000.0             # m de modelo por mm de papel
        self.ds = {50: "COTA-50", 75: "COTA-75", 100: "COTA-100"}[scale]

    def p(self, h, v):
        return (self.ox + h, v)

    def line(self, a, b, layer="F-LINEAS", lts=None):
        e = msp.add_line(self.p(*a), self.p(*b), dxfattribs={"layer": layer})
        if lts:
            e.dxf.ltscale = lts
        return e

    def rect(self, h0, v0, h1, v1, layer="F-VANOS"):
        return msp.add_lwpolyline([self.p(h0, v0), self.p(h1, v0), self.p(h1, v1),
                                   self.p(h0, v1)], close=True, dxfattribs={"layer": layer})

    def glass(self, h0, v0, h1, v1):
        """Marca de vidrio: dos diagonales cortas."""
        w, hh = h1 - h0, v1 - v0
        for f in (0.55, 0.70):
            a = (h0 + w * (f - 0.12), v0 + hh * (f - 0.12))
            b = (h0 + w * (f + 0.0), v0 + hh * (f + 0.0))
            self.line(a, b, "F-VIDRIO")

    def window(self, h0, h1, v0, v1, mullions=0, transom=None, sand=False):
        self.rect(h0, v0, h1, v1)
        self.rect(h0 + 0.05, v0 + 0.05, h1 - 0.05, v1 - 0.05, "F-VIDRIO")
        for i in range(1, mullions + 1):
            hm = h0 + (h1 - h0) * i / (mullions + 1)
            self.line((hm, v0), (hm, v1), "F-VANOS")
        if transom:
            self.line((h0, v0 + transom), (h1, v0 + transom), "F-VANOS")
        if sand:
            ht = msp.add_hatch(dxfattribs={"layer": "F-TRAMA"})
            ht.paths.add_polyline_path([self.p(h0 + 0.05, v0 + 0.05), self.p(h1 - 0.05, v0 + 0.05),
                                        self.p(h1 - 0.05, v1 - 0.05), self.p(h0 + 0.05, v1 - 0.05)])
            ht.set_pattern_fill("DOTS", scale=0.95 * self.k)
        else:
            self.glass(h0, v0, h1, v1)

    def text(self, s, h, v, size_mm=2.2, align="MIDDLE_CENTER", rot=0, layer="F-TXT"):
        return cl.text(msp, s, self.p(h, v), size_mm * self.k, layer, align, rot)

    def mtext(self, s, h, v, size_mm=2.0, width_mm=40, attach=5):
        return cl.mtext(msp, s, self.p(h, v), size_mm * self.k, width_mm * self.k,
                        layer="F-TXT", attach=attach)

    def hdim(self, a, b, v_base):
        d = msp.add_linear_dim(base=self.p(0, v_base), p1=self.p(a, v_base), p2=self.p(b, v_base),
                               angle=0, dimstyle=self.ds, dxfattribs={"layer": "F-COTA"})
        d.render()

    def vdim(self, a, b, h_base, h_pt=None):
        hp = h_base if h_pt is None else h_pt
        d = msp.add_linear_dim(base=self.p(h_base, 0), p1=self.p(hp, a), p2=self.p(hp, b),
                               angle=90, dimstyle=self.ds, dxfattribs={"layer": "F-COTA"})
        d.render()

    def level(self, h, v, label):
        s = 1.6 * self.k
        x, y = self.p(h, v)
        msp.add_lwpolyline([(x - s, y + s), (x + s, y + s), (x, y)], close=True,
                           dxfattribs={"layer": "F-NIVEL"})
        msp.add_line((x - s, y + s), (x + 18 * self.k, y + s), dxfattribs={"layer": "F-NIVEL"})
        cl.text(msp, label, (x + 2.5 * self.k, y + s + 0.6 * self.k), 1.9 * self.k, "F-NIVEL",
                "BOTTOM_LEFT")

    def axis(self, h, label, v_top, v_bot):
        e = msp.add_line(self.p(h, v_top), self.p(h, v_bot), dxfattribs={"layer": "A-EJES"})
        e.dxf.ltscale = 0.05 * self.k / 0.05 * 1.0
        r = 3.5 * self.k
        c = self.p(h, v_bot - r)
        msp.add_circle(c, r, dxfattribs={"layer": "A-EJES-TXT"})
        cl.text(msp, label, c, 3.0 * self.k, "A-EJES-TXT", "MIDDLE_CENTER")


def _ds75(doc):
    if "COTA-75" not in doc.dimstyles:
        cl._dimstyle(doc, "COTA-75", 75)


_ds75(doc)

# ================================================================ FACHADA PRINCIPAL (norte)
F = Elev(0.0, 50)


def hx(x):
    """Fachada principal: vista desde la calle, el este queda a la izquierda."""
    return W - x


F.line((-1.5, 0), (W + 1.5, 0), "F-TERRENO")
F.rect(0, 0, W, NIV["PRE"], "F-CONTORNO")                 # volumen
F.line((0, NIV["CUB"]), (W, NIV["CUB"]), "F-OCULTO", 0.08)  # losa de cubierta (oculta)
for lv in ("N2", "N3"):
    F.line((0, NIV[lv]), (W, NIV[lv]), "F-OCULTO", 0.08)
# muros de colindancia (franjas laterales)
for x0, x1 in ((0.0, 0.15), (8.85, 9.0)):
    F.line((hx(x0), 0), (hx(x0), NIV["PRE"]), "F-LINEAS")
    F.line((hx(x1), 0), (hx(x1), NIV["PRE"]), "F-LINEAS")
# Nivel 1: portón vehicular, pilastra y puerta peatonal
PV = (hx(8.85), hx(1.56))                                # 0.15 - 7.44
PP = (hx(1.26), hx(0.15))                                # 7.74 - 8.85
F.rect(PV[0], 0, PV[1], POR_H)
for i in range(1, 4):
    hm = PV[0] + (PV[1] - PV[0]) * i / 4
    F.line((hm, 0), (hm, POR_H), "F-VANOS")
for i in range(1, 12):
    v = POR_H * i / 12
    F.line((PV[0] + 0.05, v), (PV[1] - 0.05, v), "F-VIDRIO")
F.rect(PP[0] + 0.05, 0, PP[1] - 0.06, POR_H)
F.line((PP[0] + 0.85, 1.05), (PP[0] + 0.85, 1.25), "F-VANOS")       # jaladera
F.line((PV[0], POR_H), (PP[1], POR_H), "F-LINEAS")                # fascia sobre portón
F.mtext("PORTÓN ABATIBLE\\P4 HOJAS (PLEGABLES)", (PV[0] + PV[1]) / 2, 1.2, 2.2, 45)
F.mtext("ACCESO\\PPEATONAL", (PP[0] + PP[1]) / 2, 1.8, 1.8, 18)
F.mtext("VIGA / FASCIA\\P(PERALTE SEGÚN ESTRUCTURAL)", 3.8, 2.70, 1.8, 50)
# Niveles 2 y 3: ventanas de piso a 2.20 m, alineadas
VENT = [((0.70, 2.90), "DORM.", 1, False), ((3.95, 4.95), "BAÑO", 0, True),
        ((6.40, 8.20), "WALK-IN", 1, False)]
for lv in ("N2", "N3"):
    v0 = NIV[lv]
    for (xa, xb), lab, mul, sand in VENT:
        F.window(hx(xb), hx(xa), v0, v0 + HEAD, mullions=mul, transom=None if sand else 0.90,
                 sand=sand)
    F.line((0.15, v0 + HEAD + 0.0), (8.85, v0 + HEAD), "F-LINEAS")   # inicio franja opaca
F.text("VIDRIO ARENADO", hx(4.45), NIV["N2"] + 1.1, 1.8, rot=90)
F.text("VIDRIO ARENADO", hx(4.45), NIV["N3"] + 1.1, 1.8, rot=90)
F.mtext("FRANJA OPACA (VIGA Y LOSA)", 4.5, NIV["N3"] + 2.60, 1.8, 60)
F.mtext("PRETIL (ALTURA POR DEFINIR)", 4.5, 9.30, 1.8, 60)
# cotas
for lv, lab in (("N1", "NPT ±0.00 (ACERA)"), ("N2", "NPT +3.00"), ("N3", "NPT +6.00"),
                ("CUB", "CUBIERTA +9.00 (PD)"), ("PRE", "PRETIL +9.60 (PD)")):
    F.level(W + 0.6, NIV[lv], lab)
chain_v = [0.0, POR_H, 3.00, 3.00 + HEAD, 6.00, 6.00 + HEAD, 9.00, NIV["PRE"]]
for a, b in zip(chain_v[:-1], chain_v[1:]):
    F.vdim(a, b, -0.70, 0.0)
F.vdim(0.0, NIV["PRE"], -1.40, 0.0)
hs = sorted({0.0, W} | {hx(x) for (xa, xb), *_ in VENT for x in (xa, xb)})
for a, b in zip(hs[:-1], hs[1:]):
    F.hdim(a, b, NIV["PRE"] + 0.55)
F.hdim(0.0, W, NIV["PRE"] + 1.15)
for a, b in ((0.0, 0.15), (0.15, 7.44), (7.44, 7.74), (7.74, 8.85), (8.85, 9.0)):
    F.hdim(a, b, -0.55)
for lab, x in H.EJES_X.items():
    F.axis(hx(x), lab, -0.9, -1.0)

# ================================================================ FACHADA POSTERIOR (sur)
PO = Elev(30.0, 75)
PO.line((-1.5, 0), (W + 1.5, 0), "F-TERRENO")
PO.rect(0, NIV["N2"] - 0.40, W, NIV["PRE"], "F-CONTORNO")        # volumen sobre N1
PO.rect(0, 0, 0.15, NIV["N2"] - 0.40, "F-CONTORNO")              # muro colindancia oeste
PO.rect(W - 0.15, 0, W, NIV["N2"] - 0.40, "F-CONTORNO")          # muro colindancia este
PO.rect(4.69, 0, 4.99, NIV["N2"] - 0.40, "F-CONTORNO")           # columna C6
PO.mtext("NIVEL 1 ABIERTO\\P(JARDÍN SECO)", 2.4, 1.3, 2.0, 40)
PO.line((0, NIV["CUB"]), (W, NIV["CUB"]), "F-OCULTO", 0.08)
PO.line((0, NIV["N3"]), (W, NIV["N3"]), "F-OCULTO", 0.08)
# N2 sala (antepecho 0.90); N3 suite 3: dormitorio 0.90, baño y walk-in altos 1.60
for xa, xb in ((0.90, 3.90), (5.00, 8.00)):
    PO.window(xa, xb, 3.00 + 0.90, 3.00 + HEAD, mullions=1)
PO.window(0.70, 2.90, 6.00 + 0.90, 6.00 + HEAD, mullions=1)
PO.window(3.95, 4.95, 6.00 + 1.60, 6.00 + HEAD, sand=True)
PO.window(6.40, 8.20, 6.00 + 1.60, 6.00 + HEAD, mullions=1)
for lv, lab in (("N1", "±0.00"), ("N2", "+3.00"), ("N3", "+6.00"), ("CUB", "+9.00 (PD)"),
                ("PRE", "+9.60 (PD)")):
    PO.level(W + 0.6, NIV[lv], lab)
for a, b in zip([0.0, 2.60, 3.00, 3.90, 5.20, 6.00, 6.90, 7.60, 8.20, 9.00, 9.60][:-1],
                [0.0, 2.60, 3.00, 3.90, 5.20, 6.00, 6.90, 7.60, 8.20, 9.00, 9.60][1:]):
    PO.vdim(a, b, -0.70, 0.0)
for lab, x in H.EJES_X.items():
    PO.axis(x, lab, -0.9, -1.0)

# ================================================================ LATERALES (colindancia)
def lateral(ox, east_side):
    L = Elev(ox, 100)
    hy = (lambda y: Y_LP - y) if east_side else (lambda y: y)
    L.line((hy(0.0), 0), (hy(Y_LP), 0), "F-TERRENO")
    a, b = sorted((hy(EY0), hy(EY1)))
    L.rect(a, 0, b, NIV["PRE"], "F-CONTORNO")
    for lv in ("N2", "N3", "CUB"):
        L.line((a, NIV[lv]), (b, NIV[lv]), "F-OCULTO", 0.15)
    L.mtext("MURO DE COLINDANCIA CIEGO\\P(SIN VENTANAS NI VANOS)", (a + b) / 2, 4.5, 2.4, 80)
    # tapias en retiros (altura por confirmar)
    for ya, yb in ((0.0, EY0), (EY1, Y_LP)):
        c, d = sorted((hy(ya), hy(yb)))
        L.line((c, 2.40), (d, 2.40), "F-OCULTO", 0.15)
    L.mtext("TAPIA\\P(H POR CONFIRMAR)", (hy(EY1) + hy(Y_LP)) / 2, 3.1, 1.8, 30)
    L.text("FRENTE", hy(0.0), -0.6 if True else 0, 2.2)
    L.text("FONDO", hy(Y_LP), -0.6, 2.2)
    for lv, lab in (("N1", "±0.00"), ("N2", "+3.00"), ("N3", "+6.00"), ("PRE", "+9.60 (PD)")):
        L.level(max(hy(0.0), hy(Y_LP)) + 0.6, NIV[lv], lab)
    ys = [0.0, EY0, EY1, Y_LP]
    for ya, yb in zip(ys[:-1], ys[1:]):
        L.hdim(*sorted((hy(ya), hy(yb))), NIV["PRE"] + 0.8)
    for lab, y in H.EJES_Y.items():
        L.axis(hy(y), lab, -1.0, -1.1)
    return L


LE = lateral(60.0, True)
LO = lateral(100.0, False)

# ================================================================ hoja
psp = doc.layouts.new("A5-FACHADAS")
psp.page_setup(size=(cl.A1_W, cl.A1_H), margins=(0, 0, 0, 0), units="mm")
doc.layouts.set_active_layout("A5-FACHADAS")
cl.frame(psp)


def vp(center, size, scale, mc):
    v = psp.add_viewport(center=center, size=size, view_center_point=mc,
                         view_height=size[1] * scale / 1000.0, dxfattribs={"layer": "A-VIEWPORT"})
    v.dxf.flags = v.dxf.flags | 16384
    return v


vp((165.0, 420.0), (260.0, 290.0), 50, (4.75, 4.6))
cl.view_title(psp, 40.0, 262.0, "FACHADA PRINCIPAL (NORTE)", "VISTA DESDE LA CALLE",
              "Esc. 1:50", 130)
vp((385.0, 420.0), (170.0, 290.0), 75, (30.0 + 4.75, 4.6))
cl.view_title(psp, 305.0, 262.0, "FACHADA POSTERIOR (SUR)", "VISTA DESDE EL PATIO POSTERIOR",
              "Esc. 1:75", 130)
vp((198.0, 150.0), (330.0, 150.0), 100, (60.0 + 14.3, 4.4))
cl.view_title(psp, 40.0, 70.0, "FACHADA LATERAL ESTE", "MURO DE COLINDANCIA", "Esc. 1:100", 110)
vp((530.0, 150.0), (330.0, 150.0), 100, (100.0 + 14.3, 4.4))
cl.view_title(psp, 372.0, 70.0, "FACHADA LATERAL OESTE", "MURO DE COLINDANCIA", "Esc. 1:100",
              110)
cl.scale_bar(psp, 40.0, 236.0, 50, 5, 1)
cl.scale_bar(psp, 305.0, 236.0, 75, 5, 1)
cl.scale_bar(psp, 230.0, 52.0, 100, 10, 2)

X3 = 485.0
y = 572.0
cl.text(psp, "NOTAS:", (X3, y), 3.5, "A-TITULOS", "TOP_LEFT")
notas = [
    "TODAS LAS MEDIDAS ESTÁN DADAS EN METROS, SALVO INDICACIÓN CONTRARIA. [PR]",
    "LA TAPIA COLINDANTE DE MAMPOSTERÍA DEBERÁ PROLONGARSE HASTA EL NIVEL DE LA VIGA CORONA "
    "DEL ÚLTIMO NIVEL, GARANTIZANDO EL APANTALLAMIENTO VISUAL PERMANENTE HACIA LA PROPIEDAD "
    "COLINDANTE.",
    "LOS BAÑOS CONTARÁN CON EXTRACTOR MECÁNICO DE AIRE.",
    "NIVELES: NPT N1 ±0.00 (ACERA), N2 +3.00, N3 +6.00. CUBIERTA +9.00 Y PRETIL +9.60 SON "
    "PRELIMINARES (PD = POR DEFINIR CON EL DISEÑO DE TECHOS Y LA ALTURA MÁXIMA MUNICIPAL).",
    "FACHADA PRINCIPAL: VENTANAS DE PISO A 2.20 m SOBRE NPT, ALINEADAS ENTRE NIVELES, CON "
    "FRANJA OPACA HASTA LA LOSA SUPERIOR (VIGAS). COMPOSICIÓN BASE PARA EL DISEÑO MODERNO.",
    "VENTANAS DESDE EL PISO EN NIVELES 2 Y 3: VIDRIO DE SEGURIDAD (TEMPLADO O LAMINADO) Y "
    "PROTECCIÓN CONTRA CAÍDAS EN LA PARTE INFERIOR (PAÑO FIJO LAMINADO HASTA 0.90 m O BARANDA "
    "INTERIOR). VERIFICAR CON LA NORMATIVA VIGENTE.",
    "BAÑOS: VIDRIO ARENADO (SANDBLAST) TEMPLADO. EN LA ZONA DE DUCHA EL VIDRIO DEBE QUEDAR "
    "SELLADO Y CON ANTEPECHO IMPERMEABLE O PANEL OPACO INTERIOR (POR DEFINIR).",
    "FACHADA POSTERIOR: ANTEPECHO 0.90 m EN SALA Y DORMITORIO; 1.60 m EN BAÑO Y WALK-IN.",
    "FACHADAS LATERALES SOBRE COLINDANCIA: MUROS CIEGOS.",
    "PORTÓN Y PUERTA PEATONAL CON ALTURA PRELIMINAR DE 2.40 m. TIPOS DE VENTANAS Y PUERTAS EN "
    "LÁMINAS A7 A A9; ACABADOS DE FACHADA EN LÁMINA A10.",
]
y = cl.notes_block(psp, X3, y - 6, [f"{i}.- {t}" for i, t in enumerate(notas, 1)]
                   + [cl.NOTA_PR], 2.1, 218)
y -= 4
cl.text(psp, "SIMBOLOGÍA:", (X3, y), 3.5, "A-TITULOS", "TOP_LEFT")
y -= 10
for kind, lab in (("glass", "VIDRIO CLARO"), ("sand", "VIDRIO ARENADO (SANDBLAST)"),
                  ("hid", "LÍNEA OCULTA (LOSA / NIVEL)")):
    if kind == "glass":
        cl.rect(psp, X3, y - 3, X3 + 14, y + 3, "F-VANOS")
        psp.add_line((X3 + 5, y - 1.5), (X3 + 8, y + 1.5), dxfattribs={"layer": "F-VIDRIO"})
        psp.add_line((X3 + 7, y - 1.5), (X3 + 10, y + 1.5), dxfattribs={"layer": "F-VIDRIO"})
    elif kind == "sand":
        cl.rect(psp, X3, y - 3, X3 + 14, y + 3, "F-VANOS")
        hh = psp.add_hatch(dxfattribs={"layer": "F-TRAMA"})
        hh.paths.add_polyline_path([(X3, y - 3), (X3 + 14, y - 3), (X3 + 14, y + 3), (X3, y + 3)])
        hh.set_pattern_fill("DOTS", scale=0.95)
    else:
        e = psp.add_line((X3, y), (X3 + 14, y), dxfattribs={"layer": "F-OCULTO"})
        e.dxf.ltscale = 1.5
    cl.text(psp, lab, (X3 + 18, y), 2.3, "A-TEXTO", "MIDDLE_LEFT")
    y -= 9

H.titleblock(doc, psp, "A5", "FACHADAS",
             ["FACHADA PRINCIPAL (NORTE).", "FACHADA POSTERIOR (SUR).", "FACHADA LATERAL ESTE.",
              "FACHADA LATERAL OESTE.", "NOTAS.", ""],
             [("0", "06-10-2026", "VERSIÓN DE TRABAJO PARA REVISIÓN")])

OUT.mkdir(parents=True, exist_ok=True)
doc.saveas(OUT / f"{NAME}.dxf")
cl.render_pdf(doc, "A5-FACHADAS", OUT / f"{NAME}.pdf")
print("DXF:", OUT / f"{NAME}.dxf")
