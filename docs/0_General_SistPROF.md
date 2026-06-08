📚 Conclusión
Con estos cinco documentos ya tenemos una base documental muy sólida:

🏫 Arquitectura Administrativa.

🎓 Arquitectura Académica.

📚 Arquitectura de Evaluación.

🗄️ Modelo de Datos.

📜 Decisiones de Arquitectura.

Y algo importante: estos documentos no describen únicamente cómo funciona SistPROF

📜 Documento 5: Decisiones de Arquitectura SistPROF
Objetivo

Documentar las decisiones estratégicas, funcionales y técnicas que definen la arquitectura de SistPROF, garantizando coherencia, mantenibilidad y escalabilidad futura.

| 📌 Decisión                                         | 📝 Justificación                                                | 🗄️ Impacto                       |
| --------------------------------------------------- | --------------------------------------------------------------- | --------------------------------- |
| SistPROF será una plataforma SaaS multiinstitución. | Un único sistema debe administrar múltiples colegios.           | `colegios`                        |
| Cada colegio tendrá autonomía operativa.            | Las instituciones tienen procesos y configuraciones diferentes. | Todas las tablas con `colegio_id` |
| El sistema soportará múltiples sedes por colegio.   | Muchos colegios operan desde varias sedes.                      | `sedes`                           |
| La información histórica no se elimina.             | Garantiza trazabilidad institucional.                           | Campos `activo` e historiales     |

🔐 Usuarios y Seguridad


| 📌 Decisión                                          | 📝 Justificación                                                                 | 🗄️ Impacto                                                          |
| ---------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| La autenticación será centralizada.                  | Un único mecanismo de acceso para toda la plataforma.                            | `usuarios`                                                           |
| Usuarios y personas serán entidades separadas.       | Una persona puede requerir autenticación independiente de sus datos funcionales. | `usuarios`, `docentes`, `coordinadores`, `estudiantes`, `acudientes` |
| El sistema manejará roles institucionales.           | Permite controlar accesos según responsabilidades.                               | `usuarios.rol`                                                       |
| Existirá un rol de superadministrador global.        | Administración transversal de la plataforma.                                     | `usuarios.is_superadmin`                                             |
| Se implementará protección contra accesos indebidos. | Incrementar seguridad de la plataforma.                                          | `failed_attempts`, `locked_until`                                    |

🎓 Arquitectura Académica

| 📌 Decisión                                                    | 📝 Justificación                                      | 🗄️ Impacto            |
| -------------------------------------------------------------- | ----------------------------------------------------- | ---------------------- |
| La evaluación estará basada en competencias.                   | Permite seguimiento real del aprendizaje.             | Competencias y notas   |
| Las competencias pertenecen a Grado + Materia + Período.       | Refleja la estructura académica real de los colegios. | `competencias_periodo` |
| Las competencias son definidas por el docente.                 | El docente es responsable de la planeación académica. | Módulo docente         |
| Los indicadores de logro apoyan la evaluación de competencias. | Facilitan evidencias objetivas de desempeño.          | `indicadores_logro`    |
| Las notas definitivas serán calculadas automáticamente.        | Evita errores manuales y garantiza consistencia.      | Motor académico        |


📊 Arquitectura de Evaluación

| 📌 Decisión                                         | 📝 Justificación                                                    | 🗄️ Impacto                            |
| --------------------------------------------------- | ------------------------------------------------------------------- | -------------------------------------- |
| Cada colegio tendrá su propia escala de evaluación. | Adaptación a diferentes SIEE institucionales.                       | `escala_evaluacion`                    |
| La escala será configurable por colegio.            | Flexibilidad institucional.                                         | `escala_evaluacion.colegio_id`         |
| Se soportará evaluación cuantitativa.               | Requerimiento común de muchas instituciones.                        | `configuracion_academica`              |
| Se soportará evaluación cualitativa.                | Algunos colegios evalúan por desempeños.                            | `configuracion_academica`              |
| Se soportará evaluación mixta.                      | Permite combinar conceptos y notas numéricas.                       | `configuracion_academica`              |
| Existirá conversión interna entre escalas.          | Permite cálculos unificados independientemente del tipo de captura. | `escala_evaluacion`                    |
| El tipo de captura será configurable por colegio.   | Adaptación al modelo institucional.                                 | `configuracion_academica.tipo_captura` |


