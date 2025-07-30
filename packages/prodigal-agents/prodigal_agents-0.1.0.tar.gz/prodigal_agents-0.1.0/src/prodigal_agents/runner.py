import time
import requests
from .agent import Agent
from .config import AgentConfig

def run_agent_loop(agent: Agent):
    """
    Polls the orchestrator for tasks, executes them via agent.execute(),
    then reports results.
    """
    cfg = agent.config
    while True:
        resp = requests.get(
            f"{cfg.orchestrator_url}/next-task",
            params={"agent_id": cfg.id},
            headers={"Authorization": f"Bearer {cfg.token}"}
        )
        if resp.status_code == 200 and resp.json():
            task = resp.json()
            result = agent.execute(task["payload"])
            requests.post(
                f"{cfg.orchestrator_url}/report-task",
                json={"task_id": task["id"], "result": result},
                headers={"Authorization": f"Bearer {cfg.token}"}
            )
        time.sleep(2)
