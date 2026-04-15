# LangChain Starter For Ollama

This repo is now intentionally focused on one thing:

- one very small LangChain example
- optimized for a local Ollama model
- easy to compare to the OpenAI SDK you already know

## LangChain vs LangGraph

Short version:

- LangChain is a convenient interface for talking to models, prompts, tools, and structured outputs.
- LangGraph is for multi-step workflows with state, branching, loops, and agent-style control flow.

Good mental model:

- use LangChain when you want "call a model cleanly"
- use LangGraph when you want "coordinate a process"

If you are just learning, LangChain is the better first stop. That is why `main.py` now only shows LangChain.

## Files

- `main.py`: one tiny LangChain chat example using Ollama

## Setup

Install dependencies:

```bash
uv sync
```

Make sure Ollama is running locally and that you have a model pulled, for example:

```bash
ollama pull gemma4:e4b
```

Then:

```bash
export OLLAMA_MODEL=gemma4:e4b
export OLLAMA_BASE_URL=http://localhost:11434/v1
```

`OLLAMA_API_KEY` is optional here. If you do not set it, the example uses `"ollama"`.

## Run it

```bash
uv run python main.py "Explain recursion in one paragraph."
```

## What `main.py` is showing

- Build a `ChatOpenAI` model object.
- Point it at Ollama's OpenAI-compatible endpoint.
- Send `SystemMessage` and `HumanMessage`.
- Print the returned text.

That is the simplest LangChain example that still feels realistic.
