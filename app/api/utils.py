import string
import random

from fastapi import Request

from api.repository import SqlAlchemyRepository


def get_user_ip(request: Request) -> str:
    return request.client.host


def get_short_url(db_con: SqlAlchemyRepository) -> str:
    hash = string.ascii_uppercase + string.ascii_lowercase + string.digits
    shorturl = ''.join(random.sample(hash, 8))
    while db_con.get({'shorturl': shorturl}):
        shorturl = ''.join(random.sample(hash, 8))

    return shorturl
