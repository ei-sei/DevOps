# Agentic Workflows

Notes and projects on building, optimising, and automating AI agents, learned from a DevOps engineer's perspective: concepts first, frameworks second, production concerns (cost, evaluation, security) treated as first-class from the start rather than bolted on later.

## Why this exists

DevOps work is already about building reliable systems out of unreliable parts: flaky networks, fallible humans, services that go down. Agentic AI is the same problem with a new unreliable part, the model. The instincts that make a good DevOps engineer (idempotency, retries, observability, least privilege, human approval gates) map almost directly onto what makes a good agent reliable. This track exists to make that mapping explicit and to build real, working things along the way rather than just reading about them.

```text
DevOps
  |
Automation
  |
Cloud Infrastructure
  |
AI-assisted workflows
  |
Agentic Workflows
  |
AI Infrastructure / Platform Engineering
```

## Learning philosophy

> Learn the underlying concepts before relying heavily on frameworks.

It is possible to build a working agent in LangGraph or LangChain without ever understanding what a tool call actually is on the wire, how an agent loop terminates, or why structured output matters. That produces someone who can wire components together but cannot debug them when they break, and cannot reason about cost, latency, or failure modes.

So the order here is deliberate: understand LLM APIs, prompting, structured output, tool use, and the agent loop by hand (plain Python, no framework) before ever touching LangChain or LangGraph. Frameworks are introduced afterwards, explicitly framed as "here is the abstraction, and here is the manual version it is replacing."

## Curriculum

The 14 topics build on each other in a single line, not a grab-bag. Each topic assumes the ones before it.

```text
01 LLM Fundamentals
       |
02 Prompt Engineering
       |
03 Structured Output
       |
04 Tool Use
       |
05 Agent Loops
       |
06 Memory & Persistence
       |
07 RAG
       |
08 MCP
       |
09 Subagents
       |
10 Hooks & Automation
       |
11 Agentic CI/CD
       |
12 Multi-Agent Workflows
       |
13 Cost & Performance
       |
14 Evaluation & Guardrails
```

**Why this order:**

- **01-04 (fundamentals of talking to a model)** come first because every later topic assumes you know what a token, a context window, and a structured response are. You cannot reliably call a tool if you do not understand why the model sometimes returns malformed JSON.
- **05 (agent loops)** is the hinge of the whole curriculum: it is the first point where "calling an LLM" becomes "building an agent." Everything before it is a single request/response; everything after it assumes a loop exists.
- **06-08 (memory, RAG, MCP)** extend what the agent can know and remember, in increasing order of complexity: session state, then external documents, then a standard protocol for external tools and context.
- **09-12 (subagents, hooks, CI/CD, multi-agent)** are about composition and integration, moving from a single agent to systems of agents wired into real developer workflows.
- **13-14 (cost, evaluation)** come last on purpose. You cannot meaningfully evaluate or optimise a system you have not built yet, and premature optimisation of an agent you don't understand is a waste of time. These are the topics that separate "it worked in a demo" from "it is safe to run unattended."

See [notes/README.md](notes/README.md) for the full table of contents and status.

## Framework progression

Frameworks are learned **after** the manual concepts, not instead of them. See:

- [frameworks/langchain/README.md](frameworks/langchain/README.md)
- [frameworks/langgraph/README.md](frameworks/langgraph/README.md)

Each framework README explicitly answers: what problem does this solve, what did I need to understand before using it, what would the manual version look like, and what abstraction does it actually provide.

## Projects

A progression of small, real projects that combine AI and DevOps, roadmap in [projects/README.md](projects/README.md). Only Project 1 is implemented so far; the rest are scoped but not yet built.

| # | Project | Status |
|---|---------|--------|
| 1 | Direct LLM API application | done |
| 2 | Tool-calling agent | planned |
| 3 | RAG application | planned |
| 4 | Agent implemented without a framework | planned |
| 5 | LangChain agent | planned |
| 6 | LangGraph workflow | planned |
| 7 | DevOps troubleshooting agent | planned |
| 8 | Agentic CI/CD assistant | planned |

## Learning agent

[learning-agent/](learning-agent/) is a small local CLI tutor for working through the curriculum in this folder. It is not a chatbot: it tracks which topics you've covered, asks questions before giving answers, and refuses to let you jump ahead of prerequisites you haven't demonstrated understanding of. See [learning-agent/README.md](learning-agent/README.md) for usage.

It deliberately does **not** use LangChain or LangGraph. Since its own job is to teach the concepts in topics 01-05 (LLM APIs, prompting, structured output, tool use, agent loops), it is built as a plain Python implementation of exactly those concepts. A LangGraph rewrite is a plausible future milestone, once the underlying loop is well understood, not before.

## Connection to DevOps

Every topic in this curriculum has a DevOps-shaped analogue, and the later notes call it out explicitly:

- Tool calling is an API integration with an unusually chatty client.
- The agent loop is a reconciliation loop (observe, diff against desired state, act), the same shape as a Kubernetes controller.
- Memory and persistence is state management under restarts, the same problem as session stores and checkpointing.
- Hooks and automation is CI pipeline stages with an LLM step inserted, gated the same way you'd gate a deploy step.
- Multi-agent orchestration is service orchestration: supervisor patterns, retries, and failure isolation are the same concerns as microservices.
- Cost and performance is capacity planning, just for tokens instead of CPU.
- Evaluation and guardrails is the same discipline as testing and access control, applied to a nondeterministic component.

Topic [11-agentic-cicd.md](notes/11-agentic-cicd.md) and Project 8 make this connection concrete: an agent that reads CI failure logs, proposes a root cause and a fix, and stops for human approval before anything touches production.

## Future roadmap

- Implement Projects 2-8 in order, each building on the last.
- Migrate the learning agent from plain Python to LangGraph once topics 08-09 are solid, as a worked example of "framework replaces code you already understand."
- Add a real MCP server exposing this repo's notes as resources, once topic 08 is written and understood.
- Expand evaluation (topic 14) with an actual eval harness once Project 7 or 8 exists to evaluate.
