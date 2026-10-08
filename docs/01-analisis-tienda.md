# 1. Análisis del caso de tienda musical

## 1.1 Necesidad y alcance de la propuesta

SoundShop CL representa una tienda que necesita presentar su catálogo musical de forma ordenada y permitir la consulta de precios y disponibilidad. La administración requiere revisar los productos y usuarios del caso sin depender de una interfaz recargada. El desarrollo de la Evaluación 1 utiliza datos ficticios para mostrar esos recorridos y validar formularios; no establece que exista una empresa operativa, entrevistas a clientes ni resultados de ventas reales.

El visitante consulta productos, categorías y fichas, selecciona equipos y revisa un carrito temporal. El cliente de ejemplo confirma la selección sin pagar. El administrador de ejemplo revisa productos y usuarios, completa sus formularios y visualiza la salida de la validación. El registro no almacena una cuenta; la implementación persistente corresponde a una etapa posterior.

## 1.2 Referentes de tiendas musicales

La revisión de Audiomusica identifica una búsqueda de productos, un acceso a cuenta y secciones comerciales del catálogo. La página de Thomann organiza sus productos en categorías que incluyen guitarras, grabación, micrófonos y equipos de sonido. Esas observaciones sirven para seleccionar navegación y contenidos propios de una tienda musical; no justifican incorporar todas las funciones comerciales de esos sitios (Audiomusica, s. f.; Thomann, s. f.).

| Referente consultado el 8 de octubre de 2026 | Elemento observado | Adaptación en SoundShop CL |
| --- | --- | --- |
| Audiomusica | Búsqueda y acceso a cuenta | Catálogo con búsqueda simple e inicio de sesión de ejemplo |
| Thomann | Categorías de instrumentos y audio | Cinco categorías, con descripción y acceso al catálogo filtrado |

La propuesta de negocio es vender instrumentos, equipos de audio y accesorios mediante un catálogo digital. Un producto presenta nombre, marca, descripción, precio y stock. En esta entrega esos atributos se representan con JSON; no existe un modelo comercial validado ni conexión a un proveedor, bodega o sistema de pagos.

## 1.3 Adaptación del ejemplo del docente

La corrección ilustra un sistema de tarjetas. Se toma su método de trabajo y la separación entre cliente y administrador, pero no sus operaciones financieras. El área del cliente se adapta al catálogo y carrito; el mantenimiento administrativo se adapta a productos y usuarios. Las fases 1 y 3 incluyen diseño e integración inicial en Django, mientras que la fase de persistencia queda fuera de esta entrega (Mora, 2026, pp. 6–7).

## REFERENCIAS

Audiomusica. (s. f.). *Tienda online*. Recuperado el 8 de octubre de 2026, de https://www.audiomusica.com/

Mora, B. (2026). *E1 Corrección Evaluación: Caso semestral, Unidad 1 Backend* [Material docente proporcionado por el estudiante, pp. 6–7]. INACAP. El archivo fuente fue entregado localmente; no se atribuye una URL pública.

Thomann. (s. f.). *Buy musical instruments online*. Recuperado el 8 de octubre de 2026, de https://www.thomannmusic.com/
