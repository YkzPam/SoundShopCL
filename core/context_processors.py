"""Variables disponibles en todas las plantillas."""

from .catalogo import calcular_carrito, obtener_categorias


def datos_globales(request):
    carrito = request.session.get("carrito", {})
    usuario = request.session.get("usuario_tienda", {})
    if not isinstance(usuario, dict) or not usuario.get("nombre"):
        usuario = {}
    lineas, total, cantidad = calcular_carrito(carrito if isinstance(carrito, dict) else {})
    return {
        "categorias_globales": obtener_categorias(),
        "cantidad_carrito": cantidad,
        "lineas_carrito_global": lineas,
        "total_carrito_global": total,
        "usuario_tienda": usuario,
    }
