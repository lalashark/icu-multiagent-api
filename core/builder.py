# app/core/builder.py

from schema.report import ReportInput, ReportOutput
from core.llm_client_base import LLMClient
from core import file_io  # 工具 function 放這
from prompts import PROMPTS
import datetime



class ReportBuilder:
    def __init__(self, llm: LLMClient, prompt_code: str):
        self.llm = llm
        self.prompt_code = prompt_code

    def _build_feature_report(self, data: ReportInput) -> str:
        pos, neg = [], []
        for feat, shap in data.shap_values.items():
            val = data.features.get(feat, "N/A")
            line = f"SHAP = {shap:+.4f}, {feat} = {val}"
            (pos if shap >= 0 else neg).append((shap, line))

        pos.sort(key=lambda x: -x[0])
        neg.sort(key=lambda x: x[0])

        pos_text = "\n".join(f"   -{line}" for _, line in pos)
        neg_text = "\n".join(f"   -{line}" for _, line in neg)

        return (
            "2. Features with positive SHAP values\n" + pos_text +
            "\n3. Features with negative SHAP values\n" + neg_text
        )

    def _get_risk_group(self, risk: float) -> str:
        return "l" if risk < 0.10 else "m" if risk < 0.20 else "h"

    def _get_system_prompt(self) -> str:
        """Return the system prompt based on the configured prompt code."""
        template = PROMPTS.get(self.prompt_code)
        if template is None:
            raise ValueError(f"Unknown prompt code: {self.prompt_code}")
        today = datetime.date.today().isoformat()
        return f"{template}\nDate: {today}"

    def build(self, data: ReportInput) -> ReportOutput:
        feature_report = self._build_feature_report(data)

        prompt = f"[1. Risk = {data.predicted_risk:.2%}]\n" + feature_report
        response, usage = self.llm.chat(system_prompt=self._get_system_prompt(), user_prompt=prompt)

        return ReportOutput(
            stay_id=data.stay_id,
            risk_group=self._get_risk_group(data.predicted_risk),
            predicted_risk_percent=round(data.predicted_risk * 100, 1),
            interpretation=file_io.extract_section(response, "Interpretation of Risk Factors"),
            examination=file_io.extract_section(response, "Recommended Examinations"),
            management=file_io.extract_section(response, "Recommended Management"),
            follow_up=file_io.extract_section(response, "Follow-up Plan"),
            summary=file_io.extract_section(response, "Summary"),
            tokens_used=usage,
        )
