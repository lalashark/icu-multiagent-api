from typing import Tuple, Dict
import anthropic

from core.llm_client_base import LLMClient

class ClaudeClient(LLMClient):
    """LLM client for Anthropic Claude."""

    def __init__(self, api_key: str, model: str = "claude-3-opus-20240229"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def chat(self, system_prompt: str, user_prompt: str) -> Tuple[str, Dict]:
        message = self.client.messages.create(
            model=self.model,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
            max_tokens=1024,
        )
        return message.content[0].text, {"source": "claude"}
