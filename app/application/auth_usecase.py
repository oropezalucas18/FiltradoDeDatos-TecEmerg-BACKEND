from app.domain.services.auth_service import AuthService
from app.adapters.output.supabase_repository import SupabaseRepository

class AuthUseCase:

    def __init__(self, user_repo):
        self.user_repo = user_repo
        self.supabase = SupabaseRepository()

    def register(self, email, password, names, lastnames, role):

        # Crear en Firebase + Firestore
        user_id = self.user_repo.register(email, password, names, lastnames, role)

        # Backup en Supabase
        hashed = self.user_repo.hash_password(password)
        self.supabase.save_user_backup(
            email=email,
            hashed_password=hashed,
            names=names,
            lastnames=lastnames,
            role=role,
            status="enabled"
        )

        return {"user_id": user_id}

    def login(self, email, password):
        return self.user_repo.login(email, password)
    
    def disable_user(self, user_id: str):
        return self.user_repo.disable_user(user_id)

    def list_users(self):
        return self.user_repo.list_users()

    def update_role(self, user_id: str, new_role: str):
        return self.user_repo.update_role(user_id, new_role)
