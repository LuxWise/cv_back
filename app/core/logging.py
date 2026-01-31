import json
from datetime import datetime
from typing import Optional

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

import httpx
from sqlalchemy.orm import Session

from app.models.logs import Logging
from app.core.database import SessionLocal

def _truncate(s: Optional[str], max_len: int = 8000) -> Optional[str]:
    if s is None:
        return None
    return s if len(s) <= max_len else s[:max_len] + "…(truncated)"

def _headers_to_json(headers) -> str:
    redacted = {}
    for k, v in dict(headers).items():
        lk = k.lower()
        if lk in {"authorization", "cookie", "set-cookie"}:
            redacted[k] = "***"
        else:
            redacted[k] = v
    return json.dumps(redacted, ensure_ascii=False)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        started_at = datetime.utcnow()

        req_body_bytes = await request.body()
        req_body = _truncate(req_body_bytes.decode("utf-8", errors="replace"))

        response = await call_next(request)

        resp_body_bytes = b""
        async for chunk in response.body_iterator:
            resp_body_bytes += chunk

        resp_body = _truncate(resp_body_bytes.decode("utf-8", errors="replace"))

        new_response = Response(
            content=resp_body_bytes,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
        )

        db: Session = SessionLocal()

        try:
            log_entry = Logging(
                level="INFO",
                operation=f"{request.method} {request.url.path}",
                message="Inbound HTTP request",
                http_method=request.method,
                http_url=str(request.url),
                requestHeaders=_headers_to_json(request.headers),
                requestBody=req_body,
                requestStatus=response.status_code,
                responseHeaders=_headers_to_json(response.headers),
                responseBody=resp_body,
                requestTime=started_at,
            )
            db.add(log_entry)
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"Logging failed: {e}")
        finally:
            db.close()
        
        return new_response


def outboundLogging(db: Session, operation: str = "Outbound request"):
    async def on_request(request: httpx.Request):
        request.extensions["started_at"] = datetime.utcnow()

        # Guardamos el request en extensions para usarlo en on_response
        request.extensions["logged_headers"] = _headers_to_json(request.headers)
        if request.content:
            body = request.content.decode("utf-8", errors="replace") if isinstance(request.content, (bytes, bytearray)) else str(request.content)
            request.extensions["logged_body"] = _truncate(body)
        else:
            request.extensions["logged_body"] = None

    async def on_response(response: httpx.Response):
        started_at = response.request.extensions.get("started_at")
        req_headers = response.request.extensions.get("logged_headers")
        req_body = response.request.extensions.get("logged_body")

        resp_text = None
        try:
            # Nota: leer text aquí puede cargar todo en memoria; truncamos
            resp_text = _truncate(response.text)
        except Exception:
            resp_text = None

        log_entry = Logging(
            level="INFO" if response.status_code < 400 else "ERROR",
            operation=operation,
            message="Outbound request",
            http_method=response.request.method,
            http_url=str(response.request.url),
            requestHeaders=req_headers,
            requestBody=req_body,
            requestStatus=response.status_code,
            responseHeaders=_headers_to_json(response.headers),
            responseBody=resp_text,
            requestTime=started_at,
        )
        db.add(log_entry)
        db.commit()

    return httpx.AsyncClient(
        event_hooks={"request": [on_request], "response": [on_response]},
    )