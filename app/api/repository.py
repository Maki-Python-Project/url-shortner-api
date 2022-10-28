from typing import List

from sqlalchemy import func
from sqlalchemy.orm import Session

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
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, reference: UrlShortener) -> UrlShortener:
        self.session.add(reference)
        self.session.commit()
        self.session.refresh(reference)
        return reference

    def get(self, reference: dict) -> UrlShortener:
        return self.session.query(UrlShortener).filter_by(**reference).first()

    def filter(self, reference: dict) -> UrlShortener:
        return self.session.query(UrlShortener).filter_by(**reference).all()

    def annotate(self, reference: dict) -> List[UrlShortener]:
        return (
            self.session.query(func.count(UrlShortener.id), UrlShortener.longurl).group_by(UrlShortener.longurl).all()
        )

    def count(self) -> List[UrlShortener]:
        return self.session.query(func.count(UrlShortener.id)).scalar()
