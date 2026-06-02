from sqlalchemy import (
    ARRAY,
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKeyConstraint,
    Index,
    Integer,
    JSON,
    MetaData,
    Table,
    Text,
    Uuid,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID

metadata = MetaData()


def uuid_type() -> Uuid:
    return Uuid(as_uuid=True).with_variant(UUID(as_uuid=True), "postgresql")


def json_type() -> JSON:
    return JSON().with_variant(JSONB(), "postgresql")


def tags_type() -> JSON:
    return JSON().with_variant(ARRAY(Text), "postgresql")


timestamp_type = DateTime(timezone=True)

topics = Table(
    "topics",
    metadata,
    Column("id", uuid_type(), primary_key=True),
    Column("title", Text, nullable=False),
    Column("source_platform", Text),
    Column("source_url", Text),
    Column("heat_score", Integer),
    Column("signal", Text),
    Column("raw_metadata", json_type()),
    Column("discovered_at", timestamp_type, nullable=False),
    Column("created_at", timestamp_type, nullable=False),
    CheckConstraint(
        "heat_score is null or (heat_score >= 0 and heat_score <= 100)",
        name="topics_heat_score_check",
    ),
)
Index("topics_discovered_at_idx", topics.c.discovered_at.desc())

personas = Table(
    "personas",
    metadata,
    Column("id", uuid_type(), primary_key=True),
    Column("name", Text, nullable=False),
    Column("audience", Text, nullable=False),
    Column("tone", Text, nullable=False),
    Column("instructions", Text),
    Column("is_active", Boolean, nullable=False),
    Column("created_at", timestamp_type, nullable=False),
    Column("updated_at", timestamp_type, nullable=False),
)
Index("personas_name_unique", personas.c.name, unique=True)
Index("personas_active_idx", personas.c.is_active)

drafts = Table(
    "drafts",
    metadata,
    Column("id", uuid_type(), primary_key=True),
    Column("topic_id", uuid_type()),
    Column("persona_id", uuid_type()),
    Column("title", Text, nullable=False),
    Column("body", Text, nullable=False),
    Column("tags", tags_type(), nullable=False),
    Column("status", Text, nullable=False),
    Column("generation_source", Text),
    Column("created_at", timestamp_type, nullable=False),
    Column("updated_at", timestamp_type, nullable=False),
    ForeignKeyConstraint(["topic_id"], ["topics.id"], name="drafts_topic_id_fkey", ondelete="SET NULL"),
    ForeignKeyConstraint(["persona_id"], ["personas.id"], name="drafts_persona_id_fkey", ondelete="SET NULL"),
    CheckConstraint(
        "status in ('draft', 'generated', 'editing', 'ready', 'archived')",
        name="drafts_status_check",
    ),
)
Index("drafts_updated_at_idx", drafts.c.updated_at.desc())
Index("drafts_status_idx", drafts.c.status)

draft_assets = Table(
    "draft_assets",
    metadata,
    Column("id", uuid_type(), primary_key=True),
    Column("draft_id", uuid_type(), nullable=False),
    Column("asset_type", Text, nullable=False),
    Column("source_url", Text),
    Column("local_path", Text),
    Column("alt_text", Text),
    Column("sort_order", Integer, nullable=False),
    Column("status", Text, nullable=False),
    Column("created_at", timestamp_type, nullable=False),
    ForeignKeyConstraint(["draft_id"], ["drafts.id"], name="draft_assets_draft_id_fkey", ondelete="CASCADE"),
    CheckConstraint("status in ('pending', 'ready', 'failed')", name="draft_assets_status_check"),
    CheckConstraint(
        "status <> 'ready' or source_url is not null or local_path is not null",
        name="draft_assets_ready_source_check",
    ),
)
Index("draft_assets_draft_sort_unique", draft_assets.c.draft_id, draft_assets.c.sort_order, unique=True)
Index("draft_assets_draft_id_idx", draft_assets.c.draft_id)

platform_accounts = Table(
    "platform_accounts",
    metadata,
    Column("id", uuid_type(), primary_key=True),
    Column("platform", Text, nullable=False),
    Column("display_name", Text, nullable=False),
    Column("external_account_id", Text),
    Column("connection_status", Text, nullable=False),
    Column("last_checked_at", timestamp_type),
    Column("notes", Text),
    Column("created_at", timestamp_type, nullable=False),
    Column("updated_at", timestamp_type, nullable=False),
    CheckConstraint("platform in ('douyin', 'weibo', 'xiaohongshu')", name="platform_accounts_platform_check"),
    CheckConstraint(
        "connection_status in ('not_connected', 'connected', 'expired', 'disabled')",
        name="platform_accounts_connection_status_check",
    ),
)
Index(
    "platform_accounts_platform_external_unique",
    platform_accounts.c.platform,
    platform_accounts.c.external_account_id,
    unique=True,
    postgresql_where=platform_accounts.c.external_account_id.is_not(None),
)
Index("platform_accounts_platform_status_idx", platform_accounts.c.platform, platform_accounts.c.connection_status)

platform_previews = Table(
    "platform_previews",
    metadata,
    Column("id", uuid_type(), primary_key=True),
    Column("draft_id", uuid_type(), nullable=False),
    Column("platform", Text, nullable=False),
    Column("title", Text),
    Column("body", Text, nullable=False),
    Column("tags", tags_type(), nullable=False),
    Column("cover_note", Text),
    Column("validation_status", Text, nullable=False),
    Column("validation_details", json_type()),
    Column("created_at", timestamp_type, nullable=False),
    Column("updated_at", timestamp_type, nullable=False),
    ForeignKeyConstraint(["draft_id"], ["drafts.id"], name="platform_previews_draft_id_fkey", ondelete="CASCADE"),
    CheckConstraint("platform in ('douyin', 'weibo', 'xiaohongshu')", name="platform_previews_platform_check"),
    CheckConstraint(
        "validation_status in ('draft', 'valid', 'needs_review', 'blocked')",
        name="platform_previews_validation_status_check",
    ),
)
Index("platform_previews_draft_platform_unique", platform_previews.c.draft_id, platform_previews.c.platform, unique=True)
Index("platform_previews_platform_status_idx", platform_previews.c.platform, platform_previews.c.validation_status)

schedules = Table(
    "schedules",
    metadata,
    Column("id", uuid_type(), primary_key=True),
    Column("draft_id", uuid_type(), nullable=False),
    Column("scheduled_for", timestamp_type, nullable=False),
    Column("timezone", Text, nullable=False),
    Column("status", Text, nullable=False),
    Column("created_at", timestamp_type, nullable=False),
    Column("updated_at", timestamp_type, nullable=False),
    ForeignKeyConstraint(["draft_id"], ["drafts.id"], name="schedules_draft_id_fkey", ondelete="CASCADE"),
    CheckConstraint("status in ('scheduled', 'cancelled', 'completed')", name="schedules_status_check"),
)
Index("schedules_status_time_idx", schedules.c.status, schedules.c.scheduled_for)

publish_jobs = Table(
    "publish_jobs",
    metadata,
    Column("id", uuid_type(), primary_key=True),
    Column("draft_id", uuid_type(), nullable=False),
    Column("platform_preview_id", uuid_type(), nullable=False),
    Column("schedule_id", uuid_type()),
    Column("platform_account_id", uuid_type()),
    Column("platform", Text, nullable=False),
    Column("status", Text, nullable=False),
    Column("adapter", Text, nullable=False),
    Column("scheduled_for", timestamp_type),
    Column("legacy_task_id", Text),
    Column("retry_count", Integer, nullable=False),
    Column("max_retries", Integer, nullable=False),
    Column("last_error", Text),
    Column("adapter_payload", json_type()),
    Column("queued_at", timestamp_type),
    Column("started_at", timestamp_type),
    Column("completed_at", timestamp_type),
    Column("created_at", timestamp_type, nullable=False),
    Column("updated_at", timestamp_type, nullable=False),
    ForeignKeyConstraint(["draft_id"], ["drafts.id"], name="publish_jobs_draft_id_fkey", ondelete="CASCADE"),
    ForeignKeyConstraint(
        ["platform_preview_id"],
        ["platform_previews.id"],
        name="publish_jobs_platform_preview_id_fkey",
        ondelete="RESTRICT",
    ),
    ForeignKeyConstraint(["schedule_id"], ["schedules.id"], name="publish_jobs_schedule_id_fkey", ondelete="SET NULL"),
    ForeignKeyConstraint(
        ["platform_account_id"],
        ["platform_accounts.id"],
        name="publish_jobs_platform_account_id_fkey",
        ondelete="SET NULL",
    ),
    CheckConstraint("platform in ('douyin', 'weibo', 'xiaohongshu')", name="publish_jobs_platform_check"),
    CheckConstraint(
        "status in ('scheduled', 'queued', 'publishing', 'published', 'failed', 'cancelled')",
        name="publish_jobs_status_check",
    ),
    CheckConstraint("retry_count >= 0", name="publish_jobs_retry_count_check"),
    CheckConstraint("max_retries >= 0", name="publish_jobs_max_retries_check"),
    CheckConstraint(
        "status not in ('published', 'failed', 'cancelled') or completed_at is not null",
        name="publish_jobs_completed_status_check",
    ),
)
Index("publish_jobs_status_time_idx", publish_jobs.c.status, publish_jobs.c.scheduled_for)
Index("publish_jobs_draft_platform_idx", publish_jobs.c.draft_id, publish_jobs.c.platform)
Index(
    "publish_jobs_legacy_task_id_idx",
    publish_jobs.c.legacy_task_id,
    postgresql_where=publish_jobs.c.legacy_task_id.is_not(None),
)

publish_job_events = Table(
    "publish_job_events",
    metadata,
    Column("id", uuid_type(), primary_key=True),
    Column("publish_job_id", uuid_type(), nullable=False),
    Column("from_status", Text),
    Column("to_status", Text, nullable=False),
    Column("message", Text),
    Column("payload", json_type()),
    Column("created_at", timestamp_type, nullable=False),
    ForeignKeyConstraint(
        ["publish_job_id"],
        ["publish_jobs.id"],
        name="publish_job_events_publish_job_id_fkey",
        ondelete="CASCADE",
    ),
    CheckConstraint(
        "from_status is null or from_status in ('scheduled', 'queued', 'publishing', 'published', 'failed', 'cancelled')",
        name="publish_job_events_from_status_check",
    ),
    CheckConstraint(
        "to_status in ('scheduled', 'queued', 'publishing', 'published', 'failed', 'cancelled')",
        name="publish_job_events_to_status_check",
    ),
)
Index("publish_job_events_job_time_idx", publish_job_events.c.publish_job_id, publish_job_events.c.created_at)
