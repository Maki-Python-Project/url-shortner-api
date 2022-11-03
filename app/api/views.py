import os
from operator import itemgetter

from api import schemas
from api.config import get_redis
from api.database import database, engine, metadata
from api.repository import SqlAlchemyRepository
from api.utils import get_short_url, get_user_ip
from fastapi import Depends, FastAPI, Request
from fastapi.responses import RedirectResponse

application = FastAPI()
SHORTENED_URLS = f"{os.environ.get('HOST_URL')}shorten/"
metadata.create_all(engine)


@application.get("/task")
async def all(redis_db=Depends(get_redis)):
    result_list = []
    for key in redis_db.scan_iter():
        value = redis_db.get(key)
        result_list.append({key: value})
    return result_list


@application.post("/task")
async def create(longurl: str, request: Request, redis_db=Depends(get_redis)):
    db_repo = SqlAlchemyRepository()
    shorturl = await get_short_url(db_repo)
    redis_db.set(longurl, shorturl)
    return {'longurl': longurl, 'shorturl': shorturl}


@application.on_event('startup')
async def startup():
    await database.connect()


@application.on_event('shutdown')
async def shutdown():
    await database.disconnect()


@application.post('/shorten/', response_model=schemas.UrlShortener)
async def create_shorturl(url: schemas.UrlShortenerCreate, request: Request):
    db_repo = SqlAlchemyRepository()
    longurl = url.longurl

    ip = get_user_ip(request)

    long_url_obj = await db_repo.get_by_longurl_and_ip(longurl, ip)

    if long_url_obj:
        long_url_obj.shorturl = SHORTENED_URLS + long_url_obj.shorturl
        return long_url_obj

    shorturl = await get_short_url(db_repo)

    shortened_url_obj = schemas.UrlShortenerInsert(longurl=longurl, shorturl=shorturl, user_ip_address=ip)
    shortened_url_obj = await db_repo.add(shortened_url_obj)
    shortened_url_obj['shorturl'] = SHORTENED_URLS + shortened_url_obj['shorturl']
    return shortened_url_obj


@application.get('/shorten/{shorturl}')
async def redirect_shorturl(shorturl: str) -> RedirectResponse:
    db_connection = SqlAlchemyRepository()
    redirect_link = await db_connection.get_by_shorturl(shorturl)
    return RedirectResponse(url=redirect_link.longurl, status_code=301)


@application.get('/the-most-popular/')
async def get_the_most_popular():
    db_connection = SqlAlchemyRepository()
    data = await db_connection.annotate({})
    most_popular_list = sorted(data, key=itemgetter('count_1'))
    return most_popular_list[::-1]


@application.get('/shortened-urls-count/')
async def get_count_all_shortened_url():
    db_connection = SqlAlchemyRepository()
    count = await db_connection.count()
    return {'count': count}
