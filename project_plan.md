# Plan del proyecto

Objetivo: tener, para julio-agosto 2026, un proyecto público en GitHub que demuestre integración OT-IT real con el stack que reconoce el mercado alemán, y que sirva como respuesta directa a la pregunta de entrevista "¿cuándo fue la última vez que trabajaste con PLC/SCADA?".

## Decisión pendiente: elegir el proceso a simular

✅ **Decidido: Opción B — Línea de producción simulada.**

Proceso: línea con estados **Run / Stop / Alarm**, contador de piezas producidas, y al menos una variable continua (velocidad de la banda).

### Variables (tags) modeladas en CODESYS

| Tag | Tipo | Descripción |
|---|---|---|
| `Line_State` | INT (0=Idle,1=Run,2=Alarm,3=Stop) | Estado actual de la línea |
| `Piece_Count` | DINT | Contador de piezas producidas |
| `Belt_Speed_SP` | REAL | Setpoint de velocidad (ajustable desde el celular) |
| `Belt_Speed_PV` | REAL | Valor real simulado (oscilación con dos senos) |
| `Alarm_Active` | BOOL | Disparado por desviación de velocidad, con debounce 5s |
| `Start_Button` / `Stop_Button` / `Reset_Button` | BOOL | Controles de operador, con interlock Set/Reset mutuo |
| `CurrentTime` | DT | Reloj del sistema |

### KPIs objetivo para la Fase 4 (dashboard)

- **OEE simplificado** (disponibilidad = tiempo en Run / tiempo total).
- Piezas producidas por hora.
- Frecuencia y duración de alarmas.
- Distribución de velocidad de banda (¿opera dentro de rango esperado?).

---

## Fase 0 — Setup del entorno

- [x] Instalar CODESYS Development System (versión gratuita) y crear proyecto de simulación.
- [x] Instalar Node.js + Node-RED, agregar `node-red-dashboard` + `node-red-contrib-ui-led`.
- [ ] Instalar Python 3.11+, crear entorno virtual, instalar `asyncua`, `paho-mqtt`, `pandas`, `streamlit`, `scikit-learn`.
- [ ] Instalar un broker MQTT local para pruebas (ej. Mosquitto) — opcional, evaluar si se usa.
- [x] Verificar que el celular puede acceder al Node-RED Dashboard en la red local.

## Fase 1 — Lógica de PLC ✅ CERRADA

- [x] GVL con variables globales del proceso.
- [x] Máquina de estados en SFC (Idle/Run/Alarm/Stop) con bifurcación Run→Alarm vs. Run→Stop.
- [x] Lógica de control en ST: simulación de velocidad (oscilación con dos senos, clamp con MAX), alarma por desviación con debounce 5s, temporizador TON para conteo de piezas.
- [x] Interlock de botones en Ladder (POU separado, Set/Reset mutuo).
- [x] HMI base en CODESYS Visualization siguiendo convención ISA-101.
- [x] Servidor OPC-UA expuesto: autenticación usuario/contraseña (`Administrator`), canal cifrado `Basic256Sha256 - Sign`, certificados servidor↔cliente confiados mutuamente, Symbol Set `SimSet` con permisos configurados.
- [x] Validado con lectura y escritura en tiempo real desde UaExpert.
- [x] Documentado en `docs/opcua_setup.md`: procedimiento completo + tabla de errores reales resueltos.

## Fase 2 — HMI móvil (Node-RED) ✅ CERRADA

- [x] Dashboard en Node-RED: gauge de velocidad, LED de estado (4 colores) y alarma, texto de contador de piezas, botones Start/Stop/Reset, slider de setpoint.
- [x] Conectado al servidor OPC-UA de CODESYS vía `node-red-contrib-opcua` (subscribe para lectura, write para control).
- [x] Patrón de pulso momentáneo (nodo `trigger`, 250ms) para evitar variables enclavadas en los botones de control.
- [x] Demux de variables con nodo `switch` sobre `msg.topic` + filtro `rbe` (report-by-exception) para evitar saturar el debug.
- [x] Probado end-to-end desde el celular (vía Windows Mobile Hotspot, por aislamiento de clientes en el router del ISP).
- [x] Flujo exportado a `node-red/flows.json`.
- [x] Troubleshooting documentado en `docs/fase_2_node_red_dashboard.md`.

## Fase 3 — Puente OT → IT (la pieza que cierra tu brecha) — SIGUIENTE

- [ ] Escribir `python/opcua_client.py`: cliente `asyncua` que se suscribe a las variables OPC-UA y las imprime en consola.
- [ ] (Opcional, si sumas MQTT) Escribir `python/mqtt_client.py` con `paho-mqtt` para telemetría ligera en paralelo.
- [ ] Escribir `python/database.py`: guarda cada lectura con timestamp en SQLite.
- [ ] Dejar el capturador corriendo un tiempo (horas/días) generando un histórico real.

## Fase 4 — Capa de ciencia de datos

- [ ] Limpieza/transformación de la serie temporal (Pandas).
- [ ] Dashboard en Streamlit (`dashboard/app.py`) con KPIs.
- [ ] Modelo simple de detección de anomalías (Isolation Forest).
- [ ] (Opcional) Comparar también en Power BI.

## Fase 5 — Documentación y narrativa de portafolio

- [ ] Capturas de pantalla: HMI en el celular, proyecto CODESYS, dashboard final.
- [ ] GIF o video corto (30-60 seg) mostrando el flujo end-to-end.
- [ ] Completar el README con resultados concretos.
- [ ] Post de LinkedIn explicando el *por qué* del proyecto.
- [ ] Preparar la respuesta de entrevista.

---

## Notas de honestidad para entrevistas

- Este proyecto es una **simulación educativa**, no producción real — decirlo así, sin inflar.
- El diferenciador no es "sé usar CODESYS a nivel experto", es "entiendo el flujo completo OT→IT y puedo conversar con ambos equipos".
- La demo corre con CODESYS y Node-RED en la misma máquina por simplicidad; en producción, Node-RED correría en un gateway edge dedicado, separado físicamente del PLC.