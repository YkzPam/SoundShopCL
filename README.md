# SoundShop CL — Tienda musical

La Evaluación 3 continúa la misma tienda de E2. Conserva el catálogo, las imágenes, los estilos, los diez modelos, el historial de migraciones y SQLite como base de datos. Esta etapa agrega un panel propio con autenticación de Django, gestión de productos, categorías, clientes, ventas y usuarios, y veinte consultas ORM del caso Tienda. Los formularios están escritos en HTML y se procesan en las vistas con `request.POST`, sin `forms.py` ni Django Admin.

## 1. Preparación del entorno

Abrir en Visual Studio Code la carpeta que contiene `manage.py`. Se requiere Python; SQLite está incluido en Python y guarda la información en el archivo `db.sqlite3`, junto a `manage.py`. Ese archivo se crea al ejecutar las migraciones. La descarga del proyecto no incluye el entorno virtual, una base con datos locales ni contraseñas.

La carga inicial utiliza datos de muestra definidos directamente, sin bibliotecas para generar personas ficticias. El resumen y los reportes calculan sus cifras desde los registros de SQLite; las ventas de demostración son datos locales y no forman parte de la descarga del repositorio.

En la terminal integrada seleccionar **Command Prompt / Símbolo del sistema (CMD)**. Los siguientes comandos corresponden a CMD; se ejecutan uno por uno:

```bat
python -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
```

## 2. Preparación y ejecución de la tienda

En la misma terminal, con `venv` activo, ejecutar:

```bat
python manage.py migrate
python manage.py cargar_catalogo
python manage.py createsuperuser
python manage.py configurar_grupos
python manage.py runserver
```

`migrate` crea o actualiza la base SQLite aplicando el historial existente. No se vuelve a ejecutar `startproject` ni `startapp` al descargar un proyecto ya creado. `cargar_catalogo` incorpora los equipos y los registros ficticios relacionados sin sobrescribir los que ya fueron editados. Cada computador conserva sus datos en su propio archivo `db.sqlite3`.

`createsuperuser` crea la primera cuenta de administración. Se eligen el nombre, correo y contraseña; la contraseña no aparece mientras se escribe. Esta cuenta ingresa al panel propio de E3. No se publica una contraseña administrativa predeterminada ni se habilita la ruta de Django Admin.

- Tienda: <http://127.0.0.1:8000/>.
- Panel propio: <http://127.0.0.1:8000/gestion/>.
- Inicio de sesión: <http://127.0.0.1:8000/login/>.

El grupo **Administrador** tiene acceso completo a productos, categorías, clientes, ventas, detalles y cuentas de usuario. El grupo **Operador** puede consultar el catálogo, categorías, clientes, ventas y reportes; también puede crear y editar clientes, ventas y sus detalles. Los cambios del catálogo, las eliminaciones y la gestión de usuarios quedan reservados al Administrador. Las cuentas nuevas creadas desde el panel reciben el grupo Operador. Las contraseñas se guardan con el sistema de Django, nunca como texto legible.

`configurar_grupos` crea los dos grupos y asigna sus permisos nativos de Django: consultar, crear, modificar y eliminar. Administrador recibe esos permisos para las cinco entidades principales de Tienda y las cuentas de usuario. Operador recibe consulta para las cinco entidades y creación y modificación para clientes, ventas y detalles. Los permisos de la aplicación se identifican con `core`, por ejemplo, `core.add_producto`; los de cuentas utilizan `auth`, por ejemplo, `auth.change_user`.

El comando asigna Administrador a los superusuarios activos y Operador a las cuentas activas sin grupo. Puede ejecutarse nuevamente en una base ya preparada y conserva las contraseñas. Al actualizar una copia existente se ejecuta `python manage.py configurar_grupos` para preparar los permisos. La primera cuenta creada con `createsuperuser` puede acceder al panel para preparar el proyecto.

Desde Usuarios, el Administrador puede editar, desactivar o eliminar otras cuentas. Desactivar conserva la cuenta sin permitir su acceso; eliminar la borra después de confirmar mediante POST. El usuario no puede desactivar ni eliminar su propia cuenta durante la gestión. Los clientes y las ventas son registros comerciales independientes y se conservan al borrar una cuenta de acceso.

## 3. Continuidad del modelo de la tienda

Las ventas se almacenan en los modelos existentes `Boleta` y `DetalleBoleta`: corresponden a `Venta` y `DetalleVenta` del caso de la guía. El modelo de E3 incorpora RUT de cliente, fecha y hora de venta, estado, subtotal y total. Las longitudes y los importes de las entidades principales siguen el esquema de Tienda. `Producto.codigo` utiliza la columna `sku` y `Cliente.correo` la columna `email`; se conservan los nombres Python de E2 mediante `db_column`.

Cada detalle guarda `subtotal = cantidad × precio_unitario`. Al guardar o eliminar un detalle se actualiza y guarda el total de la venta. El precio unitario histórico se conserva, por lo que cambiar el precio del catálogo no modifica ventas anteriores. Los estados Registrada, Pendiente y Finalizada permiten describir la venta; no ejecutan cobros ni cambian sus importes.

Las migraciones `0011` y `0012` completan los campos y trasladan los registros anteriores. Las ventas de E2 conservan su día y reciben las 00:00 como hora local; sus subtotales y totales se calculan a partir de los detalles existentes. El RUT es opcional y único cuando se informa; los clientes anteriores permanecen sin RUT hasta que se complete desde el panel.

