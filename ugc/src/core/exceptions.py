from http import HTTPStatus


class CustomException(Exception):
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code


JWT_EXPIRED_EXCEPTION = CustomException(
    status_code=HTTPStatus.BAD_REQUEST,
    message="JWT token is expired"
)

JWT_INVALID_EXCEPTION = CustomException(
    status_code=HTTPStatus.BAD_REQUEST,
    message="JWT token is invalid"
)

FILM_ID_EXCEPTION = CustomException(
    status_code=HTTPStatus.BAD_REQUEST,
    message="Film id has incorrect uuid4 format"
)

