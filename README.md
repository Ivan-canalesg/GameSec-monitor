# GameSec Monitor

**Trabajo Práctico (TP) – Proyecto desarrollado en Python**

## Integrantes

- Iván Gustavo Canales - DNI: 39849090 - Ciberseguridad
- Kiano kapriel marchant - DNI: 47734720 - Ciberseguridad 
- Facundo Ezequiel Sanabria - DNI: 41572847 - Tecnicatura en videojuegos
- Alejandro Ariel Barquinero - DNI: 30245471 - Tecnicatura en videojuegos 

## Descripción

Programa desarrollado en Python para el análisis de sesiones de partidas multijugador. Evalúa el rendimiento de cada servidor de forma separada, así como los reportes de jugadores y sus intentos de inicio de sesión.

## Funciones

- Carga y validación de datos desde un archivo CSV.
- Cálculo de estadísticas globales.
- Análisis del ping y los FPS promedio por servidor.
- Clasificación de sesiones en normales, sospechosas y críticas.
- Exportación de un informe consolidado en formato TXT.

## Archivos principales

| Archivo | Descripción |
|---|---|
| `main.py` | Menú principal e interacción con el usuario |
| `carga.py` | Carga y validación del CSV |
| `procesamiento.py` | Estadísticas y análisis de seguridad |
| `exportacion.py` | Generación del informe de texto |
| `gamesec_logs.csv` | Dataset de telemetría |

## Requisitos

- Python 3.10 o superior

## Ejecución

```bash
python3 main.py
```
