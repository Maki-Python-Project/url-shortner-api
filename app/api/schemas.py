from pydantic import BaseModel


class UrlShortenerBase(BaseModel):
    longurl: str

    class Config:
        orm_mode = True


class UrlShortenerCreate(UrlShortenerBase):
    pass


class UrlShortenerInsert(UrlShortenerBase):
    shorturl: str
    user_ip_address: str


class UrlShortener(UrlShortenerBase):
    id: int
    shorturl: str

    class Config:
        orm_mode = True
