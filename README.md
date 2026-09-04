# SoundShop CL

SoundShop CL es el prototipo de una tienda musical chilena desarrollado para la Evaluación 1 de Programación Backend. La aplicación permite recorrer un catálogo, buscar productos, filtrar por categoría, precio y disponibilidad, revisar fichas detalladas, modificar un carrito, crear una cuenta de sesión y completar un pedido temporal.

La entrega usa Django 5.2 LTS, plantillas DTL, datos JSON, Tailwind CSS y JavaScript. No se conecta a una base de datos porque esa integración pertenece a las siguientes unidades del caso semestral. El carrito y el nombre visible de la cuenta se guardan temporalmente en una cookie firmada por Django. El correo y la contraseña del formulario de registro se validan, pero no se almacenan.

## Funciones incluidas

- Portada responsive con categorías y productos destacados.
- Catálogo generado en el servidor mediante ciclos `{% for %}` y condiciones `{% if %}`.
- Búsqueda sin distinción de mayúsculas ni tildes.
- Filtros combinables por categoría, precio máximo y stock.
- Orden por destacados, nombre o precio.
- Ficha de producto con especificaciones, precio, disponibilidad y productos relacionados.
- Carrito temporal con agregar, actualizar, eliminar y control de stock.
- Registro de cuenta con validación de correo, contraseña, confirmación y aceptación de condiciones.
- Confirmación de pedido con código temporal, sin pago ni persistencia comercial.
- Mensajes de validación, rutas nombradas y redirecciones ante identificadores inválidos.
- Veintidós pruebas automáticas que no requieren base de datos.

La interfaz utiliza una dirección visual contemporánea inspirada en catálogos técnicos de audio: azul noche, cobalto, gris frío y acentos aqua. La tipografía combina Bahnschrift, Aptos y las variantes modernas de Segoe UI disponibles en Windows. Las seis fotografías forman una colección de estudio coherente, sin marcas de terceros. Se evitaron movimientos continuos y la hoja de estilos respeta `prefers-reduced-motion`.

## Instalación en Windows y Visual Studio Code

### 1. Abrir el proyecto

En Visual Studio Code, se selecciona **Archivo > Abrir carpeta** y se abre la carpeta `SoundShopCL`. El repositorio ya contiene recomendaciones, tareas y una configuración de depuración dentro de `.vscode`.

### 2. Crear y activar el entorno virtual

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Si PowerShell no permite ejecutar el script de activación, los comandos pueden ejecutarse directamente con el intérprete del entorno:

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe manage.py runserver
```

En una terminal `cmd`, la activación equivalente es:

```bat
venv\Scripts\activate.bat
```

### 3. Instalar dependencias

```powershell
python -m pip install -r requirements.txt
npm install
npm run build:css
```

El archivo `static/css/tailwind.css` ya está compilado y versionado, por lo que `npm install` no es obligatorio para ejecutar la tienda. Solo se necesita cuando se modifican clases o estilos de Tailwind.

### 4. Ejecutar la aplicación

```powershell
python manage.py check
python manage.py test
python manage.py runserver
```

La tienda queda disponible en `http://127.0.0.1:8000/`. Para detener el servidor se utiliza `Ctrl + C`.

## Trabajo desde Visual Studio Code

La configuración incluida apunta a `venv\Scripts\python.exe`. Si el editor no lo selecciona automáticamente, se abre la paleta con `Ctrl + Shift + P`, se ejecuta **Python: Select Interpreter** y se elige el intérprete de la carpeta `venv`.

Las tareas se encuentran en **Terminal > Ejecutar tarea**:

- `Django: ejecutar servidor`
- `Django: ejecutar pruebas`
- `Tailwind: compilar CSS`
- `Tailwind: observar cambios`

La sección **Ejecutar y depurar** contiene la configuración `SoundShop CL: Django` para iniciar el servidor con el depurador de Python.

## Rutas principales

