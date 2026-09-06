"""Pruebas del flujo principal sin utilizar base de datos."""

from django.conf import settings
from django.core.cache import caches
from django.contrib.staticfiles import finders
from django.test import SimpleTestCase
from django.urls import reverse

from .catalogo import categorias_con_resumen, filtrar_productos, obtener_producto
from .models import Producto


def guardar_sesion_cliente(cliente, **datos):
    sesion = cliente.session
    sesion.update(datos)
    sesion.save()
    cliente.cookies[settings.SESSION_COOKIE_NAME] = sesion.session_key


class CatalogoTests(SimpleTestCase):
    def test_inicio_carga_presentacion_simple_y_rutas(self):
        respuesta = self.client.get(reverse("core:inicio"))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Encuentra tu")
        self.assertContains(respuesta, "Astra Seven")
        self.assertContains(respuesta, "data-theme-toggle")
        self.assertContains(respuesta, "scroll-progress")
        self.assertContains(respuesta, "data-grid-number")
        self.assertNotContains(respuesta, "data-scroll-cue")
        self.assertContains(respuesta, "home-hero__image")
        self.assertNotContains(respuesta, "home-section-nav")
        self.assertContains(respuesta, "css/identity.css")
        self.assertContains(respuesta, 'aria-label="Navegación principal"', count=1)
        self.assertContains(respuesta, 'href="/nosotros/"')
        self.assertNotContains(respuesta, 'href="#nosotros"')
        self.assertNotContains(respuesta, 'href="#registro"')
        self.assertNotContains(respuesta, 'class="account-section"')
        self.assertNotContains(respuesta, "category-tile__media")
        self.assertNotContains(respuesta, "editorial-section")
        self.assertNotContains(respuesta, "featured-section")
        self.assertEqual(respuesta.content.decode().count('src="/static/img/'), 7)
        self.assertContains(respuesta, 'src="/static/img/footer-audio-culture.jpg"', count=1)
        self.assertContains(respuesta, 'Que suene<br><em>a ti.</em>')
        self.assertNotContains(respuesta, "about-section")
        self.assertContains(respuesta, "Nosotros")
        self.assertContains(respuesta, "data-quick-view-dialog")
        self.assertContains(respuesta, "data-mini-cart")

    def test_catalogo_entrega_diez_productos_desde_json(self):
        respuesta = self.client.get(reverse("core:catalogo"))
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.context["cantidad_resultados"], 10)
        self.assertContains(respuesta, "Record Care Kit")
        self.assertContains(respuesta, "Astra Seven")

    def test_categorias_usan_imagenes_y_rutas_editoriales(self):
        respuesta = self.client.get(reverse("core:categorias"))
        self.assertEqual(respuesta.status_code, 200)
        self.assertTemplateUsed(respuesta, "includes/category_tiles.html")
        self.assertContains(respuesta, "category-tile__thumbnail", count=5)
        self.assertContains(respuesta, "Escuchar sin distracciones")
        self.assertContains(respuesta, "Preparar el escenario")

    def test_colecciones_comparten_presentacion_y_conservan_su_filtro(self):
        for resumen in categorias_con_resumen():
            categoria = resumen["categoria"]
            with self.subTest(categoria=categoria.slug):
                respuesta = self.client.get(
                    reverse("core:detalle_categoria", args=[categoria.slug]),
                    {"categoria": "otra-categoria", "orden": "precio_asc"},
                )
                self.assertEqual(respuesta.status_code, 200)
                self.assertEqual(respuesta.context["coleccion_visual"], resumen)
                self.assertTemplateUsed(respuesta, "includes/collection_hero.html")
                self.assertContains(respuesta, resumen["titular"])
                self.assertContains(respuesta, resumen["enfasis"])
                self.assertContains(respuesta, 'class="collection-guide__item"', count=2)
                self.assertContains(respuesta, "collection-tabs")
                self.assertTemplateNotUsed(respuesta, "includes/section_nav.html")
                self.assertContains(respuesta, "css/identity.css")
                productos = respuesta.context["productos"]
                self.assertEqual(len(productos), resumen["cantidad"])
                self.assertTrue(all(p.categoria == categoria.slug for p in productos))
                self.assertEqual([p.precio for p in productos], sorted(p.precio for p in productos))

    def test_nosotros_tiene_ruta_propia_y_navegacion_consistente(self):
        respuesta = self.client.get(reverse("core:nosotros"))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "sentir el sonido.")
        self.assertNotContains(respuesta, 'class="home-hero"')
        self.assertEqual(respuesta.context["cantidad_productos"], 10)
        self.assertEqual(respuesta.context["cantidad_categorias"], 5)
        for ruta in ("core:inicio", "core:nosotros", "core:catalogo", "core:categorias", "core:registro", "core:carrito"):
            with self.subTest(ruta=ruta):
                pagina = self.client.get(reverse(ruta))
                self.assertContains(pagina, 'href="/nosotros/"', count=3)
                self.assertNotContains(pagina, 'href="/#nosotros"')
                self.assertContains(pagina, "data-motion-toggle")

    def test_busqueda_ignora_tildes_y_encuentra_equipos_de_microfono(self):
        resultados = filtrar_productos(consulta="microfono")
        self.assertEqual(
            [producto.nombre for producto in resultados],
            ["Vela C1", "MixLab 8"],
        )

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
        self.assertEqual(respuesta.context["formulario"].fields["precio_maximo"].widget.attrs["step"], "1")
        self.assertContains(respuesta, "Studio M40")
        self.assertNotContains(respuesta, "Pulse X ANC")

    def test_detalle_muestra_variables_y_especificaciones(self):
        guardar_sesion_cliente(self.client, usuario_tienda={"nombre": "Benjamin"})
        respuesta = self.client.get(reverse("core:detalle_producto", args=[3]))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Orbit One")
        self.assertContains(respuesta, "33⅓ y 45 RPM")
        self.assertContains(respuesta, "data-image-viewer-open")
        self.assertContains(respuesta, "data-ajax-cart")

    def test_identificador_inexistente_redirige_al_catalogo(self):
        respuesta = self.client.get(reverse("core:detalle_producto", args=[999]))
        self.assertRedirects(respuesta, reverse("core:catalogo"), fetch_redirect_response=False)

    def test_datos_json_se_convierten_en_objetos_tipados(self):
        producto = obtener_producto(1)
        self.assertIsInstance(producto, Producto)
        self.assertIsInstance(producto.precio, int)
        self.assertIsInstance(producto.especificaciones, dict)


