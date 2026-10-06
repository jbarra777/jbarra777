# DECISIONES TÉCNICAS — Registro permanente

**Leyenda de origen:**
- **[U]** indicado o aprobado por el usuario.
- **[CAT]** plano catastrado.
- **[A-20x]** planta base del anteproyecto (A-201 nivel 2, A-202 nivel 3).
- **[Ax]** establecido en la lámina indicada. Su vigencia depende del estado de esa lámina en `INDICE_PLANOS.md`: si está EN REVISIÓN, la decisión puede cambiar, salvo que también lleve [U].

**PENDIENTE DE DEFINIR** = no decidido. **PD** = valor preliminar dibujado, pendiente de confirmar.

## 1. Proyecto y cajetín
- **Proyecto:** VIVIENDA UNIFAMILIAR. Distrito 03 Santiago, cantón 05 San Rafael, provincia 04 Heredia, Costa Rica. [CAT]
- **Profesionales del cajetín:** "Director técnico: Steven Viales (Civil) IC-40759; David Barrantes (Electricidad) IE-27499". Vienen del proyecto de referencia y su uso fue **autorizado por el usuario**. [U]
- **Empresa:** CivilCon Diseño y Construcción SRLTDA, céd. jurídica 3-102-762712 (confirmada). [U]
- **Registro público:** folio real 4-041200-000; plano catastrado 4-57389-2023; área según catastro 256 m². [U][CAT]
- **No contemplar la segregación** que indica el catastro ("para segregar"). [U]
- **Propietario:** no se incluye en el cajetín. No fue solicitado.
- **Formato A1** (841 × 594 mm). [U] Códigos de lámina al estilo de la referencia (A1, A2…; C01…; EL1…; IS1…): en uso desde la A1 y sin objeción del usuario.
- **Cajetín:** espacio para sellos; empresa; profesional; proyecto; registro; contenido; escalas; control de revisiones; estado; lugar, lámina, fecha (OCT 2026) y total. **El total de láminas está PENDIENTE DE DEFINIR**: se muestra "--".

## 2. Lote (catastro 4-57389-2023, CRTM05) — datos en `datos/lote_catastro.json`
- **Vértices (E, N):**
  - 1 (489351.38, 1106442.25)
  - 2 (489356.04, 1106442.46)
  - 3 (489360.38, 1106442.62)
  - 4 (489361.72, 1106414.19)
  - 5 (489352.73, 1106413.77) [CAT]
- **Área por coordenadas:** 256.57 m². Para la cobertura se usa la del catastro, **256 m²**. [U]
- **Lados:**
  - 1-2: 4.66 m, 87°25′
  - 2-3: 4.34 m, 87°53′
  - 3-4: 28.46 m, 177°18′
  - 4-5: 9.00 m, 267°20′
  - 5-1: 28.51 m, 357°17′
  - Calculados de las coordenadas. [A1]
- **Amarre:** 3 – P.I., 101°22′, 75.71 m. [CAT]
- **Frente al norte, a la calle pública.** El lindero 5-1 tiene azimut 357.29°, así que en los dibujos el norte va girado −2.714°. [CAT][A1]
- **Colindantes:** identificador predial 40503004120000 al este, sur y oeste. [CAT]
- Ignorar las cotas de 7.00 y 10.67 m del catastro. [U]
- El terreno es plano y está a nivel de acera. [U]
- Los datos del catastro no sustituyen un levantamiento topográfico (nota en las láminas).

## 3. Implantación, retiros y cobertura
- **Retiros de diseño:**
  - frontal de 2.00 m medido desde el vértice 3; resulta 2.06 en el vértice 1;
  - posterior de al menos 3.00 m; resulta 3.33/3.34;
  - laterales 0, con fachadas laterales ciegas. [U]
  - Falta confirmarlos con el alineamiento y el uso de suelo municipal (nota 4).
- **Envolvente:** 9.00 × 23.12 m (208.08 m²), en y 2.06–25.18 (marco local, §4). [A-201][A1]
- **Patios abiertos desde el nivel 1 hasta el cielo:**
  - P1 de 7.38 × 2.50 (18.45 m²);
  - P2 de 4.04 × 2.50 (10.10 m²);
  - **dimensión aceptada por la municipalidad**, con la altura medida desde el nivel 1 (≈9.5 m). [U]
- **Huella (proyección de los niveles 2 y 3):** 179.53 m². **Cobertura: 70.13 % (179.53/256), aceptada por el usuario como cumplimiento.** [U][A1][A2]

## 4. Marcos de coordenadas, ejes y nomenclatura
- **Marco de diseño (local):** origen en el vértice 1. *x* crece hacia el este a lo largo del frente y *y* hacia el sur a lo largo del lindero 1-5. [A1]
- **Marcos de dibujo:**
  - Model Space de la A1: norte arriba (X = x, Y = −y).
  - Plantas: **marco girado** (X = y, Y = x), con la calle a la izquierda (`planta.py`).
  - Todos los DXF incluyen un UCS "CRTM05". [A1–A4]
