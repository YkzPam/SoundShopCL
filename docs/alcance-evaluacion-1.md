# 1. Alcance técnico de la Evaluación 1

## 1.1 Caso seleccionado

SoundShop CL desarrolla la alternativa **Sistema de Sucursal (Punto de Venta / Vitrina)**. El resultado es una tienda web con diez productos distribuidos en cinco categorías: audífonos, tornamesas y vinilos, estudio y creación, instrumentos y sonido en vivo. Incluye portada comercial, búsqueda, fichas detalladas, validación de stock, sesión obligatoria para comprar, carrito y confirmación de pedido. No corresponde a una tarjeta de pago, billetera digital ni servicio financiero.

## 1.2 Límite funcional de esta unidad

La pauta de la Evaluación 1 solicita un sitio básico en Django sin conexión a base de datos. El catálogo se almacena en `core/data/catalogo.json`; la vista lo transforma en objetos Python y construye el contexto que recibe cada plantilla. El carrito y el nombre visible de la cuenta utilizan una cookie firmada y permiten comprobar ambos flujos sin crear tablas.

| Incluido en esta entrega | Reservado para unidades posteriores |
|---|---|
| Catálogo JSON dinámico | Modelos ORM y migraciones de negocio |
| Búsqueda, filtros y categorías | Administración persistente de productos |
| Formularios de cantidad y creación de cuenta de sesión | Usuarios ORM, reingreso con credenciales y recuperación de contraseña |
| Bloqueo de agregado y confirmación sin sesión activa | Autenticación persistente asociada a una cuenta real |
| Carrito temporal firmado | Historial real de compras por usuario |
| Pedido simulado | Pasarela o medio de pago real |
| Mensajes y control de rutas | Gestión persistente del estado del pedido |

## 1.3 Criterio de seguridad

El formulario de cuenta solicita nombre, correo y contraseña para comprobar la interfaz y sus reglas. Django valida esos valores y descarta el correo y la contraseña al terminar la solicitud; la sesión conserva solo el primer nombre. Las operaciones que cambian el carrito, confirman el pedido o cierran la sesión usan `POST` y token CSRF. El servidor rechaza el agregado y la confirmación cuando no existe una sesión activa. La ruta de retorno del acceso se valida para aceptar únicamente destinos locales. Ningún pedido se registra fuera de la sesión temporal del navegador.

## 1.4 Resultado observable

Una persona puede entrar a la portada, recorrer las cinco categorías, filtrar el catálogo y abrir la vista rápida o una ficha sin registrarse. Al intentar comprar, la interfaz solicita una cuenta de sesión. Después del registro vuelve al producto, muestra el nombre en el menú, permite agregar una cantidad válida, revisar el mini carrito, modificar la selección y confirmar el pedido. Las credenciales inválidas, la ausencia de sesión, las cantidades fuera de rango, los productos agotados y los identificadores inexistentes generan mensajes o redirecciones controladas.
