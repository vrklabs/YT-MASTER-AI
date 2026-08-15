from typing import Dict, Type

class AgentRegistry:
    def __init__(self):
        self._agents: Dict[str, Type] = {}

    def register(self, name: str, agent_class: Type):
        self._agents[name] = agent_class

    def get(self, name: str):
        agent_class = self._agents.get(name)
        if agent_class:
            return agent_class()
        return None

    def list_agents(self):
        return list(self._agents.keys())
