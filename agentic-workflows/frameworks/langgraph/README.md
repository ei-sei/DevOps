# LangGraph

> Frameworks are learned AFTER understanding the underlying concepts. LangGraph in particular assumes you know what an agent loop is ([05](../../notes/05-agent-loops.md)), how state works ([06](../../notes/06-memory-and-persistence.md)), and why multi-agent structures exist ([09](../../notes/09-subagents.md), [12](../../notes/12-multi-agent-workflows.md)) - it is a tool for building those, not a substitute for understanding them.

## What problem does this framework solve?

The topic 05 loop is fine for one agent with tools. But by topic 12 the control flow got genuinely hard by hand: branches that depend on runtime results, loops with cycles, parallel fan-out and merge, state shared across many steps, pausing mid-run for a human, and resuming a crashed workflow from where it stopped. LangGraph models an agent workflow as an explicit **state machine / graph**, and gives you checkpointing, conditional routing, and human-in-the-loop interrupts as first-class features instead of hand-rolled machinery.

## What did I need to understand before using it?

- The agent loop itself ([05](../../notes/05-agent-loops.md)) - a LangGraph agent is your loop drawn as a graph
- State and checkpointing ([06](../../notes/06-memory-and-persistence.md)) - its checkpointer is topic 06's JSON snapshot, productionised
- Subagents and orchestration ([09](../../notes/09-subagents.md), [12](../../notes/12-multi-agent-workflows.md)) - supervisor and pipeline patterns are what the graphs express
- Human approval gates ([10](../../notes/10-hooks-and-automation.md)) - its `interrupt` is topic 10's approval hook, made resumable

## What would implementing this manually look like?

You built each piece already:

| LangGraph concept | Manual version you built |
|---|---|
| **Graph / nodes / edges** | Functions called in sequence by the topic 12 pipeline - the graph just makes the call order explicit data |
| **State** (typed dict flowing through nodes) | The `messages` list plus scratch state from topics 05-06 |
| **Conditional routing** | `if "COULD_NOT_DETERMINE" in findings: return early` - topic 12's boundary checks as edges |
| **Loops / cycles** | `for iteration in range(MAX_ITERATIONS)` - topic 05 |
| **Persistence / checkpoints** | `save_state()` / `load_state()` to JSON after each step - topic 06 |
| **Human-in-the-loop** | The `input("Allow? [y/N]")` approval hook - topic 10, except LangGraph can suspend the run durably and resume days later |
| **Agent orchestration** | Supervisor dispatching to workers - topic 12's Part 5 pipeline |

The honest comparison: your manual versions are simpler and fully transparent; LangGraph's versions survive crashes, resume across processes, and stay manageable as the graph grows past what readable hand-rolled control flow can express.

## What abstraction does the framework provide?

- **Explicit topology**: control flow as data (nodes and edges), which you can visualise, test per-node, and reason about - versus control flow buried in nested Python.
- **Durable execution**: every step checkpointed to a store; crash mid-run and resume from the last good node, not from scratch.
- **Interrupts**: first-class pause-for-human on any edge, resumable, which is what makes approval gates practical in long-running workflows.
- **Cycles with governance**: loops are legal in the graph but bounded and inspectable.

The trade-off is the standard one: a graph definition is more ceremony than a for-loop, and for a single agent with four tools it's strictly overkill. LangGraph earns its keep at exactly the point topic 12 identified - when the coordination itself is the hard part.

## Learning checklist

- [ ] Rebuild the topic 05 loop as a two-node graph (agent node, tools node, conditional edge) and confirm identical behaviour
- [ ] Add a checkpointer; kill the process mid-run and resume - compare with your topic 06 `--resume` flag
- [ ] Add an interrupt before a "dangerous" tool, approving from a restarted process
- [ ] [Project 6](../../projects/README.md): the topic 12 pipeline as a graph with conditional routing and a human gate
- [ ] Future milestone: port the [learning agent](../../learning-agent/) to LangGraph - the planned proof that the manual version taught the right shapes
