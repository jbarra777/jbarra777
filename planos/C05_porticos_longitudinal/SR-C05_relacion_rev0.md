# Lámina C05 · PÓRTICOS EJE LONGITUDINAL · rev0 (versión de trabajo)

**Estado:** versión de trabajo para revisión. No apta para construcción ni trámite.

## Archivos
| Archivo | Uso |
|---|---|
| `SR-C05_PORTICOS_LONGITUDINAL_rev0.pdf` | Plano para revisar (A1 al 100 %) |
| `SR-C05_PORTICOS_LONGITUDINAL_rev0.dxf` | Editable AutoCAD 2018, layout `C05-PORTICOS` |

Generador: `scripts/c05_porticos.py` (`L` = C05, `T` = C06).

## Criterio
- **Presentación:** la de la referencia (RIVERGRAND C08/C09), con elevaciones esquemáticas a 1:75 [PR].
- **Geometría:** la de las láminas C01–C04 aprobadas:
  - C1 continuas desde la placa hasta la corona (+9,00);
  - V1 de entrepiso con la cara superior a 0,10 bajo el NPT (paquete de 0,30);
  - V1 de corona a +9,00;
  - VA1 de 0,20 × 0,40;
  - placas F1/F2 con pedestal de 0,80.

## Contenido
- **Pórticos A y D** (colindancias): C1 en los ejes 1 a 6; V1 en todos los vanos de N2, N3 y corona; VA1 continua; placas F2.
- **Pórtico C:** C1 en los ejes 2 a 6.
  - Sin columna en el eje 1: la V1 de 1–2 apoya en la V1 del eje 1.
  - Sin vigas en el vano 2–3 (patio P1); la cercha CE-1 continúa (C04).
  - VA1 de 2 a 6; placas F1.
- Ejes con cotas, niveles N1–N3 y corona, cota de cimentación (1,05), simbología y notas 1 a 7.

## Pendientes y puntos a confirmar
1. **Columna C2 (4×4") y arriostre A1 (4×4") de la referencia:** no se usan. Todas las columnas son C1 continuas, como se decidió en la C01. A1 no tiene ubicación definida. ¿Se eliminan del juego o se ubica el A1?
2. **Uniones viga–columna y verificación de perfiles:** PD, según la memoria de cálculo.
3. **Columna del eje C en el eje 6:** está a 0,075 del eje (al ras de la fachada posterior). La elevación esquemática la dibuja sobre el eje.

## Validación
- DXF revisado con `recover` y `audit`: 0 errores.
- PDF revisado visualmente por zonas: sin textos superpuestos ni vistas recortadas.
- No se probó en AutoCAD.
