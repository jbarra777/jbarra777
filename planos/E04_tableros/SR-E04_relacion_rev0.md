# Lámina E04 · UNIFILAR, TABLEROS Y NOTAS ELÉCTRICAS · rev0 (versión de trabajo)

**Estado:** versión de trabajo para revisión. No apta para construcción ni trámite.

## Archivos
| Archivo | Uso |
|---|---|
| `SR-E04_TABLEROS_rev0.pdf` | Plano para revisar (A1 al 100 %) |
| `SR-E04_TABLEROS_rev0.dxf` | Editable AutoCAD 2018, layout `E04-TABLEROS` |

Generador: `scripts/e04_tableros.py` (simbología común `elec.py`).

## Criterio
- **Valores de la referencia (RIVERGRAND EL08–EL10) [PR]**, por indicación del usuario:
  - cargas por tipo de circuito: iluminación 500 VA, tomas generales 500 VA, cocina 1500 VA, calentador 6000 VA, cocina eléctrica 8000 VA, secadora 6000 VA;
  - disyuntores, conductores THHN, distancias y tuberías;
  - alimentadores: TP→TN2 como PB→TN1 y TP→TN3 como PB→TN2;
  - acometida de 200 A en 3/0;
  - factores de demanda (0,70 y 0,80) y de potencia (0,95).
- **Lista de circuitos:** la de esta vivienda, según las láminas E01–E03 aprobadas.
- **Caída de tensión:** %CT = 2 L I R / V, con la resistencia por metro deducida de los cuadros de la referencia.
- **Sin citas normativas ni marcas** (mismo criterio que la A11 y la C06). La referencia a la CNFL se cambió por "empresa distribuidora".

## Contenido
- **Diagrama unifilar eléctrico:**
  - red de suministro → medidor → interruptor principal de 200 A → transición aero-subterránea;
  - alimentador al TP, y del TP a los subtableros TN2 y TN3;
  - puesta a tierra.
- **Diagrama de voz y datos:** servicio → transición → PVD → salidas.
- **Tabla resumen:** kVA totales y demandados, conductores, longitudes y caída de tensión de TP, TN2 y TN3.
- **Cuadros de tableros** (TP, TN2 y TN3): carga por fase y caída de tensión de cada circuito.

| Tablero | kVA totales | kVA demandados | Caída de tensión |
|---|---|---|---|
| TP | 38,3 | 26,8 | 0,58 % |
| TN2 | 18,5 | 14,8 | 0,46 % |
| TN3 | 20,0 | 16,0 | 1,04 % |

- **Notas eléctricas [PR]:** generales, canalizaciones, conductores (con colores) y voz y datos.
- **Simbología.**

## Pendientes
1. Todos los valores de carga, protecciones y conductores son de la referencia [PR]. Debe verificarlos el profesional eléctrico.
2. La base del medidor y el medidor los define la empresa distribuidora (PD).
3. Las cargas reales de la cocina, la secadora y los calentadores dependen del equipo que se elija.

## Validación
- DXF revisado con `recover` y `audit`: 0 errores.
- PDF revisado visualmente por zonas.
- No se probó en AutoCAD.
