# controllers/main_controller.py
from flask import (
    Blueprint, render_template, request, redirect, url_for,
    flash, session, jsonify, send_from_directory
)
from functools import wraps
import random, time, string, os

# Modelos / DB
from models import (
    db, Compra, Transaction, Usuario,
    Blusa, Bluson, Vestido, Enterizo, Jean, VestidoGala
)

# Fachada de servicios
from services.facade import TiendaFacade

# Abstract Factory
from services.factory import VeranoFactory, InviernoFactory, crear_conjunto

# Errores de BD
from sqlalchemy.exc import IntegrityError

# ---------------------------------------------------------------------
# Blueprint y fachada
# ---------------------------------------------------------------------
main = Blueprint("main", __name__, url_prefix="")
facade = TiendaFacade()

# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------
def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            flash("Debes iniciar sesión", "warning")
            return redirect(url_for("main.login"))
        return view(*args, **kwargs)
    return wrapped

def _gen_tx_id(n=12):
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=n))

def _mask_card(number):
    return number[-4:] if number and len(number) >= 4 else number

# ---------------------------------------------------------------------
# Rutas base
# ---------------------------------------------------------------------
@main.route("/")
def home():
    return render_template("index.html")

@main.route("/favicon.ico")
def favicon():
    filename = "favicon.ico"
    fallback = "imagen2.jpeg"
    target = filename if os.path.exists(os.path.join("static", filename)) else fallback
    mimetype = "image/x-icon" if target.endswith(".ico") else "image/jpeg"
    return send_from_directory("static", target, mimetype=mimetype)

# ---------------------------------------------------------------------
# Catálogo (tus HTML existentes)
# ---------------------------------------------------------------------
@main.route("/blusas")
def blusas():
    return render_template("blusas.html", Blusa=Blusa)

@main.route("/blusones")
def blusones():
    return render_template("blusones.html", Bluson=Bluson)

@main.route("/vestidos")
def vestidos():
    return render_template("vestidos.html", Vestido=Vestido)

@main.route("/enterizos")
def enterizos():
    return render_template("enterizos.html", Enterizo=Enterizo)

@main.route("/jeans")
def jeans():
    return render_template("jeans.html", Jean=Jean)

@main.route("/vestidosgala")
def vestidosgala():
    return render_template("vestidosgala.html", VestidoGala=VestidoGala)


# ---------------------------------------------------------------------
# Autenticación
# ---------------------------------------------------------------------
@main.route("/crear", methods=["GET", "POST"])
def crear_usuario():
    if request.method == "GET":
        return render_template("crear.html")

    # POST
    nombre_completo = (request.form.get("nombre_completo") or "").strip()
    usuario         = (request.form.get("usuario") or "").strip().lower()
    email           = (request.form.get("email") or "").strip().lower()
    telefono        = (request.form.get("telefono") or "").strip()
    direccion       = (request.form.get("direccion") or "").strip()
    rol             = (request.form.get("rol") or "cliente").strip().lower()
    contrasena      = (request.form.get("contrasena") or "").strip()

    faltantes = []
    if not usuario:    faltantes.append("usuario")
    if not email:      faltantes.append("email")
    if not contrasena: faltantes.append("contraseña")
    if faltantes:
        flash(f"Faltan campos: {', '.join(faltantes)}.", "warning")
        return redirect(url_for("main.crear_usuario"))

    try:
        print("➡️ Registrando:", usuario, email)
        u = facade.registrar_usuario(
            usuario=usuario,
            email=email,
            contrasena=contrasena,
            rol=rol,
            nombre_completo=nombre_completo or None,
            telefono=telefono or None,
            direccion=direccion or None,
        )
        if not u:
            # típicamente por duplicado de email/usuario (unicidad)
            print("⛔ registrar_usuario devolvió None (duplicado/validación)")
            flash("El usuario o el correo ya existen. ❌", "warning")
            return redirect(url_for("main.crear_usuario"))

        print("✅ Usuario creado; redirigiendo a /login (303)")
        flash("Usuario creado. Ahora inicia sesión. ✅", "success")
        # 303 fuerza POST->GET en el navegador
        return redirect(url_for("main.login"), code=303)

    except IntegrityError as ie:
        db.session.rollback()
        msg = str(ie.orig) if hasattr(ie, "orig") else str(ie)
        flash(f"Ya existe un usuario o correo registrado. ❌ ({msg})", "danger")
        return redirect(url_for("main.crear_usuario"))
    except Exception as e:
        db.session.rollback()
        print("❌ Error creando usuario:", repr(e))
        flash("Error interno al crear el usuario. Revisa la consola.", "danger")
        return redirect(url_for("main.crear_usuario"))

