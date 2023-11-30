import uuid

from pydantic import BaseModel, field_serializer


class VideoFinishSchema(BaseModel):
    film_id: uuid.UUID

    @field_serializer("film_id")
    def film_id_serialize(self, film_id: uuid.UUID) -> str:
        return str(film_id)
