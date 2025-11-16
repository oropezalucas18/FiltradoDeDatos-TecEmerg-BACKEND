import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.tsa.seasonal import seasonal_decompose
from fpdf import FPDF
from datetime import datetime
import pandas as pd
import numpy as np
import os

class ReportGenerator:

    def generate(self, sensor_type: str, df: pd.DataFrame):
        report_name = f"Reporte_{sensor_type}_{datetime.utcnow().isoformat()}.pdf"
        output_path = f"/tmp/{report_name}"

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)

        # =============================
        # PORTADA
        # =============================
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, f"Reporte Analítico - {sensor_type}", ln=True, align="C")
        pdf.ln(5)
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 8,
            "Gobierno Autónomo Municipal de Cochabamba\n"
            "Sistema de Monitoreo Ambiental Subterráneo\n"
            f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        )

        # Número de filas
        pdf.ln(10)
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, f"Total de registros procesados: {len(df)}")

        # Usamos primera columna numérica
        col = df.select_dtypes(include=[np.number]).columns[0]

        # =============================
        # HISTOGRAMA
        # =============================
        try:
            hist_path = "/tmp/hist.png"
            plt.figure(figsize=(8, 4))
            plt.hist(df[col], bins=20, color="blue", alpha=0.7)
            plt.title(f"Histograma - {col}")
            plt.savefig(hist_path)
            plt.close()

            pdf.add_page()
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, "Histograma", ln=True)
            pdf.image(hist_path, x=10, y=30, w=180)
        except:
            pass

        # =============================
        # Q-Q PLOT
        # =============================
        try:
            qq_path = "/tmp/qq.png"
            stats.probplot(df[col], dist="norm", plot=plt)
            plt.savefig(qq_path)
            plt.close()

            pdf.add_page()
            pdf.cell(0, 10, "Gráfico Q-Q (Normalidad)", ln=True)
            pdf.image(qq_path, x=10, y=30, w=180)
        except:
            pass

        # =============================
        # CONTROL I-MR
        # =============================
        try:
            mean = df[col].mean()
            std = df[col].std()
            UCL = mean + 3 * std
            LCL = mean - 3 * std

            imr_path = "/tmp/imr.png"

            plt.figure(figsize=(10, 4))
            plt.plot(df[col])
            plt.axhline(mean, color="green")
            plt.axhline(UCL, color="red", linestyle="--")
            plt.axhline(LCL, color="red", linestyle="--")
            plt.savefig(imr_path)
            plt.close()

            pdf.add_page()
            pdf.cell(0, 10, "Gráfico de Control I-MR", ln=True)
            pdf.image(imr_path, x=10, y=30, w=180)
        except:
            pass

        # =============================
        # BOx-COX
        # =============================
        try:
            boxcox_path = "/tmp/boxcox.png"
            transformed, lmbda = stats.boxcox(df[col].dropna())
            plt.figure(figsize=(10, 4))
            plt.plot(transformed)
            plt.savefig(boxcox_path)
            plt.close()

            pdf.add_page()
            pdf.cell(0, 10, f"Transformación Box-Cox (λ={round(lmbda,4)})", ln=True)
            pdf.image(boxcox_path, x=10, y=30, w=180)
        except:
            pass

        # =============================
        # DESCOMPOSICIÓN TEMPORAL
        # =============================
        try:
            decomp_path = "/tmp/decomp.png"
            decomposed = seasonal_decompose(df[col], model="additive", period=12)
            decomposed.plot()
            plt.savefig(decomp_path)
            plt.close()

            pdf.add_page()
            pdf.cell(0, 10, "Descomposición Temporal", ln=True)
            pdf.image(decomp_path, x=10, y=30, w=180)
        except:
            pass

        pdf.output(output_path)
        return output_path
