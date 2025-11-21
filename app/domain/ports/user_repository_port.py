from abc import ABC, abstractmethod

class UserRepositoryPort(ABC):

    @abstractmethod
    def register(self, email, password, names, lastnames, role): pass

    @abstractmethod
    def login(self, email, password): pass

    @abstractmethod
    def get_by_id(self, user_id: str): pass

    @abstractmethod
    def list_users(self): pass

    @abstractmethod
    def disable_user(self, user_id: str): pass

    @abstractmethod
    def update_role(self, user_id: str, new_role: str): pass

    