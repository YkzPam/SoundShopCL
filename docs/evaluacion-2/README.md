# Evaluación 2 — Base de datos y Django Admin de SoundShop CL

## 1. Alcance de la entrega

La segunda evaluación continúa el mismo caso de tienda musical de E1. Su desarrollo se concentra en SQLite, diez modelos propios, diez migraciones de `core`, diagrama de base de datos, Django Admin y datos ficticios. Las cuatro cargas de Faker y la explicación del código forman parte de la demostración presencial.

La rama `evaluacion1` conserva la Evaluación 1 en el commit `381abd52a831058e2032d6c5d5eaefcf32cd8499`. La segunda entrega se publica en `evaluacion-2`, sin modificar `evaluacion1`. El diseño de la tienda se conserva y sus consultas pasan a utilizar SQLite. No se desarrollan pagos, una API, un administrador propio ni cuentas permanentes de clientes.

## 2. Configuración y reproducción en otro computador

Los pasos de instalación, migración, catálogo y creación del administrador se encuentran en el [README principal](../../README.md). La configuración utiliza `django.db.backends.sqlite3` y, por defecto, el archivo `db.sqlite3` en la carpeta de `manage.py`. La aplicación `core` está registrada en `INSTALLED_APPS` y la ruta `/admin/` utiliza el administrador incluido en Django.

La base local no se distribuye en GitHub. Al descargar el proyecto se deben ejecutar `migrate`, `cargar_catalogo` y `createsuperuser`. Este último paso crea un usuario administrativo en la nueva base; no utiliza la cuenta de GitHub ni la cuenta simulada del cliente. La extensión SQLite DB Viewer permite abrir `db.sqlite3` desde VS Code para revisar las tablas y los registros, pero no sustituye al motor SQLite utilizado por Django.

`requirements.txt` fija las mismas cinco versiones del ZIP de referencia del docente: asgiref 3.12.1, Django 6.1.1, Faker 40.40.0, sqlparse 0.6.0 y tzdata 2026.5. La instalación se comprueba con `python -m pip check` y `python -m pip freeze` dentro del entorno virtual. La rúbrica exige la configuración y el funcionamiento del proyecto, no una versión específica; estas versiones se conservan para seguir el entorno de referencia solicitado por el estudiante.

### 2.1. Preparación y comprobación del administrador en otro PC

La descarga debe realizarse desde la rama `evaluacion-2`, no desde `evaluacion1`. En VS Code se abre la carpeta donde está `manage.py`, se crea el entorno `venv` y se instalan las dependencias según el README principal. Con ese entorno preparado, ejecutar en la terminal integrada:

```powershell
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py migrate
.\venv\Scripts\python.exe manage.py cargar_catalogo
.\venv\Scripts\python.exe manage.py createsuperuser
.\venv\Scripts\python.exe manage.py runserver
```

`createsuperuser` solicita nombre de usuario, correo y contraseña. La contraseña no muestra caracteres mientras se escribe. Esta cuenta se guarda en la base seleccionada en ese computador y se crea una sola vez por base; no debe repetirse cada vez que se inicia la tienda. Si ya existe un administrador, puede utilizarse el existente. La cuenta de GitHub y el registro simulado del cliente no reemplazan este acceso.

Abrir <http://127.0.0.1:8000/admin/> con las credenciales recién elegidas y comprobar que aparecen los diez modelos de la tienda. Antes de la evaluación, practicar el CRUD con un producto nuevo siguiendo el apartado 6 y una carga pequeña de Faker siguiendo el apartado 7. Las cuatro cargas deben demostrarse con el docente. El código descargado es compartido, pero las bases, los registros y las cuentas de cada computador son independientes.

Si las cargas se realizan en otro archivo SQLite mediante `SOUNDSHOP_DB`, ese archivo tampoco comparte el administrador de `db.sqlite3`. Para consultarlo en Django Admin debe crearse una cuenta en la base de cargas e iniciarse un servidor que utilice esa misma variable. No se debe publicar la contraseña ni copiar la base privada al repositorio para evitar este paso.

## 3. Modelos y relaciones de la tienda

