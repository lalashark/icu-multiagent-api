from fastapi import APIRouter
from pydantic import BaseModel
from core.builder import ReportBuilder
from core.llm_factory import create_llm

router = APIRouter()

class GenerateRequest(BaseModel):
    stay_id: int
    predicted_risk: float
    features: dict[str, float | int | str]
    shap_values: dict[str, float]
    model: str = "gemini"
    prompt_code: str = "P1"

@router.post("/generate")
def generate(req: GenerateRequest):
    llm = create_llm(req.model)
    builder = ReportBuilder(llm, req.prompt_code)
    report = builder.build(req)
    return report.dict()
