# Reflection Agent Demo

A small LangGraph application that improves a draft tweet through a generation
and reflection cycle. It uses LangChain prompt templates and Google's Gemini
chat model.

## How it works

The graph in `main.py` follows this flow:

1. **Generate** a tweet from the initial request using the generation prompt in
   `chains.py`.
2. **Reflect** on the draft and produce critique and recommendations.
3. **Generate** a revised tweet using the critique.
4. Stop when the message history contains more than three messages.

The current threshold allows one reflection and revision cycle. The reflection
node adds a user-message instruction after the generated draft before invoking
the reflection chain; the critique is then added to the graph history as a
`HumanMessage` for the next generation.

When `main.py` runs, it also prints Mermaid and ASCII graph representations and
writes a graph image to `flow.png`.

### Reflection agent graph

![Reflection agent graph](./flow.png)

## Requirements

- Python 3.13 or newer
- [uv](https://docs.astral.sh/uv/)
- A Google Gemini API key

## Setup

Install the project dependencies from the lockfile:

```bash
uv sync
```

Copy `.env.example` to `.env` in the project root, then add your Gemini API key:

```sh
cp .env.example .env
```

Keep `.env` local; do not commit API keys or other credentials.

LangSmith tracing is enabled by default in the example configuration. Add your
LangSmith API key to `.env` to send traces to the `reflection-agent-demo`
project, or set `LANGSMITH_TRACING=false` to disable tracing.

## Run

```bash
uv run python main.py
```

The script sends the sample tweet request in `main.py` to Gemini and prints the
final graph state. API usage may incur charges according to your Google Cloud
or Gemini API plan.
