# CAMBIOS DEL PROYECTO

Formato: *propuesta o situación anterior → corrección del usuario → **decisión vigente**.*

## Estado consolidado al cierre de las primeras láminas (A1–A5, 06-10-2026)

### Alcance y bases
- **Alcance.** El resumen previo (claude.ai/ChatGPT) planteaba alternativas con 6 apartamentos y una conversión futura. → **Vigente:** solo vivienda unifamiliar, sin apartamentos ni notas de conversión. La duda "6 u 8 apartamentos" ya no aplica.
- **Plantas base.** Había varias versiones (E-2.1 de claude.ai y otras). → **Vigente:** se usan como modelo las plantas A-201 y A-202 ajustadas con ChatGPT, más la información del resumen.
- **Patios.** En el resumen previo estaba la idea de reducir P1/P2 a 2.00/2.20 para cumplir el 70 % estricto. → **Vigente:** patios de 2.50, **aceptados por la municipalidad** (altura medida desde el N1).
- **Cobertura.** Claude propuso acortar 0.05 m para no pasar del 70 % con los 256 m² del catastro. → **Vigente:** se deja 70.13 %; el usuario lo acepta.

### Lámina A1
- **Empresa y nota de tapia.** La empresa y la nota 2 de la referencia (tapia) estaban como dudosas. → **Vigente:** la empresa queda en el cajetín y la nota de la tapia se agrega. (Los profesionales de la referencia se autorizaron antes.)
- **Datos del catastro.** Se preguntó por las cotas de 7.00 y 10.67 m y por la segregación. → **Vigente:** se ignoran esas cotas y no se contempla la segregación.

### Lámina A2 (nivel 1)
- **rev0:** 6 estacionamientos (3 + 3 en tándem), bodega y espacio cubierto posterior. → **rev1 vigente:** **solo 3 estacionamientos**; todo lo demás es **jardín seco no construido**; el cuadro de áreas muestra solo estacionamientos, pasillo y gradas.
- **Portón:** el tipo estaba "por definir". → **Vigente:** abatible (4 hojas plegables que abren hacia el retiro).
- **Columnas:** no había. → **Vigente:** sobre el eje C en los ejes 2–6; **sin C1**; el eje C pasa de 4.75 a **4.84**.
- **Lavandería:** Claude la propuso varias veces. → **Vigente:** "no pensar en lavanderías aún".

### Láminas A3 y A4 (niveles 2 y 3)
- **Accesos.** En la A-201/A-202 las puertas de la suite y la sala estaban **en el muro de colindancia**. → **Vigente:** al final del pasillo (ejes 2 y 5).
- **Escalera.** En la A-201 era recta y estaba rotulada "existente". → **Vigente:** escalera **en U**, nueva, de 17 contrahuellas.
- **Baños.** Antes se habló de agrandarlos y, en la sesión previa, de achicarlos. → **Vigente:** 1.55 × 2.20 con piezas en línea y puerta de 0.80 hacia el dormitorio.
- **Baño de la suite 2.** En la A-202 estaba junto a P1. → **Vigente:** **sobre la zona húmeda de la cocina** (lado P2); aprobado. Su ducto se define en las láminas sanitarias.
- **Altura de piso a piso:** era provisional. → **Vigente:** **3.00 m confirmada**.

### Lámina A5 (fachadas) — en revisión
- **Ventanas frontales.** → Por indicación del usuario: **de piso a 2.20**, alineadas, con vidrio arenado en los baños.
- **Ventanas posteriores.** Claude las copió de cada planta y quedaron desalineadas entre N2 y N3. Además, la ventana del baño de la suite 3 **choca con C6**. → Resuelto el 06-10-2026 (ver el registro). **No repetir:** comprobar las columnas antes de ubicar ventanas en fachada.

### Lecciones de proceso (para no repetir errores)
- "Render" se refería a generar el PDF; el usuario aclaró que **no se hacen renders 3D**.
- El MTEXT con varios párrafos se unía en el PDF. → Las notas se escriben con `cl.notes_block`, una nota por texto.
- Las primeras ubicaciones de puertas no se cruzaron con los linderos. → **Verificar** que ninguna puerta ni ventana quede en un muro de colindancia ni choque con una columna.

## Registro de cambios posteriores
*(Agregar aquí, con fecha, cada cambio relevante que apruebe el usuario.)*

