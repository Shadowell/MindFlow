"""Create MindFlow MVP schema.

Revision ID: 20260602_0001
Revises: None
Create Date: 2026-06-02 00:00:00
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "20260602_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")

    op.create_table(
        "topics",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("source_platform", sa.Text(), nullable=True),
        sa.Column("source_url", sa.Text(), nullable=True),
        sa.Column("heat_score", sa.Integer(), nullable=True),
        sa.Column("signal", sa.Text(), nullable=True),
        sa.Column("raw_metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("discovered_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint(
            "heat_score is null or (heat_score >= 0 and heat_score <= 100)",
            name="topics_heat_score_check",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("topics_discovered_at_idx", "topics", [sa.text("discovered_at DESC")])

    op.create_table(
        "personas",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("audience", sa.Text(), nullable=False),
        sa.Column("tone", sa.Text(), nullable=False),
        sa.Column("instructions", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("personas_name_unique", "personas", ["name"], unique=True)
    op.create_index("personas_active_idx", "personas", ["is_active"])

    op.create_table(
        "drafts",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("topic_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("persona_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("tags", postgresql.ARRAY(sa.Text()), server_default=sa.text("'{}'::text[]"), nullable=False),
        sa.Column("status", sa.Text(), server_default=sa.text("'draft'"), nullable=False),
        sa.Column("generation_source", sa.Text(), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint(
            "status in ('draft', 'generated', 'editing', 'ready', 'archived')",
            name="drafts_status_check",
        ),
        sa.ForeignKeyConstraint(["persona_id"], ["personas.id"], name="drafts_persona_id_fkey", ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["topic_id"], ["topics.id"], name="drafts_topic_id_fkey", ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("drafts_updated_at_idx", "drafts", [sa.text("updated_at DESC")])
    op.create_index("drafts_status_idx", "drafts", ["status"])

    op.create_table(
        "draft_assets",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("draft_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("asset_type", sa.Text(), nullable=False),
        sa.Column("source_url", sa.Text(), nullable=True),
        sa.Column("local_path", sa.Text(), nullable=True),
        sa.Column("alt_text", sa.Text(), nullable=True),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.Column("status", sa.Text(), server_default=sa.text("'pending'"), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("status in ('pending', 'ready', 'failed')", name="draft_assets_status_check"),
        sa.CheckConstraint(
            "status <> 'ready' or source_url is not null or local_path is not null",
            name="draft_assets_ready_source_check",
        ),
        sa.ForeignKeyConstraint(["draft_id"], ["drafts.id"], name="draft_assets_draft_id_fkey", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("draft_assets_draft_sort_unique", "draft_assets", ["draft_id", "sort_order"], unique=True)
    op.create_index("draft_assets_draft_id_idx", "draft_assets", ["draft_id"])

    op.create_table(
        "platform_accounts",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("platform", sa.Text(), nullable=False),
        sa.Column("display_name", sa.Text(), nullable=False),
        sa.Column("external_account_id", sa.Text(), nullable=True),
        sa.Column("connection_status", sa.Text(), server_default=sa.text("'not_connected'"), nullable=False),
        sa.Column("last_checked_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("platform in ('douyin', 'weibo', 'xiaohongshu')", name="platform_accounts_platform_check"),
        sa.CheckConstraint(
            "connection_status in ('not_connected', 'connected', 'expired', 'disabled')",
            name="platform_accounts_connection_status_check",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "platform_accounts_platform_external_unique",
        "platform_accounts",
        ["platform", "external_account_id"],
        unique=True,
        postgresql_where=sa.text("external_account_id is not null"),
    )
    op.create_index(
        "platform_accounts_platform_status_idx",
        "platform_accounts",
        ["platform", "connection_status"],
    )

    op.create_table(
        "platform_previews",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("draft_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("platform", sa.Text(), nullable=False),
        sa.Column("title", sa.Text(), nullable=True),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("tags", postgresql.ARRAY(sa.Text()), server_default=sa.text("'{}'::text[]"), nullable=False),
        sa.Column("cover_note", sa.Text(), nullable=True),
        sa.Column("validation_status", sa.Text(), server_default=sa.text("'draft'"), nullable=False),
        sa.Column("validation_details", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("platform in ('douyin', 'weibo', 'xiaohongshu')", name="platform_previews_platform_check"),
        sa.CheckConstraint(
            "validation_status in ('draft', 'valid', 'needs_review', 'blocked')",
            name="platform_previews_validation_status_check",
        ),
        sa.ForeignKeyConstraint(["draft_id"], ["drafts.id"], name="platform_previews_draft_id_fkey", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "platform_previews_draft_platform_unique",
        "platform_previews",
        ["draft_id", "platform"],
        unique=True,
    )
    op.create_index(
        "platform_previews_platform_status_idx",
        "platform_previews",
        ["platform", "validation_status"],
    )

    op.create_table(
        "schedules",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("draft_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("scheduled_for", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("timezone", sa.Text(), nullable=False),
        sa.Column("status", sa.Text(), server_default=sa.text("'scheduled'"), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("status in ('scheduled', 'cancelled', 'completed')", name="schedules_status_check"),
        sa.ForeignKeyConstraint(["draft_id"], ["drafts.id"], name="schedules_draft_id_fkey", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("schedules_status_time_idx", "schedules", ["status", "scheduled_for"])

    op.create_table(
        "publish_jobs",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("draft_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("platform_preview_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("schedule_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("platform_account_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("platform", sa.Text(), nullable=False),
        sa.Column("status", sa.Text(), server_default=sa.text("'scheduled'"), nullable=False),
        sa.Column("adapter", sa.Text(), nullable=False),
        sa.Column("scheduled_for", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("legacy_task_id", sa.Text(), nullable=True),
        sa.Column("retry_count", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column("max_retries", sa.Integer(), server_default=sa.text("3"), nullable=False),
        sa.Column("last_error", sa.Text(), nullable=True),
        sa.Column("adapter_payload", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("queued_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("started_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("completed_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("platform in ('douyin', 'weibo', 'xiaohongshu')", name="publish_jobs_platform_check"),
        sa.CheckConstraint(
            "status in ('scheduled', 'queued', 'publishing', 'published', 'failed', 'cancelled')",
            name="publish_jobs_status_check",
        ),
        sa.CheckConstraint("retry_count >= 0", name="publish_jobs_retry_count_check"),
        sa.CheckConstraint("max_retries >= 0", name="publish_jobs_max_retries_check"),
        sa.CheckConstraint(
            "status not in ('published', 'failed', 'cancelled') or completed_at is not null",
            name="publish_jobs_completed_status_check",
        ),
        sa.ForeignKeyConstraint(["draft_id"], ["drafts.id"], name="publish_jobs_draft_id_fkey", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["platform_account_id"],
            ["platform_accounts.id"],
            name="publish_jobs_platform_account_id_fkey",
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["platform_preview_id"],
            ["platform_previews.id"],
            name="publish_jobs_platform_preview_id_fkey",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(["schedule_id"], ["schedules.id"], name="publish_jobs_schedule_id_fkey", ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("publish_jobs_status_time_idx", "publish_jobs", ["status", "scheduled_for"])
    op.create_index("publish_jobs_draft_platform_idx", "publish_jobs", ["draft_id", "platform"])
    op.create_index(
        "publish_jobs_legacy_task_id_idx",
        "publish_jobs",
        ["legacy_task_id"],
        postgresql_where=sa.text("legacy_task_id is not null"),
    )

    op.create_table(
        "publish_job_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("publish_job_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("from_status", sa.Text(), nullable=True),
        sa.Column("to_status", sa.Text(), nullable=False),
        sa.Column("message", sa.Text(), nullable=True),
        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint(
            "from_status is null or from_status in ('scheduled', 'queued', 'publishing', 'published', 'failed', 'cancelled')",
            name="publish_job_events_from_status_check",
        ),
        sa.CheckConstraint(
            "to_status in ('scheduled', 'queued', 'publishing', 'published', 'failed', 'cancelled')",
            name="publish_job_events_to_status_check",
        ),
        sa.ForeignKeyConstraint(
            ["publish_job_id"],
            ["publish_jobs.id"],
            name="publish_job_events_publish_job_id_fkey",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("publish_job_events_job_time_idx", "publish_job_events", ["publish_job_id", "created_at"])


def downgrade() -> None:
    op.drop_index("publish_job_events_job_time_idx", table_name="publish_job_events")
    op.drop_table("publish_job_events")
    op.drop_index("publish_jobs_legacy_task_id_idx", table_name="publish_jobs")
    op.drop_index("publish_jobs_draft_platform_idx", table_name="publish_jobs")
    op.drop_index("publish_jobs_status_time_idx", table_name="publish_jobs")
    op.drop_table("publish_jobs")
    op.drop_index("schedules_status_time_idx", table_name="schedules")
    op.drop_table("schedules")
    op.drop_index("platform_previews_platform_status_idx", table_name="platform_previews")
    op.drop_index("platform_previews_draft_platform_unique", table_name="platform_previews")
    op.drop_table("platform_previews")
    op.drop_index("platform_accounts_platform_status_idx", table_name="platform_accounts")
    op.drop_index("platform_accounts_platform_external_unique", table_name="platform_accounts")
    op.drop_table("platform_accounts")
    op.drop_index("draft_assets_draft_id_idx", table_name="draft_assets")
    op.drop_index("draft_assets_draft_sort_unique", table_name="draft_assets")
    op.drop_table("draft_assets")
    op.drop_index("drafts_status_idx", table_name="drafts")
    op.drop_index("drafts_updated_at_idx", table_name="drafts")
    op.drop_table("drafts")
    op.drop_index("personas_active_idx", table_name="personas")
    op.drop_index("personas_name_unique", table_name="personas")
    op.drop_table("personas")
    op.drop_index("topics_discovered_at_idx", table_name="topics")
    op.drop_table("topics")
