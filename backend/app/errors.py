from http import HTTPStatus
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.request_context import current_request_id


def _error_payload(code: str, message: str, details: Any = None) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "error": {"code": code, "message": message},
        "request_id": current_request_id(),
    }
    if details is not None:
        payload["error"]["details"] = details
    return payload


def _field_path(loc: Any) -> str:
    if not isinstance(loc, (list, tuple)):
        return str(loc)
    return ".".join(str(part) for part in loc)


def _field_error_code(error_type: str) -> str:
    if error_type == "missing":
        return "FIELD_REQUIRED"
    if "too_short" in error_type or "min_length" in error_type:
        return "FIELD_TOO_SHORT"
    if "too_long" in error_type or "max_length" in error_type:
        return "FIELD_TOO_LONG"
    if "type" in error_type:
        return "FIELD_TYPE_INVALID"
    return "FIELD_INVALID"


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    detail = exc.detail
    if isinstance(detail, dict):
        code = str(detail.get("code", HTTPStatus(exc.status_code).name))
        message = str(detail.get("message", HTTPStatus(exc.status_code).phrase))
        details = detail.get("details")
    else:
        code = str(detail)
        message = HTTPStatus(exc.status_code).phrase
        details = None
    return JSONResponse(status_code=exc.status_code, content=_error_payload(code, message, details), headers=exc.headers)


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    raw_errors = exc.errors()
    field_errors = [
        {
            "field": _field_path(error.get("loc", "")),
            "code": _field_error_code(str(error.get("type", ""))),
            "message": str(error.get("msg", "Invalid field")),
        }
        for error in raw_errors
    ]
    return JSONResponse(
        status_code=422,
        content=_error_payload(
            "VALIDATION_ERROR",
            "Request validation failed",
            {"field_errors": field_errors, "raw_errors": raw_errors},
        ),
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content=_error_payload("INTERNAL_ERROR", "服务暂时无法完成请求，请稍后重试"),
    )


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
