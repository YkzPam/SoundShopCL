"""Pruebas del flujo principal sin utilizar base de datos."""

from django.contrib.staticfiles import finders
from django.test import SimpleTestCase
from django.urls import reverse

from .catalogo import filtrar_productos, obtener_producto
from .models import Producto


class CatalogoTests(SimpleTestCase):
    def test_inicio_carga_productos_destacados(self):
        respuesta = self.client.get(reverse("core:inicio"))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Tu próximo sonido")
        self.assertContains(respuesta, "Pulse X ANC")
        self.assertContains(respuesta, "data-theme-toggle")
        self.assertContains(respuesta, "scroll-progress")
        self.assertContains(respuesta, "data-grid-number")

    def test_catalogo_entrega_seis_productos_desde_json(self):
        respuesta = self.client.get(reverse("core:catalogo"))
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.context["cantidad_resultados"], 6)
        self.assertContains(respuesta, "Record Care Kit")

    def test_busqueda_ignora_tildes_y_encuentra_microfono(self):
        resultados = filtrar_productos(consulta="microfono")
        self.assertEqual([producto.nombre for producto in resultados], ["Vela C1"])

    def test_filtros_combinan_categoria_precio_y_stock(self):
        respuesta = self.client.get(
            reverse("core:catalogo"),
            {
                "categoria": "audifonos",
                "precio_maximo": "70000",
                "solo_disponibles": "on",
                "orden": "precio_asc",
            },
        )
        self.assertEqual(respuesta.context["cantidad_resultados"], 1)
        self.assertContains(respuesta, "Studio M40")
        self.assertNotContains(respuesta, "Pulse X ANC")

    def test_detalle_muestra_variables_y_especificaciones(self):
        respuesta = self.client.get(reverse("core:detalle_producto", args=[3]))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Orbit One")
        self.assertContains(respuesta, "33⅓ y 45 RPM")

    def test_identificador_inexistente_redirige_al_catalogo(self):
        respuesta = self.client.get(reverse("core:detalle_producto", args=[999]))
        self.assertRedirects(respuesta, reverse("core:catalogo"), fetch_redirect_response=False)

    def test_datos_json_se_convierten_en_objetos_tipados(self):
        producto = obtener_producto(1)
        self.assertIsInstance(producto, Producto)
        self.assertIsInstance(producto.precio, int)
        self.assertIsInstance(producto.especificaciones, dict)


class CarritoTests(SimpleTestCase):
    def test_agregar_producto_actualiza_carrito(self):
        respuesta = self.client.post(
            reverse("core:agregar_al_carrito", args=[1]),
            {"cantidad": 2},
            follow=True,
        )
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.context["cantidad"], 2)
        self.assertContains(respuesta, "$179.980")

    def test_no_permite_superar_stock(self):
        respuesta = self.client.post(
            reverse("core:agregar_al_carrito", args=[3]),
            {"cantidad": 6},
            follow=True,
        )
        self.assertContains(respuesta, "Solo quedan 5 unidades de Orbit One")
        carrito = self.client.session.get("carrito", {})
        self.assertEqual(carrito, {})

    def test_no_permite_agregar_producto_agotado(self):
        respuesta = self.client.post(
            reverse("core:agregar_al_carrito", args=[4]),
            {"cantidad": 1},
            follow=True,
        )
        self.assertContains(respuesta, "temporalmente sin stock")
        self.assertEqual(self.client.session.get("carrito", {}), {})

    def test_actualizar_y_eliminar_producto(self):
        self.client.post(reverse("core:agregar_al_carrito", args=[5]), {"cantidad": 1})
        self.client.post(reverse("core:actualizar_carrito", args=[5]), {"cantidad": 3})
        respuesta = self.client.post(
            reverse("core:eliminar_del_carrito", args=[5]),
            follow=True,
        )
        self.assertEqual(respuesta.context["cantidad"], 0)
        self.assertContains(respuesta, "El carrito está vacío")

    def test_confirmacion_limpia_carrito(self):
        self.client.post(reverse("core:agregar_al_carrito", args=[1]), {"cantidad": 1})
        respuesta = self.client.post(reverse("core:confirmar_pedido"), follow=True)
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Tu pedido está confirmado")
        self.assertEqual(self.client.session.get("carrito"), {})
        self.assertTrue(self.client.session.get("ultimo_pedido", {}).get("codigo", "").startswith("SSCL-"))

    def test_rutas_de_modificacion_solo_aceptan_post(self):
        respuesta = self.client.get(reverse("core:agregar_al_carrito", args=[1]))
        self.assertEqual(respuesta.status_code, 405)


