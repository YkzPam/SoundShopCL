# 3. Aplicación de la secuencia de la corrección

## 3.1 Análisis, navegación y maquetación

La secuencia de referencia comienza investigando el caso seleccionado, define el diagrama y construye las interfaces HTML. Esta corrección adapta esos productos a una tienda musical. `01-analisis-tienda.md` identifica los referentes y el alcance; el diagrama representa la consulta, selección y confirmación, junto con el acceso por rol. Los mockups muestran la distribución de las vistas principales y `prototipo-html/` reúne maquetas estáticas navegables sin procesamiento de formularios.

El prototipo HTML de esta carpeta es una reconstrucción de la interfaz corregida, no una evidencia de que las maquetas se elaboraron antes del proyecto original. Sirve para separar la maquetación del procesamiento con Django. Las vistas de servidor y los datos dinámicos se encuentran en `core/`, mientras que la hoja propia, el JavaScript y Bootstrap se distribuyen como archivos locales de `static/`.

## 3.2 Entorno e inicialización del proyecto

El flujo general se complementa con `diagrama-administrador.excalidraw`. Ese diagrama muestra el acceso de ejemplo, el rol, el panel, los listados de productos y usuarios, el formulario seleccionado, la decisión de validación y el retorno con errores o con una vista previa. La aplicación no almacena la salida administrativa.

Antes de modificar el proyecto se conservó la versión anterior mediante un ZIP de archivos versionados, un respaldo de sus carpetas y un paquete recuperable del historial Git. Para esta corrección se volvió a generar el esqueleto con `python -m django startproject soundshop .` y `python manage.py startapp core`. Se reutilizó el entorno virtual existente, que ya tenía Django 5.2.17; no se afirma haber creado nuevamente ese entorno.

Para reproducir la instalación en otro equipo, el procedimiento comienza en una carpeta vacía o en la descarga del repositorio. En una descarga sólo se crea el entorno y se instalan los requisitos: no se ejecutan otra vez `startproject` ni `startapp`, porque esos archivos ya existen.

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

Al iniciar un proyecto desde cero, la secuencia que corresponde al ejemplo del docente es la siguiente:

```powershell
.\venv\Scripts\python.exe -m django startproject soundshop .
.\venv\Scripts\python.exe manage.py startapp core
```

## 3.3 Registro, rutas y vistas

`settings.py` incorpora `core.apps.CoreConfig` en `INSTALLED_APPS` y conserva las aplicaciones habituales del esqueleto. `soundshop/urls.py` incluye `core.urls`. Cada entrada de `core/urls.py` utiliza `path()` y un `name`; `core/views.py` define funciones que reciben `request`, leen JSON, aplican condiciones y devuelven `render(request, plantilla, contexto)`. Las plantillas se ubican en `core/templates/`, como en el ejemplo de la corrección.

La guía ilustra interfaces de tarjetas, pero el caso seleccionado necesita productos y usuarios. El panel se ubica en `/gestion/`, sin conflicto con la ruta del administrador incorporado de Django. No se usa ese administrador porque depende de modelos y base de datos. La configuración conserva las aplicaciones generadas, pero utiliza `DATABASES = {}`, sesiones en cookies y mensajes en cookies para esta demostración sin persistencia.

## 3.4 Comprobación y repositorio

La comprobación de configuración y las pruebas se ejecutan con `manage.py check` y `manage.py test core`. Las tareas de Visual Studio Code llaman a esos mismos comandos y al servidor local. Esta ejecución asistida utilizó herramientas de comprobación externas al terminal de Visual Studio Code; no se presenta como una ejecución dentro de su interfaz.

La corrección local debe revisarse antes de publicarse. La existencia del repositorio original en GitHub no demuestra que incluya estos archivos nuevos. La entrega sólo puede describirse como sincronizada después de publicar un commit y comprobar que el remoto contiene esa misma revisión.
