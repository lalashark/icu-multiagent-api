from fastapi import APIRouter
from schema.report import ReportInput
from core.builder import ReportBuilder
from core.llm_factory import create_llm

router = APIRouter()

class GenerateRequest(ReportInput):
    pass

@router.post("/generate")
def generate(req: GenerateRequest):
    llm = create_llm(req.model)
    builder = ReportBuilder(llm, req.prompt_code)
    report = builder.build(req)
    return report.dict()
