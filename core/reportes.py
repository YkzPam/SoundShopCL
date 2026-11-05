"""Las veinte preguntas de Tienda, en el mismo orden de la guía de E3.

Las consultas y sus cálculos se ejecutan con el ORM, no con SQL escrito a mano.
Boleta representa la venta de la tienda y DetalleBoleta conserva sus productos.
"""
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg, Count, F, Q, Sum
from django.db.models.functions import ExtractMonth
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from .models import Categoria, Cliente, Producto, Boleta, DetalleBoleta


PREGUNTAS = [
    "¿Cuáles son todos los productos disponibles en la tienda?",
    "¿Qué productos pertenecen a una categoría seleccionada?",
    "¿Qué productos se encuentran dentro de un rango de precios?",
    "¿Cuáles son los 10 productos más caros de la tienda?",
    "¿Cuántos clientes están registrados en el sistema?",
    "¿Cuáles son las compras realizadas por un cliente específico?",
    "¿Qué productos adquirió un cliente en una venta determinada?",
    "¿Cuántas ventas se realizaron durante un período seleccionado?",
    "¿Cuáles son los productos que tienen menos de cinco unidades disponibles?",
    "¿Cuál es el monto total vendido durante un día seleccionado?",
    "¿Cuáles son los cinco productos más vendidos según cantidad de unidades?",
    "¿Cuáles son los cinco clientes que han realizado más compras?",
    "¿Cuál es el monto total comprado por cada cliente?",
    "¿Qué productos nunca han sido vendidos?",
    "¿Cuál es el promedio de dinero gastado por venta?",
    "¿Qué categoría genera el mayor monto de ventas?",
    "¿Cuántas unidades se han vendido de cada producto durante el último mes?",
    "¿Qué cliente ha gastado más dinero durante el año?",
    "¿Cómo se distribuyen los montos de ventas por mes durante el año seleccionado?",
    "¿Cuáles son los 10 productos que generan mayores ingresos para la tienda?",
]


def identificador(valor, nombre):
    if not valor or not valor.isdigit() or int(valor) < 1:
        raise ValueError("Debe seleccionar " + nombre + ".")
    return int(valor)


