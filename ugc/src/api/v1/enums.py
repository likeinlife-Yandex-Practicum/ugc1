from enum import Enum


class KafkaTopic(str, Enum):
    click: str = "click"
    page: str = "page_view"
    video_resolution_change: str = "video_resolution_change"
    search_filter_use: str = "search_filter_use"
    video_finish: str = "video_finish"