- **06-10-2026 — Criterio del índice de láminas.** Al crear la memoria se había propuesto una lista de 38 láminas basada en la referencia. → **El usuario indicó** que la referencia no define el número de láminas. → **Vigente:** índice en tres partes (A desarrolladas, B previstas, C referencia por evaluar); el número definitivo queda pendiente.
- **06-10-2026 — Estados de las láminas.** A1 y A4 figuraban como APROBADAS. → Por indicación del usuario ("ante duda, EN REVISIÓN") → **Vigente:** A1 EN REVISIÓN (falta confirmar la rev1) y A4 EN REVISIÓN (conflicto con C6).
- **06-10-2026 — Decisiones de fachada, techo y linderos** (respuesta del usuario a las decisiones pendientes de la A5).
  - **Ventanas posteriores:** las de rev0 estaban desalineadas y una chocaba con C6. → **Vigente:** patrón 0.70–2.90 / 3.85–4.60 / 6.40–8.20 en N2 y N3, con antepecho común de 0.90.
  - **Protección de las ventanas desde el piso:** había dos opciones. → **Vigente:** opción a (paño fijo inferior hasta 0.90), **sin mencionar el vidrio de seguridad** en los planos. Walk-in con vidrios fijos.
  - **Techo:** se había supuesto losa o lámina con pretil a +9.60. → **Vigente:** lámina estructural cal. 26, a dos aguas (frente y fondo), al 13 %, con canoas, 2 bajantes por lado y conducción a la cuneta del frente. Sin pretil y sin restricción de altura.
  - **Portón:** 2.40 PD → **2.40 confirmado.**
  - **Tapias:** había tapias laterales en el retiro posterior (A2 rev1) y en la A5 aparecían "por confirmar". → **Vigente:** **no hay tapias laterales**; las paredes de la vivienda son la división en el lindero y en el N1 el muro llega hasta el entrepiso.
  - **A1:** EN REVISIÓN → **APROBADA.**
  - **Láminas afectadas:** A2 (aprobada) → rev2; A3 (aprobada) → rev1; A4 → rev1; A5 → rev1. Todas quedan EN REVISIÓN.
  - **Corrección menor de presentación:** la marca de corte A del fondo tapaba la cota 3.43 en A2–A4 y se movió.
- **06-10-2026 — Ventanas de ventilación y tapia posterior.**
  - **Walk-in:** "vidrios fijos" (rev1) → **Vigente:** todas las ventanas ventilan. Solo son fijos los paños inferiores de seguridad del frente; arriba van **ventilas abatibles hacia afuera** (alero cuando llueve). Donde interfiera un pasillo, corrediza móvil-móvil.
  - **Fachada posterior:** totalmente operable.
  - **Tapia posterior:** confirmada, hasta la viga corona del último nivel (+9.00); flecha y nota en las fachadas.
  - **Supuestos de la A5 rev1 confirmados:** 2 bajantes por canoa, ocultos en el N1 al frente; cumbrera al centro; antepecho de 0.90 en el baño de la suite 3; remate sin pretil. Canoas hacia los patios donde se requiera.
  - **Láminas afectadas:** A3 → rev2 y A4 → rev2 (solo notas); A5 → rev2.
- **06-10-2026 — Símbolo de ventila y aprobaciones.**
  - **Símbolo de ventila:** Claude lo dibujó con el vértice arriba (rev2). → **Vigente:** con la bisagra arriba el triángulo va **invertido** (A5 rev3). **No repetir** en cortes ni en los cuadros de ventanas.
  - **Galería del pasillo hacia P1:** se mantiene en vidrio fijo.
  - **Aprobadas:** A2 rev2, A3 rev2 y A4 rev2.
- **06-10-2026 — A6 sistema constructivo.**
  - Cubierta: de línea simple → **cerchas metálicas con clavadores**.
  - Columnas: dibujadas solo en el N1 (parecían desfasadas) → **continuas N1–N3**.
  - Muros: sin material → **mampostería** (linderos, tapia, frente N1) y **forro Steel Tech**.
  - Nivel 1: "contrapiso según estructural" → **contrapiso solo en estacionamientos, pasillo y gradas; grava en el resto**.
  - Cielos: gypsum en N2/N3; acero expuesto en el N1.
  - Láminas aprobadas: **no se modifican** (indicación del usuario).
- **06-10-2026 — A6 rev2.**
  - Viga de entrepiso "0.30" → **0.30 es el paquete total** (viga 0.20 + sobrelosa 0.10); el cielo sigue a 2.70.
  - Retiro frontal: grava → **zacate block (permeable)**.
  - Paredes interiores: sin definir → **Steel Tech 0.12**.
  - Cercha en el A-A: interrumpida en patios y gradas → **completa (cercha del fondo en vista)**.
  - Frente N1: el corte pasa por el portón; ahora se dibuja la hoja cortada y la línea del lindero frontal.
