from pydantic import BaseModel


class UrlShortenerBase(BaseModel):
    longurl: str

    class Config:
        orm_mode = True


class UrlShortenerCreate(UrlShortenerBase):
    pass


class UrlShortener(UrlShortenerBase):
    id: int
    shorturl: str

    class Config:
        orm_mode = True


class UrlShortenerAdmin(UrlShortener):
    user_ip_address: str
