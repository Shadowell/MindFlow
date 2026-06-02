from sqlalchemy import CheckConstraint, ForeignKeyConstraint, Index

from app.db.models import metadata


def test_metadata_includes_sprint_08_tables() -> None:
    assert set(metadata.tables) == {
        "draft_assets",
        "drafts",
        "personas",
        "platform_accounts",
        "platform_previews",
        "publish_job_events",
        "publish_jobs",
        "schedules",
        "topics",
    }


def test_drafts_table_has_status_constraint_and_recent_indexes() -> None:
    drafts = metadata.tables["drafts"]

    check_sql = {
        str(constraint.sqltext)
        for constraint in drafts.constraints
        if isinstance(constraint, CheckConstraint)
    }
    index_names = {index.name for index in drafts.indexes}

    assert "status in ('draft', 'generated', 'editing', 'ready', 'archived')" in check_sql
    assert "drafts_status_idx" in index_names
    assert "drafts_updated_at_idx" in index_names


def test_platform_preview_is_unique_per_draft_and_platform() -> None:
    previews = metadata.tables["platform_previews"]

    unique_indexes = {
        index.name: [column.name for column in index.columns]
        for index in previews.indexes
        if isinstance(index, Index) and index.unique
    }

    assert unique_indexes["platform_previews_draft_platform_unique"] == [
        "draft_id",
        "platform",
    ]


def test_publish_jobs_has_core_relationships_and_autorepost_lookup_index() -> None:
    publish_jobs = metadata.tables["publish_jobs"]

    foreign_keys = {
        constraint.name: [column.name for column in constraint.columns]
        for constraint in publish_jobs.constraints
        if isinstance(constraint, ForeignKeyConstraint)
    }
    index_names = {index.name for index in publish_jobs.indexes}

    assert foreign_keys["publish_jobs_draft_id_fkey"] == ["draft_id"]
    assert foreign_keys["publish_jobs_platform_preview_id_fkey"] == [
        "platform_preview_id"
    ]
    assert foreign_keys["publish_jobs_schedule_id_fkey"] == ["schedule_id"]
    assert foreign_keys["publish_jobs_platform_account_id_fkey"] == [
        "platform_account_id"
    ]
    assert "publish_jobs_status_time_idx" in index_names
    assert "publish_jobs_draft_platform_idx" in index_names
    assert "publish_jobs_legacy_task_id_idx" in index_names
