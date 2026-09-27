"""
Jerarquía Persona -> Cliente / Empleado.
Demuestra: clase abstracta, herencia, encapsulamiento y polimorfismo
(el método resumen() se redefine en cada subclase).
"""

from abc import ABC, abstractmethod
from datetime import date

from excepciones.excepciones import DatosInvalidosException


class Persona(ABC):
    """Clase abstracta: atributos y comportamiento comunes a Cliente y Empleado."""

    def __init__(self, dni: str, nombres: str, apellidos: str, telefono: str):
        if not (dni.isdigit() and len(dni) == 8):
            raise DatosInvalidosException("DNI", dni, "debe tener 8 dígitos numéricos")
        if not nombres.strip() or not apellidos.strip():
            raise DatosInvalidosException("nombres/apellidos", f"{nombres} {apellidos}",
                                           "no puede estar vacío")
        self._dni = dni
        self._nombres = nombres.strip().title()
        self._apellidos = apellidos.strip().title()
        self._telefono = telefono

    # --- Propiedades (encapsulamiento) ---
    @property
    def dni(self) -> str:
        return self._dni

    @property
    def nombre_completo(self) -> str:
        return f"{self._nombres} {self._apellidos}"

    @property
    def telefono(self) -> str:
        return self._telefono

    @abstractmethod
    def resumen(self) -> str:
        """Cada subclase debe describirse a sí misma (polimorfismo)."""
        raise NotImplementedError

    def __str__(self) -> str:
        return self.resumen()


class Cliente(Persona):
    """Hereda de Persona. Guarda licencia de conducir e historial de contratos."""

    def __init__(self, dni: str, nombres: str, apellidos: str, telefono: str,
                 licencia_conducir: str, es_repartidor: bool = False):
        super().__init__(dni, nombres, apellidos, telefono)
        if not licencia_conducir.strip():
            raise DatosInvalidosException("licencia_conducir", licencia_conducir,
                                           "no puede estar vacía")
        self._licencia_conducir = licencia_conducir
        self._es_repartidor = es_repartidor
        self._historial_contratos = []  # lista de ContratoAlquiler (colección)

    @property
    def licencia_conducir(self) -> str:
        return self._licencia_conducir

    @property
    def historial_contratos(self) -> list:
        return self._historial_contratos

    def agregar_contrato(self, contrato) -> None:
        self._historial_contratos.append(contrato)

    def es_cliente_frecuente(self, minimo_contratos: int = 3) -> bool:
        return len(self._historial_contratos) >= minimo_contratos

    def resumen(self) -> str:
        tipo = "Repartidor" if self._es_repartidor else "Particular"
        return (f"Cliente {self.nombre_completo} (DNI {self.dni}) - {tipo} - "
                f"Licencia: {self._licencia_conducir} - "
                f"{len(self._historial_contratos)} contrato(s) en historial")


class Empleado(Persona):
    """Hereda de Persona. Calcula el sueldo total según el cargo."""

    # Sueldo base por cargo (regla de negocio simple del caso de estudio)
    SUELDO_BASE_POR_CARGO = {
        "administrador": 3200.0,
        "recepcionista": 1600.0,
        "gerente": 4500.0,
        "tecnico_mantenimiento": 1800.0,
    }
    TASA_ESSALUD = 0.09  # aporte del empleador, referencial

    def __init__(self, dni: str, nombres: str, apellidos: str, telefono: str,
                 cargo: str, fecha_ingreso: date, sucursal=None):
        super().__init__(dni, nombres, apellidos, telefono)
        cargo_normalizado = cargo.strip().lower().replace(" ", "_")
        if cargo_normalizado not in self.SUELDO_BASE_POR_CARGO:
            raise DatosInvalidosException("cargo", cargo, "no es un cargo reconocido")
        self._cargo = cargo_normalizado
        self._fecha_ingreso = fecha_ingreso
        self._sucursal = sucursal

    @property
    def cargo(self) -> str:
        return self._cargo

    @property
    def sucursal(self):
        return self._sucursal

    @sucursal.setter
    def sucursal(self, sucursal) -> None:
        self._sucursal = sucursal

    def calcular_sueldo_total(self) -> float:
        """Cálculo específico exigido por la rúbrica: sueldo base + bonificación
        por antigüedad (2% por año completo trabajado, tope 20%)."""
        base = self.SUELDO_BASE_POR_CARGO[self._cargo]
        anios = max(0, (date.today() - self._fecha_ingreso).days // 365)
        bonificacion = base * min(0.20, 0.02 * anios)
        return round(base + bonificacion, 2)

    def resumen(self) -> str:
        return (f"Empleado {self.nombre_completo} (DNI {self.dni}) - "
                f"Cargo: {self._cargo.replace('_', ' ').title()} - "
                f"Sueldo total: S/ {self.calcular_sueldo_total():.2f}")
