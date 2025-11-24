# app_modules/auth.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from . import get_db
from .models import User, get_user_by_username

auth_bp = Blueprint("auth", __name__, template_folder="../template", url_prefix="/auth")


# -------------------------
# REGISTER
# -------------------------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        confirm = request.form.get("confirm_password", "").strip()

        # Basic validation
        if not username or not password or not confirm:
            flash("All fields are required.")
            return render_template("register.html")

        if password != confirm:
            flash("Passwords do not match.")
            return render_template("register.html")

        # Check if user already exists
        db = get_db()
        existing = get_user_by_username(username)

        if existing:
            flash("Username already exists. Choose another.")
            return render_template("register.html")

        # Create user
        hashed = generate_password_hash(password)
        db.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, hashed),
        )
        db.commit()

        flash("Registration successful. Please log in.")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


# -------------------------
# LOGIN
# -------------------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            flash("Username and password are required.")
            return render_template("login.html")

        user = get_user_by_username(username)

        if not user:
            flash("Invalid username or password.")
            return render_template("login.html")

        if not check_password_hash(user.password_hash, password):
            flash("Invalid username or password.")
            return render_template("login.html")

        # Log the user in
        login_user(user)
        return redirect(url_for("notes.dashboard"))

    return render_template("login.html")



# -------------------------
# LOGOUT
# -------------------------
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
