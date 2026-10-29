# Deployment Guide

- Python 3.10+ and pip are required.
- Install: anthropic python-dotenv mcp bandit pytest
- Store secrets in .env and use environment variables in code.
- Start MCP servers via .claude/mcp.json.
- Run pytest when committing changes.
- Run bandit on the bfsi package before merging.
- Maintain audit logs in audit_log/ for governance review.
