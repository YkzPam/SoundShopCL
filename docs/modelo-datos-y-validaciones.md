# 2. Modelo de datos, operaciones y validaciones

## 2.1 Entidades del prototipo

Las entidades se declaran como `dataclasses` inmutables en `core/models.py`. Esta decisión permite trabajar con tipos explícitos sin crear tablas durante la primera evaluación.

### 2.1.1 Categoría

| Atributo | Tipo | Uso |
|---|---|---|
| `slug` | `str` | Identificador legible utilizado en la URL |
| `nombre` | `str` | Nombre visible de la categoría |
| `descripcion` | `str` | Texto explicativo mostrado en la interfaz |
| `icono` | `str` | Clave que selecciona el símbolo visual |

### 2.1.2 Producto

| Atributo | Tipo | Uso |
|---|---|---|
| `id` | `int` | Identificador utilizado en rutas y carrito |
| `nombre` | `str` | Nombre comercial ficticio |
| `marca` | `str` | Marca ficticia del producto |
| `categoria` | `str` | Relación lógica con `Categoria.slug` |
| `descripcion` | `str` | Resumen mostrado en tarjeta y ficha |
| `precio` | `int` | Precio completo expresado en pesos chilenos |
| `stock` | `int` | Cantidad disponible para validar la compra |
| `imagen` | `str` | Ruta relativa dentro de archivos estáticos |
| `destacado` | `bool` | Controla su aparición en la portada |
| `etiquetas` | `tuple[str, ...]` | Términos adicionales para la búsqueda |
| `especificaciones` | `dict[str, str]` | Pares técnicos mostrados mediante un ciclo DTL |

La propiedad calculada `puede_comprarse` devuelve `True` cuando el stock es mayor que cero. No se repite esa comparación en todas las vistas.

## 2.2 Entradas procesadas

| Formulario u operación | Entrada | Validación aplicada | Salida |
|---|---|---|---|
| Búsqueda | `q` | Texto opcional, máximo 80 caracteres | Productos cuyo nombre, marca, descripción, etiqueta o especificación coincide |
| Categoría | `categoria` | Elección limitada a los slugs del JSON | Productos asociados a la categoría válida |
| Precio máximo | `precio_maximo` | Entero entre 1 y 2.000.000 | Productos con precio igual o inferior |
| Disponibilidad | `solo_disponibles` | Valor booleano del formulario | Exclusión de productos con stock cero |
| Orden | `orden` | Una alternativa de la lista definida | Resultado por destacados, nombre o precio |
| Agregar | `cantidad` | Entero desde 1 hasta el stock del producto | Nueva línea o incremento del carrito |
| Actualizar | `cantidad` | Entero entre 0 y 99, con segunda revisión de stock | Cantidad modificada; cero elimina la línea |
| Confirmar | Carrito firmado | Debe contener al menos una línea válida | Código, fecha, total y cantidad del pedido temporal |
| Crear cuenta | `nombre`, `correo`, `contrasena`, `confirmar_contrasena`, `acepta_terminos` | Nombre mínimo de 2 caracteres, correo válido, clave mínima de 8 caracteres con letra y número, coincidencia y aceptación obligatoria | Nombre visible guardado en la sesión; correo y contraseña descartados |

## 2.3 Salidas del servidor

Las vistas construyen diccionarios de contexto con productos, categorías, cantidades, subtotales y totales. Django renderiza esas variables con `{{ variable }}`. Los ciclos generan tarjetas y especificaciones; las condiciones cambian los estados de stock, mensajes, carrito vacío y confirmación. Los precios se presentan con el filtro propio `precio_clp`, que transforma `89990` en `$89.990` sin alterar el valor numérico original.

## 2.4 Casos inválidos controlados

- Un identificador de producto desconocido redirige al catálogo y muestra una advertencia.
- Una categoría desconocida redirige al listado de categorías.
- Un producto con stock cero no puede agregarse.
- Una cantidad superior al stock conserva intacto el carrito.
- Las operaciones de agregar, actualizar, eliminar y confirmar rechazan solicitudes `GET`.
- Un carrito vacío no puede generar una confirmación.
- Una contraseña sin letra o número se rechaza junto al campo correspondiente.
- La confirmación debe coincidir con la contraseña y las condiciones deben aceptarse.
- La pantalla de cuenta creada no se muestra si no existe un nombre de sesión válido.
