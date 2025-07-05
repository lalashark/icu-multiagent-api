# app/schema/report.py

from pydantic import BaseModel, Field

class ReportInput(BaseModel):
    stay_id: int
    predicted_risk: float = Field(..., ge=0, le=1)
    features: dict[str, float | int | str]
    shap_values: dict[str, float]

    model: str = Field("gemini", description="LLM model to use")
    prompt_code: str = Field("P1", description="Prompt template code")


class ReportOutput(BaseModel):
    stay_id: int
    risk_group: str
    predicted_risk_percent: float
    interpretation: str
    examination: str
    management: str
    follow_up: str
    summary: str
    tokens_used: dict
