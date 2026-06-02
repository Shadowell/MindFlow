from datetime import datetime, timezone
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import Select, insert, select, update
from sqlalchemy.orm import Session

from app.db.models import drafts, platform_previews, publish_jobs, schedules
from app.db.session import get_session
from app.schemas import (
    DraftCreate,
    DraftDetailResponse,
    DraftListResponse,
    DraftResponse,
    Platform,
    PlatformPreviewResponse,
    PlatformPreviewUpsert,
    PublishJobResponse,
    ScheduleCreate,
    ScheduleCreateResponse,
    ScheduleResponse,
)

router = APIRouter(prefix="/drafts", tags=["drafts"])


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def row_dict(row: object) -> dict[str, object]:
    return dict(row)  # type: ignore[arg-type]


def fetch_one(session: Session, statement: Select) -> dict[str, object] | None:
    row = session.execute(statement).mappings().one_or_none()
    if row is None:
        return None
    return row_dict(row)


def fetch_many(session: Session, statement: Select) -> list[dict[str, object]]:
    return [row_dict(row) for row in session.execute(statement).mappings().all()]


def get_draft_or_404(session: Session, draft_id: UUID) -> dict[str, object]:
    draft = fetch_one(session, select(drafts).where(drafts.c.id == draft_id))
    if draft is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Draft not found",
        )
    return draft


@router.post("", response_model=DraftResponse, status_code=status.HTTP_201_CREATED)
def create_draft(payload: DraftCreate, session: Session = Depends(get_session)) -> dict[str, object]:
    now = utc_now()
    draft = {
        "id": uuid4(),
        "topic_id": payload.topic_id,
        "persona_id": payload.persona_id,
        "title": payload.title,
        "body": payload.body,
        "tags": payload.tags,
        "status": payload.status,
        "generation_source": payload.generation_source,
        "created_at": now,
        "updated_at": now,
    }
    session.execute(insert(drafts).values(**draft))
    session.commit()
    return draft


@router.get("", response_model=DraftListResponse)
def list_drafts(session: Session = Depends(get_session)) -> dict[str, list[dict[str, object]]]:
    items = fetch_many(session, select(drafts).order_by(drafts.c.updated_at.desc()))
    return {"items": items}


@router.get("/{draft_id}", response_model=DraftDetailResponse)
def read_draft(draft_id: UUID, session: Session = Depends(get_session)) -> dict[str, object]:
    draft = get_draft_or_404(session, draft_id)
    draft["platform_previews"] = fetch_many(
        session,
        select(platform_previews)
        .where(platform_previews.c.draft_id == draft_id)
        .order_by(platform_previews.c.platform),
    )
    draft["schedules"] = fetch_many(
        session,
        select(schedules)
        .where(schedules.c.draft_id == draft_id)
        .order_by(schedules.c.scheduled_for.desc()),
    )
    draft["publish_jobs"] = fetch_many(
        session,
        select(publish_jobs)
        .where(publish_jobs.c.draft_id == draft_id)
        .order_by(publish_jobs.c.created_at.desc()),
    )
    return draft


@router.put(
    "/{draft_id}/platform-previews/{platform}",
    response_model=PlatformPreviewResponse,
)
def upsert_platform_preview(
    draft_id: UUID,
    platform: Platform,
    payload: PlatformPreviewUpsert,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    get_draft_or_404(session, draft_id)
    now = utc_now()
    existing = fetch_one(
        session,
        select(platform_previews).where(
            platform_previews.c.draft_id == draft_id,
            platform_previews.c.platform == platform,
        ),
    )
    values = {
        "title": payload.title,
        "body": payload.body,
        "tags": payload.tags,
        "cover_note": payload.cover_note,
        "validation_status": payload.validation_status,
        "validation_details": payload.validation_details,
        "updated_at": now,
    }

    if existing is None:
        preview = {
            "id": uuid4(),
            "draft_id": draft_id,
            "platform": platform,
            "created_at": now,
            **values,
        }
        session.execute(insert(platform_previews).values(**preview))
        session.commit()
        return preview

    session.execute(
        update(platform_previews)
        .where(platform_previews.c.id == existing["id"])
        .values(**values)
    )
    session.commit()
    return fetch_one(
        session, select(platform_previews).where(platform_previews.c.id == existing["id"])
    ) or existing


@router.post(
    "/{draft_id}/schedules",
    response_model=ScheduleCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_schedule(
    draft_id: UUID,
    payload: ScheduleCreate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    get_draft_or_404(session, draft_id)
    preview_rows = fetch_many(
        session,
        select(platform_previews).where(
            platform_previews.c.draft_id == draft_id,
            platform_previews.c.platform.in_(payload.platforms),
        ),
    )
    previews_by_platform = {row["platform"]: row for row in preview_rows}
    for platform in payload.platforms:
        if platform not in previews_by_platform:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Preview is required before scheduling platform: {platform}",
            )

    now = utc_now()
    schedule = {
        "id": uuid4(),
        "draft_id": draft_id,
        "scheduled_for": payload.scheduled_for,
        "timezone": payload.timezone,
        "status": "scheduled",
        "created_at": now,
        "updated_at": now,
    }
    session.execute(insert(schedules).values(**schedule))

    jobs: list[dict[str, object]] = []
    for platform in payload.platforms:
        job = {
            "id": uuid4(),
            "draft_id": draft_id,
            "platform_preview_id": previews_by_platform[platform]["id"],
            "schedule_id": schedule["id"],
            "platform": platform,
            "status": "scheduled",
            "adapter": payload.adapter,
            "scheduled_for": payload.scheduled_for,
            "legacy_task_id": None,
            "retry_count": 0,
            "max_retries": 3,
            "last_error": None,
            "adapter_payload": None,
            "queued_at": None,
            "started_at": None,
            "completed_at": None,
            "created_at": now,
            "updated_at": now,
        }
        session.execute(insert(publish_jobs).values(**job))
        jobs.append(job)

    session.commit()
    return {"schedule": schedule, "publish_jobs": jobs}
