
| 🔧 Componente / Tema                          | 📝 Descripción / Explicación / Propósito                                                                        | 🗄️ Tabla(s) Relacionada(s)                                                 |
| --------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| 📖 Módulo Académico                           | Gestiona períodos, competencias, evaluaciones, notas y boletines de cada colegio.                               | Varias tablas del módulo académico                                          |
| 🏫 Colegio                                    | Unidad principal del sistema. Toda configuración académica pertenece a un colegio específico.                   | `colegios`                                                                  |
| 📅 Períodos Académicos                        | Cada colegio administra sus propios períodos (Periodo 1, 2, 3, 4, etc.).                                        | `periodos`                                                                  |
| 📊 Escala de Evaluación                       | Cada colegio puede definir su propia escala de desempeño.                                                       | `escala_evaluacion`                                                         |
| 🔢 Escala Cuantitativa                        | Maneja rangos numéricos (0.0–5.0, 0–100, etc.) según la política institucional.                                 | `escala_evaluacion`                                                         |
| 📝 Escala Cualitativa                         | Maneja conceptos de desempeño definidos por el colegio.                                                         | `escala_evaluacion`                                                         |
| 🔄 Escala Mixta                               | Permite mostrar simultáneamente concepto cualitativo y nota cuantitativa.                                       | `escala_evaluacion`, `configuracion_academica`                              |
| ⚙️ Configuración Académica                    | Centraliza parámetros académicos del colegio.                                                                   | `configuracion_academica`                                                   |
| 🎯 Tipo de Captura                            | Define si las notas se registran como cuantitativas, cualitativas o mixtas.                                     | `configuracion_academica.tipo_captura`                                      |
| 📋 Modelo de Evaluación del Estudiante        | Define la estructura institucional de evaluación.                                                               | `modelo_evaluacion_estudiante`                                              |
| 🧩 Componentes de Evaluación                  | Componentes que participan en el cálculo de la nota final. Ej.: Competencias, Evaluación Final, Autoevaluación. | `modelo_evaluacion_estudiante`                                              |
| 📈 Porcentajes de Evaluación                  | Cada componente tiene un porcentaje configurable cuya suma debe ser 100%.                                       | `modelo_evaluacion_estudiante`                                              |
| 🏛️ Configuración Institucional de Evaluación | Cada colegio define su propio modelo de evaluación según su SIEE.                                               | `modelo_evaluacion_estudiante`, `configuracion_academica`                   |
| 👨‍🏫 Competencias                            | Son definidas por el docente para cada materia, grado y período.                                                | `competencias_periodo` *(pendiente de crear)*                               |
| 🎓 Nivel de Definición de Competencias        | Las competencias pertenecen a una combinación Grado + Materia + Período.                                        | `competencias_periodo`, `materias`, `periodos`                              |
| 📚 Materias                                   | Catálogo de materias académicas.                                                                                | `materias`                                                                  |
| 🏷️ Áreas Académicas                          | Agrupan materias afines dentro del currículo.                                                                   | `areas`                                                                     |
| 👩‍🏫 Asignación Académica                    | Relaciona docente, grupo y materia.                                                                             | `clases`                                                                    |
| ⚖️ Ponderación de Competencias                | Los porcentajes de las competencias se asignan al momento de evaluar, no al momento de crearlas.                | Tabla futura de evaluación o notas                                          |
| 📝 Registro de Notas                          | El docente registra una nota por estudiante para cada competencia.                                              | `notas_competencia` *(pendiente de crear)*                                  |
| 🎯 Evaluación Final                           | Componente opcional definido por la institución dentro de su modelo de evaluación.                              | `modelo_evaluacion_estudiante`, tabla futura de notas                       |
| 👤 Autoevaluación                             | Componente opcional donde el estudiante participa en su valoración.                                             | `modelo_evaluacion_estudiante`, tabla futura de notas                       |
| 👥 Coevaluación                               | Componente opcional utilizado por algunos colegios. Puede estar desactivado.                                    | `modelo_evaluacion_estudiante`, tabla futura de notas                       |
| 🤖 Cálculo Automático                         | SistPROF calcula automáticamente promedios y definitivas.                                                       | Procesa información de varias tablas académicas                             |
| 📄 Boletines                                  | Presentan los resultados académicos según la configuración institucional.                                       | Tabla futura de boletines                                                   |
| 📊 Boletín Cuantitativo                       | Muestra únicamente valores numéricos.                                                                           | `boletines`, `escala_evaluacion`                                            |
| 📝 Boletín Cualitativo                        | Muestra únicamente conceptos de desempeño.                                                                      | `boletines`, `escala_evaluacion`                                            |
| 🔄 Boletín Mixto                              | Muestra concepto y equivalencia numérica.                                                                       | `boletines`, `escala_evaluacion`, `configuracion_academica`                 |
| 🔒 Autonomía Institucional                    | Cada colegio administra sus escalas, modelos y parámetros académicos.                                           | Todas las tablas con `colegio_id`                                           |
| 🏗️ Principio de Diseño                       | La evaluación gira alrededor de competencias; las notas finales son el resultado de cálculos automáticos.       | `competencias_periodo`, `notas_competencia`, `modelo_evaluacion_estudiante` |

---

## ✅ Decisiones de arquitectura aprobadas

| Decisión                                                         | Tabla principal                                            |
| ---------------------------------------------------------------- | ---------------------------------------------------------- |
| Escala de evaluación por colegio                                 | `escala_evaluacion`                                        |
| Tipo de captura configurable (Cuantitativa, Cualitativa o Mixta) | `configuracion_academica`                                  |
| Modelo de evaluación configurable por colegio                    | `modelo_evaluacion_estudiante`                             |
| Componentes de evaluación configurables por colegio              | `modelo_evaluacion_estudiante`                             |
| Competencias definidas por Grado + Materia + Período             | `competencias_periodo`                                     |
| Porcentajes asignados durante la evaluación                      | Tabla futura de evaluación                                 |
| Conversión interna entre cualitativo y cuantitativo              | `escala_evaluacion`                                        |
| Boletines cuantitativos, cualitativos o mixtos                   | `boletines` + `configuracion_academica`                    |
| Cálculo automático de definitivas                                | Módulo académico                                           |
| Configuración institucional basada en el SIEE de cada colegio    | `modelo_evaluacion_estudiante` + `configuracion_academica` |

