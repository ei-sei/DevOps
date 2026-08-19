# Learning Agent

A small personal AI tutor for this folder's [curriculum](../notes/README.md). It is not a chatbot: it tracks progress across sessions, checks prerequisites before teaching, asks questions before giving answers, gives hints before solutions, and only marks a topic completed when you pass its quiz.

It is deliberately **framework-free**: its own implementation demonstrates the concepts of notes 01-06 (direct API calls, a tutor system prompt, JSON-validated quiz grading with retry, a simple conversation loop, JSON-file persistence). Migrating it to LangGraph is a planned future milestone - after those notes are understood, not before.

## Setup

```bash
cd agentic-workflows/learning-agent
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env    # add your ANTHROPIC_API_KEY
```

No key is needed for `progress` and `next`. Commands that talk to the model exit with a clear message if the key is missing.

## Usage

```bash
python agent.py learn llm-fundamentals   # interactive tutoring session
python agent.py quiz llm-fundamentals    # 4 questions; >= 3 correct marks it completed
python agent.py review                   # short quiz on your weakest topic
python agent.py exercise                 # practical exercise for your current topic
python agent.py progress                 # curriculum status (offline)
python agent.py next                     # what to do next (offline)
```

Topic names are the note slugs: `llm-fundamentals`, `prompt-engineering`, `structured-output`, `tool-use`, `agent-loops`, `memory-and-persistence`, `rag`, `mcp`, `subagents`, `hooks-and-automation`, `agentic-cicd`, `multi-agent-workflows`, `cost-and-performance`, `evaluation-and-guardrails`.

## How it behaves

- `learn` on a topic whose prerequisites you haven't passed suggests quizzing those first (override with `--force`).
- During a quiz, a wrong answer gets a hint and a second attempt; only first-attempt answers count toward the score.
- Failing a quiz flags the topic as weak; `review` targets weak topics first.
- The tutor reads the actual notes file for the topic, so its teaching stays consistent with this repo.

## State

Progress lives in `state.json` (gitignored, local only):

```json
{
  "current_topic": "tool-use",
  "completed_topics": ["llm-fundamentals", "prompt-engineering", "structured-output"],
  "confidence": {"llm-fundamentals": "high", "structured-output": "medium"},
  "quiz_results": [{"topic": "structured-output", "score": 0.75, "date": "2026-08-19"}],
  "weak_topics": []
}
```

Delete the file to start over.

## Limitations

This is a learning tool, not a product: single user, no tests, no evaluation of the tutor itself, quiz grading is LLM judgement (note 14 explains why that needs calibration in anything serious). Keeping it simple is the point.
