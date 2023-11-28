from pydantic import BaseModel


class ClickSchema(BaseModel):
    element: str
