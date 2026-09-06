# 1. Identidad visual y alcance del rediseño

SoundShop CL adopta una composición editorial centrada en fotografía, tipografía amplia y espacios abiertos. La actualización comprende el encabezado, navegación, inicio, catálogo, cinco colecciones, directorio de categorías, Nosotros, acceso, registro, cuenta activa, fichas, carrito, confirmación y gestión de productos. El cambio se concentra en plantillas, CSS y JavaScript. No incorpora base de datos, pagos, credenciales persistentes ni publicación comercial.

## 1.1 Sistema de color y tipografía

El fondo claro usa marfil `#F4F0E8` con texto `#121212`, superficies próximas al blanco y líneas cálidas. El tema oscuro usa `#121212` con texto `#F8F6F2`, superficies `#1b1b1a` y `#242320`, y divisores `#3e3b37`. El dorado `#B89B5E` aparece en el símbolo de surcos, metadatos, flechas y pequeños detalles. El violeta `#4B2E5A` identifica acciones y secciones; las variantes `#c6acd1` y `#302437` conservan su función sobre el fondo oscuro sin limitarse a invertir los colores.

La tipografía utiliza Segoe UI Variable con alternativas locales Segoe UI y Arial. Los títulos combinan pesos ligeros y medios; Georgia introduce énfasis en colecciones y Nosotros. Consolas organiza índices y datos secundarios. No se descargan fuentes externas. `static/css/identity.css` contiene el sistema visual común y se carga después de Tailwind compilado. Las hojas anteriores se conservan, pero no participan en el render actual.

## 1.2 Composición y navegación adaptable

El inicio separa el título «Escucha distinto.» de la fotografía principal de Astra Seven. Las categorías distribuyen imágenes y texto en dos columnas escalonadas y una última composición horizontal. En teléfono, cada fotografía mantiene su espacio y la ficha aparece después. El catálogo presenta los equipos sin cajas perimetrales y mantiene filtros laterales en escritorio, convertidos en un desplegable en pantallas menores. Cada colección conserva su título, fotografía y guía de selección.

El encabezado reúne la navegación en una fila en escritorio. En pantallas de hasta 860 píxeles, los cuatro enlaces principales ocupan una línea compacta dentro del mismo encabezado y permanecen visibles. El buscador de escritorio se abre bajo un control compacto y se cierra con Escape o al pulsar fuera. El menú complementario contiene búsqueda, acceso de cuenta y ubicación; bloquea el scroll del fondo y mantiene el foco dentro del encabezado y del menú. Su posición se adapta a la altura real del encabezado. Nosotros mantiene su ruta independiente.

Cuenta presenta «Backstage.» como título central, pestañas de inicio de sesión y creación de cuenta, y campos integrados sobre el fondo. La composición no utiliza una fotografía lateral ni una caja grande de formulario. Los mensajes de error conservan los datos permitidos y distinguen el campo afectado. Los formularios mantienen sus destinos POST, protección CSRF y validación del servidor. Gestión reutiliza los mismos campos y colores, sin convertir la vista previa existente en un editor persistente.

## 1.3 Movimiento y controles de interacción

Las secciones aparecen una vez al entrar en el área visible mediante opacidad y desplazamiento breve. Las fotografías se acercan suavemente al pasar el puntero; la portada limita su desplazamiento a 14 píxeles y la ficha admite una inclinación discreta. Los botones, enlaces, vistas rápidas y paneles incorporan respuestas breves, sin ciclos decorativos continuos. La preferencia `prefers-reduced-motion` tiene prioridad y el pie de página permite reducir el movimiento de forma manual. La lectura y los formularios siguen disponibles sin JavaScript.

## 1.4 Comprobación de interfaz y funcionamiento

La revisión automatizada comprobó 14 rutas en cinco anchos —320, 390, 768, 1024 y 1440 píxeles— y ambos temas. Las 140 combinaciones respondieron con HTTP 200, un encabezado principal, el fondo correspondiente al tema y sin desbordamiento horizontal del documento. Las imágenes verificadas no presentaron fallos de carga. Las galerías horizontales de navegación se desplazan dentro de su contenedor y no ensanchan la página. La revisión no sustituye una auditoría completa de accesibilidad ni pruebas en dispositivos físicos.

Las pruebas originales de interacción cubrieron búsqueda, persistencia de tema, menú móvil, ciclo de foco, cierre con Escape, navegación a Nosotros, movimiento y reducción manual. El acceso rechazó una contraseña incorrecta y aceptó la cuenta recién creada; Gestión conservó los errores, restableció datos y calculó una ficha válida sin publicarla. La actualización del carrito de invitado sustituye el antiguo bloqueo antes de agregar: ahora la sesión se solicita solo al continuar con el pedido. La verificación más reciente se detalla en `carrito-invitado-y-ubicacion.md`; las capturas anteriores conservan valor histórico y no describen necesariamente el flujo vigente.

En la revisión original del rediseño, las 44 pruebas de Django terminaron correctamente sin acceso a base de datos. Las expectativas visuales se actualizaron para comprobar la ausencia de la segunda navegación y los títulos nuevos, manteniendo las comprobaciones funcionales existentes. Las capturas `identity-*` en `docs/evidencias/` documentan la versión; las series anteriores permanecen como historial. Las cuentas y los pedidos continúan siendo temporales. El rediseño no equivale a una validación completa de la rúbrica ni a una publicación en GitHub.


La selección final de capturas y la verificación vigente se encuentran en [Prototipo de interfaz](mockups-prototipo.md) y [Verificación de entrega](verificacion-entrega.md). Las cifras anteriores describen la revisión histórica del rediseño.