class ArchivosEstaticosTests(SimpleTestCase):
    def test_tailwind_compilado_esta_disponible(self):
        self.assertIsNotNone(finders.find("css/tailwind.css"))
        self.assertIsNotNone(finders.find("js/main.js"))

    def test_imagenes_del_catalogo_existen(self):
        for ruta in (
            "img/productos/audifonos-pulse-x.webp",
            "img/productos/audifonos-studio-m40.webp",
            "img/productos/tornamesa-orbit-one.webp",
            "img/productos/kit-cuidado-vinilo.webp",
            "img/productos/microfono-vela-c1.webp",
            "img/productos/interfaz-miniwave-2.webp",
        ):
            with self.subTest(ruta=ruta):
                self.assertIsNotNone(finders.find(ruta))


class RegistroTests(SimpleTestCase):
    datos_validos = {
        "nombre": "Benjamin Soto",
        "correo": "benjamin@example.cl",
        "contrasena": "Sonido2026",
        "confirmar_contrasena": "Sonido2026",
        "acepta_terminos": "on",
    }

    def test_formulario_aparece_en_inicio_y_ruta_de_registro(self):
        inicio = self.client.get(reverse("core:inicio"))
        registro = self.client.get(reverse("core:registro"))
        self.assertContains(inicio, "Crea tu cuenta")
        self.assertContains(registro, "Completa tus datos")

    def test_contrasenas_distintas_muestran_error(self):
        datos = self.datos_validos | {"confirmar_contrasena": "OtraClave2026"}
        respuesta = self.client.post(reverse("core:registro"), datos)
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Las contraseñas no coinciden")
        self.assertNotIn("usuario_tienda", self.client.session)

    def test_contrasena_debe_incluir_letra_y_numero(self):
        datos = self.datos_validos | {
            "contrasena": "solonumeros",
            "confirmar_contrasena": "solonumeros",
        }
        respuesta = self.client.post(reverse("core:registro"), datos)
        self.assertContains(respuesta, "Incluye al menos un número")
        self.assertNotIn("usuario_tienda", self.client.session)

    def test_registro_valido_guarda_solo_nombre_visible(self):
        respuesta = self.client.post(reverse("core:registro"), self.datos_validos)
        self.assertRedirects(
            respuesta,
            reverse("core:registro_confirmado"),
            fetch_redirect_response=False,
        )
        sesion = self.client.session
        self.assertEqual(sesion.get("usuario_tienda"), {"nombre": "Benjamin"})
        self.assertNotIn("correo", str(sesion.get("usuario_tienda")))
        self.assertNotIn("Sonido2026", str(dict(sesion.items())))

    def test_confirmacion_requiere_una_cuenta_activa(self):
        respuesta = self.client.get(reverse("core:registro_confirmado"))
        self.assertRedirects(respuesta, reverse("core:registro"), fetch_redirect_response=False)

    def test_cerrar_sesion_elimina_cuenta_local(self):
        self.client.post(reverse("core:registro"), self.datos_validos)
        respuesta = self.client.post(reverse("core:cerrar_sesion"), follow=True)
        self.assertEqual(respuesta.status_code, 200)
        self.assertNotIn("usuario_tienda", self.client.session)
        self.assertContains(respuesta, "La sesión se cerró correctamente")

    def test_interfaz_no_expone_etiquetas_academicas(self):
        for ruta in ("core:inicio", "core:catalogo", "core:categorias", "core:carrito"):
            with self.subTest(ruta=ruta):
                respuesta = self.client.get(reverse(ruta))
                contenido = respuesta.content.decode().lower()
                self.assertNotIn("prototipo académico", contenido)
                self.assertNotIn("compra demostrativa", contenido)
