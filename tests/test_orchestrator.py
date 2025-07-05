from core.orchestrator import ReportOrchestrator
from core.agents.writer import WriterAgent
from core.agents.reviewer import ReviewerAgent
from core.agents.editor import EditorAgent
from core.llm_client_base import LLMClient

class DummyClient(LLMClient):
    def chat(self, system_prompt: str, user_prompt: str):
        return "response", {"tokens": 1}

def test_orchestrator_run():
    llm = DummyClient()
    orchestrator = ReportOrchestrator([
        WriterAgent(llm),
        ReviewerAgent(llm),
        EditorAgent(llm),
    ])
    context = {"predicted_risk": 0.1, "shap_explanation": "feat"}
    result = orchestrator.run(context)
    assert "final_report" in result
