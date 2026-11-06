# Evaluación 3 — Gestión y consultas de la tienda

SoundShop CL conserva el caso Tienda y SQLite como base de datos de la etapa anterior. La interfaz de gestión utiliza formularios HTML y vistas de función, siguiendo el estilo del ejercicio entregado por el docente. La guía de E3 se aplica al panel propio, la autenticación nativa y los reportes ORM. La lista de Tienda contiene veinte preguntas; se implementan las veinte confirmadas para este proyecto.

## 1. Gestión de información y acceso

El panel de `/gestion/` permite mantener productos, categorías, clientes, ventas y detalles. El grupo Administrador tiene el control completo. El grupo Operador consulta el catálogo y los reportes, y crea o edita clientes, ventas y detalles; no cambia el catálogo, elimina registros ni gestiona cuentas. Se utiliza el modelo `User` de Django, con contraseñas verificadas mediante `authenticate`, sesiones iniciadas con `login` y cierre mediante `logout`. Un cliente comercial es un registro del modelo `Cliente`, distinto de una cuenta de acceso.

Los grupos nativos de Django se preparan con `python manage.py configurar_grupos`. El decorador reutilizable `grupos_permitidos`, definido en `core/decorators.py`, comprueba el perfil antes de ejecutar cada vista. Se utiliza junto a `login_required`: una visita anónima se redirige al inicio de sesión y una cuenta sin autorización recibe HTTP 403. El bloqueo se aplica también al escribir directamente una URL o enviar una petición POST; ocultar un botón no reemplaza esta comprobación.

Cada formulario envía una petición POST con CSRF. La vista lee los campos, aplica `full_clean()` al modelo y guarda mediante el ORM cuando los datos son válidos. Los errores vuelven al formulario. Los borrados requieren confirmación con POST y respetan las relaciones protegidas. El Administrador puede desactivar o eliminar otras cuentas de acceso; no puede desactivar ni eliminar su propia cuenta durante la gestión. Borrar una cuenta no elimina los registros comerciales de clientes, productos o ventas.

La primera cuenta se prepara con `createsuperuser`, pero la gestión se realiza en las páginas propias del proyecto. La ruta `/admin/` no está habilitada y `django.contrib.admin` no está instalado en esta rama, de acuerdo con la indicación del PDF de E3 de utilizar un administrador propio. El registro de los modelos en Django Admin corresponde a la etapa E2 conservada en su rama. Las actividades de aplicación adjuntas se incorporan a E3 en lo relativo al CRUD, las peticiones POST, CSRF, los grupos, el decorador propio y el control de acceso.

## 2. Correspondencia de las veinte consultas ORM

Los números siguientes corresponden al selector de **Reportes**. Los precios se presentan con separadores de miles; los filtros numéricos se ingresan sin ese separador. Una venta equivale a una boleta, independientemente de cuántos productos contenga.

| N.º | Consulta | Filtro o cálculo |
| --- | --- | --- |
| 1 | Productos disponibles | Producto activo con stock mayor que cero. |
| 2 | Productos de una categoría | Selección de categoría y filtro por su clave. |
| 3 | Productos en un rango de precios | Precio mínimo y máximo incluidos. |
| 4 | Diez productos más caros | Precio descendente, limitado a diez. |
| 5 | Cantidad de clientes registrados | Conteo de clientes activos e inactivos. |
| 6 | Compras de un cliente | Ventas del cliente seleccionado, fecha y total histórico. |
| 7 | Productos adquiridos en una venta | Cliente y venta; se valida que la venta le pertenezca. |
| 8 | Cantidad de ventas de un período | Fecha inicial y final incluidas; cuenta boletas. |
| 9 | Productos con menos de cinco unidades | Stock menor que cinco, incluyendo cero. |
| 10 | Total vendido en un día | Suma de cantidad por precio histórico de los detalles. |
| 11 | Cinco productos más vendidos | Suma de unidades vendidas por producto. |
| 12 | Cinco clientes con más compras | Cantidad de boletas de cada cliente. |
| 13 | Monto comprado por cada cliente | Suma histórica; clientes sin compras aparecen con cero. |
| 14 | Productos nunca vendidos | Productos sin detalles de venta asociados. |
| 15 | Promedio gastado por venta | Promedio de los totales calculados por boleta. |
| 16 | Categoría con mayor monto vendido | Ingresos históricos de sus productos. |
| 17 | Unidades por producto durante el último mes | Mes calendario anterior completo; la pantalla muestra sus fechas. |
| 18 | Cliente que más gastó durante el año | Año seleccionado; suma histórica por cliente. |
| 19 | Montos vendidos por mes del año | Año seleccionado; agrupación por mes con ventas. |
| 20 | Diez productos que generan mayores ingresos | Suma histórica por producto, orden descendente. |

Los reportes se implementan en `core/reportes.py`. La interpretación de «último mes» es el mes calendario anterior completo; no se mezcla con el mes en curso. Los reportes de ingresos utilizan `DetalleBoleta.precio_unitario`, no el precio actual de `Producto`. Los listados y sus filtros están protegidos por sesión.

## 3. Recorrido de demostración

La demostración comienza con la base `db.sqlite3` preparada mediante las migraciones y una cuenta creada. Una visita anónima a `/gestion/` conduce al inicio de sesión. Después de ingresar, se crea un producto, se consulta, se modifica y se elimina un registro sin referencias. El mismo recorrido está disponible para categorías y clientes; una venta permite mantener su encabezado y sus detalles.

Desde Usuarios se puede crear una cuenta, editar sus datos, desactivarla o eliminarla con confirmación. Desde Reportes se seleccionan las preguntas y los filtros que correspondan. Al cerrar sesión, volver a una URL administrativa exige ingresar otra vez. Para explicar el código conviene ubicar `settings.py`, `models.py`, `urls.py`, `views.py`, `reportes.py` y las plantillas utilizadas en el recorrido.
