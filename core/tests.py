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

    def test_confirmacion_simulada_limpia_carrito(self):
        self.client.post(reverse("core:agregar_al_carrito", args=[1]), {"cantidad": 1})
        respuesta = self.client.post(reverse("core:confirmar_pedido"), follow=True)
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Pedido simulado confirmado")
        self.assertEqual(self.client.session.get("carrito"), {})
        self.assertTrue(self.client.session.get("ultimo_pedido", {}).get("codigo", "").startswith("SSCL-"))

    def test_rutas_de_modificacion_solo_aceptan_post(self):
        respuesta = self.client.get(reverse("core:agregar_al_carrito", args=[1]))
        self.assertEqual(respuesta.status_code, 405)


class ArchivosEstaticosTests(SimpleTestCase):
    def test_tailwind_compilado_esta_disponible(self):
        self.assertIsNotNone(finders.find("css/tailwind.css"))

    def test_imagenes_del_catalogo_existen(self):
        for ruta in (
            "img/productos/audifonos-pulse-x.png",
            "img/productos/tornamesa-orbit-one.png",
            "img/productos/microfono-vela-c1.png",
        ):
            with self.subTest(ruta=ruta):
                self.assertIsNotNone(finders.find(ruta))
