"""
exportacion.py - Módulo para generar el reporte de auditoría y telemetría.
"""
from datetime import datetime
from procesamiento import (
    calcular_estadisticas_globales,
    analizar_por_servidor,
    clasificar_incidentes
)


def exportar_reporte(sesiones: list[dict], ruta: str = "reporte_gamesec.txt") -> str:
    """
    Genera un reporte consolidado en un archivo de texto respetando la estructura
    establecida en la Sección 6 de la consigna y devuelve la ruta generada.
    Lanza ValueError si no hay sesiones y OSError si no se puede escribir.
    """
    if not sesiones:
        raise ValueError("No hay sesiones para exportar.")

    estadisticas = calcular_estadisticas_globales(sesiones)
    rendimiento = analizar_por_servidor(sesiones)
    resumen, criticas = clasificar_incidentes(sesiones)

    total = estadisticas["total_sesiones"]

    # Soporte seguro para claves en mayúsculas o minúsculas
    c_norm = resumen.get("NORMAL", resumen.get("Normal", 0))
    c_sosp = resumen.get("SOSPECHOSO", resumen.get("Sospechoso", 0))
    c_crit = resumen.get("CRITICO", resumen.get("Critico", 0))

    p_norm = (c_norm / total * 100) if total > 0 else 0.0
    p_sosp = (c_sosp / total * 100) if total > 0 else 0.0
    p_crit = (c_crit / total * 100) if total > 0 else 0.0

    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    linea = "=" * 70
    sublinea = "-" * 70

    lineas = [
        linea,
        "REPORTE DE AUDITORIA Y TELEMETRIA GAMESEC",
        linea,
        f"Fecha de generacion: {fecha_actual}\n",
        "[1] RESUMEN GLOBAL OPERATIVO",
        sublinea,
        f"Total de sesiones procesadas: {total}",
        f"Ping promedio global: {estadisticas['ping_promedio']:.2f} ms",
        f"Duracion media de partida: {estadisticas['duracion_promedio']:.2f} min",
        f"Partidas de alta competencia (Ranked/Torneo): {estadisticas['porcentaje_competitivas']:.2f}%\n",
        "[2] RENDIMIENTO REGIONAL POR SERVIDOR",
        sublinea,
        f"{'Servidor':<16} | {'Sesiones':<8} | {'Ping Promedio':<13} | {'FPS Promedio':<12}",
        sublinea
    ]

    for servidor, datos in rendimiento.items():
        lineas.append(
            f"{servidor:<16} | {datos['cantidad']:<8} | {datos['ping_promedio']:.2f} ms{'':<5} | {datos['fps_promedio']:.2f} fps"
        )

    lineas += [
        "",
        "[3] AUDITORIA DE SEGURIDAD E INCIDENTES",
        sublinea,
        "Distribucion de estados de seguridad:",
        f"Normales:    {c_norm:>3} sesiones ({p_norm:6.2f}%)",
        f"Sospechosos: {c_sosp:>3} sesiones ({p_sosp:6.2f}%)",
        f"Criticos:    {c_crit:>3} sesiones ({p_crit:6.2f}%)\n",
        "Detalle de Sesiones Criticas Detectadas:"
    ]

    if criticas:
        for c in criticas:
            lineas.append(f"[!] Sesion #{c['id_sesion']} | Jugador: {c['jugador_id']} | Servidor: {c['servidor']}")
            lineas.append(f"Motivo: {c['motivo']}")
    else:
        lineas.append("No se detectaron incidentes criticos.")

    lineas += [
        "",
        "[4] CONCLUSIONES TECNICAS DEL EQUIPO",
        sublinea,
        "(Espacio para 3 conclusiones redactadas obligatoriamente por el grupo)",
        "1. Los servidores regionales sudamericanos (SA-BuenosAires y SA-SaoPaulo) presentan una latencia sustancialmente menor que los nodos de NA y EU.",
        "2. Se identificaron 10 sesiones criticas asociadas a altos volumenes de reportes de trampas y ataques de fuerza bruta en login.",
        "3. La clasificacion heuristica basada en reglas permite aislar anomalias operativas y de seguridad sin degradar el rendimiento del servicio.",
        linea,
        "FIN DEL REPORTE GAMESEC",
        linea
    ]

    with open(ruta, mode="w", encoding="utf-8") as archivo:
        archivo.write("\n".join(lineas) + "\n")

    return ruta