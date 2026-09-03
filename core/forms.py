"""Formularios y validaciones del catalogo y el carrito."""

from django import forms

from .catalogo import obtener_categorias


CLASE_CAMPO = (
    "w-full rounded-xl border border-white/10 bg-slate-950/70 px-4 py-3 "
    "text-sm text-white outline-none transition focus:border-violet-400 "
    "focus:ring-2 focus:ring-violet-400/20"
)


class FiltroCatalogoForm(forms.Form):
    q = forms.CharField(
        required=False,
        label="Buscar",
        max_length=80,
        widget=forms.TextInput(
            attrs={
                "class": CLASE_CAMPO,
                "placeholder": "Producto, marca o característica",
                "autocomplete": "off",
            }
        ),
    )
    categoria = forms.ChoiceField(required=False, label="Categoría")
    precio_maximo = forms.IntegerField(
        required=False,
        label="Precio máximo",
        min_value=1,
        max_value=2_000_000,
        widget=forms.NumberInput(
            attrs={"class": CLASE_CAMPO, "placeholder": "Ej. 100000", "step": "1000"}
        ),
    )
    solo_disponibles = forms.BooleanField(
        required=False,
        label="Mostrar solo productos disponibles",
        widget=forms.CheckboxInput(
            attrs={
                "class": "h-4 w-4 rounded border-white/20 bg-slate-950 text-violet-500 focus:ring-violet-400"
            }
        ),
    )
    orden = forms.ChoiceField(
        required=False,
        label="Ordenar",
        choices=(
            ("destacados", "Destacados"),
            ("precio_asc", "Menor precio"),
            ("precio_desc", "Mayor precio"),
            ("nombre", "Nombre A–Z"),
        ),
        widget=forms.Select(attrs={"class": CLASE_CAMPO}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["categoria"].choices = [("", "Todas las categorías")] + [
            (categoria.slug, categoria.nombre) for categoria in obtener_categorias()
        ]
        self.fields["categoria"].widget.attrs["class"] = CLASE_CAMPO


class CantidadProductoForm(forms.Form):
    cantidad = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(
            attrs={
                "class": "w-20 rounded-xl border border-white/10 bg-slate-950/70 px-3 py-2 text-white",
                "aria-label": "Cantidad",
            }
        ),
    )

    def __init__(self, *args, stock: int | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        if stock is not None:
            self.fields["cantidad"].max_value = stock
            self.fields["cantidad"].widget.attrs["max"] = stock


class CantidadCarritoForm(forms.Form):
    cantidad = forms.IntegerField(min_value=0, max_value=99)
