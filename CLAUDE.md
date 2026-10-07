# CLAUDE.md — Instrucciones permanentes del proyecto

## IDENTIFICACIÓN DEL PROYECTO
Juego de planos constructivos de una **vivienda unifamiliar de tres niveles** en Santiago, San Rafael de Heredia, Costa Rica.
El usuario es el ingeniero civil a cargo: dirige, revisa y aprueba. Idioma de trabajo: español.

## OBJETIVO
Desarrollar el juego completo de planos constructivos para trámite ante el CFIA y la municipalidad, a partir de las plantas y decisiones aprobadas del proyecto actual.
- El alcance es **exclusivamente una vivienda unifamiliar**: no se dibujan apartamentos ni notas de conversión.
- Cada lámina se entrega como DXF editable (AutoCAD 2018), un PDF de revisión en A1 y una relación breve de contenido, ajustes y pendientes.

## ARCHIVOS DE MEMORIA (leer antes de trabajar)
| Archivo | Uso |
|---|---|
| `ESTADO_PROYECTO.md` | Dónde estamos y qué toca hacer ahora. **Leer primero.** |
| `DECISIONES_TECNICAS.md` | Qué está decidido técnicamente: dimensiones, niveles, criterios. |
| `INDICE_PLANOS.md` | Lista maestra de láminas y su estado. |
| `CAMBIOS_PROYECTO.md` | Decisiones que cambiaron y cuál está vigente (evita repetir errores). |
| `CONTEXTO_PROYECTO.md` | Histórico, reemplazado por los cuatro anteriores. Consultar solo si hace falta. |

## REGLAS FUNDAMENTALES
1. Trabajar **una lámina a la vez**. No avanzar a la siguiente sin la indicación expresa del usuario (por ejemplo, "continuar con la siguiente").
2. Nunca modificar una decisión aprobada sin autorización. Si una corrección afecta láminas ya aprobadas, avisar e identificar cuáles.
3. **Nunca inventar** dimensiones, especificaciones, datos registrales, profesionales ni normativa. Si falta información crítica, preguntar. Si se puede avanzar con un supuesto, marcarlo como *PENDIENTE DE DEFINIR*, *PD* o *[PR]* y avisar.
4. Una propuesta de Claude **no es una decisión** hasta que el usuario la aprueba.
5. Mantener consistencia total entre láminas: nomenclatura, ejes, escalas, simbología, cajetín y notas.
6. Verificar contra las láminas aprobadas antes de dibujar: cotas, niveles, puertas, ventanas, columnas y núcleos húmedos.
7. **Proyecto de referencia (RIVERGRAND, 37 láminas, otro proyecto en Alajuelita):** úsalo solo para alcance, contenido, organización, nivel de detalle, tablas y presentación. No copies su geometría, áreas, niveles, estructura, instalaciones, cálculos, datos registrales ni profesionales.
   - Excepción autorizada por el usuario: los profesionales y la empresa del cajetín (ver DECISIONES_TECNICAS §1).
   - Las notas tomadas de la referencia llevan **[PR]** hasta que el usuario las revise.
   - La referencia **no define el número ni la lista de láminas**. Cada lámina se justifica por las necesidades de esta vivienda y se puede combinar, eliminar o agregar con el usuario. Ninguna se incorpora solo porque exista en la referencia (ver `INDICE_PLANOS.md`, secciones A/B/C).
8. Normativa: cita solo fuentes verificadas. Si no está verificada, decirlo y no afirmar cumplimiento.
9. No declarar los planos aptos para construcción o trámite mientras haya pendientes. Desde el 07-10-2026, con todo verificado por el usuario, el cajetín indica "PARA TRÁMITE – CFIA Y MUNICIPALIDAD" (DECISIONES §18). Si aparece un pendiente nuevo, avisar antes de mantener ese estado.
10. No hacer renders ni imágenes 3D: solo planos. Generar el PDF a partir del DXF es parte del plano, no un render.
11. Antes de cada respuesta al usuario sobre una lámina, revisar visualmente el PDF por zonas: textos superpuestos, elementos recortados, cotas legibles.

