from collections.abc import Iterator
from functools import lru_cache

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from app.settings import BackendSettings


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    database_url = BackendSettings().require_database_url()
    return create_engine(database_url, pool_pre_ping=True)


def get_session() -> Iterator[Session]:
    with Session(get_engine()) as session:
        yield session
