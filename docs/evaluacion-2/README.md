# Evaluación 2 — Base de datos y Django Admin de SoundShop CL

## 1. Alcance de la entrega

La segunda evaluación continúa el mismo caso de tienda musical de E1. Su desarrollo se concentra en SQLite, modelos relacionados, migraciones, diagrama, Django Admin y datos ficticios. El correo del docente exige demostrar las cuatro cargas de Faker y explicar el código presencialmente. Las diez tablas propias y las diez migraciones de `core` corresponden a la exigencia de clase confirmada por el estudiante; no se atribuye esa cantidad al texto de la rúbrica.

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

Los archivos conservan la cabecera de Django 5.2.17, la versión que los generó originalmente. La actualización del entorno a Django 6.1.1 no reescribe ese historial: las diez migraciones existentes se aplicaron correctamente con la nueva versión y `makemigrations --check --dry-run` no detectó cambios pendientes. Cambiar solamente esa cabecera daría una referencia falsa de cómo se generaron.

```powershell
.\venv\Scripts\python.exe manage.py showmigrations core
.\venv\Scripts\python.exe manage.py makemigrations core --check --dry-run
```

En el historial, `[X]` identifica una migración aplicada. La comprobación sin escritura debe indicar que no existen cambios pendientes. Para realizar una modificación futura se cambia el modelo, se genera otra migración y se aplica; no se borran ni se reescriben las migraciones que ya fueron utilizadas.

## 6. Administración y demostración del CRUD

`core/admin.py` registra los diez modelos mediante `@admin.register`. `list_display` determina las columnas; `search_fields` define la búsqueda; `list_filter` agrega filtros; `ordering` ordena; `list_per_page` limita los registros por página; `fieldsets` agrupa los campos de producto. La cabecera y los títulos identifican SoundShop CL. Son opciones del administrador nativo, no páginas CRUD propias.

Los detalles pueden completarse en el formulario de la boleta o compra mediante `TabularInline`. El cliente de la boleta y las relaciones de los detalles utilizan `autocomplete_fields` para buscar registros. Los apartados independientes de detalles, la búsqueda del listado y los filtros se conservan. `readonly_fields` muestra el identificador del producto y el subtotal sin permitir su edición. En un detalle nuevo, el subtotal queda vacío hasta guardar el registro, para evitar calcularlo antes de ingresar cantidad y precio.

Para la demostración presencial se ingresa a `/admin/` con la cuenta creada mediante `createsuperuser`. En **Productos**, se crea un registro nuevo con código no utilizado, nombre, descripción, precio mayor que cero, stock y las tres relaciones existentes. Se guarda y se consulta desde el listado y desde SQLite. Se busca por código, se aplica un filtro, se modifica el nombre o precio y se comprueba el valor guardado al abrir nuevamente el registro.

La eliminación debe demostrarse con ese producto nuevo, sin asociarlo a una boleta ni compra. Si se intenta eliminar un equipo utilizado en un detalle, `PROTECT` impedirá el borrado: es una regla del modelo, no un fallo del administrador. Las validaciones rechazan códigos repetidos, precios no positivos y cantidades no positivas. Después de guardar un cambio en un producto activo, el catálogo público lo muestra al recargar la página.

El CRUD también puede practicarse en **Clientes**: crear un registro ficticio con nombre, correo y teléfono; buscarlo por correo; modificar sus datos o su estado activo; y eliminarlo si no está asociado a una boleta. Después de guardar, abrir nuevamente el registro permite comprobar que el cambio persiste. Estas operaciones utilizan el mismo Django Admin existente, sin agregar formularios ni vistas propias.

El campo `correo` del cliente utiliza `EmailField(unique=True)`. Un correo sin formato válido o un correo que ya pertenece a otro cliente debe mostrar un error en el formulario de Admin y no crear otro registro. Las pruebas comprueban ambos rechazos y que la cantidad de clientes permanece sin cambios; no se incorporan validadores nuevos al modelo.

Un cliente asociado a una boleta no puede eliminarse porque la relación utiliza `PROTECT`; Admin muestra los registros que impiden el borrado. Eliminar una boleta, en cambio, elimina sus detalles mediante `CASCADE`, pero conserva al cliente y los productos del catálogo. Las pruebas adicionales verifican ambas reglas existentes mediante solicitudes a Django Admin y consultas posteriores a la base temporal.

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

## 8. Verificaciones locales del 8 de octubre de 2026

