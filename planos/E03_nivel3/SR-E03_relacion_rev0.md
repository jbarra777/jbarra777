# Lámina E03 · PLANTA ELÉCTRICA NIVEL 3 · rev0 (versión de trabajo)

**Estado:** versión de trabajo para revisión. No apta para construcción ni trámite.

## Archivos
| Archivo | Uso |
|---|---|
| `SR-E03_NIVEL3_rev0.pdf` | Plano para revisar (A1 al 100 %) |
| `SR-E03_NIVEL3_rev0.dxf` | Editable AutoCAD 2018, layout `E03-NIVEL3` |

Generador: `scripts/e03_nivel3.py` (simbología común `elec.py`).

## Criterio
- **Base:** planta A4 rev4 aprobada, con el mobiliario en gris.
- **Ubicación:** mismos criterios de la E01 y la E02, ya aprobados. Las suites 1 y 3 repiten el esquema de la suite 1 del N2; la suite 3 en espejo.
- **Subtablero TN3:** en el pasillo, junto a la escalera, sobre el TN2 y el TP.

## Contenido
- **Iluminación, circuito TN3-1:**
  - suite 1: a, b, c;
  - galería y pasillo: d, con tres vías;
  - gradas: S3 'i' (tres vías con el N2) y luz 'j' de llegada;
  - suite 2: k, l, m;
  - suite 3: n, o, p.
- **Tomacorrientes:**
  - TN3-3: suite 1 y pasillo;
  - TN3-5: suites 2 y 3;
  - TN3-7: baños, GFCI.
- **Calentadores de paso, 240 V, 2P-40 A:** TN3-9/11 (suite 1), TN3-13/15 (suite 2) y TN3-17/19 (suite 3).
- **TV y datos:** en cada suite, desde el PVD.
- **Cuadros y notas:** cuadro de circuitos del TN3, simbología y notas 1 a 10.

## Pendientes
- Cargas, caídas de tensión y alimentador del TN3: en la E04 [PR].

## Validación
- DXF revisado con `recover` y `audit`: 0 errores.
- PDF revisado visualmente por zonas.
- No se probó en AutoCAD.