- **Ejes de letra (en x):** A 0.075 · B 1.41 · **C 4.84** (centro de columnas; antes 4.75) · D 8.925. [A2 rev1]
- **Ejes de número (en y):** 1 2.135 · 2 7.685 · 3 10.335 · 4 16.905 · 5 19.555 · 6 25.105.
  - Separaciones: 5.55 / 2.65 / 6.57 / 2.65 / 5.55. [A2]
- **Niveles:** se nombran "Nivel 1 / Nivel 2 / Nivel 3". No usar "planta baja". [U]

## 5. Niveles y alturas
- **Altura de piso a piso: 3.00 m (confirmada).** [U]
- **NPT:** N1 ±0.00 (= acera), N2 +3.00, N3 +6.00. [U][A2–A4]
- **Cubierta +9.00 y pretil +9.60: PD.** Dependen del diseño de techos y de la altura máxima municipal (PENDIENTE DE DEFINIR). [A5]

## 6. Muros y estructura arquitectónica
- **Espesores:** muros exteriores 0.15 m e interiores 0.12 m. [U]
- **Muros de colindancia** este y oeste a lo largo de toda la envolvente, ciegos. [U]
- **Nota de tapia**, tomada de la referencia por indicación del usuario: "La tapia colindante de mampostería deberá prolongarse hasta el nivel de la viga corona del último nivel…". Es la nota general 2. [U]
- **Columnas sobre el eje C**, en los ejes 2, 3, 4, 5 y 6 ("cada ~5 m ajustado a ejes"). [U]
  - Sección **0.30 × 0.30 PD**, con la cara oeste en x 4.69 para no invadir el descanso de la escalera. C6 queda al ras de la fachada posterior. [A2 rev1]
  - **Sin columna en C1**, porque obstruiría el portón y el espacio E-2. La viga del eje 1 salva unos 7.3 m entre la pilastra B y el muro D (diseño estructural pendiente). [A2 rev1]
- **Pilastra en el eje B**, en la fachada del nivel 1: x 1.26–1.56. [A2]
- **Sistema estructural, cimentación, entrepisos, secciones y refuerzo: PENDIENTE DE DEFINIR.** No copiar los perfiles de acero de la referencia.

## 7. Distribución
### Nivel 1 [U][A2 rev1]
- **Solo 3 estacionamientos** independientes, E-1 a E-3, de 2.50 × 5.00, en x 1.35–8.85 y y 2.21–7.21, con acceso recto.
- **Pasillo peatonal** de 1.20 libre al oeste (x 0.15–1.35, hasta y 19.48), separado de los carros con un bordillo.
- **Gradas.**
- **Todo lo demás es JARDÍN SECO NO CONSTRUIDO**: bajo los niveles 2 y 3, en los patios y en el patio posterior.
- **Área construida del N1:** 37.50 + 20.72 + 8.35 = **66.57 m²**. El cuadro de la A2 muestra solo estacionamientos, pasillo y gradas.
- **Portón vehicular abatible** de 4 hojas plegables de 1.82 m, que abren hacia el retiro frontal sin invadir la vía. Claro libre de 7.29 m. **Acceso peatonal** de 1.00 m (vano de 1.11). [U][A2]
- Tanque séptico y drenaje en el patio posterior. La limpieza del tanque "no es problema". [U]

### Nivel 2 [A-201][A3]
- **Suite 1** en el módulo frontal (8.70 × 5.40):
  - baño en x 3.72–5.27, y 2.21–4.41;
  - walk-in de 3.46 × 3.25 en x 5.39–8.85, y 2.21–5.46.
- **Cocina-comedor** de 7.38 × 6.42: cocina en L sobre el muro este y el muro del eje 4, isla de 2.30 × 0.90, fregadero bajo la ventana a P2, despensa, aparador y mesa para 8.
- **Sala familiar** de 8.70 × 5.40. **Sin baño** en la cocina-comedor ni en la sala. [U]
- **Área del nivel:** 179.53 m² (incluye muros).

### Nivel 3 [A-202][A4]
- **Suites 1 y 3** iguales a la suite del N2. La suite 3 es su espejo, con el baño en la fachada posterior (y 22.83–25.03) y el walk-in en y 21.78–25.03.
- **Suite 2** (7.38 × 6.42):
  - **baño en x 7.30–8.85, y 14.63–16.83, sobre la zona húmeda de la cocina del N2** (aprobado); [U]
  - walk-in de 2.75 × 4.10 junto a P1;
  - acceso desde el muro B.
- **Área del nivel:** 179.53 m².

### Generales
- **Suites:** dormitorio y estar abiertos. **Solo el baño y el walk-in son recintos cerrados.** [U]
- **Lavandería: no se considera por ahora.** [U]
- **Área total de construcción:** 66.57 + 179.53 + 179.53 = **425.63 m²**. [A3][A4]

