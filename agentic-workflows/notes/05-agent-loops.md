# 05. Agent Loops

---

## Part 1: What It Is

What is an agent?
> An agent is an LLM given tools and run in a loop until a goal is reached. Each iteration: the model observes the current state (conversation so far, latest tool results), reasons about what to do next, acts (calls a tool or produces a final answer), and the loop feeds the outcome back in. That's the entire trick, there is no additional magic component.

```text
Observe
   |
Reason / Decide
   |
Act (tool call or final answer)
   |
Observe result
   |
Decide again
   |
  ...until a stopping condition
```

What's the difference between an agent and a chatbot?
> A chatbot does one model call per user turn: you ask, it answers, done. An agent takes a goal and autonomously performs *multiple* model calls and tool executions before coming back to you. The user's single message "why is checkout failing?" might trigger eight tool calls and nine model invocations internally. Autonomy over multiple steps is the defining property, not intelligence.

---

## Part 2: Why It Matters

Why is the loop the hinge of the whole curriculum?
> Everything before this topic is a single request/response; everything after assumes a loop exists. Memory (06) is state that survives loop iterations and sessions. Subagents (09) are loops inside loops. Multi-agent workflows (12) are coordinated loops. Cost control (13) is largely about loops that run too long. If you understand this ~40-line pattern deeply, every framework you meet later is recognisably just this with extra structure.

To a DevOps engineer, what should this loop look like?
> A reconciliation loop, the same shape as a Kubernetes controller: observe current state, compare against desired state (the goal), take an action to close the gap, re-observe. The differences are that the "controller logic" is a nondeterministic model, and termination isn't guaranteed, which is exactly why stopping conditions get their own section below.

---

## Part 3: Core Concepts

What is the agent's state?
> Minimally, the message history: every user message, model response, tool call, and tool result so far. That history *is* the agent's working memory within a run, because each model call receives the whole of it. Richer agents add explicit state outside the transcript (task lists, scratch data, budgets), which topic 06 develops.

How does the model select tools across a loop?
> Each iteration, the model sees all tool definitions plus everything that's happened, and picks the next action. Good sequencing emerges from good tool descriptions and a system prompt that sets strategy ("start by listing pods before fetching logs"; "prefer the cheapest sufficient check first"). If the model keeps choosing badly, fix the descriptions and prompt before reaching for cleverer code.

What are stopping conditions, and why are they non-negotiable?
> The loop must end. Natural stop: the model responds with a final answer instead of a tool call. Enforced stops you must add yourself: a **maximum iteration count** (the seatbelt), a token/cost budget, a wall-clock timeout, and explicit failure ("I cannot determine the cause"). An agent without a max-iterations cap is an unbounded while-loop where every iteration costs money, never ship one.

How do retries fit in?
> Two distinct kinds. *Within* an iteration: transient API failures (rate limits, timeouts) get standard retry-with-backoff, invisible to the loop. *Across* iterations: a failed tool call goes back to the model as an error result, and the model itself decides to retry differently, that's the loop self-correcting, and it's why errors-as-results (topic 04) matters so much.

What are the classic failure modes of agent loops?
> **Infinite loops** (repeating the same failing call, caught by the iteration cap and by detecting repeated identical calls), **context overflow** (long runs blowing the window, addressed in topic 06), **goal drift** (wandering off-task mid-investigation), **premature success** (declaring done without verifying), and **error spirals** (each fix causing the next problem). Every one of these has an ops analogue: crash loops, memory leaks, config drift, and green health checks on a broken service.

---

## Part 4: Simple Explanation

> Hand a capable colleague a ticket: "checkout is failing, find out why." They look at the dashboard (observe), decide the logs are the next lead (reason), pull them (act), read them (observe result), decide to check the recent deploy (reason), and so on until they write up a diagnosis or conclude they're stuck. An agent is that investigation with a model making each decision, and your code enforcing the rules: which actions exist, how many steps are allowed, and when to stop.

---

## Part 5: Practical Example - an agent loop without any framework

