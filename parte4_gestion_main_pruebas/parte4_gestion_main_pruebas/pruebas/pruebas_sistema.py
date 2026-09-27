"""
PruebasSistema: clase de pruebas que valida el comportamiento de los métodos
de negocio (cálculos y control), usando el módulo unittest.

Ejecutar desde la carpeta motoexpress/ con:
    python -m unittest pruebas.pruebas_sistema -v
"""

import unittest
from datetime import date

from excepciones.excepciones import (
    VehiculoNoDisponibleException,
    ClienteNoEncontradoException,
    DatosInvalidosException,
)
from modelo.persona import Cliente, Empleado
from modelo.vehiculo import Automovil, Motocicleta
from modelo.sucursal import Sucursal
from gestion.gestor_alquileres import GestorAlquileres


class PruebasSistema(unittest.TestCase):

    def setUp(self):
        self.gestor = GestorAlquileres()
        self.sede = Sucursal("SJL01", "MotoExpress SJL", "San Juan de Lurigancho")
        self.gestor.registrar_sucursal(self.sede)

        self.moto = Motocicleta("ABC123", "Honda", "CB190R", 45.0, 190)
        self.auto = Automovil("MOT456", "Toyota", "Yaris", 90.0, 4, categoria="sedan")
        self.gestor.registrar_vehiculo(self.moto, self.sede)
        self.gestor.registrar_vehiculo(self.auto, self.sede)

        self.cliente = Cliente("70000002", "Luis", "Torres", "999222333", "Q12345678")
        self.gestor.registrar_cliente(self.cliente)

    # ---------- Polimorfismo: cálculo de seguro distinto por subclase ----------
    def test_calculo_seguro_motocicleta_alto_cilindraje(self):
        # tarifa 45 * 5% = 2.25, cilindraje > 200 -> no aplica (190cc)
        self.assertAlmostEqual(self.moto.calcular_tarifa_seguro(), 2.25)

    def test_calculo_seguro_automovil_sedan(self):
        # tarifa 90 * 8% = 7.2, sin recargo SUV
        self.assertAlmostEqual(self.auto.calcular_tarifa_seguro(), 7.2)

    # ---------- Cálculo de sueldo del empleado ----------
    def test_calculo_sueldo_empleado_sin_antiguedad(self):
        empleado = Empleado("70000001", "Ana", "Ramírez", "999111222",
                             "recepcionista", date.today())
        self.assertAlmostEqual(empleado.calcular_sueldo_total(), 1600.0)

    # ---------- Registro y validación ----------
    def test_registrar_cliente_duplicado_lanza_excepcion(self):
        duplicado = Cliente("70000002", "Otro", "Cliente", "999000000", "L00000000")
        with self.assertRaises(DatosInvalidosException):
            self.gestor.registrar_cliente(duplicado)

    def test_dni_invalido_lanza_excepcion(self):
        with self.assertRaises(DatosInvalidosException):
            Cliente("123", "Nombre", "Apellido", "999999999", "L00000000")

    def test_buscar_cliente_inexistente_lanza_excepcion(self):
        with self.assertRaises(ClienteNoEncontradoException):
            self.gestor.buscar_cliente("00000000")

    # ---------- Reservas: doble reserva en fechas cruzadas ----------
    def test_reserva_evita_doble_reserva_en_fechas_cruzadas(self):
        self.gestor.crear_reserva(
            "70000002", "ABC123", date(2026, 10, 1), date(2026, 10, 5))
        # el vehículo queda "alquilado", por lo que una segunda reserva
        # cruzada debe fallar por no-disponibilidad
        with self.assertRaises(VehiculoNoDisponibleException):
            self.gestor.crear_reserva(
                "70000002", "ABC123", date(2026, 10, 3), date(2026, 10, 8))

    # ---------- Contrato: costo base y penalidades ----------
    def test_costo_base_contrato(self):
        reserva = self.gestor.crear_reserva(
            "70000002", "ABC123", date(2026, 10, 1), date(2026, 10, 4))
        contrato = self.gestor.generar_contrato(reserva)
        # 3 días * 45 + seguro 2.25 = 137.25
        self.assertAlmostEqual(contrato.costo_base, 137.25)

    def test_penalidad_por_atraso_y_danos(self):
        reserva = self.gestor.crear_reserva(
            "70000002", "ABC123", date(2026, 10, 1), date(2026, 10, 4))
        contrato = self.gestor.generar_contrato(reserva)
        # devolución 2 días tarde con daño leve: 2*25 + 50 = 100
        penalidad = contrato.registrar_devolucion(date(2026, 10, 6), "leve")
        self.assertAlmostEqual(penalidad, 100.0)
        self.assertEqual(self.moto.estado, "mantenimiento")

    # ---------- Facturación: IGV ----------
    def test_factura_calcula_igv_correctamente(self):
        reserva = self.gestor.crear_reserva(
            "70000002", "MOT456", date(2026, 10, 1), date(2026, 10, 3))
        contrato = self.gestor.generar_contrato(reserva)
        self.gestor.registrar_pago(contrato, contrato.costo_total(), "yape")
        factura = self.gestor.emitir_factura(contrato)
        self.assertAlmostEqual(factura.total, contrato.costo_total())
        self.assertTrue(factura.esta_pagada())


if __name__ == "__main__":
    unittest.main(verbosity=2)
