"""La tienda consulta SQLite; la gestión persistente se realiza en Django Admin.

El recorrido de cuenta y carrito de la entrega anterior sigue siendo una
simulación. No genera cuentas de Django, ventas ni cobros.
"""
import json
from pathlib import Path
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .forms import LoginForm, RegistroForm
from .models import Categoria, Producto

DATA_DIR = Path(__file__).resolve().parent / "data"


def leer_json(nombre):
    with (DATA_DIR / nombre).open(encoding="utf-8") as archivo:
        return json.load(archivo)


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
    if acceso_admin:
        return redirect("admin:index")
    formulario = LoginForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and formulario.is_valid():
        correo = formulario.cleaned_data["correo"].lower()
        clave = formulario.cleaned_data["clave"]
        for usuario in leer_json("usuarios.json"):
            if (usuario["correo"] == correo and usuario.get("clave_demo") == clave
                    and usuario["activo"] and usuario["rol"] == "cliente"):
                request.session["nombre"] = usuario["nombre"]
                request.session["rol"] = "cliente"
                messages.success(request, "Sesión iniciada.")
                return redirect("core:cliente")
        formulario.add_error(None, "El correo o la contraseña no son correctos.")
    return render(request, "core/login.html", {"formulario": formulario, "titulo": "Iniciar sesión"})


def registro(request):
    formulario = RegistroForm(request.POST if request.method == "POST" else None)
    resultado = None
    if request.method == "POST" and formulario.is_valid():
        correo = formulario.cleaned_data["correo"].lower()
        if any(u["correo"] == correo for u in leer_json("usuarios.json")):
            formulario.add_error("correo", "Ese correo no está disponible.")
        else:
            resultado = {"nombre": formulario.cleaned_data["nombre"], "correo": correo}
            messages.success(request, "Datos de registro validados. No se creó una cuenta permanente.")
    return render(request, "core/registro.html", {"formulario": formulario, "resultado": resultado, "titulo": "Crear cuenta"})


def salir(request):
    if request.method == "POST":
        request.session.pop("rol", None)
        request.session.pop("nombre", None)
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


# Compatibilidad con los enlaces de la entrega anterior; el CRUD está en Admin.
def gestion(request):
    return redirect("admin:index")


def gestion_productos(request):
    return redirect("admin:core_producto_changelist")


def producto_formulario(request, producto_id=None):
    if producto_id is None:
        return redirect("admin:core_producto_add")
    return redirect("admin:core_producto_change", producto_id)


def gestion_usuarios(request):
    return redirect("admin:core_cliente_changelist")
