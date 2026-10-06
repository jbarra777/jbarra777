"""Lámina E04 - DIAGRAMA UNIFILAR, CUADROS DE TABLEROS, NOTAS ELÉCTRICAS Y SIMBOLOGÍA.

Valores de la referencia (RIVERGRAND EL08-EL10) por indicación del usuario [PR]: cargas por
tipo de circuito, disyuntores, conductores THHN, distancias, tuberías, alimentadores (TP->TN2
como PB->TN1; TP->TN3 como PB->TN2), acometida (200 A, 3/0), factores de demanda y de potencia.
Lista de circuitos de esta vivienda según E01-E03 aprobadas. Caída de tensión con el mismo
criterio de la referencia: %CT = 2 L I R / V (R por metro deducida de sus cuadros).
Sin citas normativas ni marcas (criterio del usuario en A11 y C06).
"""
import cadlib as cl
import elec as EL
import hoja as H

REV = "rev0"
OUT = cl.ROOT / "planos" / "E04_tableros"
NAME = f"SR-E04_TABLEROS_{REV}"
LAYOUT = "E04-TABLEROS"

R = {"12": 0.00624, "10": 0.00381, "8": 0.00240, "4": 0.00094, "2": 0.000596, "3/0": 0.00025}
FD = {"TP": 0.70, "TN2": 0.80, "TN3": 0.80}                     # factor de demanda [PR]
FP = 0.95


def ct(va, v, L, cond):
    """Caída de tensión en % (criterio de la referencia)."""
    if not va or L == 0:
        return 0.0
    return 2 * L * (va / v) * R[cond] / v * 100


# circuito: (n, descripción, polos, amps, fase, neutro, tierra, dist, V, VA total, prot, Ø)
LUZ = lambda n, d: (n, d, 1, 20, "12", "12", "12", 15, 120, 500, "AFCI/GFCI", 13)
TOM = lambda n, d, va=500: (n, d, 1, 20, "12", "12", "12", 15, 120, va, "AFCI/GFCI", 13)
CAL = lambda n, d: (n, d, 2, 40, "10", "-", "8", 15, 240, 6000, "CH", 19)
TN2 = [LUZ("1", "ILUMINACIÓN NIVEL 2"),
       TOM("3", "TOMAS GENERALES NIVEL 2"),
       TOM("5", "TOMAS DE COCINA 1 (GFCI)", 1500),
       TOM("7", "TOMAS DE COCINA 2", 1500),
       TOM("9", "TOMAS DE BAÑO (GFCI)"),
       ("11/13", "COCINA ELÉCTRICA", 2, 40, "8", "8", "10", 15, 240, 8000, "CH", 19),
       CAL("15/17", "CALENTADOR DE PASO BAÑO SUITE 1"),
       ("19/21", "SPD", 2, 50, "8", "8", "8", 0.5, 240, 0, "CH", 19)]
TN3 = [LUZ("1", "ILUMINACIÓN NIVEL 3"),
       TOM("3", "TOMAS GENERALES SUITE 1 Y PASILLO"),
       TOM("5", "TOMAS GENERALES SUITES 2 Y 3"),
       TOM("7", "TOMAS DE BAÑOS (GFCI)"),
       CAL("9/11", "CALENTADOR DE PASO BAÑO SUITE 1"),
       CAL("13/15", "CALENTADOR DE PASO BAÑO SUITE 2"),
       CAL("17/19", "CALENTADOR DE PASO BAÑO SUITE 3"),
       ("21/23", "SPD", 2, 50, "8", "8", "8", 0.5, 240, 0, "CH", 19)]


def totals(circs):
    a = b = 0.0
    toggle = True
    for c in circs:
        va, v = c[9], c[8]
        if v == 240:
            a += va / 2
            b += va / 2
        else:
            if toggle:
                a += va
            else:
                b += va
            toggle = not toggle
    return a, b


def tablero_demanda(circs, key):
    a, b = totals(circs)
    return (a + b), (a + b) * FD[key]


