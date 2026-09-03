# 4. Auditoría de cumplimiento de la pauta

## 4.1 Evidencia por indicador

| N.º | Indicador evaluado | Evidencia dentro del proyecto | Estado |
|---:|---|---|---|
| 1 | Atributos, tipos y diagrama según el caso | `core/models.py`, `catalogo.json`, `docs/modelo-datos-y-validaciones.md` y `docs/diagrama-flujo.svg` | Cumplido |
| 2 | Entradas, salidas y validaciones de formularios | `core/forms.py`, vistas del carrito y sección 2.2 del documento de datos | Cumplido |
| 3 | Vistas con ciclos y condiciones coherentes con el flujo | `core/views.py` filtra, calcula, decide estados y prepara colecciones iterables | Cumplido |
| 4 | Plantillas que muestran variables y operadores del servidor | Plantillas `core`, herencia desde `base.html`, `{% for %}`, `{% if %}`, filtros y `{% url %}` | Cumplido |
| 5 | Paquetes y librerías externas configuradas | `requirements.txt`, `package.json`, Tailwind CSS compilado y `package-lock.json` | Cumplido |
| 6 | Módulos Django, estilos y repositorio GitHub | Formularios, sesiones, mensajes, archivos estáticos, CSRF, Tailwind y repositorio Git local con historial segmentado | Pendiente solo la publicación pública |
| 7 | Proyecto y aplicación creados y registrados | Proyecto `soundshop`, aplicación `core` en `INSTALLED_APPS` y comandos documentados | Cumplido |
| 8 | Rutas limpias, modulares, semánticas y nombradas | `soundshop/urls.py` incluye `core.urls`; todas las rutas usan `path()` y `name` | Cumplido |
| 9 | Vistas reciben `request`, crean contexto y renderizan | Funciones de `core/views.py` y helper `_datos_catalogo` | Cumplido |
| 10 | Validación de sintaxis, rutas y visualización con apoyo de IA | `manage.py check`, quince pruebas, capturas de `docs/mockups-prototipo.md` y registro de IA | Cumplido |

## 4.2 Comprobaciones reproducibles

```powershell
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py test --verbosity 2
npm run build:css
git status
git log --oneline
```

El resultado esperado de Django es `System check identified no issues` y quince pruebas aprobadas. El compilador debe producir `static/css/tailwind.css`. La aplicación debe responder con código HTTP 200 en la portada, catálogo, categorías, productos existentes y carrito. La revisión automatizada del navegador comprobó anchos de 1440, 768, 390 y 320 píxeles sin desbordamiento horizontal ni errores de consola.

## 4.3 Límites declarados

La tabla mide la primera evaluación y no afirma funciones que el proyecto todavía no posee. No existe autenticación, administración persistente, historial real, pasarela de pago ni seguimiento logístico. Esas capacidades requieren base de datos y corresponden al desarrollo posterior del caso semestral.

El código todavía no posee un remoto de GitHub. La publicación se marcará como cumplida solo después de comprobar una URL pública que contenga la rama `main` y el historial completo; no se considera suficiente que el repositorio exista únicamente en el computador.
