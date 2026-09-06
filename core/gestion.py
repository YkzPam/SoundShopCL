"""Validación de fichas administrativas sin publicar cambios en el catálogo."""

from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .catalogo import obtener_categoria, obtener_producto, obtener_productos
from .forms import FichaGestionForm


@require_http_methods(['GET', 'POST'])
def ficha_producto(request, producto_id=1):
    producto = obtener_producto(producto_id)
    if producto is None:
        messages.warning(request, 'El producto solicitado no existe. Selecciona una ficha del catálogo.')
        return redirect('core:gestion_productos')
    inicial = {campo: getattr(producto, campo) for campo in ('nombre', 'marca', 'categoria', 'descripcion', 'precio', 'stock')}
    inicial['estado'] = 'activo'
    formulario = FichaGestionForm(request.POST if request.method == 'POST' else None, initial=inicial)
    resultado = None
    if request.method == 'POST' and formulario.is_valid():
        datos = formulario.cleaned_data
        resultado = {
            **datos,
            'categoria_nombre': obtener_categoria(datos['categoria']).nombre,
            'valor_existencias': datos['precio'] * datos['stock'],
            'disponibilidad': 'Inactivo' if datos['estado'] == 'inactivo' else ('Disponible' if datos['stock'] > 0 else 'Agotado'),
        }
    return render(request, 'core/gestion_producto.html', {
        'producto_base': producto, 'productos_gestion': obtener_productos(),
        'formulario_gestion': formulario, 'resultado_gestion': resultado,
    })
