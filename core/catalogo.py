"""Lectura y consultas del catalogo simulado de SoundShop CL."""

from functools import lru_cache
import json
from pathlib import Path
import unicodedata

from .models import Categoria, Producto


RUTA_CATALOGO = Path(__file__).resolve().parent / "data" / "catalogo.json"

CATEGORIAS_EDITORIALES = {
    "audifonos": {
        "imagen": "img/productos/audifonos-pulse-x.webp",
        "imagen_alt": "Audífonos Pulse X ANC",
        "ruta": "Escuchar sin distracciones",
        "titular": "Baja el ruido.",
        "enfasis": "Sube tu música.",
        "sello": "Escucha",
        "introduccion": "Tu disco favorito, una mezcla en proceso o un momento a solas. Encuentra los audífonos que acompañan tu forma de escuchar.",
        "guia_titulo": "Dos maneras de desconectarse.",
        "guia": (
            ("Libertad inalámbrica", "Pulse X ANC combina Bluetooth, conexión por cable y cancelación activa de ruido."),
            ("Conexión directa", "Studio M40 ofrece cable desmontable y formato cerrado para edición y práctica musical."),
        ),
    },
    "tornamesas-vinilos": {
        "imagen": "img/productos/tornamesa-orbit-one.webp",
        "imagen_alt": "Tornamesa Orbit One",
        "ruta": "Volver al ritual del vinilo",
        "titular": "El sonido tiene",
        "enfasis": "otra vuelta.",
        "sello": "33⅓ RPM",
        "introduccion": "Elegir un disco. Bajar la aguja. Escuchar hasta el último surco. Un espacio para disfrutar el vinilo y cuidar la colección.",
        "guia_titulo": "Del primer giro al cuidado del disco.",
        "guia": (
            ("El centro de la colección", "Orbit One reúne tracción por correa, salida RCA y preamplificador conmutable."),
            ("Cuidar cada surco", "Record Care Kit incluye cepillo, líquido y paño. Revisa su disponibilidad antes de comprar."),
        ),
    },
    "estudio-creacion": {
        "imagen": "img/productos/microfono-vela-c1.webp",
        "imagen_alt": "Micrófono Vela C1",
        "ruta": "Grabar y producir en casa",
        "titular": "Esa idea merece",
        "enfasis": "ser escuchada.",
        "sello": "Rec / 01",
        "introduccion": "De una voz a una primera toma. Micrófonos e interfaces para darle un lugar a tus ideas y comenzar a construir tu estudio.",
        "guia_titulo": "Arma tu espacio de creación.",
        "guia": (
            ("Capturar una idea", "Vela C1 es un micrófono de conexión XLR. Su ficha detalla el patrón y la alimentación que necesita."),
            ("Conectar el estudio", "MiniWave 2 incorpora dos entradas combo y conexión USB-C. Compara sus entradas con tu equipo."),
        ),
    },
    "instrumentos": {
        "imagen": "img/productos/guitarra-astra-seven.webp",
        "imagen_alt": "Guitarra eléctrica Astra Seven",
        "ruta": "Tocar y crear nuevas ideas",
        "titular": "Todo empieza",
        "enfasis": "con una nota.",
        "sello": "Play / 07",
        "introduccion": "Una guitarra, unas teclas y una idea propia. Instrumentos para practicar, componer y encontrar un sonido que se sienta tuyo.",
        "guia_titulo": "Elige cómo empieza tu próxima canción.",
        "guia": (
            ("Explorar las cuerdas", "Astra Seven tiene siete cuerdas, dos cápsulas humbucker y puente fijo."),
            ("Crear desde las teclas", "Keyline 49 es un controlador MIDI con teclas sensibles a la velocidad, pads y controles asignables."),
        ),
    },
    "sonido-en-vivo": {
        "imagen": "img/productos/parlante-atlas-10.webp",
        "imagen_alt": "Parlante activo Atlas 10",
        "ruta": "Preparar el escenario",
        "titular": "Haz que llegue",
        "enfasis": "a todos.",
        "sello": "En vivo",
        "introduccion": "El ensayo, la sala y ese primer público. Parlantes y mezcladores para reunir las señales y llevar la música más allá del instrumento.",
        "guia_titulo": "Cada señal tiene su lugar.",
        "guia": (
            ("Dar salida al sonido", "Atlas 10 es un parlante activo de diez pulgadas con mezclador integrado para espacios pequeños."),
            ("Organizar las entradas", "La ficha de MixLab 8 permite revisar sus canales y conexiones antes de sumarlo a tu configuración."),
        ),
    },
}


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
                "numero": len(resultado) + 1,
                "destacado": next((producto for producto in asociados if producto.destacado), asociados[0] if asociados else None),
                **CATEGORIAS_EDITORIALES.get(categoria.slug, {}),
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
