"""Personal AI tutor CLI for the agentic-workflows curriculum.

Deliberately framework-free: this agent demonstrates the concepts it teaches
(direct API calls, prompting, structured output, a simple loop, JSON persistence).
"""

import argparse
import json
import os
import sys
from datetime import date

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

import config


# ---------------------------------------------------------------- state

def load_state() -> dict:
    if config.STATE_FILE.exists():
        state = json.loads(config.STATE_FILE.read_text())
        return {**config.DEFAULT_STATE, **state}
    return json.loads(json.dumps(config.DEFAULT_STATE))


def save_state(state: dict) -> None:
    config.STATE_FILE.write_text(json.dumps(state, indent=2) + "\n")


# ---------------------------------------------------------------- curriculum

def find_topic(slug: str) -> tuple[str, str, str]:
    for entry in config.CURRICULUM:
        if entry[0] == slug:
            return entry
    sys.exit(f"Unknown topic {slug!r}. Valid topics:\n  " + "\n  ".join(config.TOPIC_SLUGS))


def unmet_prerequisites(slug: str, state: dict) -> list[str]:
    index = config.TOPIC_SLUGS.index(slug)
    return [s for s in config.TOPIC_SLUGS[:index] if s not in state["completed_topics"]]


def load_notes(filename: str) -> str:
    path = config.NOTES_DIR / filename
    if not path.exists():
        return "(no notes file found for this topic)"
    return path.read_text()[:12000]


# ---------------------------------------------------------------- LLM

def get_client():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit(
            "Error: ANTHROPIC_API_KEY is not set, and this command needs the model.\n"
            "Copy .env.example to .env and add your key, or export it:\n"
            "  export ANTHROPIC_API_KEY=sk-ant-...\n"
            "(Commands 'progress' and 'next' work without a key.)"
        )
    import anthropic

    return anthropic.Anthropic()


def build_system(topic_title: str, notes: str, state: dict) -> str:
    base = config.SYSTEM_PROMPT_FILE.read_text()
    recent = state["quiz_results"][-5:]
    progress = (
        f"Topic of this session: {topic_title}\n"
        f"Completed topics: {', '.join(state['completed_topics']) or 'none yet'}\n"
        f"Weak topics: {', '.join(state['weak_topics']) or 'none'}\n"
        f"Recent quiz results: {json.dumps(recent) if recent else 'none'}"
    )
    return f"{base}\n\n## Student progress\n\n{progress}\n\n## Repository notes for this topic\n\n<notes>\n{notes}\n</notes>"


def chat(client, system: str, messages: list) -> str:
    response = client.messages.create(
        model=config.MODEL, max_tokens=config.MAX_TOKENS, system=system, messages=messages,
    )
    return response.content[0].text


def chat_json(client, system: str, messages: list, required_keys: set, retries: int = 2) -> dict:
    """Get a JSON response, retrying with the error fed back (see note 03)."""
    attempt_messages = list(messages)
    for _ in range(retries + 1):
        raw = chat(client, system, attempt_messages)
        try:
            start, end = raw.index("{"), raw.rindex("}") + 1
            data = json.loads(raw[start:end])
            if required_keys <= set(data):
                return data
            error = f"missing keys: {required_keys - set(data)}"
        except (ValueError, json.JSONDecodeError) as e:
            error = str(e)
        attempt_messages = attempt_messages + [
            {"role": "assistant", "content": raw},
            {"role": "user", "content": f"Invalid response ({error}). Reply with ONLY the JSON object."},
        ]
    sys.exit("Error: model failed to produce valid JSON after retries.")


# ---------------------------------------------------------------- commands

def cmd_progress() -> None:
    state = load_state()
    print(f"{'':2} {'topic':28} {'status':12} confidence")
    for slug, _, title in config.CURRICULUM:
        if slug in state["completed_topics"]:
            status = "done"
        elif slug == state["current_topic"]:
            status = "in progress"
        else:
            status = "-"
        conf = state["confidence"].get(slug, "-")
        weak = "  (weak - review suggested)" if slug in state["weak_topics"] else ""
        print(f"{config.TOPIC_SLUGS.index(slug) + 1:2} {slug:28} {status:12} {conf}{weak}")
    done = len(state["completed_topics"])
    print(f"\n{done}/{len(config.CURRICULUM)} topics completed")


def cmd_next() -> None:
    state = load_state()
    if state["weak_topics"]:
        print(f"You have weak topics: {', '.join(state['weak_topics'])}.")
        print("Recommended: python agent.py review")
        return
    current = state["current_topic"]
    if current and current not in state["completed_topics"]:
        print(f"You started '{current}' but haven't passed its quiz yet.")
        print(f"Recommended: python agent.py quiz {current}")
        return
    for slug in config.TOPIC_SLUGS:
        if slug not in state["completed_topics"]:
            print(f"Next up: {slug}")
            print(f"Recommended: python agent.py learn {slug}")
            return
    print("All 14 topics completed. Time to build the projects - see ../projects/README.md")


def cmd_learn(slug: str, force: bool) -> None:
    state = load_state()
    slug, notes_file, title = find_topic(slug)
    missing = unmet_prerequisites(slug, state)
    if missing and not force:
        print(f"'{slug}' assumes topics you haven't completed yet: {', '.join(missing)}")
        print(f"Recommended: python agent.py quiz {missing[0]}   (or pass --force to continue anyway)")
        return

    client = get_client()
    system = build_system(title, load_notes(notes_file), state)
    messages = [{
        "role": "user",
        "content": (
            f"Start a tutoring session on '{title}'. Begin by briefly checking my "
            "understanding of its prerequisites with one probing question, then teach "
            "the topic step by step, asking me questions as you go."
        ),
    }]
    print(f"Tutoring session: {title}  (type /quit to end)\n")
    reply = chat(client, system, messages)
    print(f"tutor> {reply}\n")
    messages.append({"role": "assistant", "content": reply})

    while True:
        try:
            user = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if user in ("/quit", "/exit", "/q"):
            break
        if not user:
            continue
        messages.append({"role": "user", "content": user})
        reply = chat(client, system, messages)
        print(f"\ntutor> {reply}\n")
        messages.append({"role": "assistant", "content": reply})

    state["current_topic"] = slug
    save_state(state)
    print(f"\nSession saved. When you feel ready: python agent.py quiz {slug}")


