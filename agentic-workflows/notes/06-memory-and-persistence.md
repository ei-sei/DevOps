# 06. Memory & Persistence

---

## Part 1: What It Is

What is "memory" for an LLM-based system?
> Any mechanism that lets the system carry information beyond a single model call: the conversation so far, facts learned about the user, results of previous sessions, checkpoints of an in-progress task. The model itself remembers nothing between API calls, so all memory is something *your application* stores and re-supplies.

What is the difference between memory and simply passing previous messages back?
> Passing the message history back is the simplest memory, and it's what chat interfaces do, but it's raw, unbounded, and undifferentiated: everything is kept, nothing is prioritised, and it grows until it overflows the context window. "Memory" as a designed feature means *selectively* deciding what to keep, in what form, where to store it, and what subset to reinject into any given call. History replay is a tape recorder; memory is note-taking.

---

## Part 2: Why It Matters

Why can't you just keep appending to the message list forever?
> Three compounding costs. The context window is finite, so a long-running agent will eventually overflow it mid-task. You pay for every input token on *every* call, so resending a huge history makes each iteration progressively more expensive. And models attend less reliably to the middle of very long contexts, so more history can mean *worse* answers. Memory management is therefore not a nice-to-have, it's what makes agents viable beyond short runs.

---

## Part 3: Core Concepts

What is short-term (session) state?
> The working memory of a single run: the message history, plus any explicit scratch state the agent maintains (a task list, findings so far, a token budget counter). Lives in process memory, dies with the run, unless checkpointed.

What is long-term memory?
> Information that survives across sessions: user preferences ("always use the staging cluster"), facts learned in previous runs ("the payments service owns topic X"), and outcomes of past tasks. Stored externally (files, a database), and *selectively retrieved* into context when relevant, not all of it, every time.

What does context management mean in practice?
> The set of techniques for keeping context useful and bounded: **truncation** (drop oldest messages, cheap but loses information), **summarisation** (have the model compress older history into a paragraph, keeping recent messages verbatim), **selective retrieval** (store everything externally, inject only what's relevant now), and **structured notes** (the agent maintains an explicit "what I know so far" document instead of relying on the transcript). Real systems combine several.

What are checkpoints?
> A checkpoint is a serialised snapshot of an agent's full state (messages, scratch state, progress) written to durable storage, so a crashed or interrupted run can resume instead of restarting from scratch. Same concept as checkpointing a long batch job or the difference between a stateless and stateful workload: for any agent doing more than a minute of work, resumability matters.

Where does persistence actually live?
> Start with the simplest thing: **JSON files** for single-user local tools (the learning agent in this folder does exactly this), **SQLite** when you need queries without a server, a real **database** (Postgres, Redis) for concurrent multi-user systems, and **vector stores** for semantic retrieval, which is the subject of topic 07. Choosing Postgres for a single-user CLI tutor is the same over-engineering as running Kubernetes for a static site.

How does session state differ from long-term memory in shape?
> Session state is complete and chronological, the full transcript plus scratch data, because within a run you generally want everything. Long-term memory is sparse and semantic, distilled facts indexed by topic, because across runs you only ever want the relevant slice. Different shapes, different stores, different retrieval patterns.

---

## Part 4: Simple Explanation

> Think of an engineer working a multi-day incident. Their terminal scrollback is session state, everything that happened this shift, in order. Their incident doc is summarisation, key findings distilled so the next shift doesn't replay the scrollback. The team wiki is long-term memory, durable facts that outlive the incident. And a handover note mid-shift is a checkpoint. An agent needs exactly these layers, and for exactly the same reason: no single view can be both complete and usable.

---

## Part 5: Practical Example

A minimal persistent-state pattern (the same one the [learning agent](../learning-agent/) uses):

```python
import json
from pathlib import Path

STATE_FILE = Path("agent_state.json")

DEFAULT_STATE = {"completed_tasks": [], "known_facts": {}, "current_task": None}

def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return dict(DEFAULT_STATE)

def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2))

# In the agent loop: inject only the relevant slice, not everything
state = load_state()
system_prompt = (
    "You are a DevOps assistant.\n"
    f"Known facts about this environment: {json.dumps(state['known_facts'])}\n"
    f"Previously completed: {', '.join(state['completed_tasks'][-5:]) or 'nothing yet'}"
)

# ... run the loop from topic 05 ...

state["completed_tasks"].append("diagnosed shop namespace restarts")
state["known_facts"]["shop_namespace"] = "pods were OOMKilled; memory limit was 128Mi"
save_state(state)
```

The two ideas that matter: state survives the process (a later run knows what an earlier run learned), and injection is *selective*, the last five tasks and the fact table, not an ever-growing transcript.

---

## Part 6: How It Relates to Agents

> Memory determines an agent's ceiling. Without it, every run starts ignorant, long tasks die at the context limit, and crashes lose everything. With it, agents resume after interruption, accumulate environmental knowledge, and handle tasks far larger than one context window. Subagents (topic 09) lean on this too: isolating a child agent's context *is* a memory-management technique, and RAG (next topic) is memory's close cousin, retrieving relevant knowledge into context on demand.

---

## Part 7: Common Mistakes

- Conflating "chat history" with "memory" and assuming replaying messages scales, it doesn't, for the three reasons in Part 2.
- Injecting *all* stored memory into every call, recreating the context problem you were solving.
- Summarising too aggressively and losing load-bearing details (the error message, the exact flag), keep recent history verbatim, compress only the old.
- No checkpointing on long runs, a crash at step 47 of 50 means starting over.
- Reaching for a vector database when a JSON file serves, infrastructure should follow need.
- Never expiring or correcting stored facts, stale memory ("the API lives on port 8080") confidently misleads every future run. Memory needs invalidation, same as any cache.

---

## Part 8: Things I Should Know Before Moving On

- Why history replay isn't memory, and the four context-management techniques.
- The session state vs long-term memory distinction, and the different shapes they take.
- What checkpointing buys and when it's worth it.
- The escalation path for persistence: JSON → SQLite → real database → vector store, driven by need.

---

## Part 9: Practical Exercise

Take your topic 05 agent and add: (1) a checkpoint written after every iteration (messages plus iteration count to a JSON file), (2) a `--resume` flag that restores it, and (3) a `facts.json` the agent updates when it learns something durable, injected into the system prompt on later runs. Kill the agent mid-run and confirm resume works. Then run two related investigations back-to-back and confirm the second benefits from the first's facts.

---

## Part 10: Suggested Project

The [learning agent](../learning-agent/) in this folder is the working example: JSON persistence of topic progress, quiz scores, and weak areas across sessions. Read its `config.py` and the state handling in `agent.py` with this note in mind, it's deliberately the simplest version of everything above.
