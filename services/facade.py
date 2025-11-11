# services/facade.py
from typing import Optional
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash
from models import db, Usuario
from services.factory import VeranoFactory, InviernoFactory, crear_conjunto

class TiendaFacade:
    # ---------- USUARIOS ----------
    def registrar_usuario(
        self,
        usuario: str,
        email: str,
        contrasena: str,
        rol: str = "cliente",
        nombre_completo: Optional[str] = None,
        telefono: Optional[str] = None,
        direccion: Optional[str] = None,
    ) -> Optional[Usuario]:
        u = Usuario(nombre_usuario=usuario, email=email, rol=rol)

        # asigna extras solo si el modelo los tiene
        extras = {
            "nombre_completo": nombre_completo,
            "telefono": telefono,
            "direccion": direccion,
        }
        for k, v in extras.items():
            if v and hasattr(u, k):
                setattr(u, k, v)

        # hash de contraseña
        if hasattr(u, "set_password"):
            u.set_password(contrasena)
        else:
            # compatibilidad por si tu modelo usa contrasena_hash
            if hasattr(u, "contrasena_hash"):
                u.contrasena_hash = generate_password_hash(contrasena)

        try:
            db.session.add(u)
            db.session.commit()
            return u
        except IntegrityError:
            db.session.rollback()
            return None

    def iniciar_sesion(self, usuario_o_email: str, contrasena: str) -> Optional[Usuario]:
        dato = (usuario_o_email or "").lower()
        u = Usuario.query.filter(
            (Usuario.nombre_usuario == dato) | (Usuario.email == dato)
        ).first()
        if not u:
            return None
        if hasattr(u, "verificar_password"):
            return u if u.verificar_password(contrasena) else None
        if hasattr(u, "contrasena_hash"):
            return u if check_password_hash(u.contrasena_hash, contrasena) else None
        return None

    # ---------- PRODUCTOS ----------
    def crear_conjunto_temporada(self, temporada: str, **datos):
        factory = VeranoFactory() if (temporada or "").lower() == "verano" else InviernoFactory()
        prendas = crear_conjunto(factory, **datos)
        db.session.add_all(prendas)
        db.session.commit()
        return prendas
