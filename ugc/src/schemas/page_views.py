from pydantic import BaseModel


class PageViewSchema(BaseModel):
    page: str
