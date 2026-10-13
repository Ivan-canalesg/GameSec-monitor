import os

from procesamiento import (
    calcular_estadisticas_globales,
    analizar_por_servidor,
    clasificar_incidentes
)

from carga import (
    cargar_telemetria
)

from exportacion import (
        exportar_reporte
)



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
                    ruta = exportar_reporte(sesiones)
                    print(f"Reporte exportado correctamente en: {ruta}")
                except OSError as error:
                    print(f"Error al guardar el reporte: {error}")

        volver_al_menu()


if __name__ == "__main__":
    main()
