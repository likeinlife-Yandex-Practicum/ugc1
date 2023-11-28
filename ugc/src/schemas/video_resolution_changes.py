from pydantic import BaseModel


class VideoResolutionChangeSchema(BaseModel):
    from_resolution: str
    to_resolution: str
