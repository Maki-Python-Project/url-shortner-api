import os

import databases
from sqlalchemy import MetaData, create_engine

SQLALCHEMY_DATABASE_URL = os.environ.get('SQL_URI')

database = databases.Database(SQLALCHEMY_DATABASE_URL)
metadata = MetaData()
engine = create_engine(SQLALCHEMY_DATABASE_URL)
