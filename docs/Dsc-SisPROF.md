## 🎯 Objetivo
Centralizar procesos académicos, administrativos y de evaluación para instituciones escolares mediante una plataforma web escalable, segura y modular.

---

## 🏗️ Arquitectura & Stack Técnico
| Componente | Tecnología / Implementación |
|------------|-----------------------------|
| **Backend** | Flask (Python 3.10+) |
| **ORM** | SQLAlchemy |
| **Migraciones** | Alembic |
| **Frontend** | HTML5 + Jinja2 + CSS3 |
| **Base de Datos** | PostgreSQL |
| **Estructura** | `app/` (middleware, models, routes, services, templates, static, utils) |

---

## 🧩 Módulos & Checklist de Desarrollo
- [ ] **1. Autenticación** (Login, Registro, Recuperación)
- [ ] **2. Administración (Superadmin)** (Dashboard global, Gestión de usuarios)
- [ ] **3. Gestión de Colegio** (Configuración institucional, sedes, jornadas)
- [ ] **4. Gestión de Docentes** (CRUD, vinculación, carga horaria)
- [ ] **5. Gestión de Permisos** (Middleware de control, auditoría)
- [ ] **6. Evaluación Docente** 🚧 *(En desarrollo)*
- [ ] **7. Examen Tipo ICFES** 🚧 *(En desarrollo)*
- [ ] **8. Gestión de Estudiantes** ⏳ *(Pendiente)*
- [ ] **9. Citaciones y Seguimiento** ⏳ *(Pendiente)*
- [ ] **10. PIAR y Ajustes Razonables** ⏳ *(Pendiente)*

---

## 🔐 Seguridad
- Roles definidos: `superadmin`, `admin_colegio`, `docente`, `estudiante`, `acudiente`.
- Middleware `@login_required` y `@superuser_required`.
- Validación estricta de permisos por módulo.

---

## 🚀 Instalación
```bash
git clone <url>
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask db upgrade
python run.py