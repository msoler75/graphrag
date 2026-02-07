# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

"""JSON utilities with repair capabilities."""

import json
import logging
from typing import Any

from json_repair import repair_json

logger = logging.getLogger(__name__)


def safe_json_loads(json_str: str) -> dict[str, Any]:
    """Safely parse JSON string with repair fallback.

    Args:
        json_str: The JSON string to parse.

    Returns:
        The parsed dictionary.

    Raises:
        ValueError: If JSON cannot be parsed even after repair attempts.
    """
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        logger.warning("Failed to parse JSON, attempting repair: %s", json_str[:200])
        try:
            repaired = str(repair_json(json_str=json_str, return_objects=False))
            return json.loads(repaired)
        except json.JSONDecodeError:
            logger.exception("Failed to repair JSON")
            # Fallback: try to extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', json_str, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group(0))
                except json.JSONDecodeError:
                    pass
            raise ValueError(f"Unable to parse JSON: {json_str}")