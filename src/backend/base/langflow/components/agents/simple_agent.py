from langflow.base.models.model import LCModelComponent
from langflow.components.agents.tool_calling import ToolCallingAgentComponent
from langflow.components.models.azure_openai import AzureChatOpenAIComponent
from langflow.components.models.openai import OpenAIModelComponent
from langflow.io import (
    DataInput,
    DropdownInput,
    HandleInput,
    MessageTextInput,
    Output,
)
from langflow.schema.dotdict import dotdict
from langflow.schema.message import Message


class SimpleAgentComponent(ToolCallingAgentComponent):
    display_name: str = "Simple Agent"
    description: str = "Agent that uses tools"
    icon = "workflow"
    beta = True
    name = "SimpleAgent"

    openai_inputs = [
        component_input
        for component_input in OpenAIModelComponent().inputs
        if component_input.name not in [input_field.name for input_field in LCModelComponent._base_inputs]
    ]
    azure_inputs = [
        component_input
        for component_input in AzureChatOpenAIComponent().inputs
        if component_input.name not in [input_field.name for input_field in LCModelComponent._base_inputs]
    ]
    inputs = [
        HandleInput(
            name="tools", display_name="Tools", input_types=["Tool", "BaseTool", "StructuredTool"], is_list=True
        ),
        MessageTextInput(name="input_value", display_name="Input"),
        DataInput(name="chat_history", display_name="Chat History", is_list=True, advanced=True),
        DropdownInput(
            name="agent_llm",
            display_name="Language Model Type",
            options=["Azure OpenAI", "OpenAI", "Custom"],
            value="OpenAI",
            real_time_refresh=True,
            refresh_button=True,
            input_types=[],
        ),
        *openai_inputs,
    ]
    outputs = [Output(name="response", display_name="Response", method="get_response")]

    async def get_response(self) -> Message:
        llm_model = self.get_llm()
        if llm_model is None:
            msg = "No language model selected"
            raise ValueError(msg)

        agent = ToolCallingAgentComponent().set(
            llm=llm_model, tools=[self.tools], chat_history=self.chat_history, input_value=self.input_value
        )

        return await agent.message_response()

    def get_llm(self):
        try:
            if self.agent_llm == "OpenAI":
                return self._build_llm_model(OpenAIModelComponent(), self.openai_inputs)
            if self.agent_llm == "Azure OpenAI":
                return self._build_llm_model(AzureChatOpenAIComponent(), self.azure_inputs, prefix="azure_param_")
        except Exception as e:
            msg = f"Error building {self.agent_llm} language model"
            raise ValueError(msg) from e
        return self.agent_llm

    def _build_llm_model(self, component, inputs, prefix=""):
        return component.set(
            **{component_input.name: getattr(self, f"{prefix}{component_input.name}") for component_input in inputs}
        ).build_model()

    def delete_fields(self, build_config, fields):
        for field in fields:
            build_config.pop(field, None)

    def update_build_config(self, build_config: dotdict, field_value: str, field_name: str | None = None):
        if field_name == "agent_llm":
            openai_fields = {component_input.name: component_input for component_input in self.openai_inputs}
            azure_fields = {
                f"azure_param_{component_input.name}": component_input for component_input in self.azure_inputs
            }

            if field_value == "OpenAI":
                self.delete_fields(build_config, {**azure_fields})
                if not any(field in build_config for field in openai_fields):
                    build_config.update(openai_fields)
                build_config["agent_llm"]["input_types"] = []
                build_config = self.update_input_types(build_config)

            elif field_value == "Azure OpenAI":
                self.delete_fields(build_config, {**openai_fields})
                build_config.update(azure_fields)
                build_config["agent_llm"]["input_types"] = []
                build_config = self.update_input_types(build_config)
            elif field_value == "Custom":
                self.delete_fields(build_config, {**openai_fields})
                self.delete_fields(build_config, {**azure_fields})
                new_component = DropdownInput(
                    name="agent_llm",
                    display_name="Language Model",
                    options=["Azure OpenAI", "OpenAI", "Custom"],
                    value="Custom",
                    real_time_refresh=True,
                    input_types=["LanguageModel"],
                )
                build_config.update({"agent_llm": new_component.to_dict()})
                build_config = self.update_input_types(build_config)
            default_keys = ["code", "_type", "agent_llm", "tools", "input_value"]
            missing_keys = [key for key in default_keys if key not in build_config]
            if missing_keys:
                msg = f"Missing required keys in build_config: {missing_keys}"
                raise ValueError(msg)
        return build_config

    def update_input_types(self, build_config):
        for key, value in build_config.items():
            # Check if the value is a dictionary
            if isinstance(value, dict):
                if value.get("input_types") is None:
                    build_config[key]["input_types"] = []
            # Check if the value has an attribute 'input_types' and it is None
            elif hasattr(value, "input_types") and value.input_types is None:
                value.input_types = []
        return build_config
