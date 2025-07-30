from prodigal_agents.core.agent import Agent, AgentConfig

def test_agent_run():
    config = AgentConfig(name="TestAgent", model="gpt-4")
    agent = Agent(config)
    result = agent.run("What is the capital of France?")
    assert "Processed prompt" in result