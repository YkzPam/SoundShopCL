# 5. Registro del apoyo de inteligencia artificial

## 5.1 Tareas asistidas

La inteligencia artificial apoyó la lectura comparada de la pauta y la escala de apreciación, la definición del alcance técnico, la propuesta de estructura Django, la revisión de rutas, la detección de errores de plantilla, la generación de pruebas y la evaluación visual responsive. El resultado se comprobó mediante comandos locales y navegación real; no se consideró válida una función solo por haber sido sugerida.

## 5.2 Consultas de trabajo representativas

- Identificar qué funciones pertenecen a la Evaluación 1 del caso de tienda y cuáles requieren base de datos en unidades posteriores.
- Proponer un modelo tipado para categorías y productos almacenados en JSON.
- Revisar que las vistas de Django entreguen contexto y que las plantillas utilicen ciclos, condiciones, variables y URLs nombradas.
- Crear casos de prueba para búsqueda, filtros, productos agotados, límites de stock, carrito, sesión obligatoria, retornos seguros, registro y confirmación de pedido.
- Revisar el comportamiento de la interfaz en escritorio, tableta y teléfono sin eliminar funciones.
- Comprobar el modo oscuro, la persistencia de la preferencia, las animaciones de scroll y la salida para movimiento reducido.
- Comprobar la vista rápida, el agregado asincrónico, el mini carrito, la ampliación de imagen y los mensajes de error de stock.

## 5.3 Recursos visuales generados

Se crearon diez imágenes originales: audífonos inalámbricos, audífonos de estudio, tornamesa, kit de limpieza de vinilos, micrófono, interfaz de audio, guitarra eléctrica de siete cuerdas, controlador MIDI, parlante activo y mezclador. Las cuatro incorporaciones se generaron como fotografía cuadrada de catálogo con fondo gris frío, equipos en grafito y plata, acentos cobalto o aqua, luz de estudio natural y sin texto, personas, marcas ni logotipos. Las copias finales se optimizaron a 1024 × 1024 píxeles en formato WebP y se guardaron en `static/img/productos`.

## 5.4 Verificación humana esperada

Antes de entregar, el estudiante debe recorrer la tienda, revisar que los textos coincidan con el caso seleccionado, ejecutar las pruebas, confirmar el historial Git y reemplazar la identidad local por su nombre y correo reales. También debe poder explicar cómo una ruta llama a una vista, cómo se carga el JSON, qué contiene el contexto y de qué forma DTL genera las tarjetas.
