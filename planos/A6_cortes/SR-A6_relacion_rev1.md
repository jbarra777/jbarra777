# Lámina A6 · CORTES · rev1 (versión de trabajo)

**Estado:** versión de trabajo para revisión. No apta para construcción ni trámite.

## Archivos
| Archivo | Uso |
|---|---|
| `SR-A6_CORTES_rev1.pdf` | Plano para revisar (A1 al 100 %) |
| `SR-A6_CORTES_rev1.dxf` | Editable AutoCAD 2018, layout `A6-CORTES` |

## Cambios respecto a rev0 (sus instrucciones del 06-10-2026)
| Indicación | Aplicado |
|---|---|
| a) Columnas continuas y a plomo | Columnas del eje C dibujadas en vista desde ±0.00 hasta +9.00 en los tres niveles: C2–C6 en el A-A y C5 en el B-B. En las plantas ya estaban alineadas (x = 4.84); el desfase solo existía en el dibujo del corte. |
| b) Jerarquía de líneas | Elementos cortados con línea gruesa de 0.70, en vista de 0.25 y cielos de 0.18. Todos los entrepisos cortados muestran su sección completa. |
| c) Nivel 1 | **Contrapiso** (concreto, gris) en estacionamientos, pasillo y gradas. **Grava** (trama) en el resto: jardín seco, bajo los patios, retiro posterior y retiro frontal. |
| d) Cubierta | Se eliminó la línea simple. Ahora: lámina cal. 26 cortada, **clavadores** cortados y **cercha metálica** del eje C en vista (cordón superior al 13 %, cordón inferior a +9.00, montantes y diagonales tipo Pratt). En el B-B las cerchas se ven cortadas. |
| e) Rótulos y simbología | Rótulos con línea guía para lámina, cercha, cielo, forro Steel Tech, sobrelosa, viga, columna, acero expuesto, contrapiso, grava, mampostería y tapia. Simbología de materiales debajo de las notas. |
| Mampostería y Steel Tech | **Mampostería** (trama diagonal): muros de lindero, tapia posterior y frente del N1 sobre el portón. **Forro Steel Tech** (contorno con eje): fachadas y muros hacia los patios. Paredes interiores solo con contorno. Espesores de 0.15 y 0.12 sin cambio. |
| Entrepiso | Sobrelosa de **0.10** sobre lámina colaborante y vigas de acero. |
| Cielos | **Gypsum regular plano** suspendido a 2.70 en N2 y N3. **Acero expuesto** en el N1. |
| Cimentación | No se dibuja. Nota 13: "según planos estructurales". |
| Columnas de los ejes A y D | No se agregan. Quedan para el diseño estructural (nota 5). |

## Criterio de las cerchas (mi propuesta; geometría PD, según estructural)
- Van en la dirección de la pendiente (de frente a fondo), sobre la viga corona (+9.00), interrumpidas en los patios.
- **Ubicación propuesta:** junto a los dos muros de lindero (x 0.30 y 8.70) y en los ejes B y C.
  - Separación máxima de unos 3.9 m.
  - Clavadores perpendiculares a las cerchas, aproximadamente cada 1.0 m sobre la pendiente.
- **Peralte:** de unos 0.75 junto a P1 hasta 1.50 en la cumbrera. Paneles de unos 1.15 m con diagonales tipo Pratt.
- Cerca de las fachadas, donde la cercha se queda sin peralte, los clavadores apoyan en la viga corona.
- Los muros que dan a los patios en el N3 suben como culata hasta la cubierta. Los interiores llegan a +9.00.

## Puntos a confirmar
1. **Retiro frontal:** lo dibujé en grava porque usted dijo "todo lo demás en grava", pero por ahí entran los carros. ¿Grava o contrapiso?
2. **Paredes interiores (0.12):** usted indicó Steel Tech solo para el forro. ¿Qué sistema llevan las interiores? En el corte solo tienen contorno.
3. **Valores PD que siguen:**
   - viga de entrepiso de 0.20;
   - contrapiso de 0.10;
   - puertas de 2.10;
   - ventanas a patios con antepecho de 0.90 y dintel a 2.20;
   - geometría de cerchas y clavadores.

## Validación
- DXF revisado con `recover` y `audit`: 0 errores.
- PDF revisado visualmente por zonas.
- No se probó en AutoCAD.
