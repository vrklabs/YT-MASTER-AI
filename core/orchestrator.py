import asyncio
from typing import Dict, Any
from core.agent_registry import AgentRegistry
from core.task_queue import TaskQueue
from core.memory import Memory

class AIOSOrchestrator:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.registry = AgentRegistry()
        self.queue = TaskQueue()
        self.memory = Memory()
        self._load_agents()

    def _load_agents(self):
        # ടെസ്റ്റിനായി ഇപ്പോൾ രണ്ട് ഏജന്റുകൾ മാത്രം
        from agents.research_agent import ResearchAgent
        from agents.script_agent import ScriptAgent

        self.registry.register("research", ResearchAgent)
        self.registry.register("script", ScriptAgent)

    async def run_pipeline(self, task: str, parameters: Dict[str, Any]):
        task_id = self.queue.add_task(task, parameters)
        print(f"Task {task_id} added to queue.")

        if task == "create_episode":
            return await self._create_episode(parameters)
        else:
            raise NotImplementedError(f"Task '{task}' not implemented yet.")

    async def _create_episode(self, params: Dict[str, Any]):
        steps = [
            ("research", self.registry.get("research")),
            ("script", self.registry.get("script")),
        ]
        results = {}
        for step_name, agent in steps:
            if agent is None:
                results[step_name] = {"error": f"Agent '{step_name}' not registered."}
                continue
            try:
                result = await agent.run(params, self.memory)
                results[step_name] = result
                self.memory.save(step_name, result)
            except Exception as e:
                results[step_name] = {"error": str(e)}
        return results
