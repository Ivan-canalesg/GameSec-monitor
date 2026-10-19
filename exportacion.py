from datetime import datetime

from procesamiento import (
    calcular_estadisticas_globales,
    analizar_por_servidor,
    clasificar_incidentes
)


def exportar_reporte(sesiones: list[dict], ruta: str = "reporte_gamesec.txt") -> str:
    """
    Genera un reporte consolidado en un archivo de texto y devuelve la ruta.
    Lanza ValueError si no hay sesiones y OSError si no se puede escribir.
    """
    if not sesiones:
        raise ValueError("No hay sesiones para exportar.")

    estadisticas = calcular_estadisticas_globales(sesiones)
    rendimiento = analizar_por_servidor(sesiones)
    resumen, criticas = clasificar_incidentes(sesiones)

    fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    linea = "=" * 50

    lineas = [
        linea,
        "  GAMESEC MONITOR - REPORTE CONSOLIDADO",
        f"  Generado el: {fecha}",
        linea,
        "",
        "1. ESTADÍSTICAS GLOBALES",
        "-" * 50,
        f"Total de sesiones:         {estadisticas['total_sesiones']}",
        f"Ping promedio:             {estadisticas['ping_promedio']} ms",
        f"Duración promedio:         {estadisticas['duracion_promedio']} min",
        f"Partidas competitivas:     {estadisticas['porcentaje_competitivas']} %",
        "",
        "2. RENDIMIENTO POR SERVIDOR",
        "-" * 50,
    ]

    for servidor, datos in rendimiento.items():
        lineas.append(f"Servidor: {servidor}")
        lineas.append(f"  Sesiones:      {datos['cantidad']}")
        lineas.append(f"  Ping promedio: {datos['ping_promedio']} ms")
        lineas.append(f"  FPS promedio:  {datos['fps_promedio']}")
        lineas.append("")

    lineas += [
        "3. AUDITORÍA DE SEGURIDAD",
        "-" * 50,
        f"Sesiones NORMALES:    {resumen['NORMAL']}",
        f"({resumen['NORMAL'] / estadisticas['total_sesiones'] * 100:.2f} %)",
        f"Sesiones SOSPECHOSAS: {resumen['SOSPECHOSO']}",
        f"({resumen['SOSPECHOSO'] / estadisticas['total_sesiones'] * 100:.2f} %)",
        f"Sesiones CRÍTICAS:    {resumen['CRITICO']}",
        f"({resumen['CRITICO'] / estadisticas['total_sesiones'] * 100:.2f} %)",
        "",
        "Detalle de sesiones críticas:",
    ]

    if criticas:
        for incidente in criticas:
            lineas.append(
                f"  - Sesión {incidente['id_sesion']} | "
                f"Jugador {incidente['jugador_id']} | "
                f"Servidor {incidente['servidor']} | "
                f"{incidente['motivo']}"
            )
    else:
        lineas.append("  (ninguna)")

    lineas += ["", linea, "  FIN DEL REPORTE", linea]

    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write("\n".join(lineas) + "\n")

    return ruta
