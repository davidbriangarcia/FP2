"""
Jerarquía Vehiculo -> Automovil / Motocicleta.
Demuestra: clase abstracta y polimorfismo real (calcular_tarifa_seguro()
se calcula de forma distinta en cada subclase).
"""

from abc import ABC, abstractmethod

from excepciones.excepciones import DatosInvalidosException


class Vehiculo(ABC):
    """Clase abstracta. Define estado, tarifa diaria y el cálculo de seguro
    (abstracto: cada tipo de vehículo lo implementa a su manera)."""

    ESTADOS_VALIDOS = {"disponible", "alquilado", "mantenimiento"}

    def __init__(self, placa: str, marca: str, modelo: str, tarifa_diaria: float):
        if not placa.strip():
            raise DatosInvalidosException("placa", placa, "no puede estar vacía")
        if tarifa_diaria <= 0:
            raise DatosInvalidosException("tarifa_diaria", tarifa_diaria, "debe ser mayor a 0")
        self._placa = placa.upper().strip()
        self._marca = marca
        self._modelo = modelo
        self._tarifa_diaria = tarifa_diaria
        self._estado = "disponible"
        self._historial_mantenimientos = []  # colección

    @property
    def placa(self) -> str:
        return self._placa

    @property
    def tarifa_diaria(self) -> float:
        return self._tarifa_diaria

    @property
    def estado(self) -> str:
        return self._estado

    @estado.setter
    def estado(self, nuevo_estado: str) -> None:
        if nuevo_estado not in self.ESTADOS_VALIDOS:
            raise DatosInvalidosException("estado", nuevo_estado, "no es un estado válido")
        self._estado = nuevo_estado

    @property
    def historial_mantenimientos(self) -> list:
        return self._historial_mantenimientos

    def agregar_mantenimiento(self, mantenimiento) -> None:
        self._historial_mantenimientos.append(mantenimiento)

    def esta_disponible(self) -> bool:
        return self._estado == "disponible"

    @abstractmethod
    def calcular_tarifa_seguro(self) -> float:
        """Cálculo específico exigido por la rúbrica. Cada subclase lo redefine:
        esto es el ejemplo de polimorfismo pedido en el enunciado."""
        raise NotImplementedError

    def calcular_costo_alquiler(self, dias: int) -> float:
        if dias <= 0:
            raise DatosInvalidosException("dias", dias, "debe ser mayor a 0")
        return round((self._tarifa_diaria * dias) + self.calcular_tarifa_seguro(), 2)

    def __str__(self) -> str:
        return (f"{self._marca} {self._modelo} (Placa {self._placa}) - "
                f"Estado: {self._estado} - Tarifa diaria: S/ {self._tarifa_diaria:.2f}")


class Automovil(Vehiculo):
    """Hereda de Vehiculo. Redefine el cálculo de la tarifa de seguro."""

    def __init__(self, placa: str, marca: str, modelo: str, tarifa_diaria: float,
                 num_puertas: int, categoria: str = "sedan"):
        super().__init__(placa, marca, modelo, tarifa_diaria)
        self._num_puertas = num_puertas
        self._categoria = categoria

    def calcular_tarifa_seguro(self) -> float:
        # Seguro para autos: 8% de la tarifa diaria, +S/10 si es categoría SUV.
        base = self._tarifa_diaria * 0.08
        recargo = 10.0 if self._categoria.lower() == "suv" else 0.0
        return round(base + recargo, 2)


class Motocicleta(Vehiculo):
    """Hereda de Vehiculo. Redefine el cálculo de la tarifa de seguro
    según el cilindraje."""

    def __init__(self, placa: str, marca: str, modelo: str, tarifa_diaria: float,
                 cilindraje: int):
        super().__init__(placa, marca, modelo, tarifa_diaria)
        if cilindraje <= 0:
            raise DatosInvalidosException("cilindraje", cilindraje, "debe ser mayor a 0")
        self._cilindraje = cilindraje

    def calcular_tarifa_seguro(self) -> float:
        # Seguro para motos: 5% de la tarifa diaria; +S/5 extra si supera 200cc
        # (motos de mayor cilindraje son más usadas por repartidores y tienen
        # mayor riesgo de siniestro).
        base = self._tarifa_diaria * 0.05
        recargo = 5.0 if self._cilindraje > 200 else 0.0
        return round(base + recargo, 2)
