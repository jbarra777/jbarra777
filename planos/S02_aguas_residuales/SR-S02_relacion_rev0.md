# Lámina S02 · AGUAS RESIDUALES · rev0 (versión de trabajo)

**Estado:** versión de trabajo para revisión. No apta para construcción ni trámite.

## Archivos
| Archivo | Uso |
|---|---|
| `SR-S02_AGUAS_RESIDUALES_rev0.pdf` | Plano para revisar (A1 al 100 %) |
| `SR-S02_AGUAS_RESIDUALES_rev0.dxf` | Editable AutoCAD 2018, layout `S02-AGUAS-RESIDUALES` |

Generador: `scripts/s02_aguas_residuales.py`, con las piezas comunes de `scripts/sanit.py` (se agregaron los símbolos de bajante, sifón de piso, caja de registro y drenaje).
Bases en gris: A2 rev3, A3 rev4 y A4 rev4 (aprobadas).

## Contenido
1. **Plantas de los niveles 1, 2 y 3** a escala 1:100.
   - **N3:** ramales de los tres baños: WC 4", LM 2", SP (ducha) 2". Bajantes de aguas negras (AN) de 4" y de aguas grises (AG) de 2", con ventilación de 2" a techo.
   - **N2:**
     - baño de la suite 1;
     - forro con las bajantes de la suite 1 en el walk-in;
     - **ducto de la cocina** (esquina D/4) con las bajantes de la suite 2 y el fregadero (LP 2");
     - **ducto de la sala** junto a C6 con las bajantes de la suite 3.
   - **N1:**
     - colectores colgados bajo la losa del N2 desde la suite 1 hasta C2;
     - colectores enterrados AG (x 6.00) y AN (x 6.60) de 4";
     - cajas de registro al pie de cada grupo de bajantes;
     - trampa de grasa en el colector AG;
     - en el patio posterior: CR de entrada, tanque séptico, cilindro de inspección, FAFA, CR de distribución y drenaje.
2. **Detalle 1, tanque séptico con FAFA** [PR], vista superior y lateral a 1:25:
   - tanque de 2.00 × 1.04 interior, en cámaras de 2/3 y 1/3;
   - FAFA de 0.80 × 1.04 interior;
   - profundidad útil de 1.20 y borde libre de 0.30;
   - tees, falso fondo, piedra cuarta y respiradero.
3. **Detalle 2, sección de drenaje** [PR], a 1:10: zanja de 0.50 con tubo perforado de 100 mm y capas de la referencia.
4. **Detalle 3, caja de registro y trampa de grasa** [PR], sección S/E.
5. **Detalle 4, baño típico** (suite 1, y la suite 3 en espejo) a 1:40.
6. **Simbología y notas 1–18.** Las notas vienen de la referencia, sin la cita de decreto, según su política de no citar normativa.

## Decisiones del usuario aplicadas (07-10-2026)
- **Bajantes y ductos:** se aplicó la propuesta aprobada.
  - **Suite 1:** bajantes en el forro del muro baño/walk-in y colector colgado hasta C2.
  - **Suite 2 + fregadero:** ducto en la esquina D/4 de la cocina.
  - **Suite 3:** ducto junto a C6 en la sala.
- **Tanque y drenaje en el patio posterior.**

## Ajustes respecto a lo propuesto (avisar)
- **El drenaje lleva 1 línea de 7.40 m, no 2 líneas paralelas.** Con las placas de cimentación F1/F2 (1.65 × 1.65, C01) y la VA1 en el eje 6, el tanque solo cabe a partir de y 26.00. Entre el tanque y la tapia del fondo queda espacio para una sola zanja. La referencia suma 8.00 m (4 × 2.00); aquí se dibujan 7.40 m (PD), sujetos a la prueba de infiltración y al cálculo.
- **Separaciones ajustadas:**
  - del tanque a la zanja, 0.32 m;
  - de la zanja a la VA1 del fondo, unos 0.20 m.

  Se marcan PD para verificar.
- **Trampa de grasa:** en la referencia está a la entrada del tanque. Aquí se ubicó en el colector de aguas grises, bajo el jardín seco del N1, porque el patio no tiene espacio para ella.
- **FAFA:** la nota de la referencia dice 1.00 × 0.80 y su dibujo, 1.04 de ancho. Se dibujó y anotó 1.04 × 0.80 para que coincida con el ancho del tanque.

## Interferencia con una lámina aprobada (S01)
- **El punto de jardín posterior de la S01** (x 4.75, y 25.90) y la tubería AF enterrada por el eje C quedan a unos 0.10 m del borde del tanque (y 26.00) y a 0.5 m del cilindro de inspección.
  - **Recomiendo** trasladar ese punto de jardín, por ejemplo junto al muro D o al frente del patio, en una **S01 rev1**.
  - **No lo modifiqué** porque la S01 está aprobada. Indique si se hace.

## Pendientes
- **PD:**
  - dimensiones de los ductos (0.30 × 0.40) y del forro (0.20);
  - pendientes de colectores y ramales;
  - profundidad de las cajas y de la trampa;
  - camisas en los cruces con las VA1;
  - longitud del drenaje.
- **Prueba de infiltración y cálculo del tanque:** no se han hecho. El tanque es el esquema de la referencia [PR].
- **Cruces en planta:** los colectores se cruzan en dos puntos, el lateral AG de la suite 2 sobre el colector AN y el lateral AN de la suite 3 sobre el AG. Las profundidades relativas son PD.
- **[PR]:** diámetros, materiales, detalles y notas tomados de la referencia, pendientes de su revisión.

## Validación
- DXF revisado con `recover` y `audit`: 0 errores.
- PDF revisado visualmente por zonas: plantas N1–N3, detalles, simbología y notas.
- No se probó en AutoCAD.
