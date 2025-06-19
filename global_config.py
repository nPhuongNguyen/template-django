from dataclasses import dataclass
from typing import Any



# Định nghĩa class ModelError sử dụng dataclass
@dataclass
class ModelError:
    status: int
    msg: str
    detail: Any = None

class ErrorCodes:
    # Lỗi chung (Common Errors)
    SUCCESS = ModelError(1, "Ok")
    APP_SUCCESS = ModelError(0, "Ok")
    DB_FAILED = ModelError(300, "Chưa hiển thị được thông tin, vui lòng thử lại sau.")
    INVALID_INPUT = ModelError(400, "Chưa hiển thị được thông tin, vui lòng thử lại sau.")
    SYSTEM_BUSY = ModelError(800, "Chưa hiển thị được thông tin, vui lòng thử lại sau.")
    SYSTEM_ERROR = ModelError(500, "Chưa hiển thị được thông tin, vui lòng thử lại sau.")
    # Lỗi liên quan đến người dùng (User-related Errors)
    TOKEN_REQUIRED = ModelError(1000, "Token không tồn tại")
    TOKEN_EXPIRED = ModelError(1001, "Token hết hạn")
    TOKEN_INVALID_TOKEN = ModelError(1002, "Token không hợp lệ")
    TOKEN_APP_ERROR = ModelError(1040, "unauthorized")

def web_resp(error: ModelError, detail: Any = None) -> dict:
    return {
        "status": error.status,
        "msg": error.msg,
        "detail": detail if detail is not None else error.detail
    }

def local_resp(error: ModelError, detail: Any = None) -> dict:
    return {
        "statusCode": error.status,
        "message": error.msg,
        "data": detail if detail is not None else error.detail
    }