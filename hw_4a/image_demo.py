import argparse
import base64
from pathlib import Path

from openai import OpenAI


def generate_with_openai(prompt: str, output_path: Path, model: str) -> None:
    client = OpenAI()
    response = client.responses.create(
        model=model,
        input=prompt,
        tools=[{"type": "image_generation"}],
    )

    image_b64 = next(
        (
            item.result
            for item in response.output
            if item.type == "image_generation_call"
        ),
        None,
    )
    if not image_b64:
        raise RuntimeError("OpenAI response did not include an image.")

    output_path.write_bytes(base64.b64decode(image_b64))


def generate_with_ollama(
    prompt: str,
    output_path: Path,
    model: str,
    base_url: str,
) -> None:
    # Ollama exposes an OpenAI-compatible experimental image endpoint.
    client = OpenAI(base_url=base_url.rstrip("/") + "/v1", api_key="ollama")
    response = client.images.generate(
        model=model,
        prompt=prompt,
        size="1024x1024",
        response_format="b64_json",
    )

    image_b64 = response.data[0].b64_json
    if not image_b64:
        raise RuntimeError("Ollama response did not include image data.")

    output_path.write_bytes(base64.b64decode(image_b64))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate an image with OpenAI or Ollama."
    )
    parser.add_argument(
        "--provider",
        choices=("openai", "ollama"),
        required=True,
        help="Which backend to use.",
    )
    parser.add_argument("--prompt", required=True, help="Image prompt.")
    parser.add_argument(
        "--output",
        default="generated.png",
        help="Where to save the generated image.",
    )
    parser.add_argument(
        "--openai-model",
        default="gpt-5",
        help="Responses API model for OpenAI image generation.",
    )
    parser.add_argument(
        "--ollama-model",
        default="x/z-image-turbo",
        help="Ollama image model to use.",
    )
    parser.add_argument(
        "--ollama-base-url",
        default="http://localhost:11434",
        help="Base URL for the Ollama server.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if args.provider == "openai":
        generate_with_openai(args.prompt, output_path, args.openai_model)
    else:
        generate_with_ollama(
            args.prompt,
            output_path,
            args.ollama_model,
            args.ollama_base_url,
        )

    print(f"Saved image to {output_path}")


if __name__ == "__main__":
    main()
