# 4. Guion de demostración de SoundShop CL

## 4.1 Preparación local

Desde la carpeta del proyecto, ejecutar `python manage.py check`, `python manage.py test` y `python manage.py runserver` con el entorno virtual activo. Abrir `http://127.0.0.1:8000/`. La demostración utiliza datos ficticios y no realiza cobros. Si se reinicia el servidor, se debe crear nuevamente la cuenta temporal; para repetir la prueba puede utilizarse un correo de ejemplo diferente.

## 4.2 Recorrido propuesto

| Paso | Acción | Resultado que debe mostrarse |
|---|---|---|
| 1 | Presentar la alternativa tienda del caso Music Pro | Alcance E1: vitrina, formularios y Django sin base de datos |
| 2 | Abrir el enlace Excalidraw del README | Recorrido del cliente y validación administrativa; pocas decisiones |
| 3 | Mostrar Inicio, Categorías y una ficha | Navegación coherente, contenido musical y vistas dinámicas |
| 4 | Buscar un producto y combinar categoría, precio y disponibilidad | Resultados filtrados; explicar GET y validación |
| 5 | Sin sesión, agregar un producto y cambiar su cantidad | Carrito funcional; subtotales y total actualizados |
| 6 | Intentar confirmar sin sesión | Solicitud de ingreso o creación de cuenta, sin perder el carrito |
| 7 | Probar un registro inválido y corregirlo | Mensajes por campo; acceso y posterior confirmación temporal |
| 8 | Abrir `/gestion/productos/` y seleccionar una ficha | Datos iniciales procedentes del JSON |
| 9 | Enviar precio negativo, stock negativo o descripción breve | Errores visibles y ausencia de resultado válido |
| 10 | Corregir con precio 100000, stock 3 y estado Activo | Valor de existencias $300.000 y estado Disponible |
| 11 | Cambiar stock a 0; después seleccionar Inactivo | Diferenciar Agotado e Inactivo; el JSON no cambia |
| 12 | Mostrar modo oscuro y vista móvil | Menú usable, formularios legibles y mismo contenido |
| 13 | Mostrar código, pruebas y repositorio público final | Relación entre diagrama, solicitudes, validación y plantillas |

## 4.3 Explicación técnica que debe poder sostenerse

La ruta identifica una vista por nombre y parámetros. La vista obtiene objetos del JSON y usa un formulario para limpiar entradas. Un GET muestra datos; un POST permite procesar operaciones. `is_valid()` decide si se muestran errores o se utiliza `cleaned_data`. El contexto entrega variables a la plantilla; los ciclos repiten productos y campos, mientras las condiciones controlan mensajes y estados.

La ficha administrativa usa la multiplicación de precio por stock, sin escribir en el archivo original. Los tipos están declarados en dataclasses, no en modelos ORM. El filtro de precio formatea CLP para presentación. El token CSRF protege las operaciones de formulario y no debe confundirse con una contraseña. La cookie firmada permite detectar modificaciones, pero no cifra su contenido.

## 4.4 Comprobaciones de cierre

El estudiante debe poder explicar una prueba que rechaza entradas inválidas y otra que valida un resultado correcto, identificar dónde se incluyen las rutas y mostrar cómo una variable llega al HTML. El apoyo de IA está descrito en su registro, sin atribuir al estudiante una revisión oral que todavía no se realiza. La exposición debe aclarar que no hay cobros ni persistencia comercial y que la dirección física corresponde a un sector propuesto, no a una sucursal existente.
