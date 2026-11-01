
import csv
import os

def cargar_telemetria(ruta_archivo: str) -> list[dict]:
    """
    Lee el archivo CSV de telemetría, valida su existencia e integridad
    y transforma cada registro en un diccionario con tipos de datos nativos.
    """

    # Validar que el archivo exista
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(
            f"El archivo '{ruta_archivo}' no existe. Verifique la ubicación."
        )

    sesiones = []

    # Abrir el archivo en modo lectura
    with open(ruta_archivo, mode="r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)

        # Recorrer cada fila del CSV
        for fila in lector:

            # Crear el diccionario de la sesión
            sesion = {
                "id_sesion": int(fila["id_sesion"]),
                "servidor": fila["servidor"],
                "jugador_id": fila["jugador_id"],
                "tipo_partida": fila["tipo_partida"],
                "ping_promedio": int(fila["ping_promedio"]),
                "fps_promedio": int(fila["fps_promedio"]),
                "duracion_minutos": float(fila["duracion_minutos"]),
                "intentos_fallidos": int(fila["intentos_fallidos"]),
                "reportes_trampa": int(fila["reportes_trampa"])
            }

            sesiones.append(sesion)

    # Validar que haya al menos un registro
    if len(sesiones) == 0:
        raise ValueError(
            f"El archivo '{ruta_archivo}' está vacío o no contiene registros."
        )

    return sesiones

