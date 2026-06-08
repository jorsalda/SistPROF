-- DROP SCHEMA public;

CREATE SCHEMA public AUTHORIZATION pg_database_owner;

-- DROP TYPE public.dia_semana;

CREATE TYPE public.dia_semana AS ENUM (
	'lunes',
	'martes',
	'miercoles',
	'jueves',
	'viernes');

-- DROP TYPE public.diasemana;

CREATE TYPE public.diasemana AS ENUM (
	'LUNES',
	'MARTES',
	'MIERCOLES',
	'JUEVES',
	'VIERNES');

-- DROP TYPE public.nivel_desempeno;

CREATE TYPE public.nivel_desempeno AS ENUM (
	'Bajo',
	'Basico',
	'Alto',
	'Superior');

-- DROP TYPE public.niveldesempeno;

CREATE TYPE public.niveldesempeno AS ENUM (
	'BAJO',
	'BASICO',
	'ALTO',
	'SUPERIOR');

-- DROP TYPE public.rol_usuario;

CREATE TYPE public.rol_usuario AS ENUM (
	'superadmin',
	'admin_colegio',
	'docente',
	'estudiante',
	'acudiente');

-- DROP TYPE public.tipo_evento_colegio;

CREATE TYPE public.tipo_evento_colegio AS ENUM (
	'ingreso',
	'salida');

-- DROP TYPE public.tipo_gravedad;

CREATE TYPE public.tipo_gravedad AS ENUM (
	'Tipo 1',
	'Tipo 2',
	'Tipo 3');

-- DROP TYPE public.tipo_novedad_enum;

CREATE TYPE public.tipo_novedad_enum AS ENUM (
	'DISCIPLINA',
	'ACADEMICO',
	'LLEGADA_TARDE');

-- DROP TYPE public.tipoevento;

CREATE TYPE public.tipoevento AS ENUM (
	'INGRESO',
	'SALIDA');

-- DROP TYPE public.tipogravedad;

CREATE TYPE public.tipogravedad AS ENUM (
	'TIPO_1',
	'TIPO_2',
	'TIPO_3');

-- DROP TYPE public.tiponovedad;

CREATE TYPE public.tiponovedad AS ENUM (
	'DISCIPLINA',
	'ACADEMICO',
	'LLEGADA_TARDE');

-- DROP SEQUENCE acudientes_id_seq;

CREATE SEQUENCE acudientes_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE acuerdos_correctivos_id_seq;

CREATE SEQUENCE acuerdos_correctivos_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE acuerdos_evaluacion_id_seq;

CREATE SEQUENCE acuerdos_evaluacion_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE ajustes_razonables_id_seq;

CREATE SEQUENCE ajustes_razonables_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE alertas_id_seq;

CREATE SEQUENCE alertas_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE areas_gestion_id_seq;

CREATE SEQUENCE areas_gestion_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE asistencias_id_seq;

CREATE SEQUENCE asistencias_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE citaciones_acudiente_id_seq;

CREATE SEQUENCE citaciones_acudiente_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE clase_estudiantes_id_seq;

CREATE SEQUENCE clase_estudiantes_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE clases_id_seq;

CREATE SEQUENCE clases_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE colegios_id_seq;

CREATE SEQUENCE colegios_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE competencias_id_seq;

CREATE SEQUENCE competencias_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE competencias_materia_id_seq;

CREATE SEQUENCE competencias_materia_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE configuracion_disciplinaria_id_seq;

CREATE SEQUENCE configuracion_disciplinaria_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE configuracion_escalamiento_id_seq;

CREATE SEQUENCE configuracion_escalamiento_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE contribuciones_id_seq;

CREATE SEQUENCE contribuciones_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE criterios_evaluacion_id_seq;

CREATE SEQUENCE criterios_evaluacion_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE descargos_estudiante_id_seq;

CREATE SEQUENCE descargos_estudiante_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE docentes_id_seq;

CREATE SEQUENCE docentes_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE escala_evaluacion_id_seq;

CREATE SEQUENCE escala_evaluacion_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE estudiante_acudiente_id_seq;

CREATE SEQUENCE estudiante_acudiente_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE estudiantes_id_seq;

CREATE SEQUENCE estudiantes_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE evaluacion_criterio_id_seq;

CREATE SEQUENCE evaluacion_criterio_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE evaluacion_final_id_seq;

CREATE SEQUENCE evaluacion_final_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE evaluaciones_estudiante_id_seq;

CREATE SEQUENCE evaluaciones_estudiante_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE evidencias_id_seq;

CREATE SEQUENCE evidencias_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE examenes_id_seq;

CREATE SEQUENCE examenes_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE indicadores_logro_id_seq;

CREATE SEQUENCE indicadores_logro_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE ingresos_colegio_id_seq;

CREATE SEQUENCE ingresos_colegio_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE jornadas_colegio_id_seq;

CREATE SEQUENCE jornadas_colegio_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE justificaciones_acudiente_id_seq;

CREATE SEQUENCE justificaciones_acudiente_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE materias_id_seq;

CREATE SEQUENCE materias_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE novedades_id_seq;

CREATE SEQUENCE novedades_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE periodos_academicos_id_seq;

CREATE SEQUENCE periodos_academicos_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE periodos_id_seq;

CREATE SEQUENCE periodos_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE permisos_id_seq;

CREATE SEQUENCE permisos_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE piar_id_seq;

CREATE SEQUENCE piar_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE respuestas_novedad_id_seq;

CREATE SEQUENCE respuestas_novedad_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE resultados_examen_id_seq;

CREATE SEQUENCE resultados_examen_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE sede_coordinadores_id_seq;

CREATE SEQUENCE sede_coordinadores_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE sedes_id_seq;

CREATE SEQUENCE sedes_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE seguimientos_id_seq;

CREATE SEQUENCE seguimientos_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE suscripciones_id_seq;

CREATE SEQUENCE suscripciones_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE tokens_activacion_id_seq;

CREATE SEQUENCE tokens_activacion_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE usuarios_id_seq;

CREATE SEQUENCE usuarios_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;-- public.alembic_version definition

-- Drop table

-- DROP TABLE alembic_version;

CREATE TABLE alembic_version (
	version_num varchar(32) NOT NULL,
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);


-- public.colegios definition

-- Drop table

-- DROP TABLE colegios;

CREATE TABLE colegios (
	id serial4 NOT NULL,
	nombre varchar(150) NOT NULL,
	codigo_acceso varchar(20) NOT NULL,
	activo bool DEFAULT true NULL,
	fecha_expiracion timestamp DEFAULT (now() + '15 days'::interval) NULL,
	en_prueba bool DEFAULT true NULL,
	CONSTRAINT colegios_codigo_acceso_key UNIQUE (codigo_acceso),
	CONSTRAINT colegios_pkey PRIMARY KEY (id)
);


-- public.configuracion_disciplinaria definition

-- Drop table

-- DROP TABLE configuracion_disciplinaria;

CREATE TABLE configuracion_disciplinaria (
	id serial4 NOT NULL,
	tipo_novedad varchar(20) NOT NULL,
	cantidad_para_citacion int4 NOT NULL,
	activo bool DEFAULT true NULL,
	CONSTRAINT configuracion_disciplinaria_cantidad_para_citacion_check CHECK ((cantidad_para_citacion > 0)),
	CONSTRAINT configuracion_disciplinaria_pkey PRIMARY KEY (id),
	CONSTRAINT configuracion_disciplinaria_tipo_novedad_key UNIQUE (tipo_novedad)
);


