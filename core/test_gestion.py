"""Pruebas del indicador 2: entradas, validación y salidas administrativas."""
from django.conf import settings
from django.test import SimpleTestCase, Client
from django.urls import reverse

from .forms import FichaGestionForm
from .catalogo import obtener_producto


class GestionFichaTests(SimpleTestCase):
    datos = {'nombre': 'Pulse X ANC', 'marca': 'SoundLab', 'categoria': 'audifonos',
        'descripcion': 'Audífonos para escuchar música y trabajar en estudio.',
        'precio': '89990', 'stock': '8', 'estado': 'activo'}

    def test_validacion_calcula_resultado_sin_modificar_catalogo(self):
        ruta = settings.BASE_DIR / 'core/data/catalogo.json'
        original = ruta.read_bytes()
        producto_original = obtener_producto(1)
        respuesta = self.client.post(reverse('core:gestion_producto', args=[1]), self.datos | {'precio': '100000', 'stock': '3'})
        resultado = respuesta.context['resultado_gestion']
        self.assertEqual(resultado['valor_existencias'], 300000)
        self.assertEqual(resultado['disponibilidad'], 'Disponible')
        self.assertContains(respuesta, '$300.000')
        self.assertEqual(obtener_producto(1), producto_original)
        self.assertEqual(ruta.read_bytes(), original)
        self.assertNotIn('carrito', self.client.session)

    def test_limites_y_tipos_invalidos_generan_errores_del_servidor(self):
        for campo, valores in {'precio': ['0', '-1', '2000001', '1.5', 'texto'],
            'stock': ['-1', '10000', '1.5', 'texto'], 'categoria': ['inventada'],
            'estado': ['publicar'], 'nombre': [' ', 'ab', 'x'*101], 'marca': ['x'],
            'descripcion': ['corta', 'a                    b']}.items():
            for valor in valores:
                with self.subTest(campo=campo, valor=valor):
                    formulario = FichaGestionForm(self.datos | {campo: valor})
                    self.assertFalse(formulario.is_valid())
                    self.assertIn(campo, formulario.errors)

    def test_estado_agotado_e_inactivo_y_valores_limite(self):
        for stock, estado, esperado in [('0', 'activo', 'Agotado'), ('9999', 'inactivo', 'Inactivo')]:
            respuesta = self.client.post(reverse('core:gestion_productos'), self.datos | {'precio': '2000000', 'stock': stock, 'estado': estado})
            self.assertEqual(respuesta.context['resultado_gestion']['disponibilidad'], esperado)
        self.assertTrue(FichaGestionForm(self.datos | {'precio': '1', 'stock': '0'}).is_valid())

    def test_error_conserva_entrada_y_no_produce_resultado(self):
        respuesta = self.client.post(reverse('core:gestion_productos'), self.datos | {'precio': '-5', 'nombre': 'Nombre corregible'})
        self.assertIsNone(respuesta.context['resultado_gestion'])
        self.assertContains(respuesta, 'Nombre corregible')
        self.assertContains(respuesta, 'role="alert"')
        self.assertContains(respuesta, 'id_precio_errors')

    def test_carga_restablece_y_controla_identificador_inexistente(self):
        respuesta = self.client.get(reverse('core:gestion_producto', args=[7]))
        self.assertEqual(respuesta.context['formulario_gestion'].initial['nombre'], obtener_producto(7).nombre)
        self.assertIsNone(respuesta.context['resultado_gestion'])
        self.assertRedirects(self.client.get(reverse('core:gestion_producto', args=[999])), reverse('core:gestion_productos'))

    def test_csrf_metodos_y_escape_de_salida(self):
        cliente = Client(enforce_csrf_checks=True)
        url = reverse('core:gestion_productos')
        self.assertEqual(cliente.post(url, self.datos).status_code, 403)
        self.assertEqual(self.client.put(url).status_code, 405)
        respuesta = self.client.post(url, self.datos | {'nombre': '<script>alert(1)</script>'})
        self.assertNotContains(respuesta, '<script>alert(1)</script>')
        self.assertContains(respuesta, '&lt;script&gt;alert(1)&lt;/script&gt;')
