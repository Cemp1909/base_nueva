# config_singleton.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Carga variables de entorno (.env)
load_dotenv()

# Instancia global ÚNICA de SQLAlchemy
db = SQLAlchemy()

class Configuracion:
    """
    Configura la app Flask y registra la única instancia global de SQLAlchemy.
    No registra Migrate aquí (hazlo en app.py).
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_app()
        return cls._instance

    def _init_app(self):
        self.app = Flask(__name__)
        self.app.secret_key = os.getenv("SECRET_KEY", "clave_local")

        # URL desde .env, con fallback a tu Postgres local en 55432 (Docker)
        db_url = os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg://tienda:tienda@localhost:55432/tienda"
        )

        # Normaliza URLs antiguas de Postgres/MySQL
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
        if db_url.startswith("postgresql+psycopg2://"):
            db_url = db_url.replace("postgresql+psycopg2://", "postgresql+psycopg://", 1)
        if db_url.startswith("mysql://"):
            db_url = db_url.replace("mysql://", "mysql+pymysql://", 1)

        self.app.config["SQLALCHEMY_DATABASE_URI"] = db_url
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        # Inicializa SQLAlchemy con ESTA app
        db.init_app(self.app)
