from .usuario import Usuario
from .colegio import Colegio
from .docente import Docente
from .estudiante import Estudiante
from .acudiente import Acudiente

from .materia import Materia
from .clase import Clase
from .clase_estudiante import ClaseEstudiante
from .asistencia import Asistencia
from .CompetenciaEstudiante import CompetenciaEstudiante
from .CompetenciaDocente import CompetenciaDocente

from .indicador_logro import IndicadorLogro
from .evaluacion_estudiante import EvaluacionEstudiante

from .novedad import Novedad
from .respuesta_novedad import RespuestaNovedad
from .alerta import Alerta

from .citacion_acudiente import CitacionAcudiente
from .descargo_estudiante import DescargoEstudiante
from .acuerdo_correctivo import AcuerdoCorrectivo
from .justificacion_acudiente import JustificacionAcudiente

from .piar import PIAR
from .ajuste_razonable import AjusteRazonable

from .permiso import Permiso

from .acuerdo_evaluacion import AcuerdoEvaluacion
from .criterio_evaluacion import CriterioEvaluacion
from .areas_gestion import AreaGestion
from .evidencia import Evidencia
from .seguimiento import Seguimiento
from .evaluacion_final import EvaluacionFinal
from .evaluacion_criterio import EvaluacionCriterio
from .contribucion import Contribucion


from .periodo import Periodo
from .periodo_academico import PeriodoAcademico
from .escala_evaluacion import EscalaEvaluacion

from .configuracion_disciplinaria import ConfiguracionDisciplinaria
from .configuracion_escalamiento import ConfiguracionEscalamiento

from .suscripcion import Suscripcion
from .token_activacion import TokenActivacion
from .tipo_examen import TipoExamen

from .examen import Examen
from .resultado_examen import ResultadoExamen
from .docente_area import DocenteAreas
from .grupo import Grupo, GrupoAreas, DirectoresGrupo


# Agrega esta línea al final de app/models/__init__.py
from .notification_log import NotificationLog

from .coordinador import Coordinador


from app.models.grupo import Grupo