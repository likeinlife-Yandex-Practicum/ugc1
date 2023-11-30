from http import HTTPStatus

from fastapi import APIRouter, Depends, Request, Response
from src.api.v1.enums import KafkaTopic
from src.schemas import (
    ClickSchema,
    PageViewSchema,
    SearchFilterUseSchema,
    VideoFinishSchema,
    VideoResolutionChangeSchema,
)
from src.services.jwt_service import JWTService, get_jwt_service
from src.services.ugc import UGCService, get_ugc_service

router = APIRouter()


@router.post("/click", status_code=HTTPStatus.CREATED)
async def register_click(
    request: Request,
    click_schema: ClickSchema = Depends(ClickSchema),
    jwt_service: JWTService = Depends(get_jwt_service),
    ugc_service: UGCService = Depends(get_ugc_service),
) -> Response:
    access_token = request.cookies.get("access_token")
    user_id = jwt_service.get_user_id_from_token(access_token)
    topic = KafkaTopic.click.value
    await ugc_service.add_event_to_kafka(topic, user_id, click_schema)
    return Response(status_code=HTTPStatus.CREATED)


@router.post("/page_view", status_code=HTTPStatus.CREATED)
async def register_page_view(
    request: Request,
    page_view_schema: PageViewSchema = Depends(PageViewSchema),
    jwt_service: JWTService = Depends(get_jwt_service),
    ugc_service: UGCService = Depends(get_ugc_service),
) -> Response:
    access_token = request.cookies.get("access_token")
    user_id = jwt_service.get_user_id_from_token(access_token)
    topic = KafkaTopic.page.value
    await ugc_service.add_event_to_kafka(topic, user_id, page_view_schema)
    return Response(status_code=HTTPStatus.CREATED)


@router.post("/video_resolution_change", status_code=HTTPStatus.CREATED)
async def register_video_resolution_change(
    request: Request,
    video_resolution_change_schema: VideoResolutionChangeSchema = Depends(
        VideoResolutionChangeSchema
    ),
    jwt_service: JWTService = Depends(get_jwt_service),
    ugc_service: UGCService = Depends(get_ugc_service),
) -> Response:
    access_token = request.cookies.get("access_token")
    user_id = jwt_service.get_user_id_from_token(access_token)
    topic = KafkaTopic.video_resolution_change.value
    await ugc_service.add_event_to_kafka(topic, user_id, video_resolution_change_schema)
    return Response(status_code=HTTPStatus.CREATED)


@router.post("/search_filter_use", status_code=HTTPStatus.CREATED)
async def register_search_filter_use(
    request: Request,
    search_filter_use_schema: SearchFilterUseSchema = Depends(SearchFilterUseSchema),
    jwt_service: JWTService = Depends(get_jwt_service),
    ugc_service: UGCService = Depends(get_ugc_service),
) -> Response:
    access_token = request.cookies.get("access_token")
    user_id = jwt_service.get_user_id_from_token(access_token)
    topic = KafkaTopic.search_filter_use.value
    await ugc_service.add_event_to_kafka(topic, user_id, search_filter_use_schema)
    return Response(status_code=HTTPStatus.CREATED)


@router.post("/video_finish", status_code=HTTPStatus.CREATED)
async def register_video_finish(
    request: Request,
    video_finish: VideoFinishSchema = Depends(VideoFinishSchema),
    jwt_service: JWTService = Depends(get_jwt_service),
    ugc_service: UGCService = Depends(get_ugc_service),
) -> Response:
    access_token = request.cookies.get("access_token")
    user_id = jwt_service.get_user_id_from_token(access_token)
    topic = KafkaTopic.video_finish.value
    await ugc_service.add_event_to_kafka(topic, user_id, video_finish)
    return Response(status_code=HTTPStatus.CREATED)
