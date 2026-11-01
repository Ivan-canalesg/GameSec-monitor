def calcular_estadisticas_globales(sesiones: list[dict]) -> dict:
    if not sesiones:
        raise ValueError("No hay sesiones para analizar.")

    total_sesiones = len(sesiones)
    suma_ping = 0
    suma_duracion = 0
    cantidad_competitivas = 0

    for sesion in sesiones:
        suma_ping += sesion["ping_promedio"]
        suma_duracion += sesion["duracion_minutos"]

        if sesion["tipo_partida"] in ("Competitiva", "Torneo"):
            cantidad_competitivas += 1

    ping_promedio = round(suma_ping / total_sesiones, 2)
    duracion_promedio = round(suma_duracion / total_sesiones, 2)

    porcentaje_competitivas = round(
        (cantidad_competitivas / total_sesiones) * 100, 2
    )

    estadisticas = {
        "total_sesiones": total_sesiones,
        "ping_promedio": ping_promedio,
        "duracion_promedio": duracion_promedio,
        "porcentaje_competitivas": porcentaje_competitivas
    }

    return estadisticas




def analizar_por_servidor(sesiones: list[dict]) -> dict:
    if not sesiones:
        raise ValueError("No hay sesiones para analizar.")

    acumulador = {}

    for sesion in sesiones:
        servidor = sesion["servidor"]

        if servidor not in acumulador:
            acumulador[servidor] = {
                "cantidad": 0,
                "suma_ping": 0,
                "suma_fps": 0
            }

        acumulador[servidor]["cantidad"] += 1
        acumulador[servidor]["suma_ping"] += sesion["ping_promedio"]
        acumulador[servidor]["suma_fps"] += sesion["fps_promedio"]

    resultados = {}

    for servidor, datos in acumulador.items():
        cantidad = datos["cantidad"]

        resultados[servidor] = {
            "cantidad": cantidad,
            "ping_promedio": round(datos["suma_ping"] / cantidad, 2),
            "fps_promedio": round(datos["suma_fps"] / cantidad, 2)
        }

    return resultados




def clasificar_incidentes(sesiones: list[dict]) -> tuple[dict, list[dict]]:
    if not sesiones:
        raise ValueError("No hay sesiones para analizar.")

    resumen = {
        "NORMAL": 0,
        "SOSPECHOSO": 0,
        "CRITICO": 0
    }

    sesiones_criticas = []

    for sesion in sesiones:
        reportes = sesion["reportes_trampa"]
        intentos = sesion["intentos_fallidos"]
        ping = sesion["ping_promedio"]

        if reportes >= 3 or intentos >= 4:
            categoria = "CRITICO"
            motivos = []

            if reportes >= 3:
                motivos.append(
                    f"Exceso de reportes de trampa ({reportes})"
                )

            if intentos >= 4:
                motivos.append(
                    f"Exceso de intentos fallidos ({intentos})"
                )

            sesiones_criticas.append({
                "id_sesion": sesion["id_sesion"],
                "jugador_id": sesion["jugador_id"],
                "servidor": sesion["servidor"],
                "motivo": " y ".join(motivos)
            })

        elif (ping > 200 and intentos >= 2) or reportes == 2:
            categoria = "SOSPECHOSO"

        else:
            categoria = "NORMAL"

        resumen[categoria] += 1

    return resumen, sesiones_criticas


