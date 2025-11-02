import os, json, datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def save_txt(results, outdir):
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, f"report_{datetime.datetime.now():%Y%m%d_%H%M%S}.txt")
    with open(path, "w") as f:
        for r in results:
            f.write(f"=== {r['name']} ===\nStatus: {r['status']}\n")
            for d in r['details']:
                f.write(f" - {d}\n")
            f.write("\n")
    return path

def save_json(results, outdir):
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, f"report_{datetime.datetime.now():%Y%m%d_%H%M%S}.json")
    with open(path, "w") as f:
        json.dump(results, f, indent=2)
    return path

def save_pdf(results, outdir):
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, f"report_{datetime.datetime.now():%Y%m%d_%H%M%S}.pdf")
    c = canvas.Canvas(path, pagesize=A4)
    w, h = A4
    y = h - 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, "Compliance Report")
    y -= 30
    c.setFont("Helvetica", 10)
    for r in results:
        c.drawString(40, y, f"{r['name']} [{r['status']}]")
        y -= 15
        for d in r["details"]:
            c.drawString(60, y, f"- {d}")
            y -= 12
            if y < 60:
                c.showPage()
                y = h - 50
    c.save()
    return path
