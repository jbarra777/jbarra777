# Lámina C05 · PÓRTICOS · rev1 (versión de trabajo)

**Estado:** versión de trabajo para revisión. No apta para construcción ni trámite.

## Archivos
| Archivo | Uso |
|---|---|
| `SR-C05_PORTICOS_rev1.pdf` | Plano para revisar (A1 al 100 %) |
| `SR-C05_PORTICOS_rev1.dxf` | Editable AutoCAD 2018, layout `C05-PORTICOS` |

Generador: `scripts/c05_porticos.py`.

## Cambios respecto de la rev0 (C05 y C06), por indicación del usuario
- **C05 y C06 unificadas en una sola lámina, a 1:100** (la misma escala de la referencia). La C06 rev0 queda sin efecto.
- **C2 y A1 de la referencia eliminados:** no se usan en este proyecto.
- **Eje C en el eje 1:**
  - se agrega la **columna C1 en los niveles 2 y 3**;
  - arranca sobre una **viga de transferencia VT-1** en el eje 1, a nivel del entrepiso del nivel 2, de **diseño especial (PD)**;
  - **no hay columna en el nivel 1** (portón);
  - se muestra en el pórtico C y en el pórtico 1.

## Contenido
- **Pórticos A y D:** C1 en los ejes 1 a 6, V1 en N2, N3 y corona, VA1 y placas F2.
- **Pórtico C:**
  - C1 en los ejes 2 a 6, más la C1 del eje 1 en N2–N3 sobre la VT-1;
  - sin vigas en el vano 2–3 (patio P1);
  - placas F1.
- **Pórticos 2 a 6:** C1 en A, C y D; V1 de A a D; cerchas cortadas; placas F2–F1–F2.
- **Pórtico 1:** C1 en A y D en todos los niveles y en C en N2–N3; VT-1 en N2 de A a D; V1 en N3 y corona.
- Simbología (C1, V1, VT-1, VA1, F1/F2) y notas 1 a 8.

## Láminas aprobadas afectadas (corregir al final)
- **C03 (entrepisos):**
  - agregar la C1 del eje C en el eje 1 en la planta del entrepiso 2 (nivel 3) y su apoyo sobre la VT-1 del entrepiso 1;
  - cambiar la V1 del eje 1 del entrepiso 1 por la VT-1;
  - corregir la nota "SIN COLUMNA EN EL EJE C DEL EJE 1".
- **C04 (techo):** agregar la C1 en C-1 (llega a la corona) y corregir el rótulo "SIN COLUMNA EN EL EJE C".
- **A3 y A4 (plantas de los niveles 2 y 3):** agregar la columna del eje C en la fachada frontal, forrada a 0,30 como las demás del eje C, y revisar su efecto en la ventana o el muro de la fachada.
- **A5 (fachada frontal) y A7:** revisar si la columna afecta los vanos del frente.

## Pendientes
1. **VT-1:** sección y diseño especial según la memoria de cálculo (PD).
2. **Uniones y verificación de perfiles:** PD.
3. **Número de la lámina de especificaciones:** con la unión queda libre la C06.

## Validación
- DXF revisado con `recover` y `audit`: 0 errores.
- PDF revisado visualmente por zonas: sin textos superpuestos ni vistas recortadas.
- No se probó en AutoCAD.
