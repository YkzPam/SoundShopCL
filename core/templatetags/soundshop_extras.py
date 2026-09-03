"""Filtros de presentacion para las plantillas."""

from django import template


register = template.Library()


@register.filter
def precio_clp(valor):
    try:
        return f"${int(valor):,}".replace(",", ".")
    except (TypeError, ValueError):
        return "$0"


@register.filter
def nombre_categoria(slug):
    nombres = {
        "audifonos": "Audífonos",
        "tornamesas-vinilos": "Tornamesas y vinilos",
        "estudio-creacion": "Estudio y creación",
    }
    return nombres.get(str(slug), str(slug).replace("-", " ").title())
