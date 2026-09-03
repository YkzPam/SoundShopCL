# 7. Guion breve para presentar SoundShop CL

## 7.1 Preparación en el computador

La carpeta se abre directamente en Visual Studio Code. En la terminal integrada se ejecutan estos comandos:

```powershell
.\venv\Scripts\Activate.ps1
python manage.py check
python manage.py test
python manage.py runserver
```

El primer comando activa el entorno aislado; el segundo revisa la configuración; el tercero ejecuta las quince pruebas; el último inicia la página en `http://127.0.0.1:8000/`.

## 7.2 Recorrido sugerido

1. La portada permite explicar que SoundShop CL corresponde al sistema de sucursal y vitrina de Music Pro. Se muestran categorías y productos destacados enviados por una vista Django.
2. El catálogo demuestra el ciclo `{% for %}`. Se busca `microfono` sin tilde para comprobar que el servidor encuentra `Vela C1`; luego se combina categoría, precio y disponibilidad.
3. La ficha `Orbit One` muestra variables simples y un ciclo sobre el diccionario de especificaciones. La condición de stock decide si aparece el formulario o el estado agotado.
4. Se agrega una cantidad válida al carrito. El servidor revisa que sea mayor que cero y que no supere las existencias. El carrito calcula subtotal, cantidad total y total general.
5. La confirmación genera un código temporal y vacía el carrito. La pantalla declara que no hubo pago ni almacenamiento persistente.
6. Se reduce la ventana para mostrar el menú móvil y la reorganización de tarjetas y filtros. Las mismas funciones permanecen disponibles.

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

La Evaluación 1 pide un prototipo sin conexión a base de datos. Registro de usuarios, administrador Django, CRUD persistente, historial de pedidos y API REST se desarrollarán en las evaluaciones posteriores. Implementarlos ahora alteraría el alcance indicado en la página 5 del documento semestral. La entrega actual representa y comprueba el flujo principal con datos mock en JSON.
