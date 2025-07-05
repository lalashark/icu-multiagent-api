from typing import Tuple, Dict
import google.generativeai as genai

from core.llm_client_base import LLMClient

class GeminiClient(LLMClient):
    """LLM client for Google Gemini."""

    def __init__(self, api_key: str, model: str = "gemini-pro"):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)

    def chat(self, system_prompt: str, user_prompt: str) -> Tuple[str, Dict]:
        response = self.model.generate_content([
            {"role": "user", "parts": system_prompt + "\n" + user_prompt}
        ])
        return response.text, {"source": "gemini"}
