# app/core/agents/reviewer.py

from core.agents.base import Agent
from core.llm_client_base import LLMClient

class ReviewerAgent(Agent):
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def run(self, context: dict) -> dict:
        draft = context["draft_report"]

        prompt = f"""You are a senior ICU physician.
Review the following report written by a junior doctor and suggest improvements.
Report:
{draft}
"""
        response, usage = self.llm.chat(system_prompt="You are a reviewer.", user_prompt=prompt)
        context["review_notes"] = response
        context["reviewer_tokens"] = usage
        return context
