"""
GestorAlquileres: clase de control que administra las colecciones (listas)
del sistema y coordina toda la lógica de negocio (registro, búsqueda,
listado, reservas, devoluciones, pagos, mantenimientos y reportes).
"""

from datetime import date

from excepciones.excepciones import (
    VehiculoNoDisponibleException,
    ClienteNoEncontradoException,
    DatosInvalidosException,
)
from modelo.reserva import Reserva
from modelo.contrato_alquiler import ContratoAlquiler
from modelo.pago import Pago, Factura
from modelo.mantenimiento import Mantenimiento


class GestorAlquileres:
    def __init__(self):
        self._clientes = []
        self._empleados = []
        self._vehiculos = []
        self._sucursales = []
        self._reservas = []
        self._contratos = []
        self._pagos = []
        self._facturas = []

    # ---------- Registro (control) ----------
    def registrar_cliente(self, cliente) -> None:
        if self.buscar_cliente(cliente.dni, lanzar_error=False):
            raise DatosInvalidosException("dni", cliente.dni, "ya está registrado")
        self._clientes.append(cliente)

    def registrar_empleado(self, empleado) -> None:
        self._empleados.append(empleado)

    def registrar_vehiculo(self, vehiculo, sucursal=None) -> None:
        self._vehiculos.append(vehiculo)
        if sucursal:
            sucursal.asignar_vehiculo(vehiculo)

    def registrar_sucursal(self, sucursal) -> None:
        self._sucursales.append(sucursal)

    # ---------- Búsqueda (control) ----------
    def buscar_cliente(self, dni: str, lanzar_error: bool = True):
        for c in self._clientes:
            if c.dni == dni:
                return c
        if lanzar_error:
            raise ClienteNoEncontradoException(dni)
        return None

    def buscar_vehiculos_disponibles(self, tipo: str = None) -> list:
        disponibles = [v for v in self._vehiculos if v.esta_disponible()]
        if tipo:
            disponibles = [v for v in disponibles if type(v).__name__.lower() == tipo.lower()]
        return disponibles

    # ---------- Listado (control) ----------
    def listar_clientes(self) -> list:
        return list(self._clientes)

    def listar_vehiculos(self) -> list:
        return list(self._vehiculos)

    def listar_clientes_frecuentes(self) -> list:
        return [c for c in self._clientes if c.es_cliente_frecuente()]

    # ---------- Reservas y contratos ----------
    def crear_reserva(self, dni_cliente: str, placa_vehiculo: str,
                       fecha_inicio: date, fecha_fin: date) -> Reserva:
        cliente = self.buscar_cliente(dni_cliente)
        vehiculo = next((v for v in self._vehiculos if v.placa == placa_vehiculo.upper()), None)
        if vehiculo is None:
            raise VehiculoNoDisponibleException(placa_vehiculo, "no existe en el sistema")
        if not vehiculo.esta_disponible():
            raise VehiculoNoDisponibleException(placa_vehiculo)

        nueva = Reserva(cliente, vehiculo, fecha_inicio, fecha_fin)
        for reserva_existente in self._reservas:
            if reserva_existente.estado != "cancelada" and nueva.se_cruza_con(reserva_existente):
                raise VehiculoNoDisponibleException(
                    placa_vehiculo, "ya tiene una reserva en fechas que se cruzan")

        nueva.estado = "confirmada"
        vehiculo.estado = "alquilado"
        self._reservas.append(nueva)
        return nueva

    def generar_contrato(self, reserva: Reserva) -> ContratoAlquiler:
        contrato = ContratoAlquiler(reserva)
        contrato.cliente.agregar_contrato(contrato)
        self._contratos.append(contrato)
        return contrato

    def registrar_devolucion(self, codigo_contrato: str, fecha_devolucion: date,
                              danos: str = "ninguno") -> ContratoAlquiler:
        contrato = next((c for c in self._contratos if c.codigo == codigo_contrato), None)
        if contrato is None:
            raise DatosInvalidosException("codigo_contrato", codigo_contrato,
                                           "no corresponde a ningún contrato registrado")
        contrato.registrar_devolucion(fecha_devolucion, danos)
        return contrato

    # ---------- Pagos y facturación ----------
    def registrar_pago(self, contrato: ContratoAlquiler, monto: float, metodo: str) -> Pago:
        pago = Pago(contrato, monto, metodo)
        self._pagos.append(pago)
        return pago

    def emitir_factura(self, contrato: ContratoAlquiler) -> Factura:
        pagos_del_contrato = [p for p in self._pagos if p.contrato is contrato]
        factura = Factura(contrato, pagos_del_contrato)
        self._facturas.append(factura)
        return factura

    # ---------- Mantenimiento ----------
    def registrar_mantenimiento(self, vehiculo, tipo: str, descripcion: str,
                                 costo: float) -> Mantenimiento:
        return Mantenimiento(vehiculo, tipo, descripcion, costo)

    # ---------- Reportes (cálculos) ----------
    def reporte_ingresos_totales(self) -> float:
        return round(sum(c.costo_total() for c in self._contratos), 2)

    def reporte_ingresos_por_vehiculo(self) -> dict:
        reporte = {}
        for c in self._contratos:
            placa = c._vehiculo.placa
            reporte[placa] = round(reporte.get(placa, 0.0) + c.costo_total(), 2)
        return reporte
