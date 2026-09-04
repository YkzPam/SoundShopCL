# 7. Guion breve para presentar SoundShop CL

## 7.1 Preparación en el computador

La carpeta se abre directamente en Visual Studio Code. En la terminal integrada se ejecutan estos comandos:

```powershell
.\venv\Scripts\Activate.ps1
python manage.py check
python manage.py test
python manage.py runserver
```

El primer comando activa el entorno aislado; el segundo revisa la configuración; el tercero ejecuta las treinta pruebas; el último inicia la página en `http://127.0.0.1:8000/`.

## 7.2 Recorrido sugerido

1. La portada permite explicar que SoundShop CL corresponde al sistema de sucursal y vitrina de Music Pro. Se muestran el hero, las cinco categorías, las guías editoriales y los productos destacados enviados por una vista Django. Al bajar aparecen los bloques mediante scroll y los íconos responden al mouse.
2. El catálogo demuestra el ciclo `{% for %}` con diez productos. Se busca `guitarra` para encontrar `Astra Seven`; luego se combina categoría, precio y disponibilidad.
3. La ficha `Orbit One` muestra variables simples y un ciclo sobre el diccionario de especificaciones. La condición de stock decide si aparece el formulario o el estado agotado.
4. Sin una sesión activa, la ficha y la vista rápida muestran el aviso `Inicia sesión para comprar` y no presentan el formulario de cantidad. La sección de cuenta permite crear la sesión. Primero se prueban contraseñas diferentes para observar el error; después se usa una clave válida, se comprueba que `Benjamin` aparece en el encabezado y que la tienda regresa al producto solicitado.
5. Con la sesión activa se abre una vista rápida y se agregan dos unidades. El servidor vuelve a revisar la cuenta, la cantidad y el stock. La confirmación, el contador y el mini carrito se actualizan sin abandonar la página; el carrito completo conserva los controles de edición, calcula el total y exige la sesión antes de confirmar.
6. La confirmación genera un código temporal y vacía el carrito. El alcance técnico explica que la operación no se almacena como una compra comercial.
7. Se amplía la fotografía de `Orbit One` y se cambia el tema. Después se reduce la ventana para mostrar el menú móvil y la reorganización de tarjetas, paneles, filtros y formulario. Las mismas funciones permanecen disponibles.

## 7.3 Archivos que conviene explicar

- `soundshop/settings.py`: registra `core`, plantillas, estáticos, mensajes y sesiones firmadas. `DATABASES = {}` responde a la instrucción específica de la Evaluación 1.
- `core/data/catalogo.json`: simula la información mientras todavía no existe base de datos.
- `core/models.py`: define los atributos y tipos mediante `Categoria` y `Producto`.
- `core/catalogo.py`: carga el JSON, normaliza búsquedas, combina filtros y calcula el carrito.
- `core/forms.py`: declara campos, límites y elecciones válidas.
- `core/urls.py`: contiene rutas semánticas con nombres reutilizables.
- `core/views.py`: recibe cada petición, aplica la lógica, construye el contexto y llama a `render`.
- `templates/`: utiliza herencia, variables, condiciones, ciclos, filtros propios, `static` y `url`.

## 7.4 Explicación MTV y MVC

En Django, el **Model** representa los datos, el **Template** construye la salida HTML y la **View** procesa la solicitud. En la comparación solicitada por el profesor, la vista y `urls.py` cumplen la función de coordinación que suele asociarse al controlador de MVC. La plantilla no contiene la lógica de búsqueda ni los cálculos del carrito; recibe resultados ya preparados.

## 7.5 Respuesta ante funciones no incluidas

La Evaluación 1 pide un prototipo sin conexión a base de datos. El formulario valida sus campos, conserva solo el nombre en una cookie firmada y esa sesión temporal es obligatoria para comprar. El modelo de usuarios, el reingreso persistente con credenciales, la recuperación de contraseña, el administrador Django, el CRUD, el historial de pedidos y la API REST se desarrollarán en evaluaciones posteriores. La entrega actual comprueba el flujo principal con datos JSON sin crear tablas.
