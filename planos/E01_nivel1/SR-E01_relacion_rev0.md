# Lámina E01 · PLANTA ELÉCTRICA NIVEL 1 · rev0 (versión de trabajo)

**Estado:** versión de trabajo para revisión. No apta para construcción ni trámite.

## Archivos
| Archivo | Uso |
|---|---|
| `SR-E01_NIVEL1_rev0.pdf` | Plano para revisar (A1 al 100 %) |
| `SR-E01_NIVEL1_rev0.dxf` | Editable AutoCAD 2018, layout `E01-NIVEL1` |

Generadores: `scripts/e01_nivel1.py` y `scripts/elec.py` (simbología común para E01–E04).

## Criterio
- **Base:** planta A2 rev3 aprobada, en gris.
- **De la referencia [PR]:** simbología, alturas de montaje, notas y valores de conductores y disyuntores.
- **Esquema del usuario:** medidor en el frente, tablero principal TP en el vestíbulo y subtableros TN2 y TN3.

## Contenido
- **Acometida y alimentadores:**
  - acometida subterránea al medidor, en la pilastra del eje B de la fachada;
  - alimentador subterráneo al TP, por el pasillo peatonal;
  - prevista de voz y datos al PVD, en el pasillo junto al vestíbulo.
- **Iluminación, circuito TP-1:**
  - a: pasillo peatonal, con apagadores de tres vías en el acceso y en el vestíbulo;
  - b: estacionamientos;
  - c: jardín seco frontal;
  - d: vestíbulo;
  - e: gradas, tres vías con la llegada al N2;
  - f: jardín seco posterior;
  - g: aplique exterior en el acceso peatonal.
- **Tomacorrientes, circuito TP-3:** 3 GFCI de intemperie en la colindancia este (estacionamientos y jardines), 1 en el pasillo y 1 en el vestíbulo.
- **Cuadros y notas:** simbología, cuadro de circuitos del N1 y notas 1 a 7.

## Supuestos y pendientes
1. **Ubicación de luminarias, apagadores y tomas:** es una propuesta de Claude; revísela en planta.
2. **Medidor:** su ubicación exacta la define la empresa distribuidora (PD).
3. **Tubería en el N1:** la estructura queda expuesta, así que adapté la nota de la referencia ("en ningún caso tubería expuesta"). La tubería expuesta a menos de 2,5 m será EMT, tomado de las notas de canalizaciones de la referencia.
4. **Secadora (240 V):** el circuito va en el TP, pero la salida no se dibuja porque la ubicación de la lavandería está pospuesta (PD).
5. **Circuitos, cuadros completos y diagrama unifilar:** en la E04, con valores de la referencia [PR].

## Validación
- DXF revisado con `recover` y `audit`: 0 errores.
- PDF revisado visualmente por zonas.
- No se probó en AutoCAD.
