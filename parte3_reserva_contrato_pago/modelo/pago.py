"""Clases Pago y Factura.
Pago: registra un pago asociado a un contrato.
Factura: genera el comprobante con subtotal, IGV (18%) y total.
"""

from datetime import date
from itertools import count

from excepciones.excepciones import DatosInvalidosException

IGV = 0.18
METODOS_VALIDOS = {"efectivo", "tarjeta", "yape", "plin", "transferencia"}


class Pago:
    _contador = count(1)

    def __init__(self, contrato, monto: float, metodo: str, fecha: date = None):
        if monto <= 0:
            raise DatosInvalidosException("monto", monto, "debe ser mayor a 0")
        if metodo.lower() not in METODOS_VALIDOS:
            raise DatosInvalidosException("metodo", metodo, "no es un método de pago válido")
        self._codigo = f"PAG-{next(self._contador):04d}"
        self._contrato = contrato
        self._monto = monto
        self._metodo = metodo.lower()
        self._fecha = fecha or date.today()

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def monto(self) -> float:
        return self._monto

    @property
    def contrato(self):
        return self._contrato

    def __str__(self) -> str:
        return f"{self._codigo} - S/ {self._monto:.2f} ({self._metodo}) - {self._fecha}"


class Factura:
    _contador = count(1)

    def __init__(self, contrato, pagos: list):
        self._numero = f"F001-{next(self._contador):05d}"
        self._contrato = contrato
        self._pagos = pagos
        self._subtotal = round(contrato.costo_total() / (1 + IGV), 2)
        self._igv = round(contrato.costo_total() - self._subtotal, 2)
        self._total = contrato.costo_total()

    @property
    def numero(self) -> str:
        return self._numero

    @property
    def total(self) -> float:
        return self._total

    def esta_pagada(self) -> bool:
        return round(sum(p.monto for p in self._pagos), 2) >= self._total

    def __str__(self) -> str:
        return (f"Factura {self._numero} - Subtotal: S/ {self._subtotal:.2f} - "
                f"IGV: S/ {self._igv:.2f} - Total: S/ {self._total:.2f} - "
                f"Pagada: {'Sí' if self.esta_pagada() else 'No'}")
