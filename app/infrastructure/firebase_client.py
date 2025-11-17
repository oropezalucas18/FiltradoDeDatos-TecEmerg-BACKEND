import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path
from app.infrastructure.config import settings

firebase_app = None
firebase_db = None


def init_firebase():
    global firebase_app, firebase_db

    if firebase_app is not None:
        return firebase_app

    cred_path = Path(settings.FIREBASE_CREDENTIALS_PATH)

    if not cred_path.exists():
        print("❌ ERROR: Firebase credentials file NOT FOUND:", cred_path)
        print("⚠️ Firebase will NOT initialize. Only login without Firestore will work.")
        return None

    try:
        cred = credentials.Certificate(str(cred_path))
        firebase_app = firebase_admin.initialize_app(cred)
        firebase_db = firestore.client()
        print("🔥 Firebase initialized successfully")
    except Exception as e:
        print("❌ Firebase initialization FAILED:", e)
        firebase_app = None
        firebase_db = None

    return firebase_app


def get_db():
    if firebase_app is None:
        init_firebase()

    return firebase_db
