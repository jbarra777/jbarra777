# ESTADO DEL PROYECTO — dónde estamos y qué sigue

*Actualizado: 06-10-2026.*

## Resumen
- **Proyecto:** vivienda unifamiliar de 3 niveles en un lote de 9.00 × 28.5 m (256 m²) en San Rafael de Heredia.
  - Nivel 1: 3 estacionamientos y jardín seco.
  - Nivel 2: suite, cocina-comedor y sala familiar.
  - Nivel 3: tres suites.
- **Etapa:** juego de planos para el CFIA, en la parte de arquitectura.
- **Avance:** 5 láminas desarrolladas, A1 a A5. El número total de láminas está **PENDIENTE DE DEFINIR**; la referencia no lo define (ver `INDICE_PLANOS.md`).

## Situación actual
| Lámina | Estado | Motivo |
|---|---|---|
| A1 | APROBADA | rev1, "A1 aprobada" |
| A2 | APROBADA | rev3 |
| A3 | APROBADA | rev3 |
| A4 | EN REVISIÓN | rev3: referencia a la A7 |
| A5 | APROBADA | rev3 |
| A6 | APROBADA | rev2 (falta rev3: vestíbulo N1, vano de la sala y referencia A7) |
| A7 | APROBADA | rev1 |

- **Última entrega:** A4 rev3.
- **Siguiente paso:** visto bueno de la A4 rev3. Después entregar, una a la vez, A5 rev4 (referencia A7 y V-05 de la sala con vidrio arenado) y A6 rev3 (vestíbulo N1, vano de la sala y referencia A7).

## Decisiones que necesitan respuesta del usuario
- Ninguna abierta para A1–A5 (fuera del visto bueno de la A5 rev3).

## Otros pendientes
- **Lista y número definitivo de láminas.** Evaluar las combinaciones y si las aguas pluviales llevan lámina propia.
- **Notas [PR]** 1 (medidas) y 7 (canoas con malla): esperan la revisión del usuario. Ya hay canoas confirmadas.
- **Estructura:** sistema estructural, cimentación, entrepisos, secciones (las columnas de 0.30 son PD) y la viga del eje 1 sin C1.
- **Sanitarios:** tanque séptico (prueba de infiltración), ductos de las suites 2 y 3 y modelo del extractor.
- **Eléctricos:** sin datos todavía.
- **Acabados.**
- **Relación de la A1 rev1** (solo existe la rev0): pendiente de redactar.
- **Confirmaciones municipales:** retiros con alineamiento y uso de suelo; normativa vigente no verificada.
- **Lavandería:** pospuesta.
- **Privacidad del repositorio:** `jbarra777/jbarra777` es **público** y contiene el folio real, las coordenadas y los profesionales. Sin respuesta del usuario.

## ARCHIVOS FUENTE CRÍTICOS
**Almacenamiento temporal:** carpeta de cargas de la sesión inicial (`/root/.claude/uploads/86a7047e-…/`) y su copia de trabajo (`/tmp/claude-0/…/scratchpad/`, `/tmp/claude-0/…/images/`). **Se pierde al cerrar o reiniciar el contenedor.**

**Regla:** no copiar, subir ni publicar estos archivos sin la autorización del usuario.

### 1. Plantas A-201 (nivel 2) y A-202 (nivel 3), vivienda unifamiliar
- **Archivo:** `SanRafael_Propuesta_2_Vivienda_Unifamiliar.pdf` (2 páginas A2).
- **Pertenece a:** proyecto actual.
- **Función:** plantas base del diseño. Definieron la envolvente (9.00 × 23.12), los módulos, los patios y la organización de las suites.
- **Ubicación:** solo en almacenamiento temporal; no está en el repositorio.
- **Riesgo si se pierde:** medio. La geometría ya está en `datos/proyecto.json`, en los scripts y en las láminas A2–A4. No se podría volver a cotejar el original.

### 2. Planta A-200 de apartamentos
- **Archivo:** `SanRafael_Propuesta_2_Apartamentos.pdf`.
- **Pertenece a:** antecedente del proyecto actual. El alcance vigente ya no incluye apartamentos.
- **Función:** solo consulta.
- **Ubicación:** solo en almacenamiento temporal.
- **Riesgo si se pierde:** bajo.

### 3. Proyecto de referencia RIVERGRAND (37 PDF A1)
- **Archivo:** `Planos_Completos_27_agosto.zip` (12.7 MB).
- **Pertenece a:** **solo referencia**: alcance, contenido y presentación.
- **Función:** ver qué debe contener cada tipo de lámina.
- **Ubicación:** solo en almacenamiento temporal (el ZIP y una copia descomprimida).
- **Riesgo si se pierde:** **alto para las láminas que faltan** (A6–A11, estructural, eléctrica, sanitaria). Sin él no se puede revisar el alcance de cada lámina de referencia. Para lo ya hecho, ninguno.

### 4. Comprobante del plano catastrado 4-57389-2023
- **Archivo:** imagen JPG adjunta en el chat (`images/1.jpg`).
- **Pertenece a:** proyecto actual.
- **Función:** datos del lote (vértices, área, folio, amarre) e imagen de ubicación.
- **Ubicación:** el original solo está en almacenamiento temporal. **En el repositorio están** los datos (`datos/lote_catastro.json`) y el recorte de ubicación (`planos/A1_lote/A1_ubicacion_catastro.png`).
- **Riesgo si se pierde:** bajo. Los datos necesarios ya están en el repositorio. Se perdería el original para cotejar.

### 5. Resumen de la sesión anterior (claude.ai)
- **Archivo:** `CLAUDE.pdf` (10 páginas).
- **Pertenece a:** proyecto actual, como histórico.
- **Función:** decisiones previas (retiros, muros, cobertura, criterios) y normativa consultada.
- **Ubicación:** solo en almacenamiento temporal.
- **Riesgo si se pierde:** bajo a medio. Sus decisiones vigentes están en `DECISIONES_TECNICAS.md`. Se perderían las citas de normativa (Reglamento de Construcciones 1983, capítulo VI), que de todos modos no están verificadas contra la versión vigente.

### 6. Archivos persistentes en el repositorio (no requieren acción)
- `datos/lote_catastro.json`, `datos/proyecto.json`.
- `scripts/` (generadores de todas las láminas).
- `planos/` (DXF, PDF y relaciones).
- Archivos de memoria (`*.md`).

**Conclusión:** antes de compactar, lo crítico es el **ZIP de referencia (3)**. Conviene conservar también las **plantas A-201/A-202 (1)** y el **resumen `CLAUDE.pdf` (5)**. Para preservarlos hay dos opciones, ambas a decidir por el usuario:
- el usuario guarda una copia local para volver a subirla en la próxima sesión;
- se suben a una carpeta del repositorio, solo si este pasa a ser privado.

Hacer `/compact` dentro de esta misma sesión **no borra** estos archivos temporales. Sí se pierden si el contenedor se reinicia o se abre una sesión nueva.

## Notas para una sesión nueva
- Leer `CLAUDE.md` y luego este archivo.
- Si el usuario dice "continuar" sin más contexto, reanudar en "Decisiones que necesitan respuesta".
- La sesión es un contenedor temporal: todo lo importante debe quedar con commit y push en la rama.
