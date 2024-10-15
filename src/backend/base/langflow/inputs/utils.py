from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from langflow.inputs.inputs import InputTypes, InputTypesMap
else:
    InputTypes = Any
    InputTypesMap = Any

# Lazy import for InputTypesMap
_InputTypesMap: dict[str, type["InputTypes"]] | None = None


def get_InputTypesMap():
    global _InputTypesMap  # noqa: PLW0603
    if _InputTypesMap is None:
        from langflow.inputs.inputs import InputTypesMap

        _InputTypesMap = InputTypesMap
    return _InputTypesMap


def instantiate_input(input_type: str, data: dict) -> InputTypes:
    InputTypesMap = get_InputTypesMap()

    input_type_class = InputTypesMap.get(input_type)
    if "type" in data:
        # Replace with field_type
        data["field_type"] = data.pop("type")
    if input_type_class:
        return input_type_class(**data)
    msg = f"Invalid input type: {input_type}"
    raise ValueError(msg)
