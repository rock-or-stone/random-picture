import os
import typing
from contextlib import asynccontextmanager

from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import sessionmaker, scoped_session, Query, Mapper
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


def _get_query_cls(mapper, session):
    if mapper:
        m = mapper
        if isinstance(m, tuple):
            m = mapper[0]
        if isinstance(m, Mapper):
            m = m.entity

        try:
            return m.__query_cls__(mapper, session)
        except AttributeError:
            pass

    return Query(mapper, session)


convention = {
    "all_column_names": lambda constraint, table: "_".join(
        [column.name for column in constraint.columns.values()]
    ),
    "ix": "ix__%(table_name)s__%(all_column_names)s",
    "uq": "uq__%(table_name)s__%(all_column_names)s",
    "ck": "ck__%(table_name)s__%(constraint_name)s",
    "fk": ("fk__%(table_name)s__%(all_column_names)s__" "%(referred_table_name)s"),
    "pk": "pk__%(table_name)s",
}

Session = sessionmaker(query_cls=_get_query_cls, class_=AsyncSession)
engine = create_async_engine(os.environ["DB_URL"])
Session.configure(bind=engine)
metadata = MetaData(naming_convention=convention)
current_session = scoped_session(Session)


@as_declarative(metadata=metadata)
class Base:
    def _asdict(self):
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }


@asynccontextmanager
async def session(**kwargs) -> typing.AsyncGenerator[AsyncSession, None]:
    """Обеспечивает транзакционную область для серий операций"""
    new_session = Session(**kwargs)
    try:
        yield new_session
        await new_session.commit()
    except Exception:
        await new_session.rollback()
        raise
    finally:
        await new_session.close()


__all__ = ["Base", "session"]
