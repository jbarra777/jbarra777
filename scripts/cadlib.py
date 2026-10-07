"""Utilidades CAD comunes para el juego de planos (ezdxf).

Convenciones:
- Model Space en METROS, escala real 1:1.
- Paper Space (layouts) en MILÍMETROS, formato A1 841 x 594 mm.
- Viewport 1:N -> 1 m de modelo = 1000/N mm de papel.
"""
import json
import math
from pathlib import Path

import ezdxf
from ezdxf import colors
from ezdxf.enums import TextEntityAlignment

ROOT = Path(__file__).resolve().parents[1]
A1_W, A1_H = 841.0, 594.0
# Marco: margen de encuadernación izquierdo 25 mm, demás 10 mm
FRAME = (25.0, 10.0, 831.0, 584.0)
TB_X0 = 711.0  # inicio del cajetín (columna derecha)

FONT = "arial.ttf"

# nombre: (color ACI, grosor 1/100 mm, tipo de línea, imprimible)
LAYERS = {
    "A-MARCO": (7, 70, "Continuous", True),
    "A-CAJETIN": (7, 35, "Continuous", True),
    "A-CAJETIN-TXT": (7, 25, "Continuous", True),
    "A-TITULOS": (7, 35, "Continuous", True),
    "A-TEXTO": (7, 18, "Continuous", True),
    "A-TABLAS": (7, 25, "Continuous", True),
    "A-NOTAS": (7, 18, "Continuous", True),
    "A-ESCALA-GRAF": (7, 18, "Continuous", True),
    "A-NORTE": (7, 25, "Continuous", True),
    "A-IMAGEN-REF": (7, 13, "Continuous", True),
    "A-VIEWPORT": (8, 13, "Continuous", False),
    "A-PENDIENTE": (1, 25, "Continuous", True),
    # Terreno (modelo)
    "T-LINDERO": (7, 50, "Continuous", True),
    "T-VERTICE": (7, 25, "Continuous", True),
    "T-CALLE": (8, 18, "DASHED", True),
    "T-TXT-200": (7, 18, "Continuous", True),
    "T-COTA-200": (7, 18, "Continuous", True),
    "T-TXT-100": (7, 18, "Continuous", True),
    "T-COTA-100": (7, 18, "Continuous", True),
    # Arquitectura en sitio (modelo)
    "A-HUELLA": (7, 35, "Continuous", True),
    "A-HUELLA-TRAMA": (8, 9, "Continuous", True),
    "A-PATIO": (7, 25, "Continuous", True),
    "A-RETIRO": (8, 18, "DASHED2", True),
    # Plantas arquitectónicas (modelo)
    "A-MURO": (7, 50, "Continuous", True),
    "A-MURO-TRAMA": (8, 9, "Continuous", True),
    "A-PUERTA": (7, 25, "Continuous", True),
    "A-VENTANA": (7, 25, "Continuous", True),
    "A-ESCALERA": (7, 25, "Continuous", True),
    "A-VEHICULO": (8, 18, "Continuous", True),
    "A-MOBILIARIO": (8, 18, "Continuous", True),
    "A-DEMARCACION": (8, 18, "DASHED", True),
    "A-PROYECCION": (8, 18, "DASHED", True),
    "A-EJES": (8, 13, "CENTER", True),
    "A-EJES-TXT": (7, 25, "Continuous", True),
    "A-COTA-50": (7, 18, "Continuous", True),
    "A-TXT-50": (7, 18, "Continuous", True),
    "A-ESPACIOS": (7, 25, "Continuous", True),
    "A-NIVELES": (7, 18, "Continuous", True),
    "A-CORTES": (7, 35, "Continuous", True),
    "A-JARDIN": (8, 9, "Continuous", True),
    "E-COLUMNA": (7, 35, "Continuous", True),
}


