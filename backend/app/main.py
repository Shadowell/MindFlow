from fastapi import FastAPI

app = FastAPI(title="MindFlow Backend")


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "service": "mindflow-backend",
        "status": "ok",
    }
