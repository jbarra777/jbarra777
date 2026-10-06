# CONTEXTO DEL PROYECTO: Vivienda unifamiliar de 3 niveles, San Rafael de Heredia

> Archivo de traspaso. Si se abre una sesión nueva de Claude, leer este archivo primero.
> Última actualización: 06-10-2026. Lámina en curso: **A5 rev0 (en revisión)**. A4 rev0 aprobada; el ducto de la suite 3 se ubica en las láminas sanitarias. A3 rev0 aprobada ("Está perfecto"); altura de piso a piso de 3.00 m confirmada. A2 rev1 aprobada ("De acuerdo, continuar con la siguiente"). A1 en rev1 (cambios pedidos aplicados; el ingeniero indicó continuar).

## 1. Encargo vigente (sustituye al de anteproyecto del 05-10-2026)
- Juego completo de planos constructivos para el CFIA de una **vivienda unifamiliar de 3 niveles**. Solo uso unifamiliar: sin apartamentos ni notas de conversión.
- **Una lámina a la vez.** Se avanza únicamente cuando el ingeniero escribe: *"Lámina aprobada, continuar con la siguiente"*.
- Cada lámina se entrega como DXF editable (AutoCAD 2018) + PDF de revisión en A1 + una relación breve del contenido, los ajustes y los pendientes.
- No se inventan datos. Las notas y tablas tomadas de la referencia se marcan **[PR]** (pendiente de revisión) hasta que el ingeniero indique otra cosa.
- No se copian de la referencia la estructura, las instalaciones, los cálculos ni la geometría.
- Referencia de formato: juego RIVERGRAND (37 láminas A1: ARQ A1–A11, CIVIL C01–C10, ELECT EL1–EL10, SANIT IS1–IS6). Las plantas siguen el lenguaje gráfico de las páginas 3 y 4.

## 2. Programa
- **Nivel 1:** parqueos (al menos 6: 3 independientes + 3 en tándem, espacios de 2.50 × 5.00 m), acceso peatonal de 1.20 m al oeste y escalera.
- **Nivel 2:** suite al frente, cocina-comedor en el centro, sala familiar al fondo. La cocina y la sala no llevan baño.
- **Nivel 3:** tres suites.
- **Cada suite:** dormitorio abierto con estar, baño y walk-in closet. Solo el baño y el walk-in son recintos cerrados.
- **Modelo de plantas:** A-201 (nivel 2) y A-202 (nivel 3), versión del 05-10-2026 ajustada con ChatGPT. Se conserva esa versión y se corrigen detalles.

## 3. Lote (catastro 4-57389-2023, CRTM05). Ver `datos/lote_catastro.json`
- Vértices: 1 (489351.38, 1106442.25) · 2 (489356.04, 1106442.46) · 3 (489360.38, 1106442.62) · 4 (489361.72, 1106414.19) · 5 (489352.73, 1106413.77).
- Área: 256 m² según catastro; 256.57 m² según coordenadas. Frente al **norte**. El eje del lote tiene azimut 177.3°, así que en los dibujos el norte va girado −2.714°.
- Folio real 4-041200-000. No se contempla la segregación. Se ignoran las cotas de 7.00 y 10.67 m del catastro.
- Amarre: desde el vértice 3 al P.I., acimut 101°22′, 75.71 m.

## 4. Decisiones aprobadas
| Tema | Decisión |
|---|---|
| Altura de piso a piso | 3.00 m en los 3 niveles (**confirmada**) |
| Terreno | Plano, a nivel de acera |
| Retiros | Frontal 2.00 m desde el vértice 3 (2.06 en el vértice 1); posterior ≥ 3.00 m (resulta 3.33); laterales 0 con fachadas ciegas |
| Muros | Exteriores 0.15 m, interiores 0.12 m |
| Pasillo | 1.20 m libres, al oeste |
| Cobertura | 70.13 % (179.53 / 256). **El ingeniero la acepta como cumplimiento.** |
| Baños | Con extractor mecánico |
| Aguas residuales | Tanque séptico + drenaje en el patio posterior (no hay alcantarillado) |
| Agua potable | Red de la ESPH |
| Aguas pluviales | A la cuneta pública |
| Lavandería | Pospuesta ("no pensar en lavanderías aún") |
| Altura para medir patios | Desde el nivel 1, ≈ 9.50 m |
| Cajetín | Profesionales de la referencia: Steven Viales (Civil) IC-40759 y David Barrantes (Electricidad) IE-27499. Folio real y plano catastrado del catastro. |
| Ubicación geográfica | La misma imagen del catastro |
| Formato | A1 (841 × 594 mm); códigos de lámina como la referencia (A1, A2…) |
| Patios P1/P2 | 2.50 m: **aceptados por la municipalidad** (altura medida desde N1) |
| Empresa del cajetín | CivilCon Diseño y Construcción SRLTDA, céd. 3-102-762712 (confirmada) |
| Nota de tapia | Se incluye la nota 2 de la referencia (prolongar tapia hasta viga corona) |

