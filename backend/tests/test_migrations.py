import subprocess
from pathlib import Path


def test_alembic_renders_initial_migration_offline() -> None:
    backend_dir = Path(__file__).resolve().parents[1]

    result = subprocess.run(
        [
            "python3",
            "-m",
            "alembic",
            "-c",
            str(backend_dir / "alembic.ini"),
            "upgrade",
            "head",
            "--sql",
        ],
        cwd=backend_dir,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert "CREATE TABLE topics" in result.stdout
    assert "CREATE TABLE publish_jobs" in result.stdout
    assert "publish_jobs_legacy_task_id_idx" in result.stdout