| N.º | Modelo | Tabla propia | Función |
| --- | --- | --- | --- |
| 1 | Categoria | core_categoria | Clasifica los equipos musicales. |
| 2 | Marca | core_marca | Identifica la marca del equipo. |
| 3 | Proveedor | core_proveedor | Almacena los datos de los proveedores. |
| 4 | Sucursal | core_sucursal | Identifica el punto de venta. |
| 5 | Cliente | core_cliente | Conserva nombre y datos de contacto comerciales. |
| 6 | Producto | core_producto | Almacena código, descripción, precio, stock e imagen. |
| 7 | Boleta | core_boleta | Identifica una venta registrada en Admin. |
| 8 | DetalleBoleta | core_detalleboleta | Relaciona boleta y producto con cantidad y precio histórico. |
| 9 | CompraProveedor | core_compraproveedor | Identifica una compra al proveedor. |
| 10 | DetalleCompra | core_detallecompra | Relaciona compra y producto con cantidad y costo histórico. |

Los nombres y códigos utilizan campos de texto; los precios utilizan `DecimalField(max_digits=10, decimal_places=2)`; el stock y las cantidades utilizan enteros positivos; las fechas utilizan `DateField`; el estado activo utiliza `BooleanField`. Django incorpora la clave primaria `id` a cada modelo. El código de producto y el correo del cliente son únicos. La imagen conserva una ruta relativa a `static/`; no se agrega una gestión de archivos subidos.

Un producto pertenece a una categoría, una marca y un proveedor mediante `ForeignKey`. Cada boleta pertenece a un cliente y una sucursal. Cada compra pertenece a un proveedor y una sucursal. Las relaciones de muchos productos con muchas boletas y compras utilizan las tablas de detalle mediante `ManyToManyField(..., through=...)`; no se crean tablas intermedias adicionales.

`PROTECT` evita borrar registros que todavía están referenciados. `CASCADE` elimina los detalles cuando se elimina su documento principal. Cada detalle conserva el precio o costo de ese momento, sin depender de futuros cambios en el precio de catálogo. Su propiedad `subtotal` multiplica cantidad por precio; no es una columna adicional. El stock no se descuenta automáticamente y las boletas no se generan desde el carrito.

## 4. Diagrama de base de datos

El esquema representa las diez tablas propias, atributos, tipos, claves primarias, campos únicos y claves foráneas. Las líneas muestran las relaciones uno a muchos; las tablas de detalle representan las relaciones muchos a muchos. No se agregan párrafos ni títulos externos dentro del diagrama.

- [Imagen PNG para adjuntar en la plataforma](diagrama-base-datos.png).
- [SVG para ampliar sin perder nitidez](diagrama-base-datos.svg).
- [Archivo editable de Excalidraw](diagrama-base-datos.excalidraw).
- [Descripción del esquema utilizada para comprobar correspondencia](esquema.json).

Para abrir el editable, ingresar a <https://excalidraw.com/> y utilizar **Abrir**. Las tablas internas de Django, como `auth_user`, `django_session` y `django_migrations`, existen en la base, pero no se cuentan entre las diez tablas propias.

## 5. Historial de migraciones

| Archivo | Cambio de estructura |
| --- | --- |
| 0001_categorias_y_marcas | Crea categorías y marcas. |
| 0002_proveedores | Crea proveedores. |
| 0003_sucursales | Crea sucursales. |
| 0004_clientes | Crea clientes. |
| 0005_productos | Crea productos y sus relaciones; inicialmente utiliza precio entero. |
| 0006_boletas | Crea boletas, relacionadas con cliente y sucursal. |
| 0007_detalle_boletas | Crea el detalle y la relación muchos a muchos de boleta y producto. |
| 0008_compras_proveedores | Crea las compras, relacionadas con proveedor y sucursal. |
| 0009_detalle_compras | Crea el detalle y la relación muchos a muchos de compra y producto. |
| 0010_producto_activo_precios_decimal | Añade producto activo y cambia los tres campos de precio a DecimalField. |