📋 Modelo de Evaluación

| 📌 Decisión                                           | 📝 Justificación                         | 🗄️ Impacto                    |
| ----------------------------------------------------- | ---------------------------------------- | ------------------------------ |
| Cada colegio definirá su propio modelo de evaluación. | Cumplimiento del SIEE institucional.     | `modelo_evaluacion_estudiante` |
| Los componentes de evaluación serán parametrizables.  | Evita reglas rígidas codificadas.        | `modelo_evaluacion_estudiante` |
| La suma de componentes debe ser 100%.                 | Garantiza consistencia matemática.       | Validaciones                   |
| Autoevaluación será opcional.                         | No todos los colegios la utilizan.       | `modelo_evaluacion_estudiante` |
| Coevaluación será opcional.                           | No todos los colegios la utilizan.       | `modelo_evaluacion_estudiante` |
| Evaluación final será configurable.                   | Algunos colegios la utilizan y otros no. | `modelo_evaluacion_estudiante` |


⚖️ Reglas de Ponderación

| 📌 Decisión                                                   | 📝 Justificación                                      | 🗄️ Impacto     |
| ------------------------------------------------------------- | ----------------------------------------------------- | --------------- |
| Las competencias no almacenan porcentaje al crearse.          | La planeación y la evaluación son procesos distintos. | Competencias    |
| Los porcentajes se asignan durante la evaluación.             | Permite flexibilidad al docente.                      | Evaluación      |
| La suma de porcentajes debe respetar el modelo institucional. | Mantiene coherencia con el SIEE.                      | Validaciones    |
| El sistema validará automáticamente las ponderaciones.        | Evita errores de captura.                             | Motor académico |


📄 Boletines

| 📌 Decisión                                        | 📝 Justificación                       | 🗄️ Impacto         |
| -------------------------------------------------- | -------------------------------------- | ------------------- |
| Los boletines serán configurables por institución. | Cada colegio tiene formatos distintos. | Módulo de boletines |
| Se soportarán boletines cuantitativos.             | Compatibilidad institucional.          | Boletines           |
| Se soportarán boletines cualitativos.              | Compatibilidad institucional.          | Boletines           |
| Se soportarán boletines mixtos.                    | Mayor flexibilidad institucional.      | Boletines           |
| Los resultados se generarán automáticamente.       | Reducir carga operativa.               | Motor académico     |


🏗️ Principios Rectores de SistPROF

| Principio                            | Descripción                                                |
| ------------------------------------ | ---------------------------------------------------------- |
| Multiinstitución                     | Un único sistema para múltiples colegios.                  |
| Multisede                            | Cada colegio puede operar varias sedes.                    |
| Configuración antes que programación | Las reglas institucionales deben parametrizarse.           |
| Autonomía institucional              | Cada colegio define sus procesos.                          |
| Trazabilidad                         | La información histórica se conserva.                      |
| Escalabilidad                        | La arquitectura debe permitir crecimiento futuro.          |
| Flexibilidad académica               | Adaptación a diferentes modelos educativos.                |
| Automatización                       | Los cálculos y procesos repetitivos deben ser automáticos. |


🎯 Decisiones Estratégicas Más Importantes Tomadas Hasta Hoy


| Prioridad | Decisión                                                             |
| --------- | -------------------------------------------------------------------- |
| ⭐⭐⭐⭐⭐     | SistPROF será multiinstitución.                                      |
| ⭐⭐⭐⭐⭐     | Cada colegio tendrá su propio SIEE configurable.                     |
| ⭐⭐⭐⭐⭐     | La evaluación estará centrada en competencias.                       |
| ⭐⭐⭐⭐⭐     | Escalas cualitativas, cuantitativas y mixtas coexistirán.            |
| ⭐⭐⭐⭐⭐     | El modelo de evaluación será parametrizable.                         |
| ⭐⭐⭐⭐⭐     | Las notas definitivas serán calculadas automáticamente.              |
| ⭐⭐⭐⭐⭐     | Los boletines se adaptarán a la configuración institucional.         |
| ⭐⭐⭐⭐⭐     | La configuración prevalecerá sobre reglas codificadas en el sistema. |




