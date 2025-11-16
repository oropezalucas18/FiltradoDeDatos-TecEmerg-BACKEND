import json
import pandas as pd
import numpy as np
import pika
import io
import os
from datetime import datetime

# Reportes
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.tsa.seasonal import seasonal_decompose
from fpdf import FPDF

# Limpieza y validación
from app.domain.services.cleaner_service import CleanerService
from app.domain.services.sensor_validator import SensorValidator

# Repositorios
from app.adapters.output.firebase_repository import FirebaseRepository
from app.adapters.output.supabase_repository import SupabaseRepository

# Config
from app.infrastructure.config import settings

from app.domain.entities.sensor_data import SensorData


# ===========================
#  CONEXIÓN RABBITMQ
# ===========================
def connect_rabbit():
    credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASS)

    parameters = pika.ConnectionParameters(
        host=settings.RABBITMQ_HOST,
        port=5672,
        credentials=credentials
    )

    return pika.BlockingConnection(parameters)


# ===========================
#  FUNCIÓN PARA GENERAR REPORTES PDF
# ===========================
def generate_pdf_report(sensor_type, df):
    report_name = f"Reporte_{sensor_type}_{datetime.utcnow().isoformat()}.pdf"

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # --- PORTADA ---
    pdf.add_page()
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 10, f"Reporte Analítico - Sensor {sensor_type}", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 8, "Gobierno Autónomo Municipal de Cochabamba\n"
                         "Sistema de Monitoreo Ambiental Subterráneo\n"
                         f"Generado el {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    # ===============================
    # 1) HISTOGRAMA
    # ===============================
    try:
        col = df.select_dtypes(include=[np.number]).columns[0]

        plt.figure(figsize=(8, 4))
        plt.hist(df[col], bins=20, color="blue", alpha=0.7)
        plt.title(f"Histograma - {col}")
        plt.xlabel(col)
        plt.ylabel("Frecuencia")
        hist_path = "/tmp/hist.png"
        plt.savefig(hist_path)
        plt.close()

        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Histograma de distribución", ln=True)
        pdf.image(hist_path, x=10, y=30, w=180)
    except Exception as e:
        print("Error histograma:", e)

    # ===============================
    # 2) Q-Q PLOT
    # ===============================
    try:
        stats.probplot(df[col], dist="norm", plot=plt)
        qq_path = "/tmp/qq.png"
        plt.savefig(qq_path)
        plt.close()

        pdf.add_page()
        pdf.cell(0, 10, "Gráfico Q-Q (Normalidad)", ln=True)
        pdf.image(qq_path, x=10, y=30, w=180)
    except:
        pass

    # ===============================
    # 3) BOXPLOT + 6 SIGMA / I-MR
    # ===============================
    try:
        mean = df[col].mean()
        std = df[col].std()

        UCL = mean + 3 * std
        LCL = mean - 3 * std

        plt.figure(figsize=(10, 4))
        plt.plot(df[col], label="Valores")
        plt.axhline(UCL, color="red", linestyle="--", label="UCL")
        plt.axhline(LCL, color="red", linestyle="--", label="LCL")
        plt.axhline(mean, color="green", linestyle="-", label="Media")
        plt.legend()
        imr_path = "/tmp/imr.png"
        plt.savefig(imr_path)
        plt.close()

        pdf.add_page()
        pdf.cell(0, 10, "Gráfico de Control I-MR", ln=True)
        pdf.image(imr_path, x=10, y=30, w=180)
    except:
        pass

    # ===============================
    # 4) BOXPLOT COX
    # ===============================
    try:
        transformed, lmbda = stats.boxcox(df[col].dropna())
        plt.figure(figsize=(8, 4))
        plt.plot(transformed)
        boxcox_path = "/tmp/boxcox.png"
        plt.savefig(boxcox_path)
        plt.close()

        pdf.add_page()
        pdf.cell(0, 10, f"Transformación Box-Cox (λ={round(lmbda,4)})", ln=True)
        pdf.image(boxcox_path, x=10, y=30, w=180)
    except:
        pass

    # ===============================
    # 5) SEASONAL DECOMPOSITION
    # ===============================
    try:
        decomposed = seasonal_decompose(df[col], period=12, model="additive", extrapolate_trend="freq")

        plt.figure(figsize=(10, 6))
        decomposed.plot()
        decomp_path = "/tmp/decompose.png"
        plt.savefig(decomp_path)
        plt.close()

        pdf.add_page()
        pdf.cell(0, 10, "Descomposición temporal (Trend / Seasonal / Residual)", ln=True)
        pdf.image(decomp_path, x=10, y=30, w=180)
    except Exception as e:
        print("Error decomposition:", e)

    output_path = f"/tmp/{report_name}"
    pdf.output(output_path)

    return output_path


# ===========================
#  PROCESAR MENSAJE DE RABBITMQ
# ===========================
def process_message(ch, method, properties, body):
    print(" [✔] Mensaje recibido del broker")

    data = json.loads(body)
    tipo = data["tipo"]
    rows = data["rows"]
    origen = data.get("origen", "archivo")

    df = pd.DataFrame(rows)

    try:
        SensorValidator.validar_campos(tipo, df)
        df = CleanerService.clean(df)
        df = CleanerService.normalize(df)
    except Exception as e:
        print("❌ Error validando o limpiando:", e)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    firebase = FirebaseRepository()
    supabase = SupabaseRepository()

    print(" [✔] Guardando datos en Firebase y Supabase...")

    for r in df.to_dict(orient="records"):
        firebase.save(
            SensorData(
                tipo=tipo,
                valores=r,
                timestamp=r.get("timestamp"),
                origen=origen,
                procesado=True
            )
        )
        supabase.save({
            "tipo": tipo,
            "valores": r,
            "timestamp": r.get("timestamp")
        })

    print(" [✔] Datos guardados. Generando reporte PDF...")

    pdf_path = generate_pdf_report(tipo, df)

    print(" [✔] Subiendo PDF a Supabase Storage...")

    try:
        with open(pdf_path, "rb") as f:
            supabase.client.storage.from_("reportes").upload(
                f"{tipo}/{os.path.basename(pdf_path)}", f, {"content-type": "application/pdf"}
            )
    except Exception as e:
        print("❌ Error subiendo PDF:", e)

    print(" [✔] COMPLETADO ✔")

    ch.basic_ack(delivery_tag=method.delivery_tag)



# ===========================
#  MAIN LOOP DEL WORKER
# ===========================
def main():
    print(" [*] Worker iniciado. Esperando mensajes...")

    connection = connect_rabbit()
    channel = connection.channel()

    channel.queue_declare(queue="sensor_ingest", durable=True)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="sensor_ingest", on_message_callback=process_message)

    channel.start_consuming()


if __name__ == "__main__":
    main()
