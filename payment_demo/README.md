# Payment Form Agent

Automatically fills subject payment forms from a spreadsheet.
Pick a patient, confirm, get a filled PDF on your Desktop.
Spreadsheet updates automatically to mark them done.

---

## What it does

Reads `patients.csv` for anyone who completed the study but hasn't
been paid yet. You pick one by number, confirm, and a clean filled
PDF drops to your Desktop. The CSV updates automatically so that
patient won't show up again next time.

---

## Setup (one time, 2 minutes)

**1. Install dependencies**

```bash
bash run.sh
```

That's it — `run.sh` installs everything it needs automatically.

**2. Add your patients**

Open `patients.csv` and replace the sample rows with your real patients.
You can do this in Excel, Google Sheets, or any spreadsheet app.
Just keep the column headers exactly as they are.

Required columns (already in the file):
- First Name, Last Name, Subject ID, Visit Date
- Address, City, State, ZIP, Phone, Email
- Study Type (In-Facility or At-Home)
- Study Completed (Yes or No)
- Payment Done (Yes or No) — the agent fills this in automatically

**3. Swap in your form**

Replace `subject_payment_form_BLANK.pdf` with your own blank payment form.
Then open `app.py` and update the `PDF_FIELDS` coordinates to match
where your fields sit on your form.

If you're not sure how to do that, paste your blank PDF into Claude and ask:
"Update the PDF_FIELDS coordinates in this app.py to match my form."
Claude will measure the fields and give you the updated lines to paste in.

---

## Every time you use it

```bash
bash run.sh
```

1. Shows patients where Study Completed = Yes and Payment Done = No
2. Type a number to pick one
3. Confirm (y)
4. PDF saves to ~/Desktop/PaymentForms/
5. CSV updates: that patient's Payment Done → Yes
6. Ask if you need another one — refreshed list, that patient is gone

---

## Files

| File | What it is |
|------|-----------|
| `app.py` | The agent — ~80 lines of Python |
| `run.sh` | Launcher — installs deps and runs the app |
| `patients.csv` | Your participant tracking sheet |
| `subject_payment_form_BLANK.pdf` | Blank form template |

---

## Adapting to your study

Three things to change:

1. **`patients.csv`** — replace sample rows with your patients
2. **`subject_payment_form_BLANK.pdf`** — replace with your blank form
3. **`PDF_FIELDS` in `app.py`** — update coordinates to match your form

Everything else runs as-is.

---

## A note on privacy

This script runs entirely on your local machine.
No data is transmitted, uploaded, or stored anywhere external.
It reads a CSV and writes a PDF — that is all it does.

No patient data is sent to Claude, an API, or any third party.
Compliance with HIPAA, IRB requirements, and institutional data
policies depends on the device and environment you run it on —
same as any local software tool. Ensure your machine meets your
organization's security requirements.

---

## Free to use and adapt

Shared as-is. Take it, change it, make it work for your workflow.
If you want help adjusting it to your own form or sheet structure,
drop it into Claude and ask — it can update the coordinates and
column names in a few minutes.
