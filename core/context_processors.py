"""Variables disponibles en todas las plantillas."""

from .catalogo import calcular_carrito, obtener_categorias


def datos_globales(request):
    carrito = request.session.get("carrito", {})
    _, _, cantidad = calcular_carrito(carrito if isinstance(carrito, dict) else {})
    return {
        "categorias_globales": obtener_categorias(),
        "cantidad_carrito": cantidad,
    }
