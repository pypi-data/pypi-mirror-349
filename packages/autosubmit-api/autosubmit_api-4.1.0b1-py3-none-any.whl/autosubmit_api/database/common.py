import os
from typing import Any
from sqlalchemy import (
    Connection,
    Engine,
    NullPool,
    Select,
    create_engine,
    select,
    text,
    func,
)
from autosubmit_api.builders import BaseBuilder
from autosubmit_api.logger import logger
from autosubmit_api.config.basicConfig import APIBasicConfig


class AttachedDatabaseConnBuilder(BaseBuilder):
    """
    SQLite utility to build attached databases.
    """

    def __init__(self) -> None:
        super().__init__(False)
        APIBasicConfig.read()
        self.engine = create_engine("sqlite://", poolclass=NullPool)
        self._product = self.engine.connect()

    def attach_db(self, path: str, name: str):
        self._product.execute(text(f"attach database '{path}' as {name};"))

    def attach_autosubmit_db(self):
        autosubmit_db_path = os.path.abspath(APIBasicConfig.DB_PATH)
        self.attach_db(autosubmit_db_path, "autosubmit")

    def attach_as_times_db(self):
        as_times_db_path = os.path.join(
            APIBasicConfig.DB_DIR, APIBasicConfig.AS_TIMES_DB
        )
        self.attach_db(as_times_db_path, "as_times")

    @property
    def product(self) -> Connection:
        return super().product


def create_main_db_conn() -> Connection:
    """
    Connection with the autosubmit and as_times DDBB.
    """
    builder = AttachedDatabaseConnBuilder()
    builder.attach_autosubmit_db()
    builder.attach_as_times_db()

    return builder.product


def create_sqlite_db_engine(db_path: str) -> Engine:
    """
    Create an engine for a SQLite DDBB.
    """
    return create_engine(f"sqlite:///{ os.path.abspath(db_path)}", poolclass=NullPool)


def create_autosubmit_db_engine() -> Engine:
    """
    Create an engine for the autosubmit DDBB. Usually named autosubmit.db
    """
    APIBasicConfig.read()
    return create_sqlite_db_engine(APIBasicConfig.DB_PATH)


def create_as_times_db_engine() -> Engine:
    """
    Create an engine for the AS_TIMES DDBB. Usually named as_times.db
    """
    APIBasicConfig.read()
    db_path = os.path.join(APIBasicConfig.DB_DIR, APIBasicConfig.AS_TIMES_DB)
    return create_sqlite_db_engine(db_path)


def execute_with_limit_offset(
    statement: Select[Any], conn: Connection, limit: int = None, offset: int = None
):
    """
    Execute query statement adding limit and offset.
    Also, it returns the total items without applying limit and offset.
    """
    count_stmnt = select(func.count()).select_from(statement.subquery())

    # Add limit and offset
    if offset and offset >= 0:
        statement = statement.offset(offset)
    if limit and limit > 0:
        statement = statement.limit(limit)

    # Execute query
    logger.debug(statement.compile(conn))
    query_result = conn.execute(statement).all()
    logger.debug(count_stmnt.compile(conn))
    total = conn.scalar(count_stmnt)

    return query_result, total
