import os
import markdown
from flask import Blueprint, render_template, abort

docs_bp = Blueprint("docs", __name__, url_prefix="/docs")

DOCS_PATH = os.path.join(os.path.dirname(__file__), "..", "docs")

@docs_bp.route("/")
def index():
    files = sorted(os.listdir(DOCS_PATH))
    return render_template("docs/index.html", files=files)

@docs_bp.route("/<filename>")
def show_doc(filename):
    file_path = os.path.join(DOCS_PATH, filename)

    if not os.path.exists(file_path):
        abort(404)

    with open(file_path, "r", encoding="utf-8") as f:
        content = markdown.markdown(f.read())

    return render_template("docs/doc.html", content=content, filename=filename)