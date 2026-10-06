"""Ayudas para plantas arquitectónicas (A2-A4 y especialidades).

Marco de PLANTA (Model Space, metros): girado 90° respecto al de la lámina A1
para dibujar la vivienda horizontal a 1:50 (calle a la izquierda):
    X = y_local  (fondo, desde la línea de frente hacia el sur)
    Y = x_local  (ancho, desde el lindero oeste hacia el este)
x_local / y_local son las del marco de diseño (datos/proyecto.json).
"""
import json
import math

from ezdxf.math import Vec2

import cadlib as cl

LT_DASH = 0.10   # escala de tipo de línea por entidad para 1:50
LT_CENTER = 0.05


def P(x, y):
    """Marco de diseño (x este, y fondo) -> marco de planta."""
    return Vec2(y, x)


def lot_model():
    lote = json.loads((cl.ROOT / "datos" / "lote_catastro.json").read_text(encoding="utf-8"))
    V = {int(k): Vec2(v) for k, v in lote["vertices_crtm05"].items()}
    O = V[1]
    v_s = (V[5] - O).normalize()
    u_e = Vec2(-v_s.y, v_s.x)
    if u_e.x < 0:
        u_e = -u_e

    def to_local(p):
        d = Vec2(p) - O
        return d.dot(u_e), d.dot(v_s)

    loc = {k: to_local(p) for k, p in V.items()}
    return lote, V, loc, (O, u_e, v_s)


def add_crtm_ucs(doc, frame):
    """UCS 'CRTM05' para el marco de planta."""
    O, u_e, v_s = frame

    def to_plan(c):
        d = Vec2(c) - O
        return P(d.dot(u_e), d.dot(v_s))

    org = to_plan((0.0, 0.0))
    ux = to_plan(O + Vec2(1, 0)) - to_plan(O)
    uy = to_plan(O + Vec2(0, 1)) - to_plan(O)
    doc.ucs.new("CRTM05", dxfattribs={"origin": (org.x, org.y, 0),
                                      "xaxis": (ux.x, ux.y, 0),
                                      "yaxis": (uy.x, uy.y, 0)})
    # ángulo del norte en el marco de planta (grados, antihorario desde +X)
    return math.degrees(math.atan2(uy.y, uy.x))


def wall(msp, x0, x1, y0, y1, hatch=True):
    pts = [P(x0, y0), P(x1, y0), P(x1, y1), P(x0, y1)]
    msp.add_lwpolyline(pts, close=True, dxfattribs={"layer": "A-MURO"})
    if hatch:
        h = msp.add_hatch(dxfattribs={"layer": "A-MURO-TRAMA"})
        h.paths.add_polyline_path(pts)
        h.set_pattern_fill("ANSI31", scale=0.03)


def line(msp, a, b, layer, ltscale=None):
    e = msp.add_line(P(*a), P(*b), dxfattribs={"layer": layer})
    if ltscale:
        e.dxf.ltscale = ltscale
    return e


def poly(msp, pts, layer, close=True, ltscale=None):
    e = msp.add_lwpolyline([P(*p) for p in pts], close=close, dxfattribs={"layer": layer})
    if ltscale:
        e.dxf.ltscale = ltscale
    return e


def door(msp, hinge, width, closed_dir, open_dir, label=None):
    """Puerta abatible en planta.

    hinge: (x, y) bisagra; closed_dir: vector unitario de la hoja cerrada (a lo
    largo del vano); open_dir: vector unitario hacia donde abre (perpendicular).
    """
    h = Vec2(hinge)
    c = Vec2(closed_dir)
    o = Vec2(open_dir)
    tip = h + o * width
    line(msp, h, tip, "A-PUERTA")
    # arco desde la posición cerrada hasta la abierta
    a0 = math.degrees(math.atan2(*reversed(tuple(P(*c)))))
    a1 = math.degrees(math.atan2(*reversed(tuple(P(*o)))))
    # elegir el arco corto de 90°
    d = (a1 - a0) % 360
    start, end = (a0, a1) if d <= 180 else (a1, a0)
    msp.add_arc(P(*h), width, start, end, dxfattribs={"layer": "A-PUERTA"})


