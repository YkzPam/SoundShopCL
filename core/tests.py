"""Pruebas pequeñas del recorrido de la tienda, sin acceso a BD."""
from pathlib import Path
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.test import Client, SimpleTestCase, override_settings
from django.urls import reverse
from .views import DATA_DIR


ADMIN_USUARIO_PRUEBA = "admin-pruebas@soundshop.local"
ADMIN_CLAVE_PRUEBA = "ClaveUnicaSoloParaTests2026"


@override_settings(
    SOUNDSHOP_ADMIN_ENABLED=True,
    SOUNDSHOP_ADMIN_USERNAME_HASH=make_password(ADMIN_USUARIO_PRUEBA),
    SOUNDSHOP_ADMIN_PASSWORD_HASH=make_password(ADMIN_CLAVE_PRUEBA),
)
class TiendaTests(SimpleTestCase):
    def entrar_admin(self):
        return self.client.post(reverse("core:login"), {
            "correo": ADMIN_USUARIO_PRUEBA, "clave": ADMIN_CLAVE_PRUEBA})

    def datos_producto(self):
        return {"nombre": "Equipo de prueba", "marca": "Marca ejemplo", "categoria": "audifonos",
                "descripcion": "Descripción suficiente del equipo.", "precio": "50000", "stock": "3"}

    def test_paginas_publicas(self):
        for nombre in ["inicio", "catalogo", "categorias", "nosotros", "login", "registro", "carrito"]:
            with self.subTest(pagina=nombre):
                self.assertEqual(self.client.get(reverse("core:" + nombre)).status_code, 200)

    def test_datos_dinamicos(self):
        respuesta = self.client.get(reverse("core:catalogo"))
        self.assertEqual(len(respuesta.context["productos"]), 10)
        self.assertContains(respuesta, "Pulse X ANC")
        self.assertContains(respuesta, "Sin stock")

    def test_busqueda(self):
        respuesta = self.client.get(reverse("core:catalogo"), {"q": "astra"})
        self.assertEqual(len(respuesta.context["productos"]), 1)

    def test_filtro_categoria(self):
        respuesta = self.client.get(reverse("core:catalogo"), {"categoria": "audifonos"})
        self.assertEqual(len(respuesta.context["productos"]), 2)

    def test_busqueda_sin_resultados(self):
        self.assertContains(self.client.get(reverse("core:catalogo"), {"q": "inexistente"}),
                            "No hay productos")

    def test_detalle_y_no_encontrado(self):
        self.assertEqual(self.client.get(reverse("core:detalle_producto", args=[1])).status_code, 200)
        self.assertEqual(self.client.get(reverse("core:detalle_producto", args=[999])).status_code, 404)

    def test_login_cliente(self):
        respuesta = self.client.post(reverse("core:login"), {
            "correo": "cliente@soundshop.example", "clave": "Demo1234"})
        self.assertRedirects(respuesta, reverse("core:cliente"))

    def test_login_administrador(self):
        self.assertRedirects(self.entrar_admin(), reverse("core:gestion"))

    def test_acceso_admin_identificado(self):
        respuesta = self.client.get(reverse("core:login_admin"))
        self.assertContains(respuesta, "<h1>Panel de administración</h1>", html=True)
        self.assertContains(respuesta, "Entrar al panel")
        self.assertNotContains(respuesta, "Ver formulario de registro")
        respuesta_cliente = self.client.get(reverse("core:login"))
        self.assertContains(respuesta_cliente, "<h1>Iniciar sesión</h1>", html=True)
        self.assertContains(respuesta_cliente, "Ver formulario de registro")

    def test_acceso_admin_acepta_credenciales_privadas(self):
        respuesta = self.client.post(reverse("core:login_admin"), {
            "correo": ADMIN_USUARIO_PRUEBA, "clave": ADMIN_CLAVE_PRUEBA})
        self.assertRedirects(respuesta, reverse("core:gestion"))

    def test_acceso_admin_rechaza_cuenta_cliente(self):
        respuesta = self.client.post(reverse("core:login_admin"), {
            "correo": "cliente@soundshop.example", "clave": "Demo1234"})
        self.assertContains(respuesta, "no son correctos")
        self.assertNotIn("rol", self.client.session)

    def test_admin_con_sesion_abre_panel_directamente(self):
        self.entrar_admin()
        self.assertRedirects(self.client.get(reverse("core:login_admin")), reverse("core:gestion"))

    def test_login_incorrecto(self):
        respuesta = self.client.post(reverse("core:login"), {
            "correo": ADMIN_USUARIO_PRUEBA, "clave": "incorrecta"})
        self.assertContains(respuesta, "no son correctos")
        self.assertNotIn("rol", self.client.session)

    def test_antiguo_admin_publico_no_ingresa(self):
        respuesta = self.client.post(reverse("core:login"), {
            "correo": "admin@soundshop.example", "clave": "Demo1234"})
        self.assertEqual(respuesta.status_code, 200)
        self.assertNotIn("rol", self.client.session)

    def test_login_vacio(self):
        respuesta = self.client.post(reverse("core:login"), {})
        self.assertTrue(respuesta.context["formulario"].errors)
        self.assertContains(respuesta, 'aria-invalid="true"')

    def test_restriccion_admin(self):
        for nombre in ["gestion", "gestion_productos", "gestion_usuarios", "producto_nuevo"]:
            self.assertRedirects(self.client.get(reverse("core:" + nombre)), reverse("core:login_admin"))
        self.client.post(reverse("core:login"), {"correo": "cliente@soundshop.example", "clave": "Demo1234"})
        self.assertRedirects(self.client.get(reverse("core:gestion")), reverse("core:login_admin"))

    def test_rol_sin_verificacion_no_abre_admin(self):
        sesion = self.client.session
        sesion["rol"] = "administrador"
        sesion.save()
        self.assertRedirects(self.client.get(reverse("core:gestion")), reverse("core:login_admin"))

    def test_login_no_muestra_claves_publicas(self):
        respuesta = self.client.get(reverse("core:login"))
        self.assertNotContains(respuesta, "Demo1234")
        self.assertNotContains(respuesta, "admin@soundshop.example")
        self.assertNotContains(respuesta, "Evaluación 1")

    def test_paginas_sin_rotulos_academicos(self):
        rutas_publicas = ["inicio", "catalogo", "categorias", "nosotros",
                          "login", "registro", "carrito"]
        for nombre in rutas_publicas:
            with self.subTest(pagina=nombre):
                contenido = self.client.get(reverse("core:" + nombre)).content.decode()
                self.assertNotRegex(contenido, r"Evaluaci[oó]n 1|de ejemplo|Demo1234")
        self.entrar_admin()
        for nombre in ["gestion", "gestion_productos", "gestion_usuarios", "producto_nuevo"]:
            with self.subTest(pagina=nombre):
                contenido = self.client.get(reverse("core:" + nombre)).content.decode()
                self.assertNotRegex(contenido, r"Evaluaci[oó]n 1|de ejemplo|Demo1234")

    def test_paginas_admin(self):
        self.entrar_admin()
        for nombre in ["gestion", "gestion_productos", "gestion_usuarios", "producto_nuevo"]:
            self.assertEqual(self.client.get(reverse("core:" + nombre)).status_code, 200)
        respuesta = self.client.get(reverse("core:producto_editar", args=[1]))
        self.assertEqual(respuesta.context["formulario"].initial["nombre"], "Pulse X ANC")

    def test_producto_valido_no_modifica_json(self):
        self.entrar_admin()
        antes = (DATA_DIR / "catalogo.json").read_bytes()
        respuesta = self.client.post(reverse("core:producto_nuevo"), self.datos_producto())
        self.assertContains(respuesta, "Vista previa validada")
        self.assertEqual(respuesta.context["resultado"]["precio"], 50000)
        self.assertEqual(antes, (DATA_DIR / "catalogo.json").read_bytes())

    def test_producto_invalido(self):
        self.entrar_admin()
        datos = self.datos_producto()
        datos.update(precio="-1", stock="-2", categoria="no-existe", nombre="  ")
        respuesta = self.client.post(reverse("core:producto_nuevo"), datos)
        self.assertIsNone(respuesta.context["resultado"])
        for campo in ["precio", "stock", "categoria", "nombre"]:
            self.assertIn(campo, respuesta.context["formulario"].errors)

    def test_registro_con_claves_diferentes(self):
        respuesta = self.client.post(reverse("core:registro"), {
            "nombre": "Cliente ejemplo", "correo": "nuevo@example.com",
            "clave": "Demo1234", "confirmar": "Otra1234"})
        self.assertContains(respuesta, "deben coincidir")

    def test_registro_valido_no_guarda_cuenta(self):
        antes = (DATA_DIR / "usuarios.json").read_bytes()
        respuesta = self.client.post(reverse("core:registro"), {
            "nombre": "Cliente ejemplo", "correo": "nuevo@example.com",
            "clave": "Demo1234", "confirmar": "Demo1234"})
        self.assertContains(respuesta, "Datos de registro validados")
        self.assertNotContains(respuesta, 'value="Demo1234"')
        self.assertEqual(antes, (DATA_DIR / "usuarios.json").read_bytes())

    def test_usuario_correo_duplicado(self):
        self.entrar_admin()
        respuesta = self.client.post(reverse("core:gestion_usuarios"), {
            "nombre": "Cliente ejemplo", "correo": "cliente@soundshop.example", "rol": "cliente"})
        self.assertIn("correo", respuesta.context["formulario"].errors)

    def test_usuario_valido_y_estado_booleano(self):
        self.entrar_admin()
        antes = (DATA_DIR / "usuarios.json").read_bytes()
        respuesta = self.client.post(reverse("core:gestion_usuarios"), {
            "nombre": "Cliente ejemplo", "correo": "nuevo@example.com", "rol": "cliente"})
        self.assertIs(respuesta.context["resultado"]["activo"], False)
        self.assertEqual(antes, (DATA_DIR / "usuarios.json").read_bytes())

    def test_carrito_invitado_y_total(self):
        self.client.post(reverse("core:agregar_carrito", args=[1]))
        respuesta = self.client.get(reverse("core:carrito"))
        self.assertEqual(respuesta.context["total"], 89990)
        self.assertEqual(respuesta.context["lineas"][0]["cantidad"], 1)

    def test_carrito_stock_y_get_sin_mutacion(self):
        self.client.get(reverse("core:agregar_carrito", args=[1]))
        self.client.post(reverse("core:agregar_carrito", args=[4]))
        self.assertEqual(self.client.session.get("carrito", {}), {})
        for _ in range(9):
            self.client.post(reverse("core:agregar_carrito", args=[1]))
        self.assertEqual(self.client.session["carrito"]["1"], 8)

    def test_quitar_y_confirmar(self):
        self.client.post(reverse("core:agregar_carrito", args=[1]))
        self.assertRedirects(self.client.post(reverse("core:confirmar")), reverse("core:login"))
        self.entrar_admin()
        respuesta = self.client.post(reverse("core:confirmar"))
        self.assertContains(respuesta, "No se efectuó un pago")
        self.assertEqual(self.client.session["carrito"], {})
        self.client.post(reverse("core:agregar_carrito", args=[1]))
        self.client.post(reverse("core:quitar_carrito", args=[1]))
        self.assertEqual(self.client.session["carrito"], {})

    def test_csrf_y_salida(self):
        seguro = Client(enforce_csrf_checks=True)
        self.assertEqual(seguro.post(reverse("core:agregar_carrito", args=[1])).status_code, 403)
        self.entrar_admin()
        self.client.post(reverse("core:salir"))
        self.assertNotIn("rol", self.client.session)
        self.assertNotIn("admin_revision", self.client.session)

    def test_sin_base_de_datos(self):
        self.assertEqual(settings.DATABASES["default"]["ENGINE"], "django.db.backends.dummy")
        self.assertFalse((Path(settings.BASE_DIR) / "db.sqlite3").exists())