-- public.escala_evaluacion definition

-- Drop table

-- DROP TABLE escala_evaluacion;

CREATE TABLE escala_evaluacion (
	id serial4 NOT NULL,
	nombre varchar(20) NOT NULL,
	nota_min numeric(3, 2) NOT NULL,
	nota_max numeric(3, 2) NOT NULL,
	CONSTRAINT escala_evaluacion_pkey PRIMARY KEY (id)
);


-- public.examenes definition

-- Drop table

-- DROP TABLE examenes;

CREATE TABLE examenes (
	id serial4 NOT NULL,
	titulo varchar(200) NOT NULL,
	descripcion text NULL,
	tiempo_limite_minutos int4 DEFAULT 60 NULL,
	activo bool DEFAULT true NULL,
	fecha_creacion timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT examenes_pkey PRIMARY KEY (id)
);


-- public.materias definition

-- Drop table

-- DROP TABLE materias;

CREATE TABLE materias (
	id serial4 NOT NULL,
	nombre varchar(100) NOT NULL,
	CONSTRAINT materias_pkey PRIMARY KEY (id)
);


-- public.periodos definition

-- Drop table

-- DROP TABLE periodos;

CREATE TABLE periodos (
	id serial4 NOT NULL,
	nombre varchar(50) NOT NULL,
	anio_lectivo int4 NULL,
	fecha_inicio date NULL,
	fecha_fin date NULL,
	activo bool NULL,
	CONSTRAINT periodos_pkey PRIMARY KEY (id)
);


-- public.resultados_examen definition

-- Drop table

-- DROP TABLE resultados_examen;

CREATE TABLE resultados_examen (
	id serial4 NOT NULL,
	estudiante_id int4 NOT NULL,
	examen_id int4 NOT NULL,
	materia_id int4 NOT NULL,
	nota_numerica numeric(3, 2) NULL,
	nivel public.nivel_desempeno NULL,
	fecha timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT resultado_unico_estudiante_examen UNIQUE (estudiante_id, examen_id),
	CONSTRAINT resultados_examen_pkey PRIMARY KEY (id)
);

-- Table Triggers

create trigger trigger_calcular_nivel before
insert
    or
update
    on
    public.resultados_examen for each row execute function calcular_nivel_desempeno();


-- public.areas_gestion definition

-- Drop table

-- DROP TABLE areas_gestion;

CREATE TABLE areas_gestion (
	id serial4 NOT NULL,
	colegio_id int4 NOT NULL,
	nombre varchar(100) NOT NULL,
	porcentaje numeric(5, 2) NOT NULL,
	activo bool DEFAULT true NULL,
	fecha_creacion timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT areas_gestion_pkey PRIMARY KEY (id),
	CONSTRAINT porcentaje_valido CHECK (((porcentaje > (0)::numeric) AND (porcentaje <= (100)::numeric))),
	CONSTRAINT fk_area_colegio FOREIGN KEY (colegio_id) REFERENCES colegios(id) ON DELETE CASCADE
);


-- public.competencias definition

-- Drop table

-- DROP TABLE competencias;

CREATE TABLE competencias (
	id serial4 NOT NULL,
	area_id int4 NOT NULL,
	nombre varchar(150) NOT NULL,
	descripcion text NULL,
	activo bool DEFAULT true NULL,
	fecha_creacion timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	orden int4 DEFAULT 1 NOT NULL,
	CONSTRAINT competencias_pkey PRIMARY KEY (id),
	CONSTRAINT unica_competencia_por_area UNIQUE (area_id, nombre),
	CONSTRAINT unico_orden_por_area UNIQUE (area_id, orden),
	CONSTRAINT fk_competencia_area FOREIGN KEY (area_id) REFERENCES areas_gestion(id) ON DELETE CASCADE
);


-- public.competencias_materia definition

-- Drop table

-- DROP TABLE competencias_materia;

CREATE TABLE competencias_materia (
	id serial4 NOT NULL,
	materia_id int4 NOT NULL,
	nombre varchar(150) NULL,
	porcentaje numeric(5, 2) NULL,
	CONSTRAINT competencias_materia_pkey PRIMARY KEY (id),
	CONSTRAINT competencias_materia_materia_id_fkey FOREIGN KEY (materia_id) REFERENCES materias(id)
);


-- public.configuracion_escalamiento definition

-- Drop table

-- DROP TABLE configuracion_escalamiento;

CREATE TABLE configuracion_escalamiento (
	id serial4 NOT NULL,
	usar_tiempo bool DEFAULT false NULL,
	dias_evaluacion int4 DEFAULT 30 NULL,
	cantidad_tipo2 int4 DEFAULT 3 NULL,
	institucion_id int4 NOT NULL,
	CONSTRAINT configuracion_escalamiento_pkey PRIMARY KEY (id),
	CONSTRAINT unique_institucion UNIQUE (institucion_id),
	CONSTRAINT fk_config_escalamiento_colegio FOREIGN KEY (institucion_id) REFERENCES colegios(id) ON DELETE CASCADE
);


-- public.contribuciones definition

-- Drop table

-- DROP TABLE contribuciones;

CREATE TABLE contribuciones (
	id serial4 NOT NULL,
	competencia_id int4 NOT NULL,
	descripcion text NOT NULL,
	activo bool DEFAULT true NULL,
	fecha_creacion timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	orden int4 DEFAULT 1 NOT NULL,
	CONSTRAINT contribuciones_pkey PRIMARY KEY (id),
	CONSTRAINT unico_orden_por_competencia UNIQUE (competencia_id, orden),
	CONSTRAINT fk_contribucion_competencia FOREIGN KEY (competencia_id) REFERENCES competencias(id) ON DELETE CASCADE
);


-- public.indicadores_logro definition

-- Drop table

-- DROP TABLE indicadores_logro;

CREATE TABLE indicadores_logro (
	id serial4 NOT NULL,
	competencia_materia_id int4 NOT NULL,
	descripcion text NULL,
	CONSTRAINT indicadores_logro_pkey PRIMARY KEY (id),
	CONSTRAINT fk_indicador_competencia_materia FOREIGN KEY (competencia_materia_id) REFERENCES competencias_materia(id) ON DELETE CASCADE
);


-- public.periodos_academicos definition

-- Drop table

-- DROP TABLE periodos_academicos;

CREATE TABLE periodos_academicos (
	id serial4 NOT NULL,
	colegio_id int4 NOT NULL,
	nombre varchar(50) NULL,
	fecha_inicio date NULL,
	fecha_fin date NULL,
	activo bool DEFAULT true NULL,
	CONSTRAINT periodos_academicos_pkey PRIMARY KEY (id),
	CONSTRAINT periodos_academicos_colegio_id_fkey FOREIGN KEY (colegio_id) REFERENCES colegios(id)
);


-- public.sedes definition

-- Drop table

-- DROP TABLE sedes;

CREATE TABLE sedes (
	id serial4 NOT NULL,
	colegio_id int4 NOT NULL,
	nombre varchar(150) NOT NULL,
	direccion varchar(255) NULL,
	telefono varchar(30) NULL,
	activo bool DEFAULT true NULL,
	CONSTRAINT sede_colegio_unico UNIQUE (id, colegio_id),
	CONSTRAINT sedes_pkey PRIMARY KEY (id),
	CONSTRAINT fk_sede_colegio FOREIGN KEY (colegio_id) REFERENCES colegios(id) ON DELETE CASCADE
);


