from typing import List

from api.models import UrlShortener


class AbstractRepository:
    def add(self, reference: dict) -> None:
        raise NotImplementedError

    def get_one(self, reference: dict) -> UrlShortener:
        raise NotImplementedError

    def annotate(self, reference: dict) -> List[UrlShortener]:
        raise NotImplementedError

    def count(self, reference: dict) -> List[UrlShortener]:
        raise NotImplementedError

    def delete(self, reference: dict) -> List[UrlShortener]:
        raise NotImplementedError


class PostgresRepository(AbstractRepository):
    def __init__(self, session) -> None:
        self.session = session

    def add(self, reference: dict) -> None:
        pass

    def get_one(self, reference: dict) -> UrlShortener:
        pass

    def annotate(self, reference: dict) -> List[UrlShortener]:
        pass

    def count(self, reference: dict) -> List[UrlShortener]:
        pass

    def delete(self, reference: dict) -> List[UrlShortener]:
        pass
