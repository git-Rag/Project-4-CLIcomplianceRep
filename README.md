# **CLI Compliance Reporter — Project 4**

This repository contains a portfolio-ready demo of **CLI Compliance Reporter**, a Python project that performs real-time system compliance checks (like firewall, SSH root login, and password policy) and generates a **PDF or text report** using `reportlab`. It also includes a **basic PyQt GUI** to generate reports and view the actions performed.

## **What is included**

**Core Idea:**
Write a command-line tool that runs real system checks (e.g., password policy, SSH root login, firewall status), stores the results, and exports them as a PDF or text report.
**Concepts Covered:** subprocess calls, loops, modular code, reportlab, CLI argument parsing, PyQt5 UI.

## **Run locally**

1. Create a Python environment (Python 3.10+ recommended). *(Optional)*
2. Install dependencies:

   ```bash
   pip install reportlab pyqt5
   ```
3. Run from CLI:

   ```bash
   python main.py --export pdf
   ```
4. Run the GUI:

   ```bash
   python ui_main.py
   ```

