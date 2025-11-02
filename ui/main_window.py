from PyQt6.QtWidgets import (
    QWidget, QPushButton, QTextEdit, QVBoxLayout, QLabel, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from compliance import checks, reports
import traceback, os

class Worker(QThread):
    progress = pyqtSignal(str)
    done = pyqtSignal(list)

    def run(self):
        self.progress.emit("Running compliance checks...\n")
        try:
            results = checks.run_all_checks()
            self.progress.emit("Checks complete.\n")
            self.done.emit(results)
        except Exception as e:
            self.progress.emit("Error: " + str(e) + "\n" + traceback.format_exc())

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SafeCore Compliance Checker")
        self.resize(800, 600)

        self.label = QLabel("<b>SafeCore Compliance Tool</b>")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.text = QTextEdit()
        self.text.setReadOnly(True)

        self.button_run = QPushButton("Run Compliance Checks")
        self.button_run.clicked.connect(self.run_checks)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.text)
        layout.addWidget(self.button_run)
        self.setLayout(layout)

    def run_checks(self):
        self.text.clear()
        self.button_run.setEnabled(False)
        self.worker = Worker()
        self.worker.progress.connect(self.text.insertPlainText)
        self.worker.done.connect(self.on_done)
        self.worker.start()

    def on_done(self, results):
        self.text.append("\n--- Compliance Results ---\n")
        for r in results:
            self.text.append(f"{r['name']}: {r['status']}")
            for d in r['details']:
                self.text.append(f"  - {d}")
            self.text.append("")

        outdir = os.path.join(os.getcwd(), "reports")
        txt = reports.save_txt(results, outdir)
        js = reports.save_json(results, outdir)
        pdf = reports.save_pdf(results, outdir)

        self.text.append(f"\nReports saved to:\n{txt}\n{js}\n{pdf}")
        self.button_run.setEnabled(True)
        QMessageBox.information(self, "Done", f"Reports generated in:\n{outdir}")
