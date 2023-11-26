from pydantic import BaseModel, Field


class ClickHouseField(BaseModel):
    name: str = Field()
    type: str = Field()

    def to_clickhouse_str(self) -> str:
        return f"{self.name} {self.type}"


class Table(BaseModel):
    name: str = Field()
    topic: str = Field()
    fields: list[ClickHouseField] = Field()

    def get_fields_in_str(self) -> str:
        return ",\n".join([i.to_clickhouse_str() for i in self.fields])
