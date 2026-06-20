# Multi-Agent Customer Intake & Revenue Prioritization Platform

An AI Operations case study demonstrating how a multi-agent workflow can qualify, score, prioritize, and route inbound customer inquiries for service businesses.

![Multi-Agent Office Visualization](docs/office-visualization.png)

*Interactive multi-agent office concept showing specialized agents collaborating within a shared workflow environment.*

---

## Executive Summary

Service businesses receive customer inquiries with varying urgency, revenue potential, and completeness. Treating every inquiry the same creates operational inefficiency and can result in missed opportunities.

This project demonstrates a multi-agent workflow that transforms unstructured customer inquiries into prioritized operational actions. The system extracts relevant information, evaluates lead quality, scores opportunity value, and recommends the appropriate next step.

---

## System Architecture

![System Architecture](docs/architecture-diagram.png)

The workflow consists of four specialized agents:

### Intake Agent

Extracts relevant information from inbound inquiries including service type, urgency, timing requirements, and customer intent.

### Qualification Agent

Evaluates lead completeness, relevance, and revenue potential.

### Priority Scoring Agent

Assigns a weighted priority score based on business rules.

### Routing Agent

Determines the next operational action and routes the inquiry appropriately.

---

## Business Problem

Service businesses often struggle with:

* Large volumes of inbound inquiries
* Inconsistent lead quality
* Urgent requests hidden among routine requests
* Manual prioritization processes
* Time spent responding to low-value inquiries

Without a structured intake process, high-priority opportunities can be delayed while low-priority requests consume attention.

---

## Solution Overview

The system processes inbound customer inquiries through a sequence of specialized agents:

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

The output is a structured queue of prioritized leads with recommended next actions.

---

## Example Output

The workflow generates a prioritized lead queue that business operators can use to focus on the highest-impact opportunities first.

![Prioritized Lead Queue](docs/lead-queue-screenshot.png)

Each processed inquiry receives:

* Service Type
* Lead Quality
* Priority Score
* Priority Level
* Routing Decision

---

## Results

The final workflow processed 500 simulated inbound customer inquiries.

![Summary Metrics](docs/summary-metrics.png)

### Processing Summary

| Metric                    | Value |
| ------------------------- | ----- |
| Total Inquiries Processed | 500   |
| Critical Priority Leads   | 110   |
| High Priority Leads       | 110   |
| Medium Priority Leads     | 170   |
| Low Priority Leads        | 110   |
| Spam / Out-of-Scope Leads | 50    |
| Average Priority Score    | 51.72 |

### Key Findings

* 220 inquiries required elevated attention
* 50 inquiries were automatically identified as spam or out-of-scope
* The workflow successfully separated urgent opportunities from routine requests
* The system produced consistent routing recommendations across all inquiries

---

## Repository Contents

```text
README.md
requirements.txt

data/
├── inbound_customer_inquiries.csv

src/
├── run_pipeline.py
├── intake_and_qualification_agents.py
├── priority_scoring.py
├── routing_decisions.py

outputs/
├── prioritized_lead_queue.csv
├── lead_summary_metrics.csv
├── executive_summary.md

docs/
├── office-visualization.png
├── architecture-diagram.png
├── lead-queue-screenshot.png
├── summary-metrics.png
├── architecture.md
├── implementation-notes.md
```

---

## Technologies Used

* Python
* CSV Data Processing
* Rule-Based Decision Systems
* Multi-Agent Workflow Design
* Business Logic Modeling

---

## Limitations

Current version limitations include:

* Rule-based decision logic
* Simulated customer inquiries
* No CRM integration
* No SMS integration
* No LLM-powered extraction
* No human approval workflow

---

## Future Improvements

Potential production enhancements include:

* LLM-powered information extraction
* CRM integration
* SMS and email automation
* Calendar scheduling integration
* Human approval workflows
* Confidence scoring
* Audit logging
* Dashboard visualization
* Real-time lead processing

---

## Portfolio Context

This project was developed as an AI Operations and AI Implementation case study focused on workflow architecture, business decision systems, and operational automation.

The objective is to demonstrate how specialized AI agents can work together to support practical business processes, improve prioritization, and create structured operational workflows.