## 5. Geometría base (marco local: x hacia el este desde el lindero oeste; y hacia el sur desde el frente en el vértice 1)
- Envolvente: x 0.00–9.00 · y 2.06–25.18 (9.00 × 23.12 = 208.08 m²).
- Cadena de fondos en y: 2.06 | módulo 1 (0.15 + 5.40 + 0.15) | 7.76 P1 10.26 | módulo 2 (0.15 + 6.42 + 0.15) | 16.98 escalera/P2 19.48 | módulo 3 (0.15 + 5.40 + 0.15) | 25.18.
- Pasillo en x 0.15–1.35. P1 en x 1.47–8.85 (7.38 × 2.50). Escalera en x 1.35–4.69. P2 en x 4.81–8.85 (4.04 × 2.50).
- Escalera en U transversal: 17 contrahuellas de ≈ 0.176 m, huella de 0.28 m, tramos de 1.10 m, descanso.

## 6. Correcciones detectadas en A-201 y A-202 (aplicar en las láminas de plantas)
1. Las puertas de la suite del frente (N2), la sala familiar (N2) y la suite 3 (N3) están en el muro de colindancia oeste. Hay que moverlas al muro del eje 2 y al del eje 5, al final del pasillo.
2. La escalera está dibujada como tramo recto y rotulada "existente". Debe ser en U y nueva.
3. Baños de 1.55 × 2.20 m: amueblar en línea (ducha de 0.85 en el extremo de la ventana, inodoro, lavatorio). Puerta de 0.80 m, abatible hacia afuera o corrediza donde haya muro.
4. "Paso común" pasa a llamarse "pasillo". Va cerrado con vidrio o baranda frente a P1.
5. Las cotas mezclan medidas libres y brutas. Hay que redefinir los ejes en el centro de los muros.
6. Proponer cocina en L con península (ahora tiene una mesada de 2.5 m).
7. Los walk-in de 3.46 × 3.25 m son holgados; se mantienen salvo indicación.

## 7. Pendientes abiertos
- Verificar el reglamento vigente (INVU 2018/2022) y el plan regulador de San Rafael.
- Definir el índice y el total de láminas del juego.
- Estructura, instalaciones y prueba de infiltración: pendientes de los criterios del profesional responsable.

## 8. Estado de láminas
| Lámina | Contenido | Estado |
|---|---|---|
| A1 | Lote: ubicación, poligonal, retiros y huella, derrotero, coordenadas, áreas, notas | rev1 (cambios aplicados; se indicó continuar) |
| A2 | Planta nivel 1 (1:50): parqueos, acceso, gradas, jardín seco, derrotero, áreas, cobertura, notas | **rev1 aprobada** |
| A3 | Planta nivel 2 (1:50): suite 1, cocina-comedor, sala familiar, áreas, cobertura, detalle extractor, notas | **rev0 aprobada** |
| A4 | Planta nivel 3 (1:50): suites 1, 2 y 3, áreas, cobertura, detalle extractor, notas | **rev0 aprobada** |
| A5 | Fachadas: principal 1:50, posterior 1:75, laterales 1:100 | rev0 entregada, en revisión |

### Fachadas (A5 rev0)
- **Criterio del ingeniero:** fachadas sencillas. En la principal, ventanas de piso a 2.20 m (dormitorio, baño y walk-in), alineadas entre niveles, para modelar después una fachada moderna. Baños con vidrio arenado (sandblast).
- Ventanas del frente (x local): dormitorio 0.70–2.90, baño 3.95–4.95, walk-in 6.40–8.20. Portón de 2.40 m de alto (supuesto).
- Cubierta +9.00 y pretil +9.60: por definir con el diseño de techos y la altura municipal.
- Fachada posterior: antepecho 0.90 (sala y dormitorio) y 1.60 (baño y walk-in).

