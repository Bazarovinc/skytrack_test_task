from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://skytrack_test_task:skytrack@localhost:5432/skytrack_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_database():
    database = session_local()
    try:
        yield database
    except:
        database.close()
