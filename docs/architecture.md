# System Architecture

This project demonstrates a local multi-agent workflow for customer inquiry intake and revenue prioritization. The goal is to show how a service business could turn raw inbound messages into an ordered queue of next actions.

## Architecture Diagram

```text
                 +--------------------------------------+
                 | data/inbound_customer_inquiries.csv  |
                 | 500 fake inbound customer messages   |
                 +------------------+-------------------+
                                    |
                                    v
                         +--------------------+
                         | Intake Agent       |
                         | extracts facts     |
                         +---------+----------+
                                   |
                                   v
                         +--------------------+
                         | Qualification Agent|
                         | checks fit/action  |
                         +---------+----------+
                                   |
                                   v
                         +--------------------+
                         | Scoring Agent      |
                         | ranks priority     |
                         +---------+----------+
                                   |
                                   v
                         +--------------------+
                         | Routing Agent      |
                         | chooses next step  |
                         +---------+----------+
                                   |
        +--------------------------+--------------------------+
        |                          |                          |
        v                          v                          v
+-----------------------+ +-----------------------+ +----------------------+
| Prioritized Lead Queue| | Lead Summary Metrics  | | Executive Summary    |
| CSV for operations    | | CSV for reporting     | | Markdown report      |
+-----------------------+ +-----------------------+ +----------------------+
```

## Agent Responsibilities

### Intake Agent

The Intake Agent converts unstructured text into structured business fields:

- Service Type
- Issue Summary
- Urgency
- Customer Intent
- Timing Need
- Missing Information

### Qualification Agent

The Qualification Agent evaluates whether a lead is in scope, complete enough for action, and worth follow-up. It assigns lead quality labels such as High, Medium, Needs follow-up, Out of scope, or Spam.

### Scoring Agent

The Scoring Agent applies deterministic business rules to create a 0-100 priority score. The score considers urgency, service value, customer intent, timing sensitivity, and information completeness.

### Routing Agent

The Routing Agent translates the score and qualification result into an operational recommendation:

- Notify contractor immediately
- Send booking link
- Ask follow-up question
- Schedule normal callback
- Nurture
- Ignore/spam

## Why This Architecture

The four-agent design keeps the business logic easy to explain. Each agent owns one decision stage, which makes the workflow easier to audit and improve. In a production setting, each agent could be upgraded independently without changing the full pipeline.

This is intentionally not a web app. The project focuses on the operational decision system: intake, qualification, prioritization, and routing.
