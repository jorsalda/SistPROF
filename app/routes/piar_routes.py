# ==========================================================
# PIAR ROUTES - SistPROF
# ==========================================================
from flask import Blueprint, render_template, abort, request, flash, redirect, url_for
from flask_login import login_required, current_user
from datetime import date, datetime

from app.extensions import db
from app.models.piar import PIAR
from app.models.piar_profesional import PiarProfesional
from app.models.estudiante import Estudiante
from app.models.docente import Docente
from app.models.materia import Materia
from app.models.ajuste_razonable import AjusteRazonable
from app.models.acudiente import Acudiente  # 👈 IMPORTANTE: Importar Acudiente

piar_bp = Blueprint("piar", __name__, url_prefix="/piar")


def obtener_base_template(rol):
    """Retorna el template base según el rol para mantener el menú correspondiente."""
    if rol in ('admin_colegio', 'superadmin'):
        return "colegio/colegio_base.html"
    elif rol == 'docente':
        return "docentes/docente_base.html"
    elif rol == 'coordinador':
        return "coordinador/coordinador_base.html"
    elif rol == 'psicologo':
        return "psicologo/psicologo_base.html"
    elif rol == 'acudiente':
        return "acudientes/acudiente_base.html"
    elif rol == 'estudiante':
        return "estudiantes/estudiante_base.html"
    else:
        return "colegio/colegio_base.html"  # Fallback


# ════════════════════════════════════════════════════════════════
# DASHBOARD DEL MÓDULO PIAR
# ════════════════════════════════════════════════════════════════

@piar_bp.route("/dashboard")
@login_required
def dashboard():
    """Panel principal del módulo PIAR."""
    if current_user.rol not in ('profesional_piar', 'psicologo', 'coordinador', 'admin_colegio', 'superadmin'):
        abort(403)

    piar_asignados = PiarProfesional.query.filter_by(
        profesional_id=current_user.id
    ).all()

    piares_directos = [p.piar for p in piar_asignados]

    if current_user.rol in ('psicologo', 'coordinador', 'admin_colegio', 'superadmin'):
        piares_colegio = PIAR.query.join(Estudiante).filter(
            Estudiante.colegio_id == current_user.colegio_id,
            PIAR.activo == True
        ).all()
    else:
        piares_colegio = []

    return render_template(
        "piar/dashboard.html",
        piares_directos=piares_directos,
        piares_colegio=piares_colegio,
        base_template=obtener_base_template(current_user.rol)
    )


# ════════════════════════════════════════════════════════════════
# LISTADO GENERAL DE PIAR
# ════════════════════════════════════════════════════════════════
@piar_bp.route("/lista")
@login_required
def lista():
    """Listado general de PIAR."""
    if current_user.rol == 'docente':
        docente = Docente.query.filter_by(usuario_id=current_user.id).first()
        if not docente:
            abort(403)
        piares = PIAR.query.filter_by(docente_id=docente.id).all()

    elif current_user.rol == 'estudiante':
        estudiante = Estudiante.query.filter_by(usuario_id=current_user.id).first()
        if not estudiante:
            abort(403)
        piares = PIAR.query.filter_by(estudiante_id=estudiante.id, activo=True).all()

    elif current_user.rol == 'acudiente':
        acudiente = Acudiente.query.filter_by(usuario_id=current_user.id).first()
        if not acudiente:
            abort(403)
        estudiantes_a_cargo = [e.id for e in acudiente.estudiantes]
        piares = PIAR.query.filter(PIAR.estudiante_id.in_(estudiantes_a_cargo), PIAR.activo == True).all()

    # 👇 AQUÍ AGREGAMOS AL PSICOLOGO Y AL PROFESIONAL_PIAR
    elif current_user.rol in ('coordinador', 'admin_colegio', 'secretaria', 'psicologo', 'profesional_piar',
                              'superadmin'):
        piares = PIAR.query.join(Estudiante).filter(
            Estudiante.colegio_id == current_user.colegio_id
        ).all()
    else:
        abort(403)

    return render_template(
        "piar/lista.html",
        piares=piares,
        base_template=obtener_base_template(current_user.rol)
    )


# ════════════════════════════════════════════════════════════════
# CREAR UN NUEVO PIAR
# ════════════════════════════════════════════════════════════════

