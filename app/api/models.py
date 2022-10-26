from sqlalchemy import Column, Integer, String

from .database import Base


class UrlShortener(Base):
    __tablename__ = "urlshortener"
    id = Column(Integer, primary_key=True, index=True)
    user_ip_address = Column(String, index=True, default='127.0.0.0')
    longurl = Column(String, index=True)
    shorturl = Column(String(8), index=True)
