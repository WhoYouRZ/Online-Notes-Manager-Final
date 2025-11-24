# app_modules/__init__.py

import os
import sqlite3
from flask import Flask, g, current_app, redirect, url_for, render_template
from flask_login import LoginManager, current_user

from config import Config  # import project-wide paths

# Flask-Login manager
login_manager = LoginManager()
login_manager.login_view = "auth.login"


# ======================================================
# DATABASE HELPERS
# ======================================================

def get_db():
    """Return SQLite DB connection for this request."""
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    """Close DB connection after request."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Initialize DB schema using models.create_tables()."""
    from .models import create_tables
    db = get_db()
    create_tables(db)


# ======================================================
# APP FACTORY
# ======================================================

def create_app(test_config=None):
    """
    Application factory for Online Notes Manager.
    """

    # -----------------------------------------------
    # FORCE FLASK TO USE THE ROOT /static AND /templates
    # -----------------------------------------------
    app = Flask(
        __name__,
        static_folder=Config.STATIC_FOLDER,
        template_folder=Config.TEMPLATES_FOLDER,
        instance_relative_config=True
    )

    # Default configuration
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-change-me"),
        DATABASE=os.path.join(Config.INSTANCE_DIR, "notes.db"),
        DEBUG=True
    )

    # Apply test overrides (used in app.py)
    if test_config is not None:
        app.config.update(test_config)

    # Ensure instance folder exists
    os.makedirs(Config.INSTANCE_DIR, exist_ok=True)

    # Teardown DB after request
    app.teardown_appcontext(close_db)

    # Initialize Flask-Login
    login_manager.init_app(app)

    # Avoid circular imports
    from .models import get_user_by_id
    from .auth import auth_bp
    from .notes import notes_bp
    from .main import main_bp
    from .categories import categories_bp

    # User loader for LoginManager
    @login_manager.user_loader
    def load_user(user_id):
        return get_user_by_id(user_id)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(notes_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(categories_bp)

    # -----------------------------------------------
    # ROOT ROUTE (Homepage: guest mode or dashboard)
    # -----------------------------------------------
    @app.route("/")
    def index():
        if current_user.is_authenticated:
            return redirect(url_for("notes.dashboard"))
        return render_template("index.html")

    # DB Init CLI
    import click
    @app.cli.command("init-db")
    def init_db_command():
        init_db()
        click.echo("Initialized the database.")

    return app


__all__ = [
    "create_app",
    "get_db",
    "init_db",
    "login_manager",
]
