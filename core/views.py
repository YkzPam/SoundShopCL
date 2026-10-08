"""Petición, JSON, condiciones y contexto para HTML.

La cuenta y el carrito son temporales. Los formularios administrativos validan
y muestran una vista previa, pero no escriben archivos ni base de datos.
"""
import json
import hashlib
from pathlib import Path
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.http import Http404
from django.shortcuts import redirect, render
from django.views.decorators.debug import sensitive_post_parameters
from .forms import LoginForm, ProductoForm, RegistroForm, UsuarioForm

DATA_DIR = Path(__file__).resolve().parent / "data"


def leer_json(nombre):
    with (DATA_DIR / nombre).open(encoding="utf-8") as archivo:
        return json.load(archivo)


def usuarios_disponibles(request):
    usuarios = leer_json("usuarios.json")
    usuarios.append({"nombre": "Administrador", "correo": request.session.get("admin_email", ""),
                     "rol": "administrador", "activo": True})
    return usuarios


def admin_autorizado(request):
    return (settings.SOUNDSHOP_ADMIN_ENABLED
            and request.session.get("rol") == "administrador"
            and request.session.get("admin_revision") ==
            hashlib.sha256(settings.SOUNDSHOP_ADMIN_PASSWORD_HASH.encode()).hexdigest())


def obtener_producto(producto_id):
    for producto in leer_json("catalogo.json")["productos"]:
        if producto["id"] == producto_id:
            return producto
    raise Http404("Producto no encontrado")


def inicio(request):
    datos = leer_json("catalogo.json")
    return render(request, "core/inicio.html", {"productos": datos["productos"][:4], "titulo": "Inicio"})


def catalogo(request):
    datos = leer_json("catalogo.json")
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
    datos = leer_json("catalogo.json")
    categorias_lista = []
    for categoria in datos["categorias"]:
        productos = [p for p in datos["productos"] if p["categoria"] == categoria["slug"]]
        categoria["cantidad"] = len(productos)
        categoria["imagen"] = productos[0]["imagen"] if productos else ""
        categorias_lista.append(categoria)
    return render(request, "core/categorias.html", {"categorias": categorias_lista, "titulo": "Categorías"})


def nosotros(request):
    return render(request, "core/nosotros.html", {"titulo": "Nosotros"})


@sensitive_post_parameters("clave")
def login(request):
    formulario = LoginForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and formulario.is_valid():
        usuario_encontrado = None
        correo = formulario.cleaned_data["correo"].lower()
        clave = formulario.cleaned_data["clave"]
        if (settings.SOUNDSHOP_ADMIN_ENABLED
                and check_password(correo, settings.SOUNDSHOP_ADMIN_USERNAME_HASH)
                and check_password(clave, settings.SOUNDSHOP_ADMIN_PASSWORD_HASH)):
            usuario_encontrado = {"nombre": "Administrador", "rol": "administrador"}
        else:
            for usuario in leer_json("usuarios.json"):
                if (usuario["rol"] == "cliente" and usuario["correo"] == correo
                        and usuario.get("clave_demo") == clave and usuario["activo"]):
                    usuario_encontrado = usuario
                    break
        if usuario_encontrado:
            request.session["nombre"] = usuario_encontrado["nombre"]
            request.session["rol"] = usuario_encontrado["rol"]
            if usuario_encontrado["rol"] == "administrador":
                request.session["admin_email"] = correo
                request.session["admin_revision"] = hashlib.sha256(
                    settings.SOUNDSHOP_ADMIN_PASSWORD_HASH.encode()).hexdigest()
                messages.success(request, "Bienvenido al panel de administración.")
                return redirect("core:gestion")
            request.session.pop("admin_email", None)
            request.session.pop("admin_revision", None)
            messages.success(request, "Sesión iniciada.")
            return redirect("core:cliente")
        formulario.add_error(None, "El correo o la contraseña no son correctos.")
    return render(request, "core/login.html", {"formulario": formulario, "titulo": "Iniciar sesión"})


