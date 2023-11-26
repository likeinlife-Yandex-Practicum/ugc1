import textwrap


class JsonConfigNotFound(Exception):
    def __init__(self, *args: object) -> None:
        msg = textwrap.dedent(
            """
            json-config-file not found
            Config file must be in event_etl/data/clickhouse_tables.json
            """
        )

        super().__init__(msg, *args)


class InvalidJsonConfig(Exception):
    def __init__(self, *args: object) -> None:
        msg = textwrap.dedent(
            """
            Config file must be like this:
            [
                {
                    "name": "click",
                    "topic": "click",
                    "fields": [
                        {"name": "user_id", "type": "UUID"},
                        {"name": "element", "type": "String"},
                        {"name": "timestamp", "type": "Datetime"}
                    ]
                }
            ]
            """
        )

        super().__init__(msg, *args)
