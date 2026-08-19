# 10. Hooks & Automation

---

## Part 1: What It Is

What are hooks in an agentic context?
> Hooks are deterministic scripts or checks that run automatically at defined points in an agent's lifecycle, before a tool executes, after it completes, when the agent finishes, when an event arrives, without the model deciding to run them. The agent reasons probabilistically; hooks enforce rules absolutely. "Run the linter after every file edit" as a hook *always* happens; as a prompt instruction it happens *usually*, and usually isn't a guarantee.

What is an event-driven agent workflow?
> An agent invoked by an event rather than a human: a CI failure fires a webhook that launches a log-analysis agent; an alert triggers an investigation agent; a PR opening triggers a review agent. The same trigger-action wiring DevOps already builds everywhere, with an agent as the action.

---

## Part 2: Why It Matters

Why do hooks matter more as agents become more autonomous?
> Because prompt instructions are requests, not controls. An agent told "never touch production config" will *almost* always comply, and almost-always is exactly the reliability level DevOps exists to engineer away. Hooks move critical rules out of the probabilistic layer into code: a pre-tool-use hook that blocks writes to `prod/` paths fails closed, every time, regardless of what the model "decided." The division of labour: the model handles judgement, hooks handle rules.

---

## Part 3: Core Concepts

What are pre-action hooks?
> Checks that run before a tool call executes and can block it: validate the command against an allowlist, reject writes outside permitted paths, require approval for anything matching a dangerous pattern (`rm -rf`, `terraform apply`, `kubectl delete`). This is admission control, the same concept as a Kubernetes admission webhook or a branch-protection rule: a policy gate in front of a requested action.

What are post-action hooks?
> Steps that run after an action completes: auto-format the file the agent just edited, run the tests after a code change, log every executed command to an audit trail, notify a channel when the agent finishes. They're the "verify and record" half, catching problems immediately and creating the paper trail that makes agent behaviour reviewable after the fact.

Where does validation fit?
> Hooks are where validation becomes *systematic* instead of per-tool: rather than trusting each tool function to sanitise its own inputs (topic 04), a single pre-action hook applies policy to every call uniformly, one place to audit, one place to update. Defence in depth says do both.

What is human approval as a control?
> A hook that pauses the workflow for a person on high-consequence actions: the agent proposes (`terraform apply` with this plan), a human disposes. The skill is placing the gate at the *consequence* boundary, not everywhere: approving every read makes humans rubber-stamp and defeats the purpose; approving every mutation of shared state is exactly right. Same philosophy as deployment approval stages in a pipeline.

What safety controls belong in hooks rather than prompts?
> Anything that must hold 100% of the time: path and command allowlists, credential-access blocks, rate and budget caps, environment fences (agent may touch staging, never prod), audit logging. The prompt can *also* say these things, belt and braces, but the hook is the enforcement layer. If violating a rule would page someone, that rule is a hook.

How do agents integrate with developer workflows?
> Through the event surfaces that already exist: git hooks (agent reviews staged changes pre-commit), CI steps (agent analyses failures, next topic), issue/PR webhooks (agent triages new issues), chat commands, schedulers (nightly dependency-audit agent). The mature pattern is the agent as *pipeline citizen*, triggered by events, bounded by hooks, reporting through normal channels, not a chat window someone has to remember to use.

---

## Part 4: Simple Explanation

> A capable new hire has judgement, but you still don't give them unreviewed prod access on day one. You give them an environment where guardrails are structural: CI runs whether or not they remember, branch protection blocks direct pushes to main, deploys need a second pair of eyes, and everything is logged. Hooks build exactly that environment around an agent. Nothing about it distrusts the agent's intelligence, it's the standard engineering answer to *any* capable-but-fallible actor, humans included.

---

## Part 5: Practical Example

A pre-action hook enforcing command policy (structure over completeness):

```python
import re

BLOCKED = [r"\brm\s+-rf\b", r"--force\b", r"\bkubectl\s+delete\b", r"\bDROP\s+TABLE\b"]
NEEDS_APPROVAL = [r"\bterraform\s+apply\b", r"\bkubectl\s+(apply|scale|rollout)\b"]

def pre_tool_hook(tool_name: str, tool_args: dict) -> tuple[bool, str]:
    """Returns (allowed, reason). Runs before EVERY tool call - no exceptions."""
    if tool_name != "run_command":
        return True, "ok"
    cmd = tool_args.get("command", "")
    for pat in BLOCKED:
        if re.search(pat, cmd, re.IGNORECASE):
            return False, f"Blocked by policy: matches {pat}"
    for pat in NEEDS_APPROVAL:
        if re.search(pat, cmd, re.IGNORECASE):
            answer = input(f"Agent wants to run: {cmd!r}. Allow? [y/N] ")
            return answer.lower() == "y", "human decision"
    return True, "ok"

# Wired into the topic 05 loop, replacing the direct dispatch:
allowed, reason = pre_tool_hook(block.name, block.input)
output = TOOL_FUNCTIONS[block.name](**block.input) if allowed \
         else f"Action blocked: {reason}"          # the block goes back as data
```

Real agent platforms make this declarative, e.g. Claude Code hooks in `settings.json` running arbitrary scripts on PreToolUse/PostToolUse events with the power to block, but the mechanic is identical: deterministic code interposed on every action, with denials returned to the model as information it can work with.

---

## Part 6: How It Relates to Agents

> Hooks are what make agent autonomy *affordable*: the more decisions the loop takes unsupervised, the more you need guarantees that don't depend on the model's judgement. They wrap the topic 05 loop without changing it (interposed at the act step), they're where topic 04's permission thinking becomes enforced policy, and they're the enabling layer for the next topic, nobody sanely wires an agent into CI/CD without exactly these controls. Topic 14 completes the picture with evaluation and sandboxing.

---

## Part 7: Common Mistakes

- Enforcing safety rules in the prompt alone, the canonical mistake this whole note exists to prevent.
- Denylist-only thinking: blocking known-bad patterns misses novel bad ones. Allowlists of known-good actions fail closed.
- Approval gates on everything, training humans to click yes reflexively. Gate consequences, not activity.
- Silent blocking: a hook that denies without telling the model *why* produces a confused agent retrying variants; return the reason as data.
- No audit trail, when (not if) an agent does something surprising, the post-action log is how you reconstruct it.
- Forgetting hooks are code with their own bugs: a broken pre-action hook that fails open is worse than none, because you *believe* you're protected. Test the hooks.

---

## Part 8: Things I Should Know Before Moving On

- The probabilistic/deterministic division: model for judgement, hooks for rules.
- Pre-action (admission control) vs post-action (verify and record), and what belongs in each.
- Where human approval earns its cost, and where it degrades into rubber-stamping.
- That agents join workflows through existing event surfaces: git, CI, webhooks, schedulers.

---

## Part 9: Practical Exercise

Wire the Part 5 hook pair into your topic 05 agent: pre-action policy enforcement plus a post-action hook appending every call (tool, args, allowed/blocked, result summary, timestamp) to a JSON-lines audit log. Then ask the agent to do something that requires a blocked command and watch it receive the denial, explain the constraint, and propose an alternative, an agent behaving well *because of* structural limits is the whole lesson.

---

## Part 10: Suggested Project

A pre-commit review hook: on `git commit`, an agent reviews the staged diff against a small checklist (secrets, debug prints, missing tests) and can veto with reasons, overridable with a flag, and logging every decision. Small, genuinely useful daily, and it exercises event triggering, pre-action gating, and audit logging in one artefact. It's also the seed of [Project 8](../projects/README.md), where the same pattern moves into CI.