@login_required
def reportes(request):
    numero = request.GET.get("reporte", "1")
    if not numero.isdigit() or not 1 <= int(numero) <= 20:
        return HttpResponseBadRequest("El reporte debe ser un número del 1 al 20.")
    numero = int(numero)
    filtros = request.GET.copy()
    hoy = date.today()
    filtros.setdefault("desde", hoy.replace(day=1).isoformat())
    filtros.setdefault("hasta", hoy.isoformat())
    filtros.setdefault("fecha", hoy.isoformat())
    filtros.setdefault("anio", str(hoy.year))
    filas = []
    columnas = []
    monedas = []
    error = ""
    informacion = ""

    try:
        if numero in (2,):
            categoria = identificador(filtros.get("categoria"), "una categoría")
            if not Categoria.objects.filter(pk=categoria).exists():
                raise ValueError("La categoría seleccionada no existe.")
        if numero in (6, 7):
            cliente = identificador(filtros.get("cliente"), "un cliente")
            if not Cliente.objects.filter(pk=cliente).exists():
                raise ValueError("El cliente seleccionado no existe.")
        if numero == 7:
            venta = identificador(filtros.get("venta"), "una venta")
            if not Boleta.objects.filter(pk=venta, cliente_id=cliente).exists():
                raise ValueError("La venta seleccionada no pertenece a ese cliente.")
        if numero == 8:
            desde = date.fromisoformat(filtros.get("desde", ""))
            hasta = date.fromisoformat(filtros.get("hasta", ""))
            if hasta < desde:
                raise ValueError("La fecha final no puede ser anterior a la inicial.")
        if numero == 10:
            fecha = date.fromisoformat(filtros.get("fecha", ""))
        if numero in (18, 19):
            anio = identificador(filtros.get("anio"), "un año válido")
            if anio > 9999:
                raise ValueError("El año debe estar entre 1 y 9999.")

        # 1. Disponible significa activo y con unidades en stock.
        if numero == 1:
            columnas = ["Código", "Producto", "Precio", "Stock"]
            monedas = [2]
            filas = Producto.objects.filter(activo=True, stock__gt=0).order_by("codigo").values_list("codigo", "nombre", "precio", "stock")

        # 2. Filtro por la clave de la categoría.
        elif numero == 2:
            columnas = ["Código", "Producto", "Categoría", "Stock"]
            filas = Producto.objects.filter(categoria_id=categoria).order_by("codigo").values_list("codigo", "nombre", "categoria__nombre", "stock")

        # 3. Los dos extremos del intervalo están incluidos.
        elif numero == 3:
            minimo = Decimal(filtros.get("minimo", ""))
            maximo = Decimal(filtros.get("maximo", ""))
            if not minimo.is_finite() or not maximo.is_finite() or minimo < 0 or maximo < minimo or maximo > Decimal("99999999.99"):
                raise ValueError("Debe indicar un rango de precios válido, sin puntos de miles.")
            columnas = ["Código", "Producto", "Precio"]
            monedas = [2]
            filas = Producto.objects.filter(precio__range=(minimo, maximo)).order_by("precio", "codigo").values_list("codigo", "nombre", "precio")

        # 4. Orden descendente y límite de diez productos.
        elif numero == 4:
            columnas = ["Código", "Producto", "Precio"]
            monedas = [2]
            filas = Producto.objects.order_by("-precio", "codigo").values_list("codigo", "nombre", "precio")[:10]

        # 5. Conteo, incluyendo clientes desactivados que siguen registrados.
        elif numero == 5:
            columnas = ["Clientes registrados"]
            filas = [(Cliente.objects.count(),)]

        # 6. Son compras del cliente (ventas), no compras a proveedores.
        elif numero == 6:
            columnas = ["Venta", "Fecha", "Cliente", "Total"]
            monedas = [3]
            filas = Boleta.objects.filter(cliente_id=cliente).annotate(
                total=Sum(F("detalleboleta__cantidad") * F("detalleboleta__precio_unitario"), default=0)
            ).order_by("-fecha", "-numero").values_list("numero", "fecha", "cliente__nombre", "total")

        # 7. Se comprueba también que la venta corresponde al cliente.
        elif numero == 7:
            columnas = ["Producto", "Cantidad", "Precio histórico", "Subtotal"]
            monedas = [2, 3]
            filas = DetalleBoleta.objects.filter(boleta_id=venta, boleta__cliente_id=cliente).annotate(
                importe=F("cantidad") * F("precio_unitario")
            ).order_by("id").values_list("producto__nombre", "cantidad", "precio_unitario", "importe")

        # 8. Cuenta ventas, no líneas de detalle.
        elif numero == 8:
            columnas = ["Desde", "Hasta", "Ventas realizadas"]
            filas = [(desde, hasta, Boleta.objects.filter(fecha__range=(desde, hasta)).count())]

        # 9. Incluye productos sin stock.
        elif numero == 9:
            columnas = ["Código", "Producto", "Stock"]
            filas = Producto.objects.filter(stock__lt=5).order_by("stock", "codigo").values_list("codigo", "nombre", "stock")

        # 10. Se usan los precios históricos de las líneas, no el precio actual.
        elif numero == 10:
            columnas = ["Fecha", "Total vendido"]
            monedas = [1]
            total = DetalleBoleta.objects.filter(boleta__fecha=fecha).aggregate(total=Sum(F("cantidad") * F("precio_unitario"), default=0))["total"]
            filas = [(fecha, total)]

        # 11. Más vendido se mide por unidades, no por cantidad de boletas.
        elif numero == 11:
            columnas = ["Código", "Producto", "Unidades vendidas"]
            filas = Producto.objects.annotate(unidades=Sum("detalleboleta__cantidad", default=0)).filter(unidades__gt=0).order_by("-unidades", "codigo").values_list("codigo", "nombre", "unidades")[:5]

        # 12. Se cuenta una compra por boleta, independientemente de sus líneas.
        elif numero == 12:
            columnas = ["Cliente", "Correo", "Compras realizadas"]
            filas = Cliente.objects.annotate(compras=Count("boleta")).filter(compras__gt=0).order_by("-compras", "id").values_list("nombre", "correo", "compras")[:5]

        # 13. Los clientes sin ventas aparecen con total cero.
        elif numero == 13:
            columnas = ["Cliente", "Correo", "Total comprado"]
            monedas = [2]
            filas = Cliente.objects.annotate(total=Sum(F("boleta__detalleboleta__cantidad") * F("boleta__detalleboleta__precio_unitario"), default=0)).order_by("-total", "id").values_list("nombre", "correo", "total")

        # 14. Un producto nunca vendido no tiene detalles de venta asociados.
        elif numero == 14:
            columnas = ["Código", "Producto", "Stock"]
            filas = Producto.objects.filter(detalleboleta__isnull=True).order_by("codigo").values_list("codigo", "nombre", "stock")

        # 15. Primero se totaliza cada venta y después se promedian esos totales.
        elif numero == 15:
            columnas = ["Promedio por venta"]
            monedas = [0]
            promedio = Boleta.objects.annotate(total_venta=Sum(F("detalleboleta__cantidad") * F("detalleboleta__precio_unitario"), default=0)).aggregate(promedio=Avg("total_venta", default=0))["promedio"]
            filas = [(promedio,)]

        # 16. La categoría se alcanza desde el producto de cada detalle.
        elif numero == 16:
            columnas = ["Categoría", "Monto vendido"]
            monedas = [1]
            filas = Categoria.objects.annotate(total=Sum(F("producto__detalleboleta__cantidad") * F("producto__detalleboleta__precio_unitario"), default=0)).filter(total__gt=0).order_by("-total", "id").values_list("nombre", "total")[:1]

        # 17. Último mes se define como el mes calendario anterior completo.
        elif numero == 17:
            fin_mes = hoy.replace(day=1) - timedelta(days=1)
            inicio_mes = fin_mes.replace(day=1)
            informacion = f"Mes anterior completo: {inicio_mes:%d/%m/%Y} al {fin_mes:%d/%m/%Y}."
            columnas = ["Código", "Producto", "Unidades vendidas"]
            filas = Producto.objects.annotate(unidades=Sum("detalleboleta__cantidad", filter=Q(detalleboleta__boleta__fecha__range=(inicio_mes, fin_mes)), default=0)).order_by("codigo").values_list("codigo", "nombre", "unidades")

        # 18. El año se recibe del filtro de la página.
        elif numero == 18:
            columnas = ["Cliente", "Correo", "Total del año"]
            monedas = [2]
            filas = Cliente.objects.annotate(total=Sum(F("boleta__detalleboleta__cantidad") * F("boleta__detalleboleta__precio_unitario"), filter=Q(boleta__fecha__year=anio), default=0)).filter(total__gt=0).order_by("-total", "id").values_list("nombre", "correo", "total")[:1]

        # 19. Agrupación por mes del año solicitado.
        elif numero == 19:
            columnas = ["Mes (1–12)", "Monto vendido"]
            monedas = [1]
            filas = DetalleBoleta.objects.filter(boleta__fecha__year=anio).annotate(mes=ExtractMonth("boleta__fecha")).values("mes").annotate(total=Sum(F("cantidad") * F("precio_unitario"))).order_by("mes").values_list("mes", "total")

        # 20. Ingresos históricos acumulados por producto, con límite de diez.
        elif numero == 20:
            columnas = ["Código", "Producto", "Ingresos"]
            monedas = [2]
            filas = Producto.objects.annotate(total=Sum(F("detalleboleta__cantidad") * F("detalleboleta__precio_unitario"), default=0)).filter(total__gt=0).order_by("-total", "codigo").values_list("codigo", "nombre", "total")[:10]
    except (ValueError, InvalidOperation):
        error = "Revise los filtros: seleccione los registros solicitados e ingrese fechas, año o precios válidos."
        filas = []

    pagina = Paginator(filas, 25).get_page(request.GET.get("page"))
    return render(request, "core/e3/reportes.html", {"titulo": "Reportes de la tienda", "numero": numero,
        "pregunta": PREGUNTAS[numero - 1], "preguntas": enumerate(PREGUNTAS, 1), "filtros": filtros,
        "columnas": columnas, "filas": pagina.object_list, "pagina": pagina, "monedas": monedas,
        "error": error, "informacion": informacion, "categorias": Categoria.objects.order_by("nombre"),
        "clientes": Cliente.objects.order_by("nombre"), "ventas": Boleta.objects.order_by("-fecha", "-numero")})
