# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

"""Structure response as pydantic base model."""

from typing import Any, TypeVar

from pydantic import BaseModel

from graphrag_llm.utils.json_utils import safe_json_loads

T = TypeVar("T", bound=BaseModel, covariant=True)


def structure_completion_response(response: str, model: type[T]) -> T:
    """Structure completion response as pydantic base model.

    Args
    ----
        response: str
            The completion response as a JSON string.
        model: type[T]
            The pydantic base model type to structure the response into.

    Returns
    -------
        The structured response as a pydantic base model.
    """
    parsed_dict: dict[str, Any] = safe_json_loads(response)
    return model(**parsed_dict)
