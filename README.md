# SoundShop CL

Repositorio público de la entrega: [YkzPam/SoundShopCL](https://github.com/YkzPam/SoundShopCL). La documentación, el diagrama original y las capturas están incluidos en la carpeta `docs`.

La identidad visual vigente utiliza marfil, negro, dorado suave y violeta. La descripción del sistema y las pruebas del rediseño se encuentran en [Identidad visual](docs/identidad-visual.md); la selección final de capturas está en [Prototipo de interfaz](docs/mockups-prototipo.md), con el prefijo `final-`.

La vista inicial de [Gestión de productos](http://127.0.0.1:8000/gestion/productos/) permite validar fichas comerciales y calcular sus salidas sin publicar cambios. La evidencia del indicador 2 se encuentra en [Formularios administrativos](docs/indicador-2-formularios.md).

SoundShop CL es el prototipo de una tienda musical chilena desarrollado para la Evaluación 1 de Programación Backend. La aplicación reúne diez productos en cinco categorías, permite buscar y filtrar, revisar fichas detalladas, crear una cuenta de sesión, modificar un carrito y completar un pedido temporal.

La entrega usa Django 5.2 LTS, plantillas DTL, datos JSON, Tailwind CSS y JavaScript. No se conecta a una base de datos porque esa integración pertenece a las siguientes unidades del caso semestral. El carrito y el nombre visible de la cuenta se guardan temporalmente en una cookie firmada por Django. Cuenta ofrece formularios separados para crear una cuenta e iniciar sesión. El servidor conserva temporalmente un identificador derivado del correo, el nombre y el hash de la contraseña en memoria; las credenciales no se incluyen en la cookie. Reiniciar el servidor elimina estas cuentas. Este acceso local de un proceso no sustituye autenticación persistente ni un despliegue seguro de producción.

## Diagrama de flujo de la Evaluación 1

El diagrama se puede revisar directamente en [Excalidraw, mediante este enlace compartido](https://excalidraw.com/#json=5k4AdvqFxTW7Augb5Dje6,N09tmaInLWdoyR_nV9ib3Q). La carpeta `docs` contiene la [imagen PNG exportada desde Excalidraw](docs/diagrama-flujo.png), la [versión SVG](docs/diagrama-flujo.svg) y el [archivo editable de Excalidraw](docs/diagrama-flujo.excalidraw). La imagen conserva la composición vertical original; no es una recreación del diagrama.

## Funciones incluidas

- Portada responsive, limpia y centrada en una sola fotografía protagonista, tipografía XXL y accesos directos.
- Cinco categorías con fotografías y composición asimétrica abierta en el inicio y en su directorio.
- Página independiente Nosotros, con presentación de SoundShop CL y sus áreas de catálogo.
- Cuenta en su propia ruta, con una composición tipográfica centrada y formularios separados de acceso y registro.
- Catálogo generado en el servidor mediante ciclos `{% for %}` y condiciones `{% if %}`.
- Búsqueda sin distinción de mayúsculas ni tildes.
- Filtros combinables por categoría, precio máximo y stock.
- Orden por destacados, nombre o precio.
- Tarjetas con estados de stock claros, movimiento al pasar el mouse y vista rápida accesible.
- Ficha de producto con especificaciones, precio, disponibilidad, ampliación de imagen y productos relacionados.
- Carrito temporal con agregado sin recargar, confirmación visual, mini carrito, edición y control de stock.
- Carrito de invitado: cualquier visitante puede agregar, editar y eliminar productos. La cuenta se solicita solo al continuar con el pedido y la selección se conserva después del acceso.
- Creación de cuenta con validación de correo, contraseña, confirmación, aceptación de condiciones y regreso seguro al producto solicitado.
- Modo claro y oscuro con preferencia guardada en el navegador.
- Animaciones vinculadas al scroll, profundidad en imágenes, microinteracciones por categoría y respuesta visual al seleccionar un producto.
- Confirmación de pedido con código temporal, sin pago ni persistencia comercial.
- Mensajes de validación, rutas nombradas y redirecciones ante identificadores inválidos.
- Cincuenta pruebas automáticas que no requieren base de datos.

La interfaz utiliza negro `#121212`, marfil `#F4F0E8`, dorado `#B89B5E`, violeta `#4B2E5A` y texto claro `#F8F6F2`. El modo oscuro adapta superficies y contraste con variantes claras del violeta para textos pequeños. Una sola navegación acompaña los títulos amplios, las fotografías abiertas y los formularios sin contenedores pesados. Segoe UI Variable, con alternativas locales, se combina con Georgia en algunos títulos. La hoja `static/css/identity.css` reúne el sistema visual actual; las hojas anteriores permanecen como historial y no se cargan desde la plantilla base. Se conserva Tailwind compilado. Las animaciones de entrada, el acercamiento de las fotografías, los diálogos y el desplazamiento de la portada respetan la reducción de movimiento del sistema y el control del pie de página.

## Instalación en Windows y Visual Studio Code

### 1. Abrir el proyecto

En Visual Studio Code, se selecciona **Archivo > Abrir carpeta** y se abre la carpeta `SoundShopCL`. La carpeta local y el repositorio de GitHub utilizan este mismo nombre. Al descargar mediante Download ZIP, GitHub añade el sufijo `-main` al archivo y a la carpeta. El repositorio ya contiene recomendaciones, tareas y una configuración de depuración dentro de `.vscode`.

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

Cada colección incorpora una portada editorial propia, un equipo destacado y dos notas de orientación basadas en el catálogo. Las composiciones usan formas relacionadas con audífonos, vinilo, grabación, cuerdas y escenario, conservando la paleta de la tienda. El movimiento incluye entrada de página, revelado al recorrer secciones, profundidad limitada al scroll y respuesta al puntero. El pie de página permite reducirlo y guardar la preferencia; la configuración de movimiento reducido del sistema siempre tiene prioridad. Los enlaces navegan sin retardos artificiales. El enlace antiguo `/#nosotros` se redirige en el navegador a `/nosotros/`.

| Ruta | Nombre Django | Función |
|---|---|---|
| `/gestion/productos/` | `core:gestion_productos` | Validación de ficha administrativa |
| `/gestion/productos/<id>/` | `core:gestion_producto` | Selección de ficha por identificador |
| `/` | `core:inicio` | Portada y productos destacados |
| `/nosotros/` | `core:nosotros` | Presentación y propósito de la tienda, fuera del inicio |
| `/productos/` | `core:catalogo` | Catálogo, filtros y ordenamiento |
| `/productos/<id>/` | `core:detalle_producto` | Ficha dinámica de un producto |
| `/categorias/` | `core:categorias` | Directorio fotográfico con las tarjetas compartidas del inicio |
| `/categorias/<slug>/` | `core:detalle_categoria` | Colección con cabecera, navegación entre categorías y filtros |
| `/buscar/?q=texto` | `core:buscar` | Resultado de búsqueda |
| `/carrito/` | `core:carrito` | Resumen y edición del carrito |
| `/pedido/confirmado/` | `core:pedido_confirmado` | Resultado del pedido temporal |
| `/registro/` | `core:registro` | Inicio de sesión; `?modo=crear` abre la creación de cuenta |
| `/registro/confirmado/` | `core:registro_confirmado` | Confirmación de la sesión activa |
| `/cuenta/salir/` | `core:cerrar_sesion` | Cierre de sesión mediante `POST` |

Las operaciones que alteran el carrito aceptan únicamente solicitudes `POST` y están protegidas con token CSRF. Agregar, actualizar y eliminar productos no exige una cuenta; confirmar el pedido sí mantiene la validación de sesión en el servidor. La vista rápida utiliza la misma ruta y recibe un resumen JSON cuando JavaScript solicita actualizar el mini carrito; si JavaScript no está disponible, el formulario conserva el flujo Django tradicional. Los retornos posteriores al acceso solo aceptan rutas locales para impedir redirecciones externas. El pedido sigue siendo temporal: no existe pasarela de pago ni cobro real.

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

- [Preparación y condiciones de entrega](docs/preparacion-entrega.md)
- [Lámina de mockups esquemáticos del diseño actual](docs/mockups-esquematicos.svg)
- [Verificación final de la entrega](docs/verificacion-entrega.md)
- [Investigación de tiendas similares](docs/investigacion-referentes.md)
- [Alcance de la Evaluación 1](docs/alcance-evaluacion-1.md)
- [Modelo de datos, entradas y validaciones](docs/modelo-datos-y-validaciones.md)
- [Arquitectura y flujo de navegación](docs/arquitectura-y-flujo.md)
- Diagrama de flujo: [abrir en Excalidraw](https://excalidraw.com/#json=5k4AdvqFxTW7Augb5Dje6,N09tmaInLWdoyR_nV9ib3Q), [descargar el archivo editable](docs/diagrama-flujo.excalidraw) o [consultar la vista previa](docs/diagrama-flujo.png)
- [Mockups y evidencia del prototipo](docs/mockups-prototipo.md)
- [Auditoría de los diez indicadores](docs/auditoria-rubrica.md)
- [Registro del apoyo de inteligencia artificial](docs/uso-inteligencia-artificial.md)
- [Guion breve para la demostración](docs/guion-demostracion.md)

## Git y publicación en GitHub

El repositorio público está en [GitHub](https://github.com/YkzPam/SoundShopCL), utiliza la rama `main` y conserva el historial del proyecto. Para obtener la entrega en otro computador:

```powershell
git clone https://github.com/YkzPam/SoundShopCL.git SoundShopCL
cd SoundShopCL
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py test
.\venv\Scripts\python.exe manage.py runserver
```

En el archivo original, los commits locales se identifican como `SoundShop CL Student`, con el correo técnico no entregable `soundshopcl@local.invalid`. La cuenta propietaria del repositorio es `YkzPam`; no se presenta ese correo técnico como una dirección personal del estudiante.

La publicación contiene código y documentación, no un sitio Django alojado en GitHub Pages. El docente puede clonar el proyecto y seguir la instalación para ejecutar la aplicación. No se incluyen `venv`, `node_modules`, bases de datos ni archivos `.env`. La configuración de Django corresponde únicamente al servidor local de esta entrega.

## Decisiones de la primera entrega

`core/models.py` utiliza `dataclasses` para describir las entidades y sus tipos. Los registros se cargan desde `core/data/catalogo.json`, se convierten en objetos Python y se envían a cada plantilla mediante diccionarios de contexto. La cuenta de esta etapa valida los datos y abre una sesión firmada para proteger la compra; no reemplaza el modelo de usuarios ni la autenticación persistente que requieren ORM y base de datos.

Los nombres, precios y marcas del catálogo son ficticios. Las diez imágenes de productos y la variante panorámica de portada fueron creadas específicamente para SoundShop CL, optimizadas en WebP y no contienen logotipos de terceros. El pedido final no es una transacción comercial.