def new_doc():
    doc = ezdxf.new("R2018", setup=True)
    doc.header["$INSUNITS"] = 6  # metros
    doc.header["$MEASUREMENT"] = 1  # métrico
    doc.header["$LUNITS"] = 2
    doc.header["$LUPREC"] = 2
    doc.header["$AUNITS"] = 1  # grados/min/seg
    doc.header["$LWDISPLAY"] = 1
    doc.header["$PSLTSCALE"] = 1
    doc.header["$LTSCALE"] = 1
    if "ARIAL" not in doc.styles:
        doc.styles.new("ARIAL", dxfattribs={"font": FONT})
    for name, (col, lw, lt, plot) in LAYERS.items():
        lay = doc.layers.add(name, color=col, linetype=lt, lineweight=lw)
        lay.dxf.plot = 1 if plot else 0
    _dimstyle(doc, "COTA-50", 50)
    _dimstyle(doc, "COTA-100", 100)
    _dimstyle(doc, "COTA-200", 200)
    return doc


def _dimstyle(doc, name, scale):
    """Estilo de cota en metros, con tamaño de texto 2.2 mm en papel."""
    k = scale / 1000.0  # m de modelo por mm de papel
    ds = doc.dimstyles.new(name)
    ds.dxf.dimtxsty = "ARIAL"
    ds.dxf.dimtxt = 2.2 * k
    ds.dxf.dimtsz = 1.2 * k  # trazos oblicuos (arquitectónico)
    ds.dxf.dimasz = 1.2 * k
    ds.dxf.dimexe = 1.0 * k
    ds.dxf.dimexo = 1.0 * k
    ds.dxf.dimgap = 0.8 * k
    ds.dxf.dimdle = 1.0 * k
    ds.dxf.dimtad = 1
    ds.dxf.dimtih = 0
    ds.dxf.dimtoh = 0
    ds.dxf.dimdec = 2
    ds.dxf.dimzin = 0
    ds.dxf.dimlunit = 2
    ds.dxf.dimdsep = ord(".")
    ds.dxf.dimclrd = 7
    ds.dxf.dimclre = 7
    ds.dxf.dimclrt = 7
    ds.dxf.dimlwd = 18
    ds.dxf.dimlwe = 13
    ds.dxf.dimscale = 1.0
    return ds


def text(space, s, pos, h, layer="A-TEXTO", align="LEFT", rot=0.0, style="ARIAL"):
    t = space.add_text(s, height=h, rotation=rot,
                       dxfattribs={"layer": layer, "style": style})
    t.set_placement(pos, align=TextEntityAlignment[align])
    return t


def mtext(space, s, pos, h, width, layer="A-NOTAS", attach=1, spacing=1.0):
    m = space.add_mtext(s, dxfattribs={"layer": layer, "style": "ARIAL",
                                       "char_height": h, "width": width,
                                       "attachment_point": attach,
                                       "line_spacing_factor": spacing})
    m.dxf.insert = pos
    return m


def rect(space, x0, y0, x1, y1, layer):
    return space.add_lwpolyline([(x0, y0), (x1, y0), (x1, y1), (x0, y1)],
                                close=True, dxfattribs={"layer": layer})


def table(space, x0, y_top, col_w, rows, row_h=7.0, h=2.5, layer="A-TABLAS",
          txt_layer="A-TEXTO", aligns=None, merge=None):
    """Tabla con líneas y textos independientes (editables).

    rows: lista de listas de textos. Una celda None se fusiona con la anterior.
    Devuelve la coordenada y inferior.
    """
    n = len(rows)
    total_w = sum(col_w)
    xs = [x0]
    for w in col_w:
        xs.append(xs[-1] + w)
    y_bot = y_top - n * row_h
    rect(space, x0, y_bot, x0 + total_w, y_top, layer)
    for i, row in enumerate(rows):
        yt = y_top - i * row_h
        yb = yt - row_h
        if i > 0:
            space.add_line((x0, yt), (x0 + total_w, yt), dxfattribs={"layer": layer})
        j = 0
        while j < len(row):
            span = 1
            while j + span < len(row) and row[j + span] is None:
                span += 1
            if j > 0:
                space.add_line((xs[j], yt), (xs[j], yb), dxfattribs={"layer": layer})
            s = row[j]
            if s:
                a = (aligns[j] if aligns else "MIDDLE_CENTER")
                if a == "MIDDLE_LEFT":
                    p = (xs[j] + 1.5, (yt + yb) / 2)
                elif a == "MIDDLE_RIGHT":
                    p = (xs[j + span] - 1.5, (yt + yb) / 2)
                else:
                    p = ((xs[j] + xs[j + span]) / 2, (yt + yb) / 2)
                text(space, s, p, h, txt_layer, a)
            j += span
    return y_bot


