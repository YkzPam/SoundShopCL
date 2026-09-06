"""Formularios y validaciones de la tienda."""

from django import forms

from .catalogo import obtener_categorias


CLASE_CAMPO = "form-control"


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
            attrs={"class": CLASE_CAMPO, "placeholder": "Ej. 100000", "step": "1"}
        ),
    )
    solo_disponibles = forms.BooleanField(
        required=False,
        label="Mostrar solo productos disponibles",
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-checkbox"
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
                "class": "quantity-input",
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


class FichaGestionForm(forms.Form):
    """Entradas administrativas de una ficha, sin persistencia en E1."""

    nombre = forms.CharField(label="Nombre del producto", min_length=3, max_length=100)
    marca = forms.CharField(label="Marca", min_length=2, max_length=60)
    categoria = forms.ChoiceField(label="Categoría")
    descripcion = forms.CharField(label="Descripción", min_length=20, max_length=600,
        widget=forms.Textarea(attrs={"rows": 4}))
    precio = forms.IntegerField(label="Precio de venta (CLP)", min_value=1, max_value=2_000_000,
        help_text="Pesos enteros, entre $1 y $2.000.000.", widget=forms.NumberInput(attrs={"step": 1}))
    stock = forms.IntegerField(label="Stock disponible", min_value=0, max_value=9999,
        help_text="Entre 0 y 9.999 unidades. Cero indica producto agotado.")
    estado = forms.ChoiceField(label="Estado de publicación",
        choices=(("activo", "Activo"), ("inactivo", "Inactivo")))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].choices = [(c.slug, c.nombre) for c in obtener_categorias()]
        for nombre, campo in self.fields.items():
            campo.widget.attrs['class'] = 'form-control'
            campo.widget.attrs['aria-describedby'] = f'id_{nombre}_help id_{nombre}_errors'

    def clean(self):
        datos = super().clean()
        for nombre in ('nombre', 'marca', 'descripcion'):
            if nombre in datos:
                datos[nombre] = ' '.join(datos[nombre].split())
                if len(datos[nombre]) < self.fields[nombre].min_length:
                    self.add_error(nombre, f"Ingresa al menos {self.fields[nombre].min_length} caracteres de contenido.")
        return datos


class IniciarSesionForm(forms.Form):
    correo = forms.EmailField(label="Correo electrónico", max_length=120,
        widget=forms.EmailInput(attrs={"class": "account-form__input", "autocomplete": "username", "placeholder": "nombre@correo.cl"}))
    contrasena = forms.CharField(label="Contraseña", max_length=128,
        widget=forms.PasswordInput(attrs={"class": "account-form__input", "autocomplete": "current-password", "placeholder": "Ingresa tu contraseña"}))


class RegistroForm(forms.Form):
    nombre = forms.CharField(
        label="Nombre",
        min_length=2,
        max_length=60,
        widget=forms.TextInput(
            attrs={
                "class": "account-form__input",
                "autocomplete": "name",
                "placeholder": "Nombre y apellido",
            }
        ),
    )
    correo = forms.EmailField(
        label="Correo electrónico",
        max_length=120,
        widget=forms.EmailInput(
            attrs={
                "class": "account-form__input",
                "autocomplete": "email",
                "placeholder": "nombre@correo.cl",
            }
        ),
    )
    contrasena = forms.CharField(
        label="Contraseña",
        min_length=8,
        max_length=128,
        widget=forms.PasswordInput(
            attrs={
                "class": "account-form__input",
                "autocomplete": "new-password",
                "placeholder": "Mínimo 8 caracteres",
            }
        ),
    )
    confirmar_contrasena = forms.CharField(
        label="Confirmar contraseña",
        min_length=8,
        max_length=128,
        widget=forms.PasswordInput(
            attrs={
                "class": "account-form__input",
                "autocomplete": "new-password",
                "placeholder": "Repite tu contraseña",
            }
        ),
    )
    acepta_terminos = forms.BooleanField(
        label="Acepto los términos de uso y la política de privacidad.",
        widget=forms.CheckboxInput(attrs={"class": "account-form__checkbox"}),
    )

    def clean_contrasena(self):
        contrasena = self.cleaned_data["contrasena"]
        if not any(caracter.isalpha() for caracter in contrasena):
            raise forms.ValidationError("Incluye al menos una letra.")
        if not any(caracter.isdigit() for caracter in contrasena):
            raise forms.ValidationError("Incluye al menos un número.")
        return contrasena

    def clean(self):
        datos = super().clean()
        contrasena = datos.get("contrasena")
        confirmacion = datos.get("confirmar_contrasena")
        if contrasena and confirmacion and contrasena != confirmacion:
            self.add_error("confirmar_contrasena", "Las contraseñas no coinciden.")
        return datos
