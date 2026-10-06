# Lámina A1 · LOTE DE TERRENO · rev0 (versión de trabajo)

**Estado:** versión de trabajo para revisión. No apta para construcción ni trámite.

## Archivos
| Archivo | Uso |
|---|---|
| `SR-A1_LOTE_rev0.dxf` | Editable, AutoCAD 2018 (AC1032). Layout de impresión `A1-LOTE`. |
| `A1_ubicacion_catastro.png` | Imagen referenciada por el DXF (ruta relativa: mantener en la misma carpeta). |
| `SR-A1_LOTE_rev0.pdf` | PDF de revisión, A1 841×594 mm, imprimir al 100 %. |
| `scripts/a1_lote.py` | Genera DXF y PDF a partir de `datos/*.json` (es reproducible). |

## Organización del DXF
- **Model Space** en metros (INSUNITS = 6), escala 1:1. Usa un marco local con origen en el vértice 1, el eje Y paralelo al lindero 5-1 y el norte girado −2.714°. El **UCS "CRTM05"** guardado en el dibujo devuelve las coordenadas CRTM05 exactas del catastro (verificado en los 5 vértices).
- **Paper Space** `A1-LOTE` en mm. Tiene 2 viewports bloqueados: poligonal a 1:200 y retiros y huella a 1:100. Cada uno congela las capas de la otra escala.
- **Capas:** `T-LINDERO`, `T-VERTICE`, `T-TXT-100/200`, `T-COTA-100/200`, `A-HUELLA`, `A-HUELLA-TRAMA`, `A-PATIO`, `A-MARCO`, `A-CAJETIN(-TXT)`, `A-TABLAS`, `A-NOTAS`, `A-TITULOS`, `A-NORTE`, `A-ESCALA-GRAF`, `A-IMAGEN-REF`. `A-VIEWPORT` no se imprime.
- **Bloques:** `CAJETIN_A1` (con atributos editables), `NORTE`, `VERTICE`.
- **Cotas:** 18 entidades DIMENSION auténticas, con estilos `COTA-100` y `COTA-200` (trazo oblicuo, 2 decimales). Su asociatividad con la geometría no está garantizada; en AutoCAD se puede restablecer con `DIMREASSOCIATE`.
- **Tablas:** dibujadas con líneas y textos independientes, no con entidades TABLE.

## Contenido
1. Ubicación geográfica: imagen del plano catastrado, sin escala.
2. Poligonal a 1:200: 5 vértices, longitudes de los lados, colindantes y calle pública.
3. Retiros y huella a 1:100, con:
   - envolvente de 9.00 × 23.12 m;
   - patios abiertos P1 (7.38 × 2.50) y P2 (4.04 × 2.50);
   - retiro frontal de 2.06 m (2.00 m en el vértice 3) y retiro posterior de 3.33/3.34 m;
   - zona reservada para tanque séptico.
4. Derrotero con el amarre 3 – P.I. (101°22′, 75.71 m, dato del catastro).
5. Cuadro de coordenadas CRTM05.
6. Cuadro de áreas y cobertura: huella de 179.53 m², cobertura de 70.13 % sobre los 256 m² del catastro. Usted la aceptó.
7. Notas 1–11, simbología, norte, escalas gráficas y cajetín con control de revisiones.

## Ajustes respecto a la referencia (lámina A1 de RIVERGRAND)
- El ancho de vía (cotas de 7.00 y 10.67 m) no se reproduce, por su indicación.
- Se agregó el cuadro de coordenadas de los vértices del lote.
- Se agregaron la flecha norte, las escalas gráficas, el control de revisiones, el cuadro de áreas en tabla y la simbología.
- La nota 2 de la referencia (prolongar la tapia hasta la viga corona) **no se trasladó**. Queda pendiente su decisión.
- Las notas 1 y 6 vienen de la referencia: están marcadas **[PR]**, pendientes de revisión.

## Pendientes y verificaciones
1. **Nota 11:** con la altura medida desde el nivel 1 (≈9.50 m), el texto del reglamento consultado (1983) pide un lado mínimo de 3.00 m y 9.00 m² para patios que sirven a piezas habitables. P1 y P2 miden 2.50 m. **No cumpliría** si ese texto sigue vigente. Hay que decidir o confirmar con la municipalidad y con el reglamento vigente.
2. **Retiros:** son de diseño. Faltan el alineamiento municipal y el certificado de uso de suelo.
3. **Empresa del cajetín:** "CivilCon Diseño y Construcción SRLTDA, céd. 3-102-762712" se tomó de la referencia junto con los profesionales. Hay que confirmarlo.
4. **Total de láminas:** aparece "--" hasta cerrar el índice del juego.
5. **Tanque séptico y drenaje:** requieren prueba de infiltración. El tamaño del patio posterior (≈30 m²) está por verificar.
6. **Imagen de ubicación:** la del catastro tiene baja resolución (≈60 dpi al tamaño impreso).
7. **Cálculo de derrotero y área:** se hizo con las coordenadas del catastro y no sustituye un levantamiento topográfico.

## Validación realizada
- Apertura con `ezdxf.recover` y `audit`: 0 errores.
- Las cotas medidas coinciden con la geometría: 4.66, 4.34, 28.46, 9.00, 28.51, 2.06, 23.12, 3.33, 2.00, 5.70, 2.50, 6.72, 2.50, 5.70, 3.34, 7.38, 4.04 y 9.00.
- El área por coordenadas (256.57 m²) y la huella (179.53 m²) se recalcularon desde la geometría.
- Se comprobó que la envolvente queda dentro del lindero este (holgura de 0.001 a 0.007 m).
- El PDF se generó desde el mismo DXF (layout `A1-LOTE`) y se revisó visualmente por zonas.
- **No se probó en AutoCAD:** no está disponible en este entorno.
