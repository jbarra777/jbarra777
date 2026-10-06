# Lámina C03 · ENTREPISO NIVEL 2 · rev0 (versión de trabajo)

**Estado:** versión de trabajo para revisión. No apta para construcción ni trámite.

## Archivos
| Archivo | Uso |
|---|---|
| `SR-C03_ENTREPISO_N2_rev0.pdf` | Plano para revisar (A1 al 100 %) |
| `SR-C03_ENTREPISO_N2_rev0.dxf` | Editable AutoCAD 2018, layout `C03-ENTREPISO` |

Generador: `scripts/c03_entrepisos.py N2`. El mismo script con `N3` producirá la C04.

## Criterio
Las secciones son las de la referencia (RIVERGRAND C03–C05), marcadas [PR]:
- viguetas de tubo rectangular 2×6" en 2,38 mm @0,60 m;
- lámina ondulada de hierro galvanizado;
- losa colada en sitio con malla #3 electrosoldada;
- vigas V1 4×8" en 3,17 mm y columnas C1 6×6".

El paquete es el aprobado en la A6: **0,30 = V1 0,20 + losa 0,10**. Las viguetas quedan a ras del borde superior de las vigas.

## Contenido
- **Planta de entrepiso del nivel 2, a 1:50:**
  - 17 columnas C1 (las del eje C con forro de 0,30);
  - vigas V1 en los ejes 1 a 6 (marcos A-C-D) y en los ejes A, C y D;
  - V1 en el eje B como borde del patio P1 (ejes 2–3) y de la escalera (ejes 4–5);
  - viguetas en sentido transversal, con separación máxima de 0,60 m repartida en cada paño;
  - vacíos de los patios P1 y P2 y de la escalera;
  - ejes y cotas.
- **Detalle de entrepiso (1:10):** corte perpendicular a las viguetas.
- **Sección A-A (1:10):** a lo largo de la vigueta, con la unión a la V1.
- **Simbología y notas 1–9.**

## Supuestos y puntos a confirmar
1. **Sentido de las viguetas:** las dispuse en sentido transversal (x), con luces de **4,77 m (A–C)** y **4,09 m (C–D)**. Son mayores que las de la referencia (≈3,6 m), así que hay que verificar el perfil 2×6" en el cálculo.
2. **Eje C entre los ejes 1 y 2:** la V1 del eje C apoya a media luz en la V1 del eje 1, porque no hay columna C1 en ese punto (portón). Esa viga salva 8,85 m entre A y D con la sección V1 de la referencia. **Es el punto más crítico: hay que verificarlo en el cálculo** (puede requerir otro perfil).
3. **Eje C entre los ejes 2 y 3:** no lleva viga, porque queda dentro del vacío del patio P1.
4. **Arriostre A1 (4×4"):** no lo ubiqué en el entrepiso. Lo dejo para los pórticos (C06–C07), salvo que usted indique otra cosa.
5. **Separación de la malla #3 y uniones soldadas:** PD, según el cálculo.
6. **Terminología:** la A6 dice "lámina colaborante" y aquí, como en la referencia, "lámina ondulada de hierro galvanizado". Es el mismo elemento.

## Validación
- DXF revisado con `recover` y `audit`: 0 errores.
- PDF revisado visualmente por zonas: sin textos superpuestos ni vistas recortadas.
- No se probó en AutoCAD.
