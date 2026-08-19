# 09. Subagents

---

## Part 1: What It Is

What is a subagent?
> A subagent is an agent launched by another agent to handle a delimited piece of work: it runs its own loop (topic 05) with its own context, tools, and system prompt, and returns a result to its parent. The parent treats "spawn a subagent" like any other tool call, delegate the task, receive the summary.

```text
Main Agent
├── Research Agent      (searches docs/code, returns findings)
├── Coding Agent        (writes the change)
├── Testing Agent       (runs and interprets the test suite)
└── Documentation Agent (updates the docs)
```

---

## Part 2: Why It Matters

What problem do subagents actually solve?
> Mostly a *context* problem, and this is the non-obvious part. A single agent doing a large task accumulates everything in one transcript: file dumps, dead-end searches, tool noise, until the context is bloated, expensive, and degrading the model's attention. A subagent absorbs all that mess in its own context and returns only the distilled result, three useful sentences instead of three thousand exploratory tokens in the parent's transcript. Specialisation is the second win: a focused prompt and a minimal tool set beat one agent juggling every concern.

---

## Part 3: Core Concepts

What is delegation, concretely?
> The parent formulates a task brief (goal, relevant context, expected output shape), spawns the child with it, and consumes the result. The brief is prompt engineering under topic 02's rules, and it's where delegation usually fails: the child knows *only* what the brief says. "Investigate the checkout failures in namespace shop, started ~14:00 UTC, return probable cause plus the evidence" delegates well; "look into the checkout thing" does not.

What makes a specialised agent better than a generalist?
> Narrower prompt, narrower tools, narrower success criteria. A testing agent whose entire system prompt is about running and interpreting this project's test suite, with only test-running tools, makes fewer tool-selection errors and produces more consistent output than a generalist deciding among thirty tools. Same reason single-purpose services are easier to operate than a monolith doing everything.

What is context isolation?
> Each subagent's transcript is its own: the parent doesn't see the child's intermediate steps, and the child doesn't see the parent's history beyond the brief. This is the memory-management payoff (topic 06 by other means), but it cuts both ways, isolation is also *information loss*. If the child needed a fact the parent forgot to include, the child fails or, worse, guesses. Brief quality is the price of isolation.

What does orchestration involve at this level?
> The parent decides what to delegate, in what order, with what briefs, and how to combine results, sequentially here (research, then code, then test). It also enforces budgets: a subagent is a loop, so it needs the same caps (iterations, cost, time) as any agent, plus the parent needs a plan for a child that returns nothing useful. Full multi-agent patterns, parallelism, supervisors, shared state, are topic 12; this note is the two-level parent/child case.

How should subagent failure be handled?
> The parent receives the child's result and must not blindly trust it, a subagent can fail loudly (error, budget exhausted) or quietly (confident wrong answer, the worse case). Treat child results like tool results: check them against expectations, retry with a sharpened brief where sensible, escalate to a human when retries don't converge. Verification of the "premature success" failure mode from topic 05 applies doubly, the parent asserting "the testing agent said tests pass" should ideally be checkable against the actual test exit code.

---

## Part 4: Simple Explanation

> A tech lead doesn't do everything in one head. They hand the investigation to one engineer, the fix to another, the test run to a third, each works in their own "context" (their own terminal, their own notes), and reports back a summary, not their scrollback. The lead's job becomes writing good task descriptions and judging returned work. Subagents are exactly this, with the same two classic failure modes: briefs that assume knowledge the delegate doesn't have, and accepting reported results without spot-checking them.

---

## Part 5: Practical Example

A subagent is just the topic 05 loop invoked as a tool:

```python
def run_subagent(system_prompt: str, brief: str, tools: list, max_iters: int = 8) -> str:
    """A fresh agent loop with its own context; returns only the final text."""
    return run_agent_loop(                 # the loop from topic 05
        system=system_prompt, goal=brief, tools=tools, max_iterations=max_iters,
    )

SUBAGENT_TOOL = {
    "name": "delegate_research",
    "description": ("Delegate a self-contained research question to a research agent "
                    "with doc-search and log-reading tools. Include ALL context the "
                    "researcher needs - it cannot see this conversation."),
    "input_schema": {
        "type": "object",
        "properties": {"brief": {"type": "string",
                       "description": "Complete task description with context and expected output"}},
        "required": ["brief"],
    },
}

def delegate_research(brief: str) -> str:
    return run_subagent(
        system_prompt=("You are a research agent. Investigate exactly the question in "
                       "the brief using your tools, and reply with findings plus evidence. "
                       "If you cannot answer, say what you tried and what's missing."),
        brief=brief,
        tools=[SEARCH_DOCS_TOOL, READ_LOGS_TOOL],   # narrow, read-only
    )
```

Three deliberate choices to notice: the tool description *warns the parent model* that the child can't see the conversation (directly improving brief quality), the child gets a narrow read-only tool set, and the child's prompt demands evidence and an explicit "couldn't answer" path, making quiet failure less likely.

---

## Part 6: How It Relates to Agents

> Subagents are agents composed recursively, the loop calling the loop, which is why topics 04-05 had to come first: a subagent invocation is a tool call whose implementation is another agent. This is the first step from "an agent" to "a system of agents": one parent, sequential children, results flowing up. Topic 12 generalises it to parallel execution, supervisor hierarchies, and shared state, and topic 13 will note the cost implication (every child is its own stream of model calls).

---

## Part 7: Common Mistakes

- Thin briefs, delegating with context the child doesn't have and can't get. The number one failure, and it's the *parent's* bug, not the child's.
- Spawning subagents for small tasks where one loop iteration would do, each spawn has overhead in latency, cost, and information loss at the boundary.
- Giving children the parent's full tool set instead of a scoped one, throwing away the specialisation and safety benefits.
- Trusting child summaries without verification, quiet failure propagates upward as confident wrongness.
- Unbounded children: no iteration/cost caps on something that is, by definition, an agent loop.
- Deep nesting (children spawning children spawning children) before mastering one level, debugging difficulty compounds per level.

---

## Part 8: Things I Should Know Before Moving On

- Context isolation as the core benefit *and* its price (information loss at the boundary).
- What a good brief contains, and why brief-writing is the parent's key skill.
- Subagent = agent loop exposed as a tool, no new mechanics.
- The trust problem: child results are claims, not facts.

---

## Part 9: Practical Exercise

Give your topic 05 agent the `delegate_research` tool from Part 5 and pose a task needing both research and action. Compare against the single-agent version on the same task: transcript sizes, token cost, and result quality. Then sabotage the brief deliberately, have the parent omit a key detail, and watch how the child fails, this builds the instinct for what briefs must contain.

---

## Part 10: Suggested Project

Extend [Project 4](../projects/README.md) (the no-framework agent) with a two-agent split: an investigator subagent (read-only tools, returns diagnosis with evidence) invoked by a main agent that owns the conversation and verifies findings. This structure carries directly into Project 7's troubleshooting agent, and is the pattern Claude Code itself uses for its Task/Explore agents.
