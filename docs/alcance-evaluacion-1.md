# 1. Alcance de SoundShop CL para la Evaluación 1

## 1.1 Caso y necesidad abordada

SoundShop CL desarrolla la alternativa de tienda del caso semestral Music Pro: una vitrina digital de productos musicales. La primera entrega reúne información de productos, categorías, precios y disponibilidad en una navegación común. El catálogo permite explorar y comparar equipos; una ficha administrativa permite revisar entradas y resultados antes de una futura publicación. No corresponde al proyecto de tarjetas digitales BeatPay.

El alcance se limita a la Evaluación 1. El caso completo describe procesos comerciales que se desarrollan en etapas posteriores; esta entrega utiliza Django, plantillas HTML, datos JSON y formularios sin conexión a una base de datos. La aprobación del alcance por el docente debe confirmarse personalmente: este documento no acredita una autorización que no consta en el repositorio.

## 1.2 Funciones incluidas

| Área | Alcance de esta entrega |
|---|---|
| Vitrina | Inicio, diez productos, cinco categorías, búsqueda, filtros y detalle |
| Presentación | Nosotros y ubicación propuesta en Las Condes; no se anuncia un local confirmado |
| Cuenta | Crear cuenta e iniciar sesión con validación; almacenamiento temporal en memoria |
| Carrito | Agregar, actualizar y eliminar como invitado, con límites de stock |
| Pedido | Solicitar cuenta al confirmar; conservar selección al ingresar y generar un comprobante temporal |
| Gestión | Cargar una ficha del JSON, validar siete campos, mostrar errores o resultado calculado |
| Interfaz | HTML semántico, DTL, Tailwind compilado, CSS propio, JavaScript y variantes responsive |
| Evidencia | Diagrama en Excalidraw, selección de pantallas, trazabilidad, pruebas y documentación |

## 1.3 Límites explícitos

La gestión no guarda cambios en el JSON ni publica productos. Las cuentas desaparecen al reiniciar el proceso del servidor; la cookie de sesión es firmada, no cifrada, y no contiene la contraseña. El pedido no realiza cobros, reservas comerciales ni descuentos persistentes de inventario. La ficha de gestión es una pantalla de validación local, no un panel de administración protegido por roles.

La primera entrega no implementa ORM, modelo entidad-relación, pasarela de pago, facturación, despacho, integración de proveedores ni recuperación de contraseñas. Estas funciones no deben presentarse como terminadas. La configuración local tampoco debe publicarse como un servicio comercial sin una revisión de seguridad.

## 1.4 Entregables y revisión

El [diagrama y su correspondencia con el código](arquitectura-y-flujo.md), los [mockups y pantallas seleccionadas](mockups-prototipo.md) y la implementación forman los entregables principales. La [investigación de referentes](investigacion-referentes.md) documenta una revisión realizada el 6 de septiembre de 2026, sin atribuirle una fecha anterior al desarrollo. La [auditoría](auditoria-rubrica.md) distingue evidencia técnica, publicación y actividades que requieren la participación del estudiante. La [preparación de entrega](preparacion-entrega.md) precisa la confirmación del alcance, la ejecución en otro computador y la exposición pendientes de acreditar.
