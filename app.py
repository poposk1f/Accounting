#!/usr/bin/env python3
"""Simple accounting assistant for labeled transaction analysis."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class Transaction:
    date: str
    description: str
    amount: float
    label: str


def load_transactions(csv_path: Path) -> list[Transaction]:
    transactions: list[Transaction] = []
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        expected = {"date", "description", "amount", "label"}
        if not reader.fieldnames or not expected.issubset(set(reader.fieldnames)):
            raise ValueError(
                "CSV must contain these columns: date, description, amount, label"
            )

        for row in reader:
            transactions.append(
                Transaction(
                    date=row["date"].strip(),
                    description=row["description"].strip(),
                    amount=float(row["amount"]),
                    label=row["label"].strip().lower(),
                )
            )
    return transactions


def summarize_by_label(transactions: Iterable[Transaction]) -> dict[str, float]:
    totals: dict[str, float] = defaultdict(float)
    for txn in transactions:
        totals[txn.label] += txn.amount
    return dict(sorted(totals.items(), key=lambda item: item[1], reverse=True))


def filter_by_label(transactions: Iterable[Transaction], label: str) -> list[Transaction]:
    normalized = label.strip().lower()
    return [txn for txn in transactions if txn.label == normalized]


def render_summary(summary: dict[str, float]) -> str:
    lines = ["Label Summary", "=" * 40]
    for label, total in summary.items():
        lines.append(f"{label:<20} {total:>12.2f}")
    return "\n".join(lines)


def render_transactions(transactions: Iterable[Transaction]) -> str:
    lines = ["Matching Transactions", "=" * 40]
    for txn in transactions:
        lines.append(f"{txn.date} | {txn.label:<12} | {txn.amount:>10.2f} | {txn.description}")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Analyze accounting transactions from a labeled CSV file"
    )
    parser.add_argument("csv_file", type=Path, help="Path to transactions CSV file")
    parser.add_argument(
        "--label",
        help="Optional label filter (for example: utilities, payroll, software)",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    transactions = load_transactions(args.csv_file)
    print(render_summary(summarize_by_label(transactions)))

    if args.label:
        filtered = filter_by_label(transactions, args.label)
        print()
        print(render_transactions(filtered))


if __name__ == "__main__":
    main()
