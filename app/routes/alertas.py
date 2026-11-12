from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from datetime import datetime
from sqlalchemy import or_
from app.extensions import db
from app.models.alerta import Alerta
from app.models.estudiante import Estudiante
from app.models.docente import Docente
from app.models.grupo_materia import GrupoMateria
from app.models.acudiente import Acudiente
from app.models.estudiante_acudiente import EstudianteAcudiente
from app.models.justificacion_acudiente import JustificacionAcudiente

bp = Blueprint('alertas', __name__, url_prefix='/alertas')


@bp.route('/')
@login_required
def index():
    roles_permitidos = ['admin_colegio', 'superadmin', 'docente', 'coordinador', 'estudiante', 'acudiente']
    if current_user.rol not in roles_permitidos:
        abort(403)

    query = Alerta.query.join(Estudiante, Alerta.estudiante_id == Estudiante.id).filter(
        Estudiante.colegio_id == current_user.colegio_id
    )

    if current_user.rol == 'docente':
        docente = Docente.query.filter_by(usuario_id=current_user.id).first()
        if not docente:
            abort(403)
        mis_grupos = [gm.grupo_id for gm in GrupoMateria.query.filter_by(docente_id=docente.id, activo=True).all()]
        mis_estudiantes = [e.id for e in Estudiante.query.filter(Estudiante.grupo_id.in_(mis_grupos)).all()]
        query = query.filter(Alerta.estudiante_id.in_(mis_estudiantes))

    elif current_user.rol == 'acudiente':
        acudiente = Acudiente.query.filter_by(usuario_id=current_user.id).first()
        if not acudiente:
            acudiente = Acudiente.query.filter_by(email=current_user.email).first()

        if acudiente:
            vinculaciones = EstudianteAcudiente.query.filter_by(acudiente_id=acudiente.id).all()
            mis_estudiantes = [v.estudiante_id for v in vinculaciones]
            if mis_estudiantes:
                query = query.filter(Alerta.estudiante_id.in_(mis_estudiantes))
            else:
                query = query.filter(False)
        else:
            query = query.filter(False)

    elif current_user.rol == 'estudiante':
        estudiante = Estudiante.query.filter_by(usuario_id=current_user.id).first()
        if not estudiante:
            abort(403)
        query = query.filter(Alerta.estudiante_id == estudiante.id)

    busqueda = request.args.get('q', '').strip()
    estado = request.args.get('estado', 'todas')

    if busqueda:
        query = query.filter(or_(Estudiante.nombre.ilike(f'%{busqueda}%'), Estudiante.apellido.ilike(f'%{busqueda}%')))

    if estado == 'pendientes':
        query = query.filter(or_(Alerta.atendida == False, Alerta.atendida.is_(None)))
    elif estado == 'atendidas':
        query = query.filter(Alerta.atendida == True)

    alertas_raw = query.order_by(Alerta.fecha_creacion.desc()).all()

    # Agrupación por estudiante para el acordeón
    estudiantes_agrupados = {}
    for alerta in alertas_raw:
        est_id = alerta.estudiante_id
        if est_id not in estudiantes_agrupados:
            estudiantes_agrupados[est_id] = {
                'estudiante': alerta.estudiante,
                'alertas': [],
                'pendientes': 0
            }

        # ✅ BUSCAR JUSTIFICACIÓN MANUAL
        justificacion = JustificacionAcudiente.query.filter(
            JustificacionAcudiente.novedad_id == alerta.id
        ).first()
        alerta.justificacion_manual = justificacion

        estudiantes_agrupados[est_id]['alertas'].append(alerta)
        if not alerta.atendida:
            estudiantes_agrupados[est_id]['pendientes'] += 1

    lista_agrupada = list(estudiantes_agrupados.values())

    return render_template('alertas/index.html', alertas=lista_agrupada, busqueda=busqueda, estado_actual=estado)


@bp.route('/atender/<int:alerta_id>', methods=['POST'])
@login_required
def atender(alerta_id):
    if current_user.rol not in ['admin_colegio', 'superadmin', 'docente', 'coordinador', 'acudiente']:
        abort(403)

    alerta = Alerta.query.get_or_404(alerta_id)

    if alerta.estudiante.colegio_id != current_user.colegio_id:
        abort(403)

    try:
        alerta.atendida = True
        alerta.atendida_por = current_user.id
        alerta.fecha_atencion = datetime.now()
        db.session.commit()
        flash('Alerta marcada como atendida correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al atender la alerta: {str(e)}', 'danger')

    return redirect(url_for('alertas.index'))


@bp.route('/justificar/<int:alerta_id>', methods=['POST'])
@login_required
def justificar(alerta_id):
    if current_user.rol not in ['acudiente', 'estudiante']:
        abort(403)

    alerta = Alerta.query.get_or_404(alerta_id)
    justificacion_texto = request.form.get('justificacion', '').strip()

    if not justificacion_texto:
        flash('Debes escribir una justificación.', 'warning')
        return redirect(url_for('alertas.index'))

    try:
        acudiente = Acudiente.query.filter_by(usuario_id=current_user.id).first()
        if not acudiente:
            acudiente = Acudiente.query.filter_by(email=current_user.email).first()

        acudiente_id = acudiente.id if acudiente else None

        existente = JustificacionAcudiente.query.filter_by(novedad_id=alerta.id).first()

        if existente:
            existente.descripcion = justificacion_texto
            existente.justificacion = justificacion_texto
            existente.fecha = datetime.now()
            flash('Justificación actualizada correctamente.', 'success')
        else:
            nueva_justificacion = JustificacionAcudiente(
                novedad_id=alerta.id,
                acudiente_id=acudiente_id,
                descripcion=justificacion_texto,
                justificacion=justificacion_texto
            )
            db.session.add(nueva_justificacion)
            flash('Justificación enviada correctamente.', 'success')

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash(f'Error al guardar la justificación: {str(e)}', 'danger')

    return redirect(url_for('alertas.index'))