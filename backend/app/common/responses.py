from typing import Any, Optional

from pydantic import BaseModel


class SuccessResponse(BaseModel):
    success: bool = True
    message: str = "OK"
    data: Optional[Any] = None


def ok(data: Any = None, message: str = "OK") -> dict:
    return {"success": True, "message": message, "data": data}
