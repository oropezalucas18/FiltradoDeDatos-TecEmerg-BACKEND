from app.infrastructure.supabase_client import supabase_client
from app.infrastructure.config import settings

class SupabaseRepository:

    TABLE = "sensores"  # backup general JSONB

    def save(self, data: dict):
        supabase_client.table(self.TABLE).insert(data).execute()

    # ==============================================
    # GUARDADO EN TABLAS FIJAS (NO ESCALABLES)
    # ==============================================

    def save_co2_fixed(self, row):
        supabase_client.table("em500_aire").insert({
            "timestamp": row.get("timestamp"),
            "co2": row.get("co2"),
            "temperatura": row.get("temperatura"),
            "humedad": row.get("humedad"),
            "bateria": row.get("bateria"),
            "rssi": row.get("rssi"),
            "snr": row.get("snr"),
            "ubicacion": row.get("ubicacion")
        }).execute()

    def save_sonido_fixed(self, row):
        supabase_client.table("ws302_sonido").insert({
            "timestamp": row.get("timestamp"),
            "nivel_sonido": row.get("nivel_sonido"),
            "max_sonido": row.get("max_sonido"),
            "min_sonido": row.get("min_sonido"),
            "temperatura": row.get("temperatura"),
            "bateria": row.get("bateria"),
            "rssi": row.get("rssi"),
            "snr": row.get("snr"),
            "ubicacion": row.get("ubicacion")
        }).execute()

    def save_soterrado_fixed(self, row):
        supabase_client.table("em310_soterrados").insert({
            "timestamp": row.get("timestamp"),
            "nivel_agua": row.get("nivel_agua"),
            "distancia": row.get("distancia"),
            "temperatura": row.get("temperatura"),
            "bateria": row.get("bateria"),
            "rssi": row.get("rssi"),
            "snr": row.get("snr"),
            "ubicacion": row.get("ubicacion")
        }).execute()

    def save_user_backup(self, email, hashed_password, names, lastnames, role, status="enabled"):
        supabase_client.table("usuarios").insert({
            "email": email,
            "hashed_password": hashed_password,
            "names": names,
            "lastnames": lastnames,
            "role": role,
            "status": status
        }).execute()
