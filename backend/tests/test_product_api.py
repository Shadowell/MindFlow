from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.db.models import metadata
from app.db.session import get_session
from app.main import app


@pytest.fixture()
def client() -> Iterator[TestClient]:
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    metadata.create_all(engine)

    def override_session() -> Iterator[Session]:
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_session
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()
        metadata.drop_all(engine)
        engine.dispose()


def create_draft(client: TestClient) -> str:
    response = client.post(
        "/api/drafts",
        json={
            "title": "3 个适合普通创作者的自动化选题",
            "body": "把热点、人设和排期放在一个工作台里，减少重复劳动。",
            "tags": ["自动化", "内容运营"],
            "status": "generated",
            "generation_source": "manual",
        },
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["title"] == "3 个适合普通创作者的自动化选题"
    assert payload["status"] == "generated"
    assert payload["tags"] == ["自动化", "内容运营"]
    return payload["id"]


def test_draft_create_list_and_detail_roundtrip(client: TestClient) -> None:
    draft_id = create_draft(client)

    list_response = client.get("/api/drafts")
    assert list_response.status_code == 200
    assert [item["id"] for item in list_response.json()["items"]] == [draft_id]

    detail_response = client.get(f"/api/drafts/{draft_id}")
    assert detail_response.status_code == 200
    detail = detail_response.json()
    assert detail["id"] == draft_id
    assert detail["platform_previews"] == []
    assert detail["schedules"] == []
    assert detail["publish_jobs"] == []


def test_preview_upsert_and_schedule_create_publish_jobs(client: TestClient) -> None:
    draft_id = create_draft(client)

    preview_response = client.put(
        f"/api/drafts/{draft_id}/platform-previews/weibo",
        json={
            "title": "自动化选题怎么做",
            "body": "先抓热点，再按人设改写，最后进入排期。",
            "tags": ["自动化", "微博运营"],
            "validation_status": "valid",
            "validation_details": {"characters": 21},
        },
    )
    assert preview_response.status_code == 200
    preview = preview_response.json()
    assert preview["platform"] == "weibo"
    assert preview["validation_status"] == "valid"

    schedule_response = client.post(
        f"/api/drafts/{draft_id}/schedules",
        json={
            "scheduled_for": "2026-06-05T10:30:00+08:00",
            "timezone": "Asia/Shanghai",
            "platforms": ["weibo"],
            "adapter": "manual",
        },
    )
    assert schedule_response.status_code == 201
    scheduled = schedule_response.json()
    assert scheduled["schedule"]["status"] == "scheduled"
    assert len(scheduled["publish_jobs"]) == 1
    assert scheduled["publish_jobs"][0]["platform"] == "weibo"
    assert scheduled["publish_jobs"][0]["adapter"] == "manual"
    assert scheduled["publish_jobs"][0]["status"] == "scheduled"

    detail_response = client.get(f"/api/drafts/{draft_id}")
    detail = detail_response.json()
    assert [preview["platform"] for preview in detail["platform_previews"]] == ["weibo"]
    assert [job["platform"] for job in detail["publish_jobs"]] == ["weibo"]


def test_schedule_requires_saved_preview_for_each_platform(client: TestClient) -> None:
    draft_id = create_draft(client)

    response = client.post(
        f"/api/drafts/{draft_id}/schedules",
        json={
            "scheduled_for": "2026-06-05T10:30:00+08:00",
            "timezone": "Asia/Shanghai",
            "platforms": ["xiaohongshu"],
            "adapter": "manual",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Preview is required before scheduling platform: xiaohongshu"
    )
