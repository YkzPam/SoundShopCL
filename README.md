# SoundShop CL — Tienda musical

La Evaluación 3 continúa la misma tienda de E2. Conserva el catálogo, las imágenes, los estilos, los diez modelos y el historial de migraciones. Esta etapa utiliza MySQL local y agrega un panel propio con autenticación de Django, gestión de productos, categorías, clientes, ventas y usuarios, y veinte consultas ORM del caso Tienda. Los formularios están escritos en HTML y se procesan en las vistas con `request.POST`, sin `forms.py` ni Django Admin.

## 1. Preparación del entorno y de MySQL

Abrir en Visual Studio Code la carpeta que contiene `manage.py`. Se requiere Python y un servidor MySQL local activo. La conexión se verificó con MySQL Community Server 8.4 y `mysqlclient` 2.2.8. La descarga del proyecto no incluye el servidor de base de datos, el entorno virtual ni contraseñas.

En la terminal integrada seleccionar **Command Prompt / Símbolo del sistema (CMD)**. Los siguientes comandos corresponden a CMD; se ejecutan uno por uno:

```bat
python -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
```

En MySQL Workbench, o en la consola de MySQL, crear la base antes de aplicar las migraciones:

```sql
CREATE DATABASE soundshop_e3 CHARACTER SET utf8mb4;
```

En la misma terminal CMD donde está activo `venv`, indicar los datos de la conexión local. Sustituir `USUARIO_MYSQL` y `CLAVE_MYSQL` por los datos elegidos al configurar MySQL. El usuario de la base y el usuario que inicia sesión en la tienda son cuentas diferentes.

```bat
set MYSQL_DATABASE=soundshop_e3
set MYSQL_HOST=127.0.0.1
set MYSQL_PORT=3306
set MYSQL_USER=USUARIO_MYSQL
set MYSQL_PASSWORD=CLAVE_MYSQL
```

Si el usuario local de MySQL no tiene contraseña, usar `set MYSQL_PASSWORD=`. Si MySQL escucha en otro puerto, cambiar `MYSQL_PORT`. Estos valores duran mientras permanezca abierta esa terminal; no se deben guardar contraseñas en archivos publicados.

## 2. Preparación y ejecución de la tienda

Con MySQL activo y las variables anteriores configuradas, ejecutar:

```bat
python manage.py migrate
python manage.py cargar_catalogo
python manage.py createsuperuser
python manage.py runserver
```

`migrate` aplica el historial existente sobre la base MySQL nueva. No se vuelve a ejecutar `startproject` ni `startapp` al descargar un proyecto ya creado. `cargar_catalogo` incorpora los equipos y los registros ficticios relacionados sin sobrescribir los que ya fueron editados. La base SQLite usada en E2 se conserva fuera de esta entrega y no se transforma automáticamente en MySQL.

`createsuperuser` crea la primera cuenta de administración. Se eligen el nombre, correo y contraseña; la contraseña no aparece mientras se escribe. Esta cuenta ingresa al panel propio de E3. No se publica una contraseña administrativa predeterminada ni se habilita la ruta de Django Admin.

- Tienda: <http://127.0.0.1:8000/>.
- Panel propio: <http://127.0.0.1:8000/gestion/>.
- Inicio de sesión: <http://127.0.0.1:8000/login/>.

El panel permite crear, listar, editar y eliminar productos, categorías, clientes, ventas y sus detalles. Las cuentas de acceso se crean, consultan, editan y desactivan desde **Usuarios**, disponible para la cuenta administradora. Las nuevas cuentas pueden operar la tienda, pero no administrar usuarios. Las contraseñas se guardan con el sistema de Django, nunca como texto legible.

## 3. Continuidad del modelo de la tienda

Las ventas se almacenan en los modelos existentes `Boleta` y `DetalleBoleta`: corresponden a `Venta` y `DetalleVenta` del caso de la guía. No se crean otras tablas para duplicar esa información. El detalle relaciona cada producto con su venta y conserva la cantidad y el precio unitario histórico. El total se calcula con esos valores, por lo que cambiar el precio del catálogo no modifica ventas anteriores.

