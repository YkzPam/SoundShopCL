from django.contrib import admin
from .models import (
    Categoria, Marca, Proveedor, Sucursal, Cliente, Producto,
    Boleta, DetalleBoleta, CompraProveedor, DetalleCompra,
)

admin.site.site_header = "SoundShop CL · Administración"
admin.site.site_title = "SoundShop CL"
admin.site.index_title = "Gestión de la tienda"


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug")
    search_fields = ("nombre",)
    prepopulated_fields = {"slug": ("nombre",)}


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "pais")
    search_fields = ("nombre",)
    list_filter = ("pais",)


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "correo", "telefono", "activo")
    search_fields = ("nombre", "correo")
    list_filter = ("activo",)


@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ("nombre", "direccion", "comuna", "activo")
    search_fields = ("nombre", "comuna")
    list_filter = ("comuna", "activo")


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "correo", "telefono", "activo")
    search_fields = ("nombre", "correo")
    list_filter = ("activo",)
    list_per_page = 25
    ordering = ("id",)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    # Las mismas opciones de ModelAdmin utilizadas en el ejemplo del docente.
    list_display = ("codigo", "nombre", "categoria", "marca", "precio", "stock", "activo")
    search_fields = ("codigo", "nombre", "marca__nombre")
    list_filter = ("categoria", "marca", "activo")
    ordering = ("codigo",)
    list_select_related = ("categoria", "marca")
    readonly_fields = ("id",)
    fieldsets = (
        ("Identificación", {"fields": ("codigo", "nombre", "descripcion", "imagen")}),
        ("Clasificación", {"fields": ("categoria", "marca", "proveedor")}),
        ("Inventario", {"fields": ("precio", "stock", "activo")}),
        ("Registro", {"fields": ("id",)}),
    )
    list_per_page = 25


class DetalleBoletaInline(admin.TabularInline):
    # Permite completar los productos de una boleta dentro de su formulario.
    model = DetalleBoleta
    extra = 0
    readonly_fields = ("subtotal",)
    autocomplete_fields = ("producto",)


@admin.register(Boleta)
class BoletaAdmin(admin.ModelAdmin):
    list_display = ("numero", "fecha", "cliente", "sucursal")
    search_fields = ("=numero", "cliente__nombre")
    list_filter = ("fecha", "sucursal")
    autocomplete_fields = ("cliente",)
    inlines = (DetalleBoletaInline,)


@admin.register(DetalleBoleta)
class DetalleBoletaAdmin(admin.ModelAdmin):
    list_display = ("boleta", "producto", "cantidad", "precio_unitario", "subtotal")
    search_fields = ("=boleta__numero", "producto__nombre")
    list_filter = ("boleta__fecha",)
    readonly_fields = ("subtotal",)
    autocomplete_fields = ("boleta", "producto")


class DetalleCompraInline(admin.TabularInline):
    model = DetalleCompra
    extra = 0
    readonly_fields = ("subtotal",)
    autocomplete_fields = ("producto",)


@admin.register(CompraProveedor)
class CompraProveedorAdmin(admin.ModelAdmin):
    list_display = ("numero", "fecha", "proveedor", "sucursal")
    search_fields = ("=numero", "proveedor__nombre")
    list_filter = ("fecha", "sucursal")
    inlines = (DetalleCompraInline,)


@admin.register(DetalleCompra)
class DetalleCompraAdmin(admin.ModelAdmin):
    list_display = ("compra", "producto", "cantidad", "precio_costo", "subtotal")
    search_fields = ("=compra__numero", "producto__nombre")
    list_filter = ("compra__fecha",)
    readonly_fields = ("subtotal",)
    autocomplete_fields = ("compra", "producto")
