from agents.core.base import AgentResult, BaseAgent


class DiscoveryAgent(BaseAgent):
    name = "discovery"
    def run(self, state):
        return AgentResult({"status": "placeholder"})
