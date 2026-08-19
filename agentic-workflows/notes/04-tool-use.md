# 04. Tool Use

---

## Part 1: What It Is

What is tool use (function calling)?
> Tool use is the mechanism that lets an LLM request actions in the real world: you describe available functions to the model, and instead of (or alongside) prose, it can respond with a structured request to call one, e.g. `{"name": "get_pod_logs", "arguments": {"pod": "api-7d9f", "lines": 100}}`. Your code executes the function and sends the result back; the model then continues with real data.

Does the model execute anything itself?
> No, and this is the single most important fact in this topic. The model only ever emits a *request* to call a tool. Your code decides whether to honour it, executes it, and returns the result. The model has exactly as much power as your runtime grants it, no more.

---

## Part 2: Why It Matters

Why is tool use the moment LLMs become useful for operations work?
> Because it closes the gap between "the model can describe what to check" and "the system can actually check it." Without tools, an LLM can only reason about data you manually paste in. With tools, it can fetch logs, query APIs, run commands, and read databases on demand, which is the difference between a documentation search and a junior engineer with (carefully limited) shell access.

---

## Part 3: Core Concepts

What is a tool definition?
> A tool definition is a name, a natural-language description, and a JSON Schema for the parameters. The description is prompt engineering: the model decides *whether and when* to use a tool almost entirely from it, so "Get the last N lines of logs from a Kubernetes pod in the current namespace. Use when investigating pod failures." dramatically outperforms "gets logs."

How do tool arguments and results flow?
> Arguments arrive from the model as JSON matching your schema, and must be validated like any untrusted input (topic 03 applies directly). Results go back as a message in the conversation, so the model reads them as text. Keep results concise and relevant: returning 10,000 raw log lines burns context window and drowns the signal.

What kinds of tools come up in practice?
> **API calls** (query Prometheus, hit GitHub's API, check an endpoint's health), **shell commands** (`kubectl get pods`, `terraform plan`, usually a fixed allowlist rather than arbitrary shell), **database tools** (run a read-only query, look up a record), and **cloud tools** (describe EC2 instances, read CloudWatch metrics or S3 objects via boto3). The pattern is identical in all cases: schema in, validated execution, text result out.

What about tool permissions?
> Apply least privilege exactly as you would for a service account, because that's what the agent effectively is. Read-only tools by default; separate and gate destructive tools (restart, delete, apply) behind human approval; scope credentials to the minimum (a read-only IAM role, a single namespace). A tool the model shouldn't use freely shouldn't be freely available, don't rely on the prompt saying "be careful."

How should tool errors be handled?
> Return errors to the model as informative text results ("Error: pod 'api-7d9f' not found in namespace 'default'. Available pods: ..."), not as exceptions that kill the run. Given a clear error, models are genuinely good at correcting course: retrying with fixed arguments or choosing a different tool. A cryptic or swallowed error, by contrast, produces guessing.

---

## Part 4: Simple Explanation

> Tool use is a well-defined protocol between two parties. Your code says: "here are the functions you may request, with their signatures." The model says: "please run `get_pod_logs(pod='api-7d9f')`." Your code validates, executes, and replies: "here's what it returned." The model incorporates that and either requests another call or answers. It's an RPC system where one side is a language model, and your side holds all the actual capability.

---

## Part 5: Practical Example

A minimal tool-use round trip with the Anthropic SDK:

```python
import subprocess
import anthropic

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env

TOOLS = [{
    "name": "kubectl_get_pods",
    "description": "List pods in a namespace with status. Use when investigating workload health.",
    "input_schema": {
        "type": "object",
        "properties": {"namespace": {"type": "string", "description": "Kubernetes namespace"}},
        "required": ["namespace"],
    },
}]

def kubectl_get_pods(namespace: str) -> str:
    if not namespace.replace("-", "").isalnum():   # validate untrusted input
        return f"Error: invalid namespace {namespace!r}"
    result = subprocess.run(
        ["kubectl", "get", "pods", "-n", namespace],  # fixed command, no shell
        capture_output=True, text=True, timeout=30,
    )
    return result.stdout or f"Error: {result.stderr}"

messages = [{"role": "user", "content": "Are any pods unhealthy in the default namespace?"}]
response = client.messages.create(
    model="claude-sonnet-4-5", max_tokens=1024, tools=TOOLS, messages=messages,
)

if response.stop_reason == "tool_use":
    tool_call = next(b for b in response.content if b.type == "tool_use")
    output = kubectl_get_pods(**tool_call.input)          # execute on our side
    messages.append({"role": "assistant", "content": response.content})
    messages.append({"role": "user", "content": [{
        "type": "tool_result", "tool_use_id": tool_call.id, "content": output,
    }]})
    final = client.messages.create(
        model="claude-sonnet-4-5", max_tokens=1024, tools=TOOLS, messages=messages,
    )
    print(final.content[0].text)
```

Note the shape: the model *asked*, our code validated and executed a fixed argv (no shell injection surface), and the result went back as a message. This handles exactly one tool call, making it handle many is precisely what the next topic covers.

---

## Part 6: How It Relates to Agents

> A single tool call answers a question; an agent *chains* them, using each result to decide the next call. Tool use is therefore the last static building block: once the model can request actions and read results, wrapping that in a loop with a stopping condition gives you an agent. That loop is topic 05.

---

## Part 7: Common Mistakes

- Lazy tool descriptions, the number one cause of the model picking the wrong tool or none at all.
- Executing model-supplied arguments without validation (the classic: interpolating them into a shell string, command injection by LLM).
- Giving one broad tool ("run any shell command") instead of narrow, purpose-specific tools, harder to secure and harder for the model to use well.
- Returning raw firehose output as tool results instead of trimming to what's relevant.
- Raising exceptions on tool failure instead of returning a descriptive error the model can act on.
- Granting write/destructive capability in v1. Start read-only; add mutations only with approval gates (topic 10).

---

## Part 8: Things I Should Know Before Moving On

- The full round trip: definitions in, tool_use request out, validated execution, result back, final answer.
- That the model requests and your runtime decides, capability lives entirely on your side.
- Why tool descriptions are prompt engineering and argument validation is security engineering.
- How errors-as-results enable self-correction.

---

## Part 9: Practical Exercise

Build a two-tool script: `check_url(url)` (HTTP status and latency for an allowlisted set of hosts) and `read_file(path)` (contents of files under a fixed directory only). Ask "is my service healthy and does its config look right?" and watch the model choose tools, sequence them, and combine results. Then break it: pass a URL outside the allowlist and a path with `../`, and confirm your validation blocks both and the model handles the error result gracefully.

---

## Part 10: Suggested Project

[Project 2: Tool-calling agent](../projects/README.md), a small assistant with three or four read-only DevOps tools (pod status, service health, log tail, disk usage). Keep it to single-question interactions for now; the looping version is Project 4, after topic 05.
