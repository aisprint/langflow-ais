from crewai import Agent, Crew, Process, Task  # type: ignore

from langflow.base.agents.crewai.crew import BaseCrewComponent
from langflow.io import HandleInput
from langflow.schema.message import Message


class SequentialCrewComponent(BaseCrewComponent):
    display_name: str = "Sequential Crew"
    description: str = (
        "Represents a group of agents, defining how they should collaborate and the tasks they should perform."
    )
    documentation: str = "https://docs.crewai.com/how-to/LLM-Connections/"
    icon = "CrewAI"

    inputs = BaseCrewComponent._base_inputs + [
        HandleInput(name="tasks", display_name="Tasks", input_types=["SequentialTask"], is_list=True),
    ]

    def get_tasks_and_agents(self) -> tuple[list[Task], list[Agent]]:
        return self.tasks, [task.agent for task in self.tasks]

    def build_crew(self) -> Message:
        tasks, agents = self.get_tasks_and_agents()
        crew = Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=self.verbose,
            memory=self.memory,
            cache=self.use_cache,
            max_rpm=self.max_rpm,
            share_crew=self.share_crew,
            function_calling_llm=self.function_calling_llm,
        )
        return crew
