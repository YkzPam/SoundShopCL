# Navegación, carrito de invitado y ubicación proyectada

Actualización del 5 de septiembre de 2026. El carrito puede utilizarse sin cuenta en la ficha de producto, vista rápida y página de carrito. Las validaciones de cantidad, stock, método POST y CSRF permanecen activas. Al continuar con el pedido, el servidor exige sesión y devuelve al acceso con destino local al carrito. La selección se mantiene al crear cuenta, cerrar sesión y volver a ingresar. No se agregó base de datos ni integración de pagos; la confirmación sigue siendo un pedido temporal, no una transacción bancaria.

Los enlaces Inicio, Productos, Categorías y Nosotros permanecen visibles entre 320 y 1440 píxeles. En tamaños de hasta 860 píxeles ocupan una línea dentro del encabezado. El menú complementario mantiene búsqueda y acceso de cuenta, incorpora Ubicación y calcula su posición según la altura real del encabezado. Al volver a escritorio se cierra, libera el desplazamiento y restituye el foco a la navegación visible. El símbolo circular incorpora un punto dorado que gira lentamente; la preferencia de movimiento reducido, del sistema o del sitio, detiene la animación.

La sección de Nosotros presenta el sector Apoquindo / Manquehue, Las Condes, como ubicación proyectada. A petición del usuario, el esquema inicial fue sustituido por el mapa real de Google Maps. El iframe proviene de la opción «Compartir → Insertar un mapa» de la estación Manquehue, consultada el 5 de septiembre de 2026. Se conserva la atribución y los controles originales de Google, sin filtros de color ni capas que bloqueen la interacción. El mapa carga al acercarse a la sección y requiere conexión a Internet; el enlace externo permite abrir el sector por separado. El marcador corresponde al Metro, no a un local de SoundShop. No se atribuye una dirección comercial, horario, fecha de apertura ni local existente a la tienda. Seleccionar ese sector es una decisión de diseño, no una confirmación de disponibilidad inmobiliaria.

## Verificación ejecutada

- `python manage.py test`: 50 pruebas satisfactorias, sin base de datos.
- `node work/qa-guest-navigation.cjs`: 40 revisiones de diseño sobre ficha y Nosotros, diez anchos (320, 390, 573, 768, 860, 861, 1024, 1100, 1101 y 1440), modo claro y oscuro; enlaces visibles y ausencia de desbordamiento horizontal.
- Interacciones reales en navegador: menú, Escape, cambio de tamaño, ruta Nosotros y ancla Ubicación; animación del símbolo y ambas preferencias de reducción de movimiento; agregado AJAX anónimo desde ficha y vista rápida; acceso solo al continuar; registro de prueba y regreso con total del carrito intacto. Ningún error JavaScript capturado.
- Resultados: `work/qa-guest-navigation-results.json`. Capturas de esta actualización: `docs/evidencias/guest-*.png`. El ZIP de entrega anterior no se regeneró con estos cambios.

## Referencia de ubicación

Municipalidad de Las Condes. (s. f.). *Buses eléctricos*. https://www.lascondes.cl/servicios/muevete-en-las-condes/buses-electricos/ (consulta: 5 de septiembre de 2026).

Google. (s. f.). *Compartir, enviar o imprimir indicaciones de Google Maps*. https://support.google.com/maps/answer/7101463?co=GENIE.Platform%3DDesktop&hl=es (consulta: 5 de septiembre de 2026).
