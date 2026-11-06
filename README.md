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

`configurar_grupos` crea los dos grupos y asigna Administrador a los superusuarios activos. Las cuentas activas sin grupo reciben Operador. El comando puede ejecutarse nuevamente en una base ya preparada y conserva las contraseñas. La primera cuenta creada con `createsuperuser` puede acceder al panel para preparar el proyecto.

Desde Usuarios, el Administrador puede editar, desactivar o eliminar otras cuentas. Desactivar conserva la cuenta sin permitir su acceso; eliminar la borra después de confirmar mediante POST. El usuario no puede desactivar ni eliminar su propia cuenta durante la gestión. Los clientes y las ventas son registros comerciales independientes y se conservan al borrar una cuenta de acceso.

## 3. Continuidad del modelo de la tienda

Las ventas se almacenan en los modelos existentes `Boleta` y `DetalleBoleta`: corresponden a `Venta` y `DetalleVenta` del caso de la guía. No se crean otras tablas para duplicar esa información. El detalle relaciona cada producto con su venta y conserva la cantidad y el precio unitario histórico. El total se calcula con esos valores, por lo que cambiar el precio del catálogo no modifica ventas anteriores.

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

Las páginas administrativas y las operaciones están protegidas con `login_required` y el decorador propio `grupos_permitidos`. Una cuenta autenticada sin perfil autorizado recibe una respuesta HTTP 403, igual que un Operador que intenta acceder a una acción reservada. La comprobación se ejecuta en las vistas para peticiones GET y POST; también se adapta la interfaz al perfil. Cerrar sesión invalida el acceso y los formularios utilizan protección CSRF. El formulario de usuarios no permite otorgar privilegios administrativos a una cuenta nueva.

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
