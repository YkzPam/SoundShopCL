"""Autorización compartida por las vistas del panel propio."""
from functools import wraps
from django.shortcuts import render


def es_administrador(usuario):
    return usuario.is_authenticated and usuario.is_active and (
        usuario.is_superuser or usuario.groups.filter(name="Administrador").exists()
    )


def grupos_permitidos(*nombres):
    def decorar(vista):
        @wraps(vista)
        def verificar(request, *args, **kwargs):
            usuario = request.user
            autorizado = es_administrador(usuario)
            if usuario.is_authenticated and usuario.is_active and not autorizado:
                autorizado = usuario.groups.filter(name__in=nombres).exists()
            if not autorizado:
                return render(request, "core/e3/sin_permiso.html", {"titulo": "Acceso restringido"}, status=403)
            return vista(request, *args, **kwargs)
        return verificar
    return decorar
