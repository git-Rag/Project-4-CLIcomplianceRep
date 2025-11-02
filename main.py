import argparse
from compliance_checks import run_all_checks
from report_generator import generate_pdf_report, generate_text_report

def main():
    parser = argparse.ArgumentParser(description="CLI Compliance Report Generator")
    parser.add_argument("--export", choices=["pdf", "txt"], default="txt", help="Choose export format")
    args = parser.parse_args()

    results = run_all_checks()

    print("Compliance Check Results:")
    for check, status, desc in results:
        print(f"- {check}: {status} ({desc})")

    if args.export == "pdf":
        generate_pdf_report(results)
        print("\n✅ PDF report saved as 'compliance_report.pdf'")
    else:
        generate_text_report(results)
        print("\n✅ Text report saved as 'compliance_report.txt'")

if __name__ == "__main__":
    main()
