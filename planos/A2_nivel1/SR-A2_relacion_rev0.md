# Lámina A2 · PLANTA NIVEL 1 · rev0 (versión de trabajo)

**Estado:** versión de trabajo para revisión. No apta para construcción ni trámite.

## Archivos
| Archivo | Uso |
|---|---|
| `SR-A2_NIVEL1_rev0.pdf` | **Plano para revisar e imprimir** (A1, al 100 %) |
| `SR-A2_NIVEL1_rev0.dxf` | Editable, AutoCAD 2018. Layout de impresión `A2-NIVEL1` |
| `scripts/a2_nivel1.py` | Genera la lámina (usa `planta.py` y `cadlib.py`) |

## Contenido (equivalente a la A2 de la referencia)
1. **Planta del nivel 1 a 1:50** con:
   - ejes A–D y 1–6 en el centro de los muros, con cotas entre ejes;
   - cotas de conjunto (retiro frontal 2.06, envolvente 23.12, retiro posterior 3.33), cotas interiores y de vanos;
   - muros con trama, puertas con arco de apertura y ventanas;
   - 6 vehículos dibujados a escala;
   - escalera en U con flecha de subida y línea de corte;
   - proyecciones de los patios P1 y P2 y de las vigas del nivel 2;
   - niveles NPT, líneas de corte A-A y B-B (con referencia a la lámina A6), norte y lindero con sus vértices.
2. **Derrotero**: el mismo de la A1, con remisión al cuadro de coordenadas de esa lámina.
3. **Cuadro de áreas**: área por nivel y área de construcción, más el desglose del nivel 1.
4. **Porcentaje de cobertura**: 70.13 %.
5. **Notas**: las 12 notas generales de la A1 más las notas 13 a 17, propias del nivel 1.
6. **Cajetín** con el control de revisiones.

**Omitido a propósito:** el *detalle del extractor de aire* de la referencia no aplica aquí, porque el nivel 1 no tiene baños. Irá en las láminas A3 y A4.

## Distribución propuesta del nivel 1 (para su revisión)
| Zona | Medidas libres | Comentario |
|---|---|---|
| Estacionamientos E-1 a E-6 | 7.50 × 10.00 (6 de 2.50 × 5.00) | 3 independientes y 3 en tándem. La fila 2 queda en parte bajo el patio P1, abierto a cielo. |
| Pasillo peatonal | 1.20 libre, al oeste | Llega desde el portón peatonal hasta la escalera y el espacio posterior. Junto a los vehículos lo separa un **bordillo**, no un muro, para que se puedan abrir las puertas de los carros. |
| Fachada frontal | Peatonal 1.11 / pilastra 0.30 / vehicular **7.29** | El claro del portón baja de 7.50 a 7.29 m por la pilastra del eje B. |
| Bodega | 7.38 × 4.50 = 33.21 m² | Es el espacio sobrante del módulo central. **Uso por definir**: también podría ser un 7.º espacio en triple tándem, que no recomiendo. |
| Escalera en U | 3.34 × 2.50 | 17 contrahuellas de 0.176 m, huella de 0.28 m, tramos de 1.10 m con un ojo de 0.30 m. |
| Patio P2 | 4.04 × 2.50, abierto | Acceso desde el espacio posterior. La bodega se ventila hacia él. |
| Espacio cubierto posterior | 8.70 × 5.40 = 46.98 m² | **Uso por definir.** Tiene salida al patio posterior. |
| Patio posterior | 9.00 × 3.33 | Tanque séptico y drenaje: ubicación y dimensiones por diseñar. |

## Pendientes
1. **Usos de la bodega y del espacio cubierto posterior.** Las opciones incluyen bodega, cuarto de máquinas o tableros, lavandería (que quedó pospuesta) o área social.
2. **Tipo de portón vehicular** (seccional, corredizo o abatible) y si las 2 hojas peatonal y vehicular serán independientes.
3. **Estructura.** No dibujé columnas porque el sistema estructural está pendiente. La propuesta parte de que los estacionamientos quedan libres de columnas: claro transversal de 8.70 m entre muros de colindancia, más la pilastra del eje B. Hay que confirmarlo con el diseño estructural.
4. **Áreas de los niveles 2 y 3.** Son preliminares (179.53 m² cada uno) y se confirman en las láminas A3 y A4.
5. **NPT ±0.00 igual al nivel de acera.** Faltan las pendientes de piso hacia los desagües.
6. **Mantenimiento del tanque séptico.** El camión de limpieza no tiene acceso directo al patio posterior. Hay que prever una manguera a través del pasillo, o ubicar el tanque bajo el retiro frontal o los estacionamientos.

## Validación realizada
- DXF abierto con `recover` y `audit`.
- Cotas comparadas con la geometría.
- Área por nivel recalculada (208.08 − 28.55 = 179.53 m²).
- Revisión visual del PDF por zonas.
- No se probó en AutoCAD.
