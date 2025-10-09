
import json
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import StreamingResponse, FileResponse, HTMLResponse

from app.common.response import AppResponseModel, BusinessJsonResponse
from app.constants.business_code import BusinessCode


class ResponseWrapperMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Bỏ qua swagger / openapi / redoc
        if request.url.path.startswith(("/docs", "/openapi.json", "/redoc")):
            return await call_next(request)

        response = await call_next(request)

        # Bỏ qua các response đặc biệt
        if isinstance(response, (FileResponse, StreamingResponse, HTMLResponse)):
            return response

        # Chỉ wrap JSON
        content_type = response.headers.get("content-type", "")
        if "application/json" not in content_type.lower():
            return response

        # Đọc lại body an toàn
        try:
            body_bytes = b""
            if hasattr(response, "body") and response.body:
                body_bytes = response.body
            else:
                body_bytes = b"".join([chunk async for chunk in response.body_iterator])

            data = json.loads(body_bytes.decode()) if body_bytes else None
        except Exception:
            data = None

        # Nếu đã có business_code → giữ nguyên
        if isinstance(data, dict) and "business_code" in data:
            return BusinessJsonResponse(
                business_code=data.get("business_code", BusinessCode.SUCCESS["code"]),
                content=data,
                status_code=response.status_code,
                headers={
                    k: v
                    for k, v in response.headers.items()
                    if k.lower() != "content-length"
                },
            )

        # Nếu chưa chuẩn → wrap lại với SUCCESS
        wrapped = AppResponseModel(
            business_code=BusinessCode.SUCCESS["code"],
            status_code=response.status_code,
            message=BusinessCode.SUCCESS["message"],
            data=data,
        ).model_dump()

        # Luôn tạo response mới, xoá Content-Length cũ
        return BusinessJsonResponse(
            business_code=wrapped["business_code"],
            content=wrapped,
            status_code=response.status_code,
            headers={
                k: v
                for k, v in response.headers.items()
                if k.lower() != "content-length"
            },
        )
