import re


def camel_to_snake(text: str) -> str:
    """
    >>> camel_to_snake('CamelCaseString')
    'camel_case_string'

    :param text:
    :return:
    """
    text = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", text)
    text = re.sub("([a-z0-9])([A-Z])", r"\1_\2", text).lower()
    return text


def snake_to_camel(text: str) -> str:
    """
    >>> snake_to_camel('snake_case_string')
    'SnakeCaseString'

    :param text:
    :return:
    """
    return "".join(word.capitalize() for word in text.split("_"))
