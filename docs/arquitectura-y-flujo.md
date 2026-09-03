# 3. Arquitectura y flujo de navegación

## 3.1 Recorrido de una solicitud

```text
Navegador
   ↓ solicitud HTTP
soundshop/urls.py
   ↓ include("core.urls")
core/urls.py
   ↓ selecciona una vista por ruta
core/views.py
   ↓ consulta y valida
core/catalogo.py + core/forms.py + catalogo.json
   ↓ construye un diccionario de contexto
templates/*.html
   ↓ DTL procesa variables, ciclos y condiciones
Respuesta HTML + CSS + JavaScript
```

La configuración principal registra la aplicación `core`, la carpeta global de plantillas, los archivos estáticos, las sesiones firmadas y el sistema de mensajes. `core.urls` mantiene las rutas de negocio separadas de `soundshop.urls`. Cada ruta posee un atributo `name`, por lo que los enlaces se generan con `{% url %}` y no dependen de direcciones escritas manualmente.

## 3.2 Flujo del usuario

La portada ofrece dos entradas: catálogo completo y categorías. El catálogo acepta búsqueda y filtros; si encuentra productos, genera una tarjeta por elemento. Una ficha válida muestra sus especificaciones y habilita el formulario solo cuando existe stock. La cantidad se valida antes de modificar la sesión. El carrito recalcula subtotales y total en cada solicitud. La confirmación vacía el carrito y entrega una salida verificable.

Los errores no terminan en una página rota. Un producto inexistente vuelve al catálogo, una categoría inválida vuelve al listado y una cantidad fuera de rango mantiene al usuario en una página conocida con un mensaje explicativo.

## 3.3 Recursos visuales

Tailwind CSS se compila localmente desde `static/css/input.css`. `static/css/main.css` agrega el fondo, los paneles translúcidos y transiciones propias de SoundShop CL. El JavaScript se limita al menú móvil, cierre de mensajes y copia del código de pedido. El catálogo y el carrito continúan funcionando sin JavaScript porque las operaciones principales se resuelven en Django.

El diagrama completo está disponible en [diagrama-flujo.svg](diagrama-flujo.svg).
