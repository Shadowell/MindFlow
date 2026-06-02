from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends, status
from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from app.db.models import personas, topics
from app.db.session import get_session
from app.schemas import (
    PersonaCreate,
    PersonaListResponse,
    PersonaResponse,
    TopicCreate,
    TopicListResponse,
    TopicResponse,
)

router = APIRouter(tags=["content-inputs"])


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def row_dict(row: object) -> dict[str, object]:
    return dict(row)  # type: ignore[arg-type]


@router.post("/topics", response_model=TopicResponse, status_code=status.HTTP_201_CREATED)
def create_topic(payload: TopicCreate, session: Session = Depends(get_session)) -> dict[str, object]:
    now = utc_now()
    topic = {
        "id": uuid4(),
        "title": payload.title,
        "source_platform": payload.source_platform,
        "source_url": payload.source_url,
        "heat_score": payload.heat_score,
        "signal": payload.signal,
        "raw_metadata": payload.raw_metadata,
        "discovered_at": payload.discovered_at or now,
        "created_at": now,
    }
    session.execute(insert(topics).values(**topic))
    session.commit()
    return topic


@router.get("/topics", response_model=TopicListResponse)
def list_topics(session: Session = Depends(get_session)) -> dict[str, list[dict[str, object]]]:
    rows = session.execute(
        select(topics).order_by(topics.c.discovered_at.desc(), topics.c.created_at.desc())
    ).mappings()
    return {"items": [row_dict(row) for row in rows]}


@router.post(
    "/personas",
    response_model=PersonaResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_persona(payload: PersonaCreate, session: Session = Depends(get_session)) -> dict[str, object]:
    now = utc_now()
    persona = {
        "id": uuid4(),
        "name": payload.name,
        "audience": payload.audience,
        "tone": payload.tone,
        "instructions": payload.instructions,
        "is_active": payload.is_active,
        "created_at": now,
        "updated_at": now,
    }
    session.execute(insert(personas).values(**persona))
    session.commit()
    return persona


@router.get("/personas", response_model=PersonaListResponse)
def list_personas(session: Session = Depends(get_session)) -> dict[str, list[dict[str, object]]]:
    rows = session.execute(
        select(personas)
        .where(personas.c.is_active.is_(True))
        .order_by(personas.c.created_at.desc())
    ).mappings()
    return {"items": [row_dict(row) for row in rows]}
