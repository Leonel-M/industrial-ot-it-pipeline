# Plan del proyecto

Objetivo: tener, para julio-agosto 2026, un proyecto público en GitHub que demuestre integración OT-IT real con el stack que reconoce el mercado alemán, y que sirva como respuesta directa a la pregunta de entrevista "¿cuándo fue la última vez que trabajaste con PLC/SCADA?".

## Decisión pendiente: elegir el proceso a simular

✅ **Decidido: Opción B — Línea de producción simulada.**

Proceso: línea con estados **Run / Stop / Alarm**, contador de piezas producidas, y al menos una variable continua (ej. velocidad de la banda) para tener algo más que datos binarios en el análisis posterior.

### Variables (tags) iniciales a modelar en CODESYS

| Tag | Tipo | Descripción |
|---|---|---|
| `Line_State` | Enum (Run/Stop/Alarm) | Estado actual de la línea |
| `Piece_Count` | Entero, incremental | Contador de piezas producidas |
| `Belt_Speed_SP` | Real | Setpoint de velocidad (ajustable desde el celular) |
| `Belt_Speed_PV` | Real | Valor real simulado (con ruido/variación) |
| `Alarm_Active` | Booleano | Disparado manual o por umbral de velocidad |
| `Timestamp` | DateTime | Marca de tiempo de cada lectura |

### KPIs objetivo para la Fase 4 (dashboard)

- **OEE simplificado** (disponibilidad = tiempo en Run / tiempo total).
- Piezas producidas por hora.
- Frecuencia y duración de alarmas.
- Distribución de velocidad de banda (¿opera dentro de rango esperado?).

---

## Fase 0 — Setup del entorno (sin apuro, base sólida)

- [ ] Instalar CODESYS Development System (versión gratuita) y crear proyecto de simulación.
- [ ] Instalar Node.js + Node-RED, agregar el paquete `node-red-dashboard`.
- [ ] Instalar Python 3.11+, crear entorno virtual, instalar `opcua`/`asyncua`, `paho-mqtt`, `pandas`, `streamlit`, `scikit-learn`.
- [ ] Instalar un broker MQTT local para pruebas (ej. Mosquitto) — o usar el servidor OPC-UA embebido de CODESYS si prefieres evitar un componente extra al inicio.
- [ ] Verificar que el celular puede acceder al Node-RED Dashboard en la red local (probar con un flujo "Hola mundo" antes de construir nada más).

## Fase 1 — Lógica de PLC (tu parte de Ingeniería Electrónica)

- [ ] Modelar el proceso elegido (tanque o línea) como variables IEC 61131-3 en CODESYS.
- [ ] Programar la lógica de control (ON-OFF o PID simple) en modo simulación — sin hardware.
- [ ] Exponer las variables relevantes vía servidor OPC-UA integrado de CODESYS.
- [ ] Documentar en `docs/` un diagrama simple de las variables (tags) y su significado.

## Fase 2 — HMI móvil (Node-RED)

- [ ] Construir el dashboard en Node-RED: sliders/inputs para setpoints, indicadores de estado, botón de alarma manual.
- [ ] Conectar Node-RED al servidor OPC-UA de CODESYS (nodo `node-red-contrib-opcua`).
- [ ] Probar el flujo completo desde el celular: cambiar un setpoint desde el teléfono y verlo reflejado en la simulación.
- [ ] Exportar el flujo (`flows.json`) a `node-red/`.

## Fase 3 — Puente OT → IT (la pieza que cierra tu brecha)

- [ ] Escribir `python/opcua_client.py`: cliente que se suscribe a las variables OPC-UA y las imprime en consola.
- [ ] (Opcional, si sumas MQTT) Escribir `python/mqtt_client.py` con `paho-mqtt` para telemetría ligera en paralelo.
- [ ] Escribir `python/database.py`: guarda cada lectura con timestamp en SQLite.
- [ ] Dejar el capturador corriendo un tiempo (horas/días) generando un histórico real, no solo datos de una sesión de 5 minutos — esto da más peso analítico a la fase siguiente.

## Fase 4 — Capa de ciencia de datos

- [ ] Limpieza/transformación de la serie temporal (Pandas).
- [ ] Dashboard en Streamlit (`dashboard/app.py`) con KPIs: % tiempo en alarma, tendencia de la variable controlada, distribución de setpoints usados.
- [ ] Modelo simple de detección de anomalías (Isolation Forest) sobre la serie — marcar lecturas fuera de rango esperado.
- [ ] (Opcional, más peso) Comparar el dashboard también en Power BI, ya que es tu herramienta más fuerte laboralmente.

## Fase 5 — Documentación y narrativa de portafolio

- [ ] Capturas de pantalla: HMI en el celular, proyecto CODESYS, dashboard final.
- [ ] GIF o video corto (30-60 seg) mostrando el flujo end-to-end.
- [ ] Completar el README con el proceso elegido y resultados concretos (ej. "detecté X anomalías sobre Y horas de datos").
- [ ] Post de LinkedIn explicando el *por qué* del proyecto (la brecha OT-IT, y cómo lo resolviste).
- [ ] Preparar la respuesta de entrevista: sustituir "hace 10 años" por "en 2026 construí un pipeline OT-IT con CODESYS, OPC-UA y Python — puedo mostrarte el repo".

---

## Notas de honestidad para entrevistas

- Este proyecto es una **simulación educativa**, no producción real — decirlo así, sin inflar. Los reclutadores alemanes valoran la precisión sobre el alcance más que el over-selling.
- El diferenciador no es "sé usar CODESYS a nivel experto", es "entiendo el flujo completo OT→IT y puedo conversar con ambos equipos" — esa es tu propuesta de valor real frente a un data analyst sin trasfondo de ingeniería.
