from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import src.config.config as config

__engine = create_engine("postgresql://{}:{}@{}:{}/{}".format(
    config.USERNAME,
    config.PASSWORD,
    config.HOST,
    config.PORT,
    config.DATABASE
), encoding = "utf-8", echo = True)

__db_session = sessionmaker(__engine)

Base = declarative_base()

def get_session():
    session = __db_session()
    try:
        yield session
    finally:
        session.close()