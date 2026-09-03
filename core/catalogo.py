"""Lectura y consultas del catalogo simulado de SoundShop CL."""

from functools import lru_cache
import json
from pathlib import Path
import unicodedata

from .models import Categoria, Producto


RUTA_CATALOGO = Path(__file__).resolve().parent / "data" / "catalogo.json"


def _normalizar(texto: object) -> str:
    valor = unicodedata.normalize("NFD", str(texto).casefold())
    return "".join(caracter for caracter in valor if unicodedata.category(caracter) != "Mn")


@lru_cache(maxsize=1)
def cargar_catalogo() -> tuple[tuple[Categoria, ...], tuple[Producto, ...]]:
    """Convierte el JSON local en objetos tipados e inmutables."""

    with RUTA_CATALOGO.open(encoding="utf-8") as archivo:
        datos = json.load(archivo)

    categorias = tuple(Categoria(**item) for item in datos["categorias"])
    productos = tuple(
        Producto(
            id=item["id"],
            nombre=item["nombre"],
            marca=item["marca"],
            categoria=item["categoria"],
            descripcion=item["descripcion"],
            precio=item["precio"],
            stock=item["stock"],
            imagen=item["imagen"],
            destacado=item.get("destacado", False),
            etiquetas=tuple(item.get("etiquetas", [])),
            especificaciones=item.get("especificaciones", {}),
        )
        for item in datos["productos"]
    )
    return categorias, productos


def obtener_categorias() -> tuple[Categoria, ...]:
    return cargar_catalogo()[0]


def obtener_productos() -> tuple[Producto, ...]:
    return cargar_catalogo()[1]


def obtener_producto(producto_id: int) -> Producto | None:
    return next((producto for producto in obtener_productos() if producto.id == producto_id), None)


def obtener_categoria(slug: str) -> Categoria | None:
    return next((categoria for categoria in obtener_categorias() if categoria.slug == slug), None)


def productos_destacados() -> tuple[Producto, ...]:
    return tuple(producto for producto in obtener_productos() if producto.destacado)


def filtrar_productos(
    consulta: str = "",
    categoria: str = "",
    precio_maximo: int | None = None,
    solo_disponibles: bool = False,
    orden: str = "destacados",
) -> list[Producto]:
    productos = list(obtener_productos())

    if consulta:
        termino = _normalizar(consulta)
        productos = [
            producto
            for producto in productos
            if termino
            in _normalizar(
                " ".join(
                    [
                        producto.nombre,
                        producto.marca,
                        producto.descripcion,
                        *producto.etiquetas,
                        *producto.especificaciones.values(),
                    ]
                )
            )
        ]

    if categoria:
        productos = [producto for producto in productos if producto.categoria == categoria]
    if precio_maximo is not None:
        productos = [producto for producto in productos if producto.precio <= precio_maximo]
    if solo_disponibles:
        productos = [producto for producto in productos if producto.puede_comprarse]

    ordenamientos = {
        "precio_asc": lambda producto: producto.precio,
        "precio_desc": lambda producto: -producto.precio,
        "nombre": lambda producto: _normalizar(producto.nombre),
        "destacados": lambda producto: (not producto.destacado, producto.id),
    }
    productos.sort(key=ordenamientos.get(orden, ordenamientos["destacados"]))
    return productos


def categorias_con_resumen() -> list[dict[str, object]]:
    resultado = []
    productos = obtener_productos()
    for categoria in obtener_categorias():
        asociados = [producto for producto in productos if producto.categoria == categoria.slug]
        resultado.append(
            {
                "categoria": categoria,
                "cantidad": len(asociados),
                "disponibles": sum(producto.puede_comprarse for producto in asociados),
                "precio_desde": min((producto.precio for producto in asociados), default=0),
            }
        )
    return resultado


def calcular_carrito(carrito: dict[str, int]) -> tuple[list[dict[str, object]], int, int]:
    lineas: list[dict[str, object]] = []
    total = 0
    cantidad_total = 0

    for producto_id, cantidad_bruta in carrito.items():
        try:
            producto = obtener_producto(int(producto_id))
            cantidad = int(cantidad_bruta)
        except (TypeError, ValueError):
            continue
        if producto is None or cantidad < 1:
            continue

        cantidad = min(cantidad, producto.stock) if producto.stock else 0
        if cantidad == 0:
            continue
        subtotal = producto.precio * cantidad
        lineas.append({"producto": producto, "cantidad": cantidad, "subtotal": subtotal})
        total += subtotal
        cantidad_total += cantidad

    return lineas, total, cantidad_total
