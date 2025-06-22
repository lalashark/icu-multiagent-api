# app/router/multi_agent.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.orchestrator import ReportOrchestrator
from core.agents.writer import WriterAgent
from core.agents.reviewer import ReviewerAgent
from core.agents.editor import EditorAgent
from core.llm_factory import create_llm

router = APIRouter()


class MultiAgentRequest(BaseModel):
    stay_id: int
    predicted_risk: float
    shap_explanation: str


@router.post("/generate_multi_agent_report")
def generate_multi_agent_report(req: MultiAgentRequest):
    try:
        llm = create_llm("gemini")  # or "azure" based on your setup

        orchestrator = ReportOrchestrator([
            WriterAgent(llm),
            ReviewerAgent(llm),
            EditorAgent(llm),
        ])

        context = {
            "stay_id": req.stay_id,
            "predicted_risk": req.predicted_risk,
            "shap_explanation": req.shap_explanation,
        }

        result = orchestrator.run(context)

        return {
            "stay_id": req.stay_id,
            "final_report": result["final_report"],
            "review_notes": result["review_notes"],
            "writer_tokens": result.get("writer_tokens", {}),
            "reviewer_tokens": result.get("reviewer_tokens", {}),
            "editor_tokens": result.get("editor_tokens", {}),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