def registro(request):
    formulario = RegistroForm(request.POST if request.method == "POST" else None)
    resultado = None
    if request.method == "POST" and formulario.is_valid():
        correo = formulario.cleaned_data["correo"].lower()
        existe = (any(u["correo"] == correo for u in leer_json("usuarios.json"))
                  or check_password(correo, settings.SOUNDSHOP_ADMIN_USERNAME_HASH))
        if existe:
            formulario.add_error("correo", "Ese correo no está disponible.")
        else:
            resultado = {"nombre": formulario.cleaned_data["nombre"], "correo": correo}
            messages.success(request, "Datos de registro validados. No se creó una cuenta permanente.")
    return render(request, "core/registro.html", {"formulario": formulario, "resultado": resultado,
                                                 "titulo": "Crear cuenta"})


def salir(request):
    if request.method == "POST":
        request.session.pop("rol", None)
        request.session.pop("nombre", None)
        request.session.pop("admin_email", None)
        request.session.pop("admin_revision", None)
        messages.success(request, "Sesión cerrada.")
    return redirect("core:inicio")


def cliente(request):
    if not request.session.get("rol"):
        return redirect("core:login")
    return render(request, "core/cliente.html", {"titulo": "Mi cuenta"})


def carrito(request):
    cantidades = request.session.get("carrito", {})
    lineas = []
    total = 0
    for producto in leer_json("catalogo.json")["productos"]:
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


def confirmar(request):
    if request.method != "POST":
        return redirect("core:carrito")
    if not request.session.get("rol"):
        messages.info(request, "Para continuar debe iniciar sesión.")
        return redirect("core:login")
    if not request.session.get("carrito"):
        messages.warning(request, "El carrito está vacío.")
        return redirect("core:carrito")
    request.session["carrito"] = {}
    return render(request, "core/confirmacion.html", {"titulo": "Confirmación"})


def gestion(request):
    if not admin_autorizado(request):
        return redirect("core:login")
    datos = leer_json("catalogo.json")
    contexto = {"titulo": "Administración", "total_productos": len(datos["productos"]),
                "total_usuarios": len(usuarios_disponibles(request)),
                "sin_stock": len([p for p in datos["productos"] if p["stock"] == 0])}
    return render(request, "core/gestion.html", contexto)


def gestion_productos(request):
    if not admin_autorizado(request):
        return redirect("core:login")
    return render(request, "core/gestion_productos.html", {
        "productos": leer_json("catalogo.json")["productos"], "titulo": "Administrar productos"})


def producto_formulario(request, producto_id=None):
    if not admin_autorizado(request):
        return redirect("core:login")
    datos = leer_json("catalogo.json")
    producto = obtener_producto(producto_id) if producto_id is not None else None
    formulario = ProductoForm(request.POST if request.method == "POST" else None,
                               initial=producto, categorias=datos["categorias"])
    resultado = None
    if request.method == "POST" and formulario.is_valid():
        resultado = formulario.cleaned_data
        messages.success(request, "Producto validado. Esta salida es una vista previa, no un cambio guardado.")
    return render(request, "core/producto_formulario.html", {
        "formulario": formulario, "resultado": resultado, "producto": producto,
        "titulo": "Editar producto" if producto else "Nuevo producto"})


def gestion_usuarios(request):
    if not admin_autorizado(request):
        return redirect("core:login")
    formulario = UsuarioForm(request.POST if request.method == "POST" else None)
    resultado = None
    usuarios = usuarios_disponibles(request)
    if request.method == "POST" and formulario.is_valid():
        if any(u["correo"] == formulario.cleaned_data["correo"].lower() for u in usuarios):
            formulario.add_error("correo", "El correo ya está registrado.")
        else:
            resultado = formulario.cleaned_data
            messages.success(request, "Usuario validado para vista previa. No se guardaron cambios.")
    return render(request, "core/gestion_usuarios.html", {
        "usuarios": usuarios, "formulario": formulario, "resultado": resultado, "titulo": "Administrar usuarios"})
