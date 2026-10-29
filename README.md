# Heritage National Bank AI Banking Platform

An integrated AI-powered banking platform built for the capstone project, combining MCP-backed banking tools, a compliance-guarded chatbot, fraud detection, sanctions screening, transaction processing, model routing, audit logging, and security automation.

## Overview

This project demonstrates a production-oriented BFSI architecture that combines:

- Claude Skills-based reasoning layer
- MCP integration for customer and banking operations
- Guardrailed customer support chatbot
- Fraud risk scoring and transaction monitoring
- KYC, AML, and sanctions compliance workflow
- Model routing across Haiku, Sonnet, and Opus
- End-to-end transaction logging and audit tracing
- Security scanning and governance checks

## Project Structure

```text
.
├── CLAUDE.md
├── README.md
├── .claude/
│   ├── mcp.json
│   ├── settings.json
│   └── commands/
├── .github/
│   └── workflows/
├── audit_log/
│   ├── mcp_tool_calls.jsonl
│   ├── model_routing.jsonl
│   ├── transactions.jsonl
│   └── bandit_scan.txt
├── bfsi/
│   ├── __init__.py
│   ├── batch_fraud.py
│   ├── chatbot.py
│   ├── fraud_engine.py
│   ├── judge.py
│   ├── kyc_vision.py
│   ├── main.py
│   ├── model_router.py
│   ├── skills_loader.py
│   ├── transactions.py
│   ├── compliance/
│   │   ├── __init__.py
│   │   ├── pipeline.py
│   │   └── sanctions_check.py
│   └── mcp/
│       ├── __init__.py
│       ├── banking_api_server.py
│       ├── customer_info_server.py
│       └── registry.py
├── docs/
│   ├── architecture.md
│   └── deployment.md
├── skills/
│   ├── compliance-narrative/
│   ├── customer-support/
│   ├── fraud-triage/
│   ├── kyc-extraction/
│   ├── risk-scoring/
│   └── sanctions-summary/
├── tests/
│   └── test_platform.py
└── .env
```

## Main Features

### 1. MCP Banking Integration
- Customer lookup and history retrieval
- Balance checks and transfer flows
- Banking API tools exposed via MCP for internal orchestration
- Audit logging for every tool call

### 2. Skills Layer
- Reusable skill pack for compliance, customer support, fraud, risk scoring, sanctions summaries, and KYC extraction
- Cached prompt system used for consistent reasoning and lower overhead

### 3. Compliance Pipeline
The platform enforces the required order:

KYC -> AML -> Sanctions -> Approval

Transactions are blocked if the pipeline fails at any stage.

### 4. Model Routing
- Haiku for lightweight classification and batch scoring
- Sonnet for chatbot and compliance reasoning
- Opus for high-risk decisions and gate evaluation

### 5. Security and Governance
- Environment-variable-only secret handling
- Input sanitization for prompts
- Audit trail for transactions and MCP calls
- Bandit security scan in the workflow
- PCI-DSS-style controls enforced in design and execution

## Setup

### Prerequisites

- Python 3.10+
- Virtual environment recommended
- OpenRouter-compatible API key
- GitHub token for repository automation

### Install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install anthropic python-dotenv mcp bandit pytest
```

### Environment variables
Create a `.env` file with:

```env
OPENROUTER_API_KEY="your_key_here"
ANTHROPIC_BASE_URL="https://openrouter.ai/api"
MODEL_HAIKU="anthropic/claude-3.5-haiku"
MODEL_SONNET="anthropic/claude-sonnet-4.5"
MODEL_OPUS="anthropic/claude-opus-4.1"
GITHUB_TOKEN="your_github_token"
```

## Running the Project

### Run the main workflow

```bash
python -m bfsi.main
```

### Run validation tests

```bash
python -m pytest tests/ -q
```

### Run the judge gate

```bash
python -m bfsi.judge
```

### Run security scan

```bash
bandit -q -r bfsi -ll
```

## Validation Status

The project has been validated with fresh checks:

- Pytest: 8 passed
- Bandit: no medium+ findings
- Judge gate: score 4/5, PASS

## Notes

This repository is structured as a production-ready capstone demonstration and is intended to show how AI, MCP, governance, compliance, and operational auditing can be combined inside a real financial-services platform.