## FUENTES DE VERDAD (prioridad de mayor a menor)
1. Instrucciones y correcciones más recientes del usuario.
2. Información aprobada del proyecto actual: catastro, plantas A-201/A-202 como base y datos que dio el usuario.
3. Láminas APROBADAS, sin correcciones pendientes (ver `INDICE_PLANOS.md`). Una lámina EN REVISIÓN no es fuente de verdad para lo que esté en discusión.
4. `DECISIONES_TECNICAS.md`.
5. `ESTADO_PROYECTO.md`.
6. Archivos fuente del proyecto: `datos/*.json`, `scripts/`.
7. Proyecto de referencia: solo contenido y presentación.

**Contradicciones:** no las resuelvas en silencio. Informa al usuario y registra la decisión en `CAMBIOS_PROYECTO.md`.

## FLUJO DE TRABAJO PARA CADA LÁMINA
**Antes**
- Identificar la lámina en `INDICE_PLANOS.md` (secciones A o B). Si solo aparece en la C (referencia), confirmar primero con el usuario si aplica.
- Revisar la lámina equivalente de la referencia: alcance y componentes.
- Consultar `DECISIONES_TECNICAS.md` y las láminas relacionadas.
- Pedir solo los datos indispensables.

**Durante**
- Usar solo información válida del proyecto actual.
- Verificar la coherencia dimensional y técnica: áreas recalculadas desde la geometría, cotas contra geometría, puertas que abren, mobiliario a escala.

**Después**
- Revisión interna: auditoría del DXF (`ezdxf.recover` + `audit`) y revisión visual del PDF.
- Entregar el PDF, el DXF y la relación (`SR-Ax_relacion_revN.md`) señalando los pendientes.
- Esperar la aprobación del usuario.

**Tras la aprobación**, actualizar:
1. `INDICE_PLANOS.md` (estado).
2. `ESTADO_PROYECTO.md`.
3. `DECISIONES_TECNICAS.md`, con las decisiones nuevas aprobadas o definidas por el usuario.
4. `CAMBIOS_PROYECTO.md`, solo con cambios relevantes.

Después hacer commit y push a la rama de trabajo.

## CONVENCIONES DE ARCHIVOS Y HERRAMIENTAS
- **Rama:** `claude/planos-vivienda-tres-plantas-cdy6qs` (repositorio `jbarra777/jbarra777`; el usuario pidió hacerlo **privado** el 07-10-2026, cambio que hace él en GitHub).
- **Láminas:** `planos/<Código>_<tema>/SR-<Código>_<TEMA>_revN.{dxf,pdf}` más `SR-<Código>_relacion_revN.md`. Para cambiar una lámina se crea la revisión siguiente (revN+1); nunca se sobrescribe una revisión entregada.
- **Generadores:** `scripts/aN_*.py`, más los módulos comunes:
  - `cadlib.py`: capas, cotas, cajetín, notas, PDF;
  - `planta.py`: muros, puertas, mobiliario, marco de planta;
  - `hoja.py`: piezas comunes de las láminas de planta.
- **Datos:** `datos/lote_catastro.json` y `datos/proyecto.json`.
- **Entorno:** `pip install ezdxf pymupdf pillow`. El PDF se genera con ezdxf + PyMuPDF.
  - Los viewports girados no se dibujan, por eso las plantas usan el marco girado de `planta.py`.
  - El MTEXT de varios párrafos puede unirse en el PDF: usar `cl.notes_block`.
  - Una lámina tarda unos minutos en generarse.
- **Archivos de entrada que no están en el repositorio:** PDF de referencia, plantas A-200/A-201/A-202, imagen del catastro y resumen de la sesión anterior (`CLAUDE.pdf`). Estaban en la carpeta de cargas de la sesión inicial. En una sesión nueva hay que pedir al usuario que los vuelva a subir si se necesitan. El detalle y el riesgo de cada uno están en `ESTADO_PROYECTO.md` → ARCHIVOS FUENTE CRÍTICOS. No subirlos ni publicarlos sin autorización.
