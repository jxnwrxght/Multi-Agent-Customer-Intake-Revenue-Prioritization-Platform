# Multi-Agent Customer Intake & Prioritization Platform

A local Python prototype that uses specialized agents to extract, qualify, score, and route inbound service-business leads.

## Business Problem

Service businesses often receive customer inquiries from SMS, web forms, email, chat, voicemail, and referral channels. Some messages are urgent emergencies, some are normal quote requests, some are follow-ups from existing customers, and some are too vague or irrelevant to act on.

Basic automations often treat every inbound lead the same. In practice, a same-day HVAC emergency, a cleaning quote, an existing customer warranty question, and a spam message should not receive the same response path.

This project demonstrates a practical local prototype for turning inbound messages into prioritized operational decisions.

## System Architecture

```text
data/inbound_customer_inquiries.csv
        |
        v
+----------------+
| Intake Agent   |
+----------------+
        |
        v
+----------------------+
| Qualification Agent  |
+----------------------+
        |
        v
+----------------+
| Scoring Agent  |
+----------------+
        |
        v
+----------------+
| Routing Agent  |
+----------------+
        |
        v
outputs/prioritized_lead_queue.csv
outputs/lead_summary_metrics.csv
```

## Agent Responsibilities

### Intake Agent

Extracts structured fields from each raw customer message:

- Service type
- Issue summary
- Urgency
- Customer intent
- Timing need
- Missing information

### Qualification Agent

Determines whether the lead is in scope, likely revenue-generating, complete enough to act on, and whether follow-up is needed.

### Scoring Agent

Scores leads from 0 to 100 based on urgency, service value, customer intent, timing sensitivity, and completeness of information. It assigns each lead a priority level: Critical, High, Medium, or Low.

### Routing Agent

Chooses the next action:

- Notify contractor immediately
- Send booking link
- Ask follow-up question
- Schedule normal callback
- Nurture
- Ignore/spam

## Example Input

```csv
lead_id,timestamp,source,customer_name,message
L0002,2026-04-15 07:47,Website Form,Jordan Hayes,Water is leaking from the ceiling under the upstairs bathroom. Need emergency plumbing help as soon as possible.
```

## Example Output

```csv
lead_id,service_type,urgency,customer_intent,lead_quality,priority_score,priority_level,routing_decision
L0002,Plumbing,Emergency,Request service,High,100,Critical,Notify contractor immediately
```

## Summary Metrics From 500-Lead Run

| Metric | Value |
| --- | ---: |
| Total leads processed | 500 |
| Critical leads | 110 |
| High priority leads | 110 |
| Medium priority leads | 170 |
| Low priority leads | 110 |
| Spam/out-of-scope leads | 50 |
| Average priority score | 51.72 |

## How to Run Locally

From the project folder:

```bash
python3 src/run_pipeline.py
```

The script reads:

```text
data/inbound_customer_inquiries.csv
```

It writes:

```text
outputs/prioritized_lead_queue.csv
outputs/lead_summary_metrics.csv
```

No API keys, paid APIs, or external services are required. Version 1 uses only the Python standard library.

## Repository Contents

```text
multi-agent-customer-intake-prioritization-platform/
├── README.md
├── requirements.txt
├── data/
│   └── inbound_customer_inquiries.csv
├── outputs/
│   ├── prioritized_lead_queue.csv
│   └── lead_summary_metrics.csv
├── src/
│   ├── run_pipeline.py
│   ├── intake_agent.py
│   ├── qualification_agent.py
│   ├── scoring_agent.py
│   └── routing_agent.py
└── docs/
    ├── architecture.md
    └── implementation-notes.md
```

- `data/inbound_customer_inquiries.csv`: 500 fake inbound customer messages across HVAC, plumbing, electrical, cleaning, maintenance, installation, emergency, quote, vague, existing-customer, and spam scenarios.
- `src/run_pipeline.py`: Main script that runs the full workflow from input CSV to output CSVs.
- `src/intake_agent.py`: Extracts service type, issue summary, urgency, customer intent, timing needs, and missing information.
- `src/qualification_agent.py`: Determines whether each lead is in scope, complete enough for action, and worth follow-up.
- `src/scoring_agent.py`: Scores each lead from 0 to 100 based on urgency, service value, intent, timing sensitivity, and completeness.
- `src/routing_agent.py`: Decides the next best action: immediate notification, booking link, follow-up question, normal callback, nurture, or ignore/spam.
- `outputs/prioritized_lead_queue.csv`: Lead-level output sorted by priority score.
- `outputs/lead_summary_metrics.csv`: Run-level summary metrics.
- `docs/architecture.md`: Simple architecture explanation and ASCII diagram.
- `docs/implementation-notes.md`: Notes on design choices, scoring, routing, and production next steps.

## Portfolio Framing

This is a working local prototype designed to demonstrate multi-agent system architecture for customer intake and prioritization. It is not presented as a deployed product. The goal is to show modular decision logic, measurable output, and practical business reasoning in a repo that can be run and reviewed locally.

## Limitations

- Rule-based prototype
- Fake sample data only
- No live SMS, email, chat, or web form integration yet
- No CRM integration yet
- No calendar or booking integration yet
- No LLM API calls in Version 1
- No human approval workflow yet

## Future Improvements

- LLM-powered extraction for messier real-world messages
- Confidence scores for extracted fields and routing decisions
- CRM integration for customer history and lead ownership
- SMS, email, and website form ingestion
- Calendar and booking-link integration
- Human approval layer for critical or uncertain routing decisions
- Dashboard visualization for daily lead queues and service mix
- Automated tests for scoring and routing regressions
