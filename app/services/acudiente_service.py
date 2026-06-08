from app.extensions import db
from sqlalchemy import func, desc
from datetime import datetime, date

# Importaciones de modelos (estas sí se necesitan al inicio)
from app.models.usuario import Usuario
from app.models.acudiente import Acudiente
from app.models.estudiante import Estudiante
from app.models.estudiante_acudiente import EstudianteAcudiente
from app.models.evaluacion_estudiante import EvaluacionEstudiante
from app.models.asistencia import Asistencia
from app.models.novedad import Novedad
from app.models.citacion_acudiente import CitacionAcudiente
from app.models.resultado_examen import ResultadoExamen
from app.models.periodo_academico import PeriodoAcademico
from app.models.materia import Materia
from app.models.clase import Clase


class AcudienteService:

    def get_estudiantes_by_acudiente(self, usuario_id):
        """Obtener todos los estudiantes asociados a un acudiente"""
        from app.models.acudiente import Acudiente
        from app.models.estudiante import Estudiante
        from app.models.estudiante_acudiente import EstudianteAcudiente

        acudiente = Acudiente.query.filter_by(usuario_id=usuario_id).first()
        if not acudiente:
            return []

        estudiantes = db.session.query(Estudiante). \
            join(EstudianteAcudiente, EstudianteAcudiente.estudiante_id == Estudiante.id). \
            filter(EstudianteAcudiente.acudiente_id == acudiente.id). \
            all()

        result = []
        for est in estudiantes:
            result.append({
                'id': est.id,
                'nombre': est.nombre,
                'grado': est.grado,
                'grupo': est.grupo,
                'jornada': self._get_jornada_nombre(est.jornada_id),
                'promedio_general': self.get_promedio_general(est.id),
                'asistencia': self.get_asistencia_porcentaje(est.id),
                'total_novedades': self.get_total_novedades(est.id),
                'ultima_novedad': self.get_ultima_novedad_texto(est.id),
                'alerta': self.get_alerta_estudiante(est.id)
            })

        return result

    def _get_jornada_nombre(self, jornada_id):
        """Obtener nombre de la jornada"""
        if not jornada_id:
            return "Mañana"
        return "Mañana"

    def verificar_pertenencia(self, usuario_id, estudiante_id):
        """Verificar que un estudiante pertenezca al acudiente"""
        from app.models.acudiente import Acudiente
        from app.models.estudiante_acudiente import EstudianteAcudiente

        acudiente = Acudiente.query.filter_by(usuario_id=usuario_id).first()
        if not acudiente:
            return False

        relacion = EstudianteAcudiente.query.filter_by(
            estudiante_id=estudiante_id,
            acudiente_id=acudiente.id
        ).first()

        return relacion is not None

    def get_estudiante_info(self, estudiante_id):
        """Obtener información básica del estudiante"""
        from app.models.estudiante import Estudiante

        estudiante = Estudiante.query.get(estudiante_id)
        if not estudiante:
            return None

        return {
            'id': estudiante.id,
            'nombre': estudiante.nombre,
            'grado': estudiante.grado,
            'grupo': estudiante.grupo,
            'jornada': self._get_jornada_nombre(estudiante.jornada_id),
            'direccion': estudiante.direccion,
            'telefono': estudiante.telefono
        }

    def get_periodos_activos(self):
        """Obtener períodos académicos activos"""
        from app.models.periodo_academico import PeriodoAcademico

        periodos = PeriodoAcademico.query.filter_by(activo=True).order_by(PeriodoAcademico.orden).all()
        return [{'id': p.id, 'nombre': p.nombre, 'anio_lectivo': 2024, 'activo': p.activo} for p in periodos]

    def get_calificaciones(self, estudiante_id, periodo_id=None):
        """Obtener calificaciones del estudiante"""
        from app.models.materia import Materia
        from app.models.evaluacion_estudiante import EvaluacionEstudiante

        query = db.session.query(
            Materia.nombre.label('materia'),
            func.avg(EvaluacionEstudiante.calificacion).label('calificacion')
        ).join(
            EvaluacionEstudiante, EvaluacionEstudiante.estudiante_id == estudiante_id
        ).join(
            Materia, Materia.id == EvaluacionEstudiante.materia_id
        )

        if periodo_id:
            query = query.filter(EvaluacionEstudiante.periodo_id == periodo_id)

        query = query.group_by(Materia.nombre)
        resultados = query.all()

        calificaciones = []
        for r in resultados:
            cal = float(r.calificacion) if r.calificacion else 0
            calificaciones.append({
                'materia': r.materia,
                'calificacion': cal,
                'desempeno': self._get_nivel_desempeno(cal),
                'observacion': ''
            })

        return calificaciones

    def get_promedio_general(self, estudiante_id, periodo_id=None):
        """Calcular promedio general del estudiante"""
        from app.models.evaluacion_estudiante import EvaluacionEstudiante

        query = db.session.query(func.avg(EvaluacionEstudiante.calificacion)). \
            filter(EvaluacionEstudiante.estudiante_id == estudiante_id)

        if periodo_id:
            query = query.filter(EvaluacionEstudiante.periodo_id == periodo_id)

        promedio = query.scalar()
        return float(promedio) if promedio else 0

    def get_asistencia_stats(self, estudiante_id):
        """Obtener estadísticas de asistencia"""
        from app.models.asistencia import Asistencia

        fecha_inicio = date.today().replace(day=1)

        total_clases = db.session.query(func.count(Asistencia.id)). \
                           filter(Asistencia.estudiante_id == estudiante_id). \
                           filter(Asistencia.fecha >= fecha_inicio).scalar() or 1

        presente = db.session.query(func.count(Asistencia.id)). \
                       filter(Asistencia.estudiante_id == estudiante_id). \
                       filter(Asistencia.estado == 'presente'). \
                       filter(Asistencia.fecha >= fecha_inicio).scalar() or 0

        ausente = db.session.query(func.count(Asistencia.id)). \
                      filter(Asistencia.estudiante_id == estudiante_id). \
                      filter(Asistencia.estado == 'ausente'). \
                      filter(Asistencia.fecha >= fecha_inicio).scalar() or 0

        porcentaje = round((presente / total_clases) * 100, 1) if total_clases > 0 else 0

        return {
            'porcentaje': porcentaje,
            'presente': presente,
            'ausente': ausente
        }

    def get_asistencias_recientes(self, estudiante_id, limit=10):
        """Obtener asistencias recientes"""
        from app.models.asistencia import Asistencia
        from app.models.clase import Clase
        from app.models.materia import Materia

        asistencias = Asistencia.query. \
            filter(Asistencia.estudiante_id == estudiante_id). \
            order_by(desc(Asistencia.fecha)). \
            limit(limit).all()

        result = []
        for a in asistencias:
            result.append({
                'fecha': a.fecha.strftime('%Y-%m-%d'),
                'materia': self._get_materia_by_clase(a.clase_id),
                'estado': a.estado,
                'observacion': a.observacion
            })

        return result

    def _get_materia_by_clase(self, clase_id):
        """Obtener nombre de materia desde clase_id"""
        from app.models.clase import Clase
        from app.models.materia import Materia

        if not clase_id:
            return "General"
        clase = Clase.query.get(clase_id)
        if clase and clase.materia_id:
            materia = Materia.query.get(clase.materia_id)
            return materia.nombre if materia else "General"
        return "General"

    def get_examenes_estudiante(self, estudiante_id):
        """Obtener exámenes del estudiante con sus resultados"""
        from app.models.resultado_examen import ResultadoExamen
        from app.models.materia import Materia

        examenes = ResultadoExamen.query. \
            filter(ResultadoExamen.estudiante_id == estudiante_id). \
            order_by(desc(ResultadoExamen.fecha)).all()

        result = []
        for e in examenes:
            materia = Materia.query.get(e.materia_id)
            result.append({
                'id': e.id,
                'titulo': f'Examen de {materia.nombre if materia else "Materia"}',
                'descripcion': f'Total preguntas: {e.total_preguntas}',
                'fecha': e.fecha.strftime('%Y-%m-%d'),
                'tiempo_limite_minutos': 60,
                'total_preguntas': e.total_preguntas,
                'resultado': {
                    'porcentaje': e.porcentaje,
                    'nota_numerica': float(e.nota_numerica) if e.nota_numerica else 0
                } if e.porcentaje else None
            })

        return result

    def get_novedades_estudiante(self, estudiante_id):
        """Obtener novedades del estudiante"""
        from app.models.novedad import Novedad

        novedades = Novedad.query. \
            filter(Novedad.estudiante_id == estudiante_id). \
            order_by(desc(Novedad.fecha), desc(Novedad.hora)).all()

        result = []
        for n in novedades:
            tipo_val = n.tipo_novedad.value if hasattr(n.tipo_novedad, 'value') else str(n.tipo_novedad)
            gravedad_val = n.gravedad.value if hasattr(n.gravedad, 'value') else str(n.gravedad)

            result.append({
                'id': n.id,
                'tipo_novedad': tipo_val,
                'informe': n.informe,
                'fecha': n.fecha.strftime('%Y-%m-%d'),
                'hora': str(n.hora),
                'gravedad': gravedad_val,
                'respuesta': None
            })

        return result

    def get_citaciones_estudiante(self, estudiante_id):
        """Obtener citaciones del estudiante"""
        from app.models.citacion_acudiente import CitacionAcudiente

        citaciones = CitacionAcudiente.query. \
            filter(CitacionAcudiente.estudiante_id == estudiante_id). \
            order_by(desc(CitacionAcudiente.fecha_citacion)).all()

        result = []
        for c in citaciones:
            result.append({
                'id': c.id,
                'motivo': c.motivo,
                'fecha_citacion': c.fecha_citacion.strftime('%Y-%m-%d %H:%M'),
                'observaciones': c.observaciones,
                'estado': c.estado
            })

        return result

    def get_rendimiento_grafico(self, estudiante_id):
        """Obtener datos para el gráfico de rendimiento"""
        calificaciones = self.get_calificaciones(estudiante_id)

        materias = [c['materia'] for c in calificaciones]
        valores = [c['calificacion'] for c in calificaciones]

        return {
            'materias': materias,
            'calificaciones': valores
        }

    def get_calificaciones_json(self, estudiante_id, periodo_id=None):
        """Obtener calificaciones en formato JSON para API"""
        calificaciones = self.get_calificaciones(estudiante_id, periodo_id)
        promedio = self.get_promedio_general(estudiante_id, periodo_id)

        return {
            'calificaciones': calificaciones,
            'promedio_general': promedio
        }

    def get_novedades_recientes(self, estudiantes_ids, limit=5):
        """Obtener novedades recientes de varios estudiantes"""
        from app.models.novedad import Novedad
        from app.models.estudiante import Estudiante

        if not estudiantes_ids:
            return []

        novedades = Novedad.query. \
            filter(Novedad.estudiante_id.in_(estudiantes_ids)). \
            order_by(desc(Novedad.fecha), desc(Novedad.hora)). \
            limit(limit).all()

        estudiantes = {e.id: e.nombre for e in Estudiante.query.filter(Estudiante.id.in_(estudiantes_ids)).all()}

        result = []
        for n in novedades:
            tipo_val = n.tipo_novedad.value if hasattr(n.tipo_novedad, 'value') else str(n.tipo_novedad)
            gravedad_val = n.gravedad.value if hasattr(n.gravedad, 'value') else str(n.gravedad)

            result.append({
                'id': n.id,
                'estudiante_nombre': estudiantes.get(n.estudiante_id, 'Desconocido'),
                'tipo_novedad': tipo_val,
                'informe': n.informe,
                'fecha': n.fecha.strftime('%Y-%m-%d'),
                'hora': str(n.hora),
                'gravedad': gravedad_val
            })

        return result

    def get_citaciones_pendientes(self, estudiantes_ids):
        """Obtener citaciones pendientes"""
        from app.models.citacion_acudiente import CitacionAcudiente
        from app.models.estudiante import Estudiante

        if not estudiantes_ids:
            return []

        citaciones = CitacionAcudiente.query. \
            filter(CitacionAcudiente.estudiante_id.in_(estudiantes_ids)). \
            filter(CitacionAcudiente.estado == 'pendiente'). \
            order_by(CitacionAcudiente.fecha_citacion).all()

        estudiantes = {e.id: e.nombre for e in Estudiante.query.filter(Estudiante.id.in_(estudiantes_ids)).all()}

        result = []
        for c in citaciones:
            result.append({
                'id': c.id,
                'estudiante_nombre': estudiantes.get(c.estudiante_id, 'Desconocido'),
                'motivo': c.motivo,
                'fecha_citacion': c.fecha_citacion.strftime('%Y-%m-%d %H:%M'),
                'estado': c.estado
            })

        return result

    def reportar_novedad(self, estudiante_id, tipo_novedad, informe, usuario_id):
        """Registrar una novedad reportada por el acudiente"""
        from app.models.novedad import Novedad

        try:
            nueva_novedad = Novedad(
                estudiante_id=estudiante_id,
                tipo_novedad=tipo_novedad,
                informe=informe,
                fecha=date.today(),
                hora=datetime.now().time(),
                gravedad='Tipo 1',
                registrada_por=usuario_id
            )

            db.session.add(nueva_novedad)
            db.session.commit()

            return {'success': True, 'mensaje': 'Novedad reportada correctamente', 'id': nueva_novedad.id}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}

    def responder_novedad(self, novedad_id, respuesta, usuario_id):
        """Responder a una novedad"""
        from app.models.respuesta_novedad import RespuestaNovedad

        try:
            nueva_respuesta = RespuestaNovedad(
                novedad_id=novedad_id,
                usuario_id=usuario_id,
                rol='acudiente',
                mensaje=respuesta,
                fecha=datetime.now()
            )

            db.session.add(nueva_respuesta)
            db.session.commit()

            return {'success': True, 'mensaje': 'Respuesta enviada'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}

    def confirmar_citacion(self, citacion_id, usuario_id):
        """Confirmar asistencia a una citación"""
        from app.models.citacion_acudiente import CitacionAcudiente

        try:
            citacion = CitacionAcudiente.query.get(citacion_id)
            if not citacion:
                return {'success': False, 'error': 'Citación no encontrada'}

            citacion.estado = 'confirmada'
            db.session.commit()

            return {'success': True, 'mensaje': 'Citación confirmada'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}

    def enviar_mensaje(self, estudiante_id, mensaje, acudiente_id):
        """Enviar mensaje al colegio"""
        from app.models.notification_log import NotificationLog

        try:
            nuevo_log = NotificationLog(
                tipo='alerta_sistema',
                destinatario='colegio',
                asunto=f'Mensaje de acudiente para estudiante {estudiante_id}',
                payload_json={'mensaje': mensaje, 'acudiente_id': acudiente_id}
            )

            db.session.add(nuevo_log)
            db.session.commit()

            return {'success': True, 'mensaje': 'Mensaje enviado'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}

    def solicitar_reunion(self, estudiante_id, fecha, motivo, mensaje, acudiente_id):
        """Solicitar reunión con el colegio"""
        from app.models.acudiente import Acudiente
        from app.models.citacion_acudiente import CitacionAcudiente

        try:
            acudiente = Acudiente.query.filter_by(usuario_id=acudiente_id).first()
            if not acudiente:
                return {'success': False, 'error': 'Acudiente no encontrado'}

            nueva_citacion = CitacionAcudiente(
                estudiante_id=estudiante_id,
                acudiente_id=acudiente.id,
                motivo=f'Solicitud de reunión: {motivo}',
                fecha_citacion=datetime.strptime(fecha, '%Y-%m-%d'),
                observaciones=mensaje,
                estado='pendiente'
            )

            db.session.add(nueva_citacion)
            db.session.commit()

            return {'success': True, 'mensaje': 'Solicitud de reunión enviada'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}

    def get_notificaciones_count(self, usuario_id):
        """Obtener número de notificaciones pendientes"""
        from app.models.acudiente import Acudiente
        from app.models.estudiante_acudiente import EstudianteAcudiente
        from app.models.citacion_acudiente import CitacionAcudiente

        acudiente = Acudiente.query.filter_by(usuario_id=usuario_id).first()
        if not acudiente:
            return 0

        estudiantes_ids = [ea.estudiante_id for ea in
                           EstudianteAcudiente.query.filter_by(acudiente_id=acudiente.id).all()]

        if not estudiantes_ids:
            return 0

        citaciones_count = CitacionAcudiente.query. \
            filter(CitacionAcudiente.estudiante_id.in_(estudiantes_ids)). \
            filter(CitacionAcudiente.estado == 'pendiente').count()

        return citaciones_count

    def _get_nivel_desempeno(self, calificacion):
        """Obtener nivel de desempeño según calificación"""
        if calificacion >= 4.6:
            return 'Superior'
        elif calificacion >= 3.9:
            return 'Alto'
        elif calificacion >= 3.0:
            return 'Básico'
        else:
            return 'Bajo'

    def get_asistencia_porcentaje(self, estudiante_id):
        """Calcular porcentaje de asistencia"""
        stats = self.get_asistencia_stats(estudiante_id)
        return stats['porcentaje']

    def get_total_novedades(self, estudiante_id):
        """Contar total de novedades"""
        from app.models.novedad import Novedad
        return Novedad.query.filter_by(estudiante_id=estudiante_id).count()

    def get_ultima_novedad_texto(self, estudiante_id):
        """Obtener texto de la última novedad"""
        from app.models.novedad import Novedad
        ultima = Novedad.query.filter_by(estudiante_id=estudiante_id).order_by(desc(Novedad.fecha)).first()
        return ultima.informe[:50] + '...' if ultima and len(ultima.informe) > 50 else (
            ultima.informe if ultima else None)

    def get_alerta_estudiante(self, estudiante_id):
        """Verificar si el estudiante tiene alertas activas"""
        promedio = self.get_promedio_general(estudiante_id)
        if promedio < 3.0:
            return {'tipo': 'danger', 'mensaje': f'Promedio bajo: {promedio:.1f}'}

        asistencia = self.get_asistencia_porcentaje(estudiante_id)
        if asistencia < 80:
            return {'tipo': 'warning', 'mensaje': f'Asistencia baja: {asistencia}%'}

        return None