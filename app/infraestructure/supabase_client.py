from supabase import create_client
from app.infrastructure.config import settings

supabase = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_KEY
)

# Acceso corto
supabase_client = supabase