-- public.suscripciones definition

-- Drop table

-- DROP TABLE suscripciones;

CREATE TABLE suscripciones (
	id serial4 NOT NULL,
	colegio_id int4 NOT NULL,
	fecha_inicio timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	fecha_fin timestamp NOT NULL,
	en_prueba bool DEFAULT true NULL,
	activo bool DEFAULT true NULL,
	limite_sedes int4 DEFAULT 1 NULL,
	precio_base numeric(10, 2) DEFAULT 0 NULL,
	CONSTRAINT suscripciones_pkey PRIMARY KEY (id),
	CONSTRAINT unico_colegio_suscripcion UNIQUE (colegio_id),
	CONSTRAINT fk_suscripcion_colegio FOREIGN KEY (colegio_id) REFERENCES colegios(id) ON DELETE CASCADE
);


-- public.usuarios definition

-- Drop table

-- DROP TABLE usuarios;

CREATE TABLE usuarios (
	id serial4 NOT NULL,
	email varchar(120) NOT NULL,
	password_hash varchar(256) NOT NULL,
	colegio_id int4 NULL,
	fecha_registro timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	nombre varchar(100) NULL,
	is_active bool DEFAULT true NULL,
	is_approved bool DEFAULT false NULL,
	fecha_aprobacion timestamp NULL,
	failed_attempts int4 DEFAULT 0 NOT NULL,
	locked_until timestamp NULL,
	rol public.rol_usuario NOT NULL,
	sede_id int4 NULL,
	is_superadmin bool DEFAULT false NULL,
	dias_prueba int4 DEFAULT 15 NULL,
	fecha_expiracion timestamp NULL,
	CONSTRAINT usuarios_email_key UNIQUE (email),
	CONSTRAINT usuarios_pkey PRIMARY KEY (id),
	CONSTRAINT fk_usuario_sede_colegio FOREIGN KEY (sede_id,colegio_id) REFERENCES sedes(id,colegio_id),
	CONSTRAINT usuarios_colegio_id_fkey FOREIGN KEY (colegio_id) REFERENCES colegios(id)
);


-- public.acudientes definition

-- Drop table

-- DROP TABLE acudientes;

CREATE TABLE acudientes (
	id serial4 NOT NULL,
	nombre varchar(100) NOT NULL,
	telefono varchar(20) NULL,
	email varchar(120) NOT NULL,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	parentesco varchar(50) NULL,
	usuario_id int4 NULL,
	CONSTRAINT acudientes_email_key UNIQUE (email),
	CONSTRAINT acudientes_pkey PRIMARY KEY (id),
	CONSTRAINT acudientes_usuario_id_unique UNIQUE (usuario_id),
	CONSTRAINT fk_acudiente_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL
);


-- public.docentes definition

-- Drop table

-- DROP TABLE docentes;

CREATE TABLE docentes (
	id serial4 NOT NULL,
	nombre varchar(150) NOT NULL,
	colegio_id int4 NOT NULL,
	documento varchar(20) NULL,
	telefono varchar(20) NULL,
	email varchar(120) NULL,
	activo bool DEFAULT true NULL,
	fecha_creacion timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	usuario_id int4 NULL,
	sede_id int4 NULL,
	CONSTRAINT docentes_pkey PRIMARY KEY (id),
	CONSTRAINT docentes_usuario_id_key UNIQUE (usuario_id),
	CONSTRAINT fk_colegio FOREIGN KEY (colegio_id) REFERENCES colegios(id),
	CONSTRAINT fk_docente_sede FOREIGN KEY (sede_id) REFERENCES sedes(id) ON DELETE RESTRICT,
	CONSTRAINT fk_docente_sede_colegio FOREIGN KEY (sede_id,colegio_id) REFERENCES sedes(id,colegio_id),
	CONSTRAINT fk_docente_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);


-- public.jornadas_colegio definition

-- Drop table

-- DROP TABLE jornadas_colegio;

CREATE TABLE jornadas_colegio (
	id serial4 NOT NULL,
	colegio_id int4 NOT NULL,
	nombre varchar(50) NOT NULL,
	hora_inicio time NOT NULL,
	hora_fin time NOT NULL,
	activo bool DEFAULT true NULL,
	tolerancia_minutos int4 DEFAULT 0 NULL,
	sede_id int4 NULL,
	CONSTRAINT chk_horario_valido CHECK ((hora_inicio < hora_fin)),
	CONSTRAINT jornadas_colegio_pkey PRIMARY KEY (id),
	CONSTRAINT unique_jornada_colegio UNIQUE (colegio_id, id),
	CONSTRAINT unique_jornada_nombre_por_colegio UNIQUE (colegio_id, nombre),
	CONSTRAINT fk_jornada_colegio FOREIGN KEY (colegio_id) REFERENCES colegios(id) ON DELETE CASCADE,
	CONSTRAINT fk_jornada_sede FOREIGN KEY (sede_id) REFERENCES sedes(id)
);
CREATE UNIQUE INDEX unique_jornada_colegio_lower ON public.jornadas_colegio USING btree (colegio_id, lower((nombre)::text));


-- public.permisos definition

-- Drop table

-- DROP TABLE permisos;

CREATE TABLE permisos (
	id serial4 NOT NULL,
	docente_id int4 NOT NULL,
	fecha_inicio date NOT NULL,
	fecha_fin date NOT NULL,
	tipo varchar(100) NOT NULL,
	observacion text NULL,
	colegio_id int4 NOT NULL,
	activo bool DEFAULT true NULL,
	CONSTRAINT chk_permiso_fechas CHECK ((fecha_fin >= fecha_inicio)),
	CONSTRAINT permisos_pkey PRIMARY KEY (id),
	CONSTRAINT fk_colegio FOREIGN KEY (colegio_id) REFERENCES colegios(id),
	CONSTRAINT fk_docente FOREIGN KEY (docente_id) REFERENCES docentes(id)
);


-- public.sede_coordinadores definition

-- Drop table

-- DROP TABLE sede_coordinadores;

CREATE TABLE sede_coordinadores (
	id serial4 NOT NULL,
	sede_id int4 NOT NULL,
	docente_id int4 NOT NULL,
	cargo varchar(100) NOT NULL,
	activo bool DEFAULT true NULL,
	CONSTRAINT sede_coordinadores_pkey PRIMARY KEY (id),
	CONSTRAINT sede_coordinadores_docente_id_fkey FOREIGN KEY (docente_id) REFERENCES docentes(id) ON DELETE CASCADE,
	CONSTRAINT sede_coordinadores_sede_id_fkey FOREIGN KEY (sede_id) REFERENCES sedes(id) ON DELETE CASCADE
);


-- public.tokens_activacion definition

-- Drop table

-- DROP TABLE tokens_activacion;

CREATE TABLE tokens_activacion (
	id serial4 NOT NULL,
	usuario_id int4 NOT NULL,
	"token" varchar(120) NOT NULL,
	fecha_expiracion timestamp NOT NULL,
	usado bool DEFAULT false NULL,
	CONSTRAINT tokens_activacion_pkey PRIMARY KEY (id),
	CONSTRAINT tokens_activacion_token_key UNIQUE (token),
	CONSTRAINT tokens_activacion_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);