def frame(psp):
    x0, y0, x1, y1 = FRAME
    rect(psp, 0, 0, A1_W, A1_H, "A-VIEWPORT")  # límite de hoja (no imprime)
    rect(psp, x0, y0, x1, y1, "A-MARCO")
    text(psp, "FORMATO A1  841 mm x 594 mm", (x0, 4.0), 1.8, "A-TEXTO")


def scale_bar(psp, x, y, scale, length_m, step_m, label=None, h=2.2):
    """Escala gráfica en papel para una escala 1:scale."""
    mm = 1000.0 / scale
    n = int(round(length_m / step_m))
    bar_h = 1.6
    for i in range(n):
        xa = x + i * step_m * mm
        xb = xa + step_m * mm
        r = rect(psp, xa, y, xb, y + bar_h, "A-ESCALA-GRAF")
        if i % 2 == 0:
            hatch = psp.add_hatch(color=7, dxfattribs={"layer": "A-ESCALA-GRAF"})
            hatch.paths.add_polyline_path([(xa, y), (xb, y), (xb, y + bar_h), (xa, y + bar_h)])
    for i in range(n + 1):
        v = i * step_m
        s = f"{v:g}"
        text(psp, s, (x + v * mm, y - 1.2), h * 0.85, "A-ESCALA-GRAF", "TOP_CENTER")
    text(psp, label or "m", (x + n * step_m * mm + 3, y + bar_h / 2), h * 0.85,
         "A-ESCALA-GRAF", "MIDDLE_LEFT")


def view_title(psp, x, y, title, sub, scale_txt, w=120):
    text(psp, title, (x, y), 6.0, "A-TITULOS", "BOTTOM_LEFT")
    psp.add_line((x, y - 1.5), (x + w, y - 1.5), dxfattribs={"layer": "A-TITULOS"})
    text(psp, sub, (x, y - 7.5), 3.5, "A-TEXTO", "BOTTOM_LEFT")
    text(psp, scale_txt, (x, y - 13.0), 3.0, "A-TEXTO", "BOTTOM_LEFT")


def north_block(doc):
    if "NORTE" in doc.blocks:
        return
    b = doc.blocks.new("NORTE")
    # flecha de 24 mm (unidad de bloque = mm de papel)
    b.add_lwpolyline([(0, 12), (-4.5, -9), (0, -5), (4.5, -9)], close=True,
                     dxfattribs={"layer": "0"})
    h = b.add_hatch(color=0, dxfattribs={"layer": "0"})
    h.paths.add_polyline_path([(0, 12), (0, -5), (-4.5, -9)])
    b.add_circle((0, 0), 10.5, dxfattribs={"layer": "0"})
    t = b.add_text("N", height=5.0, dxfattribs={"layer": "0", "style": "ARIAL"})
    t.set_placement((0, 14.5), align=TextEntityAlignment.BOTTOM_CENTER)


def vertex_block(doc):
    if "VERTICE" in doc.blocks:
        return
    b = doc.blocks.new("VERTICE")
    b.add_circle((0, 0), 0.35, dxfattribs={"layer": "0"})


