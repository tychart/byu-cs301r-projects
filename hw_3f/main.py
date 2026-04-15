from __future__ import annotations

import argparse
import os

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI


def build_model() -> ChatOpenAI:
    return ChatOpenAI(
        model=os.getenv("OLLAMA_MODEL", "gemma4:e4b"),
        api_key=os.getenv("OLLAMA_API_KEY", "ollama"),
        base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
    )


def message_to_text(message) -> str:
    content = message.content
    if isinstance(content, str):
        return content
    return str(content)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Super simple LangChain starter for a local Ollama model."
    )
    parser.add_argument("prompt", help="Prompt to send to the model.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    model = build_model()
    response = model.invoke(
        [
            SystemMessage(content="You are a concise teaching assistant."),
            HumanMessage(content=args.prompt),
        ]
    )
    answer = message_to_text(response)
    print(answer)


if __name__ == "__main__":
    main()
