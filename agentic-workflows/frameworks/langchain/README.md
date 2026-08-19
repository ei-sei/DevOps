# LangChain

> Frameworks are learned AFTER understanding the underlying concepts. Do not start here - work through [notes 01-07](../../notes/README.md) first, and build the no-framework agent ([Project 4](../../projects/README.md)) before touching this.

## What problem does this framework solve?

LangChain provides pre-built components for the LLM application patterns you'd otherwise hand-roll repeatedly: talking to any provider through one interface, composing prompt → model → parser pipelines, defining tools, running agents, and wiring up RAG. Its real value is breadth of **integrations** - hundreds of maintained connectors for models, vector stores, document loaders, and APIs - so swapping Anthropic for another provider, or one vector store for another, is a one-line change instead of a rewrite.

## What did I need to understand before using it?

- LLM APIs, messages, tokens ([01](../../notes/01-llm-fundamentals.md))
- Prompting and prompt templates ([02](../../notes/02-prompt-engineering.md))
- Structured output and Pydantic ([03](../../notes/03-structured-output.md)) - LangChain's `with_structured_output` is exactly the topic 03 pattern
- Tool calling ([04](../../notes/04-tool-use.md)) - its `@tool` decorator generates the schema you wrote by hand
- Agent loops ([05](../../notes/05-agent-loops.md)) - its agent executors run the loop you built yourself
- RAG ([07](../../notes/07-rag.md)) - its retrievers/loaders/splitters are the pipeline you built with numpy

Without these, LangChain is a wall of opaque abstractions. With them, every LangChain class maps to code you have already written.

## What would implementing this manually look like?

You already did - that's the point of the curriculum order:

| LangChain concept | Manual version you built |
|---|---|
| **Chains** (prompt \| model \| parser, composed with LCEL) | A prompt template string, an API call, a Pydantic parse - topic 03's `analyse()` function |
| **Tools** (`@tool` decorated functions) | Hand-written JSON Schema tool definitions plus a dispatch dict - topic 04 |
| **Agents** (agent executor) | The ~40-line loop with stopping conditions - topic 05 |
| **Retrievers** (loaders, splitters, vector stores) | Chunk on headings, embed, cosine top-k - topic 07 |
| **Integrations** | The one part with no manual equivalent - this is what you're actually buying |

## What abstraction does the framework provide?

- **Chains / LCEL**: composition of steps (`prompt | model | parser`) with batching, streaming, and async handled for you.
- **Tools**: schema generation from Python type hints and docstrings, instead of hand-written JSON Schema.
- **Agents**: a maintained agent loop with tool routing (note: LangChain now delegates serious agent work to LangGraph - see [langgraph/](../langgraph/README.md)).
- **Retrievers**: a uniform interface over document loading, splitting, embedding, and vector search.
- **Integrations**: the provider/store/loader ecosystem - the strongest reason to reach for it.

The trade-off: abstraction hides the loop, and when behaviour is wrong you debug through framework layers instead of your own 40 lines. Reach for LangChain when integration breadth or team standardisation pays for that; skip it when your manual version is small and clear.

## Learning checklist

- [ ] Rebuild topic 03's structured-output analyser as a chain with `with_structured_output`
- [ ] Rebuild topic 04's tools with `@tool`; compare the generated schema with your hand-written one
- [ ] Rebuild the topic 07 RAG pipeline with loaders/splitters/a vector store
- [ ] [Project 5](../../projects/README.md): port Project 2's tool-calling agent, then diff behaviour, cost, and debuggability against your manual version - written up honestly
