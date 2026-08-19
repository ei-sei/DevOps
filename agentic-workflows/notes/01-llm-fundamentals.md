# 01. LLM Fundamentals

---

## Part 1: What It Is

What is a large language model, in one sentence?
> A large language model (LLM) is a neural network trained on huge amounts of text that predicts the next token in a sequence, and generates text by doing that prediction repeatedly.

What is inference?
> Inference is the act of running a trained model to produce output, as opposed to training, which is the (much more expensive) process of learning the model's weights in the first place. When you call an LLM API, you are doing inference against a model someone else already trained.

What is a token?
> A token is the model's unit of text, roughly three-quarters of a word on average in English. "Kubernetes" might be one or two tokens, "unbelievably" might split into three. Tokens, not characters or words, are what you pay for and what count against context limits.

What is a context window?
> The context window is the maximum number of tokens (input plus output combined) a model can process in a single request. Everything the model "knows" about the current conversation, including system prompt, prior messages, and any documents you've pasted in, has to fit inside it.

---

## Part 2: Why It Matters

Why does an infrastructure engineer need to understand tokens and context windows specifically?
> Because they are the two things that directly limit and cost you: a context window is a hard capacity limit (like memory on a box), and tokens are the billing unit (like compute-seconds). An agent that reads a 50,000-line log file and pastes all of it into a prompt will either blow the context window or blow the budget, often both. Every later topic (RAG, memory, multi-agent) exists partly to work around this one constraint.

---

## Part 3: Core Concepts

What are system and user messages?
> Most chat-style LLM APIs structure input as a list of messages, each with a role. The **system** message sets persistent instructions and framing for the whole conversation ("you are a Kubernetes troubleshooting assistant"); **user** messages are the actual queries; **assistant** messages are the model's prior replies, included so the model has conversational memory. There is no magic memory between calls, the full message list is resent every single time (see [06-memory-and-persistence.md](06-memory-and-persistence.md)).

What is temperature?
> Temperature controls how deterministic the model's token choices are. Low temperature (near 0) makes the model consistently pick its highest-probability next token, good for factual or structured tasks. High temperature makes it sample more randomly among plausible tokens, good for creative or varied output. For agents and tool use, you almost always want low temperature: predictability beats creativity when the output has to be parsed by code.

What does model selection actually trade off?
> Bigger/newer models are more capable and more expensive per token, and often slower. Smaller/cheaper models are faster and cheaper but make more reasoning mistakes. In production this is a real engineering decision, not just "always use the best model": a log-classification step that runs on every CI failure might use a cheap fast model, while a step that proposes a production fix might justify a stronger, slower one. See [13-cost-and-performance.md](13-cost-and-performance.md).

What is streaming?
> Streaming returns the model's output token-by-token as it's generated, instead of waiting for the full response. It doesn't reduce total latency or cost, but it drastically improves *perceived* latency for a human watching output appear, the same reason `docker build` shows layer-by-layer progress instead of going silent for two minutes.

What are embeddings, at a conceptual level?
> An embedding is a vector (a list of numbers) that represents the meaning of a piece of text, produced by a separate, much smaller model than the LLM itself. Texts with similar meaning end up with vectors that are numerically close together. This is what makes semantic search possible: compare vectors, not keywords. Embeddings are covered in depth in [07-rag.md](07-rag.md); for now, just know they exist and are a different kind of model call than chat completion.

What is an API, in this context?
> An LLM API is an HTTP endpoint you send a JSON request to (model name, messages, parameters) and get a JSON response back (generated text, token usage, stop reason). This is the entire interface. There is no SDK magic underneath it that isn't just a wrapper around this HTTP call, which is worth knowing because it means you can always fall back to `curl` to debug what's actually happening on the wire.

What is a hallucination?
> A hallucination is the model producing fluent, confident output that is factually wrong: an AWS CLI flag that doesn't exist, a plausible-looking but fake URL, a misremembered API signature. It happens because the model is generating statistically plausible text, not retrieving facts, and "plausible" and "true" often overlap but are not the same thing. Hallucinations are not a bug that will be patched out; they are inherent to how generation works, and everything from RAG to guardrails exists partly to contain them.

What are the practical limitations of LLMs to keep in mind?
> A knowledge cutoff (the model knows nothing after its training data ends), no access to your systems unless you explicitly give it tools, nondeterminism (even at low temperature across model versions), inability to reliably do precise arithmetic or count characters, degraded attention over very long contexts, and confident wrongness (hallucination). Treat an LLM like a very well-read colleague with no internet access and no accountability: enormously useful, never blindly trusted.

---

## Part 4: Simple Explanation

If you strip away all the terminology, what is actually happening when you "use an LLM"?
> You send a block of text (the prompt, built from your messages). The model reads it and, one token at a time, predicts the single most statistically plausible next token given everything so far, appends it, and repeats until it decides to stop or hits a length limit. There is no database lookup, no "thinking" step separate from this, and no persistent memory of you between API calls. Every apparent capability (reasoning, tool use, memory) is built on top of this one repeated operation, either by the model itself during generation or by the surrounding application code.

---

## Part 5: Practical Example

A minimal request/response, shown as `curl` so the HTTP reality is visible before any SDK hides it:

```bash
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-sonnet-4-5",
    "max_tokens": 200,
    "temperature": 0,
    "system": "You are a terse Kubernetes troubleshooting assistant.",
    "messages": [
      {"role": "user", "content": "A pod is stuck in CrashLoopBackOff. First thing to check?"}
    ]
  }'
```

The response includes the generated text, a `stop_reason` (did it finish naturally, hit `max_tokens`, or stop for a tool call), and `usage` (input/output token counts), the three things you'll inspect constantly once you're building agents.

---

## Part 6: How It Relates to Agents

> An agent is not a different kind of model, it's the same request/response mechanic wrapped in a loop with tools and state. Everything in this note (tokens, context windows, message roles, temperature) applies unchanged to every single call an agent makes. If you don't understand a plain chat call, you cannot debug why an agent is behaving strangely, because there is no additional layer of magic to blame, it's still just messages in, tokens out.

---

## Part 7: Common Mistakes

- Assuming the model "remembers" previous conversations by default. It doesn't, the client resends the whole message history every time.
- Treating the context window as effectively unlimited and dumping raw files/logs into prompts without thinking about token count.
- Using high temperature for anything that needs to be parsed programmatically (structured output, tool arguments).
- Confusing token count with word or character count when estimating cost or context usage.
- Assuming a bigger/newer model is always the right choice, ignoring the cost and latency trade-off.

---

## Part 8: Things I Should Know Before Moving On

- What a token, context window, and system/user/assistant message are.
- Why low temperature matters for anything agentic.
- That embeddings are a separate kind of model call from chat, covered properly in topic 07.
- That "the API" is just HTTP + JSON, nothing more mysterious underneath.

---

## Part 9: Practical Exercise

Pick any LLM provider you have API access to (or a free-tier one). Send the same prompt twice with `temperature: 0` and confirm the output is identical or near-identical both times. Then send it twice more with `temperature: 1` and confirm the outputs differ. Note the `usage` token counts in each response and manually verify roughly how many tokens your input text was (as a rule of thumb, divide word count by 0.75).

---

## Part 10: Suggested Project

See [Project 1: Direct LLM API application](../projects/01-direct-llm-api/) for a small script that exercises everything in this note: a raw API call, inspecting token usage, and comparing temperature settings.
