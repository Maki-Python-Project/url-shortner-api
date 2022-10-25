from pydantic import BaseModel
from ipaddress import IPv4Address


class UrlShortener(BaseModel):
    id: int
    user_ip_address: IPv4Address
    longurl: str
    shorturl: str
