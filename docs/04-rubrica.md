# 4. Correspondencia técnica con la rúbrica

## 4.1 Revisión de los diez indicadores

La rúbrica asigna un máximo de diez puntos por indicador, con cien puntos totales. Las capturas proporcionadas muestran diez puntos en los indicadores 1–5 y 8–10, y cinco puntos en 6 y 7: noventa puntos en esa calificación. Las imágenes no contienen comentarios que permitan atribuir la rebaja a una causa específica. La tabla siguiente identifica evidencias de la corrección; no reemplaza la decisión del docente ni asigna una nota futura.

| N.º | Máximo | Requerimiento | Evidencia de la versión corregida | Estado técnico local |
| --- | ---: | --- | --- | --- |
| 1 | 10 | Atributos y tipos según caso y flujo | JSON, diagrama y `02-datos-y-validaciones.md` | Implementado para tienda |
| 2 | 10 | Entrada/salida y validaciones administrativas | `forms.py`, formularios de productos y usuarios, pruebas de datos válidos e inválidos | Implementado; vista previa sin persistencia |
| 3 | 10 | Condiciones y bucles en vistas según flujo | `views.py`: acceso por rol, búsqueda, stock y carrito | Implementado |
| 4 | 10 | HTML administrativo con variables y operadores | Tablas, estados y vistas previas en `core/templates/core/` | Implementado |
| 5 | 10 | Paquetes y librerías externos | Django en `requirements.txt`; Bootstrap 5.3.8 local y licencia | Implementado sin compilación |
| 6 | 10 | Módulos Django, buenas prácticas y GitHub | `forms.Form`, mensajes, CSRF, herencia de plantillas; repositorio configurado | Código implementado; verificar la revisión remota antes de entregar |
| 7 | 10 | startproject, startapp y registro en settings | Esqueleto regenerado, `CoreConfig` registrado y `check` sin incidencias | Implementado; pasos explicados |
| 8 | 10 | URLs semánticas con path y name | Inclusión de `core.urls`; rutas nombradas y `{% url %}` | Implementado |
| 9 | 10 | Petición, contexto y render en views | Lectura de JSON, diccionarios de contexto y `render()` | Implementado |
| 10 | 10 | Validación visual y apoyo de IA | `05-verificacion.md`, pruebas y evidencias visuales | Revisión documentada; explicación del estudiante pendiente |

## 4.2 Entregables y límites de la evaluación

El análisis, diagrama, mockups, HTML estático e integración inicial de Django pertenecen a las fases 1 y 3. Los datos son simulados y no existe conexión definitiva a base de datos. El registro, la gestión y la confirmación de compra no tienen persistencia. La propuesta no añade tarjetas financieras, pagos, inventario real de bodega ni autenticación de producción.

La revisión del estudiante debe comprobar que puede explicar las variables, el recorrido de cada petición, los errores de los formularios y la función de las rutas nombradas. La publicación de estos cambios y la entrega al docente son estados distintos de la revisión local; no deben indicarse como completados antes de verificarlos.