def window_y(msp, x0, x1, y_face0, y_face1):
    """Ventana en un muro paralelo al eje x (muro entre y_face0 y y_face1)."""
    ym = (y_face0 + y_face1) / 2
    for yy in (y_face0, y_face1):
        line(msp, (x0, yy), (x1, yy), "A-VENTANA")
    line(msp, (x0, ym), (x1, ym), "A-VENTANA")
    line(msp, (x0, y_face0), (x0, y_face1), "A-VENTANA")
    line(msp, (x1, y_face0), (x1, y_face1), "A-VENTANA")


def window_x(msp, y0, y1, x_face0, x_face1):
    xm = (x_face0 + x_face1) / 2
    for xx in (x_face0, x_face1):
        line(msp, (xx, y0), (xx, y1), "A-VENTANA")
    line(msp, (xm, y0), (xm, y1), "A-VENTANA")
    line(msp, (x_face0, y0), (x_face1, y0), "A-VENTANA")
    line(msp, (x_face0, y1), (x_face1, y1), "A-VENTANA")


def car(msp, xc, yc, front_dir=-1):
    """Vehículo 1.80 x 4.50 m con el frente hacia y decreciente (front_dir=-1)."""
    w, L = 1.80, 4.50
    x0, x1 = xc - w / 2, xc + w / 2
    y0, y1 = yc - L / 2, yc + L / 2
    r = 0.25
    pts = [(x0 + r, y0), (x1 - r, y0), (x1, y0 + r), (x1, y1 - r), (x1 - r, y1),
           (x0 + r, y1), (x0, y1 - r), (x0, y0 + r)]
    poly(msp, pts, "A-VEHICULO")
    # parabrisas y vidrio trasero
    yf = yc + front_dir * 0.95
    yr = yc - front_dir * 1.35
    poly(msp, [(x0 + 0.15, yf), (x1 - 0.15, yf), (x1 - 0.25, yf - front_dir * 0.45),
               (x0 + 0.25, yf - front_dir * 0.45)], "A-VEHICULO")
    poly(msp, [(x0 + 0.20, yr), (x1 - 0.20, yr), (x1 - 0.25, yr + front_dir * 0.35),
               (x0 + 0.25, yr + front_dir * 0.35)], "A-VEHICULO")


def text(msp, s, x, y, h=0.12, layer="A-TXT-50", align="MIDDLE_CENTER", rot=0.0):
    return cl.text(msp, s, P(x, y), h, layer, align, rot)


def mtext(msp, s, x, y, h=0.12, width=3.0, layer="A-TXT-50", attach=5):
    return cl.mtext(msp, s, P(x, y), h, width, layer=layer, attach=attach)


def dim(msp, a, b, base, horizontal, style="COTA-50", layer="A-COTA-50"):
    """Cota lineal en el marco de diseño. horizontal=True mide a lo largo de x_local."""
    pa, pb, pbase = P(*a), P(*b), P(*base)
    # en planta x_local es el eje Y -> ángulo 90°
    ang = 90 if horizontal else 0
    d = msp.add_linear_dim(base=pbase, p1=pa, p2=pb, angle=ang, dimstyle=style,
                           dxfattribs={"layer": layer})
    d.render()
    return d


def axis(msp, label, along, value, start, end, bubble_at="start", r=0.28):
    """Eje constructivo. along='x' -> eje de letra (x constante)."""
    if along == "x":
        a, b = (value, start), (value, end)
    else:
        a, b = (start, value), (end, value)
    e = line(msp, a, b, "A-EJES", LT_CENTER)
    for pos in ([a] if bubble_at == "start" else [b] if bubble_at == "end" else [a, b]):
        pv = Vec2(pos)
        dirv = (Vec2(a) - Vec2(b)).normalize() if pos == a else (Vec2(b) - Vec2(a)).normalize()
        c = pv + dirv * r
        msp.add_circle(P(*c), r, dxfattribs={"layer": "A-EJES-TXT"})
        text(msp, label, c.x, c.y, 0.22, "A-EJES-TXT")
    return e


