# app.py
import os
from flask import Flask
from flask_migrate import Migrate
from sqlalchemy import inspect, text

# Tu singleton de config expone 'app' y 'db'
from config_singleton import Configuracion, db

# ================================
# 1) Crear la app desde tu Singleton
# ================================
config = Configuracion()
app = config.app  # Flask app ya configurada (SECRET_KEY, DB, etc.)

# ================================
# 2) Registrar Blueprints (después de tener 'app')
# ================================
from controllers.main_controller import main  # importa después de crear 'app'
app.register_blueprint(main)

# ================================
# 3) Flask-Migrate (Alembic)
# ================================
migrate = Migrate(app, db)

# ================================
# 4) Importar modelos (para que Alembic los vea)
# ================================
from models import (
    Blusa, Bluson, Vestido, Enterizo, Jean, VestidoGala,
    Compra, Usuario, Transaction
)

# ================================
# 5) Diagnóstico opcional
# ================================
RUN_CREATE_ALL = False  # déjalo en False si usas Alembic

with app.app_context():
    if RUN_CREATE_ALL:
        db.create_all()
        print("✅ Tablas creadas automáticamente.")

    insp = inspect(db.engine)
    # Usa 'public' solo si es Postgres
    is_pg = db.engine.url.get_backend_name().startswith("postgres")
    schema = "public" if is_pg else None
    tablas = insp.get_table_names(schema=schema)
    print("📦 Tablas detectadas:", tablas)

# ================================
# 6) Rutas de prueba
# ================================
@app.route("/health")
def health():
    return {"status": "OK", "app": "Flask conectado correctamente"}

@app.route("/dbcheck")
def dbcheck():
    try:
        db.session.execute(text("SELECT 1"))
        return {"database": "ok"}
    except Exception as e:
        return {"database": "error", "detail": str(e)}, 500

@app.route("/tablas")
def tablas():
    insp = inspect(db.engine)
    is_pg = db.engine.url.get_backend_name().startswith("postgres")
    schema = "public" if is_pg else None
    return {"tablas": insp.get_table_names(schema=schema)}

# ================================
# 7) Ejecución local
# ================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
