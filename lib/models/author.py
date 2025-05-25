# lib/models/author.py
from lib.models.base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from lib.models.article import Article


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    articles = relationship(Article, back_populates="author")

    def __repr__(self):
        return f"<Author(name = '{self.name}')>"
