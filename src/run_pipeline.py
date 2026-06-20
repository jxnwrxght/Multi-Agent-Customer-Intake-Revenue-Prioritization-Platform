"""Command-line entry point for the lead prioritization prototype."""

from __future__ import annotations

import csv
from pathlib import Path

from intake_agent import IntakeAgent
from qualification_agent import QualificationAgent
from routing_agent import RoutingAgent
from scoring_agent import ScoringAgent


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_ROOT / "data" / "inbound_customer_inquiries.csv"
OUTPUT_PATH = PROJECT_ROOT / "outputs" / "prioritized_lead_queue.csv"
SUMMARY_OUTPUT_PATH = PROJECT_ROOT / "outputs" / "lead_summary_metrics.csv"

OUTPUT_COLUMNS = [
    "lead_id",
    "original_message",
    "service_type",
    "issue_summary",
    "urgency",
    "customer_intent",
    "timing_need",
    "missing_info",
    "lead_quality",
    "priority_score",
    "priority_level",
    "routing_decision",
    "routing_reason",
]


def load_leads(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def write_prioritized_leads(path: Path, rows: list[dict[str, str | int]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def calculate_summary_metrics(rows: list[dict[str, str | int]]) -> dict[str, str | int | float]:
    total = len(rows)
    critical = sum(1 for row in rows if row["priority_level"] == "Critical")
    high = sum(1 for row in rows if row["priority_level"] == "High")
    medium = sum(1 for row in rows if row["priority_level"] == "Medium")
    low = sum(1 for row in rows if row["priority_level"] == "Low")
    spam_or_out_of_scope = sum(
        1
        for row in rows
        if row["lead_quality"] in {"Spam", "Out of scope"}
        or row["routing_decision"] == "Ignore/spam"
    )
    average_score = round(
        sum(int(row["priority_score"]) for row in rows) / total,
        2,
    ) if total else 0.0

    return {
        "total_leads_processed": total,
        "critical_leads": critical,
        "high_priority_leads": high,
        "medium_priority_leads": medium,
        "low_priority_leads": low,
        "spam_or_out_of_scope_leads": spam_or_out_of_scope,
        "average_priority_score": average_score,
    }


def write_summary_metrics(path: Path, metrics: dict[str, str | int | float]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(metrics.keys()))
        writer.writeheader()
        writer.writerow(metrics)


def print_summary_metrics(metrics: dict[str, str | int | float]) -> None:
    print(f"Total leads processed: {metrics['total_leads_processed']}")
    print(f"Critical leads: {metrics['critical_leads']}")
    print(f"High priority leads: {metrics['high_priority_leads']}")
    print(f"Medium priority leads: {metrics['medium_priority_leads']}")
    print(f"Low priority leads: {metrics['low_priority_leads']}")
    print(f"Spam/out-of-scope leads: {metrics['spam_or_out_of_scope_leads']}")
    print(f"Average priority score: {metrics['average_priority_score']}")


def process_leads(leads: list[dict[str, str]]) -> list[dict[str, str | int]]:
    intake_agent = IntakeAgent()
    qualification_agent = QualificationAgent()
    scoring_agent = ScoringAgent()
    routing_agent = RoutingAgent()

    processed_rows: list[dict[str, str | int]] = []

    for lead in leads:
        intake = intake_agent.process(lead)
        qualification = qualification_agent.process(intake)
        priority_score, priority_level = scoring_agent.process(intake, qualification)
        routing_decision, routing_reason = routing_agent.process(
            intake,
            qualification,
            priority_score,
            priority_level,
        )

        processed_rows.append(
            {
                "lead_id": lead["lead_id"],
                "original_message": lead["message"],
                "service_type": intake.service_type,
                "issue_summary": intake.issue_summary,
                "urgency": intake.urgency,
                "customer_intent": intake.customer_intent,
                "timing_need": intake.timing_need,
                "missing_info": intake.missing_info,
                "lead_quality": qualification.lead_quality,
                "priority_score": priority_score,
                "priority_level": priority_level,
                "routing_decision": routing_decision,
                "routing_reason": routing_reason,
            }
        )

    return sorted(processed_rows, key=lambda row: int(row["priority_score"]), reverse=True)


def main() -> None:
    leads = load_leads(INPUT_PATH)
    prioritized_leads = process_leads(leads)
    summary_metrics = calculate_summary_metrics(prioritized_leads)
    write_prioritized_leads(OUTPUT_PATH, prioritized_leads)
    write_summary_metrics(SUMMARY_OUTPUT_PATH, summary_metrics)
    print_summary_metrics(summary_metrics)
    print(f"Wrote prioritized output to {OUTPUT_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Wrote summary metrics to {SUMMARY_OUTPUT_PATH.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
