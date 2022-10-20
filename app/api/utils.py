import random
import string

from django.conf import settings
from django.http import HttpRequest
from pymongo import CursorType, MongoClient

from api.repository import AbstractRepository, MongoRepository


def convert_cursor_to_dict(data: CursorType) -> dict:
    dict_data = {}
    dict_data = {item['_id']: item for item in data}
    return dict_data


def get_user_ip(request: HttpRequest) -> str:
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[-1].strip()
    else:
        return request.META.get('REMOTE_ADDR')


def get_short_url(db_connection: AbstractRepository) -> str:
    hash = string.ascii_uppercase + string.ascii_lowercase + string.digits
    shorturl = ''.join(random.sample(hash, 8))
    while db_connection.get_one({'shorturl': shorturl}) is not None:
        shorturl = ''.join(random.sample(hash, 8))

    return shorturl


def get_db_connection() -> AbstractRepository:
    client = MongoClient('mongodb://mongoadmin:mongoadmin@localhost:27017/')
    db = client['url_test']
    return MongoRepository(db)
