from typing import Callable, List, Tuple, Union

from crewai import Agent, Crew, Process, Task  # type: ignore
from crewai.task import TaskOutput
from langchain_core.agents import AgentAction, AgentFinish

from langflow.custom import Component
from langflow.inputs.inputs import HandleInput, InputTypes
from langflow.io import BoolInput, IntInput, Output
from langflow.schema.data import Data
from langflow.schema.message import Message


class BaseCrewComponent(Component):
    description: str = (
        "Represents a group of agents, defining how they should collaborate and the tasks they should perform."
    )
    icon = "CrewAI"

    _base_inputs: list[InputTypes] = [
        IntInput(name="verbose", display_name="Verbose", value=0, advanced=True),
        BoolInput(name="memory", display_name="Memory", value=False, advanced=True),
        BoolInput(name="use_cache", display_name="Cache", value=True, advanced=True),
        IntInput(name="max_rpm", display_name="Max RPM", value=100, advanced=True),
        BoolInput(name="share_crew", display_name="Share Crew", value=False, advanced=True),
        HandleInput(
            name="function_calling_llm",
            display_name="Function Calling LLM",
            input_types=["LanguageModel"],
            required=False,
            advanced=True,
        ),
    ]

    outputs = [
        Output(display_name="Output", name="output", method="build_output"),
    ]

    def task_is_valid(self, task_data: Data, crew_type: Process) -> Task:
        return "task_type" in task_data and task_data.task_type == crew_type

    def get_tasks_and_agents(self) -> tuple[list[Task], list[Agent]]:
        return self.tasks, self.agents

    def build_crew(self) -> Crew:
        raise NotImplementedError("build_crew must be implemented in subclasses")

    def get_task_callback(
        self,
    ) -> Callable:
        def task_callback(task_output: TaskOutput):
            self.log(task_output.model_dump(), name=f"Task (Agent: {task_output.agent}) - {self.vertex.id}")

        return task_callback

    def get_step_callback(
        self,
    ) -> Callable:
        def step_callback(agent_output: Union[AgentFinish, List[Tuple[AgentAction, str]]]):
            if isinstance(agent_output, AgentFinish):
                messages = agent_output.messages
                self.log(messages[0], name=f"Finish (Agent: {self.vertex.id})")
            elif isinstance(agent_output, list):
                messages = {f"Action {i}": action.messages for i, (action, _) in enumerate(agent_output)}
                messages = {k: v[0] if len(v) == 1 else v for k, v in messages.items()}
                self.log(messages, name=f"Step (Agent: {self.vertex.id})")

        return step_callback

    async def build_output(self) -> Message:
        crew = self.build_crew()
        result = await crew.kickoff_async()
        message = Message(text=result, sender="Machine")
        self.status = "\n\n".join([result] + [str(message) for message in self._logs])
        return message
