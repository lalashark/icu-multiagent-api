# main.py
from fastapi import FastAPI
from router import multi_agent
from api import health, generate, evaluate

app = FastAPI(
    title="ICU LLM Multi-Agent Report API",
    description="Generate ICU reports with multi-agent collaboration",
    version="0.1.0",
)

app.include_router(health.router)
app.include_router(generate.router)
app.include_router(evaluate.router)
app.include_router(multi_agent.router)
