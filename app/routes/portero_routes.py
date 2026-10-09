# ==========================================================
# PORTERO ROUTES - SistPROF
# ==========================================================
from datetime import datetime, date

from flask import Blueprint, render_template, request, jsonify, abort
from flask_login import login_required, current_user
from sqlalchemy import or_

from app.extensions import db
from app.models.estudiante import Estudiante
from app.models.ingreso_colegio import IngresoColegio, TipoEvento

portero_bp = Blueprint("portero", __name__, url_prefix="/portero")


# ════════════════════════════════════════════════════════════════
# DASHBOARD
# ════════════════════════════════════════════════════════════════

@portero_bp.route("/dashboard")
@login_required
def dashboard():
    """Panel principal del portero."""
    if current_user.rol != 'portero':
        abort(403)

    colegio_id = current_user.colegio_id

    total_estudiantes = Estudiante.query.filter_by(
        colegio_id=colegio_id, activo=True
    ).count()

    hoy = date.today()
    total_registros_hoy = IngresoColegio.query.filter_by(
        colegio_id=colegio_id, fecha=hoy
    ).count()

    return render_template(
        "portero/dashboard.html",
        total_estudiantes=total_estudiantes,
        total_registros_hoy=total_registros_hoy,
    )


# ════════════════════════════════════════════════════════════════
# PÁGINA DEL LECTOR QR
# ════════════════════════════════════════════════════════════════

@portero_bp.route("/lector")
@login_required
def lector():
    """Página del lector de QR + búsqueda manual."""
    if current_user.rol != 'portero':
        abort(403)

    colegio_id = current_user.colegio_id
    hoy = date.today()

    registros_hoy = (
        IngresoColegio.query
        .filter_by(colegio_id=colegio_id, fecha=hoy)
        .order_by(IngresoColegio.hora.desc())
        .limit(20)
        .all()
    )

    registros = []
    for r in registros_hoy:
        est = Estudiante.query.get(r.estudiante_id)
        # tipo_evento puede ser Enum o string según de dónde venga
        te = r.tipo_evento
        te_str = te.value.upper() if hasattr(te, 'value') else str(te).upper()

        registros.append({
            "id": r.id,
            "hora": r.hora.strftime("%H:%M:%S") if r.hora else "—",
            "tipo_evento": te_str,
            "metodo": r.metodo or "—",
            "estudiante": f"{est.nombre} {est.apellido or ''}".strip() if est else "Desconocido",
            "documento": est.documento if est else "—",
        })

    return render_template(
        "portero/lector_qr.html",
        registros=registros,
        total_registros_hoy=len(registros),
    )


# ════════════════════════════════════════════════════════════════
# API: REGISTRAR ENTRADA / SALIDA
# ════════════════════════════════════════════════════════════════

@portero_bp.route("/registrar", methods=["POST"])
@login_required
def registrar():
    """
    Recibe JSON:
      { "identificador": "<qr_token|id|documento>", "tipo_evento": "INGRESO"|"SALIDA", "metodo": "QR"|"MANUAL" }
    Registra en ingresos_colegio y notifica al acudiente SOLO si:
      - INGRESO después de hora_inicio + tolerancia_minutos
      - SALIDA antes de hora_fin
    """
    if current_user.rol != 'portero':
        return jsonify({"error": "No autorizado"}), 403

    data = request.get_json() or {}
    identificador = (data.get("identificador") or "").strip()
    tipo_evento_str = (data.get("tipo_evento") or "").strip().upper()
    metodo = (data.get("metodo") or "QR").strip().upper()

    if not identificador:
        return jsonify({"error": "Identificador vacío"}), 400

    if tipo_evento_str not in ("INGRESO", "SALIDA"):
        return jsonify({"error": "tipo_evento debe ser INGRESO o SALIDA"}), 400

    # Convertir a Enum de Python
    tipo_evento = TipoEvento.INGRESO if tipo_evento_str == "INGRESO" else TipoEvento.SALIDA

    colegio_id = current_user.colegio_id

    # Buscar estudiante
    filtros = [
        Estudiante.qr_token == identificador,
        Estudiante.documento == identificador,
    ]
    if identificador.isdigit():
        filtros.append(Estudiante.id == int(identificador))

    estudiante = (
        Estudiante.query
        .filter_by(colegio_id=colegio_id)
        .filter(or_(*filtros))
        .first()
    )

    if not estudiante:
        return jsonify({"error": "Estudiante no encontrado"}), 404

    ahora = datetime.now()

    # ──────────────────────────────────────────────────────────────
    # Guardar el registro en ingresos_colegio
    # ──────────────────────────────────────────────────────────────
    registro = IngresoColegio(
        fecha=ahora.date(),
        hora=ahora.time(),
        metodo=metodo,
        creado_en=ahora,
        tipo_evento=tipo_evento,
        estudiante_id=estudiante.id,
        colegio_id=colegio_id,
    )
    db.session.add(registro)
    db.session.commit()

    # ──────────────────────────────────────────────────────────────
    # Decidir si se notifica al acudiente
    # ──────────────────────────────────────────────────────────────
    debe_notificar, motivo = _evaluar_si_notificar(
        estudiante=estudiante,
        tipo_evento=tipo_evento_str,
        hora_actual=ahora.time()
    )

    notificado = False
    if debe_notificar:
        try:
            from app.services.notification_worker import notify_student_movement

            sede_nombre = ""
            if estudiante.sede_id:
                from app.models.sede import Sede
                sede_obj = Sede.query.get(estudiante.sede_id)
                if sede_obj:
                    sede_nombre = sede_obj.nombre

            notificado = notify_student_movement(
                estudiante_id=estudiante.id,
                hora=ahora.strftime('%H:%M'),
                sede_nombre=sede_nombre,
                tipo_evento=tipo_evento_str
            )
        except Exception as e:
            print(f"⚠️ Notificación no enviada: {e}")

    return jsonify({
        "success": True,
        "estudiante": {
            "id": estudiante.id,
            "nombre": f"{estudiante.nombre} {estudiante.apellido or ''}".strip(),
            "documento": estudiante.documento or "",
        },
        "tipo_evento": tipo_evento_str,
        "hora": ahora.strftime("%H:%M:%S"),
        "notificado": notificado,
        "motivo_notificacion": motivo,
    })

