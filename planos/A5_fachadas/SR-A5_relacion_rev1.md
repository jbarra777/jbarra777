# Lámina A5 · FACHADAS · rev1 (versión de trabajo)

**Estado:** versión de trabajo para revisión. No apta para construcción ni trámite.

## Archivos
| Archivo | Uso |
|---|---|
| `SR-A5_FACHADAS_rev1.pdf` | Plano para revisar (A1 al 100 %) |
| `SR-A5_FACHADAS_rev1.dxf` | Editable AutoCAD 2018, layout `A5-FACHADAS` |

## Cambios respecto a rev0 (sus indicaciones del 06-10-2026)
| Indicación | Aplicado |
|---|---|
| Patrón de ventanas posteriores y antepecho común | N2 y N3: **0.70–2.90 / 3.85–4.60 / 6.40–8.20**, todas con antepecho de 0.90 y dintel a 2.20. La ventana angosta libra C6. Baño de la suite 3 con vidrio arenado. Cotas horizontales agregadas. |
| Ventanas desde el piso: opción a | Frente: travesaño a 0.90 en todas las ventanas desde el piso, **incluido el baño** (paño fijo inferior). No se menciona el vidrio de seguridad: se quitaron "templado o laminado" y "verificar normativa". |
| Walk-in con vidrios fijos | Rótulo "VIDRIO FIJO" en las ventanas de los walk-in del frente (N2 y N3) y de la suite 3 (fondo). Nota 8. |
| Techo | **Lámina estructural cal. 26 a dos aguas** (frente y fondo), **pendiente 13 %**. Arranque en la viga corona +9.00. **Cumbrera +10.50**: 9.00 + 0.13 × 11.56. Se eliminó el pretil. Canoa frontal y posterior. |
| Aguas pluviales | 2 bajantes por canoa (4 en total), uno en cada extremo, conducidos hacia la cuneta del frente (nota 6). |
| Altura sin restricción | Se quitaron las referencias a la altura máxima municipal. |
| Portón y puerta peatonal 2.40 | Confirmados; se quitó "preliminar". |
| Sin tapias laterales; los muros son la división | En las fachadas laterales se quitaron las tapias de los retiros (rótulo "RETIRO (SIN TAPIA)"). El muro de colindancia sube desde el N1 con el remate según la pendiente de la cubierta (hastial). Nota 11. |

## Supuestos que tomé y necesitan su visto bueno
1. **"2 bajantes a cada lado"** lo interpreté como 2 en la canoa frontal y 2 en la posterior, uno en cada extremo. ¿Es así?
2. **Cumbrera al centro de la envolvente** (y = 13.62), con faldones iguales de 11.56 m.
3. **Antepecho común de 0.90 también en el baño de la suite 3.** Es la ventana angosta, con vidrio arenado. Queda sobre la ducha, así que se mantiene la nota 9 (vidrio sellado y antepecho impermeable).
4. **Remate de los muros de colindancia:** siguen la pendiente del techo, sin pretil por encima de la cubierta.
5. **Canoa y bajantes con representación esquemática**, sin dimensiones. Se definen en la lámina pluvial.

## Pendientes detectados
1. **Bajantes frontales en el N1.** En el frente, un bajante en cada extremo choca en el N1 con el portón (bisagra en el eje D) y con el acceso peatonal (eje A). Por eso el tramo del N1 se dibujó oculto (punteado). Hay que decidir si va empotrado en el muro o en la columna, o si se desplaza (por ejemplo, a la pilastra del eje B).
2. **Patios P1 y P2.** El techo tiene bordes abiertos hacia los patios y el agua de esos bordes cae a ellos. Hay que definir canoas internas y su conducción. No está en sus indicaciones; lo veremos en la lámina de techos o la pluvial.
3. **Bajantes posteriores:** necesitan tubería bajo el N1 hasta la cuneta del frente. Va en la lámina pluvial.

## Validación
- DXF revisado con `recover` y `audit`.
- PDF revisado visualmente.
- No se probó en AutoCAD.
