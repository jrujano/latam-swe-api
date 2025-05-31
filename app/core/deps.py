from typing import Generator
from app.db.session import Session


def get_db() -> Generator:
    db = Session()
    db.current_user_id = None
    try:
        yield db
    finally:
        db.close()
