# main.py

from fastapi import FastAPI
from router import multi_agent

app = FastAPI(
    title="ICU LLM Multi-Agent Report API",
    description="Generate ICU reports with multi-agent collaboration",
    version="0.1.0",
)

# 註冊多 Agent 路由
app.include_router(multi_agent.router)