This is the important one. The complete pattern, no LangChain, no abstractions:

```python
import anthropic

client = anthropic.Anthropic()
MODEL = "claude-sonnet-4-5"
MAX_ITERATIONS = 10

TOOLS = [...]           # tool definitions as in topic 04
TOOL_FUNCTIONS = {...}  # {"kubectl_get_pods": kubectl_get_pods, ...}

SYSTEM = (
    "You are a DevOps investigation agent. Use the available tools to "
    "diagnose the user's issue. When you have a conclusion (or determine "
    "you cannot reach one), respond with your final answer instead of "
    "calling more tools."
)

def run_agent(goal: str) -> str:
    messages = [{"role": "user", "content": goal}]

    for iteration in range(MAX_ITERATIONS):
        response = client.messages.create(
            model=MODEL, max_tokens=2048, system=SYSTEM,
            tools=TOOLS, messages=messages,
        )
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":            # natural stop
            return next(b.text for b in response.content if b.type == "text")

        results = []
        for block in response.content:                     # act
            if block.type == "tool_use":
                fn = TOOL_FUNCTIONS.get(block.name)
                try:
                    output = fn(**block.input) if fn else f"Error: unknown tool {block.name}"
                except Exception as e:                     # errors go back as data
                    output = f"Error running {block.name}: {e}"
                print(f"[{iteration}] {block.name}({block.input})")   # observability
                results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(output)[:4000],          # cap result size
                })
        messages.append({"role": "user", "content": results})  # observe result

    return "Stopped: iteration limit reached without a conclusion."  # enforced stop

print(run_agent("Pods in the 'shop' namespace keep restarting. Diagnose why."))
```

Everything essential is visible in ~40 lines: state is `messages`, the decision is the model call, actions are dictionary-dispatched functions, errors return as data, results are size-capped, every step is logged, and two stopping conditions bound the run. Every agent framework you will ever use is this loop with more structure around it.

---

## Part 6: How It Relates to Agents

> This *is* the agent. Later topics don't replace the loop, they attach things to it: persistent state (06), retrieved context (07), a standard tool protocol (08), child loops (09), event triggers (10), and evaluation around the outside (14). When a framework agent misbehaves later, the debugging move is always to ask "where in this loop is it going wrong?", which you can only do if you've built the loop bare-handed once.

---

## Part 7: Common Mistakes

- No iteration cap, unbounded loops that burn money until someone notices.
- Killing the run on tool exceptions instead of returning the error to the model.
- No logging of tool calls, making misbehaving agents undebuggable. Log every action with its arguments, like an audit trail.
- Letting huge tool results accumulate until the context overflows mid-run.
- No detection of the agent repeating the same failing call verbatim.
- Trusting "the agent said it's done": for anything that matters, verify the claimed result (run the test, hit the endpoint) rather than believing the transcript.
- Jumping to a framework before ever writing this loop yourself, and thus never knowing what the framework is actually doing.

---

## Part 8: Things I Should Know Before Moving On

- The observe → reason → act → observe cycle, and where state lives (the message list).
- Both kinds of stopping condition (natural and enforced) and both kinds of retry.
- The five failure modes and their guards.
- The Part 5 code well enough to rewrite it from memory, it's the foundation of everything after this.

---

## Part 9: Practical Exercise

Implement the Part 5 loop with the two tools from topic 04's exercise. Then engineer each failure mode and confirm your guards catch it: point a tool at a permanently failing target (does the model adapt or spiral?), set `MAX_ITERATIONS = 2` on a task needing more (does it stop cleanly?), and make a tool return 100KB of noise (what happens to the context?). Breaking your own agent on purpose teaches more than any successful run.

---

## Part 10: Suggested Project

[Project 4: Agent without a framework](../projects/README.md), a polished version of this loop: config-driven tools, JSON-lines audit logging of every step, a cost budget as a stopping condition, and repeated-call detection. This is the reference implementation you'll compare LangChain and LangGraph against in Projects 5 and 6.
