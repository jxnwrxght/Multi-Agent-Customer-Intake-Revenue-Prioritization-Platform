# Multi-Agent Customer Intake & Revenue Prioritization Platform

![Office Visualization](docs/office-visualization.png)

A practical AI Operations case study exploring how specialized agents can work together to review, qualify, prioritize, and route inbound customer inquiries.

---

## Why I Built This

As I learned more about AI Operations and workflow automation, I became interested in how multiple AI agents could collaborate on a real business process rather than operate as isolated tools.

Customer intake felt like a useful example.

Service businesses receive inquiries with very different levels of urgency, value, and completeness. An HVAC emergency should not be handled the same way as a routine estimate request or an incomplete customer message.

I wanted to build a simple system that simulates how specialized agents could work together to review inbound inquiries, evaluate lead quality, assign priority scores, and recommend the next operational action.

The goal was not to build a production product. The goal was to design and demonstrate a clear multi-agent workflow that solves a practical business problem.

---

## Business Context

Imagine a contractor receiving dozens of inquiries every week.

Some customers need emergency service immediately.

Some are requesting estimates for future projects.

Others provide incomplete information or are not legitimate opportunities at all.

When every inquiry enters the same queue, valuable opportunities can be delayed while low-priority requests consume time and attention.

This project explores how a multi-agent workflow can help solve that problem by automatically reviewing, prioritizing, and routing inquiries before a human operator becomes involved.

---

## System Overview

The workflow is organized around four specialized agents.

### Intake Agent

Responsibilities:

- Extract service type
- Identify urgency
- Capture timing requirements
- Determine customer intent

Output:

Structured inquiry details.

---

### Qualification Agent

Responsibilities:

- Review completeness
- Verify relevance
- Evaluate lead quality
- Identify missing information

Output:

Qualified lead assessment.

---

### Priority Scoring Agent

Responsibilities:

- Score urgency
- Score revenue potential
- Score timing sensitivity
- Score information completeness

Output:

Priority score from 0–100 and assigned priority level.

---

### Routing Agent

Responsibilities:

- Recommend next action
- Escalate critical inquiries
- Route booking opportunities
- Request missing information
- Ignore spam or out-of-scope inquiries

Output:

Operational recommendation for the business.

---

## Workflow Architecture

![Architecture Diagram](docs/architecture-diagram.png)

```text
Customer Inquiry
        ↓
Intake Agent
        ↓
Qualification Agent
        ↓
Priority Scoring Agent
        ↓
Routing Agent
        ↓
Prioritized Lead Queue
```

---

## Example Output

The workflow generates a prioritized lead queue that business operators can use to focus on the highest-impact opportunities first.

![Prioritized Lead Queue](docs/prioritized-lead-queue.png)

Each processed inquiry receives:

- Service Type
- Lead Quality
- Priority Score
- Priority Level
- Routing Decision

---

## Results

The final workflow processed 500 simulated inbound customer inquiries.

![Lead Summary Metrics](docs/lead-summary-metrics.png)

### Processing Summary

| Metric | Value |
|----------|----------|
| Total Inquiries Processed | 500 |
| Critical Leads | 110 |
| High Priority Leads | 110 |
| Medium Priority Leads | 170 |
| Low Priority Leads | 110 |
| Spam / Out-of-Scope Leads | 50 |
| Average Priority Score | 51.7 |

---

## What This Project Demonstrates

This project is less about Python itself and more about workflow design.

The focus was on:

- Breaking a business process into specialized agent responsibilities
- Designing decision logic between agents
- Creating explainable prioritization rules
- Producing outputs that operations teams can actually use
- Simulating how multiple agents can collaborate within a larger workflow

While the current version uses rule-based logic and simulated data, the same architecture could be extended with:

- LLM-powered extraction
- CRM integrations
- SMS and email systems
- Scheduling platforms
- Human approval workflows
- Operational dashboards

---

## Repository Contents

```text
Multi-Agent-Customer-Intake-Revenue-Prioritization-Platform/

README.md
requirements.txt

data/
│
├── inbound_customer_inquiries.csv

docs/
│
├── office-visualization.png
├── architecture-diagram.png
├── prioritized-lead-queue.png
├── lead-summary-metrics.png
├── implementation-notes.md

outputs/
│
├── prioritized_lead_queue.csv
├── lead_summary_metrics.csv

src/
│
├── run_pipeline.py
├── intake_and_qualification_agents.py
├── priority_scoring.py
├── routing_decisions.py
```

---

## Limitations

Current version:

- Rule-based decision engine
- Simulated customer inquiries
- No live CRM integration
- No SMS integration
- No LLM-powered extraction
- No human review layer

This project is intended as a workflow design and AI Operations case study rather than a production deployment.

---

## Future Enhancements

Potential next steps include:

- LLM-powered lead extraction
- CRM integration
- Real-time messaging workflows
- Calendar and booking integrations
- Human approval checkpoints
- Agent performance monitoring
- Explainability and audit logging

---

## Author

Jon Wright

AI Operations • Workflow Automation • Process Design

This project was created as part of my AI Operations portfolio to explore how specialized agents can collaborate to solve practical business problems.
