# config.py

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")

    # Move paths INTO the class
    BASE_DIR = BASE_DIR
    INSTANCE_DIR = INSTANCE_DIR
    STATIC_FOLDER = STATIC_DIR
    TEMPLATES_FOLDER = TEMPLATE_DIR

    DATABASE = os.path.join(INSTANCE_DIR, "notes.db")

    DEBUG = True
    REMEMBER_COOKIE_DURATION = 60 * 60 * 24 * 7


class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.environ.get("SECRET_KEY")


class DevelopmentConfig(Config):
    DEBUG = True


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
