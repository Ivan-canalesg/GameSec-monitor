
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

"""
#script de prueba, descomentar si se quiere testear de forma aislada

if __name__ == "__main__":
    archivo_prueba = "gamesec_logs.csv"

    try:
        datos = cargar_telemetria(archivo_prueba)

        print(f"-> Carga exitosa: se leyeron {len(datos)} registros.")

        primer_registro = datos[0]

        print("\nPrimer registro procesado:")
        print(primer_registro)

        print("\nVerificación de tipos de datos:")
        print(
            "id_sesion es entero?:",
            isinstance(primer_registro["id_sesion"], int)
        )

        print(
            "duracion_minutos es float?:",
            isinstance(primer_registro["duracion_minutos"], float)
        )

        print(
            "ping_promedio es entero?:",
            isinstance(primer_registro["ping_promedio"], int)
        )

    except Exception as error:
        print(f"Error al ejecutar la carga: {error}")

"""

