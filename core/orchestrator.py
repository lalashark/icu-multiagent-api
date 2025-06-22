# app/core/orchestrator.py

from core.agents.base import Agent
from typing import Dict, List


class ReportOrchestrator:
    def __init__(self, agents: List[Agent]):
        self.agents = agents

    def run(self, input_data: Dict) -> Dict:
        context = input_data.copy()
        for agent in self.agents:
            context = agent.run(context)
        return context