- **06-10-2026 — A6 aprobada; cambios de distribución por la A7.**
  - **Acceso principal:** no había puerta principal → **vestíbulo de escalera cerrado en el N1 con P-01 de madera** (paredes Steel Tech 0.12).
  - **Nivel 2:** se quitan las puertas de la cocina y de la sala y el muro de la cocina hacia el pasillo. La sala se abre 1.20 hacia el pasillo.
  - **Puertas, ventanas y acabados:** previstos en A7–A9 → **una sola lámina A7**.
  - **Láminas aprobadas afectadas:** A2, A3 y A6 (geometría); A4, A5 y A6 (referencia a "A7–A9").
- **06-10-2026 — A11 aprobada.** Gradas con PI-A antideslizante con nariz. Sin citas normativas en los planos; marcas comerciales reemplazadas por "o similar". La A7 queda como está: PI-B todavía menciona las gradas del N1; el usuario decidió no revisarla.
- **06-10-2026 — C03 aprobada; entrepisos en una sola lámina.**
  - Entrepisos: C03 (nivel 2) y C04 (nivel 3) → **una sola C03, "PLANTA DE ENTREPISO 1 Y 2"** (entrepiso 1 = nivel 2; entrepiso 2 = nivel 3; armado idéntico). Solo cambia la leyenda (C03 rev1).
  - Numeración (usuario): **C04 techo, C05–C06 pórticos, C07 especificaciones**. Las referencias "C08" de C01–C03 se corrigen al terminar los estructurales.
- **06-10-2026 — C04 aprobada (opción a).** Niveles de la lámina: +9,00 alero / +10,50 cumbrera → **+9,20 / +10,70**, por el peralte de la cercha y el clavador. **Láminas aprobadas afectadas: A5 y A6** (se corrigen al terminar los estructurales).
- **06-10-2026 — Pórticos (C05 rev1).**
  - C05 + C06 → una sola **C05**; C2 y A1 eliminados.
  - **"Sin columna en el eje C del eje 1" → columna C1 en N2–N3 sobre la viga de transferencia VT-1 (diseño especial); sigue sin columna en el N1.**
  - **Láminas aprobadas afectadas:** C03, C04, A3 y A4 (corregir); A5 y A7 (revisar). Se corrigen al terminar los estructurales.
- **06-10-2026 — C05 aprobada.** Especificaciones: C07 → **C06** (usuario). Las referencias "C08"/"C07" de C01–C05 se corrigen al final.
- **06-10-2026 — Correcciones sobre láminas aprobadas (pedidas por el usuario).**
  - Referencias a especificaciones: "C08"/"C07" → **C06** (C01–C05).
  - Cubierta: +9,00/+10,50 → **+9,20 alero / +10,70 cumbrera** (A5 rev6, A6 rev4).
  - C1 del eje C en el eje 1 (N2–N3, sobre VT-1): C03 rev2, C04 rev1, A3 rev4, A4 rev4.
  - **V-03: 1,00 → 0,90** (x 3,76–4,66) en A3, A4, A5 y A7 rev2.
  - C06 rev1: notas de materiales 8 y 9 eliminadas.
- **06-10-2026 — E04 aprobada.** El usuario agrega la **E05 (detalles eléctricos)**: el juego eléctrico pasa de E01–E04 a E01–E05.

- **07-10-2026 — S02 aprobada; S01 rev1.** El punto de jardín posterior de la S01 (x 4.75, y 25.90) interfería con el tanque séptico de la S02 → **se traslada a (x 1.50, y 25.40)**. Lámina aprobada afectada: **S01 → rev1**.
- **07-10-2026 — S01 rev1 y S03 aprobadas; corrección de referencias.** Referencias genéricas ("planos estructurales", "lámina pluvial", "láminas sanitarias/IS", "por diseñar") → láminas vigentes C01–C06, S01–S03, E02–E03. A3 rev5 dibuja los ductos sanitarios aprobados en la S02. C04 rev2 elimina la nota de niveles pendientes. Nuevas revisiones: A1 rev2, A2 rev4, A3 rev5, A4 rev5, A5 rev7, A6 rev5, A7 rev3, C04 rev2. **Sin cambio:** A11 (la estructura de la escalera no está en ninguna lámina C; pendiente).
- **07-10-2026 — Corrección de referencias aprobada.** La A11 se mantiene sin cambio (decisión del usuario).