def run_quiz(slug: str, n_questions: int, review_mode: bool = False) -> None:
    state = load_state()
    slug, notes_file, title = find_topic(slug)
    client = get_client()
    system = build_system(title, load_notes(notes_file), state)

    kind = "review quiz" if review_mode else "quiz"
    print(f"{title} - {kind}, {n_questions} questions. Answer in your own words.\n")
    messages = []
    correct_count = 0

    for i in range(1, n_questions + 1):
        messages.append({
            "role": "user",
            "content": (
                f"Ask quiz question {i} of {n_questions} on '{title}'. One question only, "
                "no answer, not a repeat of an earlier question. Mix conceptual and practical."
            ),
        })
        question = chat(client, system, messages)
        messages.append({"role": "assistant", "content": question})
        print(f"Q{i}: {question}\n")

        first_attempt_correct = False
        for attempt in (1, 2):
            try:
                answer = input("your answer> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nQuiz abandoned - nothing recorded.")
                return
            messages.append({
                "role": "user",
                "content": (
                    f"My answer: {answer}\n\nEvaluate it. Reply with ONLY a JSON object: "
                    '{"correct": true/false, "feedback": "<one or two sentences>", '
                    '"hint": "<a hint if incorrect, else null>"}'
                ),
            })
            verdict = chat_json(client, system, messages, {"correct", "feedback"})
            messages.append({"role": "assistant", "content": json.dumps(verdict)})
            print(f"\n{verdict['feedback']}\n")
            if verdict["correct"]:
                first_attempt_correct = attempt == 1
                break
            if attempt == 1 and verdict.get("hint"):
                print(f"Hint: {verdict['hint']}\n")
            else:
                break
        if first_attempt_correct:
            correct_count += 1

    score = correct_count / n_questions
    state["quiz_results"].append({"topic": slug, "score": round(score, 2), "date": str(date.today())})

    if score >= config.PASS_THRESHOLD:
        if slug not in state["completed_topics"]:
            state["completed_topics"].append(slug)
        state["confidence"][slug] = "high" if score == 1.0 else "medium"
        if slug in state["weak_topics"]:
            state["weak_topics"].remove(slug)
        print(f"Score: {correct_count}/{n_questions} - passed. '{slug}' marked completed.")
    else:
        state["confidence"][slug] = "low"
        if slug not in state["weak_topics"]:
            state["weak_topics"].append(slug)
        print(f"Score: {correct_count}/{n_questions} - not yet. '{slug}' flagged for review.")
        print(f"Suggested: python agent.py learn {slug}   (revisit, then quiz again)")

    save_state(state)


def cmd_review() -> None:
    state = load_state()
    if state["weak_topics"]:
        target = state["weak_topics"][0]
    elif state["completed_topics"]:
        target = min(
            state["completed_topics"],
            key=lambda s: {"low": 0, "medium": 1, "high": 2}.get(state["confidence"].get(s), 0),
        )
    else:
        print("Nothing to review yet - complete a quiz first.")
        return
    run_quiz(target, n_questions=3, review_mode=True)


def cmd_exercise() -> None:
    state = load_state()
    slug = state["current_topic"] or (state["completed_topics"][-1] if state["completed_topics"] else None)
    if not slug:
        print("No topic in progress. Start with: python agent.py learn llm-fundamentals")
        return
    slug, notes_file, title = find_topic(slug)
    client = get_client()
    system = build_system(title, load_notes(notes_file), state)
    print(chat(client, system, [{
        "role": "user",
        "content": (
            f"Give me one small practical exercise for '{title}' that I can do on my own "
            "machine in under an hour. State the goal, the constraints, and how I will "
            "know I succeeded. Do NOT include the solution - offer one starting hint only."
        ),
    }]))


def main() -> None:
    parser = argparse.ArgumentParser(description="Personal AI tutor for the agentic-workflows curriculum.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_learn = sub.add_parser("learn", help="interactive tutoring session on a topic")
    p_learn.add_argument("topic", choices=config.TOPIC_SLUGS, metavar="topic")
    p_learn.add_argument("--force", action="store_true", help="skip the prerequisite check")

    p_quiz = sub.add_parser("quiz", help="quiz on a topic; passing marks it completed")
    p_quiz.add_argument("topic", choices=config.TOPIC_SLUGS, metavar="topic")

    sub.add_parser("review", help="short quiz on your weakest topic")
    sub.add_parser("exercise", help="practical exercise for your current topic")
    sub.add_parser("progress", help="show curriculum progress (works offline)")
    sub.add_parser("next", help="recommend what to do next (works offline)")

    args = parser.parse_args()
    if args.command == "learn":
        cmd_learn(args.topic, args.force)
    elif args.command == "quiz":
        run_quiz(args.topic, config.QUIZ_QUESTIONS)
    elif args.command == "review":
        cmd_review()
    elif args.command == "exercise":
        cmd_exercise()
    elif args.command == "progress":
        cmd_progress()
    elif args.command == "next":
        cmd_next()


if __name__ == "__main__":
    main()
