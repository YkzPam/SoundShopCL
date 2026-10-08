# 2. Datos y lógica de los formularios

## 2.1 Atributos del caso tienda

Los datos se leen desde `core/data/catalogo.json` y `core/data/usuarios.json` mediante `json.load()`. Python recibe listas y diccionarios; las vistas los entregan a las plantillas mediante un diccionario de contexto. El archivo `models.py` no contiene modelos ORM y la configuración no conecta una base de datos.

| Entidad | Atributos | Tipos en Python | Utilización |
| --- | --- | --- | --- |
| Categoría | slug, nombre, descripcion | str | Filtrar y describir el catálogo |
| Producto | id | int | Identificar una ficha en la ruta |
| Producto | nombre, marca, categoria, descripcion, imagen | str | Mostrar información y ruta del recurso local |
| Producto | precio, stock | int | Precio en pesos enteros y cantidad disponible |
| Usuario de prueba | id | int | Identificar el acceso de cliente |
| Usuario de prueba | nombre, correo, rol, clave_demo | str | Recorrer el área de cliente con datos públicos |
| Usuario de prueba | activo | bool | Permitir o rechazar el acceso de cliente |
| Administrador | verificadores de usuario y contraseña | str | Validar el acceso privado sin publicar credenciales legibles |
| Carrito temporal | claves de producto y cantidades | dict[str, int] | Calcular subtotales sin guardar un pedido |

El catálogo inicial contiene diez productos y cinco categorías. El JSON conserva un cliente de prueba; el administrador se comprueba con verificadores de Django incluidos en la configuración. La contraseña administrativa no se publica. La clave del cliente es pública y no representa una cuenta personal.

## 2.2 Entradas, validaciones y salidas

| Formulario | Entrada y tipo | Validación del servidor | Salida |
| --- | --- | --- | --- |
| Acceso | correo str; clave str | Correo válido, campos obligatorios; cliente activo en JSON o administrador con verificadores | Error o redirección según rol |
| Registro | nombre, correo, clave, confirmar str | Nombre de 3–80 caracteres; correo válido no duplicado; clave de 8–60 caracteres; confirmación coincidente | Nombre y correo validados, sin guardar cuenta ni mostrar contraseña |
| Producto administrativo | nombre, marca, categoria, descripcion str; precio y stock int | Nombre 3–80; marca obligatoria hasta 60; categoría existente; descripción 10–500; precio 1–10.000.000; stock 0–999 | Errores por campo o vista previa con precio y disponibilidad |
| Usuario administrativo | nombre, correo y rol str; activo bool | Nombre 3–80; correo válido no duplicado; rol dentro de las opciones | Errores o vista previa de nombre, correo, rol y estado |

La petición GET presenta el formulario. POST entrega la entrada a `forms.Form`; `is_valid()` decide si corresponde mostrar errores o utilizar `cleaned_data`. `messages.success()` comunica una validación correcta. Ninguna validación administrativa modifica los archivos JSON.

## 2.3 Operaciones y decisiones de la tienda

El catálogo recorre los productos con `for` y usa condiciones para comparar texto y categoría. La ficha compara `stock > 0` para habilitar la selección. El carrito suma una unidad únicamente si no supera el stock; el subtotal corresponde a `cantidad * precio` y el total suma los subtotales. La confirmación exige una sesión iniciada y un carrito no vacío. El ingreso correcto bifurca hacia cliente o administración según `rol`; un ingreso incorrecto permanece en el formulario.

Las plantillas presentan listas con `{% for %}`, estados con `{% if %}` y filtros como `floatformat`, `capfirst`, `length` y `pluralize`. Las rutas HTML usan `{% url %}` y las imágenes, estilos y scripts utilizan `{% static %}`. Los formularios POST incluyen `{% csrf_token %}`.
