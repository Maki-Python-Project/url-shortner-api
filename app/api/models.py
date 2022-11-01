import sqlalchemy

from api.database import metadata


urlshortener = sqlalchemy.Table(
    "urlshortener",
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True, index=True),
    sqlalchemy.Column('user_ip_address', sqlalchemy.String, index=True, default='127.0.0.0'),
    sqlalchemy.Column('longurl', sqlalchemy.String, index=True),
    sqlalchemy.Column('shorturl', sqlalchemy.String, index=True),
)
