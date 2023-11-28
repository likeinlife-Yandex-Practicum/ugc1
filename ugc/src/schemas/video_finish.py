import re

from pydantic import BaseModel, field_validator
from src.core.exceptions import FILM_ID_EXCEPTION


class VideoFinishSchema(BaseModel):
    film_id: str

    @field_validator('film_id')
    @classmethod
    def validate_film_id(cls, value: str):
        is_correct_uuid4 = re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', value)
        if not is_correct_uuid4:
            raise FILM_ID_EXCEPTION
