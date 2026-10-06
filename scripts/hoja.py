"""Piezas comunes de las láminas de planta (A3 en adelante): lote, ejes, columnas,
cotas generales, viewport 1:50, norte, título, derrotero, cobertura y cajetín."""
import cadlib as cl
import planta as pl
from planta import P

prj = cl.load_project()
G = prj["geometria_m"]
lote, V, LOC, FRAME = pl.lot_model()

E, I = G["muro_ext"], G["muro_int"]
W = 9.0
EY0, EY1 = G["envolvente_y"]                 # 2.06 / 25.18
C = G["cadena_y"]
P1, P2, ESC = G["patio_P1"], G["patio_P2"], G["escalera"]
XB0, XB1 = 1.35, 1.47                        # muro eje B (pasillo)
XC = 4.84                                    # eje C (centro de columnas)
Y_P1a, Y_P1b = P1["y"]                       # 7.76 / 10.26
Y2a, Y2b = Y_P1a - E, Y_P1a                  # muro eje 2 (7.61-7.76)
Y3a, Y3b = Y_P1b, Y_P1b + E                  # muro eje 3 (10.26-10.41)
Y4a, Y4b = C["sba"] - E, C["sba"]            # muro eje 4 (16.83-16.98)
Y5a, Y5b = C["sbb"], C["sbb"] + E            # muro eje 5 (19.48-19.63)
YF0, YF1 = EY0, EY0 + E                      # fachada frontal (2.06-2.21)
YR0, YR1 = EY1 - E, EY1                      # fachada posterior (25.03-25.18)
Y_LP = LOC[5][1]
EJES_X = {"A": E / 2, "B": (XB0 + XB1) / 2, "C": XC, "D": W - E / 2}
EJES_Y = {"1": EY0 + E / 2, "2": (Y2a + Y2b) / 2, "3": (Y3a + Y3b) / 2,
          "4": (Y4a + Y4b) / 2, "5": (Y5a + Y5b) / 2, "6": EY1 - E / 2}
COLS = {"2": EJES_Y["2"], "3": EJES_Y["3"], "4": EJES_Y["4"], "5": EJES_Y["5"],
        "6": EY1 - 0.15}
A_CAT = lote["area_catastro_m2"]
A_ENV = W * (EY1 - EY0)
A_PAT = (P1["x"][1] - P1["x"][0]) * (Y_P1b - Y_P1a) + (P2["x"][1] - P2["x"][0]) * (
    P2["y"][1] - P2["y"][0])
A_HUELLA = A_ENV - A_PAT
A_N1 = 66.57                                 # área construida nivel 1 (lámina A2 rev1)


def lot(msp):
    pl.poly(msp, [LOC[k] for k in (1, 2, 3, 4, 5)], "T-LINDERO")
    for k, (x, y) in LOC.items():
        msp.add_circle(P(x, y), 0.18, dxfattribs={"layer": "T-VERTICE"})
        off = {1: (-0.35, -0.35), 2: (-0.35, -0.35), 3: (9.35, -0.35), 4: (9.35, 28.85),
               5: (-0.35, 28.85)}[k]
        pl.text(msp, str(k), off[0], off[1], 0.18, "T-VERTICE")


def columns(msp, label=True):
    for k, yc in COLS.items():
        pts = [P(XC - 0.15, yc - 0.15), P(XC + 0.15, yc - 0.15), P(XC + 0.15, yc + 0.15),
               P(XC - 0.15, yc + 0.15)]
        msp.add_lwpolyline(pts, close=True, dxfattribs={"layer": "E-COLUMNA"})
        h = msp.add_hatch(color=7, dxfattribs={"layer": "E-COLUMNA"})
        h.paths.add_polyline_path(pts)
        if label:
            pl.text(msp, f"C{k}", XC + 0.27, yc + 0.27, 0.10, "E-COLUMNA", "MIDDLE_LEFT")


def axes(msp):
    for k, x in EJES_X.items():
        pl.axis(msp, k, "x", x, -0.2, 29.85, "end")
    for k, y in EJES_Y.items():
        pl.axis(msp, k, "y", y, -2.35, 10.2, "start")


