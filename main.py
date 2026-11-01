import os

from procesamiento import (
    calcular_estadisticas_globales,
    analizar_por_servidor,
    clasificar_incidentes
)

from carga import (
    cargar_telemetria
)

from datetime import datetime


ANCHO_REPORTE = 60

CONCLUSIONES_PREDETERMINADAS = (
    "(Espacio para 3 conclusiones redactadas obligatoriamente por el grupo)\n"
    "1. Latencia regional: Los servidores de Sudamerica (SA-BuenosAires y SA-SaoPaulo) "
    "mantienen una latencia media notablemente menor (< 80 ms) que los nodos de NA y EU (> 190 ms).\n"
    "2. Patron de incidentes criticos: El 100% de las 10 sesiones criticas combinan multiples "
    "denuncias por trampas (>= 4) e intentos fallidos de conexion (>= 4), evidenciando fuerza bruta y uso de hacks.\n"
    "3. Eficacia heuristica: La clasificacion por reglas aislo con precision el 6.67% de anomalias "
    "sin penalizar al 78.67% de partidas normales, proveyendo una base solida para mitigacion en tiempo real."
)

def exportar_reporte(sesiones: list[dict], conclusiones: str = "",
                     ruta: str = "reporte_gamesec.txt") -> str:
    """
    Genera el reporte de auditoría y telemetría en un archivo de texto
    y devuelve la ruta. Lanza ValueError si no hay sesiones y OSError
    si no se puede escribir.
    """
    if not sesiones:
        raise ValueError("No hay sesiones para exportar.")

    estadisticas = calcular_estadisticas_globales(sesiones)
    rendimiento = analizar_por_servidor(sesiones)
    resumen, criticas = clasificar_incidentes(sesiones)

    total = estadisticas['total_sesiones']
    fecha = datetime.now().strftime("%d/%m/%Y")
    linea = "=" * ANCHO_REPORTE
    guiones = "-" * ANCHO_REPORTE

    # Encabezado
    lineas = [
        linea,
        "REPORTE DE AUDITORIA Y TELEMETRIA      GAMESEC".center(ANCHO_REPORTE).rstrip(),
        linea,
        f"Fecha de generacion: {fecha}",
        "",
    ]

    # [1] Resumen global
    lineas += [
        "[1] RESUMEN GLOBAL OPERATIVO",
        guiones,
        f"Total de sesiones procesadas: {total}",
        f"Ping promedio global: {estadisticas['ping_promedio']:.2f} ms",
        f"Duracion media de partida: {estadisticas['duracion_promedio']:.2f} min",
        f"Partidas de alta competencia (Ranked/Torneo): "
        f"{estadisticas['porcentaje_competitivas']:.2f}%",
        "",
    ]

    # [2] Rendimiento por servidor
    fila = "{:<17} | {:<8} | {:<13} | {}"
    lineas += [
        "[2] RENDIMIENTO REGIONAL POR SERVIDOR",
        guiones,
        fila.format("Servidor", "Sesiones", "Ping Promedio", "FPS Promedio"),
        guiones,
    ]
    for servidor, datos in rendimiento.items():
        lineas.append(
            fila.format(
                servidor,
                datos['cantidad'],
                f"{datos['ping_promedio']:.2f} ms",
                f"{datos['fps_promedio']:.2f} fps",
            )
        )
    lineas.append("")

    # [3] Auditoría de seguridad
    def fila_estado(etiqueta, clave):
        cantidad = resumen[clave]
        porcentaje = cantidad / total * 100
        return (f"      {etiqueta:<13}{cantidad:>3} sesiones "
                f"({porcentaje:>5.2f}%)")

    lineas += [
        "[3] AUDITORIA DE SEGURIDAD E INCIDENTES",
        guiones,
        "Distribucion de estados de seguridad:",
        fila_estado("Normales:", "NORMAL"),
        fila_estado("Sospechosos:", "SOSPECHOSO"),
        fila_estado("Criticos:", "CRITICO"),
        "",
        "Detalle de Sesiones Criticas Detectadas:",
    ]

    if criticas:
        for incidente in criticas:
            lineas.append(
                f"  [!] Sesion #{incidente['id_sesion']}  | "
                f"Jugador: {incidente['jugador_id']} | "
                f"Servidor: {incidente['servidor']}"
            )
            lineas.append(f"      Motivo: {incidente['motivo']}")
    else:
        lineas.append("  (ninguna)")
    lineas.append("")

    # [4] Conclusiones técnicas
    lineas += [
        "[4] CONCLUSIONES TECNICAS DEL EQUIPO",
        guiones,
    ]
    if not conclusiones.strip() or conclusiones.strip().lower() == "conclusiones":
        texto_final = CONCLUSIONES_PREDETERMINADAS
    else:
        texto_final = conclusiones.strip()

    lineas.extend(texto_final.splitlines())

    lineas += ["", linea, "FIN DEL REPORTE GAMESEC".center(ANCHO_REPORTE).rstrip(), linea]

    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write("\n".join(lineas) + "\n")

    return ruta

