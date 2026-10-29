# AI Banking Platform — Architecture

The project is layered to keep governance and performance separate:

1. Repository instrumentation via CLAUDE.md sets the authoritative contract.
2. MCP servers expose customer info and banking APIs with an audited registry.
3. The skills library provides reusable cached reasoning blocks.
4. The chatbot uses sanitized prompts and fraud-tool access.
5. Frauds, KYC, and sanctions feed the compliance pipeline.
6. Transactions and batch scoring are logged to the audit trail.
7. Hooks and CI enforce security and evaluation gates.
