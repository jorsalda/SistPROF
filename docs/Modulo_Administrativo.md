| 🔧 Componente / Tema                   | 📝 Descripción / Explicación / Propósito                                                                         | 🗄️ Tabla(s) Relacionada(s)                                          |
| -------------------------------------- | ---------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| 🏫 Colegios                            | Instituciones educativas registradas en la plataforma. Constituyen la unidad principal de operación del sistema. | `colegios`                                                           |
| 🔑 Código de Acceso Institucional      | Permite vincular usuarios y registros a una institución específica.                                              | `colegios.codigo_acceso`                                             |
| ⏳ Estado Institucional                 | Controla si un colegio está activo, en prueba o expirado.                                                        | `colegios`                                                           |
| 👤 Usuarios                            | Núcleo de autenticación y acceso al sistema. Todo actor institucional debe poseer un usuario.                    | `usuarios`                                                           |
| 🔐 Seguridad de Acceso                 | Control de contraseñas, intentos fallidos, bloqueos temporales y activación de cuentas.                          | `usuarios`                                                           |
| 🎭 Roles                               | Define el perfil de acceso del usuario dentro de la plataforma.                                                  | `usuarios.rol`                                                       |
| 🏢 Sedes                               | Permite administrar múltiples sedes dentro de una misma institución.                                             | `sedes`                                                              |
| 👨‍🏫 Docentes                         | Personal docente vinculado a un colegio y una sede.                                                              | `docentes`                                                           |
| 👨‍💼 Coordinadores                    | Personal encargado de supervisión académica y administrativa.                                                    | `coordinadores`                                                      |
| 🎓 Estudiantes                         | Alumnos matriculados en la institución.                                                                          | `estudiantes`                                                        |
| 👨‍👩‍👧 Acudientes                    | Responsables legales de los estudiantes.                                                                         | `acudientes`                                                         |
| 🔗 Vinculación Usuario–Persona         | Relaciona cuentas de acceso con docentes, coordinadores, estudiantes y acudientes.                               | `usuarios`, `docentes`, `coordinadores`, `estudiantes`, `acudientes` |
| 📱 Información de Contacto             | Administración de correos, teléfonos y direcciones institucionales.                                              | `docentes`, `estudiantes`, `acudientes`                              |
| 🏫 Organización por Sedes              | Permite distribuir personal y estudiantes entre sedes.                                                           | `sedes`, `docentes`, `estudiantes`                                   |
| 📚 Organización Académica              | Permite clasificar estudiantes por grado, grupo y jornada.                                                       | `estudiantes`                                                        |
| 👨‍👩‍👧 Relación Estudiante–Acudiente | Asociación entre estudiantes y responsables legales.                                                             | `estudiantes.acudiente_principal_id`, `acudientes`                   |
| 📷 Identificación QR                   | Permite generar identificadores únicos para procesos institucionales.                                            | `estudiantes.qr_token`                                               |
| 💳 Suscripciones                       | Controla la vigencia comercial del servicio SaaS.                                                                | `suscripciones`                                                      |
| 🧪 Período de Prueba                   | Permite habilitar instituciones antes de contratar el servicio.                                                  | `colegios`, `suscripciones`, `usuarios`                              |
| 📅 Vigencia de Licencia                | Controla fechas de inicio, finalización y expiración del servicio.                                               | `suscripciones`, `usuarios`                                          |
| 🏢 Límites Operativos                  | Restringe recursos contratados, como cantidad de sedes.                                                          | `suscripciones`                                                      |
| 💰 Facturación Base                    | Almacena información económica del plan contratado.                                                              | `suscripciones`                                                      |
| 👨‍🏫 Novedades Docentes               | Registro de incapacidades, permisos, licencias y situaciones administrativas.                                    | `novedades_docentes`                                                 |
| 📜 Historial Administrativo            | Conserva observaciones y trazabilidad de novedades laborales.                                                    | `novedades_docentes`                                                 |
| 🔒 Activación y Desactivación          | Permite conservar historial sin eliminar registros.                                                              | Campos `activo`, `is_active`                                         |

🏗️ Decisiones de Arquitectura Identificadas

| Decisión                           | Implementación                                 |
| ---------------------------------- | ---------------------------------------------- |
| Plataforma Multiinstitución        | `colegios`                                     |
| Plataforma Multisede               | `sedes`                                        |
| Autenticación centralizada         | `usuarios`                                     |
| Roles institucionales              | `usuarios.rol`                                 |
| Control de seguridad               | `failed_attempts`, `locked_until`              |
| Gestión SaaS integrada             | `suscripciones`                                |
| Períodos de prueba                 | `en_prueba`, `dias_prueba`                     |
| Trazabilidad histórica             | Campos `activo` e historiales                  |
| Separación entre usuario y persona | `usuarios` + tablas de actores institucionales |
| Superadministración global         | `usuarios.is_superadmin`                       |



