"""Clase Mantenimiento: registra mantenimientos preventivos/correctivos
y cambia el estado del vehículo."""

from datetime import date
from itertools import count

from excepciones.excepciones import DatosInvalidosException

TIPOS_VALIDOS = {"preventivo", "correctivo"}


class Mantenimiento:
    _contador = count(1)

    def __init__(self, vehiculo, tipo: str, descripcion: str, costo: float,
                 fecha: date = None):
        if tipo.lower() not in TIPOS_VALIDOS:
            raise DatosInvalidosException("tipo", tipo, "debe ser 'preventivo' o 'correctivo'")
        if costo < 0:
            raise DatosInvalidosException("costo", costo, "no puede ser negativo")
        self._codigo = f"MNT-{next(self._contador):04d}"
        self._vehiculo = vehiculo
        self._tipo = tipo.lower()
        self._descripcion = descripcion
        self._costo = costo
        self._fecha = fecha or date.today()
        vehiculo.agregar_mantenimiento(self)
        vehiculo.estado = "mantenimiento"

    @property
    def costo(self) -> float:
        return self._costo

    def finalizar(self) -> None:
        self._vehiculo.estado = "disponible"

    def __str__(self) -> str:
        return (f"{self._codigo} - {self._vehiculo.placa} - {self._tipo} - "
                f"{self._descripcion} - S/ {self._costo:.2f} - {self._fecha}")
