"""Clase ContratoAlquiler: calcula el costo base, registra la devolución
y calcula penalidades por atraso o daños."""

from datetime import date
from itertools import count

from excepciones.excepciones import DatosInvalidosException

PENALIDAD_POR_DIA_ATRASO = 25.0
PENALIDAD_POR_DANO = {"leve": 50.0, "moderado": 150.0, "grave": 400.0}


class ContratoAlquiler:
    _contador = count(1)

    def __init__(self, reserva):
        self._codigo = f"CTR-{next(self._contador):04d}"
        self._reserva = reserva
        self._cliente = reserva.cliente
        self._vehiculo = reserva.vehiculo
        self._fecha_devolucion_real = None
        self._costo_base = self._vehiculo.calcular_costo_alquiler(reserva.dias_reservados())
        self._penalidad = 0.0
        self._danos = "ninguno"

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def cliente(self):
        return self._cliente

    @property
    def costo_base(self) -> float:
        return self._costo_base

    @property
    def penalidad(self) -> float:
        return self._penalidad

    def registrar_devolucion(self, fecha_devolucion_real: date, danos: str = "ninguno") -> float:
        """Registra la devolución del vehículo y calcula penalidades por
        atraso y/o daños. Devuelve el monto total de la penalidad."""
        self._fecha_devolucion_real = fecha_devolucion_real
        fecha_pactada = self._reserva._fecha_fin
        dias_atraso = max(0, (fecha_devolucion_real - fecha_pactada).days)

        penalidad_atraso = dias_atraso * PENALIDAD_POR_DIA_ATRASO
        danos_normalizado = danos.strip().lower()
        if danos_normalizado not in PENALIDAD_POR_DANO and danos_normalizado != "ninguno":
            raise DatosInvalidosException("danos", danos, "no es un nivel de daño reconocido")
        penalidad_danos = PENALIDAD_POR_DANO.get(danos_normalizado, 0.0)

        self._danos = danos_normalizado
        self._penalidad = round(penalidad_atraso + penalidad_danos, 2)
        self._vehiculo.estado = "mantenimiento" if danos_normalizado != "ninguno" else "disponible"
        return self._penalidad

    def costo_total(self) -> float:
        return round(self._costo_base + self._penalidad, 2)

    def __str__(self) -> str:
        return (f"{self._codigo} - {self._cliente.nombre_completo} - "
                f"Base: S/ {self._costo_base:.2f} - Penalidad: S/ {self._penalidad:.2f} - "
                f"Total: S/ {self.costo_total():.2f}")
