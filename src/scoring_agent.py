"""Scoring Agent: converts lead signals into a 0-100 priority score."""

from __future__ import annotations

from intake_agent import IntakeResult
from qualification_agent import QualificationResult


class ScoringAgent:
    """Scores urgency, service value, intent, timing sensitivity, and completeness."""

    URGENCY_POINTS = {"Emergency": 35, "High": 28, "Medium": 16, "Low": 5}
    SERVICE_VALUE_POINTS = {"HVAC": 17, "Plumbing": 17, "Electrical": 16, "Cleaning": 12, "Unknown": 2, "Out of Scope": 0}
    INTENT_POINTS = {"Book installation": 20, "Request service": 18, "Request quote": 15, "Request maintenance": 10, "Existing customer follow-up": 12, "Unclear": 3, "Spam or opt-out": 0}
    TIMING_POINTS = {"Immediate": 15, "Same day": 13, "Tomorrow": 10, "This week": 7, "Within two weeks": 6, "Next week": 5, "This month": 4, "Flexible": 2, "Not specified": 0}

    def process(self, intake: IntakeResult, qualification: QualificationResult) -> tuple[int, str]:
        if qualification.lead_quality == "Spam":
            return 0, "Low"
        score = self.URGENCY_POINTS.get(intake.urgency, 0) + self.SERVICE_VALUE_POINTS.get(intake.service_type, 0) + self.INTENT_POINTS.get(intake.customer_intent, 0) + self.TIMING_POINTS.get(intake.timing_need, 0) + self._completeness_points(intake)
        if not qualification.in_scope:
            score = min(score, 10)
        elif not qualification.actionable:
            score = max(score - 12, 0)
        score = max(0, min(score, 100))
        return score, self._priority_level(score)

    def _completeness_points(self, intake: IntakeResult) -> int:
        if intake.missing_info == "None":
            return 15
        return max(0, 15 - (len(intake.missing_info.split(";")) * 6))

    def _priority_level(self, score: int) -> str:
        if score >= 80:
            return "Critical"
        if score >= 60:
            return "High"
        if score >= 35:
            return "Medium"
        return "Low"