Los otros modelos heredados —marcas, proveedores, sucursales y compras a proveedores— se conservan como parte del proyecto anterior. El CRUD de E3 se concentra en las entidades del caso Tienda. Un producto, categoría o cliente utilizado en otros registros tiene protección de borrado; al eliminar una venta se eliminan sus detalles y se mantienen los productos y el cliente.

El carrito público conserva el recorrido anterior: su confirmación vacía la selección y no realiza cobros ni crea ventas. Las ventas persistentes de esta etapa se registran en el panel. No se agregan pagos reales, API ni JWT.

## 4. Reportes comerciales y archivos de esta etapa

Los veinte reportes se abren desde **Reportes** dentro del panel y exigen iniciar sesión. Utilizan consultas ORM de Django con filtros, ordenamientos, conteos, sumas, promedios y agrupaciones. La [guía de consultas de E3](docs/evaluacion-3/README.md) identifica cada reporte y sus filtros.

El resumen del panel presenta gráficos de ingresos mensuales y de los cinco productos más vendidos del año seleccionado, junto con indicadores, accesos rápidos y un aviso de stock bajo. Los gráficos utilizan HTML y CSS, sin agregar librerías, y consultan los mismos registros de la tienda. Sus cifras se actualizan al volver a abrir el resumen después de modificar una venta o un producto; los meses sin ventas aparecen con cero.

Las pantallas del CRUD comparten animaciones breves en formularios, listados, indicadores, avisos y gráficos, junto con respuestas visuales de botones y campos. Se realizan con CSS y se desactivan cuando el sistema tiene activada la preferencia de reducir movimiento.

```text
soundshop/settings.py            Conexión a MySQL y autenticación
soundshop/urls.py                Rutas del proyecto sin Django Admin
core/models.py                  Modelo de datos conservado de E2
core/migrations/                Historial conservado de E2
core/views.py                   Login, logout y CRUD con request.POST
core/reportes.py                Las veinte consultas ORM de Tienda
core/urls.py                    Rutas propias de la tienda y el panel
core/templates/core/e3/          Formularios y páginas del panel
static/css/gestion.css          Diseño propio del panel
core/tests.py                   Pruebas funcionales de E3
.vscode/tasks.json              Ejecución de tareas desde VS Code
```

Las páginas administrativas y las operaciones están protegidas con `login_required`. Cerrar sesión invalida el acceso y los formularios utilizan protección CSRF. La gestión de cuentas requiere también `is_staff`; el formulario no permite otorgar privilegios administrativos a una cuenta nueva.

## 5. Comprobación y conservación de las entregas

Para revisar la configuración, comprobar que no faltan migraciones y ejecutar las pruebas en otra base temporal de MySQL:

```bat
python manage.py check
python manage.py showmigrations core
python manage.py makemigrations core --check --dry-run
python manage.py test core
```

El usuario MySQL utilizado para las pruebas debe poder crear y eliminar la base `test_soundshop_e3`. Las pruebas verifican sesiones, rutas protegidas, CRUD, validaciones, persistencia y resultados conocidos de los veinte reportes. No reemplazan la demostración presencial ni la explicación del código.

La rama `evaluacion-3` continúa el trabajo de `evaluacion-2`. La primera entrega se conserva en `evaluacion1` y la segunda en `evaluacion-2`; sus archivos e historiales no se sustituyen. Los materiales de `docs/evaluacion-2/`, los diagramas de flujo y los mockups anteriores permanecen como antecedentes de esas etapas. Sus instrucciones sobre SQLite y Django Admin corresponden a E2; la instalación vigente de esta rama es la descrita aquí.

La entrega de E3 se debe identificar con la rama y el hash del commit que efectivamente esté publicado en GitHub. Descargar o ejecutar el proyecto local no equivale a publicarlo ni a enviarlo a la plataforma.
