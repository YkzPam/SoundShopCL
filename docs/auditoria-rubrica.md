# 3. Auditoría de la Evaluación 1

## 3.1 Criterio de revisión

La revisión utiliza la escala incluida en `Instrucciones Evaluación 1-20260903.zip`: diez indicadores con un máximo de 10 puntos cada uno, para un total de 100. La tabla siguiente resume los indicadores; no reemplaza su redacción oficial ni asigna una nota docente. Las marcas presentes en la plantilla Excel no constituyen una calificación de SoundShop CL.

| N.º | Indicador resumido | Máximo | Evidencia en la entrega | Estado |
|---|---|---:|---|---|
| 1 | Atributos y tipos según caso y flujo | 10 | `core/models.py`, JSON y modelo de datos documentado | Evidencia implementada |
| 2 | Entradas, salidas y validaciones de formularios administrativos | 10 | `FichaGestionForm`, siete campos, errores y resultado; seis pruebas de gestión | Evidencia implementada |
| 3 | Condiciones y ciclos del servidor vinculados al flujo administrativo | 10 | `core/gestion.py`, validación, estados y recorrido de fichas documentado | Evidencia implementada |
| 4 | Plantillas administrativas, variables y operadores coherentes con el diagrama | 10 | `gestion_producto.html`, ciclos, condiciones y cálculo de existencias | Evidencia implementada |
| 5 | Uso de paquetes externos | 10 | `requirements.txt`, `package.json`, lockfile y Tailwind compilado | Evidencia implementada |
| 6 | Formularios, mensajes, estilos y proyecto en GitHub | 10 | Formularios Django, mensajes, CSS y pruebas; falta verificar publicación pública final | Parcial hasta publicar |
| 7 | Creación e instalación de proyecto y aplicación Django | 10 | `manage.py`, paquete `soundshop`, app `core` registrada | Evidencia implementada |
| 8 | Rutas semánticas, nombradas y organizadas | 10 | `soundshop/urls.py`, `core/urls.py`, namespace `core` | Evidencia implementada |
| 9 | Vistas, solicitudes, contexto y renderizado | 10 | `core/views.py`, `core/gestion.py` y plantillas | Evidencia implementada |
| 10 | Validación asistida por IA de código, rutas y plantillas | 10 | Registro de apoyo y comprobaciones reproducibles | Evidencia documentada |
| | Total posible de la escala | **100** | No corresponde a un puntaje obtenido | Pendiente de evaluación |

## 3.2 Entregables adicionales de las instrucciones

| Requisito | Respaldo | Situación |
|---|---|---|
| Diagrama simple | Enlace Excalidraw y archivo editable | Disponible; correspondencia explicada en arquitectura |
| Mockups o prototipo de interfaz | Selección de vistas y estados en `mockups-prototipo.md` | Disponible; las capturas se identifican como evidencia de implementación |
| HTML semántico y framework CSS | Plantilla base, vistas DTL y Tailwind compilado | Implementado |
| Investigación de proyectos similares | `investigacion-referentes.md` con dos fuentes oficiales | Documentada retrospectivamente |
| Alcance validado por docente | `alcance-evaluacion-1.md` | Aprobación por confirmar con el docente |
| Sistema integrado y documentación básica | README, rutas, datos y guía de instalación | Disponible |
| Repositorio público | Enlace real de GitHub y última versión subida | Pendiente |
| Demostración y comprensión del código | `guion-demostracion.md` | Guion preparado; exposición pendiente |

## 3.3 Verificación y límites

Las comprobaciones finales y sus resultados se registran en [Verificación de entrega](verificacion-entrega.md). Las pruebas automáticas no sustituyen la revisión visual, la evaluación del docente ni la explicación del estudiante. No se presenta una estimación numérica como nota garantizada. Para cerrar la entrega se debe verificar el repositorio público desde fuera de la cuenta propietaria, confirmar el alcance aceptado y realizar la demostración solicitada.

La aplicación sigue sin base de datos. El formulario administrativo valida, pero no guarda ni publica. El carrito admite invitados y exige cuenta solo al confirmar. Las cuentas y los pedidos son temporales; no existe pago real. Estas restricciones deben explicarse con el mismo criterio en la presentación.
