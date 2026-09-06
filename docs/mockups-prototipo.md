# 7. Prototipo de interfaz y selección de evidencias

## 7.1 Criterio de entrega

La aplicación navegable constituye el prototipo implementado de la Evaluación 1. Las capturas permiten revisar sus vistas sin iniciar Django; no se presentan como bocetos anteriores al desarrollo. La selección `final-*` corresponde a la revisión de entrega del 6 de septiembre de 2026. Las series anteriores se conservan como historial y no deben mezclarse para interpretar el flujo vigente.

## 7.2 Vistas principales

| Vista | Ruta | Escritorio claro | Móvil claro |
|---|---|---|---|
| Inicio | `/` | [1440 px](evidencias/final-inicio-light-1440.png) | [390 px](evidencias/final-inicio-light-390.png) |
| Productos | `/productos/` | [1440 px](evidencias/final-catalogo-light-1440.png) | [390 px](evidencias/final-catalogo-light-390.png) |
| Categorías | `/categorias/` | [1440 px](evidencias/final-categorias-light-1440.png) | [390 px](evidencias/final-categorias-light-390.png) |
| Ficha de producto | `/productos/1/` | [1440 px](evidencias/final-producto-light-1440.png) | [390 px](evidencias/final-producto-light-390.png) |
| Nosotros | `/nosotros/` | [1440 px](evidencias/final-nosotros-light-1440.png) | [390 px](evidencias/final-nosotros-light-390.png) |
| Iniciar sesión | `/registro/` | [1440 px](evidencias/final-cuenta-light-1440.png) | [390 px](evidencias/final-cuenta-light-390.png) |
| Crear cuenta | `/registro/?modo=crear` | [1440 px](evidencias/final-crear-light-1440.png) | [390 px](evidencias/final-crear-light-390.png) |
| Carrito vacío | `/carrito/` | [1440 px](evidencias/final-carrito-light-1440.png) | [390 px](evidencias/final-carrito-light-390.png) |
| Gestión de ficha | `/gestion/productos/` | [1440 px](evidencias/final-gestion-light-1440.png) | [390 px](evidencias/final-gestion-light-390.png) |

Cada vista dispone de una variante oscura en la misma carpeta, cambiando `light` por `dark` en el nombre. Por ejemplo, [Inicio oscuro](evidencias/final-inicio-dark-1440.png), [Cuenta oscura móvil](evidencias/final-cuenta-dark-390.png) y [Gestión oscura](evidencias/final-gestion-dark-1440.png). La revisión también comprueba un ancho intermedio de 768 px.

## 7.3 Estados funcionales complementarios

Se conservan como evidencia de interacciones previamente capturadas la [ficha con errores](evidencias/identity-gestion-error.png), la [ficha validada](evidencias/identity-gestion-validada.png), el [carrito con productos](evidencias/identity-carrito-lleno-light-1440.png), los [errores de registro](evidencias/identity-registro-errores.png) y el [pedido confirmado](evidencias/identity-pedido-confirmado.png). Estas imágenes no son nuevas capturas de la revisión final; los comportamientos actuales se contrastan con la suite de Django.

## 7.4 Correspondencia visual y navegación

La estructura comparte marca, tipografía, navegación, Cuenta y carrito. Negro y marfil forman las superficies principales; dorado y violeta se reservan para acentos y estados. Inicio conduce al catálogo y a categorías; una ficha conduce al carrito; Cuenta interviene al confirmar. La gestión presenta ingreso, errores y resultado en una misma vista, tal como explica [Arquitectura y flujo](arquitectura-y-flujo.md).

El menú móvil mantiene los destinos principales sin depender de una navegación de escritorio desbordada. Los formularios incluyen etiquetas y mensajes, y el movimiento respeta la preferencia de reducción del sistema. Las capturas no acreditan por sí solas accesibilidad completa ni pruebas en teléfonos físicos; su alcance se precisa en [Verificación de entrega](verificacion-entrega.md).