class CarritoTests(SimpleTestCase):
    def setUp(self):
        guardar_sesion_cliente(self.client, usuario_tienda={"nombre": "Benjamin"})

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

    def test_agregar_por_ajax_devuelve_resumen_para_mini_carrito(self):
        respuesta = self.client.post(
            reverse("core:agregar_al_carrito", args=[1]),
            {"cantidad": 2},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(respuesta.status_code, 200)
        datos = respuesta.json()
        self.assertTrue(datos["ok"])
        self.assertEqual(datos["cantidad"], 2)
        self.assertEqual(datos["total_formateado"], "$179.980")
        self.assertEqual(datos["lineas"][0]["nombre"], "Pulse X ANC")
        self.assertEqual(datos["producto_agregado"]["cantidad_en_carrito"], 2)

    def test_error_ajax_informa_stock_sin_modificar_carrito(self):
        respuesta = self.client.post(
            reverse("core:agregar_al_carrito", args=[3]),
            {"cantidad": 6},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(respuesta.status_code, 400)
        datos = respuesta.json()
        self.assertFalse(datos["ok"])
        self.assertIn("Solo quedan 5 unidades", datos["mensaje"])
        self.assertEqual(datos["cantidad"], 0)
        self.assertEqual(self.client.session.get("carrito", {}), {})

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
            "img/productos/guitarra-astra-seven.webp",
            "img/productos/controlador-keyline-49.webp",
            "img/productos/parlante-atlas-10.webp",
            "img/productos/mezclador-mixlab-8.webp",
        ):
            with self.subTest(ruta=ruta):
                self.assertIsNotNone(finders.find(ruta))


class RegistroTests(SimpleTestCase):
    def setUp(self):
        caches['cuentas'].clear()

    datos_validos = {
        "nombre": "Benjamin Soto",
        "correo": "benjamin@example.cl",
        "contrasena": "Sonido2026",
        "confirmar_contrasena": "Sonido2026",
        "acepta_terminos": "on",
    }

    def test_acceso_separado_y_sin_bloque_en_inicio(self):
        inicio = self.client.get(reverse("core:inicio"))
        registro = self.client.get(reverse("core:registro"))
        self.assertNotContains(inicio, "Inicia sesión para comprar")
        self.assertContains(registro, 'name="accion" value="ingresar"')
        self.assertNotContains(registro, 'name="confirmar_contrasena"')
        crear = self.client.get(reverse('core:registro'), {'modo': 'crear'})
        self.assertContains(crear, 'name="confirmar_contrasena"')
        self.assertContains(crear, "Completa tus datos")

    def test_ingreso_despues_de_cerrar_sesion(self):
        self.client.post(reverse('core:registro'), self.datos_validos)
        self.client.post(reverse('core:cerrar_sesion'))
        respuesta = self.client.post(reverse('core:registro'), {
            'accion': 'ingresar', 'correo': 'BENJAMIN@example.cl',
            'contrasena': 'Sonido2026', 'next': '/productos/7/',
        })
        self.assertRedirects(respuesta, '/productos/7/', fetch_redirect_response=False)
        self.assertEqual(self.client.session['usuario_tienda'], {'nombre': 'Benjamin'})

    def test_ingreso_incorrecto_no_abre_sesion(self):
        self.client.post(reverse('core:registro'), self.datos_validos)
        self.client.post(reverse('core:cerrar_sesion'))
        for correo in ('benjamin@example.cl', 'desconocido@example.cl'):
            respuesta = self.client.post(reverse('core:registro'), {
                'accion': 'ingresar', 'correo': correo, 'contrasena': 'Incorrecta123',
            })
            self.assertContains(respuesta, 'El correo o la contraseña no coinciden')
            self.assertNotIn('usuario_tienda', self.client.session)

    def test_no_sobrescribe_una_cuenta_existente(self):
        self.client.post(reverse('core:registro'), self.datos_validos)
        self.client.post(reverse('core:cerrar_sesion'))
        respuesta = self.client.post(reverse('core:registro'), self.datos_validos)
        self.assertContains(respuesta, 'Este correo ya tiene una cuenta')
        self.assertNotIn('usuario_tienda', self.client.session)

    def test_login_conserva_destino_y_rechaza_destino_externo(self):
        pagina = self.client.get(reverse('core:registro'), {'next': '/productos/7/'})
        self.assertContains(pagina, 'next=/productos/7/')
        self.client.post(reverse('core:registro'), self.datos_validos)
        self.client.post(reverse('core:cerrar_sesion'))
        respuesta = self.client.post(reverse('core:registro'), {
            'accion': 'ingresar', 'correo': 'benjamin@example.cl',
            'contrasena': 'Sonido2026', 'next': 'https://externo.invalid/',
        })
        self.assertRedirects(respuesta, reverse('core:registro_confirmado'), fetch_redirect_response=False)

    def test_limita_intentos_y_no_incluye_hash_en_cookie(self):
        from .cuentas import clave_correo
        self.client.post(reverse('core:registro'), self.datos_validos)
        cuenta = caches['cuentas'].get('cuenta:' + clave_correo('benjamin@example.cl'))
        self.assertNotEqual(cuenta['clave'], self.datos_validos['contrasena'])
        self.assertNotIn(cuenta['clave'], str(dict(self.client.session)))
        self.client.post(reverse('core:cerrar_sesion'))
        caches['cuentas'].set('intentos:' + clave_correo('benjamin@example.cl'), 5, 300)
        respuesta = self.client.post(reverse('core:registro'), {
            'accion': 'ingresar', 'correo': 'benjamin@example.cl', 'contrasena': 'Sonido2026',
        })
        self.assertContains(respuesta, 'Demasiados intentos')
        self.assertNotIn('usuario_tienda', self.client.session)

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
        inicio = self.client.get(reverse("core:inicio"))
        self.assertContains(inicio, f'href="{reverse("core:registro_confirmado")}"')

    def test_registro_regresa_a_un_producto_cuando_next_es_local(self):
        destino = reverse("core:detalle_producto", args=[7])
        respuesta = self.client.post(
            reverse("core:registro"),
            self.datos_validos | {"next": destino},
        )
        self.assertRedirects(respuesta, destino, fetch_redirect_response=False)
        self.assertEqual(self.client.session.get("usuario_tienda"), {"nombre": "Benjamin"})

    def test_registro_rechaza_un_next_externo(self):
        respuesta = self.client.post(
            reverse("core:registro"),
            self.datos_validos | {"next": "https://ejemplo-malicioso.invalid/"},
        )
        self.assertRedirects(
            respuesta,
            reverse("core:registro_confirmado"),
            fetch_redirect_response=False,
        )

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


class SesionCompraTests(SimpleTestCase):
    def test_ficha_anonima_permite_agregar_sin_bloque_de_acceso(self):
        respuesta = self.client.get(reverse("core:detalle_producto", args=[7]))
        self.assertNotContains(respuesta, "Inicia sesión para comprar")
        self.assertNotContains(respuesta, "purchase-lock")
        self.assertContains(respuesta, "data-ajax-cart")
        self.assertContains(respuesta, "Agregar al carrito")

    def test_publicacion_anonima_agrega_y_abre_carrito(self):
        respuesta = self.client.post(
            reverse("core:agregar_al_carrito", args=[1]),
            {"cantidad": 1},
        )
        destino = reverse("core:carrito")
        self.assertRedirects(respuesta, destino, fetch_redirect_response=False)
        self.assertEqual(self.client.session.get("carrito"), {"1": 1})
        self.assertNotIn("usuario_tienda", self.client.session)

    def test_publicacion_ajax_anonima_agrega_y_actualiza_mini_carrito(self):
        respuesta = self.client.post(
            reverse("core:agregar_al_carrito", args=[1]),
            {"cantidad": 1},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(respuesta.status_code, 200)
        datos = respuesta.json()
        self.assertTrue(datos["ok"])
        self.assertFalse(datos["requiere_sesion"])
        self.assertEqual(datos["cantidad"], 1)
        self.assertEqual(datos["producto_agregado"]["id"], 1)
        self.assertEqual(self.client.session.get("carrito"), {"1": 1})

    def test_confirmacion_anonima_con_carrito_redirige_al_acceso(self):
        guardar_sesion_cliente(self.client, carrito={"1": 1})
        respuesta = self.client.post(reverse("core:confirmar_pedido"))
        destino = f'{reverse("core:registro")}?next={reverse("core:carrito")}'
        self.assertRedirects(respuesta, destino, fetch_redirect_response=False)
        self.assertEqual(self.client.session.get("carrito"), {"1": 1})
        self.assertNotIn("ultimo_pedido", self.client.session)

    def test_vista_rapida_anonima_ofrece_formulario(self):
        respuesta = self.client.get(reverse("core:catalogo"))
        self.assertContains(respuesta, 'class="quick-view__form" data-ajax-cart')
        self.assertNotContains(respuesta, "purchase-lock")

    def test_carrito_invitado_solicita_acceso_solo_al_continuar(self):
        guardar_sesion_cliente(self.client, carrito={"1": 2})
        respuesta = self.client.get(reverse("core:carrito"))
        self.assertContains(respuesta, "Continuar con el pedido")
        self.assertNotContains(respuesta, "Cuenta requerida")
        respuesta = self.client.post(reverse("core:confirmar_pedido"), follow=True)
        self.assertContains(respuesta, "Inicia sesión o crea una cuenta para continuar")
        self.assertContains(respuesta, "Tu selección sigue aquí")
        self.assertEqual(self.client.session.get("carrito"), {"1": 2})

    def test_invitado_conserva_limites_y_validacion_de_cantidad(self):
        for cantidad in (0, -1, "texto", 9999):
            with self.subTest(cantidad=cantidad):
                respuesta = self.client.post(reverse("core:agregar_al_carrito", args=[1]), {"cantidad": cantidad}, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
                self.assertEqual(respuesta.status_code, 400)
                self.assertFalse(respuesta.json()["ok"])
                self.assertEqual(self.client.session.get("carrito", {}), {})

    def test_invitado_puede_actualizar_y_eliminar(self):
        self.client.post(reverse("core:agregar_al_carrito", args=[1]), {"cantidad": 1})
        self.client.post(reverse("core:actualizar_carrito", args=[1]), {"cantidad": 2})
        self.assertEqual(self.client.session.get("carrito"), {"1": 2})
        self.client.post(reverse("core:eliminar_del_carrito", args=[1]))
        self.assertEqual(self.client.session.get("carrito"), {})

    def test_carrito_se_conserva_al_crear_cuenta_y_al_volver_a_ingresar(self):
        caches["cuentas"].clear()
        self.client.post(reverse("core:agregar_al_carrito", args=[1]), {"cantidad": 2})
        datos = {"accion": "crear", "nombre": "Cliente Prueba", "correo": "invitado@example.cl", "contrasena": "Sonido2026", "confirmar_contrasena": "Sonido2026", "acepta_terminos": "on", "next": reverse("core:carrito")}
        respuesta = self.client.post(reverse("core:registro"), datos)
        self.assertRedirects(respuesta, reverse("core:carrito"), fetch_redirect_response=False)
        self.assertEqual(self.client.session.get("carrito"), {"1": 2})
        self.client.post(reverse("core:cerrar_sesion"))
        self.assertEqual(self.client.session.get("carrito"), {"1": 2})
        respuesta = self.client.post(reverse("core:registro"), {"accion": "ingresar", "correo": datos["correo"], "contrasena": datos["contrasena"], "next": datos["next"]})
        self.assertRedirects(respuesta, reverse("core:carrito"), fetch_redirect_response=False)
        self.assertEqual(self.client.session.get("carrito"), {"1": 2})
        respuesta = self.client.post(reverse("core:confirmar_pedido"))
        self.assertRedirects(respuesta, reverse("core:pedido_confirmado"), fetch_redirect_response=False)
        self.assertEqual(self.client.session["ultimo_pedido"]["cantidad"], 2)
        self.assertEqual(self.client.session.get("carrito"), {})

    def test_ubicacion_distingue_sector_propuesto_de_local_confirmado(self):
        respuesta = self.client.get(reverse("core:nosotros"))
        self.assertContains(respuesta, 'id="ubicacion"')
        self.assertContains(respuesta, "Ubicación proyectada")
        self.assertContains(respuesta, "Local y fecha de apertura por confirmar")
        self.assertContains(respuesta, "Metro Manquehue")
        self.assertContains(respuesta, 'class="store-location__map"')
        self.assertContains(respuesta, 'https://www.google.com/maps/embed?pb=')
        self.assertContains(respuesta, 'loading="lazy"')
        self.assertNotContains(respuesta, 'id="sector-grid"')
