# Lámina E05 · DETALLES ELÉCTRICOS · rev0 (versión de trabajo)

**Estado:** versión de trabajo para revisión. No apta para construcción ni trámite. Lámina agregada a pedido del usuario.

## Archivos
| Archivo | Uso |
|---|---|
| `SR-E05_DETALLES_rev0.pdf` | Plano para revisar (A1 al 100 %) |
| `SR-E05_DETALLES_rev0.dxf` | Editable AutoCAD 2018, layout `E05-DETALLES` |

Generador: `scripts/e05_detalles.py` (simbología común `elec.py`).

## Contenido (dibujos esquemáticos, sin escala)
1. **Alturas de montaje:** tomas a 0,30 y 1,50 m, apagador a 1,30 m y medidor a 1,90 m, según la simbología de E01–E04 [PR].
2. **Conexión de apagador** (fase, retorno y tierra; caja rectangular; tubería y conector) [PR].
3. **Conexión de tomacorriente** (fase, neutro y tierra) [PR].
4. **Caja octogonal de paso:** conexión de luminaria con cola 3 × 14 AWG [PR].
5. **Ubicación de accesorios en pared:** borde de pared, mocheta menor a 40 cm y apagadores en caja de varios gangs [PR].
6. **Previstas para TV en pared:** caja cuadrada con aro de 1 gang; tuberías de 13, 19 y 25 mm [PR].
7. **Zanja de acometida subterránea:** eléctrica a 0,50 m mínimo sobre 5 cm de lastre y con 10 cm de arena; voz y datos a 0,25 m; separación mínima de 15 cm (notas de la E04) [PR].
8. **Puesta a tierra:** dos electrodos a 3 m, cable #6 desnudo, profundidad ≥ 3,05 m, resistencia ≤ 25 Ω (unifilar de la E04) [PR].

## Diferencias con la referencia (EL07)
- **Detalle de cableado estructurado:** no se incluyó, porque solo describe productos de una marca comercial. La conexión de voz y datos queda en el diagrama de la E04.
- **Detalles de caja cuadrada y de tomacorrientes en circuito:** se integraron a los detalles 3 y 6.
- **Detalles nuevos:** se agregaron los 1, 7 y 8, con datos ya aprobados en la E04.

## Validación
- DXF revisado con `recover` y `audit`: 0 errores.
- PDF revisado visualmente por zonas.
- No se probó en AutoCAD.
