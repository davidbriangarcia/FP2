"""Clase Reserva: solicitud de alquiler de un cliente sobre un vehículo,
en un rango de fechas (asociación Cliente - Vehiculo)."""

from datetime import date
from itertools import count

from excepciones.excepciones import DatosInvalidosException


class Reserva:
    _contador = count(1)  # genera códigos de reserva correlativos

    def __init__(self, cliente, vehiculo, fecha_inicio: date, fecha_fin: date):
        if fecha_fin <= fecha_inicio:
            raise DatosInvalidosException(
                "fecha_fin", fecha_fin, "debe ser posterior a la fecha de inicio")
        self._codigo = f"RES-{next(self._contador):04d}"
        self._cliente = cliente
        self._vehiculo = vehiculo
        self._fecha_inicio = fecha_inicio
        self._fecha_fin = fecha_fin
        self._estado = "pendiente"  # pendiente | confirmada | cancelada

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def cliente(self):
        return self._cliente

    @property
    def vehiculo(self):
        return self._vehiculo

    @property
    def estado(self) -> str:
        return self._estado

    @estado.setter
    def estado(self, valor: str) -> None:
        self._estado = valor

    def dias_reservados(self) -> int:
        return (self._fecha_fin - self._fecha_inicio).days

    def se_cruza_con(self, otra_reserva) -> bool:
        """Evita la doble reserva de un mismo vehículo en fechas que se cruzan
        (problema detectado en el Capítulo 1 del informe)."""
        if self._vehiculo.placa != otra_reserva.vehiculo.placa:
            return False
        return (self._fecha_inicio < otra_reserva._fecha_fin and
                otra_reserva._fecha_inicio < self._fecha_fin)

    def __str__(self) -> str:
        return (f"{self._codigo} - {self._cliente.nombre_completo} / "
                f"{self._vehiculo.placa} - {self._fecha_inicio} a {self._fecha_fin} "
                f"({self._estado})")
