"""Carga inicial sin sobrescribir registros ya editados en Admin."""
import json
from decimal import Decimal
from pathlib import Path
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
from core.models import (
    Categoria, Marca, Proveedor, Sucursal, Cliente, Producto,
    Boleta, DetalleBoleta, CompraProveedor, DetalleCompra,
)


class Command(BaseCommand):
    help = "Carga los diez equipos musicales y registros ficticios relacionados."

    @transaction.atomic
    def handle(self, *args, **options):
        ruta = Path(__file__).resolve().parents[2] / "data" / "catalogo.json"
        with ruta.open(encoding="utf-8") as archivo:
            datos = json.load(archivo)
        fake = Faker("es_CL")
        fake.seed_instance(42)

        for categoria in datos["categorias"]:
            Categoria.objects.get_or_create(
                slug=categoria["slug"],
                defaults={"nombre": categoria["nombre"], "descripcion": categoria["descripcion"]},
            )
        proveedor, _ = Proveedor.objects.get_or_create(
            correo="distribuidor@example.test",
            defaults={"nombre": "Distribuidor Musical", "telefono": "+56 9 0000 0000"},
        )
        sucursal, _ = Sucursal.objects.get_or_create(
            nombre="SoundShop CL",
            defaults={"direccion": "Sector Apoquindo / Manquehue", "comuna": "Las Condes"},
        )
        productos = []
        for datos_producto in datos["productos"]:
            marca, _ = Marca.objects.get_or_create(nombre=datos_producto["marca"])
            categoria = Categoria.objects.get(slug=datos_producto["categoria"])
            producto, _ = Producto.objects.get_or_create(
                codigo=f"SS-{datos_producto['id']:04d}",
                defaults={
                    "nombre": datos_producto["nombre"], "descripcion": datos_producto["descripcion"],
                    "precio": datos_producto["precio"], "stock": datos_producto["stock"],
                    "imagen": datos_producto["imagen"], "marca": marca,
                    "categoria": categoria, "proveedor": proveedor,
                },
            )
            productos.append(producto)

        clientes = []
        for numero in range(1, 4):
            cliente, _ = Cliente.objects.get_or_create(
                correo=f"cliente-{numero}@example.test",
                defaults={"nombre": fake.name()[:100], "telefono": fake.phone_number()[:20]},
            )
            clientes.append(cliente)
        boleta, _ = Boleta.objects.get_or_create(
            numero=1, defaults={"cliente": clientes[0], "sucursal": sucursal},
        )
        compra, _ = CompraProveedor.objects.get_or_create(
            numero=1, defaults={"proveedor": proveedor, "sucursal": sucursal},
        )
        for producto in productos[:2]:
            DetalleBoleta.objects.get_or_create(
                boleta=boleta, producto=producto,
                defaults={"cantidad": 1, "precio_unitario": producto.precio},
            )
            DetalleCompra.objects.get_or_create(
                compra=compra, producto=producto,
                defaults={"cantidad": 5, "precio_costo": Decimal(producto.precio) * Decimal("0.70")},
            )
        self.stdout.write(self.style.SUCCESS(
            f"Catálogo listo: {Producto.objects.count()} productos, {Categoria.objects.count()} categorías. "
            "Las diez tablas propias contienen datos. No se sobrescribieron registros existentes."
        ))