@piar_bp.route("/nuevo", methods=["GET", "POST"])
@login_required
def nuevo():
    """Formulario para crear un nuevo PIAR."""
    if current_user.rol not in ('docente', 'coordinador', 'admin_colegio', 'psicologo', 'superadmin'):
        abort(403)

    docente = Docente.query.filter_by(usuario_id=current_user.id).first() if current_user.rol == 'docente' else None

    if request.method == "POST":
        try:
            estudiante_id = request.form.get("estudiante_id")
            materia_id = request.form.get("materia_id")

            # El docente no escribe diagnóstico, lo hace el admin/psicologo o ya viene de la matrícula
            diagnostico = request.form.get("diagnostico", "").strip()
            contexto_familiar = request.form.get("contexto_familiar", "").strip()
            entidades_apoyo = request.form.get("entidades_apoyo", "").strip()
            fecha_inicio = request.form.get("fecha_inicio")

            if not estudiante_id or not materia_id:
                flash("Estudiante y materia son obligatorios.", "danger")
                return redirect(url_for("piar.nuevo"))

            docente_id_final = docente.id if docente else None

            # Crear el PIAR
            nuevo_piar = PIAR(
                estudiante_id=int(estudiante_id),
                materia_id=int(materia_id),
                docente_id=docente_id_final,
                diagnostico=diagnostico if diagnostico else None,
                contexto_familiar=contexto_familiar if contexto_familiar else None,
                entidades_apoyo=entidades_apoyo if entidades_apoyo else None,
                fecha_inicio=fecha_inicio if fecha_inicio else date.today(),
                activo=True
            )
            db.session.add(nuevo_piar)
            db.session.commit()

            flash("✅ PIAR creado exitosamente.", "success")
            return redirect(url_for("piar.lista"))

        except Exception as e:
            db.session.rollback()
            flash(f"Error al crear PIAR: {str(e)}", "danger")
            return redirect(url_for("piar.nuevo"))

    # 👇 FILTRO LÓGICO PARA LA CARGA DE ESTUDIANTES
    if docente:
        from app.models.grupo_materia import GrupoMateria
        asignaciones = GrupoMateria.query.filter_by(docente_id=docente.id, activo=True).all()
        grupos_ids = [a.grupo_id for a in asignaciones]

        # Aquí aplicamos la regla: Solo estudiantes de sus grupos, activos, y que TENGAN diagnóstico o requieran PIAR
        estudiantes = Estudiante.query.filter(
            Estudiante.grupo_id.in_(grupos_ids),
            Estudiante.activo == True,
            db.or_(
                Estudiante.diagnostico_base.isnot(None),
                Estudiante.requiere_piar == True
            )
        ).order_by(Estudiante.apellido).all()

        materias = [a.materia for a in asignaciones if a.materia]
    else:
        # Para el admin, mostramos los mismos filtros (solo los que tienen diagnóstico)
        estudiantes = Estudiante.query.filter(
            Estudiante.colegio_id == current_user.colegio_id,
            Estudiante.activo == True,
            db.or_(
                Estudiante.diagnostico_base.isnot(None),
                Estudiante.requiere_piar == True
            )
        ).all()
        materias = Materia.query.filter_by(estado=True).all()

    return render_template(
        "piar/formulario.html",
        estudiantes=estudiantes,
        materias=materias,
        piar=None,
        base_template=obtener_base_template(current_user.rol)
    )



# ════════════════════════════════════════════════════════════════
# VER DETALLE DE UN PIAR
# ════════════════════════════════════════════════════════════════
@piar_bp.route("/<int:piar_id>")
@login_required
def detalle(piar_id):
    """Muestra el detalle completo de un PIAR."""
    piar = PIAR.query.get_or_404(piar_id)

    if current_user.rol == 'docente':
        docente = Docente.query.filter_by(usuario_id=current_user.id).first()
        if piar.docente_id != docente.id:
            abort(403)
    elif current_user.rol == 'estudiante':
        estudiante = Estudiante.query.filter_by(usuario_id=current_user.id).first()
        if piar.estudiante_id != estudiante.id:
            abort(403)
    elif current_user.rol == 'acudiente':
        acudiente = Acudiente.query.filter_by(usuario_id=current_user.id).first()
        estudiantes_a_cargo = [e.id for e in acudiente.estudiantes]
        if piar.estudiante_id not in estudiantes_a_cargo:
            abort(403)
    elif current_user.rol not in ('coordinador', 'admin_colegio', 'secretaria', 'psicologo', 'profesional_piar', 'superadmin'):
        abort(403)

    ajustes = piar.ajustes_razonables
    profesionales_asignados = piar.profesionales

    from app.models.usuario import Usuario
    profesionales_disponibles = Usuario.query.filter(
        Usuario.colegio_id == current_user.colegio_id,
        Usuario.rol.in_(['psicologo', 'profesional_piar']),
        Usuario.is_active == True
    ).all()

    return render_template(
        "piar/detalle.html",
        piar=piar,
        ajustes=ajustes,
        profesionales=profesionales_asignados,
        profesionales_disponibles=profesionales_disponibles,
        base_template=obtener_base_template(current_user.rol) # 👈 ESTO ES LO QUE FALTABA
    )

# ════════════════════════════════════════════════════════════════
# CREAR UN AJUSTE RAZONABLE PARA UN PIAR
# ════════════════════════════════════════════════════════════════

