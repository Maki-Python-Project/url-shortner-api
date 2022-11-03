import random
import string
from collections.abc import Callable

import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture()
def create_hash() -> str:
    hash = string.ascii_uppercase + string.ascii_lowercase + string.digits
    shorturl = ''.join(random.sample(hash, 8))

    return shorturl


@pytest.fixture()
def create_longurl_and_shorturl(create_hash: Callable) -> str:
    longurl = 'https://www.amazon.com/'
    shorturl = create_hash
    return longurl, shorturl