def general_dims(msp):
    for ya, yb in ((0.0, EY0), (EY0, EY1), (EY1, Y_LP)):
        pl.dim(msp, (0, ya), (0, yb), (-1.75, 0), False)
    ys = list(EJES_Y.values())
    for ya, yb in zip(ys[:-1], ys[1:]):
        pl.dim(msp, (E / 2, ya), (E / 2, yb), (-1.15, 0), False)
    xs = list(EJES_X.values())
    for xa, xb in zip(xs[:-1], xs[1:]):
        pl.dim(msp, (xa, EY1), (xb, EY1), (0, 29.25), True)
    pl.dim(msp, (W, EY0), (W, EY1), (W + 1.65, 0), False)
    pl.dim(msp, (0.0, EY0), (W, EY0), (0, -1.35), True)


def sections(msp):
    pl.section_mark(msp, "A", "A6", (3.0, -1.6), (3.0, 29.4), (1, 0))
    pl.section_mark(msp, "B", "A6", (-2.0, 18.25), (11.05, 18.25), (0, 1))


def sheet(doc, layout, title, subtitle):
    psp = doc.layouts.new(layout)
    psp.page_setup(size=(cl.A1_W, cl.A1_H), margins=(0, 0, 0, 0), units="mm")
    doc.layouts.set_active_layout(layout)
    cl.frame(psp)
    vp = psp.add_viewport(center=(368.0, 430.0), size=(668.0, 296.0),
                          view_center_point=(14.05, 4.05), view_height=296 * 50 / 1000.0,
                          dxfattribs={"layer": "A-VIEWPORT"})
    vp.dxf.flags = vp.dxf.flags | 16384
    vp.frozen_layers = ["T-TXT-100", "T-TXT-200", "T-COTA-100", "T-COTA-200"]
    return psp


def north(psp, north_ang):
    psp.add_blockref("NORTE", (672.0, 300.0), dxfattribs={"layer": "A-NORTE",
                                                           "rotation": north_ang - 90.0})
    cl.text(psp, "NORTE SEGÚN CATASTRO", (672.0, 280.0), 1.8, "A-TEXTO", "TOP_CENTER")


def title_and_derrotero(psp, title, subtitle):
    cl.view_title(psp, 35.0, 262.0, title, subtitle, "Esc. 1:50", 150)
    cl.scale_bar(psp, 35.0, 236.0, 50, 5, 1)
    y = 222.0
    cl.text(psp, "D E R R O T E R O", (35 + 95, y), 5.0, "A-TITULOS", "TOP_CENTER")
    y = cl.table(psp, 35.0, y - 8, [38.0] * 5, cl.derrotero_rows(V), row_h=6.0, h=2.5)
    cl.text(psp, "VER CUADRO DE COORDENADAS CRTM05 EN LÁMINA A1.", (35.0, y - 2.0), 2.0,
            "A-TEXTO", "TOP_LEFT")


def cobertura(psp, x, y):
    cl.text(psp, "PORCENTAJE DE COBERTURA", (x + 100, y), 4.5, "A-TITULOS", "TOP_CENTER")
    rows = [["CONCEPTO", "VALOR"],
            ["ÁREA DE LOTE (SEGÚN CATASTRO)", cl.m2(A_CAT)],
            ["HUELLA CONSTRUCTIVA (PROYECCIÓN NIVELES 2 Y 3)", cl.m2(A_HUELLA)],
            ["% COBERTURA", f"{A_HUELLA / A_CAT * 100:.2f} %".replace(".", ",")]]
    y = cl.table(psp, x, y - 8, [140, 60], rows, row_h=6.0, h=2.5,
                 aligns=["MIDDLE_LEFT", "MIDDLE_RIGHT"])
    cl.text(psp, f"CÁLCULO: (HUELLA / ÁREA DE LOTE) x 100 = ({A_HUELLA:.2f} / {A_CAT:.2f}) x 100"
            f" = {A_HUELLA / A_CAT * 100:.2f} %".replace(".", ","), (x, y - 1.5), 2.0,
            "A-TEXTO", "TOP_LEFT")
    return y - 6


