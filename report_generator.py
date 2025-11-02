from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import datetime

def generate_pdf_report(results, filename="compliance_report.pdf"):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    c.setTitle("System Compliance Report")

    c.drawString(50, height - 50, "System Compliance Report")
    c.drawString(50, height - 70, f"Generated: {datetime.datetime.now()}")

    y = height - 120
    for check, status, desc in results:
        c.drawString(50, y, f"{check}: {status} - {desc}")
        y -= 20
    c.save()

def generate_text_report(results, filename="compliance_report.txt"):
    with open(filename, "w") as f:
        f.write("System Compliance Report\n")
        f.write(f"Generated: {datetime.datetime.now()}\n\n")
        for check, status, desc in results:
            f.write(f"{check}: {status} - {desc}\n")
