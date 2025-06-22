# app/core/llm_factory.py

from core.llm_client_claude import ClaudeClient
from core.llm_client_gemini import GeminiClient
from core.llm_client_base import LLMClient

def get_llm_client(model: str, api_key: str) -> LLMClient:
    if model == "claude":
        return ClaudeClient(api_key)
    elif model == "gemini":
        return GeminiClient(api_key)
    else:
        raise ValueError(f"Unsupported model type: {model}")
