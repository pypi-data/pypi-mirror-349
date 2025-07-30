from .config import AgentConfig
from typing import Any, Dict

class Agent:
    def __init__(self, config: AgentConfig):
        self.config = config

    def execute(self, payload: Dict[str, Any]) -> Any:
        """
        Override in subclasses: runs the payload and returns a result.
        """
        raise NotImplementedError("Agent.execute must be implemented")

    def run_local(self, prompt: str) -> str:
        # simple placeholder
        return f"[{self.config.name}] processed: {prompt}"
