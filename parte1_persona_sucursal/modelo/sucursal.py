"""Clase Sucursal: agrupa los vehículos y empleados asignados a una sede (agregación)."""

from excepciones.excepciones import DatosInvalidosException


class Sucursal:
    def __init__(self, codigo: str, nombre: str, distrito: str):
        if not codigo.strip():
            raise DatosInvalidosException("codigo", codigo, "no puede estar vacío")
        self._codigo = codigo.upper()
        self._nombre = nombre
        self._distrito = distrito
        self._vehiculos = []   # agregación: la sucursal referencia vehículos,
        self._empleados = []   # pero estos existen de forma independiente.

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def vehiculos(self) -> list:
        return self._vehiculos

    @property
    def empleados(self) -> list:
        return self._empleados

    def asignar_vehiculo(self, vehiculo) -> None:
        if vehiculo not in self._vehiculos:
            self._vehiculos.append(vehiculo)

    def asignar_empleado(self, empleado) -> None:
        if empleado not in self._empleados:
            self._empleados.append(empleado)
            empleado.sucursal = self

    def vehiculos_disponibles(self) -> list:
        return [v for v in self._vehiculos if v.esta_disponible()]

    def __str__(self) -> str:
        return (f"Sucursal {self._nombre} ({self._codigo}) - {self._distrito} - "
                f"{len(self._vehiculos)} vehículo(s), {len(self._empleados)} empleado(s)")