| Ruta | Nombre Django | Función |
|---|---|---|
| `/` | `core:inicio` | Portada y productos destacados |
| `/productos/` | `core:catalogo` | Catálogo, filtros y ordenamiento |
| `/productos/<id>/` | `core:detalle_producto` | Ficha dinámica de un producto |
| `/categorias/` | `core:categorias` | Resumen de categorías |
| `/categorias/<slug>/` | `core:detalle_categoria` | Productos de una categoría |
| `/buscar/?q=texto` | `core:buscar` | Resultado de búsqueda |
| `/carrito/` | `core:carrito` | Resumen y edición del carrito |
| `/pedido/confirmado/` | `core:pedido_confirmado` | Resultado del pedido temporal |
| `/registro/` | `core:registro` | Formulario de creación de cuenta |
| `/registro/confirmado/` | `core:registro_confirmado` | Confirmación y nombre de sesión |
| `/cuenta/salir/` | `core:cerrar_sesion` | Cierre de sesión mediante `POST` |

Las operaciones que alteran el carrito aceptan únicamente solicitudes `POST` y están protegidas con token CSRF.

## Estructura del proyecto

```text
SoundShopCL/
├── .vscode/                  Configuración y tareas del editor
├── core/
│   ├── data/catalogo.json    Datos simulados
│   ├── templatetags/         Filtros CLP y nombres de categoría
│   ├── catalogo.py           Lectura, búsqueda y cálculos
│   ├── forms.py              Formularios y validaciones
│   ├── models.py             Modelo de datos tipado con dataclasses
│   ├── urls.py               Rutas de la aplicación
│   ├── views.py              Vistas y contextos Django
│   └── tests.py              Pruebas automáticas
├── docs/                     Diagramas, alcance y auditoría de rúbrica
├── soundshop/                Configuración general del proyecto
├── static/                   CSS, JavaScript e imágenes
├── templates/                Plantillas DTL
├── manage.py
├── package.json
└── requirements.txt
```

## Documentación académica

- [Alcance de la Evaluación 1](docs/alcance-evaluacion-1.md)
- [Modelo de datos, entradas y validaciones](docs/modelo-datos-y-validaciones.md)
- [Arquitectura y flujo de navegación](docs/arquitectura-y-flujo.md)
- Diagrama de flujo: [SVG editable](docs/diagrama-flujo.svg) y [PNG listo para presentar](docs/diagrama-flujo.png)
- [Mockups y evidencia del prototipo](docs/mockups-prototipo.md)
- [Auditoría de los diez indicadores](docs/auditoria-rubrica.md)
- [Registro del apoyo de inteligencia artificial](docs/uso-inteligencia-artificial.md)
- [Guion breve para la demostración](docs/guion-demostracion.md)

## Git y publicación en GitHub

El repositorio usa la rama `main` y separa el trabajo en commits verificables. Mientras no se configure la identidad personal del estudiante, los commits locales emplean el nombre técnico `SoundShop CL Student` y el correo no publicable `soundshopcl@local.invalid`. Antes de publicar, se deben reemplazar por los datos de la cuenta real:

```powershell
git config user.name "Nombre Apellido"
git config user.email "correo-vinculado-a-github@example.com"
```

Después de crear un repositorio público vacío en GitHub, se conecta y publica con:

```powershell
git remote add origin https://github.com/USUARIO/SoundShopCL.git
git push -u origin main
```

No se debe subir la carpeta `venv`, `node_modules`, cookies, claves personales ni un archivo `.env`. Estas rutas ya están cubiertas por `.gitignore`.

## Decisiones de la primera entrega

`core/models.py` utiliza `dataclasses` para describir las entidades y sus tipos. Los registros se cargan desde `core/data/catalogo.json`, se convierten en objetos Python y se envían a cada plantilla mediante diccionarios de contexto. El registro agregado en esta etapa representa la interfaz y sus validaciones; no reemplaza el modelo de usuarios, la autenticación ni la persistencia que requieren ORM y base de datos.

Los nombres, precios y marcas del catálogo son ficticios. Las seis imágenes fueron creadas específicamente para SoundShop CL, optimizadas en WebP y no contienen logotipos de terceros. El pedido final no es una transacción comercial.