def titleblock_block(doc):
    """Cajetín A1 como bloque con atributos editables (unidades mm)."""
    if "CAJETIN_A1" in doc.blocks:
        return
    b = doc.blocks.new("CAJETIN_A1")
    x0, x1 = 0.0, FRAME[2] - TB_X0  # ancho 120 mm
    W = x1 - x0
    top = FRAME[3] - FRAME[1]  # 574 mm de alto, origen en esquina inferior izq.
    L = "0"

    def hline(y):
        b.add_line((x0, y), (x1, y), dxfattribs={"layer": L})

    def label(s, x, y, h=2.2):
        t = b.add_text(s, height=h, dxfattribs={"layer": L, "style": "ARIAL"})
        t.set_placement((x, y), align=TextEntityAlignment.TOP_LEFT)

    def att(tag, x, y, h, align="TOP_LEFT", default=""):
        a = b.add_attdef(tag, insert=(x, y), height=h, text=default,
                         dxfattribs={"layer": L, "style": "ARIAL"})
        a.set_placement((x, y), align=TextEntityAlignment[align])

    b.add_lwpolyline([(x0, 0), (x1, 0), (x1, top), (x0, top)], close=True,
                     dxfattribs={"layer": L})
    # Bloques de arriba hacia abajo (y medido desde abajo)
    # alturas fijas de secciones (mm); el espacio para sellos absorbe el resto
    y_sellos = 62.0 + 18 + 22 + 29 + 22 + 50 + 7 + 6 + 5 + 3 * 5.2 + 19
    label("ESPACIO PARA SELLOS Y TIMBRES", 3, top - 3, 2.0)
    hline(y_sellos)
    # Empresa
    att("EMPRESA", W / 2, y_sellos - 4, 3.2, "TOP_CENTER")
    att("EMPRESA_CED", W / 2, y_sellos - 10, 2.5, "TOP_CENTER")
    y = y_sellos - 18
    hline(y)
    label("PROFESIONAL RESPONSABLE:", 3, y - 2.5)
    att("PROF_1", 3, y - 7.5, 2.6)
    att("PROF_2", 3, y - 12.0, 2.6)
    att("PROF_3", 3, y - 16.5, 2.6)
    y -= 22
    hline(y)
    label("PROYECTO:", 3, y - 2.5)
    att("PROYECTO", 3, y - 7.5, 4.2)
    att("UBIC_1", 3, y - 14.5, 2.5)
    att("UBIC_2", 3, y - 19.0, 2.5)
    att("UBIC_3", 3, y - 23.5, 2.5)
    y -= 29
    hline(y)
    label("INFORMACIÓN REGISTRO PÚBLICO:", 3, y - 2.5)
    att("REG_1", 3, y - 7.5, 2.5)
    att("REG_2", 3, y - 12.0, 2.5)
    att("REG_3", 3, y - 16.5, 2.5)
    y -= 22
    hline(y)
    label("CONTENIDO:", 3, y - 2.5)
    att("CONT_TIT", 3, y - 7.5, 5.0)
    for i in range(1, 7):
        att(f"CONT_{i}", 3, y - 9.5 - i * 5.5, 3.0)
    y -= 50
    hline(y)
    label("ESCALAS:", 3, y - 2.5)
    att("ESCALAS", 25, y - 2.5, 2.2)
    y -= 7
    hline(y)
    # Control de revisiones
    label("CONTROL DE REVISIONES", 3, y - 2.0)
    y -= 6
    hline(y)
    cols = [0, 12, 34, W]
    head = ["REV.", "FECHA", "DESCRIPCIÓN"]
    for i, s in enumerate(head):
        t = b.add_text(s, height=2.0, dxfattribs={"layer": L, "style": "ARIAL"})
        t.set_placement(((cols[i] + cols[i + 1]) / 2, y - 2.5),
                        align=TextEntityAlignment.MIDDLE_CENTER)
    y_head = y
    y -= 5
    hline(y)
    for r in range(3):
        att(f"REV{r}_N", (cols[0] + cols[1]) / 2, y - 2.6, 2.0, "MIDDLE_CENTER")
        att(f"REV{r}_F", (cols[1] + cols[2]) / 2, y - 2.6, 2.0, "MIDDLE_CENTER")
        att(f"REV{r}_D", cols[2] + 1.5, y - 2.6, 2.0, "MIDDLE_LEFT")
        y -= 5.2
        hline(y)
    for c in cols[1:3]:
        b.add_line((c, y_head), (c, y), dxfattribs={"layer": L})
    # Estado
    label("ESTADO:", 3, y - 2.5)
    att("ESTADO_1", W / 2, y - 8.0, 3.0, "TOP_CENTER")
    att("ESTADO_2", W / 2, y - 13.0, 2.4, "TOP_CENTER")
    y -= 19
    hline(y)
    # Lugar / lámina / fecha / total
    xm = 66.0
    r1 = y - 9
    r2 = r1 - 26
    hline(r1)
    hline(r2)
    b.add_line((xm, y), (xm, 0), dxfattribs={"layer": L})
    for s, x in (("LUGAR", xm / 2), ("LÁMINA", (xm + W) / 2)):
        t = b.add_text(s, height=3.0, dxfattribs={"layer": L, "style": "ARIAL"})
        t.set_placement((x, (y + r1) / 2), align=TextEntityAlignment.MIDDLE_CENTER)
    att("LUGAR", xm / 2, (r1 + r2) / 2, 5.0, "MIDDLE_CENTER")
    att("LAMINA", (xm + W) / 2, (r1 + r2) / 2, 14.0, "MIDDLE_CENTER")
    att("FECHA", xm / 2, r2 / 2, 6.0, "MIDDLE_CENTER")
    t = b.add_text("TOTAL", height=3.0, dxfattribs={"layer": L, "style": "ARIAL"})
    t.set_placement((xm + 4, r2 / 2), align=TextEntityAlignment.MIDDLE_LEFT)
    att("TOTAL", xm + 38, r2 / 2, 9.0, "MIDDLE_CENTER")


