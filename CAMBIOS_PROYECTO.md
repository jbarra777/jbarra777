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
