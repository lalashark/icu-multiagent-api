from core.agents.writer import WriterAgent
from core.agents.editor import EditorAgent
from core.agents.reviewer import ReviewerAgent
from core.llm_factory import get_llm_client

from typing import Dict, Any


def generate_multi_agent_report(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    核心單輪多 Agent 協作邏輯：
    Writer → Editor → Reviewer → Output
    """
    # 初始化 LLM 客戶端（例如 Gemini）
    llm = get_llm_client(model_name=input_data.get("llm", "gemini"))

    # 初始化各角色 Agent（可以考慮依參數決定是否啟用）
    writer = WriterAgent(llm)
    editor = EditorAgent(llm)
    reviewer = ReviewerAgent(llm)

    # Writer 根據輸入生成初稿
    initial_report = writer.generate(input_data)

    # Editor 進行潤稿
    edited_report = editor.edit(initial_report, context=input_data)

    # Reviewer 給出最終版本
    final_report = reviewer.review(edited_report, context=input_data)

    return {
        "report": final_report,
        "agents": {
            "writer_output": initial_report,
            "editor_output": edited_report,
            "reviewer_output": final_report,
        }
    }


def generate_multi_round_report(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    預留多輪次對話產文接口：由 teammate 接手實作
    """
    raise NotImplementedError("Multi-round agent workflow is not implemented yet.")
