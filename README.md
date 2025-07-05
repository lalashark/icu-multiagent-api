# ICU Multi-Agent API

This project exposes a simple FastAPI service that demonstrates how a
multi-agent workflow can be wrapped as an API for generating ICU
reports. The service coordinates writer, reviewer and editor agents that
communicate with language models (Gemini or Claude).

## Installation

```bash
pip install -r requirements.txt
```

Environment variables `GEMINI_API_KEY` and `CLAUDE_API_KEY` are required
when using the real LLM services.

## Running

```bash
uvicorn main:app --reload
```

## Testing

```bash
pytest
```
