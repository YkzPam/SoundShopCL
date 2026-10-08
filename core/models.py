from datetime import date

from django.core.validators import MinValueValidator
from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=80, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre


class Marca(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    pais = models.CharField(max_length=60, blank=True)

    def __str__(self):
        return self.nombre


class Proveedor(models.Model):
    nombre = models.CharField(max_length=120)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "proveedores"

    def __str__(self):
        return self.nombre


class Sucursal(models.Model):
    nombre = models.CharField(max_length=80)
    direccion = models.CharField(max_length=180)
    comuna = models.CharField(max_length=60)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "sucursales"

    def __str__(self):
        return self.nombre


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    codigo = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=80)
    descripcion = models.TextField(max_length=500)
    precio = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(1)],
    )
    stock = models.PositiveIntegerField(default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    imagen = models.CharField(max_length=200, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Boleta(models.Model):
    numero = models.PositiveIntegerField(unique=True, validators=[MinValueValidator(1)])
    fecha = models.DateField(default=date.today)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    productos = models.ManyToManyField(Producto, through="DetalleBoleta")

    def __str__(self):
        return f"Boleta {self.numero}"


class DetalleBoleta(models.Model):
    boleta = models.ForeignKey(Boleta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    precio_unitario = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(1)],
    )

    class Meta:
        unique_together = ("boleta", "producto")
        verbose_name_plural = "detalles de boleta"

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.boleta} / {self.producto}"


class CompraProveedor(models.Model):
    numero = models.PositiveIntegerField(unique=True, validators=[MinValueValidator(1)])
    fecha = models.DateField(default=date.today)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    productos = models.ManyToManyField(Producto, through="DetalleCompra")

    class Meta:
        verbose_name_plural = "compras a proveedores"

    def __str__(self):
        return f"Compra {self.numero}"


class DetalleCompra(models.Model):
    compra = models.ForeignKey(CompraProveedor, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    precio_costo = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(1)],
    )

    class Meta:
        unique_together = ("compra", "producto")
        verbose_name_plural = "detalles de compra"

    @property
    def subtotal(self):
        return self.cantidad * self.precio_costo

    def __str__(self):
        return f"{self.compra} / {self.producto}"
