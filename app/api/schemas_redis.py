from redis_om import HashModel

from api.config import redis_db


class Task(HashModel):
    longurl: str
    shorturl: str

    class Meta:
        database: redis_db
