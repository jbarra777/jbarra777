# Lámina S01 · AGUA POTABLE · rev0 (versión de trabajo)

**Estado:** versión de trabajo para revisión. No apta para construcción ni trámite.

## Archivos
| Archivo | Uso |
|---|---|
| `SR-S01_AGUA_POTABLE_rev0.pdf` | Plano para revisar (A1 al 100 %) |
| `SR-S01_AGUA_POTABLE_rev0.dxf` | Editable AutoCAD 2018, layout `S01-AGUA-POTABLE` |

Generador: `scripts/s01_agua_potable.py`, con las piezas comunes de `scripts/sanit.py`.
Bases en gris: A2 rev3, A3 rev4 y A4 rev4 (aprobadas), con el mobiliario.

## Contenido
1. **Plantas de agua potable de los niveles 1, 2 y 3** a escala 1:100.
   - **N1:** acometida ESPH 3/4", medidor y llave de paso 3/4" en el frente. Tramo principal de 3/4" bajo contrapiso hasta el montante. Dos puntos de jardín de 1/2" (frontal y posterior).
   - **Montante AF 3/4"** embebido en el muro del eje C, junto a la escalera y el patio P2. Sube del N1 al N3.
   - **N2:**
     - fregadero de cocina (LP 1/2") con llave de paso;
     - baño de la suite 1: ramal por el entrepiso y el pasillo, llave de paso, LM, WC y ducha con calentador de paso.
   - **N3:** baños de las suites 1, 2 y 3. Cada uno lleva llave de paso, LM, WC y ducha con calentador de paso. La suite 3 es el espejo de la suite 1.
2. **Diagrama vertical esquemático:** montante y ramales por nivel.
3. **Detalle 1, acometida y medidor** [PR]: la caja del medidor queda según la ESPH (PD).
4. **Detalle 2, calentador de paso en ducha:** elevación esquemática. La altura y la conexión van según el fabricante; el circuito está en E02/E03.
5. **Simbología y notas 1–8.**

## Criterios aplicados (definidos por el usuario el 06-10-2026)
- Abastecimiento directo de la red ESPH, **sin tanque ni bombeo**. Los valores son de la referencia [PR].
- **Agua caliente solo en duchas**, con un calentador de paso por baño, coherente con los circuitos de 240 V aprobados en E02 y E03.
- Diámetros de la referencia [PR]: 3/4" en la acometida, el tramo principal y el montante; 1/2" en los ramales y las salidas.

## Pendientes
- **PD:** ubicación y tipo de la caja del medidor, según la ESPH.
- **PD:** clase o SDR de las tuberías, según el cálculo hidráulico. Esta lámina no incluye el cálculo de demanda ni de presiones.
- **PD:** prueba de presión de la red.
- **[PR]:** diámetros y notas tomados de la referencia, a la espera de la revisión del usuario.
- **A confirmar:** la ubicación del montante en el muro del eje C y el recorrido de los ramales por el entrepiso. Son propuesta mía, no decisión aprobada.

## Validación
- DXF revisado con `recover` y `audit`.
- PDF revisado visualmente por zonas: se corrigieron los rótulos del N3 que se superponían con el patio P2, la columna C5 y el muro del vestidor de la suite 3.
- No se probó en AutoCAD.