@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("inicio.html")

    usuario_o_email = (request.form.get("usuario") or "").strip().lower()
    contrasena      = (request.form.get("contrasena") or "").strip()

    u = facade.iniciar_sesion(usuario_o_email, contrasena)
    if u:
        session["user_id"]  = u.id
        session["username"] = u.nombre_usuario
        flash("Has iniciado sesión correctamente ✅", "success")
        return redirect(url_for("main.home"))

    flash("Usuario o contraseña incorrectos ❌", "danger")
    return redirect(url_for("main.login"))

@main.route("/logout")
@login_required
def logout():
    session.clear()
    flash("Sesión cerrada", "info")
    return redirect(url_for("main.login"))

@main.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", username=session.get("username"))

# ---------------------------------------------------------------------
# Flujo de compra
# ---------------------------------------------------------------------
# --- Mostrar formulario de compra (desde links del catálogo) ---
@main.route("/comprar")
def comprar():
    talla = (request.args.get("talla") or "").strip()
    color = (request.args.get("color") or "").strip()
    tipo  = (request.args.get("tipo")  or "").strip()

    precios = {
        "Blusa": 20.00, "Blusas": 20.00,
        "Bluson": 25.00, "Blusones": 25.00,
        "Vestido": 40.00, "Vestidos": 40.00,
        "Enterizo": 35.00, "Enterizos": 35.00,
        "Jean": 30.00, "Jeans": 30.00,
        "Vestido de Gala": 80.00, "Vestidos de Gala": 80.00, "VestidosGala": 80.00
    }

    if not tipo:
        flash("Falta el tipo de producto.", "warning")
        return redirect(url_for("main.home"))

    precio_unitario = precios.get(tipo, 0.0)
    if precio_unitario == 0.0 and tipo.endswith("s"):
        precio_unitario = precios.get(tipo[:-1], 0.0)

    return render_template(
        "formulario_compra.html",
        talla=talla or "", color=color or "", tipo=tipo,
        precio_unitario=precio_unitario, cantidad=1,
        nombre="", direccion="", telefono=""
    )


@main.route("/formulario_compra", methods=["GET", "POST"])
def formulario_compra():
    if request.method == "GET":
        return render_template(
            "formulario_compra.html",
            talla=request.args.get("talla", ""),
            color=request.args.get("color", ""),
            tipo=request.args.get("tipo", ""),
            precio_unitario=float(request.args.get("precio_unitario", 0) or 0),
            cantidad=int(request.args.get("cantidad", 1) or 1),
            nombre="", direccion="", telefono=""
        )

    # --- POST ---
    nombre    = (request.form.get("nombre")    or "").strip()
    direccion = (request.form.get("direccion") or "").strip()
    telefono  = (request.form.get("telefono")  or "").strip()
    talla     = (request.form.get("talla")     or "").strip()
    color     = (request.form.get("color")     or "").strip()
    tipo      = (request.form.get("tipo")      or "").strip()

    # normaliza para comparar contra DB sin problemas de mayúsculas/plurales
    tipo_low  = tipo.lower()
    talla_q   = talla.strip()
    color_q   = color.strip()

    try:
        cantidad = int(request.form.get("cantidad") or 0)
    except ValueError:
        cantidad = 0
    try:
        precio_unitario = float(request.form.get("precio_unitario") or 0)
    except ValueError:
        precio_unitario = 0.0

    faltantes = [k for k, v in {
        "nombre": nombre, "direccion": direccion, "telefono": telefono,
        "tipo": tipo, "talla": talla, "color": color
    }.items() if not v]
    if cantidad <= 0: faltantes.append("cantidad")
    if precio_unitario <= 0: faltantes.append("precio_unitario")

    if faltantes:
        flash(f"Faltan datos: {', '.join(faltantes)}", "warning")
        return render_template(
            "formulario_compra.html",
            nombre=nombre, direccion=direccion, telefono=telefono,
            talla=talla, color=color, tipo=tipo,
            precio_unitario=precio_unitario, cantidad=cantidad
        )

    total = cantidad * precio_unitario

    # ====== DESCUENTO DE STOCK + COMPRA ======
    try:
        # 1) resolver el modelo por tipo (robusto a plurales)
        modelo = None
        if "gala"   in tipo_low: modelo = VestidoGala
        elif "blusa"  in tipo_low: modelo = Blusa
        elif "bluson" in tipo_low: modelo = Bluson
        elif "enterizo" in tipo_low: modelo = Enterizo
        elif "jean"   in tipo_low: modelo = Jean
        elif "vestido" in tipo_low: modelo = Vestido

        if modelo is None:
            raise ValueError(f"Tipo de producto desconocido: {tipo}")

        # 2) buscar variante (case-insensitive) y bloquear si tu backend lo soporta
        #    usamos ILIKE para evitar fallos por mayúsculas/minúsculas/espacios
        producto = (
            modelo.query
            .filter(modelo.talla.ilike(talla_q), modelo.color.ilike(color_q))
            .first()
        )

        if producto is None:
            raise ValueError(f"No existe {tipo} talla {talla} color {color}.")

        if not hasattr(producto, "stock"):
            raise ValueError("El producto no tiene columna 'stock' definida.")

        stock_actual = int(producto.stock or 0)
        if stock_actual < cantidad:
            raise ValueError(f"Stock insuficiente: disponibles {stock_actual}, solicitados {cantidad}.")

        # 3) descontar y registrar compra en la misma transacción
        producto.stock = stock_actual - cantidad

        compra = Compra(
            nombre_cliente=nombre, direccion=direccion, telefono=telefono,
            producto=f"{tipo} - talla {talla}, Color {color}",
            cantidad=cantidad, total=total
        )
        db.session.add(compra)
        db.session.commit()

        stock_restante = int(producto.stock or 0)

    except Exception as e:
        db.session.rollback()
        flash(f"Error al procesar el pedido: {type(e).__name__}: {e}", "danger")
        return render_template(
            "formulario_compra.html",
            nombre=nombre, direccion=direccion, telefono=telefono,
            talla=talla, color=color, tipo=tipo,
            precio_unitario=precio_unitario, cantidad=cantidad
        )

    # Éxito
    flash(f"Compra registrada. Stock restante: {stock_restante}", "success")
    return render_template(
        "pedido_exitoso.html",
        nombre=nombre, tipo=tipo, talla=talla, color=color, total=total
    )



