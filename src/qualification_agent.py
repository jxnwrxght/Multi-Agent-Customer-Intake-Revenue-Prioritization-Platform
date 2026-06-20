"""Qualification Agent: determines whether a lead is actionable and worth follow-up."""

from __future__ import annotations

from dataclasses import dataclass

from intake_agent import IntakeResult


@dataclass(frozen=True)
class QualificationResult:
    in_scope: bool
    revenue_generating: bool
    actionable: bool
    follow_up_needed: bool
    completeness: str
    lead_quality: str


class QualificationAgent:
    """Checks scope, completeness, actionability, and lead quality."""

    IN_SCOPE_SERVICES = {"HVAC", "Plumbing", "Electrical", "Cleaning"}

    def process(self, intake: IntakeResult) -> QualificationResult:
        in_scope = intake.service_type in self.IN_SCOPE_SERVICES
        revenue_generating = intake.customer_intent in {
            "Request service",
            "Request quote",
            "Book installation",
            "Request maintenance",
            "Existing customer follow-up",
        }
        follow_up_needed = intake.missing_info != "None"
        completeness = "Complete" if not follow_up_needed else "Incomplete"
        actionable = in_scope and not follow_up_needed
        lead_quality = self._classify_quality(
            intake,
            in_scope,
            revenue_generating,
            actionable,
            follow_up_needed,
        )

        return QualificationResult(
            in_scope=in_scope,
            revenue_generating=revenue_generating,
            actionable=actionable,
            follow_up_needed=follow_up_needed,
            completeness=completeness,
            lead_quality=lead_quality,
        )

    def _classify_quality(
        self,
        intake: IntakeResult,
        in_scope: bool,
        revenue_generating: bool,
        actionable: bool,
        follow_up_needed: bool,
    ) -> str:
        if not in_scope and intake.customer_intent == "Spam or opt-out":
            return "Spam"
        if intake.service_type == "Unknown":
            return "Needs follow-up"
        if not in_scope:
            return "Out of scope"
        if not revenue_generating:
            return "Low"
        if actionable and intake.urgency in {"Emergency", "High"}:
            return "High"
        if actionable:
            return "Medium"
        if follow_up_needed:
            return "Needs follow-up"
        return "Low"
