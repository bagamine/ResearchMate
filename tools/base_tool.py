from abc import ABC, abstractmethod

class BaseTool(ABC):
    @abstractmethod
    def run(self, input_data: str,topic: str) -> str:
        """Run the tool on input data."""
        pass