# ---------------------------------------------------------------------
# Utilidades BD
# ---------------------------------------------------------------------
@main.route("/init-db")
def init_db():
    db.create_all()
    return "Tablas creadas correctamente ✅"

@main.route("/db-check")
def db_check():
    try:
        x = Usuario.query.first()
        return f"DB OK. Primer usuario: {x.nombre_usuario if x else 'ninguno'}"
    except Exception as e:
        return f"DB ERROR: {type(e).__name__}: {e}", 500

# ---------------------------------------------------------------------
# Pasarela de pago simulada
# ---------------------------------------------------------------------
@main.route("/pay", methods=["GET"])
def pay():
    amount = request.args.get("amount", 0)
    return render_template("pay.html", amount=amount)


@main.route("/process_payment", methods=["POST"])
def process_payment():
    nombre      = request.form.get("nombre")
    card_number = request.form.get("card_number", "").replace(" ", "")
    exp         = request.form.get("exp")
    cvv         = request.form.get("cvv")
    try:
        amount = float(request.form.get("amount", 0))
    except ValueError:
        amount = 0.0

    if not (nombre and card_number and exp and cvv and amount > 0):
        flash("Datos incompletos del pago.", "danger")
        return redirect(url_for("main.pay", amount=amount))

    time.sleep(1)
    is_success = (random.random() < 0.9)

    tx = Transaction(
        tx_id=_gen_tx_id(),
        amount=amount,
        currency="USD",
        status="success" if is_success else "failed",
        method="card_fake",
        card_last4=_mask_card(card_number),
        card_brand=("VISA" if card_number.startswith("4")
                    else "MC" if card_number.startswith("5")
                    else "UNKNOWN")
    )
    db.session.add(tx)
    db.session.commit()

    return redirect(url_for("main.payment_result", tx_id=tx.tx_id))


@main.route("/payment_result/<tx_id>")
def payment_result(tx_id):
    tx = Transaction.query.filter_by(tx_id=tx_id).first_or_404()
    return render_template("payment_result.html", tx=tx)
# ---------------------------------------------------------------------
# Abstract Factory: conjuntos por temporada
# ---------------------------------------------------------------------
@main.route("/conjunto", methods=["POST"])
@login_required
def crear_conjunto_temporada():
    temporada = (request.form.get("temporada") or "verano").strip().lower()
    datos = {
        "talla":  request.form.get("talla"),
        "color":  request.form.get("color"),
        "tipo":   request.form.get("tipo"),
        "imagen": request.form.get("imagen"),
        "stock":  int(request.form.get("stock", 0) or 0),
    }

    factory = VeranoFactory() if temporada == "verano" else InviernoFactory()
    prendas = crear_conjunto(factory, **datos)
    db.session.add_all(prendas)
    db.session.commit()

    flash(f"Conjunto de {temporada} creado con {len(prendas)} prendas ✅", "success")
    return redirect(url_for("main.home"))

# ---------------------------------------------------------------------
# 404 amable
# ---------------------------------------------------------------------
@main.app_errorhandler(404)
def not_found(e):
    flash("Ruta no encontrada.", "warning")
    return redirect(url_for("main.home"))
