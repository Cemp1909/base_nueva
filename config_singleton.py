# config_singleton.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Carga variables del archivo .env (solo útil en local)
load_dotenv()

# Instancia global única de SQLAlchemy
db = SQLAlchemy()

class Configuracion:
    """
    Configura la app Flask y registra la única instancia global de SQLAlchemy.
    Compatible con entorno local y Render.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_app()
        return cls._instance

    def _init_app(self):
        self.app = Flask(__name__)

        # ==========================
        # 1️⃣ SECRET_KEY
        # ==========================
        self.app.secret_key = os.getenv("SECRET_KEY", "clave_local_segura")

        # ==========================
        # 2️⃣ DATABASE_URL
        # ==========================
        # Usa la de Render si existe, o una local si estás en tu Mac o Docker
        db_url = os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg://tienda:tienda@localhost:55432/tienda"
        ).strip()

        # Corrige prefijos antiguos de Postgres
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
        if db_url.startswith("postgresql+psycopg2://"):
            db_url = db_url.replace("postgresql+psycopg2://", "postgresql+psycopg://", 1)
        if db_url.startswith("mysql://"):
            db_url = db_url.replace("mysql://", "mysql+pymysql://", 1)

        # ==========================
        # 3️⃣ Configuración SQLAlchemy
        # ==========================
        self.app.config.update(
            SQLALCHEMY_DATABASE_URI=db_url,
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            SQLALCHEMY_ENGINE_OPTIONS={
                "pool_pre_ping": True,    # Reconecta si Render duerme la instancia
                "pool_recycle": 280,      # Evita timeout de conexiones inactivas
            },
        )

        # Inicializa SQLAlchemy con esta app
        db.init_app(self.app)
