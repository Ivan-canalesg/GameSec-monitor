GameSec monitor.

Descripcion:
Es un programa hecho en python para el analisis de sesiones de partidas multijugador. Evalua el rendimiento
de cada servidor de forma separada, asì como los reportes de jugadores y los intentos de inicio de sesion de estos.

Funciones:

-Carga y validación de datos desde un archivo CSV.

-Cálculo de estadísticas globales.

-Análisis del ping y los FPS promedio por servidor.

-Clasificación de sesiones en normales, sospechosas y críticas.

-Exportación de un informe consolidado en formato TXT.

Archivos principales:

-main.py: menú principal e interacción con el usuario.

-carga.py: carga y validación del CSV.

-procesamiento.py: estadísticas y análisis de seguridad.

-exportacion.py: generación del informe de texto.

-gamesec_logs.csv: dataset de telemetría.

Requisitos:

Python 3.10+


Ejecucion:

python3 main.py