-- public.acuerdos_evaluacion definition

-- Drop table

-- DROP TABLE acuerdos_evaluacion;

CREATE TABLE acuerdos_evaluacion (
	id serial4 NOT NULL,
	docente_id int4 NOT NULL,
	colegio_id int4 NOT NULL,
	anio int4 NOT NULL,
	estado varchar(20) DEFAULT 'BORRADOR'::character varying NULL,
	fecha_creacion timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT acuerdos_pkey PRIMARY KEY (id),
	CONSTRAINT unico_docente_anio UNIQUE (docente_id, anio),
	CONSTRAINT fk_acuerdo_colegio FOREIGN KEY (colegio_id) REFERENCES colegios(id) ON DELETE CASCADE,
	CONSTRAINT fk_acuerdo_docente FOREIGN KEY (docente_id) REFERENCES docentes(id) ON DELETE CASCADE
);


-- public.clases definition

-- Drop table

-- DROP TABLE clases;

CREATE TABLE clases (
	id serial4 NOT NULL,
	docente_id int4 NOT NULL,
	colegio_id int4 NOT NULL,
	grado varchar(20) NOT NULL,
	grupo varchar(10) NOT NULL,
	materia varchar(100) NOT NULL,
	hora_inicio time NOT NULL,
	hora_fin time NOT NULL,
	activo bool DEFAULT true NULL,
	dia public.dia_semana NOT NULL,
	materia_id int4 NULL,
	CONSTRAINT clases_pkey PRIMARY KEY (id),
	CONSTRAINT horario_unico UNIQUE (docente_id, dia, hora_inicio, hora_fin),
	CONSTRAINT clases_materia_id_fkey FOREIGN KEY (materia_id) REFERENCES materias(id),
	CONSTRAINT fk_clase_docente FOREIGN KEY (docente_id) REFERENCES docentes(id) ON DELETE CASCADE
);


-- public.criterios_evaluacion definition

-- Drop table

-- DROP TABLE criterios_evaluacion;

CREATE TABLE criterios_evaluacion (
	id serial4 NOT NULL,
	acuerdo_id int4 NOT NULL,
	contribucion_id int4 NOT NULL,
	descripcion text NOT NULL,
	fecha_creacion timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT criterios_pkey PRIMARY KEY (id),
	CONSTRAINT fk_criterio_acuerdo FOREIGN KEY (acuerdo_id) REFERENCES acuerdos_evaluacion(id) ON DELETE CASCADE,
	CONSTRAINT fk_criterio_contribucion FOREIGN KEY (contribucion_id) REFERENCES contribuciones(id) ON DELETE CASCADE
);
CREATE INDEX idx_criterio_acuerdo ON public.criterios_evaluacion USING btree (acuerdo_id);

-- Table Triggers

create trigger trg_bloquear_criterios before
insert
    or
delete
    or
update
    on
    public.criterios_evaluacion for each row execute function bloquear_criterios_si_cerrado();


-- public.estudiantes definition

-- Drop table

-- DROP TABLE estudiantes;

CREATE TABLE estudiantes (
	id serial4 NOT NULL,
	colegio_id int4 NOT NULL,
	docente_id int4 NOT NULL,
	nombre varchar(150) NOT NULL,
	grado varchar(20) NULL,
	grupo varchar(20) NULL,
	activo bool DEFAULT true NULL,
	fecha_creacion timestamp DEFAULT now() NULL,
	usuario_id int4 NULL,
	qr_token varchar(80) NULL,
	jornada_id int4 NOT NULL,
	institucion_id int4 NULL,
	sede_id int4 NULL,
	CONSTRAINT estudiantes_pkey PRIMARY KEY (id),
	CONSTRAINT estudiantes_qr_token_key UNIQUE (qr_token),
	CONSTRAINT estudiantes_usuario_id_unique UNIQUE (usuario_id),
	CONSTRAINT fk_estudiante_colegio FOREIGN KEY (colegio_id) REFERENCES colegios(id) ON DELETE CASCADE,
	CONSTRAINT fk_estudiante_docente FOREIGN KEY (docente_id) REFERENCES docentes(id) ON DELETE RESTRICT,
	CONSTRAINT fk_estudiante_jornada FOREIGN KEY (colegio_id,jornada_id) REFERENCES jornadas_colegio(colegio_id,id) ON DELETE RESTRICT,
	CONSTRAINT fk_estudiante_sede FOREIGN KEY (sede_id) REFERENCES sedes(id) ON DELETE RESTRICT,
	CONSTRAINT fk_estudiante_sede_colegio FOREIGN KEY (sede_id,colegio_id) REFERENCES sedes(id,colegio_id),
	CONSTRAINT fk_estudiante_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL
);


-- public.evaluacion_final definition

-- Drop table

-- DROP TABLE evaluacion_final;

CREATE TABLE evaluacion_final (
	id serial4 NOT NULL,
	acuerdo_id int4 NOT NULL,
	fecha_cierre timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	estado varchar(20) DEFAULT 'ABIERTO'::character varying NULL,
	observaciones_finales text NULL,
	CONSTRAINT evaluacion_final_pkey PRIMARY KEY (id),
	CONSTRAINT unica_evaluacion_por_acuerdo UNIQUE (acuerdo_id),
	CONSTRAINT fk_eval_acuerdo FOREIGN KEY (acuerdo_id) REFERENCES acuerdos_evaluacion(id) ON DELETE CASCADE
);


-- public.evaluaciones_estudiante definition

-- Drop table

-- DROP TABLE evaluaciones_estudiante;

CREATE TABLE evaluaciones_estudiante (
	id serial4 NOT NULL,
	estudiante_id int4 NULL,
	indicador_id int4 NULL,
	periodo_id int4 NULL,
	calificacion numeric(4, 2) NULL,
	observacion text NULL,
	CONSTRAINT evaluaciones_estudiante_pkey PRIMARY KEY (id),
	CONSTRAINT evaluaciones_estudiante_estudiante_id_fkey FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id),
	CONSTRAINT evaluaciones_estudiante_indicador_id_fkey FOREIGN KEY (indicador_id) REFERENCES indicadores_logro(id) ON DELETE CASCADE,
	CONSTRAINT evaluaciones_estudiante_periodo_id_fkey FOREIGN KEY (periodo_id) REFERENCES periodos_academicos(id)
);


-- public.evidencias definition

-- Drop table

-- DROP TABLE evidencias;

CREATE TABLE evidencias (
	id serial4 NOT NULL,
	criterio_id int4 NOT NULL,
	descripcion text NOT NULL,
	tipo varchar(20) NOT NULL,
	url text NULL,
	aprobado bool DEFAULT false NULL,
	observacion_admin text NULL,
	fecha_creacion timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT evidencias_pkey PRIMARY KEY (id),
	CONSTRAINT fk_evidencia_criterio FOREIGN KEY (criterio_id) REFERENCES criterios_evaluacion(id) ON DELETE CASCADE
);


-- public.ingresos_colegio definition

-- Drop table

-- DROP TABLE ingresos_colegio;