### Nivel 3 (A4 rev0)
- Las suites 1 y 3 son iguales a la suite del nivel 2 (la 3 en espejo, con el baño contra la fachada posterior).
- Suite 2 (módulo central, 7.38 × 6.42): baño en x 7.30–8.85, y 14.63–16.83, sobre la zona húmeda de la cocina del nivel 2. Walk-in de 2.75 × 4.10 junto a P1 (x 6.10–8.85, y 10.41–14.51). Acceso desde el muro B en y 15.55–16.45.
- La suite 3 necesita un ducto sanitario a través de la sala familiar del nivel 2 (pendiente en las láminas IS).
- Altura de piso a piso: **3.00 m (confirmada)**. NPT: N1 ±0.00, N2 +3.00, N3 +6.00.

### Nivel 2 (A3 rev0)
- Suite 1 en el módulo frontal (8.70 × 5.40): baño en x 3.72–5.27, y 2.21–4.41 (1.55 × 2.20, piezas en línea, puerta de 0.80 hacia el dormitorio) y walk-in en x 5.39–8.85, y 2.21–5.46.
- Cocina-comedor de 7.38 × 6.42: cocina en L (muro este y muro del eje 4 hacia P2) con isla de 2.30 × 0.90 y mesa para 8.
- Sala familiar de 8.70 × 5.40. Pasillo de 1.20 cerrado con vidrio hacia P1. Puertas de la suite y la sala en los ejes 2 y 5, al final del pasillo.
- Área del nivel 2: 179.53 m². Total de construcción: 66.57 + 179.53 + 179.53 = 425.63 m² (el nivel 3 es preliminar).

### Nivel 1 (A2 rev1, según indicaciones del 06-10-2026)
- **Solo 3 estacionamientos** E-1 a E-3 (2.50 × 5.00) en x 1.35–8.85, y 2.21–7.21. Pasillo peatonal de 1.20 al oeste hasta y 19.48. Gradas en U.
- **Todo lo demás del nivel 1 es JARDÍN SECO NO CONSTRUIDO**: bajo los niveles 2 y 3, en los patios y en el patio posterior. No hay bodega ni espacio posterior.
- Área construida del nivel 1: estacionamientos 37.50 + pasillo 20.72 + gradas 8.35 = **66.57 m²**. El cuadro de áreas de la A2 muestra solo eso.
- **Portón vehicular abatible**: 4 hojas plegables de 1.82 m que abren hacia el retiro frontal. Claro libre de 7.29 m. Pilastra en el eje B (x 1.26–1.56). Acceso peatonal de 1.00 m.
- **Columnas sobre el eje C (x 4.84)** en los ejes 2, 3, 4, 5 y 6. Sección preliminar de 0.30 × 0.30, con la cara oeste en x 4.69. C6 queda al ras de la fachada posterior. **No hay columna en C1**, porque obstruiría el portón y el espacio E-2.
- Limpieza del tanque séptico: el ingeniero indicó que no es problema.
- Cobertura: se mantiene en 70.13 % (proyección de los niveles 2 y 3).
- Ejes: A 0.075 · B 1.41 · C 4.84 · D 8.925 / 1 2.135 · 2 7.685 · 3 10.335 · 4 16.905 · 5 19.555 · 6 25.105.
- Marco de las plantas (`planta.py`): X = fondo y local (calle a la izquierda), Y = x local.
- Escalera en U: tramo 1 en y 16.98–18.08 que sube hacia el este hasta x 3.59; descanso en x 3.59–4.69; tramo 2 en y 18.38–19.48 de regreso al oeste.

## 9. Herramientas
- `scripts/cadlib.py`: capas, estilos de cota, cajetín, tablas, escala gráfica, render a PDF (ezdxf + PyMuPDF).
- `scripts/a1_lote.py`, `a2_nivel1.py`, `a3_nivel2.py`, `a4_nivel3.py`, `a5_fachadas.py`: generan las láminas. `hoja.py` reúne las partes comunes de las láminas de planta (A3 en adelante). Requieren `pip install ezdxf pymupdf pillow`.
- `scripts/planta.py`: muros, puertas, ventanas, ejes, niveles, cortes y vehículos en el marco de planta.
- Notas generales y derrotero comunes en `cadlib.NOTAS_GENERALES` / `cadlib.derrotero_rows`.
- Datos en `datos/lote_catastro.json` y `datos/proyecto.json`.
