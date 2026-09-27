"""
Main: punto de entrada del sistema. Muestra el menú por consola y conecta
al usuario con GestorAlquileres. MotoExpress Perú S.A.C. - Trabajo Parcial
1FIS275 Fundamentos de Programación 2.
"""

from datetime import date, datetime

from excepciones.excepciones import (
    VehiculoNoDisponibleException,
    ClienteNoEncontradoException,
    DatosInvalidosException,
)
from modelo.persona import Cliente, Empleado
from modelo.vehiculo import Automovil, Motocicleta
from modelo.sucursal import Sucursal
from gestion.gestor_alquileres import GestorAlquileres


def leer_fecha(mensaje: str) -> date:
    texto = input(mensaje + " (dd/mm/aaaa): ")
    return datetime.strptime(texto, "%d/%m/%Y").date()


def cargar_datos_demo(gestor: GestorAlquileres) -> None:
    """Carga datos iniciales para que el sistema no arranque vacío."""
    sede = Sucursal("SJL01", "MotoExpress San Juan de Lurigancho", "San Juan de Lurigancho")
    gestor.registrar_sucursal(sede)

    moto1 = Motocicleta("ABC123", "Honda", "CB190R", 45.0, 190)
    moto2 = Motocicleta("XYZ789", "Bajaj", "Boxer 150", 35.0, 150)
    auto1 = Automovil("MOT456", "Toyota", "Yaris", 90.0, 4, categoria="sedan")
    for v in (moto1, moto2, auto1):
        gestor.registrar_vehiculo(v, sede)

    empleado1 = Empleado("70000001", "Ana", "Ramírez", "999111222",
                          "recepcionista", date(2024, 3, 1), sede)
    gestor.registrar_empleado(empleado1)
    sede.asignar_empleado(empleado1)

    cliente1 = Cliente("70000002", "Luis", "Torres", "999222333",
                        "Q12345678", es_repartidor=True)
    gestor.registrar_cliente(cliente1)


def menu_principal() -> None:
    print("=" * 60)
    print(" MOTOEXPRESS PERÚ S.A.C. - Sistema de Gestión de Alquiler")
    print("=" * 60)
    print("1. Registrar cliente")
    print("2. Buscar vehículos disponibles")
    print("3. Crear reserva y generar contrato")
    print("4. Registrar devolución de vehículo")
    print("5. Registrar pago y emitir factura")
    print("6. Registrar mantenimiento de vehículo")
    print("7. Listar clientes frecuentes")
    print("8. Reporte de ingresos")
    print("9. Listar clientes / vehículos")
    print("0. Salir")


def ejecutar() -> None:
    gestor = GestorAlquileres()
    cargar_datos_demo(gestor)

    while True:
        menu_principal()
        opcion = input("Elija una opción: ").strip()
        try:
            if opcion == "1":
                dni = input("DNI (8 dígitos): ")
                nombres = input("Nombres: ")
                apellidos = input("Apellidos: ")
                telefono = input("Teléfono: ")
                licencia = input("N° de licencia de conducir: ")
                cliente = Cliente(dni, nombres, apellidos, telefono, licencia)
                gestor.registrar_cliente(cliente)
                print("Cliente registrado correctamente:", cliente)

            elif opcion == "2":
                tipo = input("Tipo (Automovil/Motocicleta) o Enter para todos: ").strip()
                disponibles = gestor.buscar_vehiculos_disponibles(tipo or None)
                if not disponibles:
                    print("No hay vehículos disponibles con ese criterio.")
                for v in disponibles:
                    print(" -", v)

            elif opcion == "3":
                dni = input("DNI del cliente: ")
                placa = input("Placa del vehículo: ")
                fecha_inicio = leer_fecha("Fecha de inicio")
                fecha_fin = leer_fecha("Fecha de fin")
                reserva = gestor.crear_reserva(dni, placa, fecha_inicio, fecha_fin)
                contrato = gestor.generar_contrato(reserva)
                print("Reserva y contrato generados:", contrato)

            elif opcion == "4":
                codigo = input("Código de contrato (ej. CTR-0001): ")
                fecha_devolucion = leer_fecha("Fecha real de devolución")
                danos = input("Daños (ninguno/leve/moderado/grave): ") or "ninguno"
                contrato = gestor.registrar_devolucion(codigo, fecha_devolucion, danos)
                print("Devolución registrada. Penalidad: S/", contrato.penalidad,
                      "- Total a cobrar: S/", contrato.costo_total())

            elif opcion == "5":
                codigo = input("Código de contrato: ")
                contrato = next((c for c in gestor._contratos if c.codigo == codigo), None)
                if contrato is None:
                    raise DatosInvalidosException("codigo_contrato", codigo, "no existe")
                monto = float(input("Monto a pagar: "))
                metodo = input("Método de pago (efectivo/tarjeta/yape/plin/transferencia): ")
                gestor.registrar_pago(contrato, monto, metodo)
                factura = gestor.emitir_factura(contrato)
                print("Factura emitida:", factura)

            elif opcion == "6":
                placa = input("Placa del vehículo: ")
                vehiculo = next((v for v in gestor.listar_vehiculos() if v.placa == placa.upper()), None)
                if vehiculo is None:
                    raise VehiculoNoDisponibleException(placa, "no existe en el sistema")
                tipo = input("Tipo (preventivo/correctivo): ")
                descripcion = input("Descripción: ")
                costo = float(input("Costo: "))
                mantenimiento = gestor.registrar_mantenimiento(vehiculo, tipo, descripcion, costo)
                print("Mantenimiento registrado:", mantenimiento)

            elif opcion == "7":
                for c in gestor.listar_clientes_frecuentes():
                    print(" -", c)

            elif opcion == "8":
                print("Ingresos totales: S/", gestor.reporte_ingresos_totales())
                for placa, monto in gestor.reporte_ingresos_por_vehiculo().items():
                    print(f"  {placa}: S/ {monto:.2f}")

            elif opcion == "9":
                print("--- Clientes ---")
                for c in gestor.listar_clientes():
                    print(" -", c)
                print("--- Vehículos ---")
                for v in gestor.listar_vehiculos():
                    print(" -", v)

            elif opcion == "0":
                print("Gracias por usar el sistema MotoExpress. Hasta pronto.")
                break

            else:
                print("Opción no válida, intente nuevamente.")

        except (VehiculoNoDisponibleException, ClienteNoEncontradoException,
                DatosInvalidosException) as e:
            # El sistema captura la excepción y muestra un mensaje claro,
            # sin detener la ejecución (requisito del enunciado).
            print(f"\n[ERROR] {e}\n")
        except ValueError:
            print("\n[ERROR] El dato ingresado no tiene el formato esperado.\n")


if __name__ == "__main__":
    ejecutar()
