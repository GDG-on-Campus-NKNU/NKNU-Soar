from _contextvars import ContextVar
from contextlib import contextmanager

from soar.config import DB_PATH
from soar.modules.database.database_interface import DatabaseInterface
from soar.modules.database.sqlite import SqliteDatabase

_db_context: ContextVar[DatabaseInterface | None] = ContextVar("db_context", default=None)


def __create_db_handler() -> DatabaseInterface:
    return SqliteDatabase(DB_PATH)


@contextmanager
def _get_db_handler():
    db = __create_db_handler()
    _db_context.set(db)

    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.disconnect()
        _clear_db_context()


def get_db_context() -> DatabaseInterface:
    db = _db_context.get()
    if db is None:
        raise RuntimeError("No database context available")
    return db


def _clear_db_context():
    _db_context.set(None)
