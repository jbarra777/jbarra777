# Lámina C06 · PÓRTICOS EJE TRANSVERSAL · rev0 (versión de trabajo)

**Estado:** versión de trabajo para revisión. No apta para construcción ni trámite.

## Archivos
| Archivo | Uso |
|---|---|
| `SR-C06_PORTICOS_TRANSVERSAL_rev0.pdf` | Plano para revisar (A1 al 100 %) |
| `SR-C06_PORTICOS_TRANSVERSAL_rev0.dxf` | Editable AutoCAD 2018, layout `C06-PORTICOS` |

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
- **Pórticos 2 a 6** (iguales): C1 en A, C y D; V1 de A a D en N2, N3 y corona; VA1; placas F2–F1–F2. Las cerchas CE-1 se muestran cortadas sobre la V1 de corona.
- **Pórtico 1** (fachada frontal): C1 solo en A y D.
  - La V1 salva 8,85 m y recibe la V1 del eje C (se muestra en sección).
  - Nota: verificar en el cálculo (PD).
- Ejes con cotas, niveles N1–N3 y corona, cota de cimentación (1,05), simbología y notas 1 a 7.

## Pendientes y puntos a confirmar
1. **Columna C2 (4×4") y arriostre A1 (4×4") de la referencia:** no se usan. Todas las columnas son C1 continuas, como se decidió en la C01. A1 no tiene ubicación definida. ¿Se eliminan del juego o se ubica el A1?
2. **Uniones viga–columna y verificación de perfiles:** PD, según la memoria de cálculo.
3. **Columna del eje C en el eje 6:** está a 0,075 del eje (al ras de la fachada posterior). La elevación esquemática la dibuja sobre el eje.

## Validación
- DXF revisado con `recover` y `audit`: 0 errores.
- PDF revisado visualmente por zonas: sin textos superpuestos ni vistas recortadas.
- No se probó en AutoCAD.
