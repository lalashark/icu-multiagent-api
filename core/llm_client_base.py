from abc import ABC, abstractmethod
from typing import Tuple, Dict

class LLMClient(ABC):
    """Abstract base client for language models."""

    @abstractmethod
    def chat(self, system_prompt: str, user_prompt: str) -> Tuple[str, Dict]:
        """Send prompts to the model and return response text and usage info."""
        raise NotImplementedError
