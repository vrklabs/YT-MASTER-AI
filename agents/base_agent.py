from abc import ABC, abstractmethod
from typing import Any, Dict
from core.memory import Memory

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    async def run(self, params: Dict[str, Any], memory: Memory) -> Dict[str, Any]:
        pass
