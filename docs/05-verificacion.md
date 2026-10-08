# 5. Verificación de la corrección y apoyo de IA

## 5.1 Pruebas del servidor

El 8 de octubre de 2026 se ejecutó `manage.py check` sin incidencias y `manage.py test core` con 23 pruebas aprobadas. Las pruebas utilizan `SimpleTestCase`, por lo que no habilitan consultas a una base de datos. Cubren páginas públicas, filtros, ficha inexistente, acceso por rol, rechazo del acceso incorrecto, restricción administrativa, errores de formularios, salida válida sin escritura de JSON, stock, totales, confirmación, salida y protección CSRF.

La primera ejecución detectó una validación anticipada que evaluaba las categorías antes de cargar sus opciones. Se eliminó esa evaluación del constructor del formulario. Otra comprobación asumía una separación de miles distinta a la localización aplicada por Django; se cambió para verificar el valor entero de salida. La segunda revisión completa aprobó las 23 pruebas. Estos resultados corresponden a comprobaciones técnicas locales, no a pruebas realizadas con usuarios reales.

## 5.2 Recursos y animaciones

La hoja `static/css/tienda.css` y el script `static/js/tienda.js` forman parte de la entrega. Bootstrap 5.3.8 está incluido con su licencia. Las animaciones usan transiciones CSS e `IntersectionObserver`; no necesitan una compilación previa. Si JavaScript no está disponible o el usuario solicita movimiento reducido, el contenido sigue visible. El cambio de tema también funciona cuando el navegador bloquea el almacenamiento local, aunque no conserva la preferencia.

La descarga de GitHub debe ejecutarse con Django. Abrir una plantilla HTML directamente no procesa `{% static %}` ni `{% url %}`. La causa concreta del problema observado en una descarga anterior no se reprodujo antes de reconstruir el proyecto; no se atribuye automáticamente a GitHub, al navegador ni a una herramienta CSS.

## 5.3 Uso de IA y explicación del estudiante

Se comprobó una copia ZIP extraída fuera de la carpeta de trabajo, con un entorno virtual nuevo y los requisitos instalados. Esa copia aprobó las mismas 23 pruebas. La revisión de navegador bloqueó los recursos externos y comprobó seis rutas en anchos de 390, 768 y 1440 píxeles: no detectó desbordamiento horizontal ni imágenes rotas. También pasó la navegación móvil, el hover, la aparición al hacer scroll, el modo oscuro, la validación administrativa y la visualización con movimiento reducido o sin JavaScript. Los resultados proceden de pruebas automatizadas locales, no de sesiones con usuarios reales.

La asistencia de IA se utilizó para comparar la estructura con la corrección, simplificar el panel, proponer formularios y revisar errores. El estudiante debe revisar el código y explicar el caso de tienda: `request.GET` y `request.POST`, `is_valid()`, `cleaned_data`, listas y diccionarios JSON, condiciones por rol, bucles de productos y renderizado DTL. No se afirma que esa explicación ya haya sido evaluada por el docente.

La versión anterior se conservó fuera de la carpeta de entrega, en un respaldo local recuperable. No se modificó la guía original del docente. La sincronización con GitHub se confirma comparando la revisión local con la remota, después de publicar los cambios.
