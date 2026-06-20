# Multi-Agent Customer Intake & Revenue Prioritization Platform

A local AI Operations case study showing how a multi-agent workflow can classify, prioritize, and route inbound service-business inquiries.

## Executive Summary

Service businesses often receive more inbound inquiries than a small team can review immediately. Some messages are emergencies, some are valuable quote requests, some need clarification, and others are spam or outside the business scope.

This project demonstrates a practical multi-agent intake system that processes 500 fake customer inquiries and produces a prioritized lead queue, summary metrics, and an executive stakeholder report. It is designed as a portfolio-ready AI Implementation example, not a deployed production system.

## Business Problem

Many basic automations treat all inbound leads the same. In a real service operation, that creates avoidable problems:

- Emergency jobs can be buried behind low-urgency quote requests.
- Office staff spend time reading incomplete or irrelevant messages.
- High-value installation opportunities may not be separated from routine maintenance.
- Spam and out-of-scope inquiries can pollute the active lead queue.

The business need is a repeatable triage process that helps operators know which inquiries require immediate action and which can be routed to follow-up, nurture, or filtering.

## Solution Overview

The system reads inbound customer inquiries from a CSV file and sends each message through four specialized agents:

- Intake Agent: extracts the operational facts from the raw message.
- Qualification Agent: determines whether the lead is in scope and complete enough for action.
- Scoring Agent: assigns a 0-100 priority score and priority level.
- Routing Agent: recommends the next best action for the business.

The workflow produces three business-facing outputs:

- `outputs/prioritized_lead_queue.csv`
- `outputs/lead_summary_metrics.csv`
- `outputs/executive_summary.md`

## Agent Architecture

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
outputs/executive_summary.md
```

## Decision Flow

1. A raw customer inquiry enters from `data/inbound_customer_inquiries.csv`.
2. The Intake Agent extracts service type, issue summary, urgency, intent, timing needs, and missing information.
3. The Qualification Agent checks scope, completeness, lead quality, and follow-up need.
4. The Scoring Agent scores urgency, service value, intent, timing sensitivity, and completeness.
5. The Routing Agent chooses immediate notification, booking link, follow-up question, normal callback, nurture, or ignore/spam.
6. The pipeline writes a prioritized lead queue and executive metrics.

## Example Outputs

Example input:

```csv
lead_id,timestamp,source,customer_name,message
L0002,2026-04-15 07:47,Website Form,Jordan Hayes,Water is leaking from the ceiling under the upstairs bathroom. Need emergency plumbing help as soon as possible.
```

Example output:

```csv
Lead ID,Service Type,Urgency,Customer Intent,Lead Quality,Priority Score,Priority Level,Routing Decision
L0002,Plumbing,Emergency,Request service,High,100,Critical,Notify contractor immediately
```

## Results

The included 500-inquiry sample run produced:

| Metric | Result |
| --- | ---: |
| Total Inquiries Processed | 500 |
| Critical Priority Leads | 110 |
| High Priority Leads | 110 |
| Medium Priority Leads | 170 |
| Low Priority Leads | 110 |
| Spam / Out-of-Scope Leads | 50 |
| Average Priority Score | 51.72 |

Business interpretation: the workflow separates urgent and high-value work from lower-priority or non-actionable messages, giving a service operator a clearer daily lead queue.

## How to Run Locally

```bash
python3 src/run_pipeline.py
```

The project uses only the Python standard library. No API keys, paid services, or external integrations are required.

## Repository Structure

```text
.
├── README.md
├── requirements.txt
├── data/
│   └── inbound_customer_inquiries.csv
├── src/
│   ├── run_pipeline.py
│   ├── intake_agent.py
│   ├── qualification_agent.py
│   ├── scoring_agent.py
│   └── routing_agent.py
├── outputs/
│   ├── prioritized_lead_queue.csv
│   ├── lead_summary_metrics.csv
│   └── executive_summary.md
└── docs/
    ├── architecture.md
    └── implementation-notes.md
```

## Future Improvements

- Replace keyword extraction with LLM-assisted extraction and confidence scores.
- Add CRM integration for customer history and lead ownership.
- Add SMS, email, and website form ingestion.
- Connect booking links and calendar availability.
- Add a human approval layer for critical or uncertain cases.
- Build a dashboard for daily lead queues, routing breakdowns, and response-time tracking.
- Add automated tests for scoring and routing rules.

## Portfolio Framing

This repository is an AI Operations / AI Implementation case study. It focuses on modular agent design, decision logic, measurable outputs, and business readability. It is intentionally local and deterministic so the system can be reviewed, run, and explained without relying on external services.
