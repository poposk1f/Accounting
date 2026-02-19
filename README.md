# Accounting Helper App

A beginner-friendly command-line app that helps with accounting by:

- reading transactions from a CSV file
- grouping totals by `label`
- optionally showing only one label (like `income` or `payroll`)

---

## 1) Install Python (first time only)

If you're new to Python, start here:

1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download Python 3.10+ for your operating system.
3. During installation on Windows, **check** "Add Python to PATH".

After install, open a terminal and verify:

```bash
python --version
```

If that doesn't work, try:

```bash
python3 --version
```

---

## 2) Open a terminal in this project folder

You should be inside the folder that contains:

- `app.py`
- `sample_transactions.csv`

---

## 3) Run the app

### Option A (most systems)

```bash
python app.py sample_transactions.csv
```

### Option B (some macOS/Linux systems)

```bash
python3 app.py sample_transactions.csv
```

You will see a **Label Summary** showing totals per label.

---

## 4) Filter by one label (optional)

Example: show only `income` transactions:

```bash
python app.py sample_transactions.csv --label income
```

(Or use `python3` if your machine needs that.)

---

## 5) Use your own CSV file

You can replace `sample_transactions.csv` with your own CSV, but it must include these columns exactly:

- `date`
- `description`
- `amount` (positive for income, negative for expenses)
- `label`

Example:

```bash
python app.py your_file.csv
```

---

## Common beginner issues

### "python is not recognized"

- Python is not installed, or not added to PATH.
- Reinstall Python and ensure "Add Python to PATH" is enabled.

### "No such file or directory"

- You're in the wrong folder.
- `cd` into the project directory first, then run the command again.

### "CSV must contain these columns..."

- Your CSV headers don't match required names.
- Rename headers to: `date,description,amount,label`.

---

## Example output

```text
Label Summary
========================================
income                    7700.00
utilities                 -120.00
software                  -300.00
tax                       -900.00
payroll                  -1800.00
rent                     -2000.00
```
