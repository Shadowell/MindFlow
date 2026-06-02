from fastapi import FastAPI

from app.api.drafts import router as drafts_router

app = FastAPI(title="MindFlow Backend")
app.include_router(drafts_router, prefix="/api")


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "service": "mindflow-backend",
        "status": "ok",
    }
