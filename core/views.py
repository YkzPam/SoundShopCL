"""Tienda de E2 continuada en E3: autenticación y páginas propias de gestión."""
from datetime import date
from django.contrib import messages
from django.contrib.auth import authenticate, login as iniciar_login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import F, Sum
from django.db.models.deletion import ProtectedError
from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.text import slugify
from .models import Categoria, Marca, Proveedor, Sucursal, Cliente, Producto, Boleta, DetalleBoleta


def producto_datos(producto):
    # Mantiene los mismos nombres de variables que usan las plantillas.
    return {"id": producto.id, "nombre": producto.nombre, "marca": producto.marca.nombre,
            "categoria": producto.categoria.slug, "descripcion": producto.descripcion,
            "precio": producto.precio, "stock": producto.stock, "imagen": producto.imagen}


def datos_catalogo():
    productos = []
    for producto in Producto.objects.filter(activo=True).select_related("marca", "categoria").order_by("id"):
        productos.append(producto_datos(producto))
    return {"productos": productos, "categorias": list(Categoria.objects.values("nombre", "slug", "descripcion"))}


def obtener_producto(producto_id):
    producto = get_object_or_404(Producto, pk=producto_id, activo=True)
    return producto_datos(producto)


def inicio(request):
    productos = Producto.objects.filter(activo=True).select_related("marca", "categoria").order_by("id")[:4]
    return render(request, "core/inicio.html", {"productos": [producto_datos(p) for p in productos], "titulo": "Inicio"})


def catalogo(request):
    datos = datos_catalogo()
    busqueda = request.GET.get("q", "").strip()
    categoria = request.GET.get("categoria", "")
    productos = []
    for producto in datos["productos"]:
        coincide_texto = busqueda.casefold() in (producto["nombre"] + " " + producto["marca"]).casefold()
        coincide_categoria = not categoria or producto["categoria"] == categoria
        if coincide_texto and coincide_categoria:
            productos.append(producto)
    contexto = {"productos": productos, "categorias": datos["categorias"], "busqueda": busqueda,
                "categoria_actual": categoria, "titulo": "Productos"}
    return render(request, "core/catalogo.html", contexto)


def detalle_producto(request, producto_id):
    producto = obtener_producto(producto_id)
    return render(request, "core/detalle.html", {"producto": producto, "titulo": producto["nombre"]})


def categorias(request):
    datos = datos_catalogo()
    for categoria in datos["categorias"]:
        productos = [p for p in datos["productos"] if p["categoria"] == categoria["slug"]]
        categoria["cantidad"] = len(productos)
        categoria["imagen"] = productos[0]["imagen"] if productos else ""
    return render(request, "core/categorias.html", {"categorias": datos["categorias"], "titulo": "Categorías"})


def nosotros(request):
    return render(request, "core/nosotros.html", {"titulo": "Nosotros"})


def login(request, acceso_admin=False):
    siguiente = request.POST.get("next") or request.GET.get("next", "")
    if not url_has_allowed_host_and_scheme(siguiente, {request.get_host()}, require_https=request.is_secure()):
        siguiente = ""
    if request.user.is_authenticated:
        return redirect(siguiente or "core:gestion")
    error = ""
    if request.method == "POST":
        usuario = authenticate(request, username=request.POST.get("username", ""), password=request.POST.get("password", ""))
        if usuario is not None:
            iniciar_login(request, usuario)
            return redirect(siguiente or "core:gestion")
        error = "El usuario o la contraseña no son correctos."
    return render(request, "core/login.html", {"titulo": "Iniciar sesión", "error": error,
        "siguiente": siguiente, "nombre_usuario": request.POST.get("username", "")})


def registro(request):
    messages.info(request, "Las cuentas de acceso se crean desde la gestión de usuarios.")
    return redirect("core:login")