## 8. Circulación y escalera
- **Pasillo** de 1.20 libre al oeste, en los niveles 2 y 3 desde el eje 2 hasta el eje 5.
  - Va cerrado con **vidrio fijo hacia P1** (galería). [A3]
  - Los accesos a las suites 1 y 3 y a la sala están **al final del pasillo** (ejes 2 y 5); la cocina y la suite 2 se abren desde el muro B. [A3][A4]
- **Escalera en U transversal**, en x 1.35–4.69 y y 16.98–19.48:
  - 17 contrahuellas de ≈0.176 y huella de 0.28;
  - tramos de 1.10 con ojo de 0.30 y descanso en x 3.59–4.69;
  - tramo 1 en y 16.98–18.08, que sube hacia el este; tramo 2 en y 18.38–19.48, que regresa al oeste. [A2–A4]
- **Barandas:** en las gradas del N1 hacia el jardín seco y en el borde del vacío en el N3. El detalle va en la A11, **PENDIENTE**.

## 9. Baños y ventilación
- **Baños de 1.55 × 2.20** libres. [A-201][U]
  - Piezas **en línea**: ducha de 0.85 junto a la ventana, inodoro y lavatorio de 0.50 sobre el mismo muro.
  - Puerta de **0.80 abatible hacia el dormitorio**. [A3]
- **Extractor mecánico** en todos los baños. [U]
  - Detalle esquemático en A3/A4. **Caudal y modelo PENDIENTE DE DEFINIR [PR].**
- **Ductos sanitarios:**
  - baño de la suite 2 sobre la cocina: se define en las láminas sanitarias; [U]
  - **baño de la suite 3 sobre la sala** del N2: requiere un ducto a definir en las láminas IS. [U]

## 10. Ventanas y puertas
- **Fachada principal, niveles 2 y 3: ventanas de piso a 2.20 m sobre el NPT**, alineadas entre niveles, con franja opaca hasta la losa. [U]
  - Posiciones en x local: dormitorio 0.70–2.90, baño 3.95–4.95, walk-in 6.40–8.20. [A3][A4][A5]
- **Baños de la fachada principal:** vidrio arenado (sandblast). [U]
- **Ventanas hacia P1** desfasadas entre ambos lados del patio, para reducir las visuales cruzadas. [A3][A4]
- **Puertas:** acceso a las suites y a la sala 0.90; baño y walk-in 0.80. Tipos y cuadros en las láminas A7–A9, **PENDIENTE**.
- **Fachada posterior:** posición, antepechos y alineación **PENDIENTE DE DEFINIR** (ver ESTADO; hay un conflicto con C6).
- **Protección de las ventanas desde el piso** (paño fijo laminado de 0.90 o baranda), vidrio de seguridad y altura del portón (2.40, PD): **PENDIENTE DE DEFINIR.**

## 11. Instalaciones (todo lo no indicado está PENDIENTE DE DEFINIR)
- **Agua potable:** red pública de la **ESPH**, conexión directa desde la calle. [U]
- **Aguas residuales:** **no hay alcantarillado**; tanque séptico y drenaje en el patio posterior. [U] Dimensionamiento y prueba de infiltración: PENDIENTE.
- **Aguas pluviales:** a la **cuneta pública**. [U]
- **Electricidad y voz/datos:** PENDIENTE DE DEFINIR. No copiar circuitos ni tableros de la referencia.

## 12. Cubierta, acabados y detalles
- **Tipo de techo** (losa o lámina con pretil): PENDIENTE DE DEFINIR.
- **Acabados de pisos, paredes y fachadas:** PENDIENTE DE DEFINIR (láminas A7–A10).
- **Tapias en los retiros:** altura PENDIENTE DE DEFINIR.

## 13. Criterios gráficos y de presentación
- **Escalas:** A1 a 1:200, 1:100 y S/E; plantas a 1:50; fachadas: principal 1:50, posterior 1:75 y laterales 1:100. [A1–A5]
- **Lenguaje gráfico de plantas** (referencia págs. 3–4): muros cortados con trama, puertas con arco, mobiliario a escala, ejes con burbuja, cotas generales, entre ejes e interiores, NPT, cortes A-A y B-B (remiten a la A6) y norte según catastro.
- **Cada lámina de planta incluye** (como la referencia): derrotero, cuadro de áreas, porcentaje de cobertura y notas. Las A3 y A4 incluyen además el detalle del extractor.
- **Notas generales 1–12** en `cadlib.NOTAS_GENERALES`; luego las notas propias de cada lámina.
  - Las notas 1 (medidas) y 7 (canoas) son **[PR]** (tomadas de la referencia, pendientes de revisión del usuario).
  - La A5 (fachadas) usa su propia lista de notas: 1 medidas [PR], 2 tapia, 3 extractor, más 4–10 propias de las fachadas, igual que la referencia, que en fachadas lleva menos notas.
- **Capas:** muros, puertas, ventanas, mobiliario, cotas, textos, ejes, tramas, estructura, etc. Cajetín como bloque con atributos. Cotas como entidades DIMENSION.
- **Decimales:** cotas con punto (5.70); áreas y porcentajes con coma (179,53 m²), como la referencia.
