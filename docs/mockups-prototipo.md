# 6. Mockups y evidencia del prototipo de interfaz

## 6.1 Criterio de presentación

Los mockups corresponden a capturas del prototipo navegable, no a pantallas dibujadas sin implementación. Cada imagen proviene de la misma aplicación Django entregada en el repositorio y muestra el HTML semántico procesado con plantillas DTL y Tailwind CSS. La dirección visual toma referencias de catálogos técnicos de audio: azul noche, cobalto, gris frío, acentos aqua, tipografía Bahnschrift/Aptos y fotografías de estudio con fondo neutro. La portada utiliza un hero de primera pantalla, tipografía XXL y una cuadrícula Bento para las categorías. La interfaz pública no muestra etiquetas de evaluación ni mensajes que la presenten como una maqueta.

## 6.2 Portada en escritorio

La vista de escritorio presenta la identidad SoundShop CL, navegación principal, buscador, selector de tema, acceso a cuenta y carrito. La primera pantalla divide la propuesta de la tienda y el producto seleccionado; al continuar aparecen la cuadrícula de categorías, los productos destacados y el formulario de registro.

![Portada de SoundShop CL en escritorio](evidencias/portada-escritorio.png)

## 6.3 Portada en modo oscuro

El modo oscuro es una variante nativa de toda la interfaz, no un filtro aplicado a la captura. Cambia superficies, texto, líneas, formularios, tarjetas y controles mediante variables CSS. La selección queda guardada en `localStorage` y se conserva al recargar o cambiar de ruta.

![Portada de SoundShop CL en modo oscuro](evidencias/portada-oscura.png)

## 6.4 Catálogo en tableta

La vista de 768 × 1024 píxeles reorganiza la navegación, convierte los filtros en un panel desplegable y mantiene dos columnas de productos. Las tarjetas muestran marca, categoría, precio, stock y acceso a la ficha.

![Catálogo de SoundShop CL en tableta](evidencias/catalogo-tableta.png)

## 6.5 Portada en teléfono

El navegador se configuró con un viewport nominal de 390 × 844 píxeles. La captura conserva la misma información y reemplaza la navegación de escritorio por un botón de menú. Los botones ocupan el ancho disponible y el contenido no genera desplazamiento horizontal.

![Portada de SoundShop CL en teléfono](evidencias/portada-movil-390.png)

La anchura mínima comprobada fue 320 píxeles. El encabezado, el texto, los botones y las estadísticas se mantienen dentro del área visible.

![Portada de SoundShop CL a 320 píxeles](evidencias/portada-movil-320.png)

## 6.6 Registro de cuenta

La ruta de registro organiza los campos en una vista propia y conserva el mismo sistema visual de la tienda. Nombre, correo, contraseña, confirmación y aceptación de condiciones poseen etiquetas visibles y errores asociados. La cuenta activa muestra el nombre en el encabezado; el correo y la contraseña no se guardan.

![Registro de cuenta en escritorio](evidencias/registro-escritorio.png)

## 6.7 Carrito y salida del proceso

El carrito representa la operación principal de entrada y cálculo. La vista muestra dos unidades, su subtotal, controles de actualización y el total del pedido. El servidor valida la cantidad antes de aceptar cualquier cambio.

![Carrito con dos productos](evidencias/carrito-escritorio.png)

La última pantalla confirma que el flujo terminó y entrega código, total y fecha. La interfaz mantiene un lenguaje comercial limpio; la limitación técnica del pedido temporal queda documentada en el alcance de la entrega.

![Pedido confirmado](evidencias/pedido-confirmado.png)

## 6.8 Comprobación responsive y movimiento

| Vista | Ancho nominal | Código HTTP | Desbordamiento horizontal | Error de JavaScript o consola |
|---|---:|---:|---|---|
| Portada escritorio | 1440 px | 200 | No | No |
| Portada oscura | 1440 px | 200 | No | No |
| Catálogo tableta | 768 px | 200 | No | No |
| Portada teléfono | 390 px | 200 | No | No |
| Portada mínima | 320 px | 200 | No | No |
| Registro | 390 px | 200 | No | No |

El flujo automatizado abrió la ficha `Pulse X ANC`, agregó dos unidades, verificó el total `$179.980`, confirmó el pedido y buscó `microfono`. La búsqueda devolvió únicamente `Vela C1`. Otra comprobación completó el registro, rechazó dos contraseñas distintas, aceptó una clave válida y verificó que `Benjamin` apareciera en el encabezado.

La interfaz incorpora una entrada inicial del hero, revelado escalonado al recorrer las secciones, barra de progreso vinculada al scroll, profundidad en la imagen principal y una respuesta breve antes de abrir la ficha seleccionada. La ficha agrega una inclinación máxima de 3,2 grados cuando existe un puntero preciso. No hay ciclos infinitos ni movimiento decorativo permanente. Con `prefers-reduced-motion: reduce`, JavaScript omite el observador, el paralaje y la inclinación; CSS muestra el contenido de inmediato y oculta la barra de progreso.
