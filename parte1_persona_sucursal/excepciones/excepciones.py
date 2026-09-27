"""
Excepciones personalizadas del sistema de gestión de alquiler de vehículos
MotoExpress Perú S.A.C.
"""


class VehiculoNoDisponibleException(Exception):
    """Se lanza cuando se intenta reservar o alquilar un vehículo que
    no está disponible (ya alquilado, en mantenimiento, etc.)."""

    def __init__(self, placa: str, motivo: str = "no está disponible"):
        self.placa = placa
        self.motivo = motivo
        super().__init__(f"El vehículo con placa '{placa}' {motivo}.")


class ClienteNoEncontradoException(Exception):
    """Se lanza cuando se busca un cliente por DNI y no existe en el sistema."""

    def __init__(self, dni: str):
        self.dni = dni
        super().__init__(f"No se encontró ningún cliente con DNI '{dni}'.")


class DatosInvalidosException(Exception):
    """Se lanza cuando un dato ingresado no cumple con el formato o rango esperado
    (DNI, placa, fechas, montos, etc.)."""

    def __init__(self, campo: str, valor, detalle: str = "no es válido"):
        self.campo = campo
        self.valor = valor
        super().__init__(f"El valor '{valor}' para el campo '{campo}' {detalle}.")
