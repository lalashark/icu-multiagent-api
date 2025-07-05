from typing import Dict, Any, List
from core.agents.base import Agent

class ReportOrchestrator:
    """Coordinate a series of agents to generate a report."""

    def __init__(self, agents: List[Agent]):
        self.agents = agents

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        for agent in self.agents:
            context = agent.run(context)
        return context
