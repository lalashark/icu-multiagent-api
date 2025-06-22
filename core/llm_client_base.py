# core/llm_client_gemini.py
from core.llm_client_base import LLMClient
import google.generativeai as genai

class GeminiClient(LLMClient):
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-pro")

    def chat(self, system_prompt, user_prompt):
        response = self.model.generate_content([
            {"role": "user", "parts": user_prompt}
        ])
        return response.text, {"source": "gemini"}