def level(msp, x, y, label):
    """Símbolo de nivel de piso terminado."""
    c = P(x, y)
    s = 0.12
    msp.add_lwpolyline([(c.x - s, c.y + s), (c.x + s, c.y + s), (c.x, c.y)], close=True,
                       dxfattribs={"layer": "A-NIVELES"})
    h = msp.add_hatch(color=7, dxfattribs={"layer": "A-NIVELES"})
    h.paths.add_polyline_path([(c.x - s, c.y + s), (c.x, c.y + s), (c.x, c.y)])
    msp.add_line((c.x - s, c.y + s), (c.x + 1.6, c.y + s), dxfattribs={"layer": "A-NIVELES"})
    cl.text(msp, label, (c.x + 0.2, c.y + s + 0.05), 0.12, "A-NIVELES", "BOTTOM_LEFT")


def section_mark(msp, label, sheet, a, b, look):
    """Línea de corte entre a y b (diseño); look = vector de visual."""
    pa, pb = P(*a), P(*b)
    for p0 in (pa, pb):
        msp.add_line(p0, p0 + (pb - pa).normalize() * (0.6 if p0 == pa else -0.6),
                     dxfattribs={"layer": "A-CORTES"})
    lk = P(*look) - P(0, 0)
    lk = lk.normalize()
    for p0 in (pa, pb):
        tip = p0 + lk * 0.45
        side = (pb - pa).normalize() * 0.22
        msp.add_solid([p0 - side, p0 + side, tip], dxfattribs={"layer": "A-CORTES"})
        cl.text(msp, f"{label}", p0 + lk * 0.75, 0.20, "A-CORTES", "MIDDLE_CENTER")
        cl.text(msp, sheet, p0 + lk * 0.75 - (pb - pa).normalize() * 0.0 + Vec2(0, -0.28),
                0.12, "A-CORTES", "MIDDLE_CENTER")
    e = msp.add_line(pa, pb, dxfattribs={"layer": "A-CORTES", "linetype": "PHANTOM"})
    e.dxf.ltscale = 0.05


# ---------------------------------------------------------------- mobiliario (marco de diseño)
def rect(msp, x0, y0, x1, y1, layer="A-MOBILIARIO"):
    return poly(msp, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], layer)


def bed(msp, x0, y0, x1, y1, head="x0"):
    """Cama en el rectángulo dado; head indica el lado de la cabecera."""
    rect(msp, x0, y0, x1, y1)
    if head in ("x0", "x1"):
        hx = x0 + 0.08 if head == "x0" else x1 - 0.08
        px = x0 + 0.55 if head == "x0" else x1 - 0.55
        rect(msp, min(hx, px), y0 + 0.08, max(hx, px), (y0 + y1) / 2 - 0.04)
        rect(msp, min(hx, px), (y0 + y1) / 2 + 0.04, max(hx, px), y1 - 0.08)
        fx = x0 + 0.75 if head == "x0" else x1 - 0.75
        line(msp, (fx, y0), (fx, y1), "A-MOBILIARIO")
    else:
        hy = y0 + 0.08 if head == "y0" else y1 - 0.08
        py = y0 + 0.55 if head == "y0" else y1 - 0.55
        rect(msp, x0 + 0.08, min(hy, py), (x0 + x1) / 2 - 0.04, max(hy, py))
        rect(msp, (x0 + x1) / 2 + 0.04, min(hy, py), x1 - 0.08, max(hy, py))
        fy = y0 + 0.75 if head == "y0" else y1 - 0.75
        line(msp, (x0, fy), (x1, fy), "A-MOBILIARIO")


def wc(msp, x, y, facing):
    """Inodoro con tanque contra el muro; (x, y) = centro del tanque; facing = (dx, dy)."""
    f = Vec2(facing)
    s = Vec2(-f.y, f.x)
    c = Vec2(x, y)
    tank = [c - s * 0.22, c + s * 0.22, c + s * 0.22 + f * 0.20, c - s * 0.22 + f * 0.20]
    poly(msp, tank, "A-MOBILIARIO")
    center = c + f * 0.45
    msp.add_ellipse(P(*center), major_axis=P(*(f * 0.25)) - P(0, 0), ratio=0.70,
                    dxfattribs={"layer": "A-MOBILIARIO"})


