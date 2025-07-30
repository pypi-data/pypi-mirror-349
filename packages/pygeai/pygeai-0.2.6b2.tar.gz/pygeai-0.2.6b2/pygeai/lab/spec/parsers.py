from pygeai.lab.models import Agent, Tool


class AgentParser:

    @classmethod
    def get_agent(cls, data: dict):
        agent = Agent.model_validate(data)

        return agent


class ToolParser:

    @classmethod
    def get_tool(cls, data: dict):
        tool = Tool.model_validate(data)

        return tool