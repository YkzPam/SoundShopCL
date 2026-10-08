from django.urls import path
from . import views

app_name = "core"
urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("productos/", views.catalogo, name="catalogo"),
    path("productos/<int:producto_id>/", views.detalle_producto, name="detalle_producto"),
    path("categorias/", views.categorias, name="categorias"),
    path("nosotros/", views.nosotros, name="nosotros"),
    path("login/", views.login, name="login"),
    path("registro/", views.registro, name="registro"),
    path("cuenta/", views.cliente, name="cliente"),
    path("cuenta/salir/", views.salir, name="salir"),
    path("carrito/", views.carrito, name="carrito"),
    path("carrito/agregar/<int:producto_id>/", views.agregar_carrito, name="agregar_carrito"),
    path("carrito/quitar/<int:producto_id>/", views.quitar_carrito, name="quitar_carrito"),
    path("carrito/confirmar/", views.confirmar, name="confirmar"),
    path("gestion/", views.gestion, name="gestion"),
    path("gestion/productos/", views.gestion_productos, name="gestion_productos"),
    path("gestion/productos/nuevo/", views.producto_formulario, name="producto_nuevo"),
    path("gestion/productos/<int:producto_id>/", views.producto_formulario, name="producto_editar"),
    path("gestion/usuarios/", views.gestion_usuarios, name="gestion_usuarios"),
]
