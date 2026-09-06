# 6. Registro de apoyo de inteligencia artificial

## 6.1 Alcance del apoyo

El desarrollo recibió asistencia de Codex para estructurar Django, revisar rutas y contexto, construir formularios, mejorar la interfaz, elaborar pruebas y ordenar la documentación. El estudiante definió el proyecto de tienda, solicitó cambios y proporcionó las instrucciones y rúbrica. Este registro declara la asistencia; no acredita autoría exclusivamente manual ni sustituye la comprensión exigida durante la evaluación.

## 6.2 Actividades y evidencia

| Actividad asistida | Resultado verificable | Revisión disponible |
|---|---|---|
| Tipos y datos del caso | Dataclasses y catálogo JSON | `core/models.py`, `core/data/catalogo.json` |
| Rutas y renderizado | Vistas con contexto y plantillas compartidas | `core/urls.py`, `core/views.py`, `templates/` |
| Validación administrativa | Formulario y vista previa sin persistencia | `core/forms.py`, `core/gestion.py`, `core/test_gestion.py` |
| Carrito y cuenta | Agregado como invitado, acceso al confirmar y retorno local | `core/tests.py`, `core/cuentas.py` |
| Diseño y responsive | Identidad visual, navegación y estados | CSS, JavaScript y selección de evidencias |
| Revisión de entrega | Correspondencia entre documentos y comportamiento | Auditoría y registro final de comprobaciones |

Las solicitudes abarcaron validación de código, coherencia de rutas, variables disponibles en plantillas, formularios inválidos y resultados esperados. Las pruebas ejecutables permiten contrastar parte de esas propuestas en lugar de aceptar únicamente una descripción generada. El [registro final](verificacion-entrega.md) identifica los comandos y resultados; no equivale a una auditoría de seguridad de producción.

## 6.3 Material visual y fuentes

La entrega utiliza imágenes generadas para la identidad de la tienda; la intervención específica en el pie se conserva en [Imagen del pie](imagen-footer.md). Las capturas de interfaz son evidencia del sitio implementado, no supuestos bocetos elaborados antes de programar. La [investigación de referentes](investigacion-referentes.md) identifica fuentes externas oficiales y separa observaciones de decisiones propias.

## 6.4 Responsabilidad y límites

Corresponde al estudiante revisar la entrega y poder explicar el flujo de solicitudes, los tipos, las condiciones, los ciclos y las validaciones. No se afirma que haya realizado una defensa oral ni recibido aprobación docente. La asistencia no garantiza puntaje máximo. El sistema conserva el alcance de E1 sin base de datos, pagos reales o gestión persistente; cualquier ampliación requiere una nueva implementación y revisión.
