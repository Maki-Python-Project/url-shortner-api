import os

from fastapi import FastAPI
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, RedirectResponse

from api import schemas
from api import models

from api.database import database, engine
from api.repository import SqlAlchemyRepository
from api.utils import get_user_ip, get_short_url


application = FastAPI()
SHORTENED_URLS = f"{os.environ.get('HOST_URL')}shorten/"
models.Base.metadata.create_all(bind=engine)


@application.on_event('startup')
async def startup():
    await database.connect()


@application.on_event('shutdown')
async def shutdown():
    await database.disconnect()


@application.post('/shorten/', response_model=schemas.UrlShortener)
async def create_shorturl(url: schemas.UrlShortenerCreate, request: Request):
    db_repo = SqlAlchemyRepository(database)
    longurl = url.longurl

    ip = get_user_ip(request)

    long_url_obj = await db_repo.get({'longurl': longurl, 'user_ip_address': ip})

    if long_url_obj:
        long_url_obj.shorturl = SHORTENED_URLS + long_url_obj.shorturl
        return long_url_obj

    shorturl = get_short_url(db_repo)

    shortened_url_obj = models.UrlShortener(longurl=longurl, shorturl=shorturl, user_ip_address=ip)
    shortened_url_obj = await db_repo.add(shortened_url_obj)
    shortened_url_obj.shorturl = SHORTENED_URLS + shorturl
    return shortened_url_obj


@application.get('/shorten/{shorturl}')
async def redirect_shorturl(shorturl: str) -> RedirectResponse:
    db_connection = SqlAlchemyRepository(database)
    redirect_link = await db_connection.get({'shorturl': shorturl})
    return RedirectResponse(url=redirect_link.longurl, status_code=301)


@application.get('/the-most-popular/')
async def get_the_most_popular() -> models.UrlShortener:
    db_connection = SqlAlchemyRepository(database)
    data = await db_connection.annotate({})
    result = []
    for pair in data:
        count, url = pair
        r = {"count": count, "url": url}
        result.append(r)

    return result


@application.get('/shortened-urls-count/')
async def get_count_all_shortened_url() -> JSONResponse:
    db_connection = SqlAlchemyRepository(database)
    count = await db_connection.count()
    return JSONResponse(content=jsonable_encoder({'count': count}))
