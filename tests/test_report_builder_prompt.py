import sys
import types

if "pandas" not in sys.modules:
    pandas_stub = types.ModuleType("pandas")
    pandas_stub.DataFrame = object
    pandas_stub.read_csv = lambda *a, **k: None
    sys.modules["pandas"] = pandas_stub

from core.builder import ReportBuilder
from schema.report import ReportInput
from core.llm_client_base import LLMClient
from prompts import PROMPTS

class DummyClient(LLMClient):
    def __init__(self):
        self.system_prompt = None
    def chat(self, system_prompt: str, user_prompt: str):
        self.system_prompt = system_prompt
        return "", {}

def _make_input():
    return ReportInput(stay_id=1, predicted_risk=0.1, features={}, shap_values={})

def test_prompt_templates_used():
    for code, template in PROMPTS.items():
        llm = DummyClient()
        builder = ReportBuilder(llm, code)
        builder.build(_make_input())
        assert llm.system_prompt.startswith(template)