@piar_bp.route("/<int:piar_id>/ajuste/nuevo", methods=["POST"])
@login_required
def nuevo_ajuste(piar_id):
    """Agrega un ajuste razonable a un PIAR existente."""
    piar = PIAR.query.get_or_404(piar_id)

    if current_user.rol == 'docente':
        docente = Docente.query.filter_by(usuario_id=current_user.id).first()
        if piar.docente_id != docente.id:
            abort(403)
    elif current_user.rol not in ('coordinador', 'admin_colegio', 'secretaria', 'psicologo', 'profesional_piar', 'superadmin'):
        abort(403)

    descripcion = request.form.get("descripcion", "").strip()

    if not descripcion:
        flash("La descripción del ajuste es obligatoria.", "danger")
        return redirect(url_for("piar.detalle", piar_id=piar.id))

    try:
        # 👇 CORRECCIÓN: Buscamos el docente de forma segura
        docente_obj = Docente.query.filter_by(usuario_id=current_user.id).first()
        docente_id_final = docente_obj.id if docente_obj else None

        nuevo_ajuste = AjusteRazonable(
            piar_id=piar.id,
            descripcion=descripcion,
            aplicado=False,
            docente_id=docente_id_final, # 👈 Usamos la variable corregida
            materia_id=piar.materia_id,
            fecha_creacion=datetime.now()
        )
        db.session.add(nuevo_ajuste)
        db.session.commit()
        flash("✅ Ajuste razonable agregado correctamente.", "success")

    except Exception as e:
        db.session.rollback()
        flash(f"Error al guardar el ajuste: {str(e)}", "danger")

    return redirect(url_for("piar.detalle", piar_id=piar.id))

# ════════════════════════════════════════════════════════════════
# ASIGNAR UN PROFESIONAL AL PIAR
# ════════════════════════════════════════════════════════════════

@piar_bp.route("/<int:piar_id>/asignar-profesional", methods=["POST"])
@login_required
def asignar_profesional(piar_id):
    """Asigna un psicólogo o profesional PIAR a un caso."""
    piar = PIAR.query.get_or_404(piar_id)

    if current_user.rol not in ('coordinador', 'admin_colegio', 'psicologo', 'superadmin'):
        abort(403)

    profesional_id = request.form.get("profesional_id")

    if not profesional_id:
        flash("Debes seleccionar un profesional.", "danger")
        return redirect(url_for("piar.detalle", piar_id=piar.id))

    try:
        existe = PiarProfesional.query.filter_by(
            piar_id=piar.id,
            profesional_id=int(profesional_id)
        ).first()

        if existe:
            flash("Este profesional ya está asignado a este PIAR.", "warning")
        else:
            nueva_asignacion = PiarProfesional(
                piar_id=piar.id,
                profesional_id=int(profesional_id)
            )
            db.session.add(nueva_asignacion)
            db.session.commit()
            flash("✅ Profesional asignado exitosamente al equipo de apoyo.", "success")

    except Exception as e:
        db.session.rollback()
        flash(f"Error al asignar profesional: {str(e)}", "danger")

    return redirect(url_for("piar.detalle", piar_id=piar.id))


# ════════════════════════════════════════════════════════════════
# EDITAR DOCUMENTOS OFICIALES (ACTA E INFORME)
# ════════════════════════════════════════════════════════════════

@piar_bp.route("/<int:piar_id>/documentos", methods=["POST"])
@login_required
def editar_documentos(piar_id):
    """Actualiza el Acta de Acuerdo y el Informe Anual."""
    piar = PIAR.query.get_or_404(piar_id)

    if current_user.rol == 'docente':
        docente = Docente.query.filter_by(usuario_id=current_user.id).first()
        if piar.docente_id != docente.id:
            abort(403)
    elif current_user.rol not in ('coordinador', 'admin_colegio', 'psicologo', 'profesional_piar', 'superadmin'):
        abort(403)

    acta = request.form.get("acta_acuerdo", "").strip()
    informe = request.form.get("informe_anual", "").strip()

    try:
        piar.acta_acuerdo = acta if acta else None
        piar.informe_anual = informe if informe else None
        db.session.commit()
        flash("✅ Documentos oficiales actualizados correctamente.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al actualizar documentos: {str(e)}", "danger")

    return redirect(url_for("piar.detalle", piar_id=piar.id))


# ════════════════════════════════════════════════════════════════
# LISTADO GLOBAL DE AJUSTES RAZONABLES (AGRUPADO POR PIAR)
# ════════════════════════════════════════════════════════════════

@piar_bp.route("/ajustes")
@login_required
def ajustes():
    """Muestra un listado agrupado de ajustes razonables por PIAR."""
    if current_user.rol not in ('docente', 'coordinador', 'admin_colegio', 'psicologo', 'profesional_piar',
                                'superadmin'):
        abort(403)

    query = PIAR.query.join(AjusteRazonable)

    if current_user.rol == 'docente':
        query = query.filter(PIAR.docente_id == current_user.docente.id)
    else:
        query = query.join(Estudiante).filter(Estudiante.colegio_id == current_user.colegio_id)

    piares_con_ajustes = query.order_by(PIAR.id.desc()).all()

    agrupados = []
    for p in piares_con_ajustes:
        if not p.ajustes_razonables:
            continue
        agrupados.append({
            'piar': p,
            'ajustes': p.ajustes_razonables
        })

    return render_template(
        "piar/ajustes.html",
        agrupados=agrupados,
        base_template=obtener_base_template(current_user.rol)
    )