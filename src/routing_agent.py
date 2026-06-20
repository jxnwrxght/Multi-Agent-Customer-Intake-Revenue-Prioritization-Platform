"""Routing Agent: chooses the next best action for each prioritized lead."""

from __future__ import annotations

from intake_agent import IntakeResult
from qualification_agent import QualificationResult


class RoutingAgent:
    """Routes leads to immediate notification, booking, follow-up, nurture, or ignore."""

    def process(
        self,
        intake: IntakeResult,
        qualification: QualificationResult,
        priority_score: int,
        priority_level: str,
    ) -> tuple[str, str]:
        if qualification.lead_quality == "Spam":
            return "Ignore/spam", "Message appears to be spam, promotional, or an opt-out request."

        if intake.missing_info != "None":
            return (
                "Ask follow-up question",
                f"Lead is missing {intake.missing_info}, so more detail is needed before dispatch or booking.",
            )

        if not qualification.in_scope:
            return "Ignore/spam", "The requested service is outside the supported HVAC, plumbing, electrical, and cleaning scope."

        if priority_level == "Critical":
            return (
                "Notify contractor immediately",
                "Emergency or same-day lead with enough information to take action.",
            )

        if intake.customer_intent == "Existing customer follow-up":
            return (
                "Schedule normal callback",
                "Existing customer follow-up should be handled by the office or service coordinator.",
            )

        if intake.customer_intent in {"Book installation", "Request quote"} and priority_score >= 50:
            return (
                "Send booking link",
                "Lead is in scope, revenue-generating, and suitable for estimate scheduling.",
            )

        if intake.urgency == "Low" and priority_score < 45:
            return (
                "Nurture",
                "Lead is in scope but low urgency, so it can be kept warm without immediate scheduling.",
            )

        if priority_level in {"High", "Medium"}:
            return (
                "Schedule normal callback",
                "Lead is actionable but does not require immediate contractor notification.",
            )

        return (
            "Schedule normal callback",
            "Lead is low urgency but still in scope and potentially useful.",
        )
