# 13. Cost & Performance

---

## Part 1: What It Is

What does cost and performance engineering mean for LLM systems?
> Treating model usage like any other production resource: measured, budgeted, optimised, and alerted on. The billing unit is the token (input and output priced separately, output typically several times dearer), the latency unit is largely output-token generation time, and both scale with usage patterns you control. This is capacity planning where the meter runs per token instead of per CPU-hour.

---

## Part 2: Why It Matters

Why does this deserve its own topic near the end?
> Because agents multiply everything. A chatbot does one call per user turn; a topic 05 loop does ten; a topic 12 supervisor with three workers does fifty, and *input tokens grow with the transcript on every iteration*, so loop cost is roughly quadratic in conversation length, not linear. A workflow that costs $0.30 per run is a curiosity in a demo and a $9,000/month line item at a thousand runs a day. It's placed late because you optimise a system you've built and understood, but in production thinking, cost is a day-one design constraint, not a retrofit.

---

## Part 3: Core Concepts

What should you know about token usage?
> Measure it before optimising it, every API response reports input and output token counts; log them per call, aggregate per run, per workflow, per day. The usual surprises when people first look: the system prompt and tool definitions are resent with *every* call in a loop, verbose tool results (topic 04's firehose warning) dominate input growth, and long transcripts make late iterations several times dearer than early ones.

What drives latency?
> Mostly output length: generation is token-by-token, so a 2,000-token answer takes roughly ten times as long as a 200-token one, the cheapest latency fix is often "answer more concisely" in the prompt. Time-to-first-token adds a base cost per call, which is why loop iterations count: an eight-step agent pays it eight times, serially. Streaming (topic 01) improves *perceived* latency only, and parallelising independent calls (topic 12) improves wall-clock but not cost.

How does model selection work as an optimisation?
> The workhorse technique: match model tier to step difficulty. Classify a log line or extract fields, small fast cheap model; propose a fix for a subtle failure, frontier model. Order-of-magnitude price differences between tiers mean **routing**, cheap model for routine cases, escalation on low confidence or high stakes, often cuts cost 5-10x with negligible quality loss. The topic 01 trade-off, now applied per-step instead of per-project.

What does caching offer?
> Two kinds. **Prompt caching** (provider-side): a large stable prefix, system prompt, tool definitions, reference docs, is cached and heavily discounted (often ~90%) on reuse; agents benefit hugely since every iteration resends that prefix. Design for it: static content first, variable content last, since caching works on unchanged prefixes. **Response caching** (your side): identical or near-identical requests (the same error signature analysed twice) can be served from a normal cache without any model call, the cheapest token is the one never generated.

What about batching?
> For latency-insensitive bulk work (nightly log triage, backfills, evals), most providers offer batch APIs at ~50% discount with relaxed delivery times. The classic interactive-vs-batch split from any capacity-planning playbook: don't pay real-time prices for work nothing is waiting on.

How do rate limits, retries, and fallbacks fit?
> Standard distributed-systems hygiene, applied to a dependency that *will* throttle you: respect rate limits with client-side throttling and exponential backoff with jitter on 429s/timeouts, cap retry budgets (retrying a whole agent run is not the same as retrying one call, know which you're doing and what each costs), and define fallbacks, another model, a degraded deterministic path, or an honest "analysis unavailable", so the provider's bad hour doesn't become your outage. An agent whose loop breaks on the first 429 was never production-ready.

What does cost monitoring look like?
> Like any other metric: per-call token/cost logging tagged by workflow and step, dashboards for cost per run and per day, budget alerts at soft thresholds, and hard caps (a run that exceeds its token budget stops, a topic 05 stopping condition doing double duty as cost control). Anomaly detection earns its keep here: a stuck agent loop is a cost incident, and you want the alert before the invoice.

What is context-size discipline as an optimisation?
> Everything from topics 01 and 06, now with a price tag: trim tool results, summarise old transcript, retrieve selectively instead of pasting wholesale, cap iteration counts. The cheapest optimisation in the entire list is sending fewer tokens, and it usually *improves* quality too, less noise for the model to attend through. Distrust any optimisation plan that starts anywhere else.

---

## Part 4: Simple Explanation

> Run the agent like a service with a cloud bill. You'd never ship a service without metrics, so log tokens per call. You'd never run every workload on the biggest instance type, so route easy steps to cheap models. You'd cache anything hot (prompt caching), move batch work off peak pricing (batch APIs), handle throttling like an adult (backoff, fallbacks), and alert before the bill surprises you (budgets, caps). Nothing here is new discipline, it's FinOps and SRE habits pointed at a new meter.

---

## Part 5: Practical Example

A cost-aware wrapper for the topic 05 loop:

```python
import random
import time

PRICES = {  # $ per million tokens: (input, output) - check current pricing
    "claude-sonnet-4-5": (3.00, 15.00),
    "claude-haiku-4-5":  (1.00, 5.00),
}

class CostTracker:
    def __init__(self, budget_usd: float):
        self.budget, self.spent, self.calls = budget_usd, 0.0, []

    def record(self, model: str, usage) -> None:
        inp, out = PRICES[model]
        cost = usage.input_tokens * inp / 1e6 + usage.output_tokens * out / 1e6
        self.spent += cost
        self.calls.append({"model": model, "in": usage.input_tokens,
                           "out": usage.output_tokens, "usd": round(cost, 5)})

    def over_budget(self) -> bool:
        return self.spent >= self.budget

def call_with_retry(client, tracker, *, max_attempts=4, **kwargs):
    for attempt in range(max_attempts):
        try:
            r = client.messages.create(**kwargs)
            tracker.record(kwargs["model"], r.usage)
            return r
        except anthropic.RateLimitError:
            time.sleep(2 ** attempt + random.random())   # backoff with jitter
    raise RuntimeError("Rate limited after retries")

# In the loop, budget as a stopping condition alongside max iterations:
if tracker.over_budget():
    return f"Stopped: budget ${tracker.budget} reached after {len(tracker.calls)} calls."
```

Routing, in one line of design: classify-type steps call `claude-haiku-4-5`, diagnose-type steps call the stronger model, and the tracker's per-model log tells you whether the split is earning its complexity.

---

## Part 6: How It Relates to Agents

> Agents are the reason this topic exists at this severity: loops multiply calls, transcripts inflate input, subagents (09) and multi-agent systems (12) multiply the multiplication, and event-driven triggers (10, 11) mean it all happens unattended at whatever rate events arrive. Cost caps are agent stopping conditions; latency budgets shape loop and orchestration design; routing decides which model each step deserves. An agent design that ignores cost isn't incomplete, it's unshippable.

---

## Part 7: Common Mistakes

- Optimising without measuring, no per-call token logging means every intuition about "what's expensive" is a guess, usually wrong.
- Frontier models for every step including trivial classification, the single most common overspend.
- Ordering prompts so variable content precedes stable content, silently defeating prompt caching.
- Ignoring the transcript-growth effect and being shocked that iteration 12 costs six times iteration 2.
- Retry logic that multiplies cost, re-running entire agent loops on failures where one call-level retry would do.
- No hard caps: a bug that loops an agent is a *financial* incident, and only a budget stop contains it.
- Over-optimising early: aggressive summarisation and cheap-model routing that degrades quality to save cents on a workflow that runs ten times a day. Measure first, then optimise where the money actually is.

---

## Part 8: Things I Should Know Before Moving On

- Why loop cost grows quadratically with transcript length, and what that implies for context discipline.
- The big four levers in rough order: send fewer tokens, route models by step difficulty, exploit prompt caching, batch the batchable.
- Budget caps as stopping conditions, and cost monitoring as ordinary observability.
- Backoff, retry budgets, and fallbacks as table stakes for a throttling dependency.

---

## Part 9: Practical Exercise

Instrument your topic 05 agent with the `CostTracker` and run three investigations. From the per-call log, answer: what fraction of spend was input vs output tokens? How did per-iteration cost grow across the run? What would each run cost at 500 runs/day? Then apply the two cheapest levers, cap tool results harder and move any classification step to a small model, and measure the delta. The habit of *measuring* the delta, not assuming it, is the topic.

---

## Part 10: Suggested Project

Add a cost report to any project you've built so far ([Project 4](../projects/README.md) is ideal): per-run JSON cost summaries, a cumulative daily log, a budget cap wired in as a stopping condition, and a one-page "cost at 10x/100x scale" projection. Carry the pattern forward into Projects 7 and 8, where event-driven triggering makes it non-optional.
