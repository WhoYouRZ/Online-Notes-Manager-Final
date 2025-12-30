# app_modules/auth.py

from flask import Blueprint, render_template
from flask_login import login_required


main_bp = Blueprint("main", __name__, template_folder="../template")

@main_bp.route("/")
def index():
    return render_template("index.html")

@main_bp.route("/category")
@login_required
def category_page():
    return render_template("category.html")