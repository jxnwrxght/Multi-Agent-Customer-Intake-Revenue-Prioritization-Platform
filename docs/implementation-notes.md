# System Notes

## Why Multiple Agents

This prototype separates the workflow into four agents because customer intake decisions are easier to understand when each step has a clear responsibility. A single script could perform every rule in one place, but that would make the business logic harder to explain, test, and adjust.

The multi-agent structure also mirrors how a production system might evolve. Extraction, qualification, scoring, and routing can each be improved independently without rewriting the full pipeline.

## Agent Responsibilities

### Intake Agent

The Intake Agent turns an unstructured customer message into structured fields:

- Service type
- Issue summary
- Urgency
- Customer intent
- Timing need
- Missing information

Version 1 uses keyword rules so the behavior is deterministic and easy to inspect.

### Qualification Agent

The Qualification Agent decides whether the lead is in scope, likely revenue-generating, and actionable. It assigns a lead quality label such as High, Medium, Needs follow-up, Out of scope, or Spam.

This keeps business fit separate from priority scoring. For example, an urgent but out-of-scope message should not be treated the same as an urgent HVAC emergency.

### Scoring Agent

The Scoring Agent assigns a score from 0 to 100 using five factors:

- Urgency
- Service value
- Customer intent
- Timing sensitivity
- Completeness of information

Emergency terms, same-day timing, clear service requests, and complete details raise the score. Missing information and out-of-scope requests reduce the score.

Priority levels are assigned from the final score:

- Critical: 80-100
- High: 60-79
- Medium: 35-59
- Low: 0-34

### Routing Agent

The Routing Agent chooses the next action based on lead quality, completeness, and priority:

- Notify contractor immediately for critical, actionable emergencies
- Send booking link for strong quote or installation leads
- Ask follow-up question when key details are missing
- Schedule normal callback for useful but non-emergency leads and existing customer follow-ups
- Nurture low-urgency in-scope leads that are not ready for immediate scheduling
- Ignore/spam for spam, opt-out, or unsupported requests

## Production Considerations

A production version would likely replace or supplement these rules with LLM-powered extraction, confidence scores, and validation against CRM data. It would also need human approval controls, audit logs, live SMS or web form integrations, calendar availability, and monitoring for missed high-priority cases.

The current version is intentionally local and rule-based. Its purpose is to demonstrate the architecture and decision logic in a way that can be reviewed, run, and explained without paid services or API keys.
