from langchain_core.documents import Document

from langflow.schema import Data
from langflow.schema.message import Message


def docs_to_data(documents: list[Document]) -> list[Data]:
    """Converts a list of Documents to a list of Data.

    Args:
        documents (list[Document]): The list of Documents to convert.

    Returns:
        list[Data]: The converted list of Data.
    """
    return [Data.from_document(document) for document in documents]


def data_to_text_list(template: str, data: Data | list[Data]) -> tuple[list[str], list[Data]]:
    """Converts a Data object or a list of Data objects into a tuple containing a list of formatted strings
    and a list of Data objects based on a given template.

    Args:
        template (str): The format string template to be used for formatting the data.
        data (Data | list[Data]): A single Data object or a list of Data objects to be formatted.

    Returns:
        tuple[list[str], list[Data]]: A tuple containing a list of formatted strings based on the
                                      provided template and data, and a list of Data objects.
    """
    if data is None:
        return [], []

    if template is None or not isinstance(template, str):
        raise ValueError("The template must be a string.")

    if isinstance(data, (Data)):
        data = [data]
    # Check if there are any format strings in the template
    _data = [
        # If it is not a record, create one with the key "text"
        Data(text=value) if not isinstance(value, Data) else value
        for value in data
    ]

    formatted_text = [template.format(data=value.data, **value.data) for value in _data]
    return formatted_text, _data


def data_to_text(template: str, data: Data | list[Data], sep: str = "\n") -> str:
    """Converts data into a formatted text string based on a given template.

    Args:
        template (str): The template string used to format each data item.
        data (Data | list[Data]): A single data item or a list of data items to be formatted.
        sep (str, optional): The separator to use between formatted data items. Defaults to "\n".

    Returns:
        str: A string containing the formatted data items separated by the specified separator.
    """
    formatted_text, _ = data_to_text_list(template, data)
    sep = "\n" if sep is None else sep
    return sep.join(formatted_text)


def messages_to_text(template: str, messages: Message | list[Message]) -> str:
    """Converts a list of Messages to a list of texts.

    Args:
        template (str): The template to use for the conversion.
        messages (list[Message]): The list of Messages to convert.

    Returns:
        list[str]: The converted list of texts.
    """
    if isinstance(messages, (Message)):
        messages = [messages]
    # Check if there are any format strings in the template
    _messages = []
    for message in messages:
        # If it is not a message, create one with the key "text"
        if not isinstance(message, Message):
            msg = "All elements in the list must be of type Message."
            raise TypeError(msg)
        _messages.append(message)

    formated_messages = [template.format(data=message.model_dump(), **message.model_dump()) for message in _messages]
    return "\n".join(formated_messages)
