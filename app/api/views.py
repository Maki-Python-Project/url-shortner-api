import os
from operator import itemgetter

from api import schemas
from api.config import get_redis
from api.database import database, engine, metadata
from api.repository import SqlAlchemyRepository
from api.utils import get_short_url, get_user_ip, create_dictionary_key
from fastapi import Depends, FastAPI, Request
from fastapi.responses import RedirectResponse

application = FastAPI()
SHORTENED_URLS = f"{os.environ.get('HOST_URL')}shorten/"
metadata.create_all(engine)


@application.on_event('startup')
async def startup():
    await database.connect()


@application.on_event('shutdown')
async def shutdown():
    await database.disconnect()


@application.post('/shorten/', response_model=schemas.UrlShortener)
async def create_shorturl(url: schemas.UrlShortenerCreate, request: Request, redis_db=Depends(get_redis)):
    db_repo = SqlAlchemyRepository()
    longurl = url.longurl

    ip = get_user_ip(request)

    long_url_obj = await db_repo.get_by_longurl_and_ip(longurl, ip)

    if long_url_obj:
        long_url_obj.shorturl = SHORTENED_URLS + long_url_obj.shorturl
        return long_url_obj

    shorturl = await get_short_url(db_repo)

    redis_db.set(shorturl, create_dictionary_key(ip, longurl))

    shortened_url_obj = schemas.UrlShortenerInsert(longurl=longurl, shorturl=shorturl, user_ip_address=ip)
    shortened_url_obj = await db_repo.add(shortened_url_obj)
    shortened_url_obj['shorturl'] = SHORTENED_URLS + shortened_url_obj['shorturl']
    return shortened_url_obj


@application.get('/shorten/{shorturl}')
async def redirect_shorturl(shorturl: str, redis_db=Depends(get_redis)) -> RedirectResponse:
    if shorturl in redis_db.scan()[1]:
        redirect_link = redis_db.get(shorturl).split('|')[1]
    else:
        db_connection = SqlAlchemyRepository()
        redirect_link = await db_connection.get_by_shorturl(shorturl)
        redirect_link = redirect_link.longurl

    return RedirectResponse(url=redirect_link, status_code=301)


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
