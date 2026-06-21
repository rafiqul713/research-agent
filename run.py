#!/usr/bin/env python3
"""Run the research agent from the command line."""

import sys
from dotenv import load_dotenv
from src.graph import research_app

load_dotenv()


def main():
    topic = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else None

    if not topic:
        topic = input("Enter a research topic: ").strip()

    if not topic:
        print("No topic provided. Exiting.")
        sys.exit(1)

    print(f"\n Starting research on: '{topic}'\n{'='*60}")

    result = research_app.invoke({"topic": topic})

    print("\n" + "="*60)
    print("FINAL REPORT")
    print("="*60 + "\n")
    print(result["report"])

    # Save to file
    filename = topic.lower().replace(" ", "_")[:40] + "_report.md"
    with open(filename, "w") as f:
        f.write(result["report"])
    print(f"\n Report saved to: {filename}")


if __name__ == "__main__":
    main()