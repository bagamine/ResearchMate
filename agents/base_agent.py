# agents/base_agent.py
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    @abstractmethod
    def execute(self, input_data: str) -> str:
        pass