Las migraciones fueron generadas por Django a medida que se incorporaron o modificaron los modelos. No son diez archivos vacíos. `makemigrations` registra el cambio en archivos Python; `migrate` aplica esos archivos a SQLite. La décima migración conserva un cambio real posterior al modelo inicial y permite explicar cómo se modifica una estructura existente.

```powershell
.\venv\Scripts\python.exe manage.py showmigrations core
.\venv\Scripts\python.exe manage.py makemigrations core --check --dry-run
```

En el historial, `[X]` identifica una migración aplicada. La comprobación sin escritura debe indicar que no existen cambios pendientes. Para realizar una modificación futura se cambia el modelo, se genera otra migración y se aplica; no se borran ni se reescriben las migraciones que ya fueron utilizadas.

## 6. Administración y demostración del CRUD

`core/admin.py` registra los diez modelos mediante `@admin.register`. `list_display` determina las columnas; `search_fields` define la búsqueda; `list_filter` agrega filtros; `ordering` ordena; `list_per_page` limita los registros por página; `fieldsets` agrupa los campos de producto. La cabecera y los títulos identifican SoundShop CL. Son opciones del administrador nativo, no páginas CRUD propias.

Los detalles pueden completarse en el formulario de la boleta o compra mediante `TabularInline`. El cliente de la boleta y las relaciones de los detalles utilizan los selectores normales de Django Admin, sin autocompletado. Los apartados independientes de detalles, la búsqueda del listado y los filtros se conservan. `readonly_fields` muestra el identificador del producto y el subtotal sin permitir su edición. En un detalle nuevo, el subtotal queda vacío hasta guardar el registro, para evitar calcularlo antes de ingresar cantidad y precio.

Para la demostración presencial se ingresa a `/admin/` con la cuenta creada mediante `createsuperuser`. En **Productos**, se crea un registro nuevo con código no utilizado, nombre, descripción, precio mayor que cero, stock y las tres relaciones existentes. Se guarda y se consulta desde el listado y desde SQLite. Se busca por código, se aplica un filtro, se modifica el nombre o precio y se comprueba el valor guardado al abrir nuevamente el registro.

La eliminación debe demostrarse con ese producto nuevo, sin asociarlo a una boleta ni compra. Si se intenta eliminar un equipo utilizado en un detalle, `PROTECT` impedirá el borrado: es una regla del modelo, no un fallo del administrador. Las validaciones rechazan códigos repetidos, precios no positivos y cantidades no positivas. Después de guardar un cambio en un producto activo, el catálogo público lo muestra al recargar la página.

El CRUD también puede practicarse en **Clientes**: crear un registro ficticio con nombre, correo y teléfono; buscarlo por correo; modificar sus datos o su estado activo; y eliminarlo si no está asociado a una boleta. Después de guardar, abrir nuevamente el registro permite comprobar que el cambio persiste. Estas operaciones utilizan el mismo Django Admin existente, sin agregar formularios ni vistas propias.

El campo `correo` del cliente utiliza `EmailField(unique=True)`. Un correo sin formato válido o un correo que ya pertenece a otro cliente debe mostrar un error en el formulario de Admin y no crear otro registro. Las pruebas comprueban ambos rechazos y que la cantidad de clientes permanece sin cambios; no se incorporan validadores nuevos al modelo.

Un cliente asociado a una boleta no puede eliminarse porque la relación utiliza `PROTECT`; Admin muestra los registros que impiden el borrado. Eliminar una boleta, en cambio, elimina sus detalles mediante `CASCADE`, pero conserva al cliente y los productos del catálogo. Las pruebas verifican ambas reglas mediante solicitudes a Django Admin y consultas posteriores a la base temporal.

## 7. Catálogo inicial y generación con Faker

`cargar_catalogo` utiliza los diez productos del JSON existente como datos iniciales. Incorpora categorías, marcas, proveedor, sucursal y documentos relacionados, además de tres clientes ficticios con Faker. `get_or_create` busca un registro y lo crea solo si no existe; repetir el comando no sobrescribe los registros que fueron modificados en Admin. Los contactos `example.test` y el sector de la sucursal son datos de prueba, no una tienda física confirmada.

