from fastapi import APIRouter
from pydantic import BaseModel
from core.llm_factory import create_llm
from core.agents.reviewer import ReviewerAgent

router = APIRouter()

class EvaluateRequest(BaseModel):
    report: str
    model: str = "claude"

@router.post("/evaluate")
def evaluate(req: EvaluateRequest) -> dict:
    llm = create_llm(req.model)
    reviewer = ReviewerAgent(llm)
    context = {"draft_report": req.report}
    reviewer.run(context)
    return {"review_notes": context["review_notes"]}
