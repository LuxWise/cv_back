import json
import httpx
from typing import Any, Iterable
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.core.vault import get_url_groq_service
from app.schemas.generate import CvGenerateAIRequest
from app.services.cv_services import get_cv
from app.models.user import User

def _is_scalar(value: Any) -> bool:
    return value is None or isinstance(value, (str, int, float, bool))


def _flatten(data: Any, prefix: str = "") -> Iterable[tuple[str, str]]:
    if _is_scalar(data):
        if data is None:
            return
        if isinstance(data, str) and not data.strip():
            return
        yield (prefix, str(data))
        return

    if isinstance(data, dict):
        for k, v in data.items():
            key = f"{prefix}.{k}" if prefix else str(k)
            yield from _flatten(v, key)
        return

    if isinstance(data, list):
        for i, item in enumerate(data, start=1):
            key = f"{prefix}[{i}]" if prefix else f"[{i}]"
            yield from _flatten(item, key)
        return

    yield (prefix, str(data))

def _format_data(data: Any) -> str:
    if isinstance(data, str):
        data = json.loads(data)

    parts: list[str] = []
    for key, value in _flatten(data):
        if not key:
            parts.append(value)
        else:
            parts.append(f"{key}: {value}")

    return ", ".join(parts)

def generate_cv(db: Session, user_id: int) -> str | None:
    try:
        cv_data = get_cv(db=db, user_id=user_id)
        if cv_data is None:
            return None

        payload = jsonable_encoder(cv_data)
        return _format_data(payload)

    except Exception as e:
        print(f"Error generating CV: {e}")
        return None
    

def generate_cv_ia(db: Session, user_id: int, job_offer: CvGenerateAIRequest) -> str | None:
    try:
        user = db.query(User).filter(User.id == user_id).first()

        cv_data = get_cv(db=db, user_id=user_id)
        if cv_data is None:
            return None

        payload = jsonable_encoder(cv_data)
        data = _format_data(payload)

        request = httpx.post(
            f"{get_url_groq_service()}/cv/create/external",
            json={
                "userDataPrompt": data,
                "jobOfferPrompt": job_offer.job_offer,
            },
            headers={
                "Content-Type": "application/json",
                "x-token-key": user.api_key
            },
        )

        if request.status_code != 201:
            raise Exception(f"Error generating CV")

        return request.json()

    except Exception as e:
        print(f"Error generating CV: {e}")
        return None