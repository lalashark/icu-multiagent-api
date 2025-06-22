# app/core/agents/base.py

from abc import ABC, abstractmethod
from typing import Dict


class Agent(ABC):
    @abstractmethod
    def run(self, context: Dict) -> Dict:
        """執行 agent 任務，接收上下文資料，回傳新的上下文"""
        pass
