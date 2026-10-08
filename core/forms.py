"""Entrada, tipos y validaciones básicas del caso tienda."""
from django import forms


class FormularioBase(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            if isinstance(campo.widget, forms.CheckboxInput):
                campo.widget.attrs["class"] = "form-check-input"
            elif isinstance(campo.widget, forms.Select):
                campo.widget.attrs["class"] = "form-select"
            else:
                campo.widget.attrs["class"] = "form-control"


class LoginForm(FormularioBase):
    correo = forms.EmailField(label="Correo", max_length=120)
    clave = forms.CharField(label="Contraseña", widget=forms.PasswordInput)


class RegistroForm(FormularioBase):
    nombre = forms.CharField(label="Nombre", min_length=3, max_length=80)
    correo = forms.EmailField(label="Correo", max_length=120)
    clave = forms.CharField(label="Contraseña", min_length=8, max_length=60, widget=forms.PasswordInput)
    confirmar = forms.CharField(label="Repetir contraseña", widget=forms.PasswordInput)

    def clean(self):
        datos = super().clean()
        if datos.get("clave") and datos.get("confirmar") != datos["clave"]:
            self.add_error("confirmar", "Las contraseñas deben coincidir.")
        return datos


class ProductoForm(FormularioBase):
    nombre = forms.CharField(label="Nombre", min_length=3, max_length=80)
    marca = forms.CharField(label="Marca", max_length=60)
    categoria = forms.ChoiceField(label="Categoría")
    descripcion = forms.CharField(label="Descripción", min_length=10, max_length=500,
                                 widget=forms.Textarea(attrs={"rows": 3}))
    precio = forms.IntegerField(label="Precio en pesos", min_value=1, max_value=10000000)
    stock = forms.IntegerField(label="Stock", min_value=0, max_value=999)

    def __init__(self, *args, categorias, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["categoria"].choices = [(c["slug"], c["nombre"]) for c in categorias]


class UsuarioForm(FormularioBase):
    nombre = forms.CharField(label="Nombre", min_length=3, max_length=80)
    correo = forms.EmailField(label="Correo", max_length=120)
    rol = forms.ChoiceField(label="Rol", choices=[("cliente", "Cliente"), ("administrador", "Administrador")])
    activo = forms.BooleanField(label="Usuario activo", required=False, initial=True)
