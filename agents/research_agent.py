from typing import Any, Dict
from agents.base_agent import BaseAgent
from core.memory import Memory

class ResearchAgent(BaseAgent):
    def __init__(self):
        super().__init__("research")

    async def run(self, params: Dict[str, Any], memory: Memory) -> Dict[str, Any]:
        topic = params.get("topic", "AI in Kerala")
        language = params.get("language", "Malayalam")
        research_output = {
            "topic": topic,
            "language": language,
            "trend": "High interest in AI jobs in Kerala",
            "keywords": ["AI Malayalam", "Kerala IT jobs", "Future of work"],
        }
        memory.save("research", research_output)
        return research_output