CREATE TABLE ingresos_colegio (
	id serial4 NOT NULL,
	estudiante_id int4 NOT NULL,
	colegio_id int4 NOT NULL,
	fecha date DEFAULT CURRENT_DATE NOT NULL,
	hora time DEFAULT CURRENT_TIME NOT NULL,
	metodo varchar(20) DEFAULT 'QR'::character varying NULL,
	creado_en timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	tipo_evento public.tipo_evento_colegio DEFAULT 'ingreso'::tipo_evento_colegio NULL,
	CONSTRAINT ingresos_colegio_pkey PRIMARY KEY (id),
	CONSTRAINT fk_ingreso_colegio FOREIGN KEY (colegio_id) REFERENCES colegios(id) ON DELETE CASCADE,
	CONSTRAINT fk_ingreso_estudiante FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE CASCADE
);
CREATE UNIQUE INDEX unico_evento_por_dia ON public.ingresos_colegio USING btree (estudiante_id, fecha, tipo_evento);


-- public.novedades definition

-- Drop table

-- DROP TABLE novedades;

CREATE TABLE novedades (
	id serial4 NOT NULL,
	estudiante_id int4 NOT NULL,
	tipo_novedad public.tipo_novedad_enum NOT NULL,
	informe text NOT NULL,
	fecha date DEFAULT CURRENT_DATE NOT NULL,
	hora time DEFAULT CURRENT_TIME NOT NULL,
	registrada_por int4 NULL,
	categoria varchar(20) NULL,
	gravedad public.tipo_gravedad NOT NULL,
	CONSTRAINT novedades_pkey PRIMARY KEY (id),
	CONSTRAINT fk_estudiante FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE CASCADE
);

-- Table Triggers

create trigger trg_citacion_automatica after
insert
    on
    public.novedades for each row execute function fn_generar_citacion_automatica();
create trigger trg_citacion_piar_tipo2 after
insert
    on
    public.novedades for each row execute function fn_citacion_piar_tipo2();
create trigger trg_escalamiento_tipo2 before
insert
    on
    public.novedades for each row execute function fn_escalamiento_tipo2_a_tipo3();


-- public.piar definition

-- Drop table

-- DROP TABLE piar;

CREATE TABLE piar (
	id serial4 NOT NULL,
	estudiante_id int4 NOT NULL,
	diagnostico text NULL,
	objetivos text NULL,
	fecha_inicio date NULL,
	fecha_fin date NULL,
	activo bool DEFAULT true NULL,
	CONSTRAINT piar_pkey PRIMARY KEY (id),
	CONSTRAINT piar_estudiante_id_fkey FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE CASCADE
);
CREATE UNIQUE INDEX unico_piar_activo ON public.piar USING btree (estudiante_id) WHERE (activo = true);


-- public.respuestas_novedad definition

-- Drop table

-- DROP TABLE respuestas_novedad;

CREATE TABLE respuestas_novedad (
	id serial4 NOT NULL,
	novedad_id int4 NOT NULL,
	usuario_id int4 NULL,
	rol public.rol_usuario NOT NULL,
	mensaje text NOT NULL,
	fecha timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT respuestas_novedad_pkey PRIMARY KEY (id),
	CONSTRAINT fk_respuesta_novedad FOREIGN KEY (novedad_id) REFERENCES novedades(id) ON DELETE CASCADE,
	CONSTRAINT fk_respuesta_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL
);


-- public.seguimientos definition

-- Drop table

-- DROP TABLE seguimientos;

CREATE TABLE seguimientos (
	id serial4 NOT NULL,
	acuerdo_id int4 NOT NULL,
	observaciones text NOT NULL,
	recomendaciones text NOT NULL,
	fecha timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT seguimientos_pkey PRIMARY KEY (id),
	CONSTRAINT fk_seguimiento_acuerdo FOREIGN KEY (acuerdo_id) REFERENCES acuerdos_evaluacion(id) ON DELETE CASCADE
);


-- public.acuerdos_correctivos definition

-- Drop table

-- DROP TABLE acuerdos_correctivos;

CREATE TABLE acuerdos_correctivos (
	id serial4 NOT NULL,
	novedad_id int4 NOT NULL,
	estudiante_id int4 NOT NULL,
	descripcion text NOT NULL,
	compromiso text NULL,
	fecha timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	estado varchar(20) DEFAULT 'ACTIVO'::character varying NULL,
	CONSTRAINT acuerdos_correctivos_pkey PRIMARY KEY (id),
	CONSTRAINT unica_novedad_acuerdo UNIQUE (novedad_id),
	CONSTRAINT fk_acuerdo_estudiante FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE CASCADE,
	CONSTRAINT fk_acuerdo_novedad FOREIGN KEY (novedad_id) REFERENCES novedades(id) ON DELETE CASCADE
);


-- public.ajustes_razonables definition

-- Drop table

-- DROP TABLE ajustes_razonables;

CREATE TABLE ajustes_razonables (
	id serial4 NOT NULL,
	piar_id int4 NOT NULL,
	descripcion text NOT NULL,
	aplicado bool DEFAULT false NULL,
	fecha_aplicacion date NULL,
	CONSTRAINT ajustes_razonables_pkey PRIMARY KEY (id),
	CONSTRAINT ajustes_razonables_piar_id_fkey FOREIGN KEY (piar_id) REFERENCES piar(id) ON DELETE CASCADE
);


-- public.alertas definition

-- Drop table

-- DROP TABLE alertas;

CREATE TABLE alertas (
	id serial4 NOT NULL,
	estudiante_id int4 NOT NULL,
	tipo varchar(50) NOT NULL,
	descripcion text NOT NULL,
	fecha timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	atendida bool DEFAULT false NULL,
	CONSTRAINT alertas_pkey PRIMARY KEY (id),
	CONSTRAINT fk_alerta_estudiante FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE CASCADE
);
CREATE UNIQUE INDEX unica_alerta_activa ON public.alertas USING btree (estudiante_id, tipo) WHERE (atendida = false);


-- public.asistencias definition

-- Drop table

-- DROP TABLE asistencias;

CREATE TABLE asistencias (
	id serial4 NOT NULL,
	estudiante_id int4 NOT NULL,
	clase_id int4 NOT NULL,
	fecha date NOT NULL,
	estado varchar(20) NOT NULL,
	observacion text NULL,
	registrada_por int4 NULL,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT asistencias_pkey PRIMARY KEY (id),
	CONSTRAINT unica_asistencia_por_clase UNIQUE (estudiante_id, clase_id, fecha),
	CONSTRAINT fk_asistencia_clase FOREIGN KEY (clase_id) REFERENCES clases(id) ON DELETE CASCADE,
	CONSTRAINT fk_asistencia_estudiante FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE CASCADE
);


-- public.citaciones_acudiente definition

-- Drop table

-- DROP TABLE citaciones_acudiente;

