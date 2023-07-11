# app/db.py

import databases
import ormar
import sqlalchemy

from .config import settings

database = databases.Database(settings.db_url)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class Request(ormar.Model):
    class Meta(BaseMeta):
        tablename = "requests"

    id: int = ormar.Integer(primary_key=True)
    returned_date: str = ormar.String(max_length=128, nullable=False)


engine = sqlalchemy.create_engine(settings.db_url)
metadata.create_all(engine)