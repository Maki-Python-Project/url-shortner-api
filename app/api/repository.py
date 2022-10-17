from api.models import UrlShortener
from typing import List


class AbstractRepository:
    def add(self, task: UrlShortener) -> None:
        raise NotImplementedError

    def get(self, reference: dict) -> UrlShortener:
        raise NotImplementedError

    def list_all(self) -> List(UrlShortener):
        raise NotImplementedError

    def annotate(self, reference: dict) -> List(UrlShortener):
        raise NotImplementedError

    def order_by(self, reference: dict) -> List(UrlShortener):
        raise NotImplementedError