T2_tot, T2_dem = tablero_demanda(TN2, "TN2")
T3_tot, T3_dem = tablero_demanda(TN3, "TN3")
TP = [LUZ("1", "ILUMINACIÓN NIVEL 1"),
      TOM("3", "TOMACORRIENTES NIVEL 1 (GFCI)", 1000),
      ("5/7", "SECADORA", 2, 40, "10", "-", "8", 15, 240, 6000, "CH", 19),
      ("9/11", "ALIMENTADOR SUBTABLERO TN2", 2, 100, "2", "2", "6", 15, 240, round(T2_dem), "CH", 32),
      ("13/15", "ALIMENTADOR SUBTABLERO TN3", 2, 100, "4", "4", "8", 20, 240, round(T3_dem), "CH", 32),
      ("17/19", "SPD", 2, 50, "8", "8", "8", 0.5, 240, 0, "CH", 19)]
TP_tot, TP_dem = tablero_demanda(TP, "TP")
ACOM = dict(f="2 #3/0", n="1 #3/0", t="1 #6", L=25, cond="3/0")

doc = cl.new_doc()
EL.layers(doc)
psp = doc.layouts.new(LAYOUT)
psp.page_setup(size=(cl.A1_W, cl.A1_H), margins=(0, 0, 0, 0), units="mm")
doc.layouts.set_active_layout(LAYOUT)
cl.frame(psp)


def L(a, b, layer="E-CIRC"):
    psp.add_line(a, b, dxfattribs={"layer": layer})


def box(x0, y0, x1, y1, layer="E-TABLERO"):
    psp.add_lwpolyline([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], close=True,
                       dxfattribs={"layer": layer})


def T(s, p, h=2.0, al="MIDDLE_LEFT", layer="A-TEXTO"):
    cl.text(psp, s, p, h, layer, al)


def M(s, p, w=70.0, h=1.9, attach=1):
    cl.mtext(psp, s, p, h, w, layer="A-TEXTO", attach=attach)


# ================================================================ diagrama unifilar eléctrico
cl.view_title(psp, 35.0, 448.0, "DIAGRAMA UNIFILAR ELÉCTRICO", "MONOFÁSICO 120/240 V", "Esc. S/E", 150)
X0, Y0 = 95.0, 565.0
L((X0, Y0), (X0, 540.0))
L((X0 - 4, Y0 + 3), (X0, Y0))
L((X0 + 4, Y0 + 3), (X0, Y0))
M("VIENE DE LA RED DE SUMINISTRO ELÉCTRICO (EMPRESA DISTRIBUIDORA)", (X0 - 58, Y0 + 4), 52)
M("CU 3 #3/0 AWG THHN\\PC: 2\" IMC [PR]", (X0 + 4, 552.0), 45)
box(X0 - 10, 500.0, X0 + 10, 540.0)
EL.sym(psp, "M", X0, 528.0, 3.0)
psp.add_arc((X0, 510.0), 3.0, 270, 90, dxfattribs={"layer": "E-CIRC"})
L((X0, 516.0), (X0, 513.0))
L((X0, 507.0), (X0, 503.0))
M("BASE PARA MEDIDOR Y MEDIDOR (SEGÚN EMPRESA DISTRIBUIDORA, PD)", (X0 - 62, 534.0), 50)
M("INTERRUPTOR PRINCIPAL 200 A, CI 18 kA [PR]", (X0 + 13, 512.0), 48)
# tierra
L((X0 - 6, 500.0), (X0 - 6, 470.0))
for i, w in enumerate((8, 5.5, 3)):
    L((X0 - 6 - w / 2, 470.0 - i * 1.5), (X0 - 6 + w / 2, 470.0 - i * 1.5))
M("PUESTA A TIERRA: CU 1 #6 AWG THHN, C: 1/2\" PVC. DOS ELECTRODOS DE PUESTA A TIERRA SEPARADOS "
  "3 m ENTRE SÍ, INTERCONECTADOS CON CABLE #6 AWG DESNUDO, ENTERRADOS A UNA PROFUNDIDAD NO "
  "MENOR A 3,05 m EN POSICIÓN VERTICAL. [PR]", (35.0, 492.0), 52, 1.7)
# acometida subterránea al TP
L((X0 + 2, 500.0), (X0 + 2, 478.0))
box(X0 - 2, 474.0, X0 + 6, 478.0, "E-CIRC")
L((X0 + 6, 476.0), (205.0, 476.0))
L((205.0, 476.0), (205.0, 500.0))
M("TRANSICIÓN AERO-SUBTERRÁNEA [PR]", (X0 + 8, 472.0), 40, 1.7)
M("CU 2 #3/0 (F) + 1 #3/0 (N) + 1 #6 (T) AWG THHN\\PC: 2\" PVC, TRAMO SUBTERRÁNEO A 45 cm "
  "MÍNIMO SOBRE CAMA DE LASTRE DE 5 cm [PR]", (X0 + 40, 486.0), 62, 1.7)
