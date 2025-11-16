import firebase_admin
from firebase_admin import credentials, firestore
from app.infrastructure.config import settings

# Inicializar Firebase solo una vez
if not firebase_admin._apps:
    cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS)
    firebase_admin.initialize_app(cred)

firebase_db = firestore.client()
