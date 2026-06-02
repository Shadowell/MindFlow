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


def create_topic(client: TestClient) -> dict[str, object]:
    response = client.post(
        "/api/topics",
        json={
            "title": "低成本通勤穿搭",
            "source_platform": "xiaohongshu",
            "heat_score": 96,
            "signal": "收藏率高，评论集中在预算和显瘦",
            "raw_metadata": {"angle": "用 3 套搭配解决一周通勤"},
            "discovered_at": "2026-06-02T10:00:00Z",
        },
    )
    assert response.status_code == 201
    return response.json()


def create_persona(client: TestClient, *, is_active: bool = True) -> dict[str, object]:
    response = client.post(
        "/api/personas",
        json={
            "name": "都市效率派" if is_active else "暂停人设",
            "audience": "职场新人、通勤用户",
            "tone": "克制、清楚、像朋友给建议",
            "instructions": "保持结构清晰",
            "is_active": is_active,
        },
    )
    assert response.status_code == 201
    return response.json()


def test_compose_draft_from_topic_and_persona(client: TestClient) -> None:
    topic = create_topic(client)
    persona = create_persona(client)

    response = client.post(
        "/api/compositions/drafts",
        json={
            "topic_id": topic["id"],
            "persona_id": persona["id"],
            "platforms": ["douyin", "weibo", "xiaohongshu"],
        },
    )

    assert response.status_code == 201
    payload = response.json()
    draft = payload["draft"]
    previews = payload["platform_previews"]

    assert draft["topic_id"] == topic["id"]
    assert draft["persona_id"] == persona["id"]
    assert draft["status"] == "generated"
    assert draft["generation_source"] == "backend_template_composer"
    assert "低成本通勤穿搭" in draft["title"]
    assert "都市效率派" in draft["body"]

    assert [preview["platform"] for preview in previews] == [
        "douyin",
        "weibo",
        "xiaohongshu",
    ]
    assert all(
        preview["validation_details"]["source"] == "backend_template_composer"
        for preview in previews
    )

    detail_response = client.get(f"/api/drafts/{draft['id']}")

    assert detail_response.status_code == 200
    assert len(detail_response.json()["platform_previews"]) == 3


def test_compose_draft_rejects_inactive_persona(client: TestClient) -> None:
    topic = create_topic(client)
    persona = create_persona(client, is_active=False)

    response = client.post(
        "/api/compositions/drafts",
        json={
            "topic_id": topic["id"],
            "persona_id": persona["id"],
            "platforms": ["weibo"],
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Active persona not found"
