# app/core/agents/writer.py

from core.agents.base import Agent
from core.llm_client_base import LLMClient

class WriterAgent(Agent):
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def run(self, context: dict) -> dict:
        risk = context["predicted_risk"]
        shap_text = context["shap_explanation"]

        prompt = f"""You are an ICU doctor.
Based on the following patient risk score and feature explanation,
write a draft ICU report.

Risk: {risk:.2%}
{shap_text}
"""
        response, usage = self.llm.chat(system_prompt="You are an ICU doctor.", user_prompt=prompt)
        context["draft_report"] = response
        context["writer_tokens"] = usage
        return context
