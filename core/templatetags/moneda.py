"""Formato de precios; no cambia el valor almacenado ni los cálculos."""
from django import template
from django.utils.numberformat import format as formato_numero

register = template.Library()


@register.filter
def pesos(valor):
    # Oculta ,00, pero conserva los centavos cuando el valor los contiene.
    decimales = 0 if valor == int(valor) else 2
    return formato_numero(
        valor, decimal_sep=",", decimal_pos=decimales,
        grouping=3, thousand_sep=".", force_grouping=True,
    )
