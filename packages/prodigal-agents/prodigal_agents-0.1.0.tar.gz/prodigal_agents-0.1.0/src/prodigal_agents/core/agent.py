from pydantic import BaseModel

class AgentConfig(BaseModel):
    name: str
    model: str
    max_tokens: int = 512
    temperature: float = 0.7

class Agent:
    def __init__(self, config: AgentConfig):
        self.config = config

    def run(self, prompt: str) -> str:
        # Placeholder for running agent logic
        return f"Processed prompt: {prompt}"