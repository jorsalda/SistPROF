from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.extensions import db
from app.models.membresia import Membresia
from app.models.usuario import Usuario
from datetime import datetime, timedelta

membresia_bp = Blueprint('membresia', __name__, url_prefix='/membresia')

from datetime import datetime, timedelta  # Asegúrate de que datetime esté importado


# ... (resto del código) ...

@membresia_bp.route('/admin/gestionar-membresias')
@login_required
def gestionar_membresias():
    """Lista todas las membresías pendientes del colegio."""

    if current_user.rol not in ['admin_colegio', 'superadmin']:
        flash("Acceso no autorizado", "danger")
        return redirect(url_for('auth.login'))

    membresias_pendientes = Membresia.query.join(
        Usuario, Membresia.usuario_id == Usuario.id
    ).filter(
        Usuario.colegio_id == current_user.colegio_id,
        Membresia.estado == 'pendiente'
    ).order_by(Membresia.fecha_inicio.desc()).all()

    membresias_aprobadas = Membresia.query.join(
        Usuario, Membresia.usuario_id == Usuario.id
    ).filter(
        Usuario.colegio_id == current_user.colegio_id,
        Membresia.estado == 'aprobado'
    ).order_by(Membresia.fecha_pago.desc()).limit(10).all()

    return render_template(
        'membresia/gestionar_membresias.html',
        membresias_pendientes=membresias_pendientes,
        membresias_aprobadas=membresias_aprobadas,
        hoy=datetime.utcnow()  # ← ✅ AGREGAR ESTA LÍNEA
    )

@membresia_bp.route('/admin/aprobar/<int:membresia_id>', methods=['POST'])
@login_required
def aprobar_membresia(membresia_id):
    """Aprobar membresía (solo admin del colegio o superadmin)"""

    if current_user.rol not in ['admin_colegio', 'superadmin']:
        flash("Acceso no autorizado", "danger")
        return redirect(url_for('auth.login'))

    membresia = Membresia.query.get_or_404(membresia_id)
    usuario = membresia.usuario  # ✅ CORREGIDO

    if current_user.rol == 'admin_colegio':
        if usuario.colegio_id != current_user.colegio_id:
            flash("No tienes permiso para aprobar esta membresía", "danger")
            return redirect(url_for('membresia.gestionar_membresias'))

    membresia.estado = 'aprobado'
    membresia.fecha_pago = datetime.utcnow()

    usuario.is_approved = True
    if membresia.fecha_fin:
        usuario.fecha_expiracion = membresia.fecha_fin

    db.session.commit()

    flash(f"✅ Membresía {membresia.tipo_plan} aprobada para {usuario.email}", "success")
    return redirect(url_for('membresia.gestionar_membresias'))


@membresia_bp.route('/admin/rechazar/<int:membresia_id>', methods=['POST'])
@login_required
def rechazar_membresia(membresia_id):
    """Rechazar membresía (solo admin del colegio o superadmin)"""

    if current_user.rol not in ['admin_colegio', 'superadmin']:
        flash("Acceso no autorizado", "danger")
        return redirect(url_for('auth.login'))

    membresia = Membresia.query.get_or_404(membresia_id)
    usuario = membresia.usuario  # ✅ CORREGIDO

    if current_user.rol == 'admin_colegio':
        if usuario.colegio_id != current_user.colegio_id:
            flash("No tienes permiso para gestionar esta membresía", "danger")
            return redirect(url_for('membresia.gestionar_membresias'))

    membresia.estado = 'rechazado'

    db.session.commit()

    flash(f"Membresía de {usuario.email} rechazada", "warning")
    return redirect(url_for('membresia.gestionar_membresias'))


@membresia_bp.route('/mi-plan')
@login_required
def ver_mi_plan():
    """El usuario independiente ve el estado de su membresía"""

    membresias = Membresia.query.filter_by(
        usuario_id=current_user.id
    ).order_by(Membresia.fecha_inicio.desc()).all()

    dias_restantes = 0
    if current_user.fecha_expiracion:
        dias_restantes = (current_user.fecha_expiracion - datetime.utcnow()).days

    return render_template(
        'membresia/mi_plan.html',
        membresias=membresias,
        dias_restantes=dias_restantes
    )


@membresia_bp.route('/renovar', methods=['GET', 'POST'])
@login_required
def renovar_membresia():
    """El usuario independiente solicita una membresía"""

    if request.method == 'POST':
        tipo_plan = request.form.get('tipo_plan')
        metodo_pago = request.form.get('metodo_pago', 'transferencia')

        precios = {
            'mensual': 50000,
            'anual': 500000,
            'vitalicio': 1000000
        }

        if tipo_plan not in precios:
            flash("Plan inválido", "danger")
            return redirect(url_for('membresia.renovar_membresia'))

        # Calcular fecha fin según el plan
        if tipo_plan == 'mensual':
            fecha_fin = datetime.utcnow() + timedelta(days=30)
        elif tipo_plan == 'anual':
            fecha_fin = datetime.utcnow() + timedelta(days=365)
        else:
            fecha_fin = None  # Vitalicio no expira

        membresia = Membresia(
            usuario_id=current_user.id,
            tipo_plan=tipo_plan,
            estado='pendiente',
            monto=precios[tipo_plan],
            fecha_fin=fecha_fin,
            metodo_pago=metodo_pago
        )

        db.session.add(membresia)
        db.session.commit()

        flash(
            f"✅ Solicitud de membresía {tipo_plan} enviada. "
            f"Valor: ${precios[tipo_plan]:,.0f} COP. "
            f"El administrador la revisará pronto.",
            "success"
        )

        return redirect(url_for('membresia.ver_mi_plan'))

    return render_template('membresia/renovar.html')