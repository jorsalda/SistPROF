

## 📋 PLAN DE TRABAJO REORGANIZADO (5 FASES)

---

### FASE 1: BACKEND - LÓGICA DE CREACIÓN DE COMPETENCIA MADRE CON INDICADORES

**Objetivo:** Implementar el servicio que recibe los datos de una competencia madre y sus 4 indicadores, los fragmenta (si es necesario) y los guarda en la base de datos con códigos autogenerados.

**Entregables:**

| # | Tarea | Detalle |
| :--- | :--- | :--- |
| 1.1 | **Modelado de Base de Datos** | Crear tablas: `competencias_madre`, `indicadores`, `planilla_competencias`, `planilla_detalle` |
| 1.2 | **Servicio de fragmentación** | Recibir 4 textos (uno por nivel) desde el frontend y procesarlos |
| 1.3 | **Generador de códigos** | Método `generateCode(nivel)` que genera códigos secuenciales por nivel: <br> - Bajo: B200, B201... <br> - Básico: B300, B301... <br> - Alto: B400, B401... <br> - Superior: B500, B501... |
| 1.4 | **Endpoint POST** | `/api/competencias-madre` que recibe: <br> - `nombre` (string) <br> - `descripcion_general` (text) <br> - `materia_id` (int) <br> - `nivel_educativo_id` (int) <br> - `indicadores` (array de 4 objetos con `nivel` y `descripcion`) <br> **Acción:** Guarda la competencia madre y genera los 4 indicadores vinculados |
| 1.5 | **Migración de datos existentes** | Unir los 4 registros actuales (A4400, B2200, B3300, S5500) en una competencia madre llamada "Matemáticas - Conjuntos y Estadística" |

**Criterios de Aceptación:**
- ✅ Al enviar una competencia madre con sus 4 descripciones, se crean 5 registros: 1 en `competencias_madre` y 4 en `indicadores`
- ✅ Cada indicador tiene su código autogenerado según el nivel
- ✅ Los indicadores tienen `orden` 1, 2, 3, 4

---

### FASE 2: BACKEND - LÓGICA DE EDICIÓN Y CONSULTA

**Objetivo:** Implementar los endpoints para editar competencias madre e indicadores, y consultar las competencias de una planilla.

**Entregables:**

| # | Tarea | Detalle |
| :--- | :--- | :--- |
| 2.1 | **Endpoint GET** | `/api/competencias-madre/{id}` - Obtener una competencia madre con sus 4 indicadores |
| 2.2 | **Endpoint PUT** | `/api/competencias-madre/{id}` - Editar nombre y descripción general de la competencia madre (NO afecta a los indicadores) |
| 2.3 | **Endpoint PUT** | `/api/indicadores/{id}` - Editar UN indicador específico (descripción) |
| 2.4 | **Endpoint GET** | `/api/planilla/{planillaId}/competencias` - Obtener todas las competencias madre asociadas a una planilla, con sus indicadores y porcentajes |
| 2.5 | **Endpoint POST** | `/api/planilla/{planillaId}/competencia` - Agregar una competencia madre existente a una planilla (crea registro en `planilla_competencias`) |

**Criterios de Aceptación:**
- ✅ El usuario puede editar la competencia madre sin perder los indicadores
- ✅ El usuario puede editar cada indicador individualmente
- ✅ Al agregar una competencia a la planilla, se crea el registro en `planilla_competencias` con un `orden_columna` autoincremental

---

### FASE 3: FRONTEND - FORMULARIO DE INGRESO DE COMPETENCIAS (IMAGEN 1)

**Objetivo:** Rediseñar la interfaz de "Agregar Nueva Competencia" para que el usuario ingrese los 4 niveles de forma estructurada.

**Entregables:**

| # | Tarea | Detalle |
| :--- | :--- | :--- |
| 3.1 | **Rediseñar el formulario** | - Campo: "Nombre de la Competencia" <br> - Campo: "Descripción General" <br> - **4 pestañas o secciones:** "Nivel Alto", "Nivel Bajo", "Nivel Básico", "Nivel Superior" <br> - Cada sección tiene un textarea para la descripción específica |
| 3.2 | **Eliminar campo "Código"** | Los códigos se autogeneran en el backend, el usuario no los ve ni los edita al crear |
| 3.3 | **Actualizar tabla "Competencias Registradas"** | Mostrar: <br> - Código (de la competencia madre) <br> - Nombre de la competencia <br> - Materia <br> - Nivel Educativo <br> - Acciones: Editar, Ver indicadores |
| 3.4 | **Modal "Ver Indicadores"** | Mostrar los 4 indicadores con: <br> - Código <br> - Nivel <br> - Descripción <br> - Opción de editar cada uno |

**Criterios de Aceptación:**
- ✅ El usuario puede crear una competencia madre ingresando 4 descripciones
- ✅ El formulario envía un array de 4 objetos al backend
- ✅ La tabla muestra solo competencias madre (no indicadores sueltos)

---

