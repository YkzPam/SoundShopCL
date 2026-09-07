# Preparación de la entrega de Evaluación 1

## 1. Material para presentar al docente

SoundShop CL corresponde a la alternativa tienda del caso Music Pro. El repositorio contiene el prototipo Django, el diagrama de navegación, una lámina de mockups esquemáticos y capturas de la interfaz implementada. Los bocetos documentan el diseño actual; no acreditan haber sido elaborados antes de programar.

El alcance propuesto comprende catálogo con búsqueda y filtros, categorías, fichas, carrito de invitado, cuenta temporal, confirmación de pedido y validación administrativa de productos. No incluye cobros reales, publicación persistente de productos, integración de bodega ni base de datos. La ficha administrativa procesa entradas, valida y muestra resultados; no es un CRUD persistente ni un panel protegido por roles.

## 2. Condiciones que requieren participación del estudiante

- Confirmar con el docente que este alcance de tienda y validación administrativa es el aceptado para E1. Registrar la respuesta real y su fecha cuando exista; no anticipar una aprobación.
- Presentar la investigación de referentes como revisión complementaria realizada después de la implementación. No atribuirle una fecha anterior.
- Comprobar la ejecución en el computador de la presentación antes de la evaluación.
- Explicar el código y realizar la demostración siguiendo el [guion](guion-demostracion.md).
- Entregar el enlace del repositorio por el medio y dentro del plazo indicados por el docente. La publicación en GitHub no sustituye una entrega en la plataforma de la asignatura.

## 3. Comprobación en otro computador

Instalar Python compatible con las dependencias y Git. Desde una terminal, seguir la sección de clonación e instalación del [README](../README.md). No copiar un entorno virtual de Windows entre computadores: crear uno nuevo e instalar `requirements.txt`. Tailwind ya está compilado; Node no es necesario para ejecutar la versión entregada.

Ejecutar `manage.py check` y `manage.py test` con el intérprete del entorno antes de `manage.py runserver`. Revisar Inicio, una búsqueda, una ficha y Gestión. Crear una cuenta de prueba nueva: las cuentas anteriores no viajan con GitHub y desaparecen al reiniciar el proceso. No introducir información personal ni financiera real.

## 4. Criterio de cierre

La disponibilidad de los archivos y las pruebas no demuestra por sí sola aprobación del alcance, cumplimiento del orden temporal de investigación ni comprensión del estudiante. La rúbrica permite hasta 100 puntos; la asignación corresponde al docente y no se declara como obtenida.
