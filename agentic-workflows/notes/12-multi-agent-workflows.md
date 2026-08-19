# 12. Multi-Agent Workflows

---

## Part 1: What It Is

What is a multi-agent workflow?
> A system where several agents, each with its own loop, prompt, and tools, cooperate on a task under some coordination structure: a fixed sequence, a parallel fan-out, or a supervisor dynamically routing work. Topic 09's parent/child pair was the two-agent special case; this topic is the general patterns and, importantly, the reasons to avoid them.

Are multi-agent systems automatically better than single agents?
> No, and this question is the heart of the topic. Every agent boundary costs money (separate model calls), latency, and *information*, context lost at each handoff, exactly as topic 09 showed. A multi-agent system is a distributed system, with a distributed system's debugging difficulty, and the industry's honest experience is that many multi-agent designs underperform one well-prompted agent with good tools. Architecture should be forced by a real constraint, not chosen for sophistication.

---

## Part 2: Why It Matters

When do you genuinely need multiple agents?
> Three forcing constraints. **Context**: the task's working set exceeds what one window can hold well, splitting isolates each agent's slice (the topic 09 argument at scale). **Parallelism**: genuinely independent subtasks (review five services' configs) can run concurrently for wall-clock wins. **Conflicting specialisations**: one prompt can't simultaneously be a thorough critic and a fast drafter, adversarial or reviewer patterns need separate identities. If none of these applies, the honest answer is usually one agent with better tools and a better prompt.

---

## Part 3: Core Concepts

What is sequential orchestration?
> A fixed pipeline: research agent → coding agent → testing agent → docs agent, each consuming the previous output. Simplest to reason about and debug (one thing happens at a time, clear handoff artefacts), at the cost of total latency being the sum of stages, and early errors compounding downstream, assembly-line semantics, assembly-line failure modes.

What is parallel orchestration?
> Independent subtasks fanned out simultaneously, results gathered and merged. Wall-clock wins scale with independence; the hard part is the merge (combining five partial analyses coherently) and partial failure (three succeed, one times out, one returns garbage, ship partial results, retry, or fail?). Scatter-gather, with scatter-gather's classic problems.

What is the supervisor pattern?
> A coordinator agent that owns the goal, decomposes it, dispatches to workers, evaluates returns, and iterates, dynamic routing rather than a fixed pipeline, so the structure adapts to what's discovered mid-task. The costs: the supervisor is a single point of failure whose mistakes multiply (bad decomposition wastes every worker), and it burns tokens on every routing decision. Delegation here is topic 09's brief-writing, at scale.

How do agents share state and communicate?
> Two broad shapes. **Message passing**: results flow along the structure (child to parent, stage to stage), simple, explicit, but strictly limited to what handoffs carry. **Shared state**: a common store (files, a database, a blackboard) that agents read and write, richer coordination, and the same hazards shared mutable state always brings: stale reads, write conflicts, ordering. A useful middle ground is an append-only shared log: agents post findings, everyone reads, nothing is overwritten, the event-sourcing instinct applied to agents.

How is failure handled across a multi-agent system?
> Layered, like any distributed system. Per-agent: the topic 05 guards (iteration caps, budgets, timeouts). Per-handoff: validate results at boundaries, don't propagate garbage (topic 09's trust problem). System-wide: overall budget and timeout, a defined partial-failure policy per pattern (a pipeline stage failing halts or falls back; one parallel branch failing usually shouldn't sink the rest), and an audit trail of who did what, without which debugging a five-agent run is archaeology.

---

## Part 4: Simple Explanation

> One strong engineer with good tools outperforms a badly coordinated committee, and a committee only beats the individual when the work genuinely exceeds one person (too much to hold in one head, truly parallelisable, or needing adversarial roles like author-vs-reviewer). Committees also bring meetings (handoff overhead), miscommunication (context loss), and "I thought you were doing that" (coordination bugs). Add agents the way a good team adds headcount: reluctantly, for a named reason, with clear interfaces.

---

## Part 5: Practical Example

A sequential pipeline with boundary validation, built entirely from topic 05/09 pieces:

```python
def pipeline(task: str) -> str:
    findings = run_subagent(
        system_prompt=RESEARCH_PROMPT, brief=task,
        tools=[SEARCH_TOOL, READ_LOGS_TOOL],
    )
    if "COULD_NOT_DETERMINE" in findings:          # boundary check: don't
        return f"Stopped at research: {findings}"   # propagate garbage

    proposal = run_subagent(
        system_prompt=FIX_PROMPT,
        brief=f"Task: {task}\n\nResearch findings:\n{findings}",  # explicit handoff
        tools=[READ_FILE_TOOL, WRITE_FILE_TOOL],
    )

    verdict = run_subagent(
        system_prompt=REVIEW_PROMPT,                # separate identity: a critic,
        brief=f"Task: {task}\n\nProposed change:\n{proposal}",     # not the author
        tools=[READ_FILE_TOOL, RUN_TESTS_TOOL],
    )
    if verdict.startswith("REJECT"):
        return f"Change rejected by review: {verdict}"
    return f"Proposal:\n{proposal}\n\nReview: {verdict}"
```

Worth noticing: handoffs are explicit strings (all the next agent will know), each stage checks its input before building on it, the reviewer is a *different agent* than the author, the conflicting-specialisations rationale in action, and the whole thing is readable Python. When LangGraph models this as a graph in [frameworks/langgraph](../frameworks/langgraph/README.md), you'll know exactly what the edges mean.

---

## Part 6: How It Relates to Agents

> This is the composition ceiling of the curriculum: loops (05) exposed as tools (09), arranged into structures, nothing mechanically new, only coordination. It's also where the DevOps parallel is strongest: sequential pipelines are CI stages, parallel fan-out is a job matrix, the supervisor is a control loop managing workers, shared state is the same hazard it is in any concurrent system. Frameworks earn their keep at precisely this layer, LangGraph exists because hand-rolling *complex* graphs of agents gets genuinely hard, and the remaining topics (13, 14) are what multi-agent systems make urgent: multiplied cost, and evaluation of emergent behaviour.

---

## Part 7: Common Mistakes

- Multi-agent as the default architecture, chosen for impressiveness rather than forced by context, parallelism, or role conflict.
- Vague handoffs: agent B receiving a summary that lacks what it needs (topic 09's thin-brief failure, now at every boundary).
- Unmanaged shared mutable state, race-condition debugging with nondeterministic actors on top.
- No boundary validation, one agent's confident garbage becoming the next agent's trusted input.
- No system-level budget: five agents with individually reasonable caps still multiply to an unreasonable total.
- No run-wide audit trail attributing actions to agents.
- Skipping the baseline: never testing whether one good agent solves the task before building the committee. Build the single-agent version first, always.

---

## Part 8: Things I Should Know Before Moving On

- The three forcing constraints, and the discipline of demanding one before adding an agent.
- Sequential vs parallel vs supervisor: costs and failure modes of each.
- Message passing vs shared state, and why append-only logs are a sane middle ground.
- That handoff quality and boundary validation dominate multi-agent reliability.

---

## Part 9: Practical Exercise

Pick a task with an independent-parts structure (audit the Dockerfiles of three [docker/](../../docker/) projects against topic 06 best practices). Build it once as a single agent handling all three, and once as the Part 5 pipeline shape with a fan-out. Compare cost, wall-clock, and quality honestly, then write three sentences on which you'd ship and why. Discovering that the single agent wins on a task this size *is* the lesson, now you know where the threshold isn't.

---

## Part 10: Suggested Project

[Project 7: DevOps troubleshooting agent](../projects/README.md) with a supervisor structure: a coordinator owning the diagnosis, dispatching to a log-analysis worker, a config-inspection worker, and a history worker, merging findings into one incident report with per-agent attribution. Build it only after the single-agent Project 4 version, so the comparison from the exercise keeps you honest about what the extra agents buy.
