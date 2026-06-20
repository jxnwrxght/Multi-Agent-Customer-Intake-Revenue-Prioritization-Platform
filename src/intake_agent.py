"""Intake Agent: extracts structured details from inbound customer messages."""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable


@dataclass(frozen=True)
class IntakeResult:
    service_type: str
    issue_summary: str
    urgency: str
    customer_intent: str
    timing_need: str
    missing_info: str


class IntakeAgent:
    """Extracts service type, urgency, intent, timing, and missing info."""

    SERVICE_KEYWORDS = {
        "HVAC": [
            "ac",
            "air conditioning",
            "furnace",
            "heat",
            "hvac",
            "thermostat",
            "warm air",
            "gas smell",
            "air ducts",
        ],
        "Plumbing": [
            "plumbing",
            "plumber",
            "toilet",
            "water heater",
            "tankless",
            "leak",
            "drain",
            "sink",
            "disposal",
            "water",
        ],
        "Electrical": [
            "breaker",
            "outlet",
            "sparking",
            "power",
            "ev charger",
            "panel",
            "ceiling fan",
            "lights",
            "dryer",
        ],
        "Cleaning": [
            "cleaning",
            "cleaner",
            "deep clean",
            "move-out clean",
            "office cleaning",
            "carpet",
            "janitorial",
            "maid",
            "house cleaning",
            "post-construction clean",
        ],
    }

    SPAM_KEYWORDS = [
        "crypto",
        "guaranteed returns",
        "click this link",
        "remove me",
        "seo services",
        "business loan",
        "sponsored post",
        "buy followers",
    ]
    EMERGENCY_KEYWORDS = [
        "emergency",
        "immediately",
        "as soon as possible",
        "asap",
        "now",
        "urgent",
        "today",
        "overflowing",
        "sparking",
        "gas smell",
        "no heat",
        "no power",
        "leaking from the ceiling",
        "backing up",
        "infant",
        "elderly",
    ]
    HIGH_VALUE_KEYWORDS = ["install", "installation", "replace", "upgrade", "renovation", "tankless"]
    MAINTENANCE_KEYWORDS = ["maintenance", "inspection", "tune-up", "monthly maintenance", "service plan"]
    EXISTING_CUSTOMER_KEYWORDS = [
        "existing customer",
        "last visit",
        "follow up",
        "follow-up",
        "warranty",
        "invoice",
        "came out",
        "installed last month",
    ]
    LOW_URGENCY_KEYWORDS = ["no rush", "flexible", "later", "planning", "comparing prices"]

    def process(self, lead: dict[str, str]) -> IntakeResult:
        message = lead["message"].strip()
        normalized = message.lower()

        service_type = self._detect_service_type(normalized)
        urgency = self._detect_urgency(normalized)
        customer_intent = self._detect_intent(normalized)
        timing_need = self._detect_timing(normalized)
        missing_info = self._detect_missing_info(message, service_type, timing_need)
        issue_summary = self._summarize_issue(message)

        return IntakeResult(
            service_type=service_type,
            issue_summary=issue_summary,
            urgency=urgency,
            customer_intent=customer_intent,
            timing_need=timing_need,
            missing_info=missing_info,
        )

    def _detect_service_type(self, normalized: str) -> str:
        if self._contains_any(normalized, self.SPAM_KEYWORDS):
            return "Out of Scope"

        for service_type, keywords in self.SERVICE_KEYWORDS.items():
            if self._contains_any(normalized, keywords):
                return service_type

        return "Unknown"

    def _detect_urgency(self, normalized: str) -> str:
        if self._contains_any(normalized, self.SPAM_KEYWORDS):
            return "Low"
        if self._contains_any(normalized, ["not an emergency", "no emergency"]):
            return "Low"
        if self._contains_any(normalized, ["gas smell", "sparking", "overflowing", "leaking from the ceiling"]):
            return "Emergency"
        if self._contains_any(normalized, self.EMERGENCY_KEYWORDS):
            return "High"
        if self._contains_any(normalized, self.LOW_URGENCY_KEYWORDS):
            return "Low"
        if self._contains_any(normalized, ["this week", "next week", "tomorrow", "this month"]):
            return "Medium"
        return "Medium"

    def _detect_intent(self, normalized: str) -> str:
        if self._contains_any(normalized, self.SPAM_KEYWORDS):
            return "Spam or opt-out"
        if self._contains_any(normalized, self.EXISTING_CUSTOMER_KEYWORDS):
            return "Existing customer follow-up"
        if self._contains_any(normalized, ["quote", "estimate", "pricing", "how much"]):
            return "Request quote"
        if self._contains_any(normalized, self.HIGH_VALUE_KEYWORDS):
            return "Book installation"
        if self._contains_any(normalized, self.MAINTENANCE_KEYWORDS):
            return "Request maintenance"
        if self._contains_any(normalized, ["come", "send", "call", "inspect", "help", "need someone"]):
            return "Request service"
        return "Unclear"

    def _detect_timing(self, normalized: str) -> str:
        if self._contains_any(normalized, ["immediate", "immediately", "asap", "as soon as possible", "now"]):
            return "Immediate"
        if "today" in normalized:
            return "Same day"
        if "tomorrow" in normalized:
            return "Tomorrow"
        if "this week" in normalized:
            return "This week"
        if "next week" in normalized:
            return "Next week"
        if "this month" in normalized:
            return "This month"
        if self._contains_any(normalized, ["two weeks", "2 weeks"]):
            return "Within two weeks"
        if self._contains_any(normalized, self.LOW_URGENCY_KEYWORDS):
            return "Flexible"
        return "Not specified"

    def _detect_missing_info(self, message: str, service_type: str, timing_need: str) -> str:
        missing = []
        word_count = len(message.split())

        if service_type == "Unknown":
            missing.append("service type")
        if timing_need == "Not specified":
            missing.append("preferred timing")
        if word_count < 6:
            missing.append("issue details")

        return "; ".join(missing) if missing else "None"

    def _summarize_issue(self, message: str) -> str:
        clean_message = " ".join(message.split())
        return clean_message if len(clean_message) <= 95 else clean_message[:92].rstrip() + "..."

    @staticmethod
    def _contains_any(text: str, keywords: Iterable[str]) -> bool:
        for keyword in keywords:
            if " " in keyword:
                if keyword in text:
                    return True
                continue

            if re.search(rf"\b{re.escape(keyword)}\b", text):
                return True

        return False
