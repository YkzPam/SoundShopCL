"""Vistas del catalogo y del flujo de compra simulado."""

import secrets

from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .catalogo import (
    calcular_carrito,
    categorias_con_resumen,
    filtrar_productos,
    obtener_categoria,
    obtener_producto,
    productos_destacados,
)
from .forms import CantidadCarritoForm, CantidadProductoForm, FiltroCatalogoForm


def _carrito_sesion(request) -> dict[str, int]:
    carrito = request.session.get("carrito", {})
    return carrito if isinstance(carrito, dict) else {}


def _guardar_carrito(request, carrito: dict[str, int]) -> None:
    request.session["carrito"] = carrito
    request.session.modified = True


def _datos_catalogo(request, categoria_forzada: str = "") -> dict[str, object]:
    datos = request.GET.copy()
    if categoria_forzada:
        datos["categoria"] = categoria_forzada
    formulario = FiltroCatalogoForm(datos or None)
    filtros = {
        "consulta": "",
        "categoria": categoria_forzada,
        "precio_maximo": None,
        "solo_disponibles": False,
        "orden": "destacados",
    }
    if formulario.is_valid():
        filtros = {
            "consulta": formulario.cleaned_data["q"],
            "categoria": categoria_forzada or formulario.cleaned_data["categoria"],
            "precio_maximo": formulario.cleaned_data["precio_maximo"],
            "solo_disponibles": formulario.cleaned_data["solo_disponibles"],
            "orden": formulario.cleaned_data["orden"] or "destacados",
        }
    productos = filtrar_productos(**filtros)
    return {
        "formulario": formulario,
        "productos": productos,
        "cantidad_resultados": len(productos),
        "consulta_activa": filtros["consulta"],
    }


def inicio(request):
    contexto = {
        "productos_destacados": productos_destacados(),
        "resumen_categorias": categorias_con_resumen(),
    }
    return render(request, "core/inicio.html", contexto)


def catalogo(request):
    contexto = _datos_catalogo(request)
    contexto["titulo_catalogo"] = "Explora el catálogo"
    return render(request, "core/catalogo.html", contexto)


def buscar(request):
    contexto = _datos_catalogo(request)
    consulta = contexto["consulta_activa"]
    contexto["titulo_catalogo"] = f'Resultados para “{consulta}”' if consulta else "Buscar productos"
    return render(request, "core/catalogo.html", contexto)


def categorias(request):
    return render(
        request,
        "core/categorias.html",
        {"resumen_categorias": categorias_con_resumen()},
    )


def detalle_categoria(request, slug: str):
    categoria = obtener_categoria(slug)
    if categoria is None:
        messages.warning(request, "La categoría solicitada no existe.")
        return redirect("core:categorias")
    contexto = _datos_catalogo(request, categoria_forzada=slug)
    contexto.update(
        {
            "categoria_actual": categoria,
            "titulo_catalogo": categoria.nombre,
        }
    )
    return render(request, "core/catalogo.html", contexto)


def detalle_producto(request, producto_id: int):
    producto = obtener_producto(producto_id)
    if producto is None:
        messages.warning(request, "El producto solicitado no existe o fue retirado del catálogo.")
        return redirect("core:catalogo")
    contexto = {
        "producto": producto,
        "categoria": obtener_categoria(producto.categoria),
        "formulario_cantidad": CantidadProductoForm(stock=producto.stock),
        "relacionados": [
            item
            for item in filtrar_productos(categoria=producto.categoria)
            if item.id != producto.id
        ][:3],
    }
    return render(request, "core/detalle_producto.html", contexto)


def carrito(request):
    lineas, total, cantidad = calcular_carrito(_carrito_sesion(request))
    contexto = {"lineas": lineas, "total": total, "cantidad": cantidad}
    return render(request, "core/carrito.html", contexto)


@require_POST
def agregar_al_carrito(request, producto_id: int):
    producto = obtener_producto(producto_id)
    if producto is None:
        messages.error(request, "No fue posible encontrar el producto.")
        return redirect("core:catalogo")
    if not producto.puede_comprarse:
        messages.warning(request, f"{producto.nombre} se encuentra temporalmente sin stock.")
        return redirect("core:detalle_producto", producto_id=producto.id)

    formulario = CantidadProductoForm(request.POST, stock=producto.stock)
    if not formulario.is_valid():
        messages.error(request, f"La cantidad debe estar entre 1 y {producto.stock} unidades.")
        return redirect("core:detalle_producto", producto_id=producto.id)

    cantidad = formulario.cleaned_data["cantidad"]
    carrito_actual = _carrito_sesion(request).copy()
    cantidad_nueva = int(carrito_actual.get(str(producto.id), 0)) + cantidad
    if cantidad_nueva > producto.stock:
        messages.warning(request, f"Solo quedan {producto.stock} unidades de {producto.nombre}.")
        return redirect("core:detalle_producto", producto_id=producto.id)

    carrito_actual[str(producto.id)] = cantidad_nueva
    _guardar_carrito(request, carrito_actual)
    messages.success(request, f"{producto.nombre} fue agregado al carrito.")
    return redirect("core:carrito")


@require_POST
def actualizar_carrito(request, producto_id: int):
    producto = obtener_producto(producto_id)
    formulario = CantidadCarritoForm(request.POST)
    if producto is None or not formulario.is_valid():
        messages.error(request, "No fue posible actualizar la cantidad indicada.")
        return redirect("core:carrito")

    cantidad = formulario.cleaned_data["cantidad"]
    carrito_actual = _carrito_sesion(request).copy()
    clave = str(producto.id)
    if cantidad == 0:
        carrito_actual.pop(clave, None)
        messages.info(request, f"{producto.nombre} fue retirado del carrito.")
    elif cantidad > producto.stock:
        messages.warning(request, f"La cantidad supera el stock disponible ({producto.stock}).")
        return redirect("core:carrito")
    else:
        carrito_actual[clave] = cantidad
        messages.success(request, "La cantidad fue actualizada.")
    _guardar_carrito(request, carrito_actual)
    return redirect("core:carrito")


@require_POST
def eliminar_del_carrito(request, producto_id: int):
    producto = obtener_producto(producto_id)
    carrito_actual = _carrito_sesion(request).copy()
    eliminado = carrito_actual.pop(str(producto_id), None)
    _guardar_carrito(request, carrito_actual)
    if eliminado and producto:
        messages.info(request, f"{producto.nombre} fue retirado del carrito.")
    return redirect("core:carrito")


@require_POST
def confirmar_pedido(request):
    lineas, total, cantidad = calcular_carrito(_carrito_sesion(request))
    if not lineas:
        messages.warning(request, "Agrega al menos un producto antes de confirmar el pedido.")
        return redirect("core:carrito")

    ahora = timezone.localtime()
    request.session["ultimo_pedido"] = {
        "codigo": f"SSCL-{ahora:%y%m%d}-{secrets.token_hex(2).upper()}",
        "total": total,
        "cantidad": cantidad,
        "fecha": ahora.strftime("%d-%m-%Y %H:%M"),
    }
    _guardar_carrito(request, {})
    return redirect("core:pedido_confirmado")


def pedido_confirmado(request):
    pedido = request.session.get("ultimo_pedido")
    if not pedido:
        return redirect("core:inicio")
    return render(request, "core/pedido_confirmado.html", {"pedido": pedido})
