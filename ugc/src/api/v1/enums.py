from enum import Enum


class KafkaTopicsEnum(str, Enum):
    click_topic: str = 'click'
    page_view_topic: str = 'page_view'
    video_resolution_change_topic: str = 'video_resolution_change'
    search_filter_use_topic: str = 'search_filter_use'
    video_finish_schema_topic: str = 'video_finish_schema'
