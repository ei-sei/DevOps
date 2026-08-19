# 07. RAG

---

## Part 1: What It Is

What is retrieval-augmented generation?
> RAG is the pattern of fetching relevant documents from your own data at query time and injecting them into the prompt, so the model answers from *your* content rather than only its training data. Ask "what's our rollback procedure?", the system retrieves the relevant runbook section, pastes it into the context, and the model answers grounded in that text.

What problem does it solve that prompting alone can't?
> The model has never seen your internal docs, and your corpus is far too large to paste wholesale into a context window. RAG is the middle path: keep the corpus outside the model, retrieve only the few relevant chunks per question.

---

## Part 2: Why It Matters

Why is RAG usually the answer to "can the AI know about our stuff"?
> Because the alternatives are worse: fine-tuning a model on your docs is expensive, slow to update, and bad at recalling specifics, while pasting everything into every prompt is impossible past trivial corpus sizes. RAG updates as easily as re-indexing a changed file, cites its sources, and dramatically reduces hallucination on covered topics, because the model paraphrases retrieved text instead of generating from statistical memory.

---

## Part 3: Core Concepts

What is chunking?
> Splitting documents into retrieval-sized pieces, typically a few hundred tokens each. Chunks must be small enough that several fit in a prompt, but large enough to stay self-contained: a chunk that starts mid-sentence with "then restart the service" is useless without knowing *which* service. Splitting on natural structure (markdown headings, paragraphs) beats fixed character counts, and overlapping adjacent chunks slightly hedges against ideas straddling a boundary.

What are embeddings, now in practice?
> As introduced in [topic 01](01-llm-fundamentals.md): a vector representing a text's meaning, where similar meanings produce nearby vectors. RAG uses them for search that survives vocabulary mismatch: "how do I undo a deploy" matches a chunk titled "rollback procedure" because the *vectors* are close, even though the words share nothing. Keyword search can't do that.

What is a vector store?
> A database optimised for "find the N stored vectors nearest to this query vector." Options span from a numpy array in memory (fine for hundreds of chunks, and what the Part 5 example uses), through embedded libraries like ChromaDB or FAISS, to Postgres with pgvector, up to managed services. Same escalation discipline as topic 06: start small, upgrade on need.

How does similarity search and retrieval work end to end?
> **Index time** (once, or on doc changes): chunk every document, embed every chunk, store vectors alongside their text. **Query time**: embed the question, find the top-k nearest chunks (cosine similarity, typically k of 3-5), and hand their text to the prompt stage.

What is context injection?
> Assembling the final prompt: retrieved chunks, clearly delimited and labelled with their sources, plus the question, plus the crucial instruction "answer using the provided context; if it doesn't contain the answer, say so." Without that escape hatch, the model blends retrieval with training-data guesswork and you lose the hallucination-reduction benefit that justified RAG in the first place.

What are RAG's limitations?
> Retrieval quality caps answer quality, if the right chunk isn't in the top-k, the model can't use it. It struggles with questions needing synthesis *across* many documents ("summarise every incident this year" retrieves five chunks, not fifty files). Stale indexes serve stale answers, re-indexing is part of the system, not an afterthought. Retrieved content is untrusted input, a poisoned document is a prompt-injection vector (topic 02's warning applies). And it adds real moving parts: embedding model, store, chunking pipeline, all of which can independently degrade.

---

## Part 4: Simple Explanation

> RAG is an open-book exam instead of a closed-book one. Without RAG, the model answers from whatever it absorbed during training, fluent, but prone to misremembering specifics. With RAG, someone first finds the three most relevant pages from *your* manual and slides them across the desk. The model still writes the answer, but now it's paraphrasing your actual documentation. The librarian doing the finding is embeddings plus similarity search.

---

## Part 5: Practical Example

Minimal RAG over this repo's notes, no framework, no vector database:

```python
import numpy as np
from pathlib import Path
import anthropic

client = anthropic.Anthropic()

# 1. Chunk: split notes on "## " headings
chunks = []
for f in Path("../../").glob("*/notes/*.md"):
    for section in f.read_text().split("\n## "):
        if len(section.strip()) > 100:
            chunks.append({"source": f.name, "text": section[:2000]})

# 2. Embed (any embedding API works; returns one vector per text)
def embed(texts: list[str]) -> np.ndarray: ...

index = embed([c["text"] for c in chunks])          # index time

# 3. Retrieve: cosine similarity, top 3
def retrieve(question: str, k: int = 3) -> list[dict]:
    q = embed([question])[0]
    sims = index @ q / (np.linalg.norm(index, axis=1) * np.linalg.norm(q))
    return [chunks[i] for i in np.argsort(sims)[-k:][::-1]]

# 4. Inject and generate
def ask(question: str) -> str:
    context = "\n\n".join(
        f"<doc source='{c['source']}'>\n{c['text']}\n</doc>" for c in retrieve(question)
    )
    r = client.messages.create(
        model="claude-sonnet-4-5", max_tokens=1024,
        system="Answer ONLY from the provided documents, citing sources. "
               "If they do not contain the answer, say exactly that.",
        messages=[{"role": "user", "content": f"{context}\n\nQuestion: {question}"}],
    )
    return r.content[0].text

print(ask("What is a StatefulSet used for?"))
```

The whole pipeline is visible: chunk on structure, embed once, cosine top-k at query time, delimited injection with sources, and the "say so if it's not there" instruction. Every RAG framework is this with better engineering.

---

## Part 6: How It Relates to Agents

> For an agent, retrieval becomes a *tool*: `search_docs(query)` alongside its other tools, letting the agent decide when to consult the knowledge base, reformulate queries, and search iteratively ("first search for the error, then for the component it names"). Agentic RAG, where the loop drives retrieval rather than a fixed pipeline, is strictly more capable than one-shot retrieve-then-answer. RAG is also the "selective retrieval" memory technique from topic 06 applied to documents, and MCP resources (next topic) give a standard way to expose such corpora to any agent.

---

## Part 7: Common Mistakes

- Chunking by fixed character count through the middle of sentences and tables, retrieval precision dies at the chunking step more often than anywhere else.
- Skipping the "answer only from context / say if absent" instruction, silently reverting to hallucination-prone closed-book answers.
- Never evaluating retrieval separately: when answers are bad, first check *what was retrieved*, the bug is usually there, not in generation.
- Setting k too high, drowning the model in marginal chunks (and paying for the tokens).
- No re-index story: the corpus changes, the index doesn't, answers go quietly stale.
- Starting with a managed vector database and a framework for a 200-chunk corpus.

---

## Part 8: Things I Should Know Before Moving On

- The two-phase shape: index (chunk, embed, store) and query (embed, retrieve, inject, generate).
- Why semantic search beats keyword search here, and what cosine top-k means.
- The limitations list, especially "retrieval quality caps everything" and cross-document synthesis.
- How RAG becomes a tool inside an agent loop.

---

## Part 9: Practical Exercise

Build the Part 5 pipeline over this repo's `notes/` folders. Then probe its edges: ask something answered in exactly one note (should work), something requiring synthesis across many notes (watch it struggle), and something the notes don't cover (confirm it says so instead of inventing). For any bad answer, print the retrieved chunks first and determine whether retrieval or generation failed, that diagnostic habit is the main skill of this topic.

---

## Part 10: Suggested Project

[Project 3: RAG application](../projects/README.md), "ask my DevOps notes": the Part 5 pipeline with a small CLI, source citations in answers, and a re-index command that only re-embeds changed files. Later it plugs into Project 7 as the troubleshooting agent's knowledge-base tool.
