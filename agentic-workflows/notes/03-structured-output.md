# 03. Structured Output

---

## Part 1: What It Is

What is structured output?
> Structured output means getting the model to respond in a machine-readable format, almost always JSON conforming to a schema you define, instead of free-form prose. `{"cause": "missing dependency", "confidence": "high"}` rather than "Well, it looks like the problem might be...".

---

## Part 2: Why It Matters

Why is structured output the bridge between "chatting with a model" and "building with a model"?
> Because code cannot branch on prose. The moment a model's output feeds into another program (an if-statement, a database insert, a tool call) it must be parseable and predictable. Every agent framework, tool-calling API, and pipeline integration is built on the model reliably emitting structured data. Without this, an LLM is a text toy; with it, it's a component.

---

## Part 3: Core Concepts

What is a schema, in this context?
> A schema is a formal definition of the expected output shape: which fields exist, their types, which are required, and allowed values. JSON Schema is the standard format, and most LLM APIs now accept a schema directly and constrain generation to match it (variously called structured outputs, JSON mode, or response format).

What is validation and why is it still needed?
> Validation is programmatically checking that the output actually conforms to the schema before using it. Even with API-level structured output support, validate anyway: models can emit values that are type-valid but semantically wrong (a confidence of "banana", an empty required list), and older models or plain-prompt approaches can produce malformed JSON outright. Trust but verify, at a system boundary, and model output is always a system boundary.

What is Pydantic and why does it come up constantly?
> Pydantic is the standard Python library for defining data models with types and validation. You define a class, and Pydantic gives you parsing, validation, clear errors, and JSON Schema generation from that single definition. Most Python LLM tooling (including LangChain later) uses Pydantic models as the way to declare expected output.

What are typed responses?
> The pattern of parsing model output directly into a typed object (a Pydantic model, a dataclass) rather than working with raw dicts. Your downstream code then gets autocomplete, type checking, and guaranteed field presence, and a malformed response fails loudly at the parse step instead of as a `KeyError` three functions later.

How do you handle malformed output?
> Layered defence: (1) use the API's native structured output support where available, (2) validate with Pydantic, (3) on validation failure, retry, ideally feeding the validation error back to the model ("your previous response failed validation: field `confidence` must be one of high/medium/low, respond again"), (4) after N failures, fail explicitly rather than limping on with garbage. This retry-with-error-feedback pattern is one of the most useful tricks in practical LLM engineering.

---

## Part 4: Simple Explanation

> Free-form model output is like a service that returns its response as an English paragraph: fine for a human, useless for the next service in the chain. Structured output is giving that service an API contract. The schema is the contract, validation is the contract test, and the retry-on-invalid loop is your error handling. Same discipline as any inter-service API, applied to a component that occasionally forgets the contract exists.

---

## Part 5: Practical Example

```python
from pydantic import BaseModel, ValidationError
from typing import Literal

class FailureAnalysis(BaseModel):
    cause: str
    fix: str
    confidence: Literal["high", "medium", "low"]

def analyse(log: str, max_retries: int = 2) -> FailureAnalysis:
    prompt = (
        "Analyse this CI failure log. Respond with ONLY a JSON object "
        'matching: {"cause": str, "fix": str, "confidence": "high"|"medium"|"low"}\n'
        f"<log>\n{log}\n</log>"
    )
    for attempt in range(max_retries + 1):
        raw = call_llm(prompt)  # returns the model's text response
        try:
            return FailureAnalysis.model_validate_json(raw)
        except ValidationError as e:
            prompt += f"\n\nYour previous response was invalid: {e}. Respond again with only valid JSON."
    raise RuntimeError("Model failed to produce valid output after retries")

analysis = analyse(open("ci-failure.log").read())
if analysis.confidence == "high":
    print(f"Cause: {analysis.cause}\nSuggested fix: {analysis.fix}")
```

The key beats: schema as a Pydantic class, validation at the boundary, the error fed back on retry, and an explicit failure after retries are exhausted.

---

## Part 6: How It Relates to Agents

> Tool calling (next topic) *is* structured output: the model emits a JSON object naming a tool and its arguments, and the runtime parses and validates it before execution. An agent's decisions ("which tool next", "am I done") are structured outputs too. If a model can't reliably produce valid JSON for you, it can't reliably drive an agent, which is exactly why this topic precedes tool use.

---

## Part 7: Common Mistakes

- Parsing model output with regex or string-splitting instead of a schema and validator.
- Skipping validation because "the API guarantees valid JSON", valid JSON is not the same as correct values.
- Retrying without feeding the validation error back, so the model repeats the same mistake.
- Schemas with vague free-text fields where an enum (`Literal`) would force a decidable answer.
- Letting a failed parse pass silently (empty dict, None) instead of failing loudly, garbage propagates.
- Asking for JSON *and* explanation in one response; keep the machine channel clean, put reasoning in a dedicated field if you want it.

---

## Part 8: Things I Should Know Before Moving On

- How to define a schema with Pydantic and validate model output against it.
- The retry-with-error-feedback pattern.
- Why enums/Literals beat free text for decision fields.
- That tool calling is structured output with a runtime attached, which is the next topic.

---

## Part 9: Practical Exercise

Extend the log explainer from topic 02: define a Pydantic `FailureAnalysis` model, make the script output validated JSON, and add the retry loop. Then test the unhappy path: temporarily corrupt the prompt so the model returns prose, and confirm your code retries and then fails cleanly rather than crashing or passing garbage through.

---

## Part 10: Suggested Project

This completes the groundwork for [Project 2: Tool-calling agent](../projects/README.md), a tool call is just a structured output the runtime acts on, which is exactly where the next note picks up.
