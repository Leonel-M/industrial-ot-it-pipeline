# Industrial OT-IT Data Pipeline

**De la planta a la decisión de negocio: un pipeline OT→IT construido desde cero, sin hardware físico, usando el stack real que usa la industria alemana.**

## Contexto del proyecto

Tengo formación en Ingeniería Electrónica (automatización y control) y experiencia real como Analista de Datos, pero un vacío de ~10 años entre ambos mundos. Este proyecto cierra esa brecha: simula un proceso industrial controlado por PLC, expone sus datos por los protocolos estándar de la industria (OPC-UA / MQTT), y construye encima un pipeline de análisis de datos completo.

## Arquitectura

```
[Celular / Node-RED Dashboard]  →  actúa como panel de operador (setpoints, estados, alarmas)
            ↓
[CODESYS — lógica de PLC simulada, IEC 61131-3]
            ↓  (OPC-UA + MQTT)
[Python — cliente OPC-UA/MQTT]  →  captura y valida datos en tiempo real
            ↓
[Base de datos — SQLite/PostgreSQL]  →  histórico de series de tiempo
            ↓
[Dashboard de análisis — Streamlit / Power BI]  →  KPIs, tendencias, detección de anomalías
```

## Stack técnico

| Capa | Herramienta | Por qué |
|---|---|---|
| Lógica PLC | [CODESYS](https://www.codesys.com/) | Estándar IEC 61131-3, empresa alemana, simulador gratuito |
| HMI / operador móvil | [Node-RED](https://nodered.org/) + Node-RED Dashboard | Open source, estándar de facto en prototipado IIoT |
| Protocolo industrial | OPC-UA (principal) + MQTT | OPC-UA es el estándar dominante en la industria alemana; MQTT para telemetría ligera |
| Captura de datos | Python (`opcua`, `paho-mqtt`) | — |
| Almacenamiento | SQLite (dev) / PostgreSQL (prod) | — |
| Análisis y visualización | Python (Pandas, Plotly) + Streamlit / Power BI | — |
| Detección de anomalías | Scikit-learn (Isolation Forest) | — |

## Proceso simulado

**Línea de producción** con estados Run/Stop/Alarm, contador de piezas y control de velocidad de banda. Detalle de tags y KPIs en `docs/project_plan.md`.

## Estructura del repositorio

```
industrial-ot-it-pipeline/
├── README.md
├── docs/
│   └── project_plan.md        # plan de fases, checklist, decisiones técnicas
├── codesys/                   # proyecto CODESYS (lógica PLC simulada)
├── node-red/                  # flujo exportado (flows.json) del dashboard móvil
├── python/
│   ├── opcua_client.py
│   ├── mqtt_client.py
│   ├── database.py
│   └── requirements.txt
├── dashboard/
│   └── app.py                 # dashboard Streamlit de análisis
├── data/                      # datos capturados (histórico, .db)
└── screenshots/               # capturas del HMI, dashboard, arquitectura
```

## Estado del proyecto

🚧 En construcción — ver `docs/project_plan.md` para el roadmap y el checklist de avance.

## Autor

[Tu nombre] — en transición hacia roles de Data/BI Analyst e Industrial Data Analyst en Alemania.
[LinkedIn] · [Portafolio]
