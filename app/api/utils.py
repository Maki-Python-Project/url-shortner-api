from pymongo import CursorType


def convert_cursor_to_dict(data: CursorType) -> dict:
    dict_data = {}
    dict_data = {item['_id']: item for item in data}
    return dict_data