EL.sym(psp, "TAB", 205.0, 505.0, 2.4)
T("TP (NIVEL 1)", (215.0, 505.0), 2.2)
for xs, lab, txt in ((255.0, "TN2 (NIVEL 2)", "CU 2 #2 (F) + 1 #2 (N) + 1 #6 (T)\\PC: 1 1/4\" PVC [PR]"),
                     (300.0, "TN3 (NIVEL 3)", "CU 2 #4 (F) + 1 #4 (N) + 1 #8 (T)\\PC: 1 1/4\" PVC [PR]")):
    L((205.0, 508.0), (205.0, 515.0 if xs == 255.0 else 520.0))
    L((205.0, 515.0 if xs == 255.0 else 520.0), (xs, 515.0 if xs == 255.0 else 520.0))
    L((xs, 515.0 if xs == 255.0 else 520.0), (xs, 535.0 if xs == 255.0 else 550.0))
    EL.sym(psp, "TAB", xs, 538.0 if xs == 255.0 else 553.0, 2.4)
    T(lab, (xs - 6.0, 543.0 if xs == 255.0 else 558.0), 2.0)
    M(txt, (xs + 2.0, 528.0 if xs == 255.0 else 545.0), 42, 1.6)

# ================================================================ voz y datos
cl.text(psp, "DIAGRAMA DE VOZ Y DATOS", (360.0, 575.0), 3.5, "A-TITULOS", "TOP_LEFT")
L((370.0, 560.0), (370.0, 520.0))
L((366.0, 563.0), (370.0, 560.0))
L((374.0, 563.0), (370.0, 560.0))
M("VIENE DEL SERVICIO TELEFÓNICO Y DE TV", (376.0, 563.0), 50, 1.7)
box(367.0, 516.0, 373.0, 520.0, "E-CIRC")
L((373.0, 518.0), (430.0, 518.0))
L((430.0, 518.0), (430.0, 535.0))
EL.sym(psp, "TVD", 430.0, 538.0, 2.4)
T("PVD (NIVEL 1)", (424.0, 543.0), 2.0)
M("PREVISTA LÍNEA TELEFÓNICA, CATV / FIBRA ÓPTICA: 2 C 1\" PVC [PR]", (376.0, 512.0), 62, 1.7)
M("DEL PVD A LAS SALIDAS DE TV Y DATOS DE CADA NIVEL (E01-E03) EN TUBERÍA INDEPENDIENTE DE LA "
  "ELÉCTRICA.", (360.0, 500.0), 95, 1.7)

# ================================================================ tabla resumen
XR, YR = 500.0, 575.0
cl.text(psp, "TABLA RESUMEN DEL PROYECTO [PR]", (XR, YR), 3.5, "A-TITULOS", "TOP_LEFT")
v_tp = ct(TP_dem, 240, ACOM["L"], "3/0")
c2, c3 = TP[3], TP[4]
v_t2 = ct(c2[9], 240, c2[7], "2")
v_t3 = ct(c3[9], 240, c3[7], "4")
fmt = lambda x: f"{x:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")
rows = [["", "TABLERO TP", "TABLERO TN2", "TABLERO TN3"],
        ["kVA TOTALES", fmt(TP_tot / 1000), fmt(T2_tot / 1000), fmt(T3_tot / 1000)],
        ["kVA DEMANDADOS", fmt(TP_dem / 1000), fmt(T2_dem / 1000), fmt(T3_dem / 1000)],
        ["FACTOR DE DEMANDA", "0,70", "0,80", "0,80"],
        ["FACTOR DE POTENCIA", "0,95", "0,95", "0,95"],
        ["FASES", "2 #3/0 AWG", "2 #2 AWG", "2 #4 AWG"],
        ["NEUTRO", "1 #3/0 AWG", "1 #2 AWG", "1 #4 AWG"],
        ["TIERRA", "1 #6 AWG", "1 #6 AWG", "1 #8 AWG"],
        ["LONGITUD (m)", "25", "15", "20"],
        ["TENSIÓN NOMINAL (V)", "120/240", "120/240", "120/240"],
        ["% CAÍDA DE TENSIÓN", f"{v_tp:.2f} %".replace(".", ","), f"{v_t2:.2f} %".replace(".", ","),
         f"{v_t3:.2f} %".replace(".", ",")]]