def load_project():
    return json.loads((ROOT / "datos" / "proyecto.json").read_text(encoding="utf-8"))


def insert_titleblock(doc, psp, values):
    titleblock_block(doc)
    ins = psp.add_blockref("CAJETIN_A1", (TB_X0, FRAME[1]),
                           dxfattribs={"layer": "A-CAJETIN"})
    ins.add_auto_attribs(values)
    for a in ins.attribs:
        a.dxf.layer = "A-CAJETIN-TXT"
    return ins


def render_pdf(doc, layout_name, pdf_path, png_path=None, dpi=150):
    """Genera el PDF de revisión del layout (hoja A1 a escala 1:1 en mm)."""
    from ezdxf.addons.drawing import Frontend, RenderContext, config, layout
    from ezdxf.addons.drawing.pymupdf import PyMuPdfBackend

    psp = doc.paperspace(layout_name)
    ctx = RenderContext(doc)
    ctx.set_current_layout(psp)
    cfg = config.Configuration(
        background_policy=config.BackgroundPolicy.WHITE,
        color_policy=config.ColorPolicy.COLOR,
        lineweight_policy=config.LineweightPolicy.ABSOLUTE,
        lineweight_scaling=1.0,
        min_lineweight=0.09,
        hatching_timeout=60,
    )
    backend = PyMuPdfBackend()
    Frontend(ctx, backend, config=cfg).draw_layout(psp, finalize=True)
    page = layout.Page(A1_W, A1_H, layout.Units.mm, margins=layout.Margins.all(0))
    settings = layout.Settings(fit_page=True)
    Path(pdf_path).write_bytes(backend.get_pdf_bytes(page, settings=settings))
    if png_path:
        Path(png_path).write_bytes(
            backend.get_pixmap_bytes(page, fmt="png", settings=settings, dpi=dpi))


def dms(az):
    d = int(az)
    m_f = (az - d) * 60
    m = int(m_f)
    s = round((m_f - m) * 60)
    if s == 60:
        s = 0
        m += 1
    if m == 60:
        m = 0
        d += 1
    return d, m, s


def azimuth(p, q):
    return math.degrees(math.atan2(q[0] - p[0], q[1] - p[1])) % 360.0


