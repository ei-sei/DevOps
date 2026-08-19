# Projects

A progression of practical projects combining AI and DevOps. Each builds on the previous, and each is gated on the notes it exercises - build the project after the note, not before. Only Project 1 is implemented so far; the rest are scoped here so the roadmap is concrete.

| # | Project | Depends on notes | Status |
|---|---------|------------------|--------|
| 1 | [Direct LLM API application](01-direct-llm-api/) | 01-02 | done |
| 2 | Tool-calling agent | 03-04 | planned |
| 3 | RAG application | 07 | planned |
| 4 | Agent without a framework | 05-06 | planned |
| 5 | LangChain agent | frameworks/langchain | planned |
| 6 | LangGraph workflow | frameworks/langgraph | planned |
| 7 | DevOps troubleshooting agent | 09, 12 | planned |
| 8 | Agentic CI/CD assistant | 10-11, 13-14 | planned |

## Project 1 - Direct LLM API application (done)

A minimal script exercising the raw API: messages, system prompts, temperature comparison, token usage inspection, and streaming - no SDK abstractions beyond the provider client. See [01-direct-llm-api/](01-direct-llm-api/).

## Project 2 - Tool-calling agent

Single-turn assistant with three or four read-only DevOps tools (pod status, service health check, log tail, disk usage). Validated arguments, errors returned as data, least-privilege by construction. No loop yet - one question, tools as needed, one answer.

## Project 3 - RAG application

"Ask my DevOps notes": chunk this repo's `notes/` folders on headings, embed, cosine top-k retrieval, delimited context injection with source citations, and an honest "not covered in the notes" path. CLI plus a re-index command that only re-embeds changed files.

## Project 4 - Agent without a framework

The polished topic 05 loop and the reference implementation for everything after it: config-driven tools, JSON-lines audit log of every step, checkpoint/resume, cost budget as a stopping condition, repeated-call detection. This is the baseline Projects 5 and 6 are compared against.

## Project 5 - LangChain agent

Port Project 2 to LangChain (`@tool`, `with_structured_output`, an agent executor). Deliverable includes a short written comparison against Project 4: behaviour, cost, debuggability - honest about what the framework bought and what it obscured.

## Project 6 - LangGraph workflow

The topic 12 sequential pipeline (research → fix → review) as an explicit graph: typed state, conditional routing on boundary checks, a checkpointer with kill-and-resume demonstrated, and a human interrupt before any write action.

## Project 7 - DevOps troubleshooting agent

The track's first genuinely useful tool: a supervisor agent that diagnoses a misbehaving service using worker subagents (log analysis, config inspection, deploy history) plus the Project 3 RAG pipeline as its knowledge-base tool. Produces an incident report with per-agent attribution and evidence. Built only after the single-agent baseline exists, per topic 12's discipline.

## Project 8 - Agentic CI/CD assistant (capstone)

The topic 11 workflow wired into this repository for real, demonstrating the full stack:

- **LLM + tools + agent workflow + state**: failure-triggered analysis agent with context-gathering tools and checkpointed runs
- **Docker**: the agent runs as a container in the pipeline
- **CI/CD**: GitHub Actions integration - triggered on failure, commenting on PRs with scoped permissions
- **Logging**: JSON-lines audit trail of every tool call and decision
- **Evaluation**: versioned eval set of real failures, harness gating prompt changes in CI
- **Security**: read-only credentials, injection-aware log handling, confidence-gated output, human approval for anything beyond commenting
