# Heritage National Bank — AI Banking Platform

Authoritative development context for Claude Code.

## Project
Unified AI-powered banking platform integrating Claude Skills, MCP servers,
chatbot, fraud detection, compliance automation, transaction processing,
model routing, and security hardening.

## MCP Registry
| Server | Purpose | Key tools |
|---|---|---|
| customer-info | customer master data and history | get_customer, check_customer_history, verify_ip_location |
| banking-api | balances, transfers, loans | get_balance, transfer_funds, apply_loan |
| github | repository operations | create_branch, create_commit, create_pull_request |

## SKILL.md Schema
Each skill declares YAML front matter:
---
name: <kebab-case>
description: <one line>
model: haiku | sonnet | opus
cache: true
---
<system prompt>

## Model Routing
- Haiku -> batch classification and lightweight scoring
- Sonnet -> chatbot and compliance reasoning
- Opus -> final approval, high-risk decisions, judge evaluation

## PCI DSS Constraints
- Never log full PAN or card data; mask to last 4 digits.
- Sanitize all chatbot and user input before it reaches a tool or model.
- Enforce rate limiting on money movement operations.
- Audit all money movement and compliance decisions.
- Secrets come from environment variables only.

## Audit Log Locations
- audit_log/mcp_tool_calls.jsonl
- audit_log/model_routing.jsonl
- audit_log/transactions.jsonl
- audit_log/bandit_scan.txt

## Compliance Pipeline Order
KYC -> AML -> Sanctions -> Approval.

## Definition of Done
- pytest passes with zero failures
- bandit has no medium+ findings
- every MCP hop is audited
- judge score is >= 4
