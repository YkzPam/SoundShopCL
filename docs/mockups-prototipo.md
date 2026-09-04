# 6. Mockups y evidencia del prototipo de interfaz

## 6.1 Criterio de presentación

Los mockups corresponden a capturas del prototipo navegable, no a pantallas dibujadas sin implementación. Cada imagen proviene de la misma aplicación Django entregada en el repositorio y muestra el HTML semántico procesado con plantillas DTL y Tailwind CSS. La dirección visual toma referencias de catálogos especializados en audio: fondo papel, negro carbón, rojo señal, bordes rectos y fotografías de producto como elemento principal. Se eliminaron los degradados decorativos, las transparencias y los movimientos continuos para obtener una presentación más sobria.

## 6.2 Portada en escritorio

La vista de escritorio presenta la identidad SoundShop CL, navegación principal, buscador, acceso al carrito y una portada editorial dividida entre la propuesta de la tienda y el producto seleccionado. La jerarquía permite identificar las acciones principales sin desplazar primero un bloque publicitario ajeno al catálogo.

![Portada de SoundShop CL en escritorio](evidencias/portada-escritorio.png)

## 6.3 Catálogo en tableta

La vista de 768 × 1024 píxeles reorganiza la navegación, convierte los filtros en un panel desplegable y mantiene dos columnas de productos. Las tarjetas muestran marca, categoría, precio, stock y acceso a la ficha.

![Catálogo de SoundShop CL en tableta](evidencias/catalogo-tableta.png)

## 6.4 Portada en teléfono

El navegador se configuró con un viewport nominal de 390 × 844 píxeles. La captura conserva la misma información y reemplaza la navegación de escritorio por un botón de menú. Los botones ocupan el ancho disponible y el contenido no genera desplazamiento horizontal.

![Portada de SoundShop CL en teléfono](evidencias/portada-movil-390.png)

La anchura mínima comprobada fue 320 píxeles. El encabezado, el texto, los botones y las estadísticas se mantienen dentro del área visible.

![Portada de SoundShop CL a 320 píxeles](evidencias/portada-movil-320.png)

## 6.5 Carrito y salida del proceso

El carrito representa la operación principal de entrada y cálculo. La vista muestra dos unidades, su subtotal, controles de actualización y el total del pedido. El servidor valida la cantidad antes de aceptar cualquier cambio.

![Carrito con dos productos](evidencias/carrito-escritorio.png)

La última pantalla confirma que el flujo terminó y entrega código, total y fecha. El texto declara que el proceso es simulado y que no utiliza pago ni base de datos.

![Pedido simulado confirmado](evidencias/pedido-confirmado.png)

## 6.6 Comprobación responsive y movimiento

| Vista | Ancho nominal | Código HTTP | Desbordamiento horizontal | Error de JavaScript o consola |
|---|---:|---:|---|---|
| Portada escritorio | 1440 px | 200 | No | No |
| Catálogo tableta | 768 px | 200 | No | No |
| Portada teléfono | 390 px | 200 | No | No |
| Portada mínima | 320 px | 200 | No | No |

El flujo automatizado abrió la ficha `Pulse X ANC`, agregó dos unidades, verificó el total `$179.980`, confirmó el pedido y buscó `microfono`. La búsqueda devolvió únicamente `Vela C1`, lo que comprueba la normalización de tildes y la representación dinámica del resultado.

La interfaz no utiliza animaciones automáticas ni entradas escalonadas. Solo conserva transiciones breves de color y opacidad, entre 140 y 160 milisegundos, para comunicar estados de interacción. La regla `prefers-reduced-motion` reduce esas transiciones cuando el sistema del usuario solicita menos movimiento.
