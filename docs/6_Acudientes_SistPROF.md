📜 Arquitectura del Módulo de Acudientes - SistPROF
Objetivo
Documentar las decisiones estratégicas, funcionales y técnicas que definen el módulo de gestión de acudientes en SistPROF, garantizando una experiencia completa tanto para la administración institucional como para el acceso directo de los padres/acudientes.

🏫 Gestión Institucional de Acudientes

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| Los acudientes dependen directamente del colegio | Permite al colegio gestionar sus propios acudientes sin intervención externa | `acudientes.colegio_id` |
| Cada acudiente tiene su propio usuario y contraseña | Facilita el acceso independiente al sistema | `usuarios` con rol 'acudiente' |
| El colegio puede crear, editar y eliminar acudientes | Autonomía operativa institucional | Rutas en `colegio_routes.py` |
| Los datos del acudiente incluyen información de contacto completa | Facilita la comunicación colegio-acudiente | `telefono`, `email`, `direccion` |
| Se registra el parentesco con el estudiante | Información relevante para el colegio | `parentesco` |


 👨‍👩‍👧‍👦 Relaciones Acudiente-Estudiante

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| Un estudiante puede tener múltiples acudientes | Situaciones reales: padres separados, tutores legales, abuelos | Tabla intermedia `estudiante_acudiente` |
| Un acudiente puede tener múltiples estudiantes | Un padre con varios hijos en el mismo colegio | Relación muchos-a-muchos |
| Existe un acudiente principal por estudiante | Contacto prioritario para emergencias | `estudiantes.acudiente_principal_id` |
| La relación es bidireccional | Permite consultas desde ambos lados | Relaciones SQLAlchemy configuradas |
| La tabla intermedia es pura (solo claves foráneas) | Simplifica la relación sin datos adicionales | `estudiante_acudiente` |

---

## 🔐 Autenticación y Acceso

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| Los acudientes tienen su propio rol en el sistema | Control de acceso específico | `usuarios.rol = 'acudiente'` |
| El login redirige automáticamente al dashboard del acudiente | Experiencia de usuario optimizada | `auth_routes.py` |
| El decorador valida el rol antes de permitir acceso | Seguridad por rol | `@login_required_acudiente` |
| Se usa `current_user` en lugar de `session` | Estándar de Flask-Login | Todas las rutas del módulo |
| El acudiente solo ve información de SUS estudiantes | Privacidad y seguridad de datos | `verificar_pertenencia()` |

---

## 📊 Dashboard del Acudiente

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| Vista consolidada de todos los estudiantes a cargo | El acudiente ve toda la información en un solo lugar | `AcudienteService.get_estudiantes_by_acudiente()` |
| Se muestra promedio general por estudiante | Información académica clave | Cálculo en tiempo real |
| Se muestra porcentaje de asistencia | Control de asistencia visible | `get_asistencia_porcentaje()` |
| Se muestran novedades recientes | Alertas inmediatas | `get_novedades_recientes()` |
| Se muestran citaciones pendientes | Acciones requeridas visibles | `get_citaciones_pendientes()` |
| Alertas automáticas por bajo rendimiento o asistencia | Notificación proactiva | `get_alerta_estudiante()` |

---

## 📚 Información Académica Detallada

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| Detalle completo por estudiante | Información profunda cuando se necesita | `estudiante_detalle()` |
| Calificaciones por materia y período | Seguimiento académico detallado | `get_calificaciones()` |
| Historial de asistencias | Trazabilidad de asistencia | `get_asistencias_recientes()` |
| Resultados de exámenes | Evaluaciones objetivas | `get_examenes_estudiante()` |
| Novedades con gravedad e informe | Transparencia disciplinaria | `get_novedades_estudiante()` |
| Citaciones con fecha y motivo | Organización de reuniones | `get_citaciones_estudiante()` |

---

## 💬 Comunicación e Interacción

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| El acudiente puede responder a novedades | Diálogo bidireccional | `responder_novedad()` |
| El acudiente puede confirmar citaciones | Gestión de asistencia a reuniones | `confirmar_citacion()` |
| El acudiente puede reportar novedades | Participación activa | `reportar_novedad()` |
| El acudiente puede solicitar reuniones | Comunicación proactiva | `solicitar_reunion()` |
| El acudiente puede enviar mensajes al colegio | Canal de comunicación directo | `enviar_mensaje()` |

---

## 🎨 Experiencia de Usuario

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| Interfaz responsiva con Tailwind CSS | Accesible desde cualquier dispositivo | Templates HTML |
| Gráficos interactivos con Chart.js | Visualización clara del rendimiento | `dashboard_acudiente.html` |
| Notificaciones con SweetAlert2 | Feedback visual atractivo | JavaScript en templates |
| Navegación intuitiva con tabs | Organización lógica de información | `estudiante_detalle.html` |
| Formularios con validación HTML5 | Prevención de errores | `formulario_acudiente.html` |

