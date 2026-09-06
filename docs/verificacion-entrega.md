# 8. Registro de verificación de entrega

## 8.1 Comprobaciones del 6 de septiembre de 2026

| Comprobación ejecutada | Resultado |
|---|---|
| `python manage.py check` | Sin problemas detectados |
| `python manage.py test` | 50 pruebas aprobadas; 6,867 segundos en esta ejecución |
| Formularios administrativos | Seis pruebas incluidas: límites, cálculo, estados, errores, JSON intacto, CSRF y escape |
| Revisión de navegador local | 9 rutas × 3 anchos × 2 temas = 54 combinaciones |
| Anchos comprobados | 390, 768 y 1440 píxeles |
| Temas comprobados | Claro y oscuro, con reducción de movimiento |
| Estado de las 54 vistas | HTTP 200, un H1 y sin desbordamiento horizontal del documento |
| Imágenes con origen definido y errores de ejecución JS | Sin fallos detectados en esas vistas |
| Capturas nuevas | 36 archivos `final-*`, escritorio y móvil en ambos temas |

Las rutas verificadas fueron Inicio, catálogo, categorías, producto 1, Nosotros, ingreso, creación de cuenta, carrito vacío y gestión. Las capturas se generaron con un navegador Chromium y son exportaciones de la aplicación local. Los controles de imagen vacíos de diálogos cerrados se excluyeron del chequeo de recursos; no se presentaron como imágenes rotas del contenido.

## 8.2 Alcance de las comprobaciones

La suite de Django contrasta solicitudes y validaciones, incluido el carrito de invitado y la confirmación con sesión. La revisión visual de esta fecha no ejecutó todas las combinaciones de compra ni reemplaza pruebas en dispositivos físicos. Se inspeccionó visualmente la captura móvil de gestión para comprobar legibilidad, distribución y continuidad de la página. Las demás capturas quedan disponibles para la revisión del estudiante y del docente.

## 8.3 Cierre de publicación y presentación

El proyecto se publicó en [YkzPam/SoundShopCL](https://github.com/YkzPam/SoundShopCL). La primera subida de esta revisión se identificó con `a72e359`; la rama remota coincidió con la local y el repositorio respondió HTTP 200 sin sesión. Se incorporó después un cierre documental y el editable extraído de la escena incrustada en el SVG original de Excalidraw, para conservar las mismas flechas lisas del PNG. El PNG del proyecto coincide por SHA-256 con el exportado desde Excalidraw.

La comprobación de enlaces locales recorrió 16 documentos Markdown sin destinos inexistentes. La aprobación del alcance por el docente y la demostración corresponden a actividades externas a estas pruebas. El documento no garantiza 100 puntos ni presenta como otorgada una calificación de la rúbrica.
