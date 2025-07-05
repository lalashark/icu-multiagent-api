from core.llm_client_claude import ClaudeClient
from core.llm_client_gemini import GeminiClient
from core.llm_client_base import LLMClient
from config import settings


def get_llm_client(model: str, api_key: str) -> LLMClient:
    if model == "claude":
        return ClaudeClient(api_key)
    elif model == "gemini":
        return GeminiClient(api_key)
    else:
        raise ValueError(f"Unsupported model type: {model}")


def create_llm(model: str) -> LLMClient:
    """Create an LLM client using API keys from settings."""
    if model == "claude":
        return get_llm_client("claude", settings.claude_api_key)
    return get_llm_client("gemini", settings.gemini_api_key)
