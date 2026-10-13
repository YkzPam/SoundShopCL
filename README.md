# SoundShop CL — Tienda musical

Proyecto individual de una tienda de equipos musicales desarrollado con Django. La Evaluación 2 continúa el trabajo de la Evaluación 1 y agrega SQLite, diez modelos propios, diez migraciones de `core`, un diagrama de base de datos, Django Admin y generación de clientes ficticios con Faker. La interfaz de la tienda se conserva; no se implementan los contenidos de la Evaluación 3.

## 1. Ejecución desde Visual Studio Code

Seleccionar la rama [evaluacion-2](https://github.com/YkzPam/SoundShopCL/tree/evaluacion-2) antes de descargar desde **Code → Download ZIP**. La rama `evaluacion1` conserva la primera entrega y no contiene esta ampliación. Extraer la descarga y abrir en Visual Studio Code la carpeta que contiene `manage.py`. Las plantillas HTML de Django no se ejecutan directamente al hacer doble clic.

Con Python 3.12 o superior instalado, ejecutar en la terminal integrada:

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py migrate
.\venv\Scripts\python.exe manage.py cargar_catalogo
.\venv\Scripts\python.exe manage.py createsuperuser
.\venv\Scripts\python.exe manage.py runserver
```

Las cinco versiones de `requirements.txt` coinciden con el archivo del ZIP `django-examples-main.zip` entregado por el docente: Django 6.1.1, Faker 40.40.0, asgiref 3.12.1, sqlparse 0.6.0 y tzdata 2026.5. Esta coincidencia corresponde al entorno de referencia; no significa que se hayan copiado sus otras aplicaciones ni que la rúbrica exija literalmente esas versiones.

Si el entorno `venv` ya existe, no hace falta crearlo otra vez. Para actualizarlo y comprobar sus dependencias, ejecutar:

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe -m pip check
.\venv\Scripts\python.exe -m pip freeze
```

El asistente de `createsuperuser` solicita un nombre de usuario, correo y contraseña elegidos por el propietario. La contraseña no se muestra mientras se escribe. No existe una contraseña administrativa pública ni una cuenta administrativa incluida en la descarga.

- Tienda: <http://127.0.0.1:8000/>.
- Django Admin: <http://127.0.0.1:8000/admin/>.

También se pueden utilizar las tareas de **Terminal → Ejecutar tarea**. Sus nombres comienzan con **E2:**; permiten instalar y verificar las dependencias, revisar la configuración, aplicar migraciones, cargar el catálogo, crear el administrador, probar la aplicación y elegir la cantidad de clientes ficticios. Primero debe existir el entorno `venv`. La tarea de creación del administrador solicita las credenciales en la terminal y no las guarda en los archivos del proyecto.

Bootstrap, las imágenes, el CSS y el JavaScript están incluidos en `static/`. La tienda no necesita Node ni una compilación de estilos. Las animaciones requieren ejecutar Django, cargar la página en el navegador y tener permitidas las animaciones en las preferencias de accesibilidad del dispositivo.

## 2. Datos y acceso administrativo

La aplicación utiliza `db.sqlite3`, creado por las migraciones. Este archivo y el entorno virtual no se publican en GitHub: cada computador crea su propia base y su propio administrador siguiendo el apartado anterior. Iniciar sesión en GitHub no inicia sesión en Django Admin.

Antes de la demostración, comprobar que las diez migraciones de `core` estén aplicadas y que la cuenta administrativa permita entrar a Django Admin. La preparación de una copia local no prepara automáticamente una descarga en otro computador.

El administrador se crea una sola vez por base de datos, no cada vez que se inicia el servidor. Una descarga nueva no incluye los usuarios ni la contraseña del computador original. Puede elegirse el mismo nombre de usuario en el otro equipo, pero será una cuenta independiente. Si ya existe una cuenta administrativa en esa base, se utiliza la existente; no hace falta crear otra para cada práctica.

La preparación y la comprobación antes de la clase se detallan en [Preparación del administrador en otro PC](docs/evaluacion-2/README.md#21-preparación-y-comprobación-del-administrador-en-otro-pc). Las credenciales deben conservarse de forma privada, fuera de los archivos publicados. No se incorpora una contraseña fija ni una creación automática de superusuarios al código.

El catálogo público consulta la base de datos. Los cambios guardados en los productos desde Django Admin se muestran al volver a cargar la tienda. `core/data/catalogo.json` se conserva como fuente del catálogo inicial; editar ese JSON no sustituye la gestión de registros en SQLite. La carga inicial puede repetirse sin sobrescribir los productos ya editados.

El enlace **Panel de administración** abre Django Admin. El acceso exige un usuario activo con permisos administrativos. Los diez modelos de la tienda están registrados con opciones de consulta; productos y clientes incluyen búsqueda, filtros y paginación.

Las boletas y compras permiten agregar sus detalles dentro del mismo formulario mediante `TabularInline`. El cliente de la boleta y las relaciones de los detalles utilizan los selectores normales de Django Admin, sin autocompletado. Los apartados independientes de detalles, las búsquedas y los filtros de los listados se conservan.

La cuenta y el carrito de cliente conservan el recorrido simulado de la primera entrega. El registro de la tienda no crea una cuenta permanente y el carrito no genera ventas ni cobros. El modelo `Cliente` almacena datos comerciales; no es una cuenta de acceso de Django. Las boletas y compras de esta evaluación se administran desde Django Admin.

## 3. Archivos de la Evaluación 2

```text
SoundShopCL/
├── manage.py
├── requirements.txt
├── .vscode/tasks.json
├── soundshop/
│   ├── settings.py              Configuración de SQLite
│   └── urls.py                  Entrada a Django Admin
├── core/
│   ├── models.py                Diez modelos de la tienda
│   ├── admin.py                 Registro y opciones de Django Admin
│   ├── migrations/              Diez cambios generados por Django
│   ├── management/commands/
│   │   ├── cargar_catalogo.py    Catálogo y registros relacionados
│   │   └── generar_clientes.py   Faker con cantidad verificable
│   ├── views.py                 Consulta del catálogo para la tienda
│   ├── templates/               Interfaz conservada
│   └── tests.py                 Verificación de modelos y Admin
├── static/                      Imágenes, estilos y animaciones locales
└── docs/evaluacion-2/            Guía y diagrama de base de datos
```

## 4. Diagramas, pruebas y defensa

- [Guía de E2: modelos, migraciones, Admin y Faker](docs/evaluacion-2/README.md).
- [Diagrama de base de datos en PNG](docs/evaluacion-2/diagrama-base-datos.png), [SVG](docs/evaluacion-2/diagrama-base-datos.svg) y [editable de Excalidraw](docs/evaluacion-2/diagrama-base-datos.excalidraw).
- [Correspondencia del esquema con los modelos](docs/evaluacion-2/esquema.json).

El diagrama contiene solamente las diez tablas propias, sus atributos, claves y relaciones. Las tablas internas de usuarios, sesiones y migraciones de Django no se cuentan entre las diez tablas de la tienda.

Para ejecutar las pruebas y revisar el historial:

```powershell
.\venv\Scripts\python.exe manage.py test core --verbosity 2
.\venv\Scripts\python.exe manage.py showmigrations core
.\venv\Scripts\python.exe manage.py makemigrations core --check --dry-run
```

La guía de E2 incluye los resultados de las cuatro cargas locales. Esas pruebas no sustituyen las cargas y la defensa presencial con el docente. La calificación depende de esa demostración y de la revisión de la entrega.

La ampliación de las pruebas del administrador se documenta en [Pruebas adicionales de administración](docs/evaluacion-2/README.md#81-pruebas-adicionales-de-administración). Comprueba el CRUD de clientes, los correos inválidos o duplicados y las reglas de eliminación entre clientes, boletas y detalles mediante solicitudes a Django Admin y consultas a la base temporal de tests; no requiere agregar modelos ni funciones a la aplicación.

Las [Pruebas de límites, relaciones y carga inicial](docs/evaluacion-2/README.md#82-pruebas-de-límites-relaciones-y-carga-inicial) incluyen cantidades inválidas de Faker, precio y stock, protección de proveedores y repetición del catálogo sin duplicar ni sobrescribir los registros identificados por sus claves existentes. La verificación del 13 de octubre de 2026 terminó con 43 pruebas aprobadas en una base temporal de tests, sin errores de configuración ni cambios pendientes de migración. La comprobación en otro computador y la defensa con el docente siguen siendo pasos separados.

## 5. Continuidad de la Evaluación 1 y publicación

La primera entrega se conserva intacta en la rama [evaluacion1](https://github.com/YkzPam/SoundShopCL/tree/evaluacion1), en el commit `381abd52a831058e2032d6c5d5eaefcf32cd8499`. La rama [evaluacion-2](https://github.com/YkzPam/SoundShopCL/tree/evaluacion-2) continúa esa misma tienda e incluye también los materiales de E1 como antecedentes para consultar las etapas del desarrollo.

Antecedentes de la Evaluación 1:

- [Análisis inicial del caso tienda](docs/01-analisis-tienda.md) y [datos y validaciones iniciales](docs/02-datos-y-validaciones.md).
- [Secuencia de la corrección](docs/03-pasos-correccion.md), [rúbrica anterior](docs/04-rubrica.md) y [verificación de E1](docs/05-verificacion.md).
- [Diagrama de flujo del cliente](docs/diagrama-flujo.excalidraw) y [diagrama administrativo de E1](docs/diagrama-administrador.excalidraw).
- [Mockups de E1](docs/mockups/index.html) y [prototipo HTML estático](prototipo-html/inicio.html).

Los documentos anteriores describen E1 y no sustituyen las instrucciones actuales de instalación, base de datos ni acceso administrativo. La guía vigente y el diagrama de base de datos de E2 están en `docs/evaluacion-2/`. El prototipo HTML es una maqueta de la etapa anterior; la tienda funcional de E2 se ejecuta con Django y utiliza las plantillas de `core/templates/`.

Para entregar E2, publicar el código actualizado y las migraciones en el mismo repositorio, verificar el último commit e informar su hash. Adjuntar también la imagen del diagrama de base de datos en la plataforma indicada por el docente. GitHub conserva el código; no ejecuta este servidor Django como una página de GitHub Pages.

El proyecto se limita al desarrollo y la demostración local. No incluye pagos reales, autenticación permanente de clientes, despliegue de producción ni un administrador propio para la Evaluación 3.