`generar_clientes` recibe la cantidad solicitada. Faker con configuración `es_CL` produce nombres y teléfonos; cada correo ficticio recibe un prefijo de carga y un número para evitar duplicados. El bucle prepara lotes de hasta mil objetos. `bulk_create` guarda cada lote sin mantener un millón de objetos en memoria. `transaction.atomic` revierte la carga completa si ocurre un error durante la inserción.

El intervalo permitido va de 1 a 1.000.000 de clientes por ejecución. Las pruebas de límites comprueban que cero, un número negativo y 1.000.001 provocan `CommandError` sin insertar registros. El último caso se rechaza antes de generar datos; no realiza una carga superior al millón ni sustituye las cuatro cargas solicitadas para la defensa.

El comando consulta la cantidad antes y después, cuenta los registros del prefijo y recupera el primero y el último. Solo informa **VERIFICADO** cuando la diferencia y el número almacenado coinciden con lo solicitado. La carga es acumulativa: agregar mil clientes no reemplaza los registros que ya existían. Los clientes ficticios no se convierten en usuarios de acceso a Django.

La primera línea también identifica el archivo SQLite seleccionado mediante `connection.settings_dict["NAME"]`. `Base: default` es el nombre de la conexión, no la ruta del archivo. El dato `archivo SQLite` permite comprobar si la carga se dirige a `db.sqlite3` o a la base separada seleccionada con `SOUNDSHOP_DB`. La prueba de Faker verifica que esa ruta aparece en la salida y que los registros se almacenan.

Para separar las cargas grandes de la tienda, ejecutar en la misma terminal de VS Code:

```powershell
New-Item -ItemType Directory -Path work -Force | Out-Null
$env:SOUNDSHOP_DB = "work/demostracion.sqlite3"
.\venv\Scripts\python.exe manage.py migrate
.\venv\Scripts\python.exe manage.py generar_clientes --cantidad 100
.\venv\Scripts\python.exe manage.py generar_clientes --cantidad 1000
.\venv\Scripts\python.exe manage.py generar_clientes --cantidad 100000
.\venv\Scripts\python.exe manage.py generar_clientes --cantidad 1000000
.\venv\Scripts\python.exe manage.py shell -c "from core.models import Cliente; print(Cliente.objects.count())"
Remove-Item Env:SOUNDSHOP_DB
```

La variable `SOUNDSHOP_DB` selecciona otro archivo SQLite durante esa terminal. Al retirarla, los comandos vuelven a utilizar `db.sqlite3`. No se borra ninguna de las dos bases. Para ver el archivo de demostración en Django Admin, se mantiene la variable, se crea un administrador en esa base y se inicia el servidor desde la misma terminal.

## 8. Pruebas y comprobaciones

La ejecución local del 13 de octubre de 2026 terminó con 43 pruebas aprobadas. `manage.py check` y `pip check` no informaron errores; `makemigrations core --check --dry-run` no detectó cambios pendientes. Las pruebas utilizan una base temporal y no modifican los registros de la tienda.

Las comprobaciones cubren la conexión SQLite, los diez modelos y migraciones, la correspondencia del esquema, el registro y acceso a Django Admin, el CRUD de productos y clientes, las validaciones, las relaciones `PROTECT` y `CASCADE`, la carga del catálogo y una carga pequeña de Faker. También verifican las páginas de la tienda y el formato de precios. El administrador de tests existe únicamente en la base temporal y no sirve para ingresar a la base de demostración.

Las bases locales revisadas presentaron integridad `ok` y ninguna referencia rota. Una base separada conserva los cuatro lotes de clientes ficticios:

| Carga | Registros acumulados |
| --- | ---: |
| 100 | 100 |
| 1.000 | 1.100 |
| 100.000 | 101.100 |
| 1.000.000 | 1.101.100 |

Las bases SQLite y la carpeta `work/` no se publican en GitHub. Cada descarga requiere aplicar las migraciones, cargar los datos y crear su administrador. Las comprobaciones locales no sustituyen las cuatro cargas con el docente ni la defensa presencial.
