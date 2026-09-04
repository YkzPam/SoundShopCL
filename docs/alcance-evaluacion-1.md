# 1. Alcance técnico de la Evaluación 1

## 1.1 Caso seleccionado

SoundShop CL desarrolla la alternativa **Sistema de Sucursal (Punto de Venta / Vitrina)**. El resultado es una tienda web de productos musicales con una portada comercial, categorías, catálogo, búsqueda, fichas detalladas, validación de stock, carrito y confirmación de pedido. No corresponde a una tarjeta de pago, billetera digital ni servicio financiero.

## 1.2 Límite funcional de esta unidad

La pauta de la Evaluación 1 solicita un sitio básico en Django sin conexión a base de datos. El catálogo se almacena en `core/data/catalogo.json`; la vista lo transforma en objetos Python y construye el contexto que recibe cada plantilla. El carrito y el nombre visible de la cuenta utilizan una cookie firmada y permiten comprobar ambos flujos sin crear tablas.

| Incluido en esta entrega | Reservado para unidades posteriores |
|---|---|
| Catálogo JSON dinámico | Modelos ORM y migraciones de negocio |
| Búsqueda, filtros y categorías | Administración persistente de productos |
| Formularios de cantidad y creación de cuenta | Usuarios ORM, inicio de sesión y recuperación de contraseña |
| Carrito temporal firmado | Historial real de compras por usuario |
| Pedido simulado | Pasarela o medio de pago real |
| Mensajes y control de rutas | Gestión persistente del estado del pedido |

## 1.3 Criterio de seguridad

El formulario de cuenta solicita nombre, correo y contraseña para comprobar la interfaz y sus reglas. Django valida esos valores y descarta el correo y la contraseña al terminar la solicitud; la sesión conserva solo el primer nombre. Las rutas de registro, carrito, confirmación y cierre usan método `POST` y token CSRF. Ningún pedido se registra fuera de la sesión temporal del navegador.

## 1.4 Resultado observable

Una persona puede entrar a la portada, crear una cuenta de sesión, ver su nombre en el menú, elegir una categoría, filtrar el catálogo, abrir un producto disponible, agregar una cantidad válida, modificarla en el carrito y confirmar el pedido. Las credenciales inválidas, cantidades fuera de rango, productos agotados e identificadores inexistentes generan mensajes o redirecciones controladas.
