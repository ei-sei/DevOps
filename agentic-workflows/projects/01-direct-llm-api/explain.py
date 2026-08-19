"""Project 1: direct LLM API usage - messages, temperature, tokens, streaming."""

import argparse
import json
import os
import sys

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

MODEL = "claude-sonnet-4-5"
PRICE_PER_MTOK = {"input": 3.00, "output": 15.00}

SYSTEM = (
    "You are a concise DevOps tutor. Explain the requested concept for an "
    "engineer with a DevOps background in at most three short paragraphs, "
    "with one practical example."
)


def get_client():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit(
            "Error: ANTHROPIC_API_KEY is not set.\n"
            "Copy .env.example to .env and add your key, or export it:\n"
            "  export ANTHROPIC_API_KEY=sk-ant-..."
        )
    import anthropic

    return anthropic.Anthropic()


def report_usage(usage) -> None:
    cost = (
        usage.input_tokens * PRICE_PER_MTOK["input"]
        + usage.output_tokens * PRICE_PER_MTOK["output"]
    ) / 1e6
    print(
        f"\n--- usage: {usage.input_tokens} in / {usage.output_tokens} out "
        f"(~${cost:.5f}) ---"
    )


def explain(topic: str, temperature: float, stream: bool, debug: bool) -> None:
    client = get_client()
    request = {
        "model": MODEL,
        "max_tokens": 1024,
        "temperature": temperature,
        "system": SYSTEM,
        "messages": [{"role": "user", "content": f"Explain: {topic}"}],
    }
    if debug:
        print("--- request payload ---")
        print(json.dumps(request, indent=2))
        print("--- response ---")

    if stream:
        with client.messages.stream(**request) as s:
            for text in s.text_stream:
                print(text, end="", flush=True)
            print()
            report_usage(s.get_final_message().usage)
    else:
        response = client.messages.create(**request)
        print(response.content[0].text)
        report_usage(response.usage)


def compare_temperature(topic: str, debug: bool) -> None:
    for temp in (0.0, 1.0):
        print(f"\n===== temperature {temp} =====")
        explain(topic, temperature=temp, stream=False, debug=debug)


def main() -> None:
    parser = argparse.ArgumentParser(description="Explain a DevOps concept via a direct LLM API call.")
    parser.add_argument("topic", help="concept to explain, e.g. 'kubernetes statefulsets'")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--no-stream", action="store_true", help="wait for the full response")
    parser.add_argument("--compare-temperature", action="store_true", help="run at temperature 0 and 1")
    parser.add_argument("--debug", action="store_true", help="print the raw request payload")
    args = parser.parse_args()

    if args.compare_temperature:
        compare_temperature(args.topic, args.debug)
    else:
        explain(args.topic, args.temperature, stream=not args.no_stream, debug=args.debug)


if __name__ == "__main__":
    main()
