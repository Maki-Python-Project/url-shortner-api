from typing import List
from sqlalchemy import func

from api.models import UrlShortener


class AbstractRepository:
    def add(self, reference: dict) -> None:
        raise NotImplementedError

    def get(self, reference: dict) -> UrlShortener:
        raise NotImplementedError
    
    def filter(self, reference: dict) -> UrlShortener:
        raise NotImplementedError

    def annotate(self, reference: dict) -> List[UrlShortener]:
        raise NotImplementedError

    def count(self, reference: dict) -> List[UrlShortener]:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session) -> None:
        self.session = session

    def add(self, reference: str) -> None:
        self.session.add(reference)

    def get(self, reference: str) -> UrlShortener:
        return self.session.query(UrlShortener).filter_by(reference=reference).one()

    def filter(self, reference: str) -> UrlShortener:
        return self.session.query(UrlShortener).filter_by(reference=reference)

    def annotate(self, reference: str) -> List[UrlShortener]:
        return self.session.query(
            func.count(UrlShortener.reference), UrlShortener.reference
        ).group_by(UrlShortener.reference)

    def count(self) -> List[UrlShortener]:
        return self.session.query(UrlShortener).all().count()