CREATE TABLE citaciones_acudiente (
	id serial4 NOT NULL,
	estudiante_id int4 NOT NULL,
	acudiente_id int4 NOT NULL,
	novedad_id int4 NULL,
	motivo text NOT NULL,
	fecha_citacion timestamp NOT NULL,
	estado varchar(20) DEFAULT 'pendiente'::character varying NULL,
	observaciones text NULL,
	tipo_origen varchar(50) NULL,
	fecha date DEFAULT CURRENT_DATE NULL,
	CONSTRAINT citaciones_acudiente_pkey PRIMARY KEY (id),
	CONSTRAINT citaciones_acudiente_acudiente_id_fkey FOREIGN KEY (acudiente_id) REFERENCES acudientes(id) ON DELETE CASCADE,
	CONSTRAINT citaciones_acudiente_estudiante_id_fkey FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE CASCADE,
	CONSTRAINT citaciones_acudiente_novedad_id_fkey FOREIGN KEY (novedad_id) REFERENCES novedades(id) ON DELETE SET NULL
);
CREATE UNIQUE INDEX unique_citacion_por_novedad ON public.citaciones_acudiente USING btree (novedad_id, tipo_origen) WHERE (tipo_origen IS NOT NULL);
CREATE UNIQUE INDEX unique_citacion_por_tipo ON public.citaciones_acudiente USING btree (estudiante_id, tipo_origen) WHERE (tipo_origen IS NOT NULL);


-- public.clase_estudiantes definition

-- Drop table

-- DROP TABLE clase_estudiantes;

CREATE TABLE clase_estudiantes (
	id serial4 NOT NULL,
	clase_id int4 NOT NULL,
	estudiante_id int4 NOT NULL,
	CONSTRAINT clase_estudiantes_pkey PRIMARY KEY (id),
	CONSTRAINT unica_matricula UNIQUE (clase_id, estudiante_id),
	CONSTRAINT fk_ce_clase FOREIGN KEY (clase_id) REFERENCES clases(id) ON DELETE CASCADE,
	CONSTRAINT fk_ce_estudiante FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE CASCADE
);


-- public.descargos_estudiante definition

-- Drop table

-- DROP TABLE descargos_estudiante;

CREATE TABLE descargos_estudiante (
	id serial4 NOT NULL,
	novedad_id int4 NOT NULL,
	estudiante_id int4 NOT NULL,
	descripcion text NOT NULL,
	fecha timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT descargos_estudiante_pkey PRIMARY KEY (id),
	CONSTRAINT fk_descargo_estudiante FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE CASCADE,
	CONSTRAINT fk_descargo_novedad FOREIGN KEY (novedad_id) REFERENCES novedades(id) ON DELETE CASCADE
);


-- public.estudiante_acudiente definition

-- Drop table

-- DROP TABLE estudiante_acudiente;

CREATE TABLE estudiante_acudiente (
	id serial4 NOT NULL,
	estudiante_id int4 NOT NULL,
	acudiente_id int4 NOT NULL,
	CONSTRAINT estudiante_acudiente_pkey PRIMARY KEY (id),
	CONSTRAINT unica_relacion UNIQUE (estudiante_id, acudiente_id),
	CONSTRAINT fk_ea_acudiente FOREIGN KEY (acudiente_id) REFERENCES acudientes(id) ON DELETE CASCADE,
	CONSTRAINT fk_ea_estudiante FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE CASCADE
);


-- public.evaluacion_criterio definition

-- Drop table

-- DROP TABLE evaluacion_criterio;

CREATE TABLE evaluacion_criterio (
	id serial4 NOT NULL,
	evaluacion_final_id int4 NOT NULL,
	criterio_id int4 NOT NULL,
	calificacion numeric(4, 2) NOT NULL,
	observacion text NULL,
	CONSTRAINT chk_calificacion_valida CHECK (((calificacion >= (0)::numeric) AND (calificacion <= (5)::numeric))),
	CONSTRAINT evaluacion_criterio_pkey PRIMARY KEY (id),
	CONSTRAINT unica_eval_por_criterio UNIQUE (evaluacion_final_id, criterio_id),
	CONSTRAINT fk_evalcriterio_criterio FOREIGN KEY (criterio_id) REFERENCES criterios_evaluacion(id) ON DELETE CASCADE,
	CONSTRAINT fk_evalcriterio_evalfinal FOREIGN KEY (evaluacion_final_id) REFERENCES evaluacion_final(id) ON DELETE CASCADE
);
CREATE INDEX idx_evalcriterio_evalfinal ON public.evaluacion_criterio USING btree (evaluacion_final_id);


-- public.justificaciones_acudiente definition

-- Drop table

-- DROP TABLE justificaciones_acudiente;

CREATE TABLE justificaciones_acudiente (
	id serial4 NOT NULL,
	novedad_id int4 NOT NULL,
	acudiente_id int4 NOT NULL,
	justificacion text NOT NULL,
	fecha timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT justificaciones_acudiente_novedad_id_key UNIQUE (novedad_id),
	CONSTRAINT justificaciones_acudiente_pkey PRIMARY KEY (id),
	CONSTRAINT justificaciones_acudiente_acudiente_id_fkey FOREIGN KEY (acudiente_id) REFERENCES acudientes(id) ON DELETE CASCADE,
	CONSTRAINT justificaciones_acudiente_novedad_id_fkey FOREIGN KEY (novedad_id) REFERENCES novedades(id) ON DELETE CASCADE
);



-- DROP FUNCTION public.bloquear_criterios_si_cerrado();

CREATE OR REPLACE FUNCTION public.bloquear_criterios_si_cerrado()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
DECLARE
    estado_acuerdo varchar;
BEGIN
    SELECT estado INTO estado_acuerdo
    FROM acuerdos_evaluacion
    WHERE id = NEW.acuerdo_id;

    IF estado_acuerdo = 'CERRADO' THEN
        RAISE EXCEPTION 'No se pueden modificar criterios de un acuerdo cerrado';
    END IF;

    RETURN NEW;
END;
$function$
;

-- DROP FUNCTION public.calcular_nivel_desempeno();

CREATE OR REPLACE FUNCTION public.calcular_nivel_desempeno()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN

    IF NEW.nota_numerica < 3.0 THEN
        NEW.nivel := 'Bajo';

    ELSIF NEW.nota_numerica < 3.9 THEN
        NEW.nivel := 'Basico';

    ELSIF NEW.nota_numerica < 4.6 THEN
        NEW.nivel := 'Alto';

    ELSE
        NEW.nivel := 'Superior';

    END IF;

    RETURN NEW;

END;
$function$
;

-- DROP FUNCTION public.fn_boletin_estudiante(int4, int4);

CREATE OR REPLACE FUNCTION public.fn_boletin_estudiante(p_estudiante_id integer, p_periodo_id integer)
 RETURNS TABLE(materia text, promedio numeric, nivel text)
 LANGUAGE plpgsql
AS $function$
BEGIN

RETURN QUERY

WITH base AS (
    SELECT 
        m.nombre AS materia,
        e.calificacion
    FROM evaluaciones_estudiante e
    JOIN indicadores_logro il ON e.indicador_id = il.id
    JOIN competencias_materia cm ON il.competencia_id = cm.id
    JOIN materias m ON cm.materia_id = m.id
    WHERE e.estudiante_id = p_estudiante_id
      AND e.periodo_id = p_periodo_id
),

promedios AS (
    SELECT 
        materia,
        AVG(calificacion) AS promedio
    FROM base
    GROUP BY materia
)

SELECT 
    materia,
    ROUND(promedio, 2),
    CASE
        WHEN promedio < 3.0 THEN 'Bajo'
        WHEN promedio < 3.9 THEN 'Básico'
        WHEN promedio < 4.6 THEN 'Alto'
        ELSE 'Superior'
    END
FROM promedios;

END;
$function$
;

-- DROP FUNCTION public.fn_boletin_estudiante_pro(int4, int4);

