from api.models import UrlShortener
from typing import List


class AbstractRepository:
    def add(self, task: UrlShortener) -> None:
        raise NotImplementedError

    def get(self, reference: dict) -> UrlShortener:
        raise NotImplementedError

    def get_one(self, reference: dict) -> UrlShortener:
        raise NotImplementedError

    def list_all(self) -> List[UrlShortener]:
        raise NotImplementedError

    def annotate(self, reference: dict) -> List[UrlShortener]:
        raise NotImplementedError

    def order_by(self, reference: dict) -> List[UrlShortener]:
        raise NotImplementedError

    def count(self, reference: dict) -> List[UrlShortener]:
        raise NotImplementedError


class MongoRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, dict_data):
        self.session.db.products.insert(dict_data)

    def get(self, dict_data):
        return self.session.Url.find(dict_data)

    def get_one(self, dict_data):
        return self.session.Url.find_one(dict_data)

    def list_all(self):
        return self.session.Url.find()

    def annotate(self, group_dict, sort_dict):
        return self.session.Url.aggregate([group_dict, sort_dict])

    def order_by(self, dict_data):
        return self.session.Url.find().sort(dict_data)

    def count(self):
        return self.session.Url.count()