def lav(msp, x0, y0, x1, y1):
    rect(msp, x0, y0, x1, y1)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    msp.add_ellipse(P(cx, cy), major_axis=Vec2(0.0, min(x1 - x0, y1 - y0) * 0.35) if False
                    else P(min(x1 - x0, y1 - y0) * 0.30, 0) - P(0, 0), ratio=0.75,
                    dxfattribs={"layer": "A-MOBILIARIO"})


def shower(msp, x0, y0, x1, y1):
    rect(msp, x0, y0, x1, y1)
    line(msp, (x0, y0), (x1, y1), "A-MOBILIARIO")
    line(msp, (x1, y0), (x0, y1), "A-MOBILIARIO")
    msp.add_circle(P((x0 + x1) / 2, (y0 + y1) / 2), 0.04, dxfattribs={"layer": "A-MOBILIARIO"})


def counter(msp, x0, y0, x1, y1):
    rect(msp, x0, y0, x1, y1)


def stove(msp, x0, y0, x1, y1):
    rect(msp, x0, y0, x1, y1)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    for dx in (-0.14, 0.14):
        for dy in (-0.14, 0.14):
            msp.add_circle(P(cx + dx, cy + dy), 0.08, dxfattribs={"layer": "A-MOBILIARIO"})


def sink(msp, x0, y0, x1, y1):
    rect(msp, x0, y0, x1, y1)
    rect(msp, x0 + 0.06, y0 + 0.06, x1 - 0.06, y1 - 0.06)


def chair(msp, x, y, facing):
    f = Vec2(facing)
    s = Vec2(-f.y, f.x)
    c = Vec2(x, y)
    pts = [c - s * 0.21 - f * 0.21, c + s * 0.21 - f * 0.21, c + s * 0.21 + f * 0.21,
           c - s * 0.21 + f * 0.21]
    poly(msp, pts, "A-MOBILIARIO")
    back = [c - s * 0.21 - f * 0.21, c + s * 0.21 - f * 0.21, c + s * 0.21 - f * 0.15,
            c - s * 0.21 - f * 0.15]
    poly(msp, back, "A-MOBILIARIO")


def sofa(msp, x0, y0, x1, y1, back="x1"):
    rect(msp, x0, y0, x1, y1)
    d = 0.20
    if back == "x1":
        rect(msp, x1 - d, y0, x1, y1)
        rect(msp, x0, y0, x1 - d, y0 + d)
        rect(msp, x0, y1 - d, x1 - d, y1)
    elif back == "x0":
        rect(msp, x0, y0, x0 + d, y1)
        rect(msp, x0 + d, y0, x1, y0 + d)
        rect(msp, x0 + d, y1 - d, x1, y1)
    elif back == "y1":
        rect(msp, x0, y1 - d, x1, y1)
        rect(msp, x0, y0, x0 + d, y1 - d)
        rect(msp, x1 - d, y0, x1, y1 - d)
    else:
        rect(msp, x0, y0, x1, y0 + d)
        rect(msp, x0, y0 + d, x0 + d, y1)
        rect(msp, x1 - d, y0 + d, x1, y1)


def closet(msp, x0, y0, x1, y1, along="y"):
    """Mueble de closet (0.60) con barra de colgar."""
    rect(msp, x0, y0, x1, y1)
    if along == "y":
        xm = (x0 + x1) / 2
        line(msp, (xm, y0 + 0.05), (xm, y1 - 0.05), "A-MOBILIARIO")
    else:
        ym = (y0 + y1) / 2
        line(msp, (x0 + 0.05, ym), (x1 - 0.05, ym), "A-MOBILIARIO")


def round_table(msp, x, y, r, n_chairs):
    msp.add_circle(P(x, y), r, dxfattribs={"layer": "A-MOBILIARIO"})
    for i in range(n_chairs):
        a = 2 * math.pi * i / n_chairs + math.pi / 4
        d = Vec2(math.cos(a), math.sin(a))
        chair(msp, x + d.x * (r + 0.25), y + d.y * (r + 0.25), (-d.x, -d.y))


def room_label(msp, name, x, y, dims=None, area=None, h=0.16):
    s = name
    if dims:
        s += "\\P" + dims
    if area is not None:
        s += f"\\P{area:.2f} m²".replace(".", ",")
    return mtext(msp, s, x, y, h, 4.0, "A-ESPACIOS")
