# 08. MCP

---

## Part 1: What It Is

What is the Model Context Protocol?
> MCP is an open protocol (introduced by Anthropic, since adopted broadly) that standardises how AI applications connect to external tools and data sources. An **MCP server** wraps some capability (GitHub, Postgres, a filesystem, your internal API) and exposes it in a standard format; any **MCP client** (Claude Code, an IDE, your own agent) can then connect and use it, no bespoke integration per pairing.

Why does MCP exist?
> Before MCP, connecting M agents to N tools meant M×N custom integrations, everyone wiring their own GitHub tools, their own database tools, incompatibly. MCP collapses that to M+N: build one GitHub MCP server, and every MCP-capable client can use it. It's the USB analogy that appears in every MCP explanation because it's accurate: one standard connector instead of a bag of proprietary cables. To a DevOps eye, it's what OCI did for container images or CRI for runtimes (see the [kubernetes notes](../../kubernetes/notes/01-basics-and-architecture.md)): an interface standard that decouples producers from consumers.

---

## Part 2: Why It Matters

Why learn MCP right after tool calling rather than instead of it?
> Because MCP *is* tool calling with a distribution mechanism, and only makes sense in that order. Topic 04 taught the mechanics: definitions, schemas, requests, results. MCP standardises how those definitions are discovered and where execution happens, so a tool can be packaged once and reused everywhere. If you skipped topic 04, MCP would look like magic; having done it, MCP looks like exactly what it is, a sensible protocol around a mechanic you already understand.

---

## Part 3: Core Concepts

What is an MCP server?
> A program exposing capabilities over the protocol, typically running locally as a subprocess (spoken to over stdio) or remotely over HTTP. It advertises what it offers; the client discovers this at connection time rather than having tools hard-coded.

What is an MCP client?
> The AI-application side: it connects to configured servers, lists their offerings, presents the discovered tools to the model alongside any built-in ones, and routes the model's tool calls to the right server. From the model's perspective, an MCP tool is indistinguishable from a native one.

What are the three things a server can expose?
> **Tools**: functions the model can invoke (query the database, create an issue), exactly the topic 04 concept, executed server-side. **Resources**: readable data identified by URI (a file, a schema, a dashboard) that the client can load into context, data to *read* rather than actions to *take*. **Prompts**: reusable parameterised prompt templates the server ships (a "review this PR" template from a GitHub server), encapsulating domain prompting expertise alongside the tools.

How does MCP differ from ordinary function calling?
> Mechanically it rides on the same model-level feature, the model still emits structured tool-use requests. The differences are architectural: **discovery** (capabilities are found at runtime, not hard-coded), **decoupling** (the tool implementation lives in a separate process, maintained independently, reusable across clients), and **standardisation** (any client speaks to any server). Plain function calling is defining functions inside your app; MCP is depending on packages.

What are the security considerations?
> An MCP server is code you run with real credentials attached, so: **trust** (a third-party server sees every tool call and its data, vet servers like any dependency, supply-chain rules apply), **least privilege** (give servers scoped credentials, the read-only database user, the repo-scoped token, not admin), **injection surface** (tool results from a server enter the model's context, a compromised or malicious server can steer your agent, topic 02's injection warning applies), and **approval gates** (clients like Claude Code prompt before tool execution, keep that for anything that mutates). Treat adding an MCP server with the seriousness of adding a CI plugin with production access, because that's what it is.

---

## Part 4: Simple Explanation

> Without MCP, giving your agent database access means writing query functions, schemas, and connection handling inside your app, and the next team writes their own incompatible version. With MCP, someone publishes a database server once; you add one config entry, your client connects, discovers `query`, `list_tables`, and a schema resource, and your model can use them immediately. Capability becomes something you *install* rather than *implement*, with the same benefits and the same supply-chain caution as any package manager.

---

## Part 5: Practical Example

Configuring servers in a client (here, Claude Code's `.mcp.json`):

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_TOKEN": "${GITHUB_TOKEN}" }
    },
    "postgres-readonly": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres",
               "postgresql://readonly_user@localhost/mydb"]
    }
  }
}
```

And the skeleton of a minimal server of your own, in Python:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("devops-notes")

@mcp.tool()
def search_notes(query: str) -> str:
    """Search the DevOps learning notes for a topic."""
    return rag_search(query)          # the retrieval pipeline from topic 07

@mcp.resource("notes://{topic}/toc")
def topic_toc(topic: str) -> str:
    """Table of contents for one topic folder's notes."""
    return (Path(topic) / "notes" / "README.md").read_text()

if __name__ == "__main__":
    mcp.run()                          # serves over stdio
```

Note the two config details that carry the security story: the token comes from the environment, never the file, and the Postgres URL bakes in a read-only user, least privilege in the connection string itself.

---

## Part 6: How It Relates to Agents

> MCP changes where an agent's tools *come from*, not how the loop works: the topic 05 loop is unchanged, but the tool list is now assembled at startup from connected servers. This makes agents composable, the same troubleshooting agent gains GitHub, Kubernetes, and database capabilities via config rather than code, and it's how ecosystem tooling (Claude Code and its peers) get their extensibility. It also previews topic 09's theme: capability living outside the agent process, coordinated over a protocol.

---

## Part 7: Common Mistakes

- Learning MCP before plain tool calling, then being unable to reason about what the model actually sees and emits.
- Running third-party servers with broad credentials because scoping felt like effort, the read-only user and the narrow token are the whole game.
- Not vetting community servers before pointing them at real systems.
- Writing an MCP server for tools only one private app will ever use, plain functions are less machinery; MCP pays off at the point of *reuse*.
- Connecting many servers and flooding the model with dozens of discovered tools, tool selection quality degrades; connect what the task needs.
- Forgetting that server responses are untrusted context input, injection defence doesn't stop at your own code.

---

## Part 8: Things I Should Know Before Moving On

- The M×N → M+N argument and the client/server split.
- Tools vs resources vs prompts, and what discovery means at connection time.
- The precise relationship to topic 04: same model mechanic, different packaging.
- The four security considerations, especially least-privilege credentials per server.

---

## Part 9: Practical Exercise

Add one well-known MCP server (filesystem or GitHub) to an MCP client you use, with deliberately scoped access (one directory; one repo's token). Use it, then inspect what was discovered: list the tools and read their schemas, connecting the config entry to the topic 04 concepts underneath. Then sketch, on paper, the tools and resources a server for *this repository* would expose, that design becomes the exercise below.

---

## Part 10: Suggested Project

Build the "devops-notes" MCP server from Part 5 for real: `search_notes` backed by your Project 3 RAG pipeline, plus a resource per topic folder's TOC. Register it in Claude Code and ask questions that make it consult your own notes. This is also the repo's future-roadmap item, and a good first taste of capability-as-a-package.
