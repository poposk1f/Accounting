# Accounting Helper App

A lightweight command-line app to make accounting workflows easier by analyzing transactions and sorting totals by label.

## What it does

- Reads a CSV of accounting transactions.
- Groups totals by `label` (sorted highest to lowest).
- Optionally filters transactions for a single label.

This can quickly answer questions like:

- "How much did we spend on payroll this month?"
- "Which categories have the biggest cash impact?"

## CSV format

Your CSV must include the following columns:

- `date`
- `description`
- `amount` (positive for income, negative for expenses)
- `label`

## Usage

```bash
python app.py sample_transactions.csv
```

Filter to a specific label:

```bash
python app.py sample_transactions.csv --label income
```

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
