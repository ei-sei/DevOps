# Project 1 - Direct LLM API Application

Exercises [notes 01-02](../../notes/README.md): raw API calls with no framework, making the fundamentals visible - messages, system prompts, temperature, token usage, and streaming.

## What it does

`explain.py` is a small CLI that asks a model to explain a DevOps concept, and prints the token usage and cost estimate after every call - the habit topic 13 later builds on.

```bash
# one-shot explanation, streamed to the terminal
python explain.py "kubernetes statefulsets"

# compare temperature 0 vs 1 on the same prompt (run each twice - see note 01, Part 9)
python explain.py --compare-temperature "docker layer caching"
```

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then add your API key
```

Requires `ANTHROPIC_API_KEY` in the environment or `.env`. The script exits with a clear error if it's missing - it never sends a request without it.

## What to notice

- The full request is just messages + parameters - run with `--debug` to print the exact payload.
- Token usage is reported on every response; input and output are priced differently.
- At `temperature 0` repeated runs are near-identical; at `1` they visibly differ.
- Streaming changes perceived latency, not cost - the usage numbers are the same.
