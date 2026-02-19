#!/usr/bin/env python3
"""Accounting insights assistant for operational decision support."""

from __future__ import annotations

import argparse
import csv
import statistics
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable


@dataclass
class Transaction:
    date: datetime
    description: str
    amount: float
    label: str

    @property
    def month(self) -> str:
        return self.date.strftime("%Y-%m")

    @property
    def is_expense(self) -> bool:
        return self.amount < 0


@dataclass
class LabelMetrics:
    count: int
    total: float
    average: float


def load_transactions(csv_path: Path) -> list[Transaction]:
    transactions: list[Transaction] = []
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        expected = {"date", "description", "amount", "label"}
        if not reader.fieldnames or not expected.issubset(set(reader.fieldnames)):
            raise ValueError("CSV must contain these columns: date, description, amount, label")

        for row in reader:
            transactions.append(
                Transaction(
                    date=datetime.strptime(row["date"].strip(), "%Y-%m-%d"),
                    description=row["description"].strip(),
                    amount=float(row["amount"]),
                    label=row["label"].strip().lower(),
                )
            )
    return sorted(transactions, key=lambda txn: txn.date)


def summarize_by_label(transactions: Iterable[Transaction]) -> dict[str, LabelMetrics]:
    grouped: dict[str, list[float]] = defaultdict(list)
    for txn in transactions:
        grouped[txn.label].append(txn.amount)

    summary: dict[str, LabelMetrics] = {}
    for label, amounts in grouped.items():
        total = sum(amounts)
        summary[label] = LabelMetrics(
            count=len(amounts),
            total=total,
            average=total / len(amounts),
        )
    return dict(sorted(summary.items(), key=lambda item: item[1].total, reverse=True))


def monthly_cashflow(transactions: Iterable[Transaction]) -> dict[str, float]:
    monthly_totals: dict[str, float] = defaultdict(float)
    for txn in transactions:
        monthly_totals[txn.month] += txn.amount
    return dict(sorted(monthly_totals.items()))


def detect_expense_anomalies(transactions: Iterable[Transaction]) -> list[Transaction]:
    by_label: dict[str, list[Transaction]] = defaultdict(list)
    for txn in transactions:
        if txn.is_expense:
            by_label[txn.label].append(txn)

    anomalies: list[Transaction] = []
    for label_txns in by_label.values():
        amounts = [abs(txn.amount) for txn in label_txns]
        if len(amounts) < 3:
            continue

        mean = statistics.mean(amounts)
        stdev = statistics.pstdev(amounts)
        threshold = mean + (2 * stdev)
        anomalies.extend(txn for txn in label_txns if abs(txn.amount) > threshold)

    return sorted(anomalies, key=lambda txn: abs(txn.amount), reverse=True)


def find_recurring_expenses(transactions: Iterable[Transaction]) -> list[tuple[str, float, int]]:
    by_description: dict[str, list[Transaction]] = defaultdict(list)
    for txn in transactions:
        if txn.is_expense:
            by_description[txn.description.lower()].append(txn)

    recurring: list[tuple[str, float, int]] = []
    for description, txns in by_description.items():
        unique_months = {txn.month for txn in txns}
        if len(unique_months) < 2:
            continue

        amounts = [abs(txn.amount) for txn in txns]
        baseline = statistics.mean(amounts)
        if baseline == 0:
            continue

        variation = max(amounts) - min(amounts)
        if variation / baseline <= 0.15:
            recurring.append((description, -baseline, len(unique_months)))

    return sorted(recurring, key=lambda item: item[1])


def filter_by_label(transactions: Iterable[Transaction], label: str) -> list[Transaction]:
    normalized = label.strip().lower()
    return [txn for txn in transactions if txn.label == normalized]


def render_label_summary(summary: dict[str, LabelMetrics]) -> str:
    lines = ["Label Performance", "=" * 76, f"{'label':<18} {'count':>5} {'average':>14} {'total':>14}"]
    for label, metric in summary.items():
        lines.append(f"{label:<18} {metric.count:>5} {metric.average:>14.2f} {metric.total:>14.2f}")
    return "\n".join(lines)


def render_cashflow(monthly: dict[str, float]) -> str:
    lines = ["Monthly Net Cashflow", "=" * 76]
    rolling = 0.0
    for month, total in monthly.items():
        rolling += total
        lines.append(f"{month}: {total:>12.2f} | running balance: {rolling:>12.2f}")
    return "\n".join(lines)


def render_anomalies(anomalies: list[Transaction]) -> str:
    lines = ["Potential Expense Anomalies", "=" * 76]
    if not anomalies:
        lines.append("None detected with current data size.")
        return "\n".join(lines)

    for txn in anomalies:
        lines.append(
            f"{txn.date.date()} | {txn.label:<14} | {txn.amount:>10.2f} | {txn.description}"
        )
    return "\n".join(lines)


def render_recurring(recurring: list[tuple[str, float, int]]) -> str:
    lines = ["Recurring Expense Signals", "=" * 76]
    if not recurring:
        lines.append("None detected with current data size.")
        return "\n".join(lines)

    for description, avg_amount, months in recurring:
        lines.append(f"{description:<35} avg {avg_amount:>10.2f} across {months} months")
    return "\n".join(lines)


def render_transactions(transactions: Iterable[Transaction]) -> str:
    lines = ["Matching Transactions", "=" * 76]
    for txn in transactions:
        lines.append(
            f"{txn.date.date()} | {txn.label:<12} | {txn.amount:>10.2f} | {txn.description}"
        )
    return "\n".join(lines)


def build_recommendations(
    monthly: dict[str, float],
    anomalies: list[Transaction],
    recurring: list[tuple[str, float, int]],
) -> list[str]:
    recommendations: list[str] = []
    months = list(monthly.values())
    if months and sum(months) < 0:
        recommendations.append(
            "Your period net cashflow is negative. Prioritize reducing non-essential recurring costs."
        )
    if len(months) >= 2 and months[-1] < months[-2]:
        recommendations.append(
            "Latest month declined versus previous month; review delayed receivables and spending spikes."
        )
    if anomalies:
        recommendations.append(
            f"Review {len(anomalies)} unusually large expense(s) for approvals, duplicates, or one-off events."
        )
    if recurring:
        recommendations.append(
            f"Track {len(recurring)} recurring expense pattern(s) and negotiate high-cost vendors proactively."
        )
    if not recommendations:
        recommendations.append("Financial signals look stable. Continue monitoring monthly trends.")
    return recommendations


def render_recommendations(recommendations: list[str]) -> str:
    lines = ["Actionable Recommendations", "=" * 76]
    lines.extend(f"- {recommendation}" for recommendation in recommendations)
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate accounting insights from labeled transaction data"
    )
    parser.add_argument("csv_file", type=Path, help="Path to transactions CSV file")
    parser.add_argument("--label", help="Optional label filter for transaction detail")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    transactions = load_transactions(args.csv_file)

    label_summary = summarize_by_label(transactions)
    monthly = monthly_cashflow(transactions)
    anomalies = detect_expense_anomalies(transactions)
    recurring = find_recurring_expenses(transactions)
    recommendations = build_recommendations(monthly, anomalies, recurring)

    print(render_label_summary(label_summary))
    print()
    print(render_cashflow(monthly))
    print()
    print(render_anomalies(anomalies))
    print()
    print(render_recurring(recurring))
    print()
    print(render_recommendations(recommendations))

    if args.label:
        filtered = filter_by_label(transactions, args.label)
        print()
        print(render_transactions(filtered))


if __name__ == "__main__":
    main()
