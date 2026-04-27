# Arquitectura de Templates — SistPROF

## Principio de diseño

La arquitectura de templates de SistPROF se divide en dos niveles:

### 1. Dashboards por rol
Cada rol tiene su propia base visual y su propio dashboard.

Regla:

```text
Rol = Dashboard propio
```

---

### 2. Módulos funcionales reutilizables
Las funcionalidades se desarrollan como módulos independientes reutilizables entre roles.

Regla:

```text
Funcionalidad = Módulo reutilizable
```

---

## Estructura oficial

```text
templates/
├── admin/
│   ├── admin_base.html
│   └── dashboard.html
│
├── colegio/
│   ├── colegio_base.html
│   └── dashboard.html
│
├── docente/
│   ├── docente_base.html
│   └── dashboard.html
│
├── estudiante/
│   ├── estudiante_base.html
│   └── dashboard.html
│
├── acudiente/
│   ├── acudiente_base.html
│   └── dashboard.html
│
├── estudiantes/
│   ├── listar.html
│   ├── form.html
│   └── ver.html
│
├── docentes/
│   ├── listar.html
│   ├── form.html
│   └── ver.html
│
├── clases/
│   ├── listar.html
│   ├── form.html
│   └── ver.html
│
├── asistencia/
│   ├── listar.html
│   ├── registrar.html
│   └── detalle.html
│
├── novedades/
│   ├── listar.html
│   ├── registrar.html
│   └── detalle.html
│
├── piar/
│   ├── listar.html
│   ├── crear.html
│   └── detalle.html
│
├── citaciones/
│   ├── listar.html
│   ├── crear.html
│   └── detalle.html
│
└── acuerdos_correctivos/
    ├── listar.html
    ├── crear.html
    └── detalle.html
```

---

## Roles del sistema

### Superadmin
Dashboard global del sistema.

Ubicación:

```text
templates/admin/
```

Funciones:
- gestión de usuarios
- gestión de colegios
- estadísticas globales
- aprobaciones

---

### Admin Colegio
Dashboard institucional.

Ubicación:

```text
templates/colegio/
```

Funciones:
- gestión académica
- docentes
- estudiantes
- clases
- reportes

---

### Docente
Dashboard operativo docente.

Ubicación:

```text
templates/docente/
```

Funciones:
- clases asignadas
- asistencia
- evaluación
- novedades

---

### Estudiante
Dashboard de consulta.

Ubicación:

```text
templates/estudiante/
```

Funciones:
- notas
- asistencia
- novedades

---

### Acudiente
Dashboard de seguimiento.

Ubicación:

```text
templates/acudiente/
```

Funciones:
- seguimiento académico
- asistencia
- citaciones

---

## Principio de reutilización

Ejemplo:

El módulo:

```text
templates/estudiantes/
```

puede ser utilizado desde:

- dashboard colegio
- dashboard docente
- dashboard acudiente
- dashboard estudiante

Sin duplicar código.

---

## Regla de escalabilidad

Todo nuevo desarrollo debe respetar esta estructura.

Ejemplo:

Nuevo módulo:

```text
convivencia/
```

No crear dentro de:

```text
colegio/
```

Debe crearse como módulo independiente.

---