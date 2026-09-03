# 1. Alcance técnico de la Evaluación 1

## 1.1 Caso seleccionado

SoundShop CL desarrolla la alternativa **Sistema de Sucursal (Punto de Venta / Vitrina)**. El resultado es una tienda web de productos musicales con una portada comercial, categorías, catálogo, búsqueda, fichas detalladas, validación de stock, carrito y confirmación de pedido. No corresponde a una tarjeta de pago, billetera digital ni servicio financiero.

## 1.2 Límite funcional de esta unidad

La pauta de la Evaluación 1 solicita un sitio básico en Django sin conexión a base de datos. El catálogo se almacena en `core/data/catalogo.json`; la vista lo transforma en objetos Python y construye el contexto que recibe cada plantilla. El carrito utiliza una cookie firmada y permite comprobar el flujo sin crear tablas ni conservar información personal.

| Incluido en esta entrega | Reservado para unidades posteriores |
|---|---|
| Catálogo JSON dinámico | Modelos ORM y migraciones de negocio |
| Búsqueda, filtros y categorías | Administración persistente de productos |
| Formulario y validación de cantidades | Registro e inicio de sesión de clientes |
| Carrito temporal firmado | Historial real de compras por usuario |
| Pedido simulado | Pasarela o medio de pago real |
| Mensajes y control de rutas | Gestión persistente del estado del pedido |

## 1.3 Criterio de seguridad

El prototipo no pide nombre, dirección, correo ni datos bancarios. Las rutas que cambian el carrito usan método `POST` y token CSRF. La confirmación genera un código solo para demostrar la salida del proceso. Ningún pedido se registra fuera de la sesión temporal del navegador.

## 1.4 Resultado observable

Una persona puede entrar a la portada, elegir una categoría, filtrar el catálogo, abrir un producto disponible, agregar una cantidad válida, modificarla en el carrito y confirmar el pedido. Las cantidades inválidas, productos agotados e identificadores inexistentes generan mensajes o redirecciones controladas.
