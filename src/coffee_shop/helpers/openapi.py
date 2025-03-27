from typing import Any

from pydantic import BaseModel


class ResponseExample(BaseModel):
    value: Any


def create_openapi_response_examples(model_examples: dict[str, Any]) -> dict[str, Any]:
    """
    Generate OpenAPI response examples from Pydantic models.

    Args:
        model_examples: A list of {"example_name": pydantic_model_instance} dicts.

    Returns:
        An OpenAPI "examples" dictionary, or an empty dict on error/empty input.
        Raises ValueError for invalid input format.
    """
    if not model_examples:
        return {}

    examples: dict[str, dict[str, Any]] = {}

    for name, model_instance in model_examples.items():
        value = ResponseExample(value=model_instance.model_dump()).model_dump()

        examples.update({name: value})

    return {"application/json": {"examples": examples}}
