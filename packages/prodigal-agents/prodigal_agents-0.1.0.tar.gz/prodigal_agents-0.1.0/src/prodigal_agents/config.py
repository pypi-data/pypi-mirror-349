from pydantic import BaseModel

class AgentConfig(BaseModel):
    id: str
    name: str
    orchestrator_url: str
    token: str
    model: str = "gpt-4"
    max_tokens: int = 512
    temperature: float = 0.7