def titleblock(doc, psp, lamina, cont_tit, cont, revs):
    vals = {
        "EMPRESA": prj["empresa"], "EMPRESA_CED": prj["empresa_ced"],
        "PROF_1": prj["profesionales"][0], "PROF_2": prj["profesionales"][1],
        "PROF_3": prj["profesionales"][2],
        "PROYECTO": prj["proyecto"], "UBIC_1": prj["ubicacion"][0],
        "UBIC_2": prj["ubicacion"][1], "UBIC_3": "",
        "REG_1": prj["registro"][0], "REG_2": prj["registro"][1], "REG_3": prj["registro"][2],
        "CONT_TIT": cont_tit, "ESCALAS": "1:50 / INDICADAS",
        "ESTADO_1": "VERSIÓN DE TRABAJO", "ESTADO_2": "NO APTA PARA CONSTRUCCIÓN NI TRÁMITE",
        "LUGAR": "COSTA RICA", "LAMINA": lamina, "FECHA": prj["fecha"],
        "TOTAL": prj["total_laminas"],
    }
    for i in range(6):
        vals[f"CONT_{i + 1}"] = cont[i] if i < len(cont) else ""
    for i in range(3):
        n, f, d = revs[i] if i < len(revs) else ("", "", "")
        vals[f"REV{i}_N"], vals[f"REV{i}_F"], vals[f"REV{i}_D"] = n, f, d
    cl.insert_titleblock(doc, psp, vals)


def extractor_detail(psp, x, y):
    """Detalle esquemático (S/E) de extractor mecánico en baño. Unidades: mm de papel."""
    cl.text(psp, "DETALLE EXTRACTOR DE AIRE", (x, y), 4.5, "A-TITULOS", "TOP_LEFT")
    cl.text(psp, "BAÑOS - ESQUEMÁTICO, Esc. S/E", (x, y - 7), 2.5, "A-TEXTO", "TOP_LEFT")
    y0 = y - 70
    L = "A-TEXTO"
    # losa / cielo
    cl.rect(psp, x, y0 + 40, x + 110, y0 + 46, "A-MURO")
    h = psp.add_hatch(dxfattribs={"layer": "A-MURO-TRAMA"})
    h.paths.add_polyline_path([(x, y0 + 40), (x + 110, y0 + 40), (x + 110, y0 + 46),
                               (x, y0 + 46)])
    h.set_pattern_fill("ANSI31", scale=0.5)
    psp.add_line((x, y0 + 34), (x + 96, y0 + 34), dxfattribs={"layer": L})        # cielo
    # muro exterior
    cl.rect(psp, x + 96, y0, x + 102, y0 + 40, "A-MURO")
    h = psp.add_hatch(dxfattribs={"layer": "A-MURO-TRAMA"})
    h.paths.add_polyline_path([(x + 96, y0), (x + 102, y0), (x + 102, y0 + 40), (x + 96, y0 + 40)])
    h.set_pattern_fill("ANSI31", scale=0.5)
    # extractor en cielo + ducto al exterior
    cl.rect(psp, x + 30, y0 + 30, x + 42, y0 + 34, "A-MOBILIARIO")
    psp.add_line((x + 33, y0 + 36), (x + 104, y0 + 36), dxfattribs={"layer": L})
    psp.add_line((x + 39, y0 + 38.5), (x + 104, y0 + 38.5), dxfattribs={"layer": L})
    psp.add_line((x + 33, y0 + 34), (x + 33, y0 + 36), dxfattribs={"layer": L})
    psp.add_line((x + 39, y0 + 34), (x + 39, y0 + 38.5), dxfattribs={"layer": L})
    cl.rect(psp, x + 104, y0 + 34.5, x + 106, y0 + 40, "A-MOBILIARIO")        # rejilla
    for i in range(4):
        psp.add_line((x + 50 + i * 8, y0 + 37.25), (x + 55 + i * 8, y0 + 37.25),
                     dxfattribs={"layer": L})
    cl.mtext(psp, "EXTRACTOR MECÁNICO EN CIELO\\PCAUDAL Y MODELO POR DEFINIR [PR]",
             (x + 2, y0 + 28), 2.0, 50, attach=7)
    cl.mtext(psp, "DUCTO AL EXTERIOR CON\\PREJILLA Y COMPUERTA ANTIRRETORNO", (x + 45, y0 + 52),
             2.0, 60, attach=7)
    cl.mtext(psp, "ENCENDIDO CON LA LUZ DEL BAÑO\\PO TEMPORIZADOR (VER ELÉCTRICOS)",
             (x + 2, y0 + 20), 2.0, 60, attach=7)
    return y0 - 4
