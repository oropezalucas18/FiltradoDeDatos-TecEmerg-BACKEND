sensor_schema = {
    "CO2": {
        "campos": [
            "co2", "temperatura", "humedad",
            "bateria", "rssi", "snr", "ubicacion"
        ]
    },
    "Sonido": {
        "campos": [
            "nivel_sonido", "max_sonido", "min_sonido",
            "temperatura", "bateria", "rssi", "snr", "ubicacion"
        ]
    },
    "Soterrado": {
        "campos": [
            "nivel_agua", "distancia", "temperatura",
            "bateria", "rssi", "snr", "ubicacion"
        ]
    }
}

class SensorValidator:

    @staticmethod
    def validar_campos(tipo: str, df):
        """
        Verifica que el dataset contiene SOLO columnas válidas
        para el tipo de sensor.
        """
        columnas = df.columns.tolist()
        campos_validos = sensor_schema[tipo]["campos"]

        for col in columnas:
            if col not in campos_validos and col != "timestamp":
                raise Exception(
                    f"Columna inválida para sensor {tipo}: '{col}' "
                    f"Permitidos: {campos_validos}"
                )

        return True