NOTAS_GENERALES = [
    "TODAS LAS MEDIDAS ESTÁN DADAS EN METROS, SALVO INDICACIÓN CONTRARIA.",
    "LA TAPIA COLINDANTE DE MAMPOSTERÍA DEBERÁ PROLONGARSE HASTA EL NIVEL DE LA VIGA "
    "CORONA DEL ÚLTIMO NIVEL, GARANTIZANDO EL APANTALLAMIENTO VISUAL PERMANENTE HACIA LA "
    "PROPIEDAD COLINDANTE.",
    "LOS DATOS DEL LOTE (VÉRTICES, DERROTERO Y ÁREA) SE TOMARON DEL PLANO CATASTRADO "
    "4-57389-2023, SISTEMA CRTM05. NO SUSTITUYEN UN LEVANTAMIENTO TOPOGRÁFICO.",
    "RETIROS DE DISEÑO: FRONTAL 2.00 m MEDIDO DESDE EL VÉRTICE 3; POSTERIOR MÍNIMO "
    "3.00 m; LATERALES 0.00 m. CONFIRMADOS CON EL ALINEAMIENTO Y EL USO DE SUELO MUNICIPAL.",
    "LAS FACHADAS LATERALES SE UBICAN SOBRE COLINDANCIA Y SERÁN CIEGAS "
    "(SIN VENTANAS NI VANOS).",
    "LOS BAÑOS CONTARÁN CON EXTRACTOR MECÁNICO DE AIRE.",
    "LAS CANOAS TENDRÁN MALLA PROTECTORA PARA EVITAR EL ACCESO DE BASURA.",
    "EL AGUA POTABLE PROVIENE DEL SISTEMA PÚBLICO (ESPH), DIRECTAMENTE DE LA "
    "CONEXIÓN DE LA CALLE (VER S01).",
    "LAS AGUAS PLUVIALES SE DIRIGEN HACIA LA CUNETA PÚBLICA (VER S03).",
    "LAS AGUAS RESIDUALES SE TRATARÁN MEDIANTE TANQUE SÉPTICO Y DRENAJE EN EL "
    "PATIO POSTERIOR (VER S02).",
    "LA COBERTURA SE CALCULA SOBRE EL ÁREA SEGÚN CATASTRO (256 m²). LOS PATIOS P1 "
    "Y P2 SON ABIERTOS DESDE EL NIVEL 1 HASTA EL CIELO Y NO SE CONTABILIZAN EN LA HUELLA.",
    "PATIOS DE LUZ P1 Y P2 DE 2.50 m DE LADO MÍNIMO, DIMENSIÓN ACEPTADA POR LA "
    "MUNICIPALIDAD (ALTURA MEDIDA DESDE EL NIVEL 1).",
]
NOTA_PR = "[PR] = NOTA TOMADA DEL PROYECTO DE REFERENCIA, PENDIENTE DE REVISIÓN."


def notas(extra=()):
    lst = NOTAS_GENERALES + list(extra)
    out = [f"{i}.- {t}" for i, t in enumerate(lst, 1)]
    return out


def derrotero_rows(V):
    rows = [["LÍNEA", "ACIMUT", None, "DISTANCIA", None],
            ["", "°", "'", "m", "cm"]]
    for a, b in ((1, 2), (2, 3), (3, 4), (4, 5), (5, 1)):
        az = azimuth(V[a], V[b])
        dd, mm, ss = dms(az + 30 / 3600)  # redondeo al minuto
        dist = math.dist(V[a], V[b])
        m_ = int(dist)
        cm = int(round((dist - m_) * 100))
        if cm == 100:
            m_, cm = m_ + 1, 0
        rows.append([f"{a} - {b}", f"{dd}", f"{mm:02d}", f"{m_}", f"{cm:02d}"])
    rows += [["AMARRE", "ACIMUT", None, "DISTANCIA", None],
             ["", "°", "'", "m", "cm"],
             ["3 - P.I.", "101", "22", "75", "71"]]
    return rows


def m2(v):
    return f"{v:,.2f} m²".replace(",", " ").replace(".", ",")


def notes_block(space, x, y_top, lines, h=2.1, width=250.0, gap=0.55):
    lines = [l for l in lines if l != NOTA_PR]
    """Cada nota como MTEXT independiente (evita uniones de párrafos en el PDF).

    Estima la altura con un ancho medio de carácter de 0.80*h. Devuelve y inferior.
    """
    import math as _m
    y = y_top
    cpl = max(10, int(width / (0.80 * h)))
    for s in lines:
        n = max(1, _m.ceil(len(s) / cpl))
        mtext(space, s, (x, y), h, width, attach=1, spacing=1.0)
        y -= n * h * 1.45 + gap * h
    return y
