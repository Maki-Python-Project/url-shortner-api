from typing import List

import sqlalchemy
from api.database import database
from api.models import urlshortener
from api.schemas import UrlShortenerInsert
from sqlalchemy import func, select


class AbstractRepository:
    def add(self, reference: dict) -> None:
        raise NotImplementedError

    def get(self, reference: dict) -> sqlalchemy.Table:
        raise NotImplementedError

    def filter(self, reference: dict) -> sqlalchemy.Table:
        raise NotImplementedError

    def annotate(self, reference: dict) -> List[sqlalchemy.Table]:
        raise NotImplementedError

    def count(self, reference: dict) -> List[sqlalchemy.Table]:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    async def add(self, reference: UrlShortenerInsert):
        query = urlshortener.insert().values(
            user_ip_address=reference.user_ip_address, longurl=reference.longurl, shorturl=reference.shorturl
        )
        last_record_id = await database.execute(query)
        return {**reference.dict(), 'id': last_record_id}

    async def get_by_longurl_and_ip(self, longurl: str, user_ip: str):
        query = urlshortener.select().where(
            urlshortener.c.longurl == longurl, urlshortener.c.user_ip_address == user_ip
        )
        return await database.fetch_one(query)

    async def get_by_shorturl(self, shorturl: str):
        query = urlshortener.select().where(urlshortener.c.shorturl == shorturl)
        return await database.fetch_one(query)

    async def annotate(self, reference: dict):
        query = select(urlshortener.c.longurl, func.count(urlshortener.c.id)).group_by(urlshortener.c.longurl)
        return await database.fetch_all(query)

    async def count(self):
        query = select(func.count(urlshortener.c.id))
        return await database.execute(query)
