from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models.docente import Docente

docente_bp = Blueprint("docente", __name__, url_prefix="/docentes")


# Listar docentes
@docente_bp.route("/")
@login_required
def listar():
    docentes = Docente.query.filter_by(
        colegio_id=current_user.colegio_id
    ).all()
    return render_template("docentes/listado.html", docentes=docentes)


# Formulario nuevo docente
@docente_bp.route("/nuevo", methods=["GET", "POST"])
@login_required
def nuevo():
    if request.method == "POST":
        nombre = request.form.get("nombre").strip()

        if not nombre:
            flash("El nombre del docente es requerido", "danger")
            return redirect(url_for("docente.nuevo"))

        # Verificar si ya existe
        existe = Docente.query.filter_by(
            nombre=nombre,
            colegio_id=current_user.colegio_id
        ).first()

        if existe:
            flash("Este docente ya está registrado", "warning")
            return redirect(url_for("docente.nuevo"))

        # Crear docente
        docente = Docente(
            nombre=nombre,
            colegio_id=current_user.colegio_id
        )

        db.session.add(docente)
        db.session.commit()

        flash("Docente registrado correctamente", "success")
        return redirect(url_for("docente.listar"))

    return render_template("docentes/formulario.html")