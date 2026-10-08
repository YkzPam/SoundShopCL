# SoundShop CL — Evaluación 1 corregida

Tienda musical con Django, HTML, Bootstrap, CSS y JavaScript. La entrega se limita a las fases 1 y 3 de la guía: análisis, diagrama, prototipo HTML e integración inicial con rutas, vistas, datos JSON y plantillas. No corresponde a un sistema de tarjetas ni a una tienda de producción.

## 1. Ejecutar desde Visual Studio Code

Descargar el ZIP de GitHub, extraerlo y abrir **la carpeta que contiene `manage.py`** en Visual Studio Code. No abrir solamente un archivo HTML de las plantillas: esas páginas necesitan el servidor de Django.

En la terminal integrada, con Python 3.12 o superior disponible:

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py test core
.\venv\Scripts\python.exe manage.py runserver
```

Abrir <http://127.0.0.1:8000/>. No ejecutar `migrate`, no crear una base de datos ni instalar Node o Tailwind. Bootstrap y el JavaScript están incluidos dentro de `static/`; no requieren internet para visualizar la tienda después de instalar Django.

Las tareas de `.vscode/tasks.json` también permiten revisar configuración, ejecutar pruebas y abrir el servidor desde **Terminal → Ejecutar tarea**. Primero se debe crear `venv` e instalar las dependencias.

## 2. Accesos ficticios

| Rol de ejemplo | Correo | Contraseña pública de demostración |
| --- | --- | --- |
| Cliente | cliente@soundshop.example | Demo1234 |
| Administrador | admin@soundshop.example | Demo1234 |

Estos datos son públicos y ficticios. El acceso sólo permite representar la bifurcación por rol de la guía. No es autenticación para una tienda real. El formulario de registro valida los datos, pero no crea una cuenta permanente; sólo las dos cuentas del JSON permiten probar el acceso.

El panel `/gestion/` tiene dos secciones: productos y usuarios. Sus formularios muestran errores o una vista previa validada. **No guardan cambios en el JSON.** Se puede añadir al carrito como invitado; para confirmar la simulación se requiere acceso de ejemplo. No existe cobro ni pedido persistente.

## 3. Entregables

- [Análisis del caso tienda e investigación](docs/01-analisis-tienda.md).
- [Diagrama editable en Excalidraw](docs/diagrama-flujo.excalidraw), [vista SVG](docs/diagrama-flujo.svg) y [copia PNG](docs/diagrama-flujo.png).
- [Flujo del administrador en Excalidraw](docs/diagrama-administrador.excalidraw), [vista SVG](docs/diagrama-administrador.svg) y [copia PNG](docs/diagrama-administrador.png).
- [Prototipo HTML navegable](prototipo-html/inicio.html). Abrir el archivo local para visualizar las maquetas; sus formularios no procesan datos.
- [Mockups de las principales interfaces](docs/mockups/index.html). Bocetos de distribución, separados de las capturas de la aplicación.
- [Atributos, tipos y operaciones de los formularios](docs/02-datos-y-validaciones.md).
- [Pasos de la corrección adaptados a la tienda](docs/03-pasos-correccion.md).
- [Correspondencia con los diez indicadores](docs/04-rubrica.md).
- [Pruebas, límites y apoyo de IA](docs/05-verificacion.md).

Para editar los diagramas: abrir <https://excalidraw.com/>, usar **Abrir** e importar el archivo `.excalidraw` correspondiente. El enlace compartido de la versión anterior no representa esta corrección y se retiró de la documentación.

## 4. Archivos principales

```text
SoundShopCL/
├── manage.py
├── requirements.txt
├── soundshop/          Configuración y rutas principales
├── core/
│   ├── urls.py         Rutas con path() y name
│   ├── views.py        Petición, condiciones, contexto y render()
│   ├── forms.py        Formularios de Django
│   ├── data/           Catálogo y usuarios ficticios en JSON
│   ├── templates/      HTML y lenguaje de plantillas DTL
│   └── tests.py        Pruebas sin base de datos
├── static/             Bootstrap local, imágenes, CSS y JavaScript
├── prototipo-html/     Maquetas estáticas de la versión corregida
└── docs/               Análisis, diagrama, mockups y evidencias
```

`core/models.py` conserva el archivo inicial de `startapp`; no define modelos de base de datos. Las sesiones temporales utilizan cookies firmadas para recordar el rol de ejemplo y la selección del carrito. La clave de desarrollo incluida no debe usarse en producción.

## 5. Cambios respecto de la entrega anterior

Se reconstruyó la base de Django siguiendo los pasos de inicialización de la corrección. Se retiraron las cuentas en caché, el mantenimiento distribuido entre módulos, las operaciones AJAX del carrito, el mapa y las numerosas capas CSS. Se conservaron diez productos musicales, imágenes acotadas, un panel sencillo, modo claro/oscuro y efectos discretos de aparición y hover.

El repositorio contiene un prototipo local, no un sitio desplegado en GitHub Pages. Una descarga debe ejecutarse con Django según el apartado 1. La revisión técnica no garantiza una calificación: el docente evalúa la entrega y la explicación del estudiante.
