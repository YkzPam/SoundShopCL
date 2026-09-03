"""Rutas semanticas y nombradas de la tienda."""

from django.urls import path

from . import views


app_name = "core"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("productos/", views.catalogo, name="catalogo"),
    path("productos/<int:producto_id>/", views.detalle_producto, name="detalle_producto"),
    path("categorias/", views.categorias, name="categorias"),
    path("categorias/<slug:slug>/", views.detalle_categoria, name="detalle_categoria"),
    path("buscar/", views.buscar, name="buscar"),
    path("carrito/", views.carrito, name="carrito"),
    path("carrito/agregar/<int:producto_id>/", views.agregar_al_carrito, name="agregar_al_carrito"),
    path("carrito/actualizar/<int:producto_id>/", views.actualizar_carrito, name="actualizar_carrito"),
    path("carrito/eliminar/<int:producto_id>/", views.eliminar_del_carrito, name="eliminar_del_carrito"),
    path("carrito/confirmar/", views.confirmar_pedido, name="confirmar_pedido"),
    path("pedido/confirmado/", views.pedido_confirmado, name="pedido_confirmado"),
]
