# Heritage National Bank — AI Banking Platform

This repository contains a capstone-style BFSI (Banking, Financial Services, and Insurance) platform that demonstrates how an AI-powered banking system can integrate customer data, transaction processing, fraud detection, sanctions screening, and compliance automation in a secure workflow.

The project is designed to model a modern digital banking environment where customer requests, risk checks, and financial actions are validated through an audit-friendly pipeline before approval.

## Project Overview

Heritage National Bank is a sample AI banking platform that combines:

- Transaction processing and validation
- Fraud risk analysis
- KYC, AML, and sanctions compliance checks
- Model routing for lightweight and high-risk decisions
- MCP-based banking and customer tools
- Audit logging for operational transparency
- AI chatbot support for customer and operations workflows

## Key Capabilities

- Secure transaction handling for account-to-account transfers
- Risk scoring for suspicious activity and fraud patterns
- Compliance pipeline covering KYC, AML, sanctions, and final approval
- Model routing between lightweight and reasoning models based on task complexity
- Audit trail generation for important platform operations
- End-to-end validation through automated tests

## Repository Structure

- `bfsi/` — Core banking platform logic, risk engine, compliance, MCP integrations, and transaction handling
- `audit_log/` — Logs for compliance, model routing, and transaction activity
- `docs/` — Project documentation and design references
- `tests/` — Automated validation for the platform
- `skills/` — Reusable agent skills and instructions
- `reports/` — Generated reports and evaluation outputs
- `images/` — Diagrams and supporting visuals

## Main Workflow

1. Customer and transaction data are validated.
2. The compliance pipeline runs in sequence: KYC → AML → SANCTIONS → APPROVAL.
3. Fraud and transaction risk are evaluated.
4. Model routing decides which model is best suited for each stage.
5. Every critical action is logged for audit and review.

## Example Execution

Run the main banking workflow:

```bash
python -m bfsi.main
```

Or execute the project entry point directly:

```bash
python bfsi/main.py
```

## Testing

Run the automated validation suite:

```bash
pytest
```

The project includes checks for:

- MCP tool audit logging
- Transaction approval and rejection logic
- Sanctions detection
- Input sanitization
- End-to-end compliance evaluation

## Security and Compliance Notes

This project follows banking-security principles, including:

- Masking sensitive financial data in logs and outputs
- Avoiding raw card or PAN exposure in records
- Keeping secrets in environment variables
- Auditing money movement and compliance decisions
- Enforcing structured approval paths for high-risk events

## Tech Stack

- Python
- AI model orchestration
- MCP tool integration
- JSONL audit logging
- Pytest-based validation

## Purpose

This repository serves as a demonstration of an AI-enabled fintech or BFSI platform, showing how modern AI systems can be integrated with compliance controls, transaction safety, and operational transparency in a banking context.

## License

This project is shared for educational and demonstration purposes.
