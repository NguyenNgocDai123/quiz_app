import json
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import StreamingResponse, FileResponse, HTMLResponse

from app.common.response import AppResponseModel, BusinessJsonResponse
from app.constants.business_code import BusinessCode


class ResponseWrapperMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Bỏ qua các response đặc biệt
        if isinstance(response,
                      (FileResponse, StreamingResponse, HTMLResponse)):
            return response

        # Đọc body gốc
        body = b"".join([chunk async for chunk in response.body_iterator])
        response.body_iterator = None

        try:
            data = json.loads(body.decode())
        except Exception:
            data = body.decode() if body else None

        # Nếu đã đúng format chuẩn thì trả về luôn
        if isinstance(data, dict) and {"business_code",
                                       "status_code",
                                       "message", "data"} <= data.keys():
            response.body_iterator = iter([body])
            return response

        # Nếu chưa chuẩn → bọc lại
        wrapped = AppResponseModel(
            business_code=BusinessCode.SUCCESS,
            status_code=response.status_code,
            message="OK",
            data=data,
        ).model_dump()

        return BusinessJsonResponse(
            business_code=BusinessCode.SUCCESS,
            content=wrapped,
            status_code=response.status_code,
        )
