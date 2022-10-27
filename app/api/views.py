import os

from fastapi import Request, Depends
from fastapi.responses import JSONResponse, RedirectResponse

from api.apps import application
from api.models import UrlShortener, Base
from api.utils import get_user_ip, get_short_url, get_db_connection
from api.database import engine


HOST_URL = os.environ.get('HOST_URL')

Base.metadata.create_all(bind=engine)


@application.post('/shorten/')
async def create_shorturl(url: UrlShortener, request: Request) -> JSONResponse:
    db_connection = get_db_connection()
    longurl = url.longurl

    ip = get_user_ip(request)

    long_url_obj = db_connection.get_one({'longurl': longurl, 'user_ip_address': ip})

    async for obj in long_url_obj:
        return JSONResponse({'longurl': obj.longurl, 'shorturl': HOST_URL + obj.shorturl})

    shorturl = await get_short_url(db_connection)

    db_connection.add({'longurl': longurl, 'shorturl': shorturl, 'user_ip_address': ip})
    shorturl = HOST_URL + shorturl

    return JSONResponse({'longurl': longurl, 'shorturl': shorturl})


@application.get('/shorten/{shorturl}')
async def redirect_shorturl(shorturl: str) -> RedirectResponse:
    db_connection = get_db_connection()
    redirect_link = db_connection.get_one({'shorturl': shorturl})
    return RedirectResponse(url=redirect_link.longurl, status_code=301)


@application.get('/the-most-popular/')
def get_the_most_popular() -> UrlShortener:
    db_connection = get_db_connection()
    data = db_connection.annotate({'$group': {'_id': '$longurl', 'count': {'$sum': 1}}}, {'$sort': {'count': -1}})
    return JSONResponse(data)


@application.get('/shortened-urls-count/')
def get_count_all_shortened_url(db=Depends(get_db_connection)) -> JSONResponse:
    db_connection = db
    data = db_connection.count()
    return JSONResponse({'count': data})
