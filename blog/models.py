from datetime import datetime
import bcrypt
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow())

    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.hashpw(
            password.encode(), bcrypt.gensalt(12))

    def is_correct_password(self, candidate_password):
        return bcrypt.checkpw(candidate_password.encode(), self.password)

    def to_json(self):
        return {"name": self.username}

    def __repr__(self):
        return "<User {}>".format(self.username)


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, onupdate=datetime.utcnow())

    user = relationship('User')