# ════════════════════════════════════════════════════════════════
# HELPER: decidir si se notifica según la jornada del estudiante
# ════════════════════════════════════════════════════════════════

def _evaluar_si_notificar(estudiante, tipo_evento, hora_actual):
    """
    Devuelve (debe_notificar: bool, motivo: str).

    Reglas:
      - INGRESO: notificar si hora_actual > hora_inicio + tolerancia
      - SALIDA:  notificar si hora_actual < hora_fin
      - Sin jornada asignada → no notificar
    """
    from datetime import datetime as _dt, timedelta

    if not estudiante.jornada_id:
        return False, "Sin jornada asignada"

    jornada = estudiante.jornada
    if not jornada:
        return False, "Jornada no encontrada"

    if not jornada.hora_inicio or not jornada.hora_fin:
        return False, "Jornada sin horario definido"

    tolerancia = jornada.tolerancia_minutos or 0

    # Convertir time a datetime para poder sumar timedelta
    base = _dt.today()
    hora_inicio_dt = _dt.combine(base, jornada.hora_inicio)
    hora_fin_dt = _dt.combine(base, jornada.hora_fin)
    hora_actual_dt = _dt.combine(base, hora_actual)

    if tipo_evento == "INGRESO":
        limite = hora_inicio_dt + timedelta(minutes=tolerancia)
        if hora_actual_dt > limite:
            return True, f"Llegada tarde (después de {limite.strftime('%H:%M')})"
        return False, "Ingreso dentro del horario"

    if tipo_evento == "SALIDA":
        if hora_actual_dt < hora_fin_dt:
            return True, f"Salida anticipada (antes de {hora_fin_dt.strftime('%H:%M')})"
        return False, "Salida dentro del horario"

    return False, "Tipo de evento desconocido"

# ════════════════════════════════════════════════════════════════
# API: BUSCAR ESTUDIANTES (para autocompletar)
# ════════════════════════════════════════════════════════════════

@portero_bp.route("/buscar")
@login_required
def buscar():
    """Devuelve JSON con estudiantes que coincidan con q."""
    if current_user.rol != 'portero':
        return jsonify({"error": "No autorizado"}), 403

    q = (request.args.get("q") or "").strip()
    if len(q) < 2:
        return jsonify([])

    colegio_id = current_user.colegio_id
    like = f"%{q}%"

    estudiantes = (
        Estudiante.query
        .filter_by(colegio_id=colegio_id, activo=True)
        .filter(
            or_(
                Estudiante.nombre.ilike(like),
                Estudiante.apellido.ilike(like),
                Estudiante.documento.ilike(like),
            )
        )
        .order_by(Estudiante.nombre, Estudiante.apellido)
        .limit(15)
        .all()
    )

    return jsonify([
        {
            "id": e.id,
            "nombre": f"{e.nombre} {e.apellido or ''}".strip(),
            "documento": e.documento or "",
        }
        for e in estudiantes
    ])