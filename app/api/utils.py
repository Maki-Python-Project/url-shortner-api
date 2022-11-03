import random
import string

from api.repository import SqlAlchemyRepository
from fastapi import Request


def get_user_ip(request: Request) -> str:
    return request.client.host


async def get_short_url(db_con: SqlAlchemyRepository) -> str:
    hash = string.ascii_uppercase + string.ascii_lowercase + string.digits
    shorturl = ''.join(random.sample(hash, 8))
    while await db_con.get_by_shorturl(shorturl):
        shorturl = ''.join(random.sample(hash, 8))

    return shorturl
