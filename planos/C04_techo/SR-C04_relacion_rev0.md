# Lámina C04 · TECHO · rev0 (versión de trabajo)

**Estado:** versión de trabajo para revisión. No apta para construcción ni trámite.

## Archivos
| Archivo | Uso |
|---|---|
| `SR-C04_TECHO_rev0.pdf` | Plano para revisar (A1 al 100 %) |
| `SR-C04_TECHO_rev0.dxf` | Editable AutoCAD 2018, layout `C04-TECHO` |

Generador: `scripts/c04_techo.py`.

## Criterio
El techo de la referencia es una losa de concreto y no aplica. Los perfiles de cubierta son los que aceptó el usuario el 06-10-2026:
- clavadores RT 2x4" en 1,50 mm @0,90 m como máximo;
- cerchas CE-1 con cordones de 2x6" en 2,38 mm (planos) y diagonales y montantes de 2x2" en 1,50 mm;
- vigas de corona V1 a +9,00 en los ejes 1 a 6 y en A, C y D;
- cercha del eje C continua sobre el patio P1.

La ubicación de las cerchas (x 0,30, eje B, eje C, x 8,70), la pendiente del 13 % y la lámina cal. 26 vienen de la A5/A6. C1 y V1 se marcan [PR].

## Contenido
- **Planta de techo 1:50:**
  - estructura: cubierta, cumbrera, cerchas CE-1, clavadores, vigas de corona y columnas;
  - patios P1 y P2 abiertos;
  - pendientes, canoas (frente, fondo y hacia P1 y P2) y bajantes.
- **Cercha típica CE-1, elevación 1:75:** alero a cumbrera, montantes @≈1,0 m, diagonales tipo Pratt, apoyos en las V1 de los ejes 1 a 6.
- **Sección típica de cubierta 1:10:** lámina, clavador, cordones, montante y V1.
- **Simbología y notas 1 a 8.**

## Pendientes y puntos a confirmar
1. **Niveles de la cubierta (afecta a A5 y A6, que están aprobadas).** Con la cercha aceptada (peralte de 0,10 en el alero sobre +9,00) más el clavador de 0,10, la lámina queda a **+9,20 en el alero y +10,70 en la cumbrera**. La A5 y la A6 indican +9,00 y +10,50.
   - Opciones:
     - a) aceptar +9,20 / +10,70 y corregir la A5 y la A6 al final, junto con las referencias C08 → C07;
     - b) bajar la V1 de corona, lo que choca con el cielo a 8,70 del nivel 3.
   - Marcado como PD en la nota 6.
2. **Uniones soldadas y verificación de perfiles:** PD, según la memoria de cálculo.
3. **Canoas y bajantes:** el detalle y las descargas van en la lámina pluvial.
4. **Cerchas junto a los linderos (x 0,30 y 8,70):** apoyan en las V1 de los ejes 1 a 6, no en las V1 de los ejes A y D.

## Validación
- DXF revisado con `recover` y `audit`: 0 errores.
- PDF revisado visualmente por zonas: sin textos superpuestos ni vistas recortadas.
- No se probó en AutoCAD.
