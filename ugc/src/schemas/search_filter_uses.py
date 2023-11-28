from pydantic import BaseModel


class SearchFilterUseSchema(BaseModel):
    filter: str
    filter_value: str
