# ESTADO DEL PROYECTO — dónde estamos y qué sigue

*Actualizado: 06-10-2026.*

## Resumen
- **Proyecto:** vivienda unifamiliar de 3 niveles en un lote de 9.00 × 28.5 m (256 m²) en San Rafael de Heredia.
  - Nivel 1: 3 estacionamientos y jardín seco.
  - Nivel 2: suite, cocina-comedor y sala familiar.
  - Nivel 3: tres suites.
- **Etapa:** juego de planos para el CFIA, en la parte de arquitectura.
- **Avance:** 5 láminas desarrolladas, A1 a A5 (ver `INDICE_PLANOS.md`).

## Situación actual
- **Última lámina trabajada:** A5 Fachadas rev0, **EN REVISIÓN**.
- **Última lámina aprobada:** A4 Planta nivel 3 rev0, con una corrección pendiente (punto 1 abajo).
- **Siguiente paso:** **no empezar la A6 todavía.** Primero hay que cerrar la A5 con las decisiones del usuario sobre los puntos de abajo y generar las revisiones necesarias (A5 rev1, A4 rev1 y posiblemente A3 rev1).
- **Lámina siguiente después de la A5:** A6 Cortes.

## Decisiones que necesitan respuesta del usuario (bloquean el cierre de la A5)
1. **Conflicto detectado:** la ventana posterior del baño de la suite 3 (N3, x 3.95–4.95) choca con la columna C6 (x 4.69–4.99). Afecta a la A4 y la A5.
2. **Ventanas posteriores no alineadas entre el N2 (sala) y el N3 (suite 3).** Claude propuso un patrón común, **aún no aprobado**:
   - 0.70–2.90;
   - una ventana angosta de unos 3.85–4.60 que libra C6;
   - 6.40–8.20.

   Falta decidir si van de piso a 2.20 o con un antepecho común. Puede afectar a la A3 (sala), la A4 y la A5.
3. **Protección de las ventanas desde el piso** en N2/N3: paño fijo laminado de 0.90 o baranda interior. También falta el tipo de vidrio de seguridad y el tratamiento del walk-in.
4. **Techo:** losa plana o lámina con pretil. Niveles de cubierta (+9.00) y pretil (+9.60) están como PD, y la altura máxima municipal no está verificada.
5. **Altura del portón y de la puerta peatonal:** 2.40 está como PD.
6. **Altura de las tapias** en los retiros.

## Otros pendientes (no bloquean la A5)
- **Total de láminas del juego.** La propuesta es de 38; el usuario estima unas 30. También falta confirmar la IS7 de aguas pluviales.
- **Notas [PR]** 1 (medidas) y 7 (canoas): esperan la revisión del usuario.
- **Sistema estructural:** cimentación, entrepisos, secciones (las columnas de 0.30 son PD) y la viga del eje 1 sin C1.
- **Sanitarios:** dimensionamiento del tanque séptico y prueba de infiltración; ductos de las suites 2 y 3; modelo del extractor.
- **Eléctricos:** sin datos todavía.
- **Acabados** de pisos, paredes y fachadas.
- **Confirmaciones municipales:** retiros con alineamiento y uso de suelo; normativa vigente (Reglamento de Construcciones del INVU y plan regulador) no verificada.
- **Lavandería:** pospuesta por el usuario.

## Riesgos de continuidad que debe conocer una sesión nueva
- **Repositorio público.** `jbarra777/jbarra777` contiene el folio real, las coordenadas y los nombres de los profesionales. El usuario no ha respondido si quiere hacerlo privado.
- **Archivos fuente fuera del repositorio:**
  - PDF de referencia (ZIP "Planos Completos 27 agosto", 37 láminas);
  - plantas A-200, A-201 y A-202;
  - imagen del catastro;
  - resumen previo `CLAUDE.pdf`.

  Solo estaban en la carpeta temporal de cargas. **Están en el repositorio:** los datos del catastro (`datos/lote_catastro.json`) y el recorte de ubicación (`planos/A1_lote/A1_ubicacion_catastro.png`). Para revisar de nuevo la referencia o las plantas base, pedir al usuario que las vuelva a subir.
- **La sesión de trabajo** es un contenedor temporal: todo lo que importe debe quedar con commit y push en la rama.
- **Si el usuario pide "continuar"** sin más contexto: reanudar en "Decisiones que necesitan respuesta" (arriba).
