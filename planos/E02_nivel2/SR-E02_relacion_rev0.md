# Lámina E02 · PLANTA ELÉCTRICA NIVEL 2 · rev0 (versión de trabajo)

**Estado:** versión de trabajo para revisión. No apta para construcción ni trámite.

## Archivos
| Archivo | Uso |
|---|---|
| `SR-E02_NIVEL2_rev0.pdf` | Plano para revisar (A1 al 100 %) |
| `SR-E02_NIVEL2_rev0.dxf` | Editable AutoCAD 2018, layout `E02-NIVEL2` |

Generador: `scripts/e02_nivel2.py` (simbología común `elec.py`).

## Criterio
- **Base:** planta A3 rev4 aprobada, con el mobiliario en gris.
- **De la referencia [PR]:** simbología, alturas, notas y valores de conductores y disyuntores.
- **Subtablero TN2:** en el pasillo, junto a la escalera, sobre el TP del N1.

## Contenido
- **Iluminación, circuito TN2-1** (luminarias empotradas en gypsum):
  - a: suite;
  - b: baño;
  - c: walk-in;
  - d: galería y pasillo, con tres vías;
  - e: tres vías de la luz de gradas del N1;
  - f: comedor;
  - g: cocina;
  - h: sala familiar;
  - i: gradas N2–N3, con tres vías.
- **Tomacorrientes:**
  - TN2-3: generales de la suite, el pasillo y la sala;
  - TN2-5: cocina 1, GFCI sobre mueble;
  - TN2-7: cocina 2 (refrigeradora, despensa a 1,50 m y aparador);
  - TN2-9: baño, GFCI.
- **Salidas especiales 240 V:**
  - TN2-11/13: cocina eléctrica, 2P-40 A;
  - TN2-15/17: calentador de paso del baño de la suite 1, 2P-40 A.
- **TV y datos:** TV en la suite y en la sala; datos en la sala y en el escritorio de la suite, desde el PVD.
- **Cuadros y notas:** cuadro de circuitos del TN2, simbología y notas 1 a 10.

## Pendientes
1. **Ubicación de salidas:** es una propuesta, para su revisión.
2. **Salidas de 240 V:** altura y conexión según el fabricante del equipo (PD).
3. **Cargas, caídas de tensión y alimentador del TN2:** en la E04 [PR].

## Validación
- DXF revisado con `recover` y `audit`: 0 errores.
- PDF revisado visualmente por zonas.
- No se probó en AutoCAD.
