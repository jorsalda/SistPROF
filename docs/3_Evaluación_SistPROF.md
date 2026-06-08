| 🔧 Componente / Tema           | 📝 Descripción / Explicación / Propósito                                   | 🗄️ Tabla(s) Relacionada(s)                               |
| ------------------------------ | -------------------------------------------------------------------------- | --------------------------------------------------------- |
| ⚙️ Configuración de Evaluación | Centraliza las reglas generales de evaluación de cada colegio.             | `configuracion_academica`                                 |
| 🏫 SIEE Institucional          | Permite que cada colegio implemente su propio sistema de evaluación.       | `configuracion_academica`, `modelo_evaluacion_estudiante` |
| 📊 Escala de Evaluación        | Define los niveles de desempeño institucionales.                           | `escala_evaluacion`                                       |
| 🔢 Escala Cuantitativa         | Evaluación mediante valores numéricos.                                     | `escala_evaluacion`                                       |
| 📝 Escala Cualitativa          | Evaluación mediante conceptos de desempeño.                                | `escala_evaluacion`                                       |
| 🔄 Escala Mixta                | Combina valoración numérica y conceptual.                                  | `escala_evaluacion`                                       |
| 🎛️ Tipo de Captura            | Define cómo registra las notas el docente.                                 | `configuracion_academica.tipo_captura`                    |
| 📋 Modelo de Evaluación        | Estructura institucional que determina cómo se calcula la nota definitiva. | `modelo_evaluacion_estudiante`                            |
| 🧩 Componentes de Evaluación   | Elementos que participan en el cálculo final.                              | `modelo_evaluacion_estudiante`                            |
| 🎯 Competencias                | Constituyen el eje principal del proceso evaluativo.                       | `competencias_periodo` *(propuesta)*                      |
| 📖 Competencias por Materia    | Competencias asociadas a cada asignatura.                                  | `competencias_materia`                                    |
| 📌 Indicadores de Logro        | Evidencias observables para valorar una competencia.                       | `indicadores_logro`                                       |
| 📈 Porcentajes de Evaluación   | Cada componente tiene una ponderación definida por la institución.         | `modelo_evaluacion_estudiante`                            |
| 👨‍🎓 Autoevaluación           | Valoración realizada por el propio estudiante.                             | `modelo_evaluacion_estudiante`                            |
| 👥 Coevaluación                | Valoración realizada por compañeros de clase.                              | `modelo_evaluacion_estudiante`                            |
| 📝 Evaluación Final            | Prueba o actividad integradora del período.                                | `modelo_evaluacion_estudiante`                            |
| 📋 Registro de Calificaciones  | Almacena las notas obtenidas por los estudiantes.                          | Tabla futura de notas                                     |
| ⚖️ Ponderación de Competencias | Distribución porcentual asignada a las competencias durante la evaluación. | Tabla futura de evaluación                                |
| 🤖 Motor de Cálculo Académico  | Calcula promedios, equivalencias y notas definitivas.                      | Procesos académicos                                       |
| 📄 Boletines                   | Presentan resultados académicos al estudiante y acudiente.                 | Tabla futura de boletines                                 |
| 🔄 Conversión de Escalas       | Permite traducir resultados cualitativos a cuantitativos y viceversa.      | `escala_evaluacion`                                       |
| 🔒 Autonomía Institucional     | Cada colegio define sus propias reglas de evaluación.                      | Todas las tablas con `colegio_id`                         |

🗄️ Tablas Principales del Subsistema de Evaluación

| Tabla                                | Función Principal                        |
| ------------------------------------ | ---------------------------------------- |
| `configuracion_academica`            | Reglas generales de evaluación.          |
| `escala_evaluacion`                  | Escalas institucionales.                 |
| `modelo_evaluacion_estudiante`       | Componentes y porcentajes de evaluación. |
| `competencias_materia`               | Competencias asociadas a materias.       |
| `indicadores_logro`                  | Evidencias de desempeño.                 |
| `competencias_periodo` *(propuesta)* | Competencias evaluadas por período.      |
| `notas` *(futura)*                   | Registro de calificaciones.              |
| `boletines` *(futura)*               | Resultados académicos consolidados.      |

🏗️ Decisiones de Arquitectura Aprobadas

| Decisión                                           | Estado |
| -------------------------------------------------- | ------ |
| Escala de evaluación por colegio                   | ✅      |
| Modelo de evaluación configurable por colegio      | ✅      |
| Captura cuantitativa, cualitativa y mixta          | ✅      |
| Conversión automática entre escalas                | ✅      |
| Competencias como eje de evaluación                | ✅      |
| Competencias asociadas a Grado + Materia + Período | ✅      |
| Porcentajes asignados durante la evaluación        | ✅      |
| Autoevaluación configurable                        | ✅      |
| Coevaluación configurable                          | ✅      |
| Evaluación final configurable                      | ✅      |
| Boletines configurables por institución            | ✅      |
| Cálculo automático de definitivas                  | ✅      |
| Adaptación al SIEE de cada colegio                 | ✅      |


📌 Modelo de Evaluación Definido Actualmente

| Componente       | Participación |
| ---------------- | ------------- |
| Competencias     | 75%           |
| Evaluación Final | 20%           |
| Autoevaluación   | 5%            |
| Total            | 100%          |


