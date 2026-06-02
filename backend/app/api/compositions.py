from datetime import datetime, timezone
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import Select, insert, select
from sqlalchemy.orm import Session

from app.db.models import drafts, personas, platform_previews, topics
from app.db.session import get_session
from app.schemas import DraftCompositionCreate, DraftCompositionResponse, Platform

router = APIRouter(prefix="/compositions", tags=["compositions"])

PLATFORM_LABELS: dict[Platform, str] = {
    "douyin": "抖音",
    "weibo": "微博",
    "xiaohongshu": "小红书",
}


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def row_dict(row: object) -> dict[str, object]:
    return dict(row)  # type: ignore[arg-type]


def fetch_one(session: Session, statement: Select) -> dict[str, object] | None:
    row = session.execute(statement).mappings().one_or_none()
    if row is None:
        return None
    return row_dict(row)


def metadata_string(metadata: object, key: str) -> str | None:
    if not isinstance(metadata, dict):
        return None
    value = metadata.get(key)
    if isinstance(value, str) and value.strip():
        return value
    return None


def compose_draft_title(topic: dict[str, object], persona: dict[str, object]) -> str:
    return f"{topic['title']}：给{persona['audience']}的 3 步图文方案"


def compose_draft_body(topic: dict[str, object], persona: dict[str, object]) -> str:
    signal = topic.get("signal") or "暂无趋势信号"
    angle = metadata_string(topic.get("raw_metadata"), "angle") or "从问题、步骤、行动建议展开"
    instructions = persona.get("instructions")
    instruction_line = f"补充要求：{instructions}" if instructions else "补充要求：保持结构清晰"

    return "\n".join(
        [
            f"选题：{topic['title']}",
            f"人设：{persona['name']}",
            f"目标受众：{persona['audience']}",
            f"语气：{persona['tone']}",
            instruction_line,
            "",
            "正文：",
            f"先把问题说清楚：{topic['title']}正在被关注，核心信号是{signal}。",
            f"内容角度：{angle}。",
            "1. 先给结论，帮助读者快速判断这条内容是否适合自己。",
            "2. 再拆步骤，每一段只解决一个具体疑问。",
            "3. 最后给行动建议，用一个问题引导评论和复盘。",
            "",
            "结尾互动：你最想先解决哪一个场景？把预算、时间和平台告诉我。",
        ],
    )


def compose_preview(
    *,
    draft_id: UUID,
    platform: Platform,
    topic: dict[str, object],
    persona: dict[str, object],
    now: datetime,
) -> dict[str, object]:
    platform_label = PLATFORM_LABELS[platform]
    title = {
        "douyin": f"{topic['title']}：3 页讲清楚",
        "weibo": f"{topic['title']}运营拆解",
        "xiaohongshu": f"{topic['title']}｜收藏版清单",
    }[platform]
    body = {
        "douyin": "首图给结论，后续卡片拆步骤，结尾用一个问题拉评论。",
        "weibo": "正文先给判断，再展开三条清单，适合配长图或投票问题。",
        "xiaohongshu": "标题强调场景和可收藏性，每页只讲一个重点，降低阅读负担。",
    }[platform]
    hints = {
        "douyin": ["9 图以内", "首图强结论", "评论问题明确"],
        "weibo": ["正文 600 字以内", "话题标签 2 个", "适合长图"],
        "xiaohongshu": ["首图优先", "标题带场景", "标签 5 到 8 个"],
    }[platform]
    cover_note = {
        "douyin": "首图保留标题安全区",
        "weibo": None,
        "xiaohongshu": "主标题放上半区，保留封面关键词",
    }[platform]

    return {
        "id": uuid4(),
        "draft_id": draft_id,
        "platform": platform,
        "title": title,
        "body": f"{body} 人设保持：{persona['name']}。",
        "tags": [str(topic["title"]), platform_label, "内容运营"],
        "cover_note": cover_note,
        "validation_status": "valid",
        "validation_details": {
            "source": "backend_template_composer",
            "topic_id": str(topic["id"]),
            "persona_id": str(persona["id"]),
            "persona_tone": persona["tone"],
        },
        "created_at": now,
        "updated_at": now,
    }


@router.post(
    "/drafts",
    response_model=DraftCompositionResponse,
    status_code=status.HTTP_201_CREATED,
)
def compose_draft(
    payload: DraftCompositionCreate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    topic = fetch_one(session, select(topics).where(topics.c.id == payload.topic_id))
    if topic is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found",
        )

    persona = fetch_one(
        session,
        select(personas).where(
            personas.c.id == payload.persona_id,
            personas.c.is_active.is_(True),
        ),
    )
    if persona is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Active persona not found",
        )

    platforms = list(dict.fromkeys(payload.platforms))
    now = utc_now()
    draft_id = uuid4()
    draft = {
        "id": draft_id,
        "topic_id": payload.topic_id,
        "persona_id": payload.persona_id,
        "title": compose_draft_title(topic, persona),
        "body": compose_draft_body(topic, persona),
        "tags": [str(topic["title"]), str(persona["name"]), "自动创作台"],
        "status": "generated",
        "generation_source": "backend_template_composer",
        "created_at": now,
        "updated_at": now,
    }
    previews = [
        compose_preview(
            draft_id=draft_id,
            platform=platform,
            topic=topic,
            persona=persona,
            now=now,
        )
        for platform in platforms
    ]

    session.execute(insert(drafts).values(**draft))
    for preview in previews:
        session.execute(insert(platform_previews).values(**preview))
    session.commit()

    return {"draft": draft, "platform_previews": previews}
