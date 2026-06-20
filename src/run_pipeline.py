"""Run the full customer inquiry intake, scoring, and routing workflow."""

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
EXECUTIVE_SUMMARY_PATH = PROJECT_ROOT / "outputs" / "executive_summary.md"

OUTPUT_COLUMNS = ["Lead ID", "Original Message", "Service Type", "Issue Summary", "Urgency", "Customer Intent", "Timing Need", "Missing Information", "Lead Quality", "Priority Score", "Priority Level", "Routing Decision", "Routing Reason"]
METRIC_LABELS = ["Total Inquiries Processed", "Critical Priority Leads", "High Priority Leads", "Medium Priority Leads", "Low Priority Leads", "Spam / Out-of-Scope Leads", "Average Priority Score"]


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
    metrics = {
        "Total Inquiries Processed": total,
        "Critical Priority Leads": sum(1 for row in rows if row["Priority Level"] == "Critical"),
        "High Priority Leads": sum(1 for row in rows if row["Priority Level"] == "High"),
        "Medium Priority Leads": sum(1 for row in rows if row["Priority Level"] == "Medium"),
        "Low Priority Leads": sum(1 for row in rows if row["Priority Level"] == "Low"),
        "Spam / Out-of-Scope Leads": sum(1 for row in rows if row["Lead Quality"] in {"Spam", "Out of scope"} or row["Routing Decision"] == "Ignore/spam"),
        "Average Priority Score": round(sum(int(row["Priority Score"]) for row in rows) / total, 2) if total else 0.0,
    }
    return metrics


def write_summary_metrics(path: Path, metrics: dict[str, str | int | float]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=METRIC_LABELS)
        writer.writeheader()
        writer.writerow(metrics)


def write_executive_summary(path: Path, metrics: dict[str, str | int | float]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    report = f"""# Executive Summary

## Customer Intake Prioritization Run

This report summarizes the results of a local multi-agent workflow that reviewed inbound customer inquiries, scored operational priority, and routed each lead to a recommended next action.

| Metric | Result |
| --- | ---: |
| Total Inquiries Processed | {metrics['Total Inquiries Processed']} |
| Critical Priority Leads | {metrics['Critical Priority Leads']} |
| High Priority Leads | {metrics['High Priority Leads']} |
| Medium Priority Leads | {metrics['Medium Priority Leads']} |
| Low Priority Leads | {metrics['Low Priority Leads']} |
| Spam / Out-of-Scope Leads | {metrics['Spam / Out-of-Scope Leads']} |
| Average Priority Score | {metrics['Average Priority Score']} |

## Business Interpretation

The workflow separated urgent, actionable service requests from lower-priority inquiries and non-actionable messages. Critical and high-priority leads represent the queue items most likely to need fast human attention, while spam and out-of-scope inquiries can be filtered away from the operating team.

For a service business, this kind of triage can help reduce missed emergencies, protect response time, and give office staff a clearer daily lead queue.
"""
    path.write_text(report, encoding="utf-8")


def print_summary_metrics(metrics: dict[str, str | int | float]) -> None:
    for label in METRIC_LABELS:
        print(f"{label}: {metrics[label]}")


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
        routing_decision, routing_reason = routing_agent.process(intake, qualification, priority_score, priority_level)
        processed_rows.append({
            "Lead ID": lead["lead_id"],
            "Original Message": lead["message"],
            "Service Type": intake.service_type,
            "Issue Summary": intake.issue_summary,
            "Urgency": intake.urgency,
            "Customer Intent": intake.customer_intent,
            "Timing Need": intake.timing_need,
            "Missing Information": intake.missing_info,
            "Lead Quality": qualification.lead_quality,
            "Priority Score": priority_score,
            "Priority Level": priority_level,
            "Routing Decision": routing_decision,
            "Routing Reason": routing_reason,
        })
    return sorted(processed_rows, key=lambda row: int(row["Priority Score"]), reverse=True)


def main() -> None:
    leads = load_leads(INPUT_PATH)
    prioritized_leads = process_leads(leads)
    summary_metrics = calculate_summary_metrics(prioritized_leads)
    write_prioritized_leads(OUTPUT_PATH, prioritized_leads)
    write_summary_metrics(SUMMARY_OUTPUT_PATH, summary_metrics)
    write_executive_summary(EXECUTIVE_SUMMARY_PATH, summary_metrics)
    print_summary_metrics(summary_metrics)
    print(f"Wrote prioritized output to {OUTPUT_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Wrote summary metrics to {SUMMARY_OUTPUT_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Wrote executive summary to {EXECUTIVE_SUMMARY_PATH.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
