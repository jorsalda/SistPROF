🗄️ Documento 4: Modelo de Datos SistPROF
Objetivo

Documentar la estructura lógica de la base de datos de SistPROF, identificando entidades principales, relaciones, dependencias y responsabilidades funcionales de cada tabla.

| 🗄️ Tabla       | 📝 Propósito                                       | 🔗 Relaciones Principales |
| --------------- | -------------------------------------------------- | ------------------------- |
| `colegios`      | Institución educativa registrada en la plataforma. | Tabla raíz del sistema.   |
| `sedes`         | Sedes físicas pertenecientes a un colegio.         | FK → `colegios`           |
| `suscripciones` | Control de licencias y vigencia del servicio SaaS. | FK → `colegios`           |
| `usuarios`      | Autenticación, seguridad y control de acceso.      | FK → `colegios`, `sedes`  |


👥 Gestión de Personas.

| 🗄️ Tabla            | 📝 Propósito                                      | 🔗 Relaciones Principales            |
| -------------------- | ------------------------------------------------- | ------------------------------------ |
| `docentes`           | Información institucional del docente.            | FK → `usuarios`, `colegios`, `sedes` |
| `coordinadores`      | Personal coordinador de la institución.           | FK → `usuarios`, `colegios`, `sedes` |
| `estudiantes`        | Información académica básica del estudiante.      | FK → `usuarios`, `colegios`, `sedes` |
| `acudientes`         | Representantes legales de estudiantes.            | FK → `usuarios`                      |
| `novedades_docentes` | Registro administrativo de novedades del docente. | FK → `docentes`, `colegios`          |

🎓 Gestión Académica

| 🗄️ Tabla                            | 📝 Propósito                                           | 🔗 Relaciones Principales               |
| ------------------------------------ | ------------------------------------------------------ | --------------------------------------- |
| `periodos`                           | Períodos académicos institucionales.                   | FK → `colegios`                         |
| `areas`                              | Agrupaciones curriculares.                             | Independiente                           |
| `materias`                           | Asignaturas académicas.                                | FK → `areas`                            |
| `clases`                             | Asignación docente por materia, grupo y horario.       | FK → `docentes`, `materias`, `colegios` |
| `competencias_materia`               | Competencias asociadas a materias.                     | FK → `materias`                         |
| `indicadores_logro`                  | Evidencias observables de aprendizaje.                 | FK → Competencias                       |
| `competencias_periodo` *(propuesta)* | Competencias utilizadas durante un período específico. | FK → `periodos`, `materias`, `colegios` |

📊 Sistema de Evaluación

| 🗄️ Tabla                      | 📝 Propósito                             | 🔗 Relaciones Principales      |
| ------------------------------ | ---------------------------------------- | ------------------------------ |
| `configuracion_academica`      | Parámetros académicos institucionales.   | FK → `colegios`                |
| `escala_evaluacion`            | Escalas cualitativas y cuantitativas.    | FK → `colegios`                |
| `modelo_evaluacion_estudiante` | Componentes de evaluación institucional. | FK → `colegios`                |
| `notas` *(futura)*             | Registro de calificaciones.              | FK → `estudiantes`             |
| `boletines` *(futura)*         | Resultados académicos consolidados.      | FK → `estudiantes`, `periodos` |


📌 Entidades Maestras

| Tabla                          | Motivo                          |
| ------------------------------ | ------------------------------- |
| `colegios`                     | Entidad principal del sistema.  |
| `usuarios`                     | Núcleo de autenticación.        |
| `periodos`                     | Estructura temporal académica.  |
| `materias`                     | Base curricular.                |
| `escala_evaluacion`            | Base del sistema de evaluación. |
| `modelo_evaluacion_estudiante` | Define el cálculo académico.    |

🏗️ Principios de Diseño del Modelo de Datos


| Principio              | Aplicación                                                           |
| ---------------------- | -------------------------------------------------------------------- |
| Multiinstitución       | Todas las configuraciones dependen de `colegios`.                    |
| Multisede              | Una institución puede tener múltiples sedes.                         |
| Normalización          | Separación entre usuarios, docentes, estudiantes y acudientes.       |
| Configurabilidad       | Escalas y modelos de evaluación parametrizables.                     |
| Escalabilidad          | Nuevos módulos pueden agregarse sin modificar la estructura central. |
| Trazabilidad           | Uso extensivo de campos `activo`, fechas y registros históricos.     |
| Flexibilidad Académica | Adaptación a diferentes SIEE institucionales.                        |

📈 Estado Actual del Modelo

| Módulo                      | Estado          |
| --------------------------- | --------------- |
| Administración              | 🟢 Implementado |
| Usuarios y Seguridad        | 🟢 Implementado |
| Académico Básico            | 🟢 Implementado |
| Configuración de Evaluación | 🟢 Implementado |
| Escalas Institucionales     | 🟢 Implementado |
| Modelo de Evaluación        | 🟢 Implementado |
| Competencias por Período    | 🟡 En diseño    |
| Registro de Notas           | 🟡 En diseño    |
| Boletines                   | 🟡 En diseño    |
| Analítica Académica         | 🔵 Futuro       |


