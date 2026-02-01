# app/routes/auth_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.services.auth_service import login_usuario, registrar_usuario
from app.extensions import db

auth_bp = Blueprint('auth', __name__)


# ⭐⭐ RUTA RAÍZ ⭐⭐
@auth_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('permiso.listado'))  # ✅ CORREGIDO: "listado"
    return redirect(url_for('auth.login'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        ok, resultado = login_usuario(
            request.form['email'],
            request.form['password']
        )

        if ok:
            login_user(resultado)
            return redirect(url_for('permiso.listado'))  # ✅ CORREGIDO: ir a LISTA, no formulario

        flash(resultado, 'danger')

    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        ok, mensaje = registrar_usuario(
            request.form['email'],
            request.form['password'],
            request.form['colegio']
        )

        if ok:
            flash("Registro exitoso. Ahora puedes iniciar sesión.", "success")
            return redirect(url_for('auth.login'))

        flash(mensaje, 'danger')

    return render_template('auth/register.html')