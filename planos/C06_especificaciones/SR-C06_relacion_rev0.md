# Lámina C06 · ESPECIFICACIONES CONSTRUCTIVAS · rev0 (versión de trabajo)

**Estado:** versión de trabajo para revisión. No apta para construcción ni trámite.

## Archivos
| Archivo | Uso |
|---|---|
| `SR-C06_ESPECIFICACIONES_rev0.pdf` | Plano para revisar (A1 al 100 %) |
| `SR-C06_ESPECIFICACIONES_rev0.dxf` | Editable AutoCAD 2018, layout `C06-ESPECIFICACIONES` |

Generador: `scripts/c06_especificaciones.py`.

## Criterio
Es la lámina C10 de la referencia, **casi sin cambios**, por indicación del usuario. Todo se marca [PR].

## Contenido
- **Tablas:**
  - dimensiones de ganchos estándar;
  - dobleces de aros y estribos;
  - longitud mínima de traslape (con las notas 1–11);
  - recubrimientos mínimos (con las notas 1–4).
- **Notas:** generales (1–7), de materiales (1–9), de cimentaciones y de apuntalamiento de vigas y viguetas.
- **Especificaciones técnicas de materiales:** concreto, acero de refuerzo, bloques, acero estructural, soldadura y pintura de uniones.

## Ajustes respecto de la referencia
1. **Sin citas normativas** (ACI 318-14, CSCR-2010) en los títulos de las tablas ni en los bloques, con el mismo criterio de la A11. Los valores no cambian.
2. **Marcas con "o similar":** Master Flow y RE-50SD de Hilti.
3. **Cimentaciones:** se quitó el informe de suelos de la referencia (n.º 3439-2016, Laboratorio INSUMA), porque es de otro proyecto. Queda qadm = 12 t/m² con F.S. = 3, a verificar con el estudio de suelos de esta vivienda (PD).
4. **Secciones eliminadas porque no aplican:** madera estructural y obras de retención (el lote es plano y no lleva muros de contención).
5. **Nota general 1:** las medidas de esta lámina están en milímetros. Las demás láminas usan metros.
6. **Se omitieron los dibujos esquemáticos** del gancho típico y del doblez a 135°. Las tablas mantienen sus valores.

## Pendientes
- **Notas de prefabricados** (materiales 8 y 9: sobrelosa de 70 mm y contraflecha): son de la referencia. El entrepiso de esta vivienda es lámina con losa de 0,10, así que se pueden eliminar si usted lo prefiere.
- **Estudio de suelos:** PD.

## Validación
- DXF revisado con `recover` y `audit`: 0 errores.
- PDF revisado visualmente: sin textos superpuestos.
- No se probó en AutoCAD.
