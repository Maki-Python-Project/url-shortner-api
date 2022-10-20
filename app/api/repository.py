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


class MongoRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, dict_data):
        self.session.Url.insert_one(dict_data)

    def get_one(self, dict_data):
        return self.session.Url.find_one(dict_data)

    def annotate(self, group_dict, sort_dict):
        return self.session.Url.aggregate([group_dict, sort_dict])

    def count(self):
        return self.session.Url.count()

    def delete(self, dict_data):
        return self.session.Url.delete_one(dict_data)