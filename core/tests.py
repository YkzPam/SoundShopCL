"""Pruebas funcionales de E3 sobre la base MySQL de pruebas de Django."""
from datetime import date, timedelta
from decimal import Decimal
from django.contrib.auth.models import User
from django.db import connection
from django.test import Client, TestCase
from django.urls import reverse
from .models import Categoria, Marca, Proveedor, Sucursal, Cliente, Producto, Boleta, DetalleBoleta


class Evaluacion3Tests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_superuser('administracion', 'admin@example.test', 'Madera!Sonido9f2026')
        cls.operador = User.objects.create_user('operador', password='Madera!Sonido9f2026')
        cls.categoria = Categoria.objects.create(nombre='Instrumentos', slug='instrumentos')
        cls.otra_categoria = Categoria.objects.create(nombre='Audio', slug='audio')
        cls.marca = Marca.objects.create(nombre='Marca musical')
        cls.proveedor = Proveedor.objects.create(nombre='Distribuidor', correo='proveedor@example.test')
        cls.sucursal = Sucursal.objects.create(nombre='Centro', direccion='Calle 10', comuna='Santiago')
        cls.ana = Cliente.objects.create(nombre='Ana', correo='ana@example.test')
        cls.beto = Cliente.objects.create(nombre='Beto', correo='beto@example.test')
        cls.sin_compras = Cliente.objects.create(nombre='Sin compras', correo='sin@example.test', activo=False)
        cls.guitarra = Producto.objects.create(codigo='P1', nombre='Guitarra', descripcion='Guitarra musical', precio=100, stock=10, categoria=cls.categoria, marca=cls.marca, proveedor=cls.proveedor)
        cls.audifonos = Producto.objects.create(codigo='P2', nombre='Audífonos', descripcion='Audio musical', precio=50, stock=3, categoria=cls.otra_categoria, marca=cls.marca, proveedor=cls.proveedor)
        cls.inactivo = Producto.objects.create(codigo='P3', nombre='Piano', descripcion='Piano musical', precio=300, stock=0, activo=False, categoria=cls.categoria, marca=cls.marca, proveedor=cls.proveedor)
        cls.sin_venta = Producto.objects.create(codigo='P4', nombre='Cable', descripcion='Cable musical', precio=25, stock=4, categoria=cls.otra_categoria, marca=cls.marca, proveedor=cls.proveedor)
        cls.hoy = date.today()
        cls.mes_anterior = cls.hoy.replace(day=1) - timedelta(days=1)
        cls.anio_anterior = date(cls.hoy.year - 1, 1, 1)
        cls.venta = Boleta.objects.create(numero=1, fecha=cls.hoy, cliente=cls.ana, sucursal=cls.sucursal)
        cls.detalle = DetalleBoleta.objects.create(boleta=cls.venta, producto=cls.guitarra, cantidad=2, precio_unitario=80)
        DetalleBoleta.objects.create(boleta=cls.venta, producto=cls.audifonos, cantidad=1, precio_unitario=50)
        cls.segunda = Boleta.objects.create(numero=2, fecha=cls.hoy, cliente=cls.ana, sucursal=cls.sucursal)
        DetalleBoleta.objects.create(boleta=cls.segunda, producto=cls.guitarra, cantidad=1, precio_unitario=90)
        tercera = Boleta.objects.create(numero=3, fecha=cls.mes_anterior, cliente=cls.beto, sucursal=cls.sucursal)
        DetalleBoleta.objects.create(boleta=tercera, producto=cls.audifonos, cantidad=4, precio_unitario=40)
        cuarta = Boleta.objects.create(numero=4, fecha=cls.anio_anterior, cliente=cls.beto, sucursal=cls.sucursal)
        DetalleBoleta.objects.create(boleta=cuarta, producto=cls.guitarra, cantidad=3, precio_unitario=70)

    def setUp(self):
        self.client.force_login(self.admin)

    def datos_producto(self):
        return {'codigo': 'NUEVO', 'nombre': 'Bajo nuevo', 'descripcion': 'Bajo para la tienda', 'precio': '20990.00', 'stock': '5', 'categoria': self.categoria.pk, 'marca': self.marca.pk, 'proveedor': self.proveedor.pk, 'activo': 'on', 'imagen': ''}

    def test_mysql_y_tablas_heredadas(self):
        self.assertEqual(connection.vendor, 'mysql')
        tablas = connection.introspection.table_names()
        self.assertEqual(len([t for t in tablas if t.startswith('core_')]), 10)
        self.assertIn('auth_user', tablas)

    def test_todas_las_rutas_de_gestion_exigen_sesion(self):
        self.client.logout()
        rutas = [('gestion', []), ('gestion_productos', []), ('producto_nuevo', []), ('producto_editar', [self.guitarra.pk]), ('producto_eliminar', [self.guitarra.pk]), ('gestion_categorias', []), ('categoria_nueva', []), ('categoria_editar', [self.categoria.pk]), ('categoria_eliminar', [self.categoria.pk]), ('gestion_clientes', []), ('cliente_nuevo', []), ('cliente_editar', [self.ana.pk]), ('cliente_eliminar', [self.ana.pk]), ('gestion_ventas', []), ('venta_nueva', []), ('venta_editar', [self.venta.pk]), ('venta_detalle', [self.venta.pk]), ('venta_eliminar', [self.venta.pk]), ('detalle_nuevo', [self.venta.pk]), ('detalle_editar', [self.venta.pk, self.detalle.pk]), ('detalle_eliminar', [self.venta.pk, self.detalle.pk]), ('gestion_usuarios', []), ('usuario_nuevo', []), ('usuario_editar', [self.operador.pk]), ('usuario_desactivar', [self.operador.pk]), ('reportes', [])]
        for nombre, args in rutas:
            for metodo in ('get', 'post'):
                with self.subTest(ruta=nombre, metodo=metodo):
                    respuesta = getattr(self.client, metodo)(reverse('core:' + nombre, args=args))
                    self.assertEqual(respuesta.status_code, 302)
                    self.assertTrue(respuesta.url.startswith(reverse('core:login') + '?next='))
        self.assertEqual(Producto.objects.count(), 4)

    def test_login_y_logout_reales(self):
        self.client.logout()
        url = reverse('core:login')
        self.assertContains(self.client.post(url, {'username': 'operador', 'password': 'incorrecta'}), 'no son correctos')
        respuesta = self.client.post(url, {'username': 'operador', 'password': 'Madera!Sonido9f2026'})
        self.assertRedirects(respuesta, reverse('core:gestion'))
        self.assertEqual(self.client.get(reverse('core:salir')).status_code, 405)
        self.client.post(reverse('core:salir'))
        self.assertEqual(self.client.get(reverse('core:gestion')).status_code, 302)
        self.operador.is_active = False
        self.operador.save()
        self.client.post(url, {'username': 'operador', 'password': 'Madera!Sonido9f2026'})
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_login_no_redirige_a_otro_sitio(self):
        self.client.logout()
        respuesta = self.client.post(reverse('core:login'), {'username': 'operador', 'password': 'Madera!Sonido9f2026', 'next': 'https://example.org/externo'})
        self.assertEqual(respuesta.url, reverse('core:gestion'))

    def test_csrf_exigido_para_modificar(self):
        navegador = Client(enforce_csrf_checks=True)
        navegador.force_login(self.admin)
        respuesta = navegador.post(reverse('core:producto_nuevo'), self.datos_producto())
        self.assertEqual(respuesta.status_code, 403)
        self.assertFalse(Producto.objects.filter(codigo='NUEVO').exists())

    def test_pantallas_de_gestion_renderizan(self):
        rutas = [('gestion', []), ('gestion_productos', []), ('producto_nuevo', []), ('producto_editar', [self.guitarra.pk]), ('producto_eliminar', [self.guitarra.pk]), ('gestion_categorias', []), ('categoria_nueva', []), ('categoria_editar', [self.categoria.pk]), ('gestion_clientes', []), ('cliente_nuevo', []), ('cliente_editar', [self.ana.pk]), ('gestion_ventas', []), ('venta_nueva', []), ('venta_editar', [self.venta.pk]), ('venta_detalle', [self.venta.pk]), ('venta_eliminar', [self.venta.pk]), ('detalle_nuevo', [self.venta.pk]), ('detalle_editar', [self.venta.pk, self.detalle.pk]), ('detalle_eliminar', [self.venta.pk, self.detalle.pk]), ('gestion_usuarios', []), ('usuario_nuevo', []), ('usuario_editar', [self.operador.pk]), ('usuario_desactivar', [self.operador.pk])]
        for nombre, args in rutas:
            with self.subTest(ruta=nombre):
                self.assertEqual(self.client.get(reverse('core:' + nombre, args=args)).status_code, 200)

    def test_tienda_conservada_y_admin_django_no_publicado(self):
        self.client.logout()
        for nombre in ('inicio', 'catalogo', 'categorias', 'nosotros', 'carrito', 'login'):
            self.assertEqual(self.client.get(reverse('core:' + nombre)).status_code, 200)
        self.assertEqual(self.client.get(reverse('core:detalle_producto', args=[self.guitarra.pk])).status_code, 200)
        self.assertEqual(self.client.get('/admin/').status_code, 404)

    def test_producto_crud_y_catalogo(self):
        datos = self.datos_producto()
        self.assertEqual(self.client.post(reverse('core:producto_nuevo'), datos).status_code, 302)
        producto = Producto.objects.get(codigo='NUEVO')
        self.assertEqual(producto.precio, Decimal('20990'))
        datos['nombre'] = 'Bajo editado'
        datos['precio'] = '22990'
        self.client.post(reverse('core:producto_editar', args=[producto.pk]), datos)
        producto.refresh_from_db()
        self.assertEqual(producto.nombre, 'Bajo editado')
        self.assertContains(self.client.get(reverse('core:catalogo')), 'Bajo editado')
        self.assertContains(self.client.get(reverse('core:gestion_productos'), {'q': 'Bajo editado'}), '22.990')
        self.client.get(reverse('core:producto_eliminar', args=[producto.pk]))
        self.assertTrue(Producto.objects.filter(pk=producto.pk).exists())
        self.client.post(reverse('core:producto_eliminar', args=[producto.pk]))
        self.assertFalse(Producto.objects.filter(pk=producto.pk).exists())

    def test_producto_rechaza_valores_invalidos(self):
        for cambio in ({'precio': '-1'}, {'stock': '-1'}, {'codigo': 'P1'}, {'categoria': '999999'}, {'categoria': 'texto'}, {'precio': 'NaN'}, {'nombre': ''}):
            datos = self.datos_producto()
            datos.update(cambio)
            with self.subTest(cambio=cambio):
                respuesta = self.client.post(reverse('core:producto_nuevo'), datos)
                self.assertEqual(respuesta.status_code, 200)
                self.assertTrue(respuesta.context['errores'])
        self.assertEqual(Producto.objects.count(), 4)

    def test_producto_vendido_protegido_y_desactivable(self):
        self.client.post(reverse('core:producto_eliminar', args=[self.guitarra.pk]))
        self.assertTrue(Producto.objects.filter(pk=self.guitarra.pk).exists())
        datos = self.datos_producto()
        datos.update(codigo='P1', nombre='Guitarra', activo='')
        self.client.post(reverse('core:producto_editar', args=[self.guitarra.pk]), datos)
        self.guitarra.refresh_from_db()
        self.assertFalse(self.guitarra.activo)
        self.assertEqual(self.client.get(reverse('core:detalle_producto', args=[self.guitarra.pk])).status_code, 404)

    def test_categoria_crud_y_proteccion(self):
        self.client.post(reverse('core:categoria_nueva'), {'nombre': 'Micrófonos', 'descripcion': 'Voces'})
        categoria = Categoria.objects.get(slug='microfonos')
        self.client.post(reverse('core:categoria_editar', args=[categoria.pk]), {'nombre': 'Estudio', 'slug': 'estudio', 'descripcion': 'Grabación'})
        categoria.refresh_from_db()
        self.assertEqual(categoria.nombre, 'Estudio')
        self.client.post(reverse('core:categoria_eliminar', args=[categoria.pk]))
        self.assertFalse(Categoria.objects.filter(pk=categoria.pk).exists())
        self.client.post(reverse('core:categoria_eliminar', args=[self.categoria.pk]))
        self.assertTrue(Categoria.objects.filter(pk=self.categoria.pk).exists())

    def test_cliente_crud_validacion_y_proteccion(self):
        datos = {'nombre': 'Carla', 'correo': 'carla@example.test', 'telefono': '123', 'activo': 'on'}
        self.client.post(reverse('core:cliente_nuevo'), datos)
        persona = Cliente.objects.get(correo='carla@example.test')
        datos['nombre'] = 'Carla editada'
        self.client.post(reverse('core:cliente_editar', args=[persona.pk]), datos)
        persona.refresh_from_db()
        self.assertEqual(persona.nombre, 'Carla editada')
        self.assertTrue(self.client.post(reverse('core:cliente_nuevo'), datos).context['errores'])
        datos['correo'] = 'no-es-correo'
        self.assertTrue(self.client.post(reverse('core:cliente_nuevo'), datos).context['errores'])
        self.client.post(reverse('core:cliente_eliminar', args=[persona.pk]))
        self.assertFalse(Cliente.objects.filter(pk=persona.pk).exists())
        self.client.post(reverse('core:cliente_eliminar', args=[self.ana.pk]))
        self.assertTrue(Cliente.objects.filter(pk=self.ana.pk).exists())

    def test_venta_y_detalles_crud(self):
        datos = {'numero': '99', 'fecha': self.hoy.isoformat(), 'cliente': self.ana.pk, 'sucursal': self.sucursal.pk}
        self.client.post(reverse('core:venta_nueva'), datos)
        venta = Boleta.objects.get(numero=99)
        datos['numero'] = '100'
        self.client.post(reverse('core:venta_editar', args=[venta.pk]), datos)
        venta.refresh_from_db()
        self.assertEqual(venta.numero, 100)
        linea = {'producto': self.guitarra.pk, 'cantidad': '2', 'precio_unitario': '20990'}
        self.client.post(reverse('core:detalle_nuevo', args=[venta.pk]), linea)
        detalle = DetalleBoleta.objects.get(boleta=venta)
        self.assertEqual(detalle.subtotal, Decimal('41980'))
        self.assertContains(self.client.get(reverse('core:venta_detalle', args=[venta.pk])), '41.980')
        linea['cantidad'] = '3'
        self.client.post(reverse('core:detalle_editar', args=[venta.pk, detalle.pk]), linea)
        detalle.refresh_from_db()
        self.assertEqual(detalle.cantidad, 3)
        self.client.post(reverse('core:detalle_eliminar', args=[venta.pk, detalle.pk]))
        self.assertFalse(DetalleBoleta.objects.filter(pk=detalle.pk).exists())
        self.client.post(reverse('core:detalle_nuevo', args=[venta.pk]), linea)
        self.client.post(reverse('core:venta_eliminar', args=[venta.pk]))
        self.assertFalse(Boleta.objects.filter(pk=venta.pk).exists())
        self.assertFalse(DetalleBoleta.objects.filter(boleta_id=venta.pk).exists())
        self.assertTrue(Producto.objects.filter(pk=self.guitarra.pk).exists())

    def test_venta_y_detalle_invalidos_no_se_guardan(self):
        respuesta = self.client.post(reverse('core:venta_nueva'), {'numero': '1', 'fecha': 'incorrecta', 'cliente': '999999', 'sucursal': ''})
        self.assertTrue(respuesta.context['errores'])
        for cambio in ({'cantidad': '0'}, {'precio_unitario': '-1'}, {'producto': '999999'}, {'producto': self.guitarra.pk}):
            datos = {'producto': self.sin_venta.pk, 'cantidad': '2', 'precio_unitario': '10'}
            datos.update(cambio)
            respuesta = self.client.post(reverse('core:detalle_nuevo', args=[self.venta.pk]), datos)
            self.assertTrue(respuesta.context['errores'])
        self.assertEqual(Boleta.objects.count(), 4)
        self.assertEqual(DetalleBoleta.objects.count(), 5)
        self.assertEqual(self.client.get(reverse('core:detalle_editar', args=[self.segunda.pk, self.detalle.pk])).status_code, 404)

    def test_precios_historicos_no_cambian_con_catalogo(self):
        self.guitarra.precio = 99999
        self.guitarra.save()
        self.detalle.refresh_from_db()
        self.assertEqual(self.detalle.precio_unitario, Decimal('80'))
        respuesta = self.client.get(reverse('core:reportes'), {'reporte': 10, 'fecha': self.hoy.isoformat()})
        self.assertEqual(list(respuesta.context['filas'])[0][1], Decimal('300'))

    def test_operador_no_administra_usuarios(self):
        self.client.force_login(self.operador)
        for nombre, args in [('gestion_usuarios', []), ('usuario_nuevo', []), ('usuario_editar', [self.admin.pk]), ('usuario_desactivar', [self.admin.pk])]:
            for metodo in ('get', 'post'):
                self.assertEqual(getattr(self.client, metodo)(reverse('core:' + nombre, args=args)).status_code, 403)

    def test_usuario_creacion_edicion_desactivacion(self):
        datos = {'username': 'nuevo_usuario', 'email': 'nuevo@example.test', 'first_name': 'Camila', 'last_name': 'Lagos', 'password': 'Cedro!Musica7z2026', 'confirmar': 'Cedro!Musica7z2026', 'is_active': 'on', 'is_staff': 'on', 'is_superuser': 'on'}
        respuesta = self.client.post(reverse('core:usuario_nuevo'), datos)
        self.assertEqual(respuesta.status_code, 302)
        cuenta = User.objects.get(username='nuevo_usuario')
        self.assertTrue(cuenta.check_password(datos['password']))
        self.assertNotEqual(cuenta.password, datos['password'])
        self.assertFalse(cuenta.is_staff)
        self.assertFalse(cuenta.is_superuser)
        datos.update(first_name='Camila editada', password='', confirmar='')
        self.client.post(reverse('core:usuario_editar', args=[cuenta.pk]), datos)
        cuenta.refresh_from_db()
        self.assertEqual(cuenta.first_name, 'Camila editada')
        self.assertTrue(cuenta.check_password('Cedro!Musica7z2026'))
        self.client.post(reverse('core:usuario_desactivar', args=[cuenta.pk]))
        cuenta.refresh_from_db()
        self.assertFalse(cuenta.is_active)

    def test_usuario_contrasena_invalida_y_autodesactivacion(self):
        datos = {'username': 'otra_cuenta', 'password': '123', 'confirmar': 'diferente', 'is_active': 'on'}
        respuesta = self.client.post(reverse('core:usuario_nuevo'), datos)
        self.assertTrue(respuesta.context['errores'])
        self.assertFalse(User.objects.filter(username='otra_cuenta').exists())
        self.client.post(reverse('core:usuario_desactivar', args=[self.admin.pk]))
        self.admin.refresh_from_db()
        self.assertTrue(self.admin.is_active)

    def test_cambio_de_contrasena_propia_conserva_sesion(self):
        datos = {'username': self.admin.username, 'email': self.admin.email, 'password': 'Pino!Frecuencia7z2026', 'confirmar': 'Pino!Frecuencia7z2026', 'is_active': 'on'}
        self.client.post(reverse('core:usuario_editar', args=[self.admin.pk]), datos)
        self.admin.refresh_from_db()
        self.assertTrue(self.admin.check_password(datos['password']))
        self.assertEqual(self.client.get(reverse('core:gestion')).status_code, 200)

    def test_veinte_reportes_con_resultados_conocidos(self):
        filtros = {2: {'categoria': self.categoria.pk}, 3: {'minimo': 50, 'maximo': 100}, 6: {'cliente': self.ana.pk}, 7: {'cliente': self.ana.pk, 'venta': self.venta.pk}, 8: {'desde': self.hoy.isoformat(), 'hasta': self.hoy.isoformat()}, 10: {'fecha': self.hoy.isoformat()}, 18: {'anio': self.hoy.year}, 19: {'anio': self.hoy.year}}
        por_mes = {self.hoy.month: Decimal('300')}
        if self.mes_anterior.year == self.hoy.year:
            por_mes[self.mes_anterior.month] = Decimal('160')
        esperados = {
            1: [('P1', 'Guitarra', Decimal('100'), 10), ('P2', 'Audífonos', Decimal('50'), 3), ('P4', 'Cable', Decimal('25'), 4)],
            2: [('P1', 'Guitarra', 'Instrumentos', 10), ('P3', 'Piano', 'Instrumentos', 0)],
            3: [('P2', 'Audífonos', Decimal('50')), ('P1', 'Guitarra', Decimal('100'))],
            4: [('P3', 'Piano', Decimal('300')), ('P1', 'Guitarra', Decimal('100')), ('P2', 'Audífonos', Decimal('50')), ('P4', 'Cable', Decimal('25'))],
            5: [(3,)], 6: [(2, self.hoy, 'Ana', Decimal('90')), (1, self.hoy, 'Ana', Decimal('210'))],
            7: [('Guitarra', 2, Decimal('80'), Decimal('160')), ('Audífonos', 1, Decimal('50'), Decimal('50'))],
            8: [(self.hoy, self.hoy, 2)], 9: [('P3', 'Piano', 0), ('P2', 'Audífonos', 3), ('P4', 'Cable', 4)],
            10: [(self.hoy, Decimal('300'))], 11: [('P1', 'Guitarra', 6), ('P2', 'Audífonos', 5)],
            12: [('Ana', 'ana@example.test', 2), ('Beto', 'beto@example.test', 2)],
            13: [('Beto', 'beto@example.test', Decimal('370')), ('Ana', 'ana@example.test', Decimal('300')), ('Sin compras', 'sin@example.test', Decimal('0'))],
            14: [('P3', 'Piano', 0), ('P4', 'Cable', 4)], 15: [(Decimal('167.5'),)], 16: [('Instrumentos', Decimal('460'))],
            17: [('P1', 'Guitarra', 0), ('P2', 'Audífonos', 4), ('P3', 'Piano', 0), ('P4', 'Cable', 0)],
            18: [('Ana', 'ana@example.test', Decimal('300'))], 19: sorted(por_mes.items()),
            20: [('P1', 'Guitarra', Decimal('460')), ('P2', 'Audífonos', Decimal('210'))],
        }
        for numero in range(1, 21):
            with self.subTest(reporte=numero):
                parametros = {'reporte': numero}
                parametros.update(filtros.get(numero, {}))
                respuesta = self.client.get(reverse('core:reportes'), parametros)
                self.assertEqual(respuesta.status_code, 200)
                self.assertFalse(respuesta.context['error'])
                self.assertEqual(list(respuesta.context['filas']), esperados[numero])

    def test_reportes_rechazan_filtros_invalidos(self):
        for parametros in ({'reporte': 2, 'categoria': '999999'}, {'reporte': 3, 'minimo': 'NaN', 'maximo': '100'}, {'reporte': 3, 'minimo': '200', 'maximo': '100'}, {'reporte': 7, 'cliente': self.beto.pk, 'venta': self.venta.pk}, {'reporte': 8, 'desde': '2026-02-10', 'hasta': '2026-01-01'}, {'reporte': 10, 'fecha': 'sin-fecha'}, {'reporte': 18, 'anio': '10000'}):
            with self.subTest(parametros=parametros):
                respuesta = self.client.get(reverse('core:reportes'), parametros)
                self.assertEqual(respuesta.status_code, 200)
                self.assertTrue(respuesta.context['error'])
        self.assertEqual(self.client.get(reverse('core:reportes'), {'reporte': 21}).status_code, 400)

    def test_reportes_sin_ventas(self):
        Boleta.objects.all().delete()
        for numero in (6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20):
            with self.subTest(reporte=numero):
                respuesta = self.client.get(reverse('core:reportes'), {'reporte': numero, 'cliente': self.ana.pk})
                self.assertEqual(respuesta.status_code, 200)
        respuesta = self.client.get(reverse('core:reportes'), {'reporte': 15})
        self.assertEqual(list(respuesta.context['filas']), [(Decimal('0'),)])

    def test_paginacion_conserva_filtros(self):
        for numero in range(30):
            Cliente.objects.create(nombre='Cliente paginado', correo=f'paginado{numero}@example.test')
        respuesta = self.client.get(reverse('core:gestion_clientes'), {'q': 'paginado'})
        self.assertEqual(len(respuesta.context['pagina']), 25)
        self.assertContains(respuesta, 'q=paginado&amp;page=2')
        respuesta = self.client.get(reverse('core:gestion_clientes'), {'q': 'paginado', 'page': 2})
        self.assertEqual(len(respuesta.context['pagina']), 5)
        respuesta = self.client.get(reverse('core:reportes'), {'reporte': 13, 'page': 2})
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'reporte=13&amp;page=1')

    def test_fecha_valida_se_conserva_si_otro_campo_falla(self):
        datos = {'numero': 1, 'fecha': '2026-09-15', 'cliente': self.ana.pk, 'sucursal': self.sucursal.pk}
        respuesta = self.client.post(reverse('core:venta_nueva'), datos)
        self.assertTrue(respuesta.context['errores'])
        self.assertContains(respuesta, 'value="2026-09-15"')

    def test_resumen_anual_graficos_e_indicadores(self):
        respuesta = self.client.get(reverse('core:gestion'), {'anio': self.hoy.year})
        datos = respuesta.context
        total_esperado = Decimal('300')
        ventas_esperadas = 2
        if self.mes_anterior.year == self.hoy.year:
            total_esperado += Decimal('160')
            ventas_esperadas += 1
        self.assertEqual(datos['ingresos'], total_esperado)
        self.assertEqual(datos['total_ventas'], ventas_esperadas)
        self.assertEqual(len(datos['meses']), 12)
        self.assertEqual(datos['meses'][self.hoy.month - 1]['monto'], Decimal('300'))
        self.assertTrue(all(0 <= m['altura'] <= 100 for m in datos['meses']))
        self.assertEqual(sum(m['monto'] for m in datos['meses']), total_esperado)
        self.assertEqual(datos['cantidad_stock_bajo'], 2)
        unidades = {p.codigo: p.unidades for p in datos['productos_vendidos']}
        self.assertEqual(unidades['P1'], 3)
        self.assertEqual(unidades['P2'], 5 if self.mes_anterior.year == self.hoy.year else 1)
        anterior = self.client.get(reverse('core:gestion'), {'anio': self.anio_anterior.year})
        monto_anterior = Decimal('210') + (Decimal('160') if self.mes_anterior.year == self.anio_anterior.year else 0)
        self.assertEqual(anterior.context['ingresos'], monto_anterior)

    def test_resumen_sin_ventas_muestra_ceros(self):
        Boleta.objects.all().delete()
        respuesta = self.client.get(reverse('core:gestion'))
        self.assertEqual(respuesta.context['ingresos'], 0)
        self.assertEqual(respuesta.context['total_ventas'], 0)
        self.assertEqual(respuesta.context['productos_vendidos'], [])
        self.assertTrue(all(m['altura'] == 0 and m['monto'] == 0 for m in respuesta.context['meses']))
        self.assertContains(respuesta, 'Todavía no hay ingresos')

    def test_resumen_rechaza_anios_invalidos(self):
        for valor in ('texto', '0', '10000'):
            with self.subTest(anio=valor):
                respuesta = self.client.get(reverse('core:gestion'), {'anio': valor})
                self.assertRedirects(respuesta, reverse('core:gestion'))

    def test_resumen_actualiza_ingresos_al_editar_una_venta(self):
        antes = self.client.get(reverse('core:gestion')).context['ingresos']
        respuesta = self.client.post(reverse('core:detalle_editar', args=[self.venta.pk, self.detalle.pk]), {'producto': self.guitarra.pk, 'cantidad': '3', 'precio_unitario': '80'})
        self.assertEqual(respuesta.status_code, 302)
        despues = self.client.get(reverse('core:gestion')).context['ingresos']
        self.assertEqual(despues, antes + Decimal('80'))