cl.table(psp, XR, YR - 6.0, [52, 42, 42, 42], rows, row_h=5.2, h=1.9,
         aligns=["MIDDLE_LEFT", "MIDDLE_CENTER", "MIDDLE_CENTER", "MIDDLE_CENTER"])

# ================================================================ cuadros de tableros
COLW = [14, 70, 11, 11, 12, 12, 12, 11, 12, 16, 16, 15, 11, 20]
HEAD = ["N.", "DESCRIPCIÓN", "POL.", "AMP.", "FASE", "NEUT.", "TIERRA", "DIST.", "V",
        "VA FASE A", "VA FASE B", "% CT", "Ø mm", "PROTECCIÓN"]


def cuadro(x, y, key, titulo, circs, info):
    cl.text(psp, titulo, (x, y), 3.2, "A-TITULOS", "TOP_LEFT")
    y -= 5.0
    M(info, (x, y), sum(COLW), 1.7)
    y -= 8.5
    rows = [HEAD]
    toggle = True
    for c in circs:
        n, d, pol, amp, f, ne, tt, dist, v, va, prot, dia = c
        if v == 240:
            a = b = va / 2
        else:
            a, b = (va, 0) if toggle else (0, va)
            toggle = not toggle
        rows.append([n, d, str(pol), str(amp), f, ne, tt, f"{dist:g}".replace(".", ","), str(v),
                     f"{a:,.0f}".replace(",", ".") if a else "-",
                     f"{b:,.0f}".replace(",", ".") if b else "-",
                     f"{ct(va, v, dist, f):.2f}".replace(".", ",") if va else "-", str(dia), prot])
    a, b = totals(circs)
    rows.append(["", "TOTAL POR FASE (VA)", None, None, None, None, None, None, None,
                 f"{a:,.0f}".replace(",", "."), f"{b:,.0f}".replace(",", "."), "", "", ""])
    al = ["MIDDLE_CENTER", "MIDDLE_LEFT"] + ["MIDDLE_CENTER"] * 12
    return cl.table(psp, x, y, COLW, rows, row_h=4.6, h=1.6, aligns=al)


XT = 35.0
y = 420.0
y = cuadro(XT, y, "TP", "TABLERO PRINCIPAL TP (NIVEL 1, VESTÍBULO) [PR]", TP,
           "TABLERO MONOFÁSICO 120/240 V, BARRAS DE TIERRA, NEUTRO SÓLIDO AL 100 %, BARRAS PRINCIPALES "
           "DE COBRE. EMPOTRADO. BARRAS 225 A, 24 POLOS, INTERRUPTOR PRINCIPAL 200 A, CI 200 A. "
           f"CARGA TOTAL {fmt(TP_tot / 1000)} kVA; DEMANDADA {fmt(TP_dem / 1000)} kVA.")
y = cuadro(XT, y - 6.0, "TN2", "SUBTABLERO TN2 (NIVEL 2) [PR]", TN2,
           "TABLERO MONOFÁSICO 120/240 V, BARRAS DE TIERRA, NEUTRO SÓLIDO AL 100 %. EMPOTRADO. BARRAS "
           "125 A, 18 POLOS, PRINCIPAL 100 A (SUBALIMENTADO). "
           f"CARGA TOTAL {fmt(T2_tot / 1000)} kVA; DEMANDADA {fmt(T2_dem / 1000)} kVA.")
y = cuadro(XT, y - 6.0, "TN3", "SUBTABLERO TN3 (NIVEL 3) [PR]", TN3,
           "TABLERO MONOFÁSICO 120/240 V, BARRAS DE TIERRA, NEUTRO SÓLIDO AL 100 %. EMPOTRADO. BARRAS "
           "125 A, 18 POLOS, PRINCIPAL 100 A (SUBALIMENTADO). "
           f"CARGA TOTAL {fmt(T3_tot / 1000)} kVA; DEMANDADA {fmt(T3_dem / 1000)} kVA.")
