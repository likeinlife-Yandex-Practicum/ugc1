import json
from pathlib import Path

from pydantic import TypeAdapter
from pydantic_core import PydanticSerializationError

from .errors import InvalidJsonConfig, JsonConfigNotFound
from .models import Table


def get_tables(path: Path) -> list[Table]:
    """Get tables from json-config-file."""
    if not path.exists():
        raise JsonConfigNotFound

    with open(path, "r", encoding="utf-8") as file_obj:
        try:
            json_obj = json.load(file_obj)
            return TypeAdapter(list[Table]).validate_python(json_obj)
        except (json.JSONDecodeError, PydanticSerializationError) as e:
            raise InvalidJsonConfig from e
