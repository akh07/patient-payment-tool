#!/usr/bin/env python3
"""
Batman Trial Payment Agent — TRP-BATMAN-01
Reads patients.csv, shows who needs payment, fills the form, updates the CSV.
"""

import csv, io, os, sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

SCRIPT_DIR   = Path(__file__).parent
CSV_FILE     = SCRIPT_DIR / "patients.csv"
TEMPLATE_PDF = SCRIPT_DIR / "subject_payment_form_BLANK.pdf"
OUTPUT_DIR   = Path.home() / "Desktop" / "BatmanTrial_Forms"

# Verified field positions on subject_payment_form_BLANK.pdf
PDF_FIELDS = [
    ("Subject ID",  103, 550.3),
    ("Visit Date",  324, 550.3),
    ("First Name",   97, 514.3),
    ("Last Name",   334, 514.3),
    ("Address",     120, 478.3),
    ("City",         65, 442.3),
    ("State",       288, 442.3),
    ("ZIP",         381, 442.3),
    ("Phone",        75, 406.3),
    ("Email",       290, 406.3),
]


def load_csv():
    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save_csv(rows):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def pending(rows):
    return [
        r for r in rows
        if r["Study Completed"].strip().lower() == "yes"
        and r["Payment Done"].strip().lower() != "yes"
    ]


def fill_pdf(patient, output_path):
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=letter)
    c.setFont("Helvetica", 9)
    c.setFillColorRGB(0, 0, 0)
    for col, x, y in PDF_FIELDS:
        val = patient.get(col, "")
        if val:
            c.drawString(x, y, str(val))
    c.save()
    packet.seek(0)

    overlay = PdfReader(packet).pages[0]
    base    = PdfReader(str(TEMPLATE_PDF)).pages[0]
    base.merge_page(overlay)
    writer  = PdfWriter()
    writer.add_page(base)
    with open(output_path, "wb") as f:
        writer.write(f)


def main():
    os.system("clear")
    print("\033[96m" + "=" * 52)
    print("  Batman Trial Payment Agent  |  TRP-BATMAN-01")
    print("=" * 52 + "\033[0m\n")

    all_rows = load_csv()

    while True:
        due = pending(all_rows)

        if not due:
            print("  No pending patients. All done.\n")
            break

        print("\033[93m  Patients pending payment:\033[0m\n")
        for i, p in enumerate(due, 1):
            print(f"  [{i}]  {p['First Name']} {p['Last Name']:<20} "
                  f"{p['Subject ID']:<12} {p['Study Type']}")
        print()

        choice = input("  Pick a number (or q to quit): ").strip()
        if choice.lower() == "q":
            break
        if not choice.isdigit() or not (1 <= int(choice) <= len(due)):
            print("  Invalid — try again.\n")
            continue

        patient = due[int(choice) - 1]
        name    = f"{patient['First Name']} {patient['Last Name']}"
        sid     = patient["Subject ID"]

        print(f"\n  Selected: \033[92m{name}\033[0m  /  {sid}")
        if input("  Confirm? (y/n): ").strip().lower() != "y":
            print("  Cancelled.\n")
            continue

        # Fill and save PDF
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        fname    = f"{sid}_{name.replace(' ','_')}_PaymentForm.pdf"
        out_path = OUTPUT_DIR / fname
        fill_pdf(patient, str(out_path))
        print(f"\n  \033[92m✓ PDF saved:\033[0m  ~/Desktop/BatmanTrial_Forms/{fname}")

        # Update CSV
        for row in all_rows:
            if row["Subject ID"] == sid:
                row["Payment Done"] = "Yes"
        save_csv(all_rows)
        print(f"  \033[92m✓ CSV updated:\033[0m {sid} → Payment Done = Yes")

        os.system(f"open '{OUTPUT_DIR}'")

        print()
        if input("  Another one? (y/n): ").strip().lower() != "y":
            print("\n  Done. Forms saved to ~/Desktop/BatmanTrial_Forms/\n")
            break
        print()


if __name__ == "__main__":
    main()
