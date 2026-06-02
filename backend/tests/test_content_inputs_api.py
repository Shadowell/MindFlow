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


def test_create_and_list_topics_newest_first(client: TestClient) -> None:
    older = client.post(
        "/api/topics",
        json={
            "title": "周末轻断舍离清单",
            "source_platform": "weibo",
            "heat_score": 82,
            "signal": "互动问题明确",
            "discovered_at": "2026-06-01T10:00:00Z",
        },
    )
    newer = client.post(
        "/api/topics",
        json={
            "title": "低成本通勤穿搭",
            "source_platform": "xiaohongshu",
            "heat_score": 96,
            "signal": "收藏率高",
            "raw_metadata": {"source": "manual-test"},
            "discovered_at": "2026-06-02T10:00:00Z",
        },
    )

    assert older.status_code == 201
    assert newer.status_code == 201
    assert newer.json()["raw_metadata"] == {"source": "manual-test"}

    response = client.get("/api/topics")

    assert response.status_code == 200
    assert [item["title"] for item in response.json()["items"]] == [
        "低成本通勤穿搭",
        "周末轻断舍离清单",
    ]


def test_create_personas_and_list_active_only(client: TestClient) -> None:
    active = client.post(
        "/api/personas",
        json={
            "name": "都市效率派",
            "audience": "职场新人、通勤用户",
            "tone": "克制、清楚、像朋友给建议",
            "instructions": "保持结构清晰",
            "is_active": True,
        },
    )
    inactive = client.post(
        "/api/personas",
        json={
            "name": "暂停账号",
            "audience": "旧账号",
            "tone": "不再使用",
            "is_active": False,
        },
    )

    assert active.status_code == 201
    assert inactive.status_code == 201

    response = client.get("/api/personas")

    assert response.status_code == 200
    assert [item["name"] for item in response.json()["items"]] == ["都市效率派"]
    assert response.json()["items"][0]["instructions"] == "保持结构清晰"
