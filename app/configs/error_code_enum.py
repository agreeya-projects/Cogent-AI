from enum import Enum


class ErrorCodeEnum(Enum):
    INVALID_INPUT = 100
    INTERNAL_SERVER_ERROR = 500
    UNAUTHORIZED_ACCESS = 401
    RESOURCE_NOT_FOUND = 404
    SUCCESS = 200
    BAD_REQUEST = 400
    RATE_LIMIT_ERROR = 429
    PERMISSION_ERROR = 403
