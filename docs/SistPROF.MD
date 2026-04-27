📋 **Resumen Técnico Completo - SistPROF (Formato Dos Columnas)**

| 🔧 **Componente / Tema / Código** | 📝 **Descripción / Explicación / Propósito** |
|---|---|
| **📖 Descripción & Visión** | |
| `SistPROF` | Plataforma web SaaS para gestión educativa, centraliza procesos académicos, administrativos y de evaluación institucional. |
| `Objetivo` | Optimizar administración escolar con herramientas digitales para seguimiento académico, control de usuarios y toma de decisiones. |
| `Características principales` | Multiusuario, gestión por roles, control de permisos, arquitectura modular y escalable, integración futura con ICFES. |
| `Tipo de sistema` | SaaS educativo basado en Flask, diseñado para operación en la nube con aislamiento por institución. |
| **🏗️ Arquitectura del Sistema** | |
| `Backend: Flask + Python` | Framework ligero para enrutamiento, manejo de sesiones y lógica de negocio. |
| `ORM: SQLAlchemy` | Mapeo objeto-relacional para consultas seguras, transacciones y relaciones entre tablas. |
| `Migraciones: Alembic` | Control de versiones del esquema de BD, permite evoluciones estructurales sin pérdida de datos. |
| `Frontend: HTML + Jinja2` | Renderizado server-side con plantillas dinámicas, inyección de variables y reutilización de layouts. |
| `CSS + JavaScript básico` | Estilos personalizados para UI profesional y JS mínimo para interactividad cliente (validaciones, toggles). |
| `Base de datos: PostgreSQL` | Motor relacional robusto para integridad referencial, concurrencia y almacenamiento seguro de datos institucionales. |
| `Estructura `app/`` | Organizada en capas: `middleware/`, `models/`, `routes/`, `services/`, `templates/`, `static/`, `utils/`. |
| `Capas del sistema` | 1. Presentación (templates) → 2. Lógica (routes + services) → 3. Datos (models + BD). |
| `Seguridad arquitectónica` | Middleware de autenticación, middleware de superusuario, control de acceso granular por permisos y roles. |
| **🧩 Módulos del Sistema** | |
| `1. Autenticación` | Login, registro de colegios/usuarios, recuperación de contraseña con tokens seguros y gestión de sesiones. |
| `2. Administración` | Dashboard global, gestión de usuarios/colegios, métricas del sistema, control de suscripciones y aprobaciones. |
| `3. Gestión de Colegio` | Panel institucional, configuración de sedes/jornadas, periodos académicos, códigos de acceso y datos organizacionales. |
| `4. Gestión de Docentes` | CRUD de profesores, vinculación a colegios/sedes, carga horaria, asignación de usuarios y estado de actividad. |
| `5. Gestión de Permisos` | Asignación y validación de accesos por rol, middleware de control, auditoría de cambios y restricciones por módulo. |
| `6. Evaluación Docente` | 🚧 *En desarrollo:* Instrumentos de retroalimentación, métricas de desempeño, rúbricas por competencia y reportes. |
| `7. Examen Tipo ICFES` | 🚧 *En desarrollo:* Banco de preguntas estructuradas, aleatorización, temporizador, calificación automática y estadísticas. |
| `8. Gestión de Estudiantes` | ⏳ *Pendiente:* Registro, vinculación a grupos/grados, historial académico, relación con acudientes y QR de asistencia. |
| `9. Citaciones y Seguimiento` | ⏳ *Pendiente:* Registro de novedades disciplinares, citaciones a acudientes, trazabilidad y escalado automático. |
| `10. PIAR y Ajustes Razonables` | ⏳ *Pendiente:* Planes de inclusión, adaptaciones curriculares, seguimiento a estudiantes con necesidades educativas. |
| **🔐 Sistema de Permisos** | |
| `Tipos de usuario` | Administrador, Docente, Usuario básico. Segmentación de accesos según responsabilidades institucionales. |
| `Implementación técnica` | `@login_required` valida sesión activa. `@superuser_required` eleva privilegios. Middleware intercepta cada request. |
| `Ejemplo de permisos` | Ver/crear docentes, editar configuración, acceder a dashboards restringidos, gestionar permisos y aprobar colegios. |
| `Flujo de validación` | 1. Usuario inicia sesión → 2. Middleware verifica token/sesión → 3. Chequeo de rol/permiso → 4. Permite o bloquea acceso. |
| **🗄️ Base de Datos & API** | |
| `Motor` | PostgreSQL (manejo nativo de JSON, índices avanzados, transacciones ACID). |
| `Tablas principales` | `usuario` (id, email, password, rol), `docente` (id, nombre, especialidad), `colegio` (id, nombre), `permiso` (id, nombre, descripción). |
| `Relaciones clave` | Usuario ↔ Colegio (N:1), Docente ↔ Colegio (N:1), Usuario ↔ Permisos (asignación por rol/middleware). |
| `Migraciones` | `flask db init`, `flask db migrate`, `flask db upgrade`. Controlado por Alembic para sincronización dev/prod. |
| `API Interna (Rutas)` | `POST /login`, `POST /register`, `GET/POST /docentes`, `GET /permisos`, `GET /colegio`. Consumo interno vía Jinja2. |
| **🚀 Instalación & Flujo** | |
| `Requisitos` | Python 3.10+, PostgreSQL, pip, git, variables de entorno (`.env`). |
| `Pasos de despliegue` | `git clone` → `python -m venv .venv` → `source .venv/bin/activate` → `pip install -r requirements.txt` → `flask db upgrade` → `python run.py`. |
| `Flujo de inicio` | Usuario accede a URL → Login → Redirección automática por rol → Dashboard principal. |
| `Navegación & Gestión` | Acceso a módulos según permisos → Admin gestiona usuarios/docentes → Asigna permisos → Monitorea actividad. |
| `Seguridad en flujo` | Cada ruta protegida por middleware. Sesiones validadas en servidor. Sin exposición directa de BD al cliente. |
| **📅 Roadmap** | |
| `Corto plazo` | Finalizar módulo estudiantes + Implementar evaluación docente. Consolidar núcleo académico y operativo. |
| `Mediano plazo` | Examen tipo ICFES dinámico + Reportes académicos automatizados. Herramientas de evaluación estandarizada y analítica. |
| `Largo plazo` | Multi-colegio completo (SaaS) + App móvil + Analítica avanzada. Escalabilidad, movilidad e inteligencia de datos. |