Las cuatro cargas se repitieron después de alinear las dependencias con el ZIP del docente, utilizando Django 6.1.1 y Faker 40.40.0. La nueva base `work/revision-e2-61fc4ac4/cargas.sqlite3` permanece separada del catálogo. El comando verificó las inserciones y una consulta posterior, en otro proceso, confirmó 1.101.100 clientes acumulados. El historial de esa base tiene las diez migraciones aplicadas. SQLite devolvió integridad `ok` y ninguna infracción de claves foráneas tanto en la base de cargas como en la del catálogo.

| Carga solicitada | Registros antes | Registros después | Tiempo local informado |
| --- | ---: | ---: | ---: |
| 100 | 0 | 100 | 0,03 s |
| 1.000 | 100 | 1.100 | 0,16 s |
| 100.000 | 1.100 | 101.100 | 16,42 s |
| 1.000.000 | 101.100 | 1.101.100 | 166,24 s |

Los tiempos corresponden a esas ejecuciones locales; no son valores garantizados en otro computador. Estas cargas no se realizaron con el docente. La base principal conserva diez productos y tres clientes comerciales de prueba. Los archivos SQLite y la carpeta `work/` están excluidos de Git.

El ajuste que identifica el archivo SQLite se comprobó con una carga nueva de 100 clientes en una base separada. La salida mostró la ruta seleccionada y una consulta posterior, desde otro proceso, confirmó los 100 registros, integridad `ok` y ninguna infracción de claves foráneas. Esta comprobación local no utilizó la base del catálogo ni representa una prueba en otro PC.

Las diecisiete pruebas automáticas iniciales pasaron con las cinco dependencias del docente, tanto en el entorno actualizado como en un entorno virtual nuevo. `pip check` no encontró conflictos y `pip freeze` mostró exactamente las cinco versiones de requirements.txt. Esas pruebas comprueban SQLite, tablas y migraciones, registro de modelos, correspondencia del esquema, acceso administrativo, creación, consulta, filtros, modificación y eliminación de productos, validaciones, relaciones, repetición del catálogo, una carga pequeña de Faker y respuesta de las páginas conservadas. En esa verificación inicial el CRUD completo se probó con productos; no se afirma que se haya repetido manualmente con cada uno de los diez modelos.

Los tests crean su administrador únicamente en la base temporal de pruebas. La contraseña de ese usuario no sirve para ingresar a la tienda real y no constituye una credencial administrativa distribuida. `self.client.get` y `self.client.post` simulan solicitudes; las comprobaciones comparan la respuesta y los registros almacenados. No son una grabación de interacción en el navegador.

El 8 de octubre también se creó un administrador activo, con permisos de personal y superusuario, en la base principal `db.sqlite3` del computador original. Su autenticación se comprobó con el cliente de pruebas de Django sobre esa base local: el panel y los listados de los diez modelos respondieron con HTTP 200; una solicitud sin sesión se redirigió al inicio de sesión. Esta comprobación no utilizó el administrador temporal de los tests. La base y las credenciales permanecen excluidas de GitHub; al descargar el proyecto en otro PC, debe prepararse su propia cuenta conforme al apartado 2.1.

### 8.1. Pruebas adicionales de administración

La ampliación mantiene el mismo patrón de `TestCase`, `self.client.get`, `self.client.post` y comprobaciones de registros utilizado en las pruebas existentes. Se incorporaron casos del CRUD, las validaciones de clientes y las relaciones con boletas, sin modificar modelos, migraciones ni opciones de Admin:

| Prueba | Comprobación |
| --- | --- |
| Crear cliente | El formulario guarda nombre, correo, teléfono y estado activo. |
| Consultar cliente | La búsqueda por correo y el filtro de estado muestran el registro correspondiente. |
| Modificar cliente | El nombre, teléfono y estado actualizados persisten al consultar de nuevo. |
| Eliminar cliente | Un cliente nuevo sin boletas se elimina y deja de existir en la base. |
| Correo inválido | Admin muestra el error del campo y no crea el cliente. |
| Correo duplicado | Admin rechaza el correo existente y conserva un único registro con ese correo. |
| Cliente con boleta | Admin impide su eliminación y conserva ambos registros mediante `PROTECT`. |
| Eliminar boleta | Se eliminan la boleta y sus detalles mediante `CASCADE`, sin borrar el cliente ni los productos. |

La primera ampliación de este apartado terminó con 25 pruebas aprobadas y ningún error de configuración. Sus ocho pruebas nuevas se agrupan en CRUD de clientes, validaciones de correo y reglas de eliminación relacionada. Las operaciones se realizan en la base temporal de tests y no eliminan ni modifican registros de la base del catálogo. No constituyen una prueba manual en otro PC ni reemplazan la defensa presencial.

### 8.2. Pruebas de límites, relaciones y carga inicial

Las comprobaciones siguientes refuerzan comportamientos ya implementados, sin agregar campos, tablas, migraciones ni funciones a la tienda. Cada grupo se incorpora después de ejecutar las pruebas y se documenta con el resultado observado. No se utilizan para simular avances anteriores ni una instalación en otro PC.

| Grupo | Comprobación |
| --- | --- |
| Límites de Faker | Cero, cantidades negativas y cantidades superiores al millón se rechazan sin crear clientes. |
| Precio y stock | Admin acepta el precio mínimo actual de 1 y stock cero; rechaza precio cero, stock negativo y stock no numérico sin guardar el producto. |
| Compras a proveedores | Admin protege al proveedor asociado a una compra. Borrar la compra elimina sus detalles, pero conserva al proveedor y los productos. |
| Repetición del catálogo | Repetir la carga mantiene la cantidad de registros de los diez modelos y conserva los datos editados de clientes y el precio, stock y estado de productos. |

La ejecución local final posterior a estos grupos terminó con 36 pruebas aprobadas. Se incorporaron once casos: dos de límites de Faker, cuatro de precio y stock, dos de relaciones de compras y tres de repetición del catálogo. La prueba del precio mínimo comprueba el límite de `MinValueValidator(1)` ya definido en el modelo; no cambia la política ni los precios de los productos del catálogo. Todos los casos utilizan la base temporal de tests; la base principal y las cuatro cargas masivas existentes no se modificaron.

La protección del proveedor se comprueba con un proveedor ficticio nuevo, asociado solamente a una compra. Así se identifica la relación `CompraProveedor.proveedor` con `PROTECT`, sin depender de productos que también impidan su eliminación. La prueba de eliminación utiliza una compra con detalles y verifica el comportamiento de `DetalleCompra.compra` con `CASCADE`. No comprueba un CRUD completo de compras ni una gestión automática del stock.

Las pruebas del catálogo repiten `cargar_catalogo` sobre registros existentes. Un caso compara las cantidades de los diez modelos antes y después; otro conserva el nombre, teléfono y estado editados de un cliente; el tercero conserva el precio, stock cero y estado inactivo de un producto. Se mantienen el correo y el código utilizados como claves de búsqueda por `get_or_create`. La comprobación no afirma que una clave modificada siga identificando el mismo registro inicial.

Se restauraron el autocompletado y los formularios de detalles dentro de boletas y compras. La prueba existente de acceso verifica los diez formularios de creación, los detalles integrados y las búsquedas de los campos autocompletados. El subtotal solo se calcula cuando el detalle ya está guardado, para que los formularios vacíos no produzcan errores. La verificación posterior a la restauración terminó con las 36 pruebas aprobadas. El ajuste no modifica los modelos, las diez migraciones, el diagrama ni los comandos de Faker.

## 9. Correspondencia con los diez indicadores de la rúbrica

| N.º | Indicador resumido | Máximo | Evidencia del proyecto | Comprobación pendiente ante el docente |
| --- | --- | ---: | --- | --- |
| 1 | Conexión y configuración de la base | 10 | SQLite en settings.py; conexión e integridad verificadas. | Identificar la base y explicar la configuración. |
| 2 | Modelos, atributos, tipos, claves y relaciones | 10 | Diez modelos en models.py y diagrama correspondiente. | Explicar campos, claves y decisiones de relaciones. |
| 3 | Migraciones, diagrama y datos Faker almacenados | 10 | Diez migraciones, esquema y cuatro cargas locales verificadas. | Ejecutar las cargas y explicar el historial. |
| 4 | Acceso y modelos registrados en Admin | 10 | Diez modelos registrados; administrador creado en la base local y acceso a los diez listados comprobado. | Preparar una cuenta si se utiliza otra base o computador e ingresar durante la demostración. |
| 5 | Presentación y usabilidad del administrador | 10 | Columnas, búsqueda, filtros, grupos, paginación y títulos. | Mostrar su uso y explicar la configuración. |
| 6 | Creación de registros desde Admin | 10 | Pruebas de creación y consulta de productos y clientes persistidos. | Crear un registro y verificarlo presencialmente. |
| 7 | Consulta y verificación de datos | 10 | Listados, búsquedas, filtros y consultas SQLite. | Buscar y mostrar información almacenada. |
| 8 | Modificación y persistencia desde Admin | 10 | Pruebas de edición y nueva consulta de productos y clientes; cambio del producto visible en catálogo. | Modificar y comprobar el registro nuevamente. |
| 9 | Eliminación y persistencia desde Admin | 10 | Borrado de productos y clientes sin referencias; protección de clientes con boletas y eliminación de detalles al borrar la boleta. | Eliminar un registro sin referencias y verificarlo. |
| 10 | Demostración y explicación de Django Admin | 10 | Recorrido y explicación de archivos en esta guía. | Defensa presencial del estudiante. |
| | Máximo posible | 100 | Cobertura técnica local; no es una calificación asignada. | La puntuación la determina el docente. |

## 10. Preparación de la explicación del código

La defensa debe poder ubicar cada parte: `settings.py` configura la base y la aplicación; `models.py` define las tablas y relaciones; `migrations/` conserva los cambios de estructura; `admin.py` habilita y configura la gestión; los comandos cargan y comprueban datos ficticios. `views.py` consulta productos para la interfaz conservada. El CRUD de E2 lo resuelve Django Admin, sin construir formularios ni vistas administrativas propias.

Antes de la clase corresponde practicar por qué un producto tiene claves foráneas, qué diferencia existe entre `makemigrations` y `migrate`, qué se conserva en un precio histórico y por qué un registro protegido no se elimina. También debe explicarse la diferencia entre `Cliente` y el usuario administrativo, cómo funciona el bucle de Faker y cómo se comprueba que una inserción quedó en SQLite. Una ejecución correcta no prueba, por sí sola, que el estudiante pueda explicar esas decisiones.

## 11. Publicación y entrega

La publicación de E2 utiliza la rama `evaluacion-2` del repositorio [YkzPam/SoundShopCL](https://github.com/YkzPam/SoundShopCL). La rama `evaluacion1` permanece en E1. Para identificar la versión entregada, consultar el hash completo del último commit de la rama publicada; no utilizar el hash de E1 ni un commit que solo exista localmente.

La entrega al docente incluye el enlace de GitHub a E2 y el hash de ese commit. La imagen PNG del diagrama debe adjuntarse según las instrucciones de la plataforma. El enlace a un commit identifica exactamente el código revisado, incluso si después se añaden otros cambios. Publicar el repositorio no equivale a enviar la tarea de AAI ni a cumplir la asistencia y la defensa presencial.

## 12. Material de referencia utilizado

La guía se contrastó con *E2 Evaluacion_inv_Caso_Semestral_Music_pro_U2 Backend (2).pdf* y *E2 Escala_Apreciacion_U2 Backend (1).xlsx*, entregados por el docente, más el correo y la exigencia de clase confirmada de diez tablas y diez migraciones. El PDF de trece páginas explicita filtros, búsquedas, personalización y las cuatro cargas en sus páginas 9 a 11. Las marcas de ejemplo de la planilla no se interpretan como una nota obtenida por este proyecto.

Café y Código. (s. f.). *django-examples* [Repositorio de código]. GitHub. https://github.com/cafeycodigo/django-examples

El ZIP del repositorio del docente se utilizó como referencia de SQLite, modelos, opciones de ModelAdmin, migraciones y seeding. El archivo requirements.txt de E2 ahora coincide con sus cinco dependencias y versiones. Los modelos y los comandos siguen adaptados a la tienda musical; no se copian las aplicaciones ajenas al caso. La coincidencia del entorno no implica que ambos proyectos sean idénticos.

*Ejercicios de Migraciones, Modelos y Administrador en Django*. (s. f.). AAI INACAP, Unidad 2 de Framework back end [Material del curso con acceso institucional]. https://aai.inacap.cl/mod/page/view.php?id=2336194

Se verificó el contenido escrito de ese apartado y sus pasos de entorno, aplicación, modelos y migraciones. Los dos videos enlazados se abrieron en Chrome: YouTube indicó que no había subtítulos, la exportación de transcripción no encontró texto y los paneles de transcripción quedaron vacíos. No se considera revisada su explicación audiovisual completa. Esa revisión requiere un archivo o una transcripción accesible; no se afirma haber reproducido todas las clases.
