from pygeai.lab.models import Agent


class AgentParser:

    @classmethod
    def get_agent(self, data: dict):
        agent = Agent.model_validate(data)

        return agent
