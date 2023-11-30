from aenum import StrEnum, auto

from .settings import settings


class ApiRoute(StrEnum):
    CLICK = auto()
    PAGE_VIEW = auto()
    VIDEO_RESOLUTION_CHANGE = auto()
    SEARCH_FILTER_USE = auto()
    VIDEO_FINISH = auto()


class KafkaTopic(StrEnum):
    CLICK = auto()
    PAGE_VIEW = auto()
    VIDEO_RESOLUTION_CHANGE = auto()
    SEARCH_FILTER_USE = auto()
    VIDEO_FINISH = auto()


class ClickHouseTable(StrEnum):
    CLICK = auto()
    PAGE_VIEW = auto()
    VIDEO_RESOLUTION_CHANGE = auto()
    SEARCH_FILTER_USE = auto()
    VIDEO_FINISH = auto()