El [diagrama de E3](docs/evaluacion-3/diagrama-base-datos.png) representa las diez tablas conservadas y sus campos actuales. También está disponible en [SVG](docs/evaluacion-3/diagrama-base-datos.svg) y como [editable de Excalidraw](docs/evaluacion-3/diagrama-base-datos.excalidraw). Los diagramas de `docs/evaluacion-2/` documentan la etapa anterior.

Los otros modelos heredados —marcas, proveedores, sucursales y compras a proveedores— se conservan como parte del proyecto anterior. El CRUD de E3 se concentra en las entidades del caso Tienda. Un producto, categoría o cliente utilizado en otros registros tiene protección de borrado; al eliminar una venta se eliminan sus detalles y se mantienen los productos y el cliente.

El carrito público conserva el recorrido anterior: su confirmación vacía la selección y no realiza cobros ni crea ventas. Las ventas persistentes de esta etapa se registran en el panel. No se agregan pagos reales, API ni JWT.

## 4. Reportes comerciales y archivos de esta etapa

Los veinte reportes se abren desde **Reportes** dentro del panel y exigen iniciar sesión. Utilizan consultas ORM de Django con filtros, ordenamientos, conteos, sumas, promedios y agrupaciones. La [guía de consultas de E3](docs/evaluacion-3/README.md) identifica cada reporte y sus filtros.

El resumen del panel presenta gráficos de ingresos mensuales y de los cinco productos más vendidos del año seleccionado, junto con indicadores, accesos rápidos y un aviso de stock bajo. Los gráficos utilizan HTML y CSS, sin agregar librerías, y consultan los mismos registros de la tienda. Sus cifras se actualizan al volver a abrir el resumen después de modificar una venta o un producto; los meses sin ventas aparecen con cero.

Las pantallas del CRUD comparten animaciones breves en formularios, listados, indicadores, avisos y gráficos, junto con respuestas visuales de botones y campos. Se realizan con CSS y se desactivan cuando el sistema tiene activada la preferencia de reducir movimiento.

Los listados muestran el número de registros y distinguen entre una lista vacía y una búsqueda sin resultados. Productos permite combinar nombre, categoría, estado y existencias; el stock bajo comprende de una a cuatro unidades y los agotados tienen cero. Los filtros se pueden limpiar y se conservan al cambiar de página o categoría. Los formularios señalan los errores junto a cada campo, y la confirmación de eliminación muestra el registro y las consecuencias antes de enviar el POST.

El catálogo administrativo incluye accesos por categoría musical, botones de acción con iconos y avisos para productos sin foto, con stock bajo, agotados o desactivados. El formulario de producto está organizado por secciones y cuenta con una vista previa de fotografía, nombre, marca, categoría, código, precio y estado. La vista previa utiliza JavaScript del proyecto y solo refleja los campos que se están editando; los cambios se guardan al enviar el formulario.

```text
soundshop/settings.py            Conexión a SQLite y autenticación
soundshop/urls.py                Rutas del proyecto sin Django Admin
core/models.py                  Modelo de datos conservado de E2
core/migrations/                Historial conservado de E2
core/views.py                   Login, logout y CRUD con request.POST
core/decorators.py              Autorización reutilizable por grupos
core/context_processors.py      Perfil y acciones disponibles en la interfaz
core/reportes.py                Las veinte consultas ORM de Tienda
core/urls.py                    Rutas propias de la tienda y el panel
core/templates/core/e3/          Formularios y páginas del panel
static/css/gestion.css          Diseño propio del panel
core/tests.py                   Pruebas funcionales de E3
.vscode/tasks.json              Ejecución de tareas desde VS Code
```

Las páginas administrativas y las operaciones están protegidas con `login_required`, el decorador propio `grupos_permitidos` y los permisos nativos de Django. Los listados y borrados utilizan `permission_required`; los formularios comprueban `has_perm` para distinguir entre crear y modificar. Una cuenta autenticada sin perfil o sin el permiso requerido recibe HTTP 403. Las plantillas consultan `perms` para mostrar las acciones autorizadas, y la vista vuelve a comprobarlas para peticiones GET y POST. Cerrar sesión invalida el acceso y los formularios utilizan protección CSRF. El formulario de usuarios no permite otorgar privilegios administrativos a una cuenta nueva.

## 5. Comprobación y conservación de las entregas

Para revisar la configuración, comprobar que no faltan migraciones y ejecutar las pruebas en una base temporal de SQLite:

```bat
python manage.py check
python manage.py showmigrations core
python manage.py makemigrations core --check --dry-run
python manage.py test core
```

Las pruebas utilizan una base temporal de SQLite y no modifican los registros de `db.sqlite3`. Verifican sesiones, rutas protegidas, CRUD, validaciones, persistencia y resultados conocidos de los veinte reportes. No reemplazan la demostración presencial ni la explicación del código.

La rama `evaluacion-3` continúa el trabajo de `evaluacion-2`. La primera entrega se conserva en `evaluacion1` y la segunda en `evaluacion-2`; sus archivos e historiales no se sustituyen. Los materiales de `docs/evaluacion-2/`, los diagramas de flujo y los mockups anteriores permanecen como antecedentes de esas etapas. E2 y E3 utilizan SQLite; las instrucciones de Django Admin corresponden a E2 y la instalación vigente de esta rama es la descrita aquí.

La entrega de E3 se debe identificar con la rama y el hash del commit que efectivamente esté publicado en GitHub. Descargar o ejecutar el proyecto local no equivale a publicarlo ni a enviarlo a la plataforma.