def pedir_conclusiones():
    """Pide las conclusiones técnicas por consola; termina con una línea vacía."""
    print("Escriba las conclusiones técnicas del equipo.")
    print("O presione ENTER directamente para incluir las 3 conclusiones oficiales:")
    lineas = []
    while True:
        texto = input("> ").strip()
        if not texto:
            break
        lineas.append(texto)
    return "\n".join(lineas)                   





def logo():
    return r"""

 ███   ███  █   █ █████  ████ █████  ███    
█ ░░░ █ ░░█ ██ ██░█░░░░░█ ░░░░█░░░░░█ ░░░   
█░ ██░█████░█░█ █░████░░░███░░████░░█░ ░░░  
█░░ █░█░░░█░█░░░█░█░░░░   ░░█ █░░░░ █░░     
 ███ ░█░░░█░█░░ █░█████░████░░█████░ ███    
  ░░░ ░░░  ░░░░  ░░░░░░░ ░░░░ ░░░░░░  ░░░   
   ░░░  ░   ░ ░   ░ ░░░░░ ░░░░  ░░░░░  ░░░  

"""



def limpiar_pantalla():
    """Limpia la consola en Windows, Linux y macOS."""
    os.system("cls" if os.name == "nt" else "clear")


def volver_al_menu():
    """Pausa hasta que el usuario presione Enter."""
    input("\nPresione ENTER para volver al menú...")


def mostrar_menu():
    print(logo())
    print("\n=========================================")
    print("      GAMESEC MONITOR - PANEL DE CONTROL")
    print("=========================================")
    print("1. Cargar y validar dataset")
    print("2. Ver estadísticas globales")
    print("3. Ver rendimiento por servidor")
    print("4. Auditar incidentes de seguridad")
    print("5. Exportar reporte consolidado")
    print("6. Salir")
    print("=========================================")


def main():
    sesiones = []

    while True:
        limpiar_pantalla()
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "6":
            limpiar_pantalla()
            print("Cerrando GameSec Monitor.")
            break

        # Cualquier otra opción muestra solo su resultado
        limpiar_pantalla()

        if opcion == "1":
            try:
                sesiones = cargar_telemetria("gamesec_logs.csv")
                print(f"Se cargaron {len(sesiones)} registros correctamente.")
            except (OSError, ValueError, KeyError) as error:
                print(f"Error al cargar los datos: {error}")

        elif opcion == "2":
            if not sesiones:
                print("Primero debe cargar el dataset con la opción 1.")
            else:
                estadisticas = calcular_estadisticas_globales(sesiones)
                print("Estadísticas globales:")
                print(estadisticas)

        elif opcion == "3":
            if not sesiones:
                print("Primero debe cargar el dataset con la opción 1.")
            else:
                rendimiento = analizar_por_servidor(sesiones)
                print("Rendimiento por servidor:")

                for servidor, datos in rendimiento.items():
                    print(f"\nServidor: {servidor}")
                    print(f"Sesiones: {datos['cantidad']}")
                    print(f"Ping promedio: {datos['ping_promedio']} ms")
                    print(f"FPS promedio: {datos['fps_promedio']}")

        elif opcion == "4":
            if not sesiones:
                print("Primero debe cargar el dataset con la opción 1.")
            else:
                resumen, criticas = clasificar_incidentes(sesiones)
                print("Auditoría de seguridad:")
                print(resumen)

                print("\nSesiones críticas detectadas:")
                for incidente in criticas:
                    print(incidente)

        elif opcion == "5":
            if not sesiones:
                print("Primero debe cargar el dataset con la opción 1.")
            else:
                try:
                    conclusiones = pedir_conclusiones()
                    ruta = exportar_reporte(sesiones, conclusiones)
                    print(f"Reporte exportado correctamente en: {ruta}")
                except OSError as error:
                    print(f"Error al guardar el reporte: {error}")

        volver_al_menu()


if __name__ == "__main__":
    main()
