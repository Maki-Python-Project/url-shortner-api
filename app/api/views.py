import os

from fastapi import FastAPI
from fastapi import Request, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.orm import Session

from api import schemas
from api import models

from api.database import engine
from api.repository import SqlAlchemyRepository
from api.utils import get_user_ip, get_short_url, get_db_connection


application = FastAPI()
SHORTENED_URLS = f"{os.environ.get('HOST_URL')}shorten/"
models.Base.metadata.create_all(bind=engine)


@application.post('/shorten/', response_model=schemas.UrlShortener)
def create_shorturl(url: schemas.UrlShortenerCreate, request: Request, db: Session = Depends(get_db_connection)):
    db_repo = SqlAlchemyRepository(db)
    longurl = url.longurl

    ip = get_user_ip(request)

    long_url_obj = db_repo.get({'longurl': longurl, 'user_ip_address': ip})

    if long_url_obj:
        long_url_obj.shorturl = SHORTENED_URLS + long_url_obj.shorturl
        return long_url_obj

    shorturl = get_short_url(db_repo)

    shortened_url_obj = models.UrlShortener(longurl=longurl, shorturl=shorturl, user_ip_address=ip)
    shortened_url_obj = db_repo.add(shortened_url_obj)
    shortened_url_obj.shorturl = SHORTENED_URLS + shorturl
    return shortened_url_obj


@application.get('/shorten/{shorturl}')
async def redirect_shorturl(shorturl: str, db=Depends(get_db_connection)) -> RedirectResponse:
    db_connection = SqlAlchemyRepository(db)
    redirect_link = db_connection.get({'shorturl': shorturl})
    return RedirectResponse(url=redirect_link.longurl, status_code=301)


@application.get('/the-most-popular/')
def get_the_most_popular(db=Depends(get_db_connection)) -> models.UrlShortener:
    db_connection = SqlAlchemyRepository(db)
    data = db_connection.annotate({})
    result = []
    for pair in data:
        count, url = pair
        r = {"count": count, "url": url}
        result.append(r)

    return result


@application.get('/shortened-urls-count/')
def get_count_all_shortened_url(db=Depends(get_db_connection)) -> JSONResponse:
    db_connection = SqlAlchemyRepository(db)
    count = db_connection.count()
    return JSONResponse(content=jsonable_encoder({'count': count}))
