from contextvars import ContextVar


CURRENT_REQUEST_ID: ContextVar[str] = ContextVar("request_id", default="")


def set_request_id(request_id: str):
    return CURRENT_REQUEST_ID.set(request_id)


def reset_request_id(token) -> None:
    CURRENT_REQUEST_ID.reset(token)


def current_request_id() -> str:
    return CURRENT_REQUEST_ID.get()
