# ESTADO DEL PROYECTO — dónde estamos y qué sigue

*Actualizado: 07-10-2026.*

## Resumen
- **Proyecto:** vivienda unifamiliar de 3 niveles en un lote de 9.00 × 28.5 m (256 m²) en San Rafael de Heredia.
- **Etapa:** juego completo de **22 láminas** (lista definitiva, DECISIONES §18), emitido **PARA TRÁMITE** el 07-10-2026.

## Situación actual
| Lámina | Estado | Revisión vigente |
|---|---|---|
| A1 | PARA TRÁMITE (por aprobar) | rev3 |
| A2 | PARA TRÁMITE (por aprobar) | rev5 |
| A3 | PARA TRÁMITE (por aprobar) | rev6 |
| A4 | PARA TRÁMITE (por aprobar) | rev6 |
| A5 | PARA TRÁMITE (por aprobar) | rev8 |
| A6 | PARA TRÁMITE (por aprobar) | rev6 |
| A7 | PARA TRÁMITE (por aprobar) | rev4 |
| A8 | PARA TRÁMITE (por aprobar) | rev2 |
| C01 | PARA TRÁMITE (por aprobar) | rev2 |
| C02 | PARA TRÁMITE (por aprobar) | rev2 |
| C03 | PARA TRÁMITE (por aprobar) | rev3 |
| C04 | PARA TRÁMITE (por aprobar) | rev3 |
| C05 | PARA TRÁMITE (por aprobar) | rev3 |
| C06 | PARA TRÁMITE (por aprobar) | rev2 |
| E01 | PARA TRÁMITE (por aprobar) | rev2 |
| E02 | PARA TRÁMITE (por aprobar) | rev1 |
| E03 | PARA TRÁMITE (por aprobar) | rev1 |
| E04 | PARA TRÁMITE (por aprobar) | rev1 |
| E05 | PARA TRÁMITE (por aprobar) | rev1 |
| S01 | PARA TRÁMITE (por aprobar) | rev2 |
| S02 | PARA TRÁMITE (por aprobar) | rev2 |
| S03 | PARA TRÁMITE (por aprobar) | rev1 |

- **Última entrega:** emisión para trámite de las 22 láminas (lista definitiva, sin [PR] ni PD).
- **Siguiente paso:** aprobación del usuario de la emisión.

## Decisiones que necesitan respuesta del usuario
- Ninguna.

## Otros pendientes
- **Privacidad del repositorio:** el usuario pidió hacerlo privado (07-10-2026). Claude no tiene permiso para cambiar la visibilidad; lo hace el usuario en GitHub (Settings → General → Danger Zone → Change visibility).
- **Lavandería:** pospuesta (sin lámina).

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
