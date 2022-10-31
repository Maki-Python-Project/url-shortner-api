import os

import databases

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_DATABASE_URL = os.environ.get('SQL_URI')

database = databases.Database(SQLALCHEMY_DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()
