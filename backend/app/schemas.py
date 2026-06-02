from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

Platform = Literal["douyin", "weibo", "xiaohongshu"]
DraftStatus = Literal["draft", "generated", "editing", "ready", "archived"]
PreviewStatus = Literal["draft", "valid", "needs_review", "blocked"]
ScheduleStatus = Literal["scheduled", "cancelled", "completed"]
PublishJobStatus = Literal[
    "scheduled",
    "queued",
    "publishing",
    "published",
    "failed",
    "cancelled",
]


class DraftCreate(BaseModel):
    title: str
    body: str
    tags: list[str] = Field(default_factory=list)
    status: DraftStatus = "draft"
    topic_id: UUID | None = None
    persona_id: UUID | None = None
    generation_source: str | None = None


class TopicCreate(BaseModel):
    title: str
    source_platform: str | None = None
    source_url: str | None = None
    heat_score: int | None = Field(default=None, ge=0, le=100)
    signal: str | None = None
    raw_metadata: dict[str, object] | None = None
    discovered_at: datetime | None = None


class TopicResponse(BaseModel):
    id: UUID
    title: str
    source_platform: str | None
    source_url: str | None
    heat_score: int | None
    signal: str | None
    raw_metadata: dict[str, object] | None
    discovered_at: datetime
    created_at: datetime


class TopicListResponse(BaseModel):
    items: list[TopicResponse]


class PersonaCreate(BaseModel):
    name: str
    audience: str
    tone: str
    instructions: str | None = None
    is_active: bool = True


class PersonaResponse(BaseModel):
    id: UUID
    name: str
    audience: str
    tone: str
    instructions: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime


class PersonaListResponse(BaseModel):
    items: list[PersonaResponse]


class DraftResponse(BaseModel):
    id: UUID
    topic_id: UUID | None
    persona_id: UUID | None
    title: str
    body: str
    tags: list[str]
    status: DraftStatus
    generation_source: str | None
    created_at: datetime
    updated_at: datetime


class DraftListResponse(BaseModel):
    items: list[DraftResponse]


class PlatformPreviewUpsert(BaseModel):
    title: str | None = None
    body: str
    tags: list[str] = Field(default_factory=list)
    cover_note: str | None = None
    validation_status: PreviewStatus = "draft"
    validation_details: dict[str, object] | None = None


class PlatformPreviewResponse(BaseModel):
    id: UUID
    draft_id: UUID
    platform: Platform
    title: str | None
    body: str
    tags: list[str]
    cover_note: str | None
    validation_status: PreviewStatus
    validation_details: dict[str, object] | None
    created_at: datetime
    updated_at: datetime


class ScheduleCreate(BaseModel):
    scheduled_for: datetime
    timezone: str
    platforms: list[Platform]
    adapter: str = "manual"


class ScheduleResponse(BaseModel):
    id: UUID
    draft_id: UUID
    scheduled_for: datetime
    timezone: str
    status: ScheduleStatus
    created_at: datetime
    updated_at: datetime


class PublishJobResponse(BaseModel):
    id: UUID
    draft_id: UUID
    platform_preview_id: UUID
    schedule_id: UUID | None
    platform: Platform
    status: PublishJobStatus
    adapter: str
    scheduled_for: datetime | None
    legacy_task_id: str | None
    retry_count: int
    max_retries: int
    last_error: str | None
    adapter_payload: dict[str, object] | None
    queued_at: datetime | None
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime
    updated_at: datetime


class ScheduleCreateResponse(BaseModel):
    schedule: ScheduleResponse
    publish_jobs: list[PublishJobResponse]


class DraftDetailResponse(DraftResponse):
    platform_previews: list[PlatformPreviewResponse]
    schedules: list[ScheduleResponse]
    publish_jobs: list[PublishJobResponse]