---

## 🔄 Integración con Otros Módulos

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| Integración con módulo de novedades | Acceso a información disciplinaria | `Novedad` model |
| Integración con módulo de citaciones | Gestión de reuniones | `CitacionAcudiente` model |
| Integración con módulo de evaluación | Acceso a calificaciones | `EvaluacionEstudiante` model |
| Integración con módulo de asistencia | Control de asistencia | `Asistencia` model |
| Integración con módulo de exámenes | Resultados de evaluaciones | `ResultadoExamen` model |
| Integración con sistema de notificaciones | Alertas automáticas | `NotificationLog` model |

---

## 🏗️ Principios de Diseño Aplicados

| Principio | Descripción |
|-----------|-------------|
| **Separación de responsabilidades** | `AcudienteService` maneja la lógica de negocio, las rutas manejan el flujo HTTP |
| **Seguridad por diseño** | Validación de pertenencia antes de mostrar información |
| **Experiencia unificada** | Mismo estándar de UI/UX en todo el módulo |
| **Escalabilidad** | Estructura preparada para agregar más funcionalidades |
| **Mantenibilidad** | Código organizado y documentado |
| **Privacidad** | Cada acudiente solo ve información de sus estudiantes |
| **Transparencia** | Toda la información relevante es visible |
| **Proactividad** | Alertas y notificaciones automáticas |

---

## 🎯 Funcionalidades Implementadas

### ✅ Gestión desde el Colegio

- [x] Listar todos los acudientes del colegio
- [x] Crear nuevo acudiente con usuario y contraseña
- [x] Editar información del acudiente
- [x] Eliminar acudiente y su usuario asociado
- [x] Validación de email único
- [x] Integración con tabla intermedia `estudiante_acudiente`

### ✅ Acceso del Acudiente

- [x] Login independiente con rol 'acudiente'
- [x] Dashboard con resumen de todos los estudiantes
- [x] Vista detallada por estudiante
- [x] Consulta de calificaciones por período
- [x] Historial de asistencias
- [x] Resultados de exámenes
- [x] Novedades disciplinarias
- [x] Citaciones pendientes

### ✅ Interacción

- [x] Responder a novedades
- [x] Confirmar asistencia a citaciones
- [x] Reportar novedades
- [x] Solicitar reuniones
- [x] Enviar mensajes al colegio

---

## 📈 Estado Actual del Módulo

| Componente | Estado |
|------------|--------|
| Modelo de datos | 🟢 Implementado |
| Gestión desde colegio | 🟢 Implementado |
| Autenticación | 🟢 Implementado |
| Dashboard principal | 🟢 Implementado |
| Detalle de estudiante | 🟢 Implementado |
| Calificaciones | 🟢 Implementado |
| Asistencia | 🟢 Implementado |
| Exámenes | 🟢 Implementado |
| Novedades | 🟢 Implementado |
| Citaciones | 🟢 Implementado |
| Comunicación bidireccional | 🟢 Implementado |
| Notificaciones automáticas | 🟡 En progreso |
| Reportes y estadísticas | 🔵 Futuro |

---

## 🔮 Próximos Pasos Recomendados

| Prioridad | Tarea | Descripción |
|-----------|-------|-------------|
| ⭐⭐⭐⭐⭐ | Asociar estudiantes a acudientes | Crear interfaz para asignar estudiantes desde el panel del colegio |
| ⭐⭐⭐⭐⭐ | Notificaciones por email | Enviar alertas automáticas cuando hay novedades o citaciones |
| ⭐⭐⭐⭐ | Descarga de boletines | Permitir que el acudiente descargue boletines en PDF |
| ⭐⭐⭐⭐ | Historial completo | Mostrar historial académico completo del estudiante |
| ⭐⭐⭐ | Chat en tiempo real | Comunicación instantánea con docentes |
| ⭐⭐ | App móvil | Versión móvil para acudientes |

---

## 📜 Conclusión

El módulo de acudientes de SistPROF representa un componente fundamental que cierra el ciclo de comunicación entre el colegio y las familias. Con una arquitectura bien definida, seguridad robusta y una experiencia de usuario optimizada, el módulo permite:

- **Para el colegio**: Gestión centralizada y autónoma de los acudientes
- **Para el acudiente**: Acceso completo y en tiempo real a la información académica y disciplinaria de sus hijos
- **Para el estudiante**: Mayor seguimiento y apoyo desde el hogar

Este módulo, combinado con los demás componentes del sistema (administración, académico, evaluación), consolida a SistPROF como una plataforma integral de gestión educativa que responde a las necesidades reales de las instituciones modernas.