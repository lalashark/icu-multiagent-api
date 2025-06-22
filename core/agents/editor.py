# app/core/agents/editor.py

from core.agents.base import Agent
from core.llm_client_base import LLMClient

class EditorAgent(Agent):
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def run(self, context: dict) -> dict:
        draft = context["draft_report"]
        notes = context["review_notes"]

        prompt = f"""You are a medical editor.
Improve the ICU report using the reviewer’s feedback.

Original Draft:
{draft}

Reviewer Feedback:
{notes}
"""
        response, usage = self.llm.chat(system_prompt="You are an editor.", user_prompt=prompt)
        context["final_report"] = response
        context["editor_tokens"] = usage
        return context
