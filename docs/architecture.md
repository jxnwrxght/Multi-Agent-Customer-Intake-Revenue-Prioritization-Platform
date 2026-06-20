# Architecture

This project is a local command-line prototype. It reads fake inbound customer messages from a CSV file, runs each message through four specialized agents, and writes lead-level and run-level outputs.

## ASCII Diagram

```text
                 +-----------------------+
                 | data/inbound_customer_inquiries.csv |
                 +-----------+-----------+
                             |
                             v
                    +----------------+
                    | Intake Agent   |
                    | extracts facts |
                    +-------+--------+
                            |
                            v
              +---------------------------+
              | Qualification Agent       |
              | checks scope and quality  |
              +-------------+-------------+
                            |
                            v
              +---------------------------+
              | Scoring Agent             |
              | scores lead from 0 to 100 |
              +-------------+-------------+
                            |
                            v
                    +----------------+
                    | Routing Agent  |
                    | chooses action |
                    +-------+--------+
                            |
              +-------------+-------------+
              |                           |
              v                           v
+-------------------------------+ +-----------------------------+
| outputs/prioritized_lead_queue.csv | | outputs/lead_summary_metrics.csv |
+-------------------------------+ +-----------------------------+
```

## Flow

1. `src/run_pipeline.py` loads rows from `data/inbound_customer_inquiries.csv`.
2. The Intake Agent extracts service type, issue summary, urgency, intent, timing, and missing information.
3. The Qualification Agent decides whether the lead is in scope, whether it is likely revenue-generating, whether it is complete, and whether follow-up is needed.
4. The Scoring Agent assigns a score from 0 to 100 and a priority level.
5. The Routing Agent chooses the next action for operations.
6. The pipeline writes a prioritized lead CSV and a summary metrics CSV.

## Design Choice

The agents are intentionally rule-based in Version 1. This keeps the project local, deterministic, and easy to explain in an interview. In a production version, the extraction step could use an LLM, while qualification, scoring, and routing could remain partly rule-based so the business logic stays auditable.
