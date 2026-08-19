"""Curriculum definition and settings for the learning agent."""

from pathlib import Path

MODEL = "claude-sonnet-4-5"
MAX_TOKENS = 1500

AGENT_DIR = Path(__file__).resolve().parent
NOTES_DIR = AGENT_DIR.parent / "notes"
STATE_FILE = AGENT_DIR / "state.json"
SYSTEM_PROMPT_FILE = AGENT_DIR / "prompts" / "system.md"

# Ordered curriculum: position defines prerequisites (each topic assumes all before it).
CURRICULUM = [
    ("llm-fundamentals", "01-llm-fundamentals.md", "LLM Fundamentals"),
    ("prompt-engineering", "02-prompt-engineering.md", "Prompt Engineering"),
    ("structured-output", "03-structured-output.md", "Structured Output"),
    ("tool-use", "04-tool-use.md", "Tool Use"),
    ("agent-loops", "05-agent-loops.md", "Agent Loops"),
    ("memory-and-persistence", "06-memory-and-persistence.md", "Memory & Persistence"),
    ("rag", "07-rag.md", "RAG"),
    ("mcp", "08-mcp.md", "MCP"),
    ("subagents", "09-subagents.md", "Subagents"),
    ("hooks-and-automation", "10-hooks-and-automation.md", "Hooks & Automation"),
    ("agentic-cicd", "11-agentic-cicd.md", "Agentic CI/CD"),
    ("multi-agent-workflows", "12-multi-agent-workflows.md", "Multi-Agent Workflows"),
    ("cost-and-performance", "13-cost-and-performance.md", "Cost & Performance"),
    ("evaluation-and-guardrails", "14-evaluation-and-guardrails.md", "Evaluation & Guardrails"),
]

TOPIC_SLUGS = [slug for slug, _, _ in CURRICULUM]

QUIZ_QUESTIONS = 4
PASS_THRESHOLD = 0.75   # quiz score needed to mark a topic completed
WEAK_THRESHOLD = 0.5    # below this, the topic is flagged for review

DEFAULT_STATE = {
    "current_topic": None,
    "completed_topics": [],
    "confidence": {},      # slug -> "high" | "medium" | "low"
    "quiz_results": [],    # {topic, score, date}
    "weak_topics": [],
}
