from uuid import uuid4
from app.infrastructure.firebase_client import firebase_db
from app.domain.entities.user import User
from app.domain.ports.user_repository_port import UserRepositoryPort

class FirebaseUserRepository(UserRepositoryPort):

    COLLECTION = "usuarios"

    def save(self, user: User):
        firebase_db.collection(self.COLLECTION).document(user.id).set(user.dict())

    def get_by_email(self, email: str):
        docs = firebase_db.collection(self.COLLECTION).where("email", "==", email).stream()
        for doc in docs:
            return User(**doc.to_dict())
        return None

    def get_by_id(self, user_id: str):
        doc = firebase_db.collection(self.COLLECTION).document(user_id).get()
        if doc.exists:
            return User(**doc.to_dict())
        return None
