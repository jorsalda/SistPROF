from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, current_user, login_required
from app.services.auth_service import (
    login_usuario,
    registrar_usuario,
    generar_token_reset,
    verificar_token_reset,
    resetear_contrasena_por_email
)
from app.services.email_service import send_reset_email
from app.models.usuario import Usuario
from app.extensions import db
from datetime import datetime
from app.middleware.auth_middleware import acceso_permitido
from flask_limiter.errors import RateLimitExceeded

auth_bp = Blueprint('auth', __name__)


# ⭐⭐ RUTA RAÍZ ⭐⭐
@auth_bp.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.rol == 'superadmin':
            return redirect(url_for('admin.dashboard'))
        else:
            return redirect(url_for('docente.listar'))
    return redirect(url_for('auth.login'))


# ⭐⭐ LOGIN ⭐⭐
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        ok, resultado = login_usuario(
            request.form['email'],
            request.form['password']
        )

        if ok:
            login_user(resultado)
            if resultado.rol == 'superadmin':
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('colegio.dashboard'))
        else:
            flash(resultado, 'danger')

    return render_template('auth/login.html')


# ⭐⭐ LOGOUT ⭐⭐
@auth_bp.route('/logout')
@login_required
@acceso_permitido
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


# ⭐⭐ REGISTRO ⭐⭐
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        ok, mensaje = registrar_usuario(
            request.form['email'],
            request.form['password'],
            request.form['colegio']
        )

        if ok:
            flash(
                "✅ Registro exitoso. Tienes 15 días de prueba gratuita. "
                "Un administrador revisará tu cuenta pronto.",
                "success"
            )
            return redirect(url_for('auth.login'))

        flash(mensaje, 'danger')

    return render_template('auth/register.html')


@auth_bp.route('/test')
def test():
    return render_template('test.html')


# ⭐⭐ ESTADO DE CUENTA ⭐⭐
@auth_bp.route('/estado-cuenta')
@login_required
@acceso_permitido
def estado_cuenta():
    fecha_registro = getattr(current_user, 'fecha_registro', datetime.utcnow())
    dias_transcurridos = (datetime.utcnow() - fecha_registro).days

    dias_prueba = getattr(current_user, 'dias_prueba', 15)
    dias_restantes = max(0, dias_prueba - dias_transcurridos)

    is_approved = getattr(current_user, 'is_approved', False)

    return render_template(
        'auth/estado_cuenta.html',
        dias_restantes=dias_restantes,
        is_approved=is_approved
    )


# ⭐⭐⭐ RECUPERAR CONTRASEÑA (CORREGIDO) ⭐⭐⭐
@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        usuario = Usuario.query.filter_by(email=email).first()

        if not usuario:
            flash("❌ El email no está registrado en nuestro sistema", "danger")
            return redirect(url_for('auth.forgot_password'))

        # ✅ Generar token
        token = generar_token_reset(usuario.email)

        # ✅ Enviar correo
        send_reset_email(usuario.email, token)

        flash(
            "📧 Te hemos enviado un correo con instrucciones para cambiar tu contraseña.",
            "success"
        )
        return redirect(url_for('auth.login'))

    return render_template('auth/forgot_password.html')


# ⭐⭐⭐ RESET DE CONTRASEÑA CON TOKEN ⭐⭐⭐
@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    email = verificar_token_reset(token)

    if not email:
        flash("❌ Token inválido o expirado (tiempo límite: 1 hora)", "danger")
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        nueva_contrasena = request.form['password']

        ok, mensaje = resetear_contrasena_por_email(email, nueva_contrasena)

        if ok:
            flash(
                "✅ Contraseña cambiada exitosamente. Ahora puedes iniciar sesión.",
                "success"
            )
            return redirect(url_for('auth.login'))

        flash(mensaje, "danger")

    return render_template('auth/reset_password.html', token=token)


# ⭐⭐ MANEJADOR DE RATE LIMIT ⭐⭐
@auth_bp.errorhandler(RateLimitExceeded)
def handle_rate_limit(error):
    flash("⚠️ Demasiados intentos. Espera un minuto e intenta de nuevo.", "danger")
    return redirect(url_for('auth.login'))
