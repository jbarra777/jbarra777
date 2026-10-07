# Lámina S03 · AGUAS PLUVIALES · rev0 (versión de trabajo)

**Estado:** versión de trabajo para revisión. No apta para construcción ni trámite.

## Archivos
| Archivo | Uso |
|---|---|
| `SR-S03_PLUVIALES_rev0.pdf` | Plano para revisar (A1 al 100 %) |
| `SR-S03_PLUVIALES_rev0.dxf` | Editable AutoCAD 2018, layout `S03-PLUVIALES` |

Generador: `scripts/s03_pluviales.py`, con los símbolos de `scripts/sanit.py`.
Bases en gris: A2 rev3 (nivel 1) y los ejes de la A4 rev4 (techo). La cubierta se dibujó según la geometría de la C04.

## Contenido
1. **Planta de techo a 1:100:**
   - lámina cal. 26 a dos aguas, con pendiente del 13 % y flechas por faldón;
   - cumbrera a +10.70 en y = 13.62, alero a +9.20 y bordes hacia los patios a +10.26;
   - **cuatro canoas:** frontal, posterior, hacia P1 (y = 10.26) y hacia P2 (y = 16.98), con la pendiente de cada una hacia sus bajantes (PD);
   - **seis bajantes:**
     - BP-1 y BP-2 en los extremos de la canoa frontal;
     - BP-3 y BP-4 en los de la canoa posterior;
     - BP-5 y BP-6 en el extremo este de las canoas de los patios.
2. **Planta del nivel 1 a 1:100:**
   - **Colector este** (x 8.55): BP-3 → CR-P3 → CR-P6 (+BP-6) → CR-P5 (+BP-5) → CR-P2 (+BP-2) → cuneta.
   - **Colector oeste** (x 0.85), por el pasillo peatonal: BP-4 → CR-P4 → CR-P7 → CR-P8 → CR-P9 → CR-P1 (+BP-1) → cuneta.
   - Cajas pluviales de 0.30 × 0.30 [PR] al pie de cada bajante y en los cambios de dirección, todas fuera de las placas F1/F2 (C01).
3. **Detalle 1, canoa:** sección típica a 1:10. Muestra la lámina, el clavador, la cercha, la V1, el muro, la canoa metálica negra, la malla protectora [PR], el soporte y el bajante. Dimensiones de 0.20 × 0.15 (PD).
4. **Detalle 2, caja pluvial [PR]:** sección y planta según la referencia (C07), con tapa armada de var. #2 @0.15 A.D. y var. #3 @0.17 A.D.
5. **Detalle 3, descarga a cuneta:** esquemático, pasando por el retiro, bajo la acera y al cordón.
6. **Cuadro de áreas tributarias**, calculado con la geometría de la C04 (proyección horizontal):

   | Canoa | Área | Por bajante |
   |---|---|---|
   | Frontal | 60.79 m² | 30.40 m² |
   | Hacia P1 | 24.80 m² | 24.80 m² |
   | Hacia P2 | 13.57 m² | 13.57 m² |
   | Posterior | 80.37 m² | 40.18 m² |
   | **Total** | **179.53 m²** | |

   El total coincide con la huella aprobada.
7. **Simbología y notas 1–14.**

## Decisiones del usuario aplicadas
- Las aguas pluviales van a la cuneta pública del frente.
- Canoas frontal y posterior con dos bajantes cada una, uno en cada extremo.
- Bajantes frontales ocultos en el N1.
- Canoas hacia los patios P1 y P2.
- Canoas y bajantes metálicos en negro (A5).
- El detalle de canoa va en esta lámina.

## Propuestas de Claude (por aprobar)
- **Un bajante por canoa de patio (BP-5 y BP-6), en el extremo este, junto al muro D.** Bajan por el patio hasta el N1 y se conectan al colector este. No descargan sobre la grava.
- **Trazado de los colectores bajo el N1:**
  - **Oeste:** va por el pasillo peatonal, entre los alimentadores eléctricos (E01, x 0.40/0.55) y la tubería AF (S01, x 1.10). Cruza los ductos eléctricos una vez entre CR-P9 y CR-P1.
  - **Este:** va junto al muro D y cruza los dos ramales sanitarios de la suite 2 (S02) entre CR-P6 y CR-P5.
  - Las profundidades relativas en los cruces son PD.
- **Material de los colectores enterrados:** PVC, como la "tubería PVC Ø indicado" de la caja pluvial de la referencia. Canoas y bajantes visibles, metálicos.

## Pendientes
- **PD:** diámetros de bajantes y colectores (dibujados como 4"). La referencia no indica diámetros pluviales y no hay cálculo hidráulico.
- **PD:** pendientes de canoas y colectores; calibre, desarrollo y soportes de las canoas.
- **PD:** cómo se ocultan BP-1 y BP-2 en el muro frontal del N1.
- **PD:** camisas en los cruces con las VA1.
- **PD:** descarga a la cuneta (ubicación, forma de conexión y permiso municipal).
- **Remates de cubierta:** hacen falta en los bordes de los patios que no llevan canoa (P1 frente y oeste, P2 fondo y oeste). Están PENDIENTES; no se dibujaron.
- **[PR]:** malla protectora, cajas de 0.30 × 0.30, detalle de caja pluvial y notas tomadas de la referencia.

## Validación
- DXF revisado con `recover` y `audit`: 0 errores.
- PDF revisado visualmente por zonas: planta de techo, nivel 1, detalles, cuadro, simbología y notas.
- No se probó en AutoCAD.
