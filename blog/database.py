import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URL = 'sqlite:///' + os.path.join(basedir, 'data.db')

engine = create_engine(SQLALCHEMY_DATABASE_URL)
db = scoped_session(sessionmaker(
    bind=engine, autocommit=False, autoflush=False))
