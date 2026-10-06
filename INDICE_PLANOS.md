# ÍNDICE DE PLANOS — Lista maestra

**Base:** la organización del proyecto de referencia (37 láminas: A1–A11, C01–C10, EL1–EL10, IS1–IS6), adaptada a este proyecto.

El usuario estima unas 30 láminas; esta lista propone **38**. **El número final está PENDIENTE DE DEFINIR**: confirmar con el usuario qué láminas se combinan o no aplican. El contenido de las láminas pendientes es tentativo.

**Estados:** APROBADA · EN REVISIÓN · EN DESARROLLO · PENDIENTE · NO APLICA

## Arquitectura
| Código | Nombre | Contenido principal | Estado | Archivo | Observaciones |
|---|---|---|---|---|---|
| A1 | Lote de terreno | Ubicación geográfica (imagen del catastro), poligonal 1:200, retiros y huella 1:100, derrotero, coordenadas CRTM05, áreas y cobertura, notas | APROBADA | `planos/A1_lote/SR-A1_LOTE_rev1.*` | El usuario pidió 3 cambios y luego "continuar con la lámina 2". La rev1 los aplica; no hubo confirmación explícita de la rev1. No existe relación rev1, solo la rev0. |
| A2 | Planta nivel 1 | Parqueos E-1 a E-3, pasillo, gradas, jardín seco, columnas eje C, portón abatible, derrotero, áreas y cobertura, notas | APROBADA | `planos/A2_nivel1/SR-A2_NIVEL1_rev1.*` | Aprobada: "De acuerdo, continuar con la siguiente". |
| A3 | Planta nivel 2 | Suite 1, cocina-comedor, sala familiar, áreas, cobertura, detalle del extractor, notas | APROBADA | `planos/A3_nivel2/SR-A3_NIVEL2_rev0.*` | "Está perfecto". Puede necesitar una revisión si se realinean las ventanas posteriores (sala). |
| A4 | Planta nivel 3 | Suites 1, 2 y 3, áreas, cobertura, detalle del extractor, notas | APROBADA | `planos/A4_nivel3/SR-A4_NIVEL3_rev0.*` | Aprobada ("ok baño de suite 2…"). **Requiere corrección:** la ventana posterior del baño de la suite 3 choca con la columna C6. |
| A5 | Fachadas | Principal 1:50, posterior 1:75, laterales 1:100, notas | EN REVISIÓN | `planos/A5_fachadas/SR-A5_FACHADAS_rev0.*` | Pendientes: ventanas posteriores, conflicto con C6 y supuestos PD (ver ESTADO). |
| A6 | Cortes | Corte A-A (longitudinal, x = 3.0) y B-B (transversal, y = 18.25), ya referenciados en las plantas | PENDIENTE | — | Depende de la cubierta, el pretil y el sistema de entrepiso. |
| A7 | Nivel 1: puertas, ventanas y acabados | Planta con códigos, cuadro de puertas y ventanas, acabados de pisos y paredes | PENDIENTE | — | |
| A8 | Nivel 2: puertas, ventanas y acabados | Ídem | PENDIENTE | — | La A3 remite a la A8. |
| A9 | Nivel 3: puertas, ventanas y acabados | Ídem | PENDIENTE | — | La A4 remite a la A9. |
| A10 | Acabados de fachadas | Fachadas con materiales y acabados | PENDIENTE | — | La A5 remite a la A10. |
| A11 | Escalera y detalles | Planta, corte, barandas y pasamanos | PENDIENTE | — | Las plantas remiten a la A11 para las barandas. |

## Civil / estructural (contenido según el sistema estructural, PENDIENTE DE DEFINIR)
| Código | Nombre | Contenido principal | Estado | Archivo | Observaciones |
|---|---|---|---|---|---|
| C01 | Planta de fundaciones | Placas, cimientos y ejes | PENDIENTE | — | Requiere el criterio estructural del usuario. |
| C02 | Detalles de fundaciones | Secciones y refuerzo | PENDIENTE | — | |
| C03 | Losa de piso nivel 1 | Contrapiso de estacionamientos, pasillo y gradas | PENDIENTE | — | En la referencia era "entrepiso PB"; confirmar si aplica. |
| C04 | Entrepiso nivel 2 | Planta estructural y detalle | PENDIENTE | — | Incluye la viga del eje 1 (sin C1). |
| C05 | Entrepiso nivel 3 | Planta estructural y detalle | PENDIENTE | — | |
| C06 | Planta de techos | Cubierta y pendientes | PENDIENTE | — | Falta definir el tipo de techo. |
| C07 | Detalles de techo y caja pluvial | Secciones y caja pluvial | PENDIENTE | — | |
| C08 | Pórticos longitudinales | Ejes A–D | PENDIENTE | — | |
| C09 | Pórticos transversales | Ejes 1–6 | PENDIENTE | — | |
| C10 | Especificaciones constructivas | Materiales y notas técnicas | PENDIENTE | — | No copiar las de la referencia sin aprobación. |

## Eléctrica
| Código | Nombre | Contenido principal | Estado | Archivo | Observaciones |
|---|---|---|---|---|---|
| EL1 | Iluminación nivel 1 | Salidas, apagadores, circuitos | PENDIENTE | — | Por confirmar si se combina con EL4 (el N1 es reducido). |
| EL2 | Iluminación nivel 2 | Ídem | PENDIENTE | — | |
| EL3 | Iluminación nivel 3 | Ídem | PENDIENTE | — | |
| EL4 | Tomacorrientes nivel 1 | Tomas y circuitos | PENDIENTE | — | |
| EL5 | Tomacorrientes nivel 2 | Ídem | PENDIENTE | — | |
| EL6 | Tomacorrientes nivel 3 | Ídem | PENDIENTE | — | |
| EL7 | Detalles constructivos eléctricos | Acometida, medidor, puesta a tierra | PENDIENTE | — | |
| EL8 | Voz y datos, simbología, notas | Diagrama y simbología | PENDIENTE | — | |
| EL9 | Diagrama unifilar | | PENDIENTE | — | Requiere cargas y criterios del profesional eléctrico. |
| EL10 | Tableros | Cuadros de cargas | PENDIENTE | — | |

## Sanitaria
| Código | Nombre | Contenido principal | Estado | Archivo | Observaciones |
|---|---|---|---|---|---|
| IS1 | Agua potable nivel 1 | Acometida ESPH y montantes | PENDIENTE | — | |
| IS2 | Agua potable nivel 2 | | PENDIENTE | — | |
| IS3 | Agua potable nivel 3 | | PENDIENTE | — | |
| IS4 | Aguas residuales nivel 1 | Cajas de registro, tanque séptico y drenaje | PENDIENTE | — | Falta la prueba de infiltración. |
| IS5 | Aguas residuales nivel 2 | Ductos, incluido el de la suite 3 | PENDIENTE | — | |
| IS6 | Aguas residuales nivel 3 | Baños de las suites 1, 2 y 3 | PENDIENTE | — | |
| IS7 | Aguas pluviales | Bajantes y conducción a la cuneta | PENDIENTE | — | **Lámina agregada**: la referencia no la tenía. Confirmar con el usuario. |
