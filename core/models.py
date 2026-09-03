"""Modelo de datos tipado para el prototipo sin base de datos.

En la Evaluacion 1 los registros se leen desde JSON. Estas dataclasses dejan
explicitos los atributos y tipos que luego pueden migrarse a modelos ORM.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Categoria:
    slug: str
    nombre: str
    descripcion: str
    icono: str


@dataclass(frozen=True, slots=True)
class Producto:
    id: int
    nombre: str
    marca: str
    categoria: str
    descripcion: str
    precio: int
    stock: int
    imagen: str
    destacado: bool = False
    etiquetas: tuple[str, ...] = field(default_factory=tuple)
    especificaciones: dict[str, str] = field(default_factory=dict)

    @property
    def puede_comprarse(self) -> bool:
        return self.stock > 0