### FASE 4: BACKEND - LÓGICA DE PLANILLA CON COMPETENCIAS DINÁMICAS

**Objetivo:** Implementar la lógica para que la planilla pueda tener columnas dinámicas (C1, C2, C3...) y que al agregar una competencia, se agregue automáticamente su columna de desempeño.

**Entregables:**

| # | Tarea | Detalle |
| :--- | :--- | :--- |
| 4.1 | **Endpoint GET** | `/api/planilla/{planillaId}/detalle` - Obtener todos los datos de la planilla incluyendo: <br> - Estudiantes <br> - Competencias (con sus indicadores) <br> - Notas de cada estudiante por competencia <br> - Nivel de desempeño alcanzado por cada estudiante |
| 4.2 | **Endpoint POST** | `/api/planilla/{planillaId}/competencia` - (Ya existe de Fase 2, pero ahora debe: <br> - Agregar la competencia <br> - **Automaticámente agregar su columna de desempeño** en `planilla_detalle` para todos los estudiantes) |
| 4.3 | **Endpoint PUT** | `/api/planilla/competencia/{planillaCompetenciaId}/porcentaje` - Actualizar el porcentaje de una competencia en la planilla |
| 4.4 | **Endpoint PUT** | `/api/planilla/detalle/{id}` - Actualizar nota y nivel de desempeño de un estudiante en una competencia |

**Criterios de Aceptación:**
- ✅ Al agregar una competencia a la planilla, se crea automáticamente un registro en `planilla_detalle` para cada estudiante con `nota=0` y `indicador_id=NULL`
- ✅ El porcentaje se puede editar desde la planilla
- ✅ Los datos de la planilla se devuelven con la estructura correcta para renderizar columnas dinámicas

---

### FASE 5: FRONTEND - PLANILLA (IMAGEN 2) CON COLUMNAS DINÁMICAS

**Objetivo:** Renderizar la planilla con columnas dinámicas (C1, C2, C3...) y permitir agregar nuevas competencias desde la misma planilla.

**Entregables:**

| # | Tarea | Detalle |
| :--- | :--- | :--- |
| 5.1 | **Renderizar columnas dinámicas** | Cada columna (C1, C2, C3...) representa UNA competencia madre. Mostrar: <br> - Código de la competencia como cabecera <br> - Porcentaje como subtítulo <br> - Al pasar el mouse: mostrar los 4 indicadores (tooltip o popup) |
| 5.2 | **Agregar columna de desempeño automáticamente** | Por cada columna de competencia, mostrar una columna adicional de "Desempeño" donde se selecciona: <br> - Alto <br> - Bajo <br> - Básico <br> - Superior |
| 5.3 | **Botón "Agregar Competencia"** | Desde la planilla, permitir agregar una nueva competencia madre (búsqueda o selección). <br> **Al agregar:** Se insertan 2 columnas nuevas: <br> - Una para la nota de la competencia <br> - Una para el desempeño |
| 5.4 | **Editar porcentajes** | Permitir editar el porcentaje de cada competencia directamente desde la cabecera de la columna |
| 5.5 | **Guardar notas y desempeños** | Al modificar una nota o desempeño, enviar al backend vía PUT |

**Criterios de Aceptación:**
- ✅ La planilla muestra N columnas de competencias (C1, C2, C3...) según las competencias asignadas
- ✅ Cada competencia tiene su columna de desempeño al lado
- ✅ Al agregar una nueva competencia, aparecen 2 nuevas columnas automáticamente
- ✅ Las notas y desempeños se guardan correctamente

---

## 📊 RESUMEN DE FASES REORGANIZADAS

| Fase | Nombre | ¿Qué se hace? |
| :--- | :--- | :--- |
| **Fase 1** | Backend - Creación de Competencia Madre | Modelo de datos + Servicio de fragmentación + Generación de códigos + Endpoint POST |
| **Fase 2** | Backend - Edición y Consulta | Endpoints GET, PUT para competencias, indicadores y planilla |
| **Fase 3** | Frontend - Formulario de Ingreso | Rediseño de Imagen 1 (4 pestañas, tabla de competencias madre, edición de indicadores) |
| **Fase 4** | Backend - Lógica de Planilla Dinámica | Endpoints para agregar competencias a planilla, manejar columnas dinámicas y desempeños |
| **Fase 5** | Frontend - Planilla con Columnas Dinámicas | Renderizado de Imagen 2 con columnas dinámicas, botón agregar competencia, edición de notas y desempeños |

---

## ✅ ¿CÓMO EJERCEMOS CONTROL?

1. **Cada fase se ejecuta una a la vez** (como acordamos).
2. **Antes de pasar a la siguiente fase**, tú revisas los entregables y dices "Aprobado" o "Ajustar".
3. **Yo te voy guiando** con el código concreto de cada tarea dentro de la fase.
4. **Tú decides cuándo pasamos a la siguiente fase.**

---

**¿Te parece bien este plan reorganizado? ¿Empezamos con la Fase 1 ahora?** 🚀