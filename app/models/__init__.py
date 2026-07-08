# app/models/__init__.py

# Usuarios y roles
from .usuario import Usuario
from .coordinador import Coordinador
from .docente import Docente
from .estudiante import Estudiante
from .acudiente import Acudiente
from .estudiante_acudiente import EstudianteAcudiente

# Institución
from .colegio import Colegio
from .sede import Sede
from .jornada import Jornada
from .jornada_bloque import JornadaBloque
from .suscripcion import Suscripcion

# Académico
from .materia import Materia
from .nivel_materia import NivelMateria
from .grupo import Grupo
from .grupo_materia import GrupoMateria
from .plan_estudios import PlanEstudios
from .periodo import Periodo
from .periodo_academico import PeriodoAcademico

# Áreas y competencias
from .areas_gestion import AreaGestion  # ✅ Corregido (singular)

from .competencia_contribucion import competencia_contribucion
from .CompetenciaDocente import CompetenciaDocente
from .CompetenciaEstudiante import CompetenciaEstudiante
from .contribucion import Contribucion
from .indicador_logro import IndicadorLogro

# Evaluación
from .examen import Examen
from .pregunta import Pregunta
from .tipo_examen import TipoExamen
from .resultado_examen import ResultadoExamen
from .respuestas_examen_detalle import RespuestaExamenDetalle
from .evaluacion_final import EvaluacionFinal
from .evaluacion_criterio import EvaluacionCriterio
from .evaluacion_estudiante import EvaluacionEstudiante
from .criterio_evaluacion import CriterioEvaluacion
from .escala_evaluacion import EscalaEvaluacion
from .acuerdo_evaluacion import AcuerdoEvaluacion
from .evidencia import Evidencia

# Asistencia
from .asistencia import Asistencia
from .clase import Clase
from .clase_estudiante import ClaseEstudiante
from .ingreso_colegio import IngresoColegio

# Disciplina
from .novedad import Novedad
from .respuesta_novedad import RespuestaNovedad
from .descargo_estudiante import DescargoEstudiante
from .citacion_acudiente import CitacionAcudiente
from .justificacion_acudiente import JustificacionAcudiente
from .acuerdo_correctivo import AcuerdoCorrectivo
from .configuracion_disciplinaria import ConfiguracionDisciplinaria
from .configuracion_escalamiento import ConfiguracionEscalamiento
from .alerta import Alerta
from .seguimiento import Seguimiento

# Inclusión
from .piar import PIAR
from .ajuste_razonable import AjusteRazonable

# Permisos y tokens
from .permiso import Permiso
from .token_activacion import TokenActivacion

# Notificaciones
from .notification_log import NotificationLog

# Docente-Áreas
from .docente_area import DocenteAreas

# Exportar
__all__ = [
    'Usuario', 'Coordinador', 'Docente', 'Estudiante',
    'Acudiente', 'EstudianteAcudiente',
    'Colegio', 'Sede', 'Jornada', 'JornadaBloque', 'Suscripcion',
    'Materia', 'NivelMateria', 'Grupo', 'GrupoMateria',
    'PlanEstudios', 'Periodo', 'PeriodoAcademico',
    'AreaGestion',  # ✅ Corregido (singular)
    'competencia_contribucion', 'CompetenciaDocente',
    'CompetenciaEstudiante', 'Contribucion', 'IndicadorLogro',
    'Examen', 'Pregunta', 'TipoExamen', 'ResultadoExamen',
    'RespuestaExamenDetalle', 'EvaluacionFinal', 'EvaluacionCriterio',
    'EvaluacionEstudiante', 'CriterioEvaluacion', 'EscalaEvaluacion',
    'AcuerdoEvaluacion', 'Evidencia',
    'Asistencia', 'Clase', 'ClaseEstudiante', 'IngresoColegio',
    'Novedad', 'RespuestaNovedad', 'DescargoEstudiante',
    'CitacionAcudiente', 'JustificacionAcudiente', 'AcuerdoCorrectivo',
    'ConfiguracionDisciplinaria', 'ConfiguracionEscalamiento',
    'Alerta', 'Seguimiento',
    'PIAR', 'AjusteRazonable',
    'Permiso', 'TokenActivacion',
    'NotificationLog',
    'DocenteAreas'
]