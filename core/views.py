"""Vistas del catálogo, el carrito y la cuenta de usuario."""

import secrets

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.templatetags.static import static
from django.urls import reverse
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .catalogo import (
    calcular_carrito,
    categorias_con_resumen,
    filtrar_productos,
    obtener_categoria,
    obtener_producto,
    obtener_productos,
    productos_destacados,
)
from .forms import (
    CantidadCarritoForm,
    CantidadProductoForm,
    FiltroCatalogoForm,
    RegistroForm,
)


def _carrito_sesion(request) -> dict[str, int]:
    carrito = request.session.get("carrito", {})
    return carrito if isinstance(carrito, dict) else {}


def _guardar_carrito(request, carrito: dict[str, int]) -> None:
    request.session["carrito"] = carrito
    request.session.modified = True


def _usuario_sesion(request) -> dict[str, str]:
    usuario = request.session.get("usuario_tienda", {})
    if not isinstance(usuario, dict) or not usuario.get("nombre"):
        return {}
    return usuario


def _destino_seguro(request, destino: str, alternativa: str) -> str:
    if destino and url_has_allowed_host_and_scheme(
        destino,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return destino
    return alternativa


def _solicitud_ajax(request) -> bool:
    return request.headers.get("X-Requested-With") == "XMLHttpRequest"


def _precio_clp(valor: int) -> str:
    return f"${valor:,}".replace(",", ".")


def _respuesta_carrito_json(
    request,
    mensaje: str,
    *,
    ok: bool,
    estado: int = 200,
    producto_agregado=None,
    cantidad_agregada: int = 0,
    requiere_sesion: bool = False,
    registro_url: str = "",
):
    lineas, total, cantidad = calcular_carrito(_carrito_sesion(request))
    datos_lineas = [
        {
            "id": linea["producto"].id,
            "nombre": linea["producto"].nombre,
            "marca": linea["producto"].marca,
            "cantidad": linea["cantidad"],
            "subtotal": linea["subtotal"],
            "subtotal_formateado": _precio_clp(linea["subtotal"]),
            "imagen": static(linea["producto"].imagen),
            "detalle_url": reverse("core:detalle_producto", args=[linea["producto"].id]),
        }
        for linea in lineas
    ]
    agregado = None
    if producto_agregado is not None:
        cantidad_en_carrito = next(
            (
                linea["cantidad"]
                for linea in lineas
                if linea["producto"].id == producto_agregado.id
            ),
            0,
        )
        agregado = {
            "id": producto_agregado.id,
            "nombre": producto_agregado.nombre,
            "imagen": static(producto_agregado.imagen),
            "cantidad_agregada": cantidad_agregada,
            "cantidad_en_carrito": cantidad_en_carrito,
            "subtotal_formateado": _precio_clp(producto_agregado.precio * cantidad_en_carrito),
        }
    return JsonResponse(
        {
            "ok": ok,
            "mensaje": mensaje,
            "cantidad": cantidad,
            "total": total,
            "total_formateado": _precio_clp(total),
            "lineas": datos_lineas,
            "producto_agregado": agregado,
            "requiere_sesion": requiere_sesion,
            "registro_url": registro_url or reverse("core:registro"),
        },
        status=estado,
    )


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
        "cantidad_productos": len(obtener_productos()),
        "registro_formulario": RegistroForm(),
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
        mensaje = "No fue posible encontrar el producto."
        if _solicitud_ajax(request):
            return _respuesta_carrito_json(request, mensaje, ok=False, estado=404)
        messages.error(request, mensaje)
        return redirect("core:catalogo")
    if not _usuario_sesion(request):
        mensaje = "Inicia sesión para agregar productos al carrito."
        if _solicitud_ajax(request):
            siguiente = reverse("core:detalle_producto", args=[producto.id])
            return _respuesta_carrito_json(
                request,
                mensaje,
                ok=False,
                estado=401,
                requiere_sesion=True,
                registro_url=f'{reverse("core:registro")}?next={siguiente}',
            )
        messages.warning(request, mensaje)
        siguiente = reverse("core:detalle_producto", args=[producto.id])
        return redirect(f'{reverse("core:registro")}?next={siguiente}')
    if not producto.puede_comprarse:
        mensaje = f"{producto.nombre} se encuentra temporalmente sin stock."
        if _solicitud_ajax(request):
            return _respuesta_carrito_json(request, mensaje, ok=False, estado=400)
        messages.warning(request, mensaje)
        return redirect("core:detalle_producto", producto_id=producto.id)

    formulario = CantidadProductoForm(request.POST, stock=producto.stock)
    if not formulario.is_valid():
        mensaje = f"La cantidad debe estar entre 1 y {producto.stock} unidades."
        if _solicitud_ajax(request):
            return _respuesta_carrito_json(request, mensaje, ok=False, estado=400)
        messages.error(request, mensaje)
        return redirect("core:detalle_producto", producto_id=producto.id)

    cantidad = formulario.cleaned_data["cantidad"]
    carrito_actual = _carrito_sesion(request).copy()
    cantidad_nueva = int(carrito_actual.get(str(producto.id), 0)) + cantidad
    if cantidad_nueva > producto.stock:
        mensaje = f"Solo quedan {producto.stock} unidades de {producto.nombre}."
        if _solicitud_ajax(request):
            return _respuesta_carrito_json(request, mensaje, ok=False, estado=400)
        messages.warning(request, mensaje)
        return redirect("core:detalle_producto", producto_id=producto.id)

    carrito_actual[str(producto.id)] = cantidad_nueva
    _guardar_carrito(request, carrito_actual)
    mensaje = f"{producto.nombre} fue agregado al carrito."
    if _solicitud_ajax(request):
        return _respuesta_carrito_json(
            request,
            mensaje,
            ok=True,
            producto_agregado=producto,
            cantidad_agregada=cantidad,
        )
    messages.success(request, mensaje)
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
    if not _usuario_sesion(request):
        messages.warning(request, "Inicia sesión antes de confirmar tu pedido.")
        return redirect(f'{reverse("core:registro")}?next={reverse("core:carrito")}')

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


def registro(request):
    formulario = RegistroForm(request.POST or None)
    siguiente_solicitado = request.POST.get("next", request.GET.get("next", ""))
    siguiente = _destino_seguro(request, siguiente_solicitado, "")
    if request.method == "POST" and formulario.is_valid():
        nombre = formulario.cleaned_data["nombre"].strip().split()[0]
        request.session["usuario_tienda"] = {"nombre": nombre}
        request.session.modified = True
        messages.success(request, f"Cuenta creada y sesión iniciada. Bienvenido, {nombre}.")
        if siguiente:
            return redirect(siguiente)
        return redirect("core:registro_confirmado")
    return render(
        request,
        "core/registro.html",
        {"registro_formulario": formulario, "siguiente": siguiente},
    )


def registro_confirmado(request):
    usuario = request.session.get("usuario_tienda")
    if not isinstance(usuario, dict) or not usuario.get("nombre"):
        return redirect("core:registro")
    return render(request, "core/registro_confirmado.html", {"usuario": usuario})


@require_POST
def cerrar_sesion(request):
    request.session.pop("usuario_tienda", None)
    request.session.modified = True
    messages.info(request, "La sesión se cerró correctamente.")
    return redirect("core:inicio")