M("CONDUCTORES THHN DE COBRE (AWG). CAÍDA DE TENSIÓN %CT = 2 L I R / V CON LA RESISTENCIA POR "
  "CONDUCTOR DEL CRITERIO DE LA REFERENCIA. CARGAS POR TIPO DE CIRCUITO, DISYUNTORES, DISTANCIAS Y "
  "TUBERÍAS DE LA REFERENCIA [PR]: A VERIFICAR POR EL PROFESIONAL ELÉCTRICO.", (XT, y - 3.0), 245, 1.7)

# ================================================================ notas y simbología
XN, W2 = 300.0, 200.0
y = 420.0
cl.text(psp, "NOTAS ELÉCTRICAS [PR]", (XN, y), 3.5, "A-TITULOS", "TOP_LEFT")
y -= 7.0


def bloque(titulo, lineas, x, y, w, h=1.8):
    """Notas con estimación de altura conservadora (mayúsculas: ~0,95 h por carácter)."""
    import math
    cl.text(psp, titulo, (x, y), 2.6, "A-TITULOS", "TOP_LEFT")
    y -= 4.5
    cpl = max(10, int(w / (0.95 * h)))
    for t in lineas:
        n = max(1, math.ceil(len(t) / cpl))
        cl.mtext(psp, t, (x, y), h, w, attach=1, spacing=1.0)
        y -= n * h * 1.55 + 0.6 * h
    return y - 3.0


y = bloque("NOTAS GENERALES", [
    "LAS INSTALACIONES ELÉCTRICAS SE REALIZARÁN DE ACUERDO CON LA NORMATIVA ELÉCTRICA VIGENTE Y LAS "
    "REGULACIONES DE LA EMPRESA DISTRIBUIDORA.",
    "CUALQUIER CAMBIO O ADICIONAL PODRÁ REALIZARSE BAJO LA AUTORIZACIÓN DEL INGENIERO DISEÑADOR, "
    "QUIEN EVALUARÁ LOS CAMBIOS.",
    "NO SE PERMITIRÁN CAMBIOS SIN LA PRESENTACIÓN Y APROBACIÓN DE LAS FICHAS TÉCNICAS "
    "CORRESPONDIENTES. CUALQUIER INSTALACIÓN ESTÁ SUJETA A RECHAZO POR PARTE DEL INSPECTOR SI NO SE "
    "PRESENTAN LAS FICHAS DE LOS MATERIALES Y EQUIPOS COMPRADOS."], XN, y, W2)
y = bloque("CANALIZACIONES", [
    "LAS CANALIZACIONES DE LAS REDES ELÉCTRICAS Y TELEFÓNICAS DEBERÁN COLOCARSE Y UTILIZARSE EN "
    "FORMA INDEPENDIENTE, CON EL 40 % DEL ESPACIO (ÁREA TRANSVERSAL) LIBRE EN TODOS SUS PUNTOS.",
    "TODAS LAS CANALIZACIONES SE HARÁN CON TUBERÍA CONDUIT PVC CERTIFICADA, DE LOS DIÁMETROS "
    "ESPECIFICADOS. LAS CONEXIONES SERÁN CONTINUAS ENTRE CAJA Y CAJA. LA TUBERÍA QUE NO VIAJE EN "
    "ESTRUCTURAS CHORREADAS SE SUJETARÁ CON GAZAS CADA 1,5 m COMO MÍNIMO.",
    "LAS TUBERÍAS EXPUESTAS QUE VIAJEN A MENOS DE 2,5 m DE ALTURA DEBEN SER METÁLICAS (EMT, RÍGIDO, "
    "GALVANIZADO). LAS TUBERÍAS ENTERRADAS EN EXTERIORES SERÁN DE PVC SCH-40.",
    "LAS CANALIZACIONES ELÉCTRICAS DE POTENCIA (BAJA TENSIÓN) DEBERÁN IR A UNA PROFUNDIDAD MÍNIMA DE "
    "50 cm, CUBIERTAS CON UNA CAPA DE 10 cm (MÍNIMO) DE ARENA LIMPIA; LAS TELEFÓNICAS A 25 cm "
    "MÍNIMO, CUBIERTAS CON 5 cm DE ARENA LIMPIA.",
    "LAS UNIONES ENTRE TUBERÍAS, CAJAS Y LÁMPARAS SE HARÁN MEDIANTE ACCESORIOS EMT DE TAMAÑO "
    "ADECUADO. LAS TUBERÍAS EN PROCESO DE INSTALACIÓN SE PROTEGERÁN CON TAPONES DE CAUCHO O MADERA."],
    XN, y, W2)
