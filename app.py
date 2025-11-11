# app.py
import os
from flask import Flask
from flask_migrate import Migrate, upgrade
from sqlalchemy import inspect, text

# ================================
# 1) Tu singleton de config expone 'app' y 'db'
# ================================
from config_singleton import Configuracion, db

# Crear la app desde el singleton
config = Configuracion()
app = config.app  # Flask app ya configurada (SECRET_KEY, DB, etc.)

# ================================
# 2) Registrar Blueprints (después de tener 'app')
# ================================
from controllers.main_controller import main
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
# 5) Aplicar migraciones o crear tablas (solo primera vez)
# ================================
AUTO_MIGRATE = os.getenv("AUTO_MIGRATE", "1") == "1"

with app.app_context():
    if AUTO_MIGRATE:
        try:
            upgrade()  # aplica migraciones si existe carpeta migrations/
            app.logger.info("✅ Alembic upgrade OK")
        except Exception as e:
            app.logger.error(f"❌ Error en upgrade(): {e}. Intentando create_all()…")
            try:
                db.create_all()  # crea tablas si no hay migrations
                app.logger.info("✅ create_all() OK (sin migrations)")
            except Exception as e2:
                app.logger.error(f"❌ Error en create_all(): {e2}")

# ================================
# 6) Diagnóstico opcional de tablas
# ================================
with app.app_context():
    try:
        insp = inspect(db.engine)
        is_pg = db.engine.url.get_backend_name().startswith("postgres")
        schema = "public" if is_pg else None
        tablas = insp.get_table_names(schema=schema)
        print("📦 Tablas detectadas:", tablas)
    except Exception as e:
        print("⚠️ Error al inspeccionar tablas:", e)

# ================================
# 7) Rutas de prueba
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
# 8) Ejecución local
# ================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
