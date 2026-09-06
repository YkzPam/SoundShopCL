# 2. Arquitectura y correspondencia del flujo

## 2.1 Organización de la aplicación

La solicitud entra por `soundshop/urls.py`, que incluye las rutas nombradas de `core/urls.py`. La vista consulta funciones de `core/catalogo.py`, valida formularios cuando corresponde y entrega un diccionario de contexto a una plantilla DTL. Los datos iniciales proceden de `core/data/catalogo.json`; `core/models.py` describe sus tipos con dataclasses, sin tablas ni migraciones.

La plantilla `templates/base.html` comparte navegación y pie de página. Las vistas específicas y los componentes de `templates/includes/` evitan duplicar la estructura. Tailwind compilado, `static/css/identity.css` y los refinamientos cargados en la base complementan el HTML; `static/js/main.js` añade interacciones sin reemplazar la validación del servidor.

## 2.2 Diagrama simplificado

El diagrama se consulta en [Excalidraw](https://excalidraw.com/#json=1MN8Hxbolx-qeb1thQvVD,qJzWBc68wzA_RRld-BPexA). El repositorio conserva un [archivo editable](diagrama-flujo.excalidraw). Se trata de un resumen de navegación y decisiones principales, no de un diagrama de cada condición interna. Las validaciones de campos y los estados vacíos se agrupan en sus procesos para mantener una lectura simple.

## 2.3 Recorrido del cliente

El visitante explora Inicio, Productos o Categorías, abre una ficha y agrega productos al carrito sin cuenta. Puede cambiar cantidades o eliminar líneas. Al confirmar el pedido, el servidor comprueba la sesión: si no existe, solicita ingreso o registro; tras completar el acceso se conserva el carrito y el visitante vuelve para confirmar. El acceso no obliga a agregar nuevamente los productos. Una sesión válida y un carrito con contenido permiten generar el pedido temporal.

| Proceso | Ruta o código | Resultado |
|---|---|---|
| Explorar y filtrar | `/productos/`, `FiltroCatalogoForm` | Listado o mensajes de validación |
| Revisar producto | `/productos/<id>/` | Datos, especificaciones y disponibilidad |
| Agregar o editar | `agregar_al_carrito`, `actualizar_carrito`, `eliminar_del_carrito` | Carrito de invitado actualizado mediante POST |
| Revisar selección | `/carrito/` | Cantidades, subtotales y total |
| Comprobar acceso | `confirmar_pedido` | Retorno a Cuenta si falta sesión |
| Ingresar o registrar | `/registro/`, `core/cuentas.py` | Sesión local y regreso seguro |
| Confirmar | `/pedido/confirmado/` | Código y resumen temporal, sin cobro |

## 2.4 Recorrido administrativo

| Paso del flujo | Implementación | Correspondencia observable |
|---|---|---|
| Seleccionar ficha | `/gestion/productos/` y `/gestion/productos/<id>/` | Ciclo de productos y datos iniciales del JSON |
| Ingresar datos | `FichaGestionForm` en `core/forms.py` | Nombre, marca, categoría, descripción, precio, stock y estado |
| Validar datos | `request.method == 'POST'` y `formulario.is_valid()` | Decisión entre error y resultado |
| Corregir errores | `templates/core/gestion_producto.html` | Mismo formulario con valores y errores por campo |
| Mostrar resultado | `core/gestion.py` | Datos limpios, valor de existencias y disponibilidad |

Los nodos de ingreso, error y resultado representan estados de una misma pantalla, no páginas independientes. El ciclo de selección permite revisar otra ficha. La operación `precio * stock` calcula valor de existencias a precio de venta; las condiciones distinguen Inactivo, Disponible y Agotado. La validación no altera el catálogo original ni acredita permisos de administrador.

## 2.5 Reglas transversales

Las operaciones de carrito usan POST y protección CSRF. Los identificadores inválidos producen redirecciones controladas. El servidor rechaza cantidades fuera de rango y no confirma carritos vacíos. Los retornos de Cuenta solo admiten destinos locales. Estos controles se respaldan en `core/tests.py` y `core/test_gestion.py`, junto con la [matriz de validaciones](modelo-datos-y-validaciones.md).
