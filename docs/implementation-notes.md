# Implementation Notes

## Design Decisions

This project uses deterministic Python rules instead of external AI services. That choice keeps the workflow transparent, local, and easy to run during portfolio review.

The code is separated into one file per agent:

- `src/intake_agent.py`
- `src/qualification_agent.py`
- `src/scoring_agent.py`
- `src/routing_agent.py`

The orchestration script, `src/run_pipeline.py`, is intentionally simple. It loads the input CSV, runs each agent in sequence, writes output files, and prints summary metrics.

## Scoring Logic

The Scoring Agent assigns points across five business factors:

- Urgency
- Service value
- Customer intent
- Timing sensitivity
- Completeness of information

Priority levels are assigned from the final score:

- Critical: 80-100
- High: 60-79
- Medium: 35-59
- Low: 0-34

## Routing Logic

Routing decisions are designed to mirror realistic service-business operations:

- Critical actionable leads notify the contractor immediately.
- Strong quote and installation leads receive a booking link.
- Incomplete leads trigger a follow-up question.
- Useful but non-emergency leads receive a normal callback.
- Low-urgency leads can be nurtured.
- Spam and out-of-scope messages are ignored or filtered.

## Assumptions

- The sample data is fake and created for demonstration.
- The service categories are HVAC, plumbing, electrical, and cleaning.
- Keyword rules are sufficient for Version 1 demonstration.
- The system is designed for local review, not live production use.
- Output files are regenerated each time `python3 src/run_pipeline.py` runs.

## Limitations

- No LLM extraction in Version 1.
- No confidence scoring for extracted fields.
- No CRM, SMS, email, or booking integration.
- No human approval workflow.
- No live customer data.
- Keyword matching can miss ambiguous or unusually phrased messages.

## Production Roadmap

- Add LLM-powered extraction with confidence scores.
- Add validation against CRM records and existing customer history.
- Connect live SMS, email, website forms, and chat inputs.
- Add calendar availability and booking-link generation.
- Add human review for critical, uncertain, or high-value leads.
- Add audit logs for each scoring and routing decision.
- Add dashboard views for operators and managers.
- Add automated tests for scoring, routing, and edge cases.