y2 = 420.0 - 7.0
y2 = bloque("CONDUCTORES ELÉCTRICOS", [
    "EL CENTRO DE CARGA DEBE SEPARARSE 15 cm (MÍNIMO) DE PAREDES, CAJAS DE DISTRIBUCIÓN TELEFÓNICA, "
    "TV, ETC. LA SEPARACIÓN ENTRE DUCTOS TELEFÓNICOS Y ELÉCTRICOS DEBE SER DE 15 cm (MÍNIMO), Y ENTRE "
    "CAJAS DE SALIDAS ELÉCTRICAS Y TELEFÓNICAS DE 5 cm (MÍNIMO).",
    "EN TODOS LOS TABLEROS SE DEBERÁ DEJAR AL MENOS UNA PREVISTA CONDUIT DE 19 mm VACÍA POR CADA 10 "
    "POLOS DE CAPACIDAD DEL TABLERO.",
    "LOS CALIBRES 8, 10 Y 12 AWG TENDRÁN AISLAMIENTO DEL COLOR INDICADO; LOS CALIBRES MAYORES, "
    "AISLAMIENTO NEGRO CON CINTA DEL COLOR CORRESPONDIENTE EN TODOS LOS TERMINALES: FASE A ROJO, "
    "FASE B NEGRO, NEUTRO BLANCO, TIERRA VERDE, RETORNO AZUL.",
    "LOS CONDUCTORES VIAJARÁN CONTINUOS Y SIN EMPALMES ENTRE CAJA Y CAJA. TODAS LAS LUMINARIAS, "
    "TOMACORRIENTES Y APAGADORES LLEVARÁN HILO DE TIERRA (CALIBRE INDICADO EN EL TABLERO).",
    "EL VALOR DE RESISTENCIA DE LA MALLA DE TIERRA NO DEBERÁ SER MAYOR A 25 OHM."],
    XN + W2 + 8.0, y2, W2)
y2 = bloque("VOZ Y DATOS", [
    "TODAS LAS SALIDAS DE TELECOMUNICACIONES SE INSTALARÁN EN CAJAS CUADRADAS (2 GANGS) CON ARO DE "
    "REPELLO DE UN GANG, CON PROFUNDIDAD NO MENOR A 6,5 cm.",
    "LOS CONDUCTORES DE DATOS SERÁN CAT 6A (MÍNIMO) Y LOS CABLES DE VOZ Y DATOS QUE VIAJEN A MENOS "
    "DE 20 cm DE UNA LÍNEA DE POTENCIA SERÁN BLINDADOS. TODAS LAS SALIDAS DE DATOS DEBERÁN IR "
    "DEBIDAMENTE ETIQUETADAS Y PROBADAS."], XN + W2 + 8.0, y2, W2)
yS = min(y, y2) - 2.0
EL.simbologia(psp, XN, yS, w_txt=150.0, row_h=5.6)
cl.notes_block(psp, XN + 180.0, yS, [
    "LÁMINAS RELACIONADAS: E01 (NIVEL 1), E02 (NIVEL 2) Y E03 (NIVEL 3).",
    "VALORES DE CARGA, PROTECCIONES Y CONDUCTORES TOMADOS DEL PROYECTO DE REFERENCIA POR "
    "INDICACIÓN DEL INGENIERO RESPONSABLE; DEBEN SER VERIFICADOS POR EL PROFESIONAL ELÉCTRICO.",
    cl.NOTA_PR], 1.9, 225.0)

H.titleblock(doc, psp, "E04", "ELECTRICIDAD",
             ["DIAGRAMA UNIFILAR.", "VOZ Y DATOS.", "CUADROS DE TABLEROS.", "NOTAS ELÉCTRICAS.",
              "SIMBOLOGÍA.", ""],
             [("0", "06-10-2026", "VERSIÓN DE TRABAJO PARA REVISIÓN")], escalas="S/E")

OUT.mkdir(parents=True, exist_ok=True)
doc.saveas(OUT / f"{NAME}.dxf")
cl.render_pdf(doc, LAYOUT, OUT / f"{NAME}.pdf")
print("TP", TP_tot, TP_dem, "TN2", T2_tot, T2_dem, "TN3", T3_tot, T3_dem, "CT", v_tp, v_t2, v_t3)
print("DXF:", OUT / f"{NAME}.dxf")