CREATE OR REPLACE FUNCTION public.fn_boletin_estudiante_pro(p_estudiante_id integer, p_periodo_id integer)
 RETURNS TABLE(materia text, promedio_materia numeric, ponderado numeric, total numeric, nivel text)
 LANGUAGE plpgsql
AS $function$
BEGIN

RETURN QUERY

WITH base AS (
    SELECT 
        m.id AS materia_id,
        m.nombre AS materia,
        cm.id AS competencia_id,
        cm.porcentaje,
        e.calificacion
    FROM evaluaciones_estudiante e
    JOIN indicadores_logro il ON e.indicador_id = il.id
    JOIN competencias_materia cm ON il.competencia_id = cm.id
    JOIN materias m ON cm.materia_id = m.id
    WHERE e.estudiante_id = p_estudiante_id
      AND e.periodo_id = p_periodo_id
),

prom_competencia AS (
    SELECT 
        materia_id,
        materia,
        competencia_id,
        porcentaje,
        AVG(calificacion) AS prom_comp
    FROM base
    GROUP BY materia_id, materia, competencia_id, porcentaje
),

prom_materia AS (
    SELECT 
        materia_id,
        materia,
        SUM(prom_comp * porcentaje / 100.0) AS promedio_materia
    FROM prom_competencia
    GROUP BY materia_id, materia
),

total_final AS (
    SELECT AVG(promedio_materia) AS total
    FROM prom_materia
)

SELECT 
    pm.materia,
    ROUND(pm.promedio_materia, 2),
    ROUND(pm.promedio_materia, 2), -- puedes ajustar ponderación después
    ROUND(tf.total, 2),
    CASE
        WHEN tf.total < 3.0 THEN 'Bajo'
        WHEN tf.total < 3.9 THEN 'Básico'
        WHEN tf.total < 4.6 THEN 'Alto'
        ELSE 'Superior'
    END
FROM prom_materia pm
CROSS JOIN total_final tf;

END;
$function$
;

-- DROP FUNCTION public.fn_citacion_piar_tipo2();

CREATE OR REPLACE FUNCTION public.fn_citacion_piar_tipo2()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
DECLARE
    tiene_piar BOOLEAN;
    cantidad_tipo2 INT;
    acudiente INT;
BEGIN

    -- Solo aplica si es Tipo 2
    IF NEW.gravedad != 'Tipo 2' THEN
        RETURN NEW;
    END IF;

    -- Verificar PIAR activo
    SELECT EXISTS (
        SELECT 1 FROM piar 
        WHERE estudiante_id = NEW.estudiante_id
          AND activo = true
    ) INTO tiene_piar;

    IF NOT tiene_piar THEN
        RETURN NEW;
    END IF;

    -- Contar Tipo 2 acumulados
    SELECT COUNT(*) 
    INTO cantidad_tipo2
    FROM novedades
    WHERE estudiante_id = NEW.estudiante_id
      AND gravedad = 'Tipo 2';

    -- Obtener acudiente
    SELECT acudiente_id
    INTO acudiente
    FROM estudiante_acudiente
    WHERE estudiante_id = NEW.estudiante_id
    LIMIT 1;

    -- Condición principal
    IF cantidad_tipo2 >= 2 THEN

        -- Validar que NO exista ya citación PIAR_TIPO3
        IF NOT EXISTS (
            SELECT 1 FROM citaciones_acudiente
            WHERE estudiante_id = NEW.estudiante_id
              AND tipo_origen = 'PIAR_TIPO3'
              AND estado = 'pendiente'
        )

        -- Validar que NO exista ya PIAR_TIPO2
        AND NOT EXISTS (
            SELECT 1 FROM citaciones_acudiente
            WHERE estudiante_id = NEW.estudiante_id
              AND tipo_origen = 'PIAR_TIPO2'
              AND estado = 'pendiente'
        ) THEN

            INSERT INTO citaciones_acudiente (
                estudiante_id,
                acudiente_id,
                novedad_id,
                motivo,
                fecha_citacion,
                tipo_origen
            )
            VALUES (
                NEW.estudiante_id,
                acudiente,
                NEW.id,
                'Citación por acumulación Tipo 2 con enfoque de inclusión',
                NOW() + INTERVAL '1 day',
                'PIAR_TIPO2'
            )
            ON CONFLICT DO NOTHING;

        END IF;

    END IF;

    RETURN NEW;
END;
$function$
;

-- DROP FUNCTION public.fn_escalamiento_tipo2_a_tipo3();

CREATE OR REPLACE FUNCTION public.fn_escalamiento_tipo2_a_tipo3()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
DECLARE
    v_cantidad_tipo2 INT;
    v_usar_tiempo BOOLEAN;
    v_dias INT;
    v_cantidad_config INT;
    v_colegio INT;
BEGIN

    -- Solo aplica si es Tipo 2
    IF NEW.gravedad != 'Tipo 2' THEN
        RETURN NEW;
    END IF;

    -- Obtener colegio del estudiante
    SELECT colegio_id
    INTO v_colegio
    FROM estudiantes
    WHERE id = NEW.estudiante_id;

    -- Leer configuración por colegio (🔥 con alias)
    SELECT 
        ce.usar_tiempo,
        ce.dias_evaluacion,
        ce.cantidad_tipo2
    INTO 
        v_usar_tiempo,
        v_dias,
        v_cantidad_config
    FROM configuracion_escalamiento ce
    WHERE ce.institucion_id = v_colegio;

    -- Valores por defecto
    IF v_usar_tiempo IS NULL THEN
        v_usar_tiempo := false;
        v_dias := 30;
        v_cantidad_config := 3;
    END IF;

    -- Contar Tipo 2
    IF v_usar_tiempo THEN

        SELECT COUNT(*)
        INTO v_cantidad_tipo2
        FROM novedades
        WHERE estudiante_id = NEW.estudiante_id
          AND gravedad = 'Tipo 2'
          AND fecha >= NOW() - (v_dias || ' days')::INTERVAL;

    ELSE

        SELECT COUNT(*)
        INTO v_cantidad_tipo2
        FROM novedades
        WHERE estudiante_id = NEW.estudiante_id
          AND gravedad = 'Tipo 2';

    END IF;

    -- Escalamiento
    IF v_cantidad_tipo2 >= v_cantidad_config THEN
        NEW.gravedad := 'Tipo 3';
    END IF;

    RETURN NEW;
END;
$function$
;

-- DROP FUNCTION public.fn_generar_citacion_automatica();

CREATE OR REPLACE FUNCTION public.fn_generar_citacion_automatica()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
DECLARE
    tiene_piar BOOLEAN;
    cantidad_tipo2 INT;
BEGIN

-- 🔎 Verificar PIAR activo
SELECT EXISTS (
    SELECT 1 
    FROM piar 
    WHERE estudiante_id = NEW.estudiante_id 
      AND activo = true
) INTO tiene_piar;

-- 🧠 Contar Tipo 2
SELECT COUNT(*) 
INTO cantidad_tipo2
FROM novedades
WHERE estudiante_id = NEW.estudiante_id
  AND gravedad = 'Tipo 2';

--------------------------------------------------
-- 🔥 REGLA 1: TIPO 3 → CITACIÓN
--------------------------------------------------

