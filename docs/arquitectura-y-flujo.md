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

La portada ofrece entradas al catálogo completo, cinco categorías, tres guías editoriales y el acceso de cuenta. El catálogo acepta búsqueda y filtros; si encuentra productos, genera una tarjeta por elemento. La vista rápida reutiliza los datos enviados por Django. Una persona sin sesión puede consultar la fotografía, el precio, el stock y las especificaciones, pero ve un bloque de acceso en lugar del formulario de compra. El registro valida nombre, correo, contraseña, confirmación y aceptación de condiciones; conserva únicamente el nombre visible en la cookie firmada y regresa a una ruta local segura cuando la compra inició desde una ficha.

Con la sesión activa, la vista rápida y la ficha habilitan la cantidad. El servidor vuelve a comprobar la cuenta, el stock y el límite solicitado antes de modificar el carrito. Una solicitud Ajax recibe el resumen necesario para actualizar el contador, la confirmación y el mini carrito; el flujo HTML tradicional redirige al carrito. La vista completa recalcula subtotales y total en cada solicitud. La confirmación exige nuevamente la sesión, vacía el carrito y entrega una salida verificable.

Los errores no terminan en una página rota. Un producto inexistente vuelve al catálogo, una categoría inválida vuelve al listado y una cantidad fuera de rango mantiene al usuario en una página conocida con un mensaje explicativo. Una compra anónima lleva al acceso sin alterar el carrito. El registro señala el campo exacto cuando la contraseña es débil, no coincide o faltan datos obligatorios; una dirección externa enviada como retorno se descarta.

## 3.3 Recursos visuales

Tailwind CSS se compila localmente desde `static/css/input.css`. `static/css/main.css` aplica la paleta azul noche, cobalto, gris frío y aqua, junto con la tipografía moderna y los componentes responsive propios de SoundShop CL. El JavaScript controla el menú móvil, el tema, las entradas por scroll, el paralaje, la inclinación de producto, la vista rápida, el mini carrito, la confirmación de agregado, la ampliación de imágenes y la copia del código de pedido. El catálogo, el registro y el carrito completo continúan funcionando sin JavaScript porque las operaciones principales se resuelven en Django; los paneles dinámicos actúan como una mejora progresiva.

El diagrama completo está disponible como [SVG editable](diagrama-flujo.svg) y como [PNG listo para insertar en la entrega](diagrama-flujo.png).
