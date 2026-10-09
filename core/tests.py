"""Pruebas de SQLite, modelos y operaciones del administrador de Django."""
import json
from io import StringIO
from pathlib import Path
from django.apps import apps
from django.contrib import admin
from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db import connection
from django.db.models.deletion import ProtectedError
from django.test import TestCase
from django.urls import reverse
from .models import Categoria, Cliente, Producto, Boleta, DetalleBoleta


class Evaluacion2Tests(TestCase):
    def setUp(self):
        call_command("cargar_catalogo", stdout=StringIO())
        self.usuario = User.objects.create_superuser(
            username="admin_tests", email="admin@example.test", password="SoloParaPruebas2026")
        self.producto = Producto.objects.first()
        self.client.force_login(self.usuario)

    def datos_producto(self):
        return {
            "codigo": "SS-TEST", "nombre": "Audífonos de prueba",
            "descripcion": "Equipo ficticio para comprobar el administrador.",
            "precio": "50000.00", "stock": "4", "activo": "on",
            "categoria": str(self.producto.categoria_id),
            "marca": str(self.producto.marca_id),
            "proveedor": str(self.producto.proveedor_id), "imagen": "",
        }

    def datos_cliente(self):
        return {
            "nombre": "Cliente de prueba E2", "correo": "crud-cliente@example.test",
            "telefono": "+56911112222", "activo": "on",
        }

    def test_conexion_sqlite_y_diez_tablas(self):
        self.assertEqual(connection.vendor, "sqlite")
        tablas = [t for t in connection.introspection.table_names() if t.startswith("core_")]
        self.assertEqual(len(tablas), 10)
        with connection.cursor() as cursor:
            cursor.execute("PRAGMA foreign_keys")
            self.assertEqual(cursor.fetchone()[0], 1)

    def test_diez_modelos_registrados_y_con_datos(self):
        modelos = list(apps.get_app_config("core").get_models())
        self.assertEqual(len(modelos), 10)
        for modelo in modelos:
            with self.subTest(modelo=modelo.__name__):
                self.assertIn(modelo, admin.site._registry)
                self.assertTrue(modelo.objects.exists())

    def test_diez_migraciones_aplicadas_y_sin_cambios_pendientes(self):
        ruta = Path(__file__).resolve().parent / "migrations"
        self.assertEqual(len(list(ruta.glob("[0-9]*.py"))), 10)
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM django_migrations WHERE app = 'core'")
            self.assertEqual(cursor.fetchone()[0], 10)
        call_command("makemigrations", "core", check=True, dry_run=True, stdout=StringIO())

    def test_diagrama_corresponde_a_los_modelos(self):
        ruta = Path(__file__).resolve().parents[1] / "docs" / "evaluacion-2" / "esquema.json"
        with ruta.open(encoding="utf-8") as archivo:
            esquema = json.load(archivo)
        self.assertEqual(len(esquema), 10)
        for tabla in esquema:
            modelo = apps.get_model("core", tabla["modelo"])
            self.assertEqual(tabla["tabla"], modelo._meta.db_table)
            self.assertEqual(
                [campo["columna"] for campo in tabla["campos"]],
                [campo.column for campo in modelo._meta.fields],
            )
            for dato, campo in zip(tabla["campos"], modelo._meta.fields):
                self.assertEqual(dato["tipo"], campo.db_type(connection))
                self.assertEqual(dato["pk"], campo.primary_key)
                destino = campo.related_model._meta.model_name if campo.is_relation else None
                self.assertEqual(dato["fk"], destino)

    def test_acceso_admin_y_listados(self):
        self.assertContains(self.client.get(reverse("admin:index")), "SoundShop CL")
        for modelo in apps.get_app_config("core").get_models():
            ruta = reverse("admin:core_" + modelo._meta.model_name + "_changelist")
            self.assertEqual(self.client.get(ruta).status_code, 200)

    def test_invitado_no_entra_admin(self):
        self.client.logout()
        respuesta = self.client.get(reverse("admin:index"))
        self.assertEqual(respuesta.status_code, 302)
        self.assertIn("/admin/login/", respuesta.url)

    def test_cliente_sin_staff_no_entra_admin(self):
        cliente = User.objects.create_user(username="sin_permisos", password="SoloTests2026")
        self.client.force_login(cliente)
        self.assertEqual(self.client.get(reverse("admin:index")).status_code, 302)

    def test_crear_cliente_desde_admin(self):
        respuesta = self.client.post(reverse("admin:core_cliente_add"), self.datos_cliente())
        self.assertEqual(respuesta.status_code, 302)
        nuevo = Cliente.objects.get(correo="crud-cliente@example.test")
        self.assertEqual(nuevo.nombre, "Cliente de prueba E2")
        self.assertEqual(nuevo.telefono, "+56911112222")
        self.assertTrue(nuevo.activo)

    def test_consulta_busqueda_y_filtro_clientes_admin(self):
        cliente = Cliente.objects.create(
            nombre="Cliente consulta E2", correo="consulta-cliente@example.test",
            telefono="", activo=False,
        )
        respuesta = self.client.get(reverse("admin:core_cliente_changelist"), {"q": cliente.correo})
        self.assertContains(respuesta, cliente.nombre)
        self.assertEqual(respuesta.context["cl"].result_count, 1)
        respuesta = self.client.get(reverse("admin:core_cliente_changelist"), {"activo__exact": "0"})
        self.assertContains(respuesta, cliente.nombre)
        self.assertEqual(respuesta.context["cl"].result_count, 1)

    def test_modificar_cliente_desde_admin(self):
        self.client.post(reverse("admin:core_cliente_add"), self.datos_cliente())
        cliente = Cliente.objects.get(correo="crud-cliente@example.test")
        datos = self.datos_cliente()
        datos["nombre"] = "Cliente actualizado"
        datos["telefono"] = "+56933334444"
        del datos["activo"]
        respuesta = self.client.post(reverse("admin:core_cliente_change", args=[cliente.id]), datos)
        self.assertEqual(respuesta.status_code, 302)
        cliente.refresh_from_db()
        self.assertEqual(cliente.nombre, "Cliente actualizado")
        self.assertEqual(cliente.telefono, "+56933334444")
        self.assertFalse(cliente.activo)
        self.assertContains(
            self.client.get(reverse("admin:core_cliente_change", args=[cliente.id])),
            "Cliente actualizado",
        )

    def test_eliminar_cliente_desde_admin(self):
        antes = Cliente.objects.count()
        self.client.post(reverse("admin:core_cliente_add"), self.datos_cliente())
        cliente = Cliente.objects.get(correo="crud-cliente@example.test")
        respuesta = self.client.post(reverse("admin:core_cliente_delete", args=[cliente.id]), {"post": "yes"})
        self.assertEqual(respuesta.status_code, 302)
        self.assertFalse(Cliente.objects.filter(correo="crud-cliente@example.test").exists())
        self.assertEqual(Cliente.objects.count(), antes)

    def test_cliente_admin_rechaza_correo_invalido(self):
        antes = Cliente.objects.count()
        datos = self.datos_cliente()
        datos["correo"] = "correo-sin-formato"
        respuesta = self.client.post(reverse("admin:core_cliente_add"), datos)
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn("correo", respuesta.context["adminform"].form.errors)
        self.assertEqual(Cliente.objects.count(), antes)

    def test_cliente_admin_rechaza_correo_duplicado(self):
        antes = Cliente.objects.count()
        existente = Cliente.objects.first()
        datos = self.datos_cliente()
        datos["correo"] = existente.correo
        respuesta = self.client.post(reverse("admin:core_cliente_add"), datos)
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn("correo", respuesta.context["adminform"].form.errors)
        self.assertEqual(Cliente.objects.filter(correo=existente.correo).count(), 1)
        self.assertEqual(Cliente.objects.count(), antes)

    def test_admin_no_elimina_cliente_con_boleta(self):
        boleta = Boleta.objects.first()
        cliente = boleta.cliente
        antes = Cliente.objects.count()
        respuesta = self.client.post(reverse("admin:core_cliente_delete", args=[cliente.id]), {"post": "yes"})
        self.assertEqual(respuesta.status_code, 200)
        self.assertTrue(respuesta.context["protected"])
        self.assertTrue(Cliente.objects.filter(id=cliente.id).exists())
        self.assertTrue(Boleta.objects.filter(id=boleta.id).exists())
        self.assertEqual(Cliente.objects.count(), antes)

    def test_admin_elimina_boleta_y_detalles_sin_borrar_cliente_ni_productos(self):
        boleta = Boleta.objects.first()
        cliente_id = boleta.cliente_id
        productos_antes = Producto.objects.count()
        self.assertTrue(DetalleBoleta.objects.filter(boleta_id=boleta.id).exists())
        respuesta = self.client.post(reverse("admin:core_boleta_delete", args=[boleta.id]), {"post": "yes"})
        self.assertEqual(respuesta.status_code, 302)
        self.assertFalse(Boleta.objects.filter(id=boleta.id).exists())
        self.assertFalse(DetalleBoleta.objects.filter(boleta_id=boleta.id).exists())
        self.assertTrue(Cliente.objects.filter(id=cliente_id).exists())
        self.assertEqual(Producto.objects.count(), productos_antes)

    def test_crear_producto_desde_admin(self):
        respuesta = self.client.post(reverse("admin:core_producto_add"), self.datos_producto())
        self.assertEqual(respuesta.status_code, 302)
        nuevo = Producto.objects.get(codigo="SS-TEST")
        self.assertEqual(nuevo.stock, 4)
        self.assertEqual(nuevo.nombre, "Audífonos de prueba")

    def test_consulta_busqueda_y_filtro_admin(self):
        respuesta = self.client.get(reverse("admin:core_producto_changelist"), {"q": self.producto.codigo})
        self.assertContains(respuesta, self.producto.nombre)
        self.assertEqual(respuesta.context["cl"].result_count, 1)
        respuesta = self.client.get(reverse("admin:core_producto_changelist"), {"activo__exact": "0"})
        self.assertEqual(respuesta.context["cl"].result_count, 0)

    def test_modificar_producto_y_reflejar_en_tienda(self):
        datos = self.datos_producto()
        datos["codigo"] = self.producto.codigo
        datos["nombre"] = "Nombre actualizado"
        respuesta = self.client.post(reverse("admin:core_producto_change", args=[self.producto.id]), datos)
        self.assertEqual(respuesta.status_code, 302)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.nombre, "Nombre actualizado")
        self.assertContains(self.client.get(reverse("core:catalogo")), "Nombre actualizado")

    def test_eliminar_producto_desde_admin(self):
        self.client.post(reverse("admin:core_producto_add"), self.datos_producto())
        nuevo = Producto.objects.get(codigo="SS-TEST")
        respuesta = self.client.post(reverse("admin:core_producto_delete", args=[nuevo.id]), {"post": "yes"})
        self.assertEqual(respuesta.status_code, 302)
        self.assertFalse(Producto.objects.filter(codigo="SS-TEST").exists())

    def test_validaciones_admin_precio_y_codigo(self):
        datos = self.datos_producto()
        datos["precio"] = "-1"
        respuesta = self.client.post(reverse("admin:core_producto_add"), datos)
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn("precio", respuesta.context["adminform"].form.errors)
        self.assertFalse(Producto.objects.filter(codigo="SS-TEST").exists())
        datos["precio"] = "50000"
        datos["codigo"] = self.producto.codigo
        respuesta = self.client.post(reverse("admin:core_producto_add"), datos)
        self.assertIn("codigo", respuesta.context["adminform"].form.errors)

    def test_relaciones_y_precio_historico(self):
        detalle = DetalleBoleta.objects.first()
        historico = detalle.subtotal
        detalle.producto.precio += 10000
        detalle.producto.save()
        detalle.refresh_from_db()
        self.assertEqual(detalle.subtotal, historico)
        self.assertIn(detalle.producto, detalle.boleta.productos.all())
        with self.assertRaises(ProtectedError):
            detalle.producto.delete()

    def test_seed_no_duplica_ni_sobrescribe(self):
        self.producto.nombre = "Edición conservada"
        self.producto.save()
        call_command("cargar_catalogo", stdout=StringIO())
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.nombre, "Edición conservada")
        self.assertEqual(Producto.objects.count(), 10)
        self.assertEqual(Categoria.objects.count(), 5)

    def test_faker_almacena_cantidad(self):
        antes = Cliente.objects.count()
        salida = StringIO()
        call_command("generar_clientes", cantidad=12, stdout=salida)
        self.assertEqual(Cliente.objects.count() - antes, 12)
        self.assertIn(f"archivo SQLite: {connection.settings_dict['NAME']}", salida.getvalue())
        self.assertIn("VERIFICADO", salida.getvalue())

    def test_faker_rechaza_cantidad_invalida(self):
        with self.assertRaises(CommandError):
            call_command("generar_clientes", cantidad=0, stdout=StringIO())

    def test_paginas_y_enlaces_anteriores(self):
        for nombre in ("inicio", "catalogo", "categorias", "nosotros", "login", "registro", "carrito"):
            self.assertEqual(self.client.get(reverse("core:" + nombre)).status_code, 200)
        self.assertRedirects(self.client.get(reverse("core:gestion")), reverse("admin:index"))
        self.assertRedirects(self.client.get(reverse("core:login_admin")), reverse("admin:index"))
