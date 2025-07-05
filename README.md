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

## Docker

A `Dockerfile` is provided to run the service in a container.

### Build the image

```bash
docker build -t icu-api .
```

### Run the container

```bash
docker run -p 8000:8000 \
  -e GEMINI_API_KEY=your_key \
  -e CLAUDE_API_KEY=your_key \
  icu-api
```

### Example request

```bash
curl -X POST http://localhost:8000/generate_multi_agent_report \
  -H 'Content-Type: application/json' \
  -d '{"stay_id": 1, "predicted_risk": 0.2, "shap_explanation": "age high"}'
```
