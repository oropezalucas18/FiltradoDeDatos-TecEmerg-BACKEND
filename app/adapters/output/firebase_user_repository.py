from firebase_admin import auth
from datetime import datetime

from app.infrastructure.firebase_client import get_db
from app.domain.ports.user_repository_port import UserRepositoryPort
from app.domain.services.auth_service import AuthService
from app.domain.entities.user import User


class FirebaseUserRepository(UserRepositoryPort):

    def __init__(self):
        # ❗ NO guardamos el cliente Firestore como atributo global
        # porque FastAPI intenta deepcopy y CRASHEA.
        pass

    # ==============================
    # Helper interno seguro
    # ==============================
    def _db(self):
        return get_db()   # siempre devuelve un cliente nuevo y seguro

    # ==============================
    # REGISTER
    # ==============================
    def register(self, email, password, names, lastnames, role):

        # Crear usuario en Firebase Authentication
        user_record = auth.create_user(
            email=email,
            password=password,
            disabled=False
        )

        hashed = AuthService.hash_password(password)

        # Guardar usuario en Firestore
        self._db().collection("usuarios").document(user_record.uid).set({
            "email": email,
            "password": hashed,
            "names": names,
            "lastnames": lastnames,
            "role": role,
            "status": "enabled",
            "created_at": datetime.utcnow().isoformat()
        })

        return user_record.uid

    # ==============================
    # LOGIN
    # ==============================
    def login(self, email, password):

        users_ref = (
            self._db()
            .collection("usuarios")
            .where("email", "==", email)
            .limit(1)
            .stream()
        )

        user_doc = next(users_ref, None)

        if not user_doc:
            raise Exception("Usuario no encontrado")

        user_data = user_doc.to_dict()

        if user_data["status"] == "disabled":
            raise Exception("Cuenta deshabilitada")

        if not AuthService.verify_password(password, user_data["password"]):
            raise Exception("Contraseña incorrecta")

        token = AuthService.create_access_token({
            "sub": user_doc.id,
            "email": user_data["email"],
            "names": user_data["names"],
            "lastnames": user_data["lastnames"],
            "role": user_data["role"]
        })

        return {
            "access_token": token,
            "user_id": user_doc.id,
            "email": user_data["email"],
            "names": user_data["names"],
            "lastnames": user_data["lastnames"],
            "role": user_data["role"]
        }

    # ==============================
    # LISTAR
    # ==============================
    def list_users(self):
        users_ref = self._db().collection("usuarios").stream()
        users = []

        for u in users_ref:
            data = u.to_dict()
            data["id"] = u.id
            users.append(data)

        return users

    # ==============================
    # DISABLE
    # ==============================
    def disable_user(self, user_id: str):
        auth.update_user(user_id, disabled=True)

        self._db().collection("usuarios").document(user_id).update({
            "status": "disabled"
        })

        return True

    # ==============================
    # UPDATE ROLE
    # ==============================
    def update_role(self, user_id: str, new_role: str):
        self._db().collection("usuarios").document(user_id).update({
            "role": new_role
        })

        return True

    # ==============================
    # Convertir documento Firestore -> Entidad
    # ==============================
    def to_user(self, data: dict, user_id: str) -> User:
        return User(
            id=user_id,
            email=data.get("email"),
            names=data.get("names"),
            lastnames=data.get("lastnames"),
            password=data.get("password"),
            role=data.get("role"),
            status=data.get("status", "enabled"),
            created_at=data.get("created_at"),
        )

    # ==============================
    # GET BY ID
    # ==============================
    def get_by_id(self, user_id: str):
        snapshot = self._db().collection("usuarios").document(user_id).get()

        if not snapshot.exists:
            return None

        return self.to_user(snapshot.to_dict(), user_id)
    
    def hash_password(self, password: str) -> str:
        return AuthService.hash_password(password)