@login_required
def salir(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    logout(request)
    return redirect("core:login")


@login_required
def cliente(request):
    return render(request, "core/cliente.html", {"titulo": "Mi cuenta"})


def carrito(request):
    cantidades = request.session.get("carrito", {})
    lineas = []
    total = 0
    for producto in datos_catalogo()["productos"]:
        cantidad = cantidades.get(str(producto["id"]), 0)
        if cantidad:
            subtotal = cantidad * producto["precio"]
            total += subtotal
            lineas.append({"producto": producto, "cantidad": cantidad, "subtotal": subtotal})
    return render(request, "core/carrito.html", {"lineas": lineas, "total": total, "titulo": "Carrito"})


def agregar_carrito(request, producto_id):
    producto = obtener_producto(producto_id)
    if request.method == "POST":
        cantidades = request.session.get("carrito", {})
        clave = str(producto_id)
        cantidad = cantidades.get(clave, 0)
        if cantidad < producto["stock"]:
            cantidades[clave] = cantidad + 1
            request.session["carrito"] = cantidades
            messages.success(request, "Producto agregado al carrito.")
        else:
            messages.warning(request, "No hay más unidades disponibles.")
    return redirect("core:carrito")


def quitar_carrito(request, producto_id):
    if request.method == "POST":
        cantidades = request.session.get("carrito", {})
        cantidades.pop(str(producto_id), None)
        request.session["carrito"] = cantidades
    return redirect("core:carrito")


@login_required
def confirmar(request):
    if request.method != "POST":
        return redirect("core:carrito")
    if not request.session.get("carrito"):
        messages.warning(request, "El carrito está vacío.")
        return redirect("core:carrito")
    request.session["carrito"] = {}
    return render(request, "core/confirmacion.html", {"titulo": "Confirmación"})


def errores_modelo(objeto):
    """Las reglas del modelo también se validan cuando no se utiliza forms.py."""
    try:
        objeto.full_clean()
    except ValidationError as error:
        return error.message_dict
    return {}


@login_required
def gestion(request):
    return render(request, "core/gestion.html", {"titulo": "Panel de administración",
        "total_productos": Producto.objects.count(), "sin_stock": Producto.objects.filter(stock=0).count(),
        "total_clientes": Cliente.objects.count(), "total_ventas": Boleta.objects.count()})


@login_required
def gestion_productos(request):
    productos = Producto.objects.select_related("categoria", "marca").order_by("codigo")
    busqueda = request.GET.get("q", "").strip()
    categoria_id = request.GET.get("categoria", "")
    if busqueda:
        productos = productos.filter(nombre__icontains=busqueda)
    if categoria_id.isdigit():
        productos = productos.filter(categoria_id=categoria_id)
    pagina = Paginator(productos, 25).get_page(request.GET.get("page"))
    return render(request, "core/e3/productos.html", {"titulo": "Productos", "pagina": pagina,
        "categorias": Categoria.objects.order_by("nombre"), "busqueda": busqueda, "categoria_actual": categoria_id})


@login_required
def producto_formulario(request, producto_id=None):
    producto = get_object_or_404(Producto, pk=producto_id) if producto_id else Producto()
    errores = {}
    if request.method == "POST":
        producto.codigo = request.POST.get("codigo", "").strip()
        producto.nombre = request.POST.get("nombre", "").strip()
        producto.descripcion = request.POST.get("descripcion", "").strip()
        producto.precio = request.POST.get("precio", "")
        producto.stock = request.POST.get("stock", "")
        producto.categoria_id = request.POST.get("categoria") or None
        producto.marca_id = request.POST.get("marca") or None
        producto.proveedor_id = request.POST.get("proveedor") or None
        producto.imagen = request.POST.get("imagen", "").strip()
        producto.activo = request.POST.get("activo") == "on"
        errores = errores_modelo(producto)
        if not errores:
            producto.save()
            messages.success(request, "Producto guardado.")
            return redirect("core:gestion_productos")
    return render(request, "core/e3/producto_form.html", {"titulo": "Editar producto" if producto_id else "Nuevo producto",
        "producto": producto, "datos": request.POST if request.method == "POST" else {}, "errores": errores,
        "categorias": Categoria.objects.order_by("nombre"), "marcas": Marca.objects.order_by("nombre"),
        "proveedores": Proveedor.objects.order_by("nombre")})


@login_required
def producto_eliminar(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    if request.method == "POST":
        try:
            producto.delete()
            messages.success(request, "Producto eliminado.")
        except ProtectedError:
            messages.error(request, "El producto está utilizado en ventas o compras. Puede desactivarlo en lugar de borrarlo.")
        return redirect("core:gestion_productos")
    return render(request, "core/e3/confirmar_eliminacion.html", {"titulo": "Eliminar producto", "objeto": producto,
        "volver": "core:gestion_productos"})


@login_required
def gestion_usuarios(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Solo el administrador puede gestionar cuentas de acceso.")
    usuarios = User.objects.order_by("username")
    busqueda = request.GET.get("q", "").strip()
    if busqueda:
        usuarios = usuarios.filter(username__icontains=busqueda)
    return render(request, "core/e3/usuarios.html", {"titulo": "Usuarios", "busqueda": busqueda,
        "pagina": Paginator(usuarios, 25).get_page(request.GET.get("page"))})


@login_required
def usuario_formulario(request, usuario_id=None):
    if not request.user.is_staff:
        return HttpResponseForbidden("Solo el administrador puede gestionar cuentas de acceso.")
    usuario = get_object_or_404(User, pk=usuario_id) if usuario_id else User()
    errores = {}
    if request.method == "POST":
        usuario.username = request.POST.get("username", "").strip()
        usuario.first_name = request.POST.get("first_name", "").strip()
        usuario.last_name = request.POST.get("last_name", "").strip()
        usuario.email = request.POST.get("email", "").strip().lower()
        usuario.is_active = request.POST.get("is_active") == "on"
        clave = request.POST.get("password", "")
        if not usuario_id and not clave:
            errores["password"] = ["La contraseña es obligatoria al crear una cuenta."]
        if clave:
            if clave != request.POST.get("confirmar", ""):
                errores["password"] = ["Las contraseñas no coinciden."]
            try:
                validate_password(clave, usuario)
            except ValidationError as error:
                errores["password"] = error.messages
            usuario.set_password(clave)
        if usuario_id == request.user.pk and not usuario.is_active:
            errores["is_active"] = ["No puede desactivar su propia cuenta mientras administra la tienda."]
        errores.update(errores_modelo(usuario))
        if not errores:
            usuario.save()
            if usuario.pk == request.user.pk and clave:
                update_session_auth_hash(request, usuario)
            messages.success(request, "Cuenta guardada. Las contraseñas se almacenan mediante el sistema de Django.")
            return redirect("core:gestion_usuarios")
    return render(request, "core/e3/usuario_form.html", {"titulo": "Editar usuario" if usuario_id else "Nuevo usuario",
        "usuario": usuario, "errores": errores, "nuevo": usuario_id is None})


@login_required
def usuario_desactivar(request, usuario_id):
    if not request.user.is_staff:
        return HttpResponseForbidden("Solo el administrador puede gestionar cuentas de acceso.")
    usuario = get_object_or_404(User, pk=usuario_id)
    if request.method == "POST":
        if usuario.pk == request.user.pk:
            messages.error(request, "No puede desactivar su propia cuenta.")
        else:
            usuario.is_active = False
            usuario.save(update_fields=["is_active"])
            messages.success(request, "Cuenta desactivada; ya no puede iniciar sesión.")
        return redirect("core:gestion_usuarios")
    return render(request, "core/e3/confirmar_eliminacion.html", {"titulo": "Desactivar usuario", "objeto": usuario,
        "volver": "core:gestion_usuarios", "desactivar": True})


@login_required
def gestion_categorias(request):
    return render(request, "core/e3/categorias.html", {"titulo": "Categorías", "categorias": Categoria.objects.order_by("nombre")})


@login_required
def categoria_formulario(request, categoria_id=None):
    categoria = get_object_or_404(Categoria, pk=categoria_id) if categoria_id else Categoria()
    errores = {}
    if request.method == "POST":
        categoria.nombre = request.POST.get("nombre", "").strip()
        categoria.slug = slugify(request.POST.get("slug", "").strip() or categoria.nombre)
        categoria.descripcion = request.POST.get("descripcion", "").strip()
        errores = errores_modelo(categoria)
        if not errores:
            categoria.save()
            messages.success(request, "Categoría guardada.")
            return redirect("core:gestion_categorias")
    return render(request, "core/e3/categoria_form.html", {"titulo": "Editar categoría" if categoria_id else "Nueva categoría",
        "categoria": categoria, "errores": errores})


@login_required
def categoria_eliminar(request, categoria_id):
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    if request.method == "POST":
        try:
            categoria.delete()
            messages.success(request, "Categoría eliminada.")
        except ProtectedError:
            messages.error(request, "La categoría tiene productos asociados y no puede eliminarse.")
        return redirect("core:gestion_categorias")
    return render(request, "core/e3/confirmar_eliminacion.html", {"titulo": "Eliminar categoría", "objeto": categoria,
        "volver": "core:gestion_categorias"})


@login_required
def gestion_clientes(request):
    clientes = Cliente.objects.order_by("nombre", "id")
    busqueda = request.GET.get("q", "").strip()
    if busqueda:
        clientes = clientes.filter(nombre__icontains=busqueda)
    return render(request, "core/e3/clientes.html", {"titulo": "Clientes", "busqueda": busqueda,
        "pagina": Paginator(clientes, 25).get_page(request.GET.get("page"))})


@login_required
def cliente_formulario(request, cliente_id=None):
    persona = get_object_or_404(Cliente, pk=cliente_id) if cliente_id else Cliente()
    errores = {}
    if request.method == "POST":
        persona.nombre = request.POST.get("nombre", "").strip()
        persona.correo = request.POST.get("correo", "").strip().lower()
        persona.telefono = request.POST.get("telefono", "").strip()
        persona.activo = request.POST.get("activo") == "on"
        errores = errores_modelo(persona)
        if not errores:
            persona.save()
            messages.success(request, "Cliente guardado.")
            return redirect("core:gestion_clientes")
    return render(request, "core/e3/cliente_form.html", {"titulo": "Editar cliente" if cliente_id else "Nuevo cliente",
        "persona": persona, "errores": errores})


@login_required
def cliente_eliminar(request, cliente_id):
    persona = get_object_or_404(Cliente, pk=cliente_id)
    if request.method == "POST":
        try:
            persona.delete()
            messages.success(request, "Cliente eliminado.")
        except ProtectedError:
            messages.error(request, "El cliente tiene ventas asociadas. Puede desactivarlo sin borrar su historial.")
        return redirect("core:gestion_clientes")
    return render(request, "core/e3/confirmar_eliminacion.html", {"titulo": "Eliminar cliente", "objeto": persona,
        "volver": "core:gestion_clientes"})


@login_required
def gestion_ventas(request):
    ventas = Boleta.objects.select_related("cliente", "sucursal").annotate(
        total=Sum(F("detalleboleta__cantidad") * F("detalleboleta__precio_unitario"), default=0)
    ).order_by("-fecha", "-numero")
    return render(request, "core/e3/ventas.html", {"titulo": "Ventas",
        "pagina": Paginator(ventas, 25).get_page(request.GET.get("page"))})


@login_required
def venta_formulario(request, venta_id=None):
    venta = get_object_or_404(Boleta, pk=venta_id) if venta_id else Boleta(fecha=date.today())
    errores = {}
    if request.method == "POST":
        venta.numero = request.POST.get("numero", "")
        venta.fecha = request.POST.get("fecha", "")
        venta.cliente_id = request.POST.get("cliente") or None
        venta.sucursal_id = request.POST.get("sucursal") or None
        errores = errores_modelo(venta)
        if not errores:
            venta.save()
            messages.success(request, "Venta guardada. Puede incorporar sus productos en el detalle.")
            return redirect("core:venta_detalle", venta_id=venta.pk)
    return render(request, "core/e3/venta_form.html", {"titulo": "Editar venta" if venta_id else "Nueva venta", "venta": venta,
        "errores": errores, "fecha_formulario": request.POST.get("fecha", "") if request.method == "POST" else venta.fecha.isoformat(),
        "clientes": Cliente.objects.order_by("nombre"), "sucursales": Sucursal.objects.order_by("nombre")})


@login_required
def venta_detalle(request, venta_id):
    venta = get_object_or_404(Boleta.objects.select_related("cliente", "sucursal"), pk=venta_id)
    detalles = DetalleBoleta.objects.filter(boleta=venta).select_related("producto").order_by("id")
    total = detalles.aggregate(total=Sum(F("cantidad") * F("precio_unitario"), default=0))["total"]
    return render(request, "core/e3/venta_detalle.html", {"titulo": f"Venta {venta.numero}", "venta": venta,
        "detalles": detalles, "total": total})


@login_required
def detalle_formulario(request, venta_id, detalle_id=None):
    venta = get_object_or_404(Boleta, pk=venta_id)
    detalle = get_object_or_404(DetalleBoleta, pk=detalle_id, boleta=venta) if detalle_id else DetalleBoleta(boleta=venta)
    errores = {}
    if request.method == "POST":
        detalle.producto_id = request.POST.get("producto") or None
        detalle.cantidad = request.POST.get("cantidad", "")
        detalle.precio_unitario = request.POST.get("precio_unitario", "")
        errores = errores_modelo(detalle)
        if not errores:
            detalle.save()
            messages.success(request, "Detalle guardado con el precio histórico indicado.")
            return redirect("core:venta_detalle", venta_id=venta.pk)
    return render(request, "core/e3/detalle_form.html", {"titulo": "Editar detalle" if detalle_id else "Agregar producto a la venta",
        "venta": venta, "detalle": detalle, "errores": errores, "productos": Producto.objects.order_by("nombre")})


@login_required
def detalle_eliminar(request, venta_id, detalle_id):
    detalle = get_object_or_404(DetalleBoleta, pk=detalle_id, boleta_id=venta_id)
    if request.method == "POST":
        detalle.delete()
        messages.success(request, "Detalle eliminado.")
        return redirect("core:venta_detalle", venta_id=venta_id)
    return render(request, "core/e3/confirmar_eliminacion.html", {"titulo": "Eliminar detalle", "objeto": detalle,
        "venta_id": venta_id})


@login_required
def venta_eliminar(request, venta_id):
    venta = get_object_or_404(Boleta, pk=venta_id)
    if request.method == "POST":
        venta.delete()
        messages.success(request, "Venta y detalles eliminados. El cliente y los productos se conservaron.")
        return redirect("core:gestion_ventas")
    return render(request, "core/e3/confirmar_eliminacion.html", {"titulo": "Eliminar venta y sus detalles", "objeto": venta,
        "volver": "core:gestion_ventas"})
