# 8. Registro de verificación de entrega

## Revisión documental de cierre: 7 de septiembre de 2026

Se corrigieron dos rótulos en la escena original de Excalidraw, sin agregar decisiones: el agregado incluye validar stock y cantidad; la revisión del carrito precede al intento de confirmar. El acceso regresa al carrito conservado. El enlace vigente se encuentra en [Arquitectura y flujo](arquitectura-y-flujo.md). El editable, el SVG y el PNG proceden de esa escena corregida. El PNG se verificó visualmente y su SHA-256 coincide con el descargado en el computador: `6eef7996e26f95c84ba36ce3fc21f97b70b8257f6b375511f93ca3915d7bc438`.

Se incorporó una lámina de mockups esquemáticos en SVG y PNG, inspeccionada visualmente. Se identifica como documentación retrospectiva y se distingue de las capturas reales. La preparación de la entrega separa los archivos terminados de la aprobación del docente, la demostración y el envío por la plataforma de la asignatura. No se cambió la lógica de Django ni se agregó persistencia. Los registros de versiones anteriores que siguen describen comprobaciones históricas, no el identificador de la revisión actual.

La revisión de cierre recorrió 17 documentos Markdown sin enlaces locales rotos. Desde la carpeta del proyecto, `manage.py test` ejecutó las 50 pruebas y todas aprobaron en 6,964 segundos. Se comprobó que el enlace antiguo ya no figura en la documentación y que la flecha de retorno del editable llega al nodo de revisión del carrito. Se mantuvieron las capturas finales de la versión visual publicada, ya que este cierre no modificó la interfaz.

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

Una clonación independiente de la publicación `2194be7` completó `manage.py check` sin problemas y las 50 pruebas en 7,005 segundos. Se utilizó el entorno Python ya instalado, pero el código se obtuvo desde GitHub; no constituye una instalación de dependencias desde cero en otro computador.

La comprobación de enlaces locales recorrió 16 documentos Markdown sin destinos inexistentes. La aprobación del alcance por el docente y la demostración corresponden a actividades externas a estas pruebas. El documento no garantiza 100 puntos ni presenta como otorgada una calificación de la rúbrica.

## 8.4 Ajuste del encuadre de categorías

El 6 de septiembre de 2026 se corrigió el recorte de las imágenes compartidas por Inicio y Categorías. Los marcos respetan la proporción cuadrada de las fotografías y utilizan `object-fit: contain`; el hover ya no amplía la imagen. El ajuste incluye la fila de Sonido en vivo, que antes cortaba el parlante por utilizar un marco horizontal. No se modificaron los datos ni el funcionamiento de Django.

La revisión cubrió ambas páginas en 320, 390, 768 y 1440 píxeles, en claro y oscuro: 16 combinaciones y 80 imágenes comprobadas, sin desbordamiento de página ni errores JavaScript detectados. Se revisaron carga, proporción y ausencia de ampliación, incluido hover en escritorio. Django completó nuevamente sus 50 pruebas. Se actualizaron las ocho capturas `final-inicio-*` y `final-categorias-*`; el detalle se puede consultar en [escritorio](evidencias/encuadre-sonido-en-vivo-light-1440.png) y [móvil](evidencias/encuadre-sonido-en-vivo-light-390.png).
