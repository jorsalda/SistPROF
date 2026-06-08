

| 🔧 Componente / Tema                   | 📝 Descripción / Explicación / Propósito                                                       | 🗄️ Tabla(s) Relacionada(s)                                  |
| -------------------------------------- | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| 🏫 Configuración Académica             | Centraliza las reglas académicas y de evaluación de cada colegio.                              | `configuracion_academica`                                    |
| 📅 Períodos Académicos                 | Define los períodos o cortes académicos de cada institución.                                   | `periodos`                                                   |
| 📚 Materias                            | Catálogo de asignaturas impartidas por la institución.                                         | `materias`                                                   |
| 🏛️ Áreas Académicas                   | Agrupan materias afines dentro del currículo institucional.                                    | `areas`                                                      |
| 👨‍🏫 Asignación Académica             | Relaciona docentes, materias, grupos y horarios.                                               | `clases`                                                     |
| 🎯 Competencias                        | Aprendizajes, desempeños o capacidades que serán evaluados durante un período.                 | `competencias_periodo` *(o tabla equivalente que definamos)* |
| 📖 Competencias por Materia            | Relaciona competencias específicas con cada materia.                                           | `competencias_materia`                                       |
| 📝 Indicadores de Logro                | Evidencias observables utilizadas para valorar el desarrollo de una competencia.               | `indicadores_logro`                                          |
| 📊 Escala de Evaluación                | Define la escala institucional utilizada para valorar el desempeño estudiantil.                | `escala_evaluacion`                                          |
| 🔢 Evaluación Cuantitativa             | Maneja notas numéricas según la escala institucional.                                          | `escala_evaluacion`                                          |
| 📝 Evaluación Cualitativa              | Maneja conceptos de desempeño definidos por el colegio.                                        | `escala_evaluacion`                                          |
| 🔄 Evaluación Mixta                    | Permite mostrar simultáneamente conceptos cualitativos y equivalencias numéricas.              | `escala_evaluacion`, `configuracion_academica`               |
| 🎛️ Tipo de Captura                    | Define cómo registran las notas los docentes: cuantitativa, cualitativa o mixta.               | `configuracion_academica.tipo_captura`                       |
| 📋 Modelo de Evaluación del Estudiante | Estructura institucional que define cómo se calcula la nota definitiva.                        | `modelo_evaluacion_estudiante`                               |
| ⚖️ Componentes de Evaluación           | Elementos que participan en la valoración final del estudiante.                                | `modelo_evaluacion_estudiante`                               |
| 📈 Porcentajes de Evaluación           | Cada componente tiene un porcentaje configurable cuya suma debe ser 100%.                      | `modelo_evaluacion_estudiante`                               |
| 👨‍🎓 Autoevaluación                   | Componente opcional donde el estudiante participa en su valoración.                            | `modelo_evaluacion_estudiante`                               |
| 👥 Coevaluación                        | Componente opcional utilizado por algunas instituciones.                                       | `modelo_evaluacion_estudiante`                               |
| 📝 Evaluación Final                    | Componente institucional para pruebas finales o actividades integradoras.                      | `modelo_evaluacion_estudiante`                               |
| 🎯 Registro de Notas                   | Almacena las calificaciones obtenidas por cada estudiante.                                     | Tabla futura de notas                                        |
| ⚖️ Ponderación de Competencias         | Los porcentajes de las competencias se asignan durante la evaluación y no durante su creación. | Tabla futura de evaluación                                   |
| 🤖 Cálculo Automático                  | Calcula promedios, equivalencias y definitivas según las reglas institucionales.               | Proceso académico                                            |
| 📄 Boletines                           | Presentan los resultados académicos del estudiante.                                            | Tabla futura de boletines                                    |
| 📊 Boletín Cuantitativo                | Presenta únicamente valores numéricos.                                                         | `boletines`                                                  |
| 📝 Boletín Cualitativo                 | Presenta únicamente conceptos de desempeño.                                                    | `boletines`                                                  |
| 🔄 Boletín Mixto                       | Presenta simultáneamente concepto y equivalencia numérica.                                     | `boletines`                                                  |
| 🔒 Autonomía Institucional             | Cada colegio administra sus propias reglas académicas y de evaluación.                         | Todas las tablas con `colegio_id`                            |

🗄️ Tablas Principales del Módulo Académico.


| Tabla                                | Función Principal                        |
| ------------------------------------ | ---------------------------------------- |
| `configuracion_academica`            | Parámetros académicos institucionales.   |
| `periodos`                           | Períodos académicos.                     |
| `areas`                              | Áreas académicas.                        |
| `materias`                           | Materias o asignaturas.                  |
| `clases`                             | Asignación académica docente.            |
| `escala_evaluacion`                  | Escalas de valoración.                   |
| `modelo_evaluacion_estudiante`       | Componentes y porcentajes de evaluación. |
| `competencias_materia`               | Competencias asociadas a materias.       |
| `indicadores_logro`                  | Evidencias de desempeño.                 |
| `competencias_periodo` *(propuesta)* | Competencias evaluadas en cada período.  |


