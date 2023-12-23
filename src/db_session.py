import os
import sqlalchemy as sa
import sqlalchemy.ext.declarative as dec
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session


class Base(orm.DeclarativeBase):
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)


SqlAlchemyBase = dec.declarative_base()

__factory = None
print("Инициализация базы данных...")


def global_init():
    global __factory

    if __factory:
        return

    db_engine = "sqlite"
    db_connection = "sqlite:///db.sqlite3?check_same_thread=False"
    engine = sa.create_engine(db_connection)

    print(f"Подключение к базе данных по адресу {db_connection}")

    __factory = orm.sessionmaker(engine, autocommit=False, autoflush=False)

    Base.metadata.create_all(engine)


def get_session() -> Session:
    session = __factory()
    return session