IF NEW.gravedad = 'Tipo 3' THEN

    INSERT INTO citaciones_acudiente (
        estudiante_id,
        acudiente_id,
        novedad_id,
        motivo,
        fecha_citacion,
        tipo_origen
    )
    SELECT 
        NEW.estudiante_id,
        ea.acudiente_id,
        NEW.id,
        CASE 
            WHEN tiene_piar 
            THEN 'Citación automática por Tipo 3 con PIAR activo'
            ELSE 'Citación automática por Tipo 3'
        END,
        NOW() + INTERVAL '1 day',
        CASE 
            WHEN tiene_piar THEN 'PIAR_TIPO3'
            ELSE 'TIPO_3'
        END
    FROM estudiante_acudiente ea
    WHERE ea.estudiante_id = NEW.estudiante_id
    ON CONFLICT DO NOTHING;

END IF;

--------------------------------------------------
-- 🔥 REGLA 2: ALERTA PIAR + TIPO 2 ACUMULADO
-- ❗ CON PRIORIDAD (NO SI YA EXISTE PIAR_TIPO3)
--------------------------------------------------

IF tiene_piar AND cantidad_tipo2 >= 2 THEN

    IF NOT EXISTS (
        SELECT 1 FROM alertas
        WHERE estudiante_id = NEW.estudiante_id
          AND tipo = 'ALERTA_PIAR_DISCIPLINA'
          AND atendida = false
    ) THEN

        INSERT INTO alertas (estudiante_id, tipo, descripcion)
        VALUES (
            NEW.estudiante_id,
            'ALERTA_PIAR_TIPO2_ACUMULADO',
            'Estudiante con PIAR y múltiples faltas Tipo 2'
        )
        ON CONFLICT DO NOTHING;

    END IF;

END IF;

--------------------------------------------------

RETURN NEW;

END;
$function$
;

-- DROP FUNCTION public.fn_informe_detalle(int4);

CREATE OR REPLACE FUNCTION public.fn_informe_detalle(p_evaluacion_final_id integer)
 RETURNS TABLE(area_nombre text, competencia_nombre text, contribucion_descripcion text, criterio_descripcion text, calificacion numeric, observacion text)
 LANGUAGE plpgsql
AS $function$
BEGIN

RETURN QUERY

SELECT 
    ag.nombre::TEXT AS area_nombre,
    comp.nombre::TEXT AS competencia_nombre,
    ctr.descripcion::TEXT AS contribucion_descripcion,
    ce.descripcion::TEXT AS criterio_descripcion,
    ec.calificacion,
    ec.observacion
FROM evaluacion_criterio ec
JOIN criterios_evaluacion ce ON ec.criterio_id = ce.id
JOIN contribuciones ctr ON ce.contribucion_id = ctr.id
JOIN competencias comp ON ctr.competencia_id = comp.id
JOIN areas_gestion ag ON comp.area_id = ag.id
WHERE ec.evaluacion_final_id = p_evaluacion_final_id

ORDER BY 
    ag.id,
    comp.orden,
    ctr.orden;

END;
$function$
;

-- DROP FUNCTION public.fn_informe_men(int4);

CREATE OR REPLACE FUNCTION public.fn_informe_men(p_evaluacion_final_id integer)
 RETURNS TABLE(area_nombre text, promedio_area numeric, porcentaje numeric, ponderado numeric, total numeric, nivel text)
 LANGUAGE plpgsql
AS $function$
BEGIN

RETURN QUERY

WITH base AS (
    SELECT 
        ag.nombre::TEXT AS area_nom,
        ag.porcentaje AS porc,
        AVG(ec.calificacion) AS prom_area
    FROM evaluacion_criterio ec
    JOIN criterios_evaluacion ce ON ec.criterio_id = ce.id
    JOIN contribuciones c ON ce.contribucion_id = c.id
    JOIN competencias comp ON c.competencia_id = comp.id
    JOIN areas_gestion ag ON comp.area_id = ag.id
    WHERE ec.evaluacion_final_id = p_evaluacion_final_id
    GROUP BY ag.nombre, ag.porcentaje
),

calc AS (
    SELECT 
        area_nom,
        prom_area,
        porc,
        (prom_area * porc / 100.0) AS pond
    FROM base
),

total_final AS (
    SELECT SUM(pond) AS total FROM calc
)

SELECT 
    c.area_nom,
    c.prom_area,
    c.porc,
    c.pond,
    t.total,
    CASE
        WHEN t.total < 3.0 THEN 'Bajo'
        WHEN t.total < 3.9 THEN 'Básico'
        WHEN t.total < 4.6 THEN 'Alto'
        ELSE 'Superior'
    END
FROM calc c
CROSS JOIN total_final t;

END;
$function$
;

-- DROP FUNCTION public.generar_codigo_colegio();

CREATE OR REPLACE FUNCTION public.generar_codigo_colegio()
 RETURNS text
 LANGUAGE plpgsql
AS $function$
DECLARE
    caracteres TEXT := 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
    codigo TEXT := '';
    i INT;
BEGIN
    FOR i IN 1..5 LOOP
        codigo := codigo || substr(caracteres, floor(random()*length(caracteres)+1)::int, 1);
    END LOOP;

    RETURN 'COL-' || codigo;
END;
$function$
;

-- DROP FUNCTION public.get_informe_men(int4);

CREATE OR REPLACE FUNCTION public.get_informe_men(p_evaluacion_final_id integer)
 RETURNS TABLE(area character varying, porcentaje numeric, promedio_area numeric, ponderado numeric, total numeric, nivel character varying)
 LANGUAGE plpgsql
AS $function$
BEGIN
    RETURN QUERY

    WITH base AS (
        SELECT 
            ec.calificacion,
            comp.id AS competencia_id,
            comp.nombre AS competencia,
            a.id AS area_id,
            a.nombre AS area_nombre,
            a.porcentaje
        FROM evaluacion_criterio ec
        JOIN criterios_evaluacion c ON ec.criterio_id = c.id
        JOIN contribuciones ctr ON c.contribucion_id = ctr.id
        JOIN competencias comp ON ctr.competencia_id = comp.id
        JOIN areas_gestion a ON comp.area_id = a.id
        WHERE ec.evaluacion_final_id = p_evaluacion_final_id
    ),

    prom_competencia AS (
        SELECT 
            competencia_id,
            competencia,
            area_id,
            area_nombre,
            porcentaje,
            AVG(calificacion) AS promedio_competencia
        FROM base
        GROUP BY competencia_id, competencia, area_id, area_nombre, porcentaje
    ),

    prom_area AS (
        SELECT 
            area_id,
            area_nombre,
            porcentaje,
            AVG(promedio_competencia) AS promedio_area
        FROM prom_competencia
        GROUP BY area_id, area_nombre, porcentaje
    ),

    total_final AS (
        SELECT 
            SUM(promedio_area * porcentaje / 100.0) AS total
        FROM prom_area
    )

    SELECT 
        pa.area_nombre,  -- 🔥 aquí evitamos el conflicto
        pa.porcentaje,
        ROUND(pa.promedio_area, 2),
        ROUND(pa.promedio_area * pa.porcentaje / 100.0, 2),
        ROUND(tf.total, 2),
        CASE
            WHEN tf.total < 3.0 THEN 'Bajo'
            WHEN tf.total < 3.9 THEN 'Basico'
            WHEN tf.total < 4.6 THEN 'Alto'
            ELSE 'Superior'
        END
    FROM prom_area pa
    CROSS JOIN total_final tf;

END;
$function$
;