# Lámina C03 · ENTREPISOS · rev1 (versión de trabajo)

**Estado:** versión de trabajo. No apta para construcción ni trámite. La rev0 está aprobada. La rev1 solo cambia la leyenda, por indicación del usuario.

## Archivos
| Archivo | Uso |
|---|---|
| `SR-C03_ENTREPISOS_rev1.pdf` | Plano para revisar (A1 al 100 %) |
| `SR-C03_ENTREPISOS_rev1.dxf` | Editable AutoCAD 2018, layout `C03-ENTREPISO` |

Generador: `scripts/c03_entrepisos.py`.

## Cambios respecto de la rev0
- Título de la vista: "PLANTA DE ENTREPISO" → **"PLANTA DE ENTREPISO 1 Y 2"**.
- Subtítulo: **"ENTREPISO 1: NIVEL 2 (NPT +3.00) / ENTREPISO 2: NIVEL 3 (NPT +6.00)"**.
- Cajetín:
  - contenido: "PLANTA DE ENTREPISO 1 Y 2.";
  - revisión 1: "ENTREPISOS 1 Y 2 EN UNA SOLA LÁMINA".
- Geometría, detalles, simbología y notas: **sin cambios** (los de la rev0 aprobada).
- Ya no habrá una lámina C04 de entrepiso del nivel 3.

## Pendientes heredados de la rev0
- Verificar en el cálculo:
  - la V1 del eje 1 (8,85 m sin columna en C);
  - las luces de las viguetas (4,77 / 4,09 m).
- Separación de la malla #3 y uniones soldadas: PD.
- Arriostre A1: va en los pórticos.

## Validación
- DXF revisado con `recover` y `audit`: 0 errores.
- PDF revisado visualmente (título y cajetín).
- No se probó en AutoCAD.
